# Deploy Runbook — Storage/Retrieval Path-to-100% — 2026-05-22

**Goal:** ship the 13 PRs from the 2026-05-21 audit + 1 backfill script + IAM/KMS hardening, get to ~95% on the structured-storage surface by EOD 2026-05-22.

**Author:** Claude (Opus 4.7) per Todd's "complete all in tandem by EOD tomorrow" directive
**Audit basis:** `/Users/admin/.claude/projects/-Users-admin/memory/api_reference_2026_05_19.md` + production state audit 2026-05-21

---

## P0 — PREREQ (do FIRST, blocks everything else)

```bash
# S17 — reauth gcloud (user-only, both user creds AND ADC expired as of 2026-05-22 morning)
gcloud auth login --account todd@gigaton.ai
gcloud auth application-default login
gcloud config set account todd@gigaton.ai
gcloud config set project gigaton-platform  # default for most commands

# Verify
gcloud auth list
gcloud auth application-default print-access-token | head -c 40 && echo " (ok)"
```

---

## Phase 1 — Merge 13 PRs (recommended order)

All 13 are `MERGEABLE` per `gh pr view`. CI is green on the 5 PRs in repos with CI configured (silo, decision-engine). ppeme/gateway/UAE have no PR-level CI configured — local tests pass; production smoke after deploy is the safety net.

### Merge order

| # | Repo | PR | Branch | Why this order |
|---|---|---|---|---|
| 1 | decision-engine | [#78](https://github.com/todd-gig/decision-engine/pull/78) | `chore/adopt-alembic` | Schema framework first; needs `alembic stamp` (step 2) |
| 2 | intelligence-silo | [#34](https://github.com/todd-gig/intelligence-silo/pull/34) | `feat/boot-gate-migrations` | Same: schema gate |
| 3 | gigaton-gateway | [#47](https://github.com/todd-gig/gigaton-gateway/pull/47) | `feat/aggregator-wire-mimi` | Edge wiring; mimi-whatsapp comes into aggregator |
| 4 | user-access-engine | [#35](https://github.com/todd-gig/user-access-engine/pull/35) | `feat/namespaces-auth-gate` | Auth gate; verify gateway proxy still passes admin tokens |
| 5 | ppeme | [#29](https://github.com/todd-gig/ppeme/pull/29) | `feat/coefficients-db` | Alembic 0008 — must merge BEFORE #30 to free up revision numbering |
| 6 | ppeme | [#30](https://github.com/todd-gig/ppeme/pull/30) | `feat/ctr-outcomes-ingest` | **REBASE FIRST:** set `down_revision = "0008_coefficients"` then push |
| 7 | ppeme | [#28](https://github.com/todd-gig/ppeme/pull/28) | `feat/bft-variable-mappings` | Independent; safe anytime after main is stable |
| 8 | intelligence-silo | [#35](https://github.com/todd-gig/intelligence-silo/pull/35) | `feat/experience-assembler-gcs` | Needs `EXPERIENCE_ASSEMBLY_BUCKET` env (see Phase 2.4) |
| 9 | intelligence-silo | [#37](https://github.com/todd-gig/intelligence-silo/pull/37) | `feat/gemini-omni-fail-soft` | S13; feature-flag default off, safe to merge anytime |
| 10 | decision-engine | [#79](https://github.com/todd-gig/decision-engine/pull/79) | `chore/backfill-execution-records-script` | Script only; prod-apply is step 7 (manual, gated) |

```bash
# Auto-merge each as CI clears (or squash-merge manually):
for pr in "todd-gig/decision-engine:78" "todd-gig/intelligence-silo:34" "todd-gig/gigaton-gateway:47" "todd-gig/user-access-engine:35" "todd-gig/ppeme:29"; do
  repo="${pr%:*}"; num="${pr#*:}"
  gh pr merge "$num" --repo "$repo" --squash --auto
done
# Then handle ppeme #30 rebase manually (see step 6 below), then:
for pr in "todd-gig/ppeme:30" "todd-gig/ppeme:28" "todd-gig/intelligence-silo:35" "todd-gig/intelligence-silo:37" "todd-gig/decision-engine:79"; do
  repo="${pr%:*}"; num="${pr#*:}"
  gh pr merge "$num" --repo "$repo" --squash --auto
done
```

### ppeme #30 pre-merge rebase

```bash
cd /Users/admin/Documents/GitHub/ppeme  # confirm via repo_registry
git fetch origin
git checkout feat/ctr-outcomes-ingest
git rebase origin/main  # picks up #29's 0008_coefficients
# Edit alembic/versions/0010_ctr_outcomes.py:
#   down_revision = "0008_coefficients"  (was "0007_experience_type_routings")
git add alembic/versions/0010_ctr_outcomes.py
git commit --amend --no-edit
git push --force-with-lease
```

---

## Phase 2 — Pre-Deploy Operator Actions

### 2.1 — S3: restore OPENAI_API_KEY secret binding on gateway

`/v1/llm/call` returns 503 for OpenAI provider until this is done. PR #45 reverted the binding due to wrong SA.

```bash
# Identify the runtime SA for gigaton-gateway (run after S17 reauth):
GATEWAY_SA=$(gcloud run services describe gigaton-gateway --project gigaton-platform --region us-central1 --format='value(spec.template.spec.serviceAccountName)')
echo "Gateway SA: $GATEWAY_SA"

# Grant secretmanager.secretAccessor on OPENAI_API_KEY:
gcloud secrets add-iam-policy-binding OPENAI_API_KEY \
  --project gigaton-platform \
  --member "serviceAccount:${GATEWAY_SA}" \
  --role roles/secretmanager.secretAccessor

# Re-apply PR #44 (the secret binding) — re-open as a new PR if #44 closed:
# Check first:
gh pr view 44 --repo todd-gig/gigaton-gateway --json state,title
# If closed: re-open or cherry-pick the binding commit into a new branch
```

### 2.2 — S2 alembic stamp (decision-engine)

After PR #78 merges, stamp prod DB at baseline BEFORE the next deploy (otherwise boot-gate will try to create existing tables):

```bash
# Open Cloud SQL proxy to decision-engine-pg:
gcloud sql connect decision-engine-pg --project carmen-beach-properties --user postgres &
# OR via proxy on 5432:
cloud-sql-proxy carmen-beach-properties:us-central1:decision-engine-pg --port 5432 &

# Stamp:
export DATABASE_URL="postgresql+psycopg2://decision_engine:${DB_PASSWORD}@127.0.0.1:5432/decision_engine"
cd /Users/admin/Documents/GitHub/decision-engine  # confirm via repo_registry
python3 -m alembic stamp 0001_baseline

# Verify:
python3 -m alembic current  # should print: 0001_baseline (head)
```

### 2.3 — ppeme require_admin env var

PR #29 introduces `require_admin` from scratch. `PPEME_ADMIN_TOKEN` must be set on the Cloud Run service env before deploy or `/v1/coefficients` CRUD returns 503.

```bash
# Generate a long admin token (store in Secret Manager):
ADMIN_TOKEN=$(openssl rand -hex 32)
echo -n "$ADMIN_TOKEN" | gcloud secrets create PPEME_ADMIN_TOKEN \
  --project gigaton-platform --data-file=- --replication-policy=automatic

# Grant ppeme SA accessor:
PPEME_SA=$(gcloud run services describe ppeme --project gigaton-platform --region us-central1 --format='value(spec.template.spec.serviceAccountName)')
gcloud secrets add-iam-policy-binding PPEME_ADMIN_TOKEN \
  --project gigaton-platform \
  --member "serviceAccount:${PPEME_SA}" \
  --role roles/secretmanager.secretAccessor

# Then in the ppeme deploy cloudbuild.yaml, ensure:
#   --set-secrets PPEME_ADMIN_TOKEN=PPEME_ADMIN_TOKEN:latest
```

### 2.4 — intel-silo EXPERIENCE_ASSEMBLY_BUCKET env

PR #35 fail-softs if the env is unset — but to actually upload, the bucket must exist:

```bash
# Create operator-scoped bucket:
gcloud storage buckets create gs://gigaton-experiences-prod \
  --project gigaton-platform --location us-central1 \
  --uniform-bucket-level-access

# Grant intel-silo SA write:
SILO_SA=$(gcloud run services describe intelligence-silo --project carmen-beach-properties --region us-central1 --format='value(spec.template.spec.serviceAccountName)')
gcloud storage buckets add-iam-policy-binding gs://gigaton-experiences-prod \
  --member "serviceAccount:${SILO_SA}" \
  --role roles/storage.objectAdmin

# Add to intel-silo deploy: --set-env-vars EXPERIENCE_ASSEMBLY_BUCKET=gigaton-experiences-prod
```

### 2.5 — UAE namespaces admin token

PR #35 hardens the soft gate. Verify `UAE_NAMESPACE_ADMIN_TOKEN` is already set in prod:

```bash
gcloud run services describe user-access-engine --project gigaton-platform --region us-central1 \
  --format='get(spec.template.spec.containers[0].env)' | grep -i namespace
# If not present: create + bind same pattern as 2.3
```

---

## Phase 3 — Deploy Window (19:00 CT)

Deploy in dependency order. Each service has its own Cloud Build pipeline triggered by main-branch push (so most of this is automatic IF PRs were merged via Phase 1's `--auto`).

Verify each deploy completes before moving on:

```bash
# Watch deploy:
gcloud builds list --project <proj> --ongoing --format='table(id,status,source.repoSource.repoName)'

# Or manual deploy if auto-trigger failed:
gcloud run deploy <service> --source . --project <proj> --region us-central1 ...
```

| Order | Service | Project | Verify command |
|---|---|---|---|
| 1 | decision-engine | carmen-beach-properties | `curl -s "$(gcloud run services describe decision-engine --project carmen-beach-properties --region us-central1 --format='value(status.url)')/health"` |
| 2 | intelligence-silo | carmen-beach-properties | same pattern + check `/openapi.json` for documentation_ingest routes |
| 3 | user-access-engine | gigaton-platform | check `/v1/namespaces` returns 401 unauthenticated (S6 gate) |
| 4 | ppeme | gigaton-platform | check `/v1/coefficients` returns 401 unauthenticated (S10 gate); check `/v1/forecasts/scenario` payload includes `ctr` field (S11) |
| 5 | gigaton-gateway | gigaton-platform | **critical:** `curl /v1/healthz` returns 11 engines all 200 |

---

## Phase 4 — S5 Backfill (Operator-Gated, Post-Deploy)

Only after Phase 3 verification passes. Runs decision-engine #79's script against prod DB.

```bash
cd /Users/admin/Documents/GitHub/decision-engine
git pull origin main

# Pilot: 10 rows
DATABASE_URL="postgresql://decision_engine:${DB_PASSWORD}@127.0.0.1:5432/decision_engine" \
  python3 scripts/backfill_execution_records.py \
  --start-date 2026-05-01 --end-date 2026-05-20 \
  --apply --limit 10

# Inspect output. If clean:
DATABASE_URL="..." python3 scripts/backfill_execution_records.py \
  --start-date 2026-05-01 --end-date 2026-05-20 \
  --apply --limit 10000

# Trigger AX-008 sweep + verify 0 new orphans:
gcloud run jobs execute sweep-executions-daily --project carmen-beach-properties --region us-central1 --wait
# Then check Penrose scoreboard:
curl -s "$(gcloud run services describe gigaton-gateway --project gigaton-platform --region us-central1 --format='value(status.url)')/v1/penrose/scoreboard"
```

---

## Phase 5 — Optional Hardening (S18 KMS, ~$1/key/mo)

Defer if time-constrained. Closes the "no KMS keyring in gigaton-platform" audit finding.

```bash
gcloud kms keyrings create gigaton-credentials \
  --project gigaton-platform --location global

gcloud kms keys create service-secrets-v1 \
  --keyring gigaton-credentials \
  --project gigaton-platform --location global \
  --purpose encryption

# Grant per-service SA `cloudkms.cryptoKeyEncrypterDecrypter` as needed.
```

---

## Rollback Playbook

Per `/Users/admin/.claude/projects/-Users-admin/memory/operator_runbook_2026_05_19.md`, the Cloud Run alembic_version cascade quirk:

```bash
# Rollback service to previous revision:
gcloud run services update-traffic <service> \
  --project <proj> --region us-central1 \
  --to-revisions <prev-revision>=100

# Rollback alembic (if S2 #78 or ppeme #29 #30 cause boot failures):
# Connect via cloud-sql-proxy, then:
python3 -m alembic downgrade -1
```

---

## Definition-of-Done Checklist

- [ ] All 13 PRs merged
- [ ] `alembic stamp 0001_baseline` run against decision-engine prod DB
- [ ] OPENAI_API_KEY secret bound on gateway, `/v1/llm/call` returns 200 with `provider=openai`
- [ ] gateway `/v1/healthz` reports 11/11 engines (mimi-whatsapp present)
- [ ] UAE `/v1/namespaces` returns 401 unauthenticated
- [ ] ppeme `/v1/coefficients` returns 401 unauthenticated; `/v1/forecasts/scenario` includes `ctr` field
- [ ] intel-silo migration tracker table `_silo_migrations` populated; documentation_ingest endpoints return 200
- [ ] decision-engine writes to `execution_records` on `/v1/decisions/process` POST
- [ ] S5 backfill run against prod, AX-008 sweep shows 0 new orphans
- [ ] Penrose scoreboard 8/8 metrics responsive

**Remaining gap (NOT closed by EOD 2026-05-22):**
- S7 + S8: relational `memory_items` + Lifecycle State Machine — 3-day sprint scheduled for week of 2026-05-25
- S19: per-engine Phase F observability dashboards — post-stabilization
