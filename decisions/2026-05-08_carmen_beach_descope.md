---
title: Decision — PDC descoped from 19:00 CT deploys until 2026-05-13 (Wed)
date: 2026-05-08
decided-by: Todd (operator)
applied-by: Claude in Cowork session
status: ACTIVE
revisits: 2026-05-13 (Wednesday) — re-add to deploy_19.sh after prereqs land
---

# Decision

`Carmen-Beach-Properties` is removed from `master-knowledge-base/scripts/deploy_19.sh`'s SERVICES array between 2026-05-08 and 2026-05-13. The other 6 services (decision-engine, gigaton-engine, sales-operating-system, intelligence-silo, sovereign-influence-engine, Gigaton-UI-Platform) deploy normally during this window.

Code was changed via comment-out (not deletion) so re-enabling on Wednesday is a single uncomment. The decoy PDC `gh_workflow` would have failed within ~13 seconds tonight and marked the whole run as failed — blocking tomorrow's preflight.

# Why

Carmen-Beach-Properties' `deploy-prod.yml` workflow needs GCP infrastructure and 6 GitHub Actions secrets that don't exist yet. **Setup time: ~30–60 min** (one-shot work) plus DNS for the production domain if going live. Doing it under deploy-window pressure tonight is high-risk; doing it Wednesday gives clean cycle.

# Prereq checklist (complete by 2026-05-13)

Reference: `Carmen-Beach-Properties/docs/DEPLOY.md`. Steps abridged below.

## A. GCP staging project + APIs

```
gcloud projects create carmen-beach-staging        # or pick existing
gcloud config set project carmen-beach-staging
gcloud services enable run.googleapis.com sqladmin.googleapis.com \
  secretmanager.googleapis.com artifactregistry.googleapis.com \
  containerregistry.googleapis.com
```

## B. Cloud SQL Postgres

```
gcloud sql instances create carmen-staging \
  --database-version=POSTGRES_15 --region=us-central1 \
  --tier=db-custom-1-3840 --storage-size=10GB
gcloud sql databases create carmen_beach --instance=carmen-staging
gcloud sql users create app --instance=carmen-staging --password=<random>
```

Connection-name format: `carmen-beach-staging:us-central1:carmen-staging`.

## C. Deploy service account `gh-deploy`

```
gcloud iam service-accounts create gh-deploy \
  --display-name="GitHub Actions Deploy"

for role in roles/run.admin roles/storage.admin roles/iam.serviceAccountUser \
            roles/cloudsql.client roles/secretmanager.secretAccessor; do
  gcloud projects add-iam-policy-binding carmen-beach-staging \
    --member="serviceAccount:gh-deploy@carmen-beach-staging.iam.gserviceaccount.com" \
    --role="$role"
done

gcloud iam service-accounts keys create gh-deploy-key.json \
  --iam-account=gh-deploy@carmen-beach-staging.iam.gserviceaccount.com
```

## D. Secret Manager values

Per environment (`_STAGING` and `_PROD` suffixes — repeat for prod project):

| Secret | Contents |
|---|---|
| `DATABASE_URL_STAGING` | `postgresql://app:<pwd>@/carmen_beach?host=/cloudsql/<instance>` |
| `AUTH_SECRET_STAGING` | `openssl rand -base64 32` |

Plus: any third-party secrets the app needs (Stripe keys, Sendgrid, Twilio, etc.) — confirm against the app code's `process.env.*` references before secrets-creation pass.

## E. GitHub Actions secrets on todd-gig/Carmen-Beach-Properties

```
gh secret set GCP_PROJECT_ID --body "carmen-beach-staging"
gh secret set GCP_SA_KEY     --body "$(cat gh-deploy-key.json)"
gh secret set GCP_CLOUDSQL_INSTANCE_STAGING --body "carmen-beach-staging:us-central1:carmen-staging"
gh secret set STAGING_DATABASE_URL --body "postgresql://app:<pwd>@/carmen_beach?host=/cloudsql/carmen-beach-staging:us-central1:carmen-staging"
# Repeat for prod env when ready:
gh secret set PROD_DATABASE_URL --body "..."
gh secret set GCP_CLOUDSQL_INSTANCE_PROD --body "..."
```

(After this: delete `gh-deploy-key.json` from disk.)

## F. Smoke-test the workflow before re-enabling

```
gh workflow run deploy-staging.yml --repo todd-gig/Carmen-Beach-Properties
# Watch:
gh run watch --repo todd-gig/Carmen-Beach-Properties --exit-status
```

If staging green → run `deploy-prod.yml` once manually to verify prod path before re-adding to deploy_19.sh.

## G. Re-enable in deploy_19.sh

In `master-knowledge-base/scripts/deploy_19.sh`, uncomment the line:
```
# "Carmen-Beach-Properties|$GH_ROOT/Carmen-Beach-Properties|gh_workflow"
```

Test with `--check` then a single-service run:
```
./scripts/deploy_19.sh --check
./scripts/deploy_19.sh Carmen-Beach-Properties
```

# What we lose during the descope window

- No PDC code reaches production this Friday or weekend
- The `add-chatgpt-snippets-carmen` and Phase-2/3 work merged today (PR #3, PR #4) sit unreleased until Wednesday — but: it sits on Bella's main and the staging-and-prod CI/CD config is now in place, so once secrets land it auto-deploys

# What we gain

- No spurious failed-deploy entries in `deploy-log.jsonl` blocking tomorrow's preflight
- Time to set up infra carefully without 19:00 CT pressure
- PDC can launch from a clean baseline on Wednesday

# Rollback (if you want PDC in tonight's deploy after all)

Edit `scripts/deploy_19.sh`, uncomment the Carmen-Beach-Properties row, and ensure prereqs are in place. Or run other 6 services tonight and PDC manually:
```
gh workflow run deploy-prod.yml --repo todd-gig/Carmen-Beach-Properties
```
