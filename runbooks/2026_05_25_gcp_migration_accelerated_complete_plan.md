---
name: gcp-engine-migration-accelerated-2026-05-25
description: "ACCELERATED migration plan — move all 4 misplaced platform engines (decision-engine + intelligence-silo + gigaton-engine + sales-operating-system) + their Cloud SQL instances from `carmen-beach-properties` GCP project to `gigaton-platform` in ONE INTENSE WEEKEND (3-4 days operator-attended), not the 90-day phased schedule originally proposed in [[gcp_project_organization_target_2026]]. Reversible at every step. Lowest-blast-radius first. Rollback path preserved for 7 days post-cutover."
metadata:
  node_type: memory
  type: project
  established: 2026-05-25
  status: ACTIVE — execution plan; NOT yet started
  serves: foundational_modular_replication_via_input_substitution + universal_connector_hub_architecture
  ppim_interaction: every platform engine relocates; zero operator-facing behavior change
  ppim_economics: ~$20/mo savings post-cutover (consolidated Cloud SQL min-instances + cross-project egress elimination); $30-50k operator-onboarding speedup (new operators no longer touch carmen-beach billing/IAM scope)
  ppim_predictability: HIGH — reversible at every step; 7-day rollback window preserved
  ppim_brand_dimension: operational integrity + boundary clarity
  lifecycle_state: active
  state_set_at: 2026-05-25
  originSessionId: this-session
---

# Accelerated GCP Engine Migration — Carmen-Beach → Gigaton-Platform

## TL;DR

Original plan ([[gcp_project_organization_target_2026]]) phased this across 90 days: 30d intel-silo → 60-90d the rest. **The user wants ALL platform engines consolidated ASAP.** This plan compresses the same work into ~3-4 calendar days (~12-16 hours operator-attended), preserving the same reversibility guarantees.

**4 services + 2 Cloud SQL instances + 8 secrets + 5 IAM SAs migrate in this window.** Old infrastructure stays alive for 7 days as rollback safety net.

## What moves

| Today (carmen-beach-properties) | Target (gigaton-platform) | Notes |
|---|---|---|
| Cloud Run: `decision-engine` (rev `00039-s27`) | Cloud Run: `decision-engine` | Highest fan-in; many engines call it. Migrate LAST. |
| Cloud Run: `intelligence-silo` | Cloud Run: `intelligence-silo` | Memory + Documentation Ingest. Resumable jobs. SECOND. |
| Cloud Run: `gigaton-engine` | Cloud Run: `gigaton-engine` | Pricing service. Lowest blast radius. FIRST. |
| Cloud Run: `sales-operating-system` | Cloud Run: `sales-operating-system` | Sales catalog + intake. THIRD. |
| Cloud SQL: `decision-engine-pg` (POSTGRES_15) | Cloud SQL: `decision-engine-pg` | Carries 002/003/004 migrations |
| Cloud SQL: `intelligence-silo-pg` (POSTGRES_15) | Cloud SQL: `intelligence-silo-pg` | Carries 001 (EO) + 030 (doc ingest) + 031 (onboarding state) |
| Secret: `decision-engine-pg-app-pw` | Secret: same name | mirror |
| Secret: `decision-engine-pg-root-pw` | Secret: same name | mirror |
| Secret: `intelligence-silo-pg-app-pw` | Secret: same name | mirror |
| Secret: `intelligence-silo-pg-root-pw` | Secret: same name | mirror |
| (any LLM API keys used by these engines) | mirror | check `gcloud secrets list` filter |
| SA: `decision-engine-runtime@carmen-beach-properties.iam` | SA: `decision-engine-runtime@gigaton-platform.iam` | new SA in gigaton-platform |
| SA: `intel-silo-runtime@carmen-beach-properties.iam` | SA: `intel-silo-runtime@gigaton-platform.iam` | new SA |
| SA: `gigaton-engine-runtime@carmen-beach-properties.iam` | SA: `gigaton-engine-runtime@gigaton-platform.iam` | new SA |
| SA: `sales-os-runtime@carmen-beach-properties.iam` | SA: `sales-os-runtime@gigaton-platform.iam` | new SA |
| Cloud Run Job: `drift-sentinel-scan` | Cloud Run Job: `drift-sentinel-scan` | re-create in gigaton-platform |
| Cloud Scheduler triggers (codification + override + drift sweeps) | re-point to new URLs | metadata-only update |

## What stays in carmen-beach-properties (correctly)

- `Carmen-Beach-Properties` monorepo Cloud Run services (action-orchestrator, calibration-service, etc.)
- `mimi-whatsapp`
- `connector-api`
- `carmen-beach-db` Cloud SQL
- `sie-postgres-production` Cloud SQL (sovereign-influence-engine; consider promoting to gigaton-platform LATER but not in this window)

## Compressed schedule

**Day 0 (preflight, 2 hours):**
- Refresh gcloud auth (`gcloud auth login` + `gcloud auth application-default login`)
- Verify Cloud SQL backups exist on both source instances; trigger fresh on-demand backup
- Provision destination Cloud SQL instances in gigaton-platform (provision time ~10 min each, parallelizable)
- Create 4 new runtime SAs in gigaton-platform with required IAM grants
- Mirror 8+ secrets from carmen-beach-properties → gigaton-platform

**Day 1 (gigaton-engine + intel-silo, ~5 hours):**
- pg_dump intelligence-silo-pg → pg_restore to new instance (~30 min)
- Deploy gigaton-engine to gigaton-platform (no DB; simplest)
- Deploy intelligence-silo to gigaton-platform (with new INSTANCE_CONNECTION_NAME)
- Update gateway routing_table.py URLs for both engines + redeploy gateway
- Smoke chain: gateway `/v1/onboarding/manifest` + `/state` should still resolve (proves intel-silo cutover worked)
- Soak 2 hours; if green, decommission OLD gigaton-engine + intel-silo Cloud Run services (keep DB + image cache alive 7 days)

**Day 2 (sales-OS + decision-engine, ~5 hours):**
- Deploy sales-OS to gigaton-platform; update gateway routing
- pg_dump decision-engine-pg → pg_restore (carries migrations 002+003+004; ~30 min)
- Deploy decision-engine to gigaton-platform; update gateway routing
- Update ppeme `PENROSE_SCOREBOARD_URL` env var to new decision-engine URL + redeploy ppeme
- Re-create `drift-sentinel-scan` Cloud Run Job in gigaton-platform; re-point Cloud Scheduler
- Smoke: 5-command chain from [[onboarding_workflow_v1_completion_verified_2026_05_22]] + decision-engine Penrose endpoints + drift_critical_count metric

**Day 3 (verification + cleanup, ~2 hours):**
- Full 5-command verification chain GREEN
- Browser smoke verifying nothing visibly changed for operators
- Cloud Scheduler audit — every job points at the new URLs
- Update `[[repo_registry]]` URL suffixes from `-rjmcrtvuzq-uc.a.run.app` → `-sqatlxhlza-uc.a.run.app`
- Update each repo's `cloudbuild.yaml` to deploy to gigaton-platform going forward (so future PRs land in the right place)

**Day 4-10 (soak, automated):**
- 7-day soak with OLD infrastructure preserved
- Monitor: Penrose `drift_critical_count`, Cloud Run error rates, Cloud SQL connection counts
- If anything regresses, rollback via gateway routing_table flip (instant) + ppeme env var revert + Cloud Scheduler re-point

**Day 11 (final decommission, ~30 min):**
- Delete old Cloud Run services
- Delete old Cloud SQL instances + secrets
- Update `[[gcp_project_organization_target_2026]]` status to COMPLETE
- Total elapsed: ~12 calendar days; ~14 operator-attended hours

## Step-by-step procedure (per engine)

The pattern repeats per engine. Detailed for `gigaton-engine` (simplest), templated for the others.

### Per-engine migration template

```bash
# ──────────────────────────────────────────────────────────────────
# Variables (set per engine)
# ──────────────────────────────────────────────────────────────────
ENGINE=gigaton-engine             # or intelligence-silo / decision-engine / sales-operating-system
SOURCE_PROJECT=carmen-beach-properties
DEST_PROJECT=gigaton-platform
REGION=us-central1
SOURCE_URL_SUFFIX=rjmcrtvuzq      # the carmen-beach Cloud Run URL hash
DEST_URL_SUFFIX=sqatlxhlza        # the gigaton-platform Cloud Run URL hash

# ──────────────────────────────────────────────────────────────────
# 1. Pre-cutover: confirm current source state
# ──────────────────────────────────────────────────────────────────
gcloud run services describe $ENGINE \
  --project=$SOURCE_PROJECT --region=$REGION \
  --format='value(status.latestReadyRevisionName,status.url)'

# Note the current rev — that's your rollback anchor

# ──────────────────────────────────────────────────────────────────
# 2. Create runtime SA in gigaton-platform (one-time per engine)
# ──────────────────────────────────────────────────────────────────
RUNTIME_SA=$ENGINE-runtime
gcloud iam service-accounts create $RUNTIME_SA \
  --project=$DEST_PROJECT \
  --display-name="$ENGINE runtime"

# Grant required roles (adjust per engine — check cloudbuild.yaml for what it needs)
for role in cloudsql.client secretmanager.secretAccessor datastore.user pubsub.editor; do
  gcloud projects add-iam-policy-binding $DEST_PROJECT \
    --member=serviceAccount:$RUNTIME_SA@$DEST_PROJECT.iam.gserviceaccount.com \
    --role=roles/$role
done

# ──────────────────────────────────────────────────────────────────
# 3. Mirror secrets (per engine — list what cloudbuild.yaml --set-secrets references)
# ──────────────────────────────────────────────────────────────────
for SECRET in db-app-pw db-root-pw; do
  # Pull from source
  gcloud secrets versions access latest \
    --secret=$ENGINE-pg-$SECRET --project=$SOURCE_PROJECT \
    > /tmp/secret-$SECRET.txt
  # Create in dest
  gcloud secrets create $ENGINE-pg-$SECRET --project=$DEST_PROJECT \
    --replication-policy=automatic \
    --data-file=/tmp/secret-$SECRET.txt 2>/dev/null || \
  gcloud secrets versions add $ENGINE-pg-$SECRET --project=$DEST_PROJECT \
    --data-file=/tmp/secret-$SECRET.txt
  # Grant runtime SA access
  gcloud secrets add-iam-policy-binding $ENGINE-pg-$SECRET \
    --project=$DEST_PROJECT \
    --member=serviceAccount:$RUNTIME_SA@$DEST_PROJECT.iam.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
  rm /tmp/secret-$SECRET.txt
done

# ──────────────────────────────────────────────────────────────────
# 4. Provision destination Cloud SQL (if engine has one)
# ──────────────────────────────────────────────────────────────────
gcloud sql instances create $ENGINE-pg \
  --project=$DEST_PROJECT \
  --region=$REGION \
  --database-version=POSTGRES_15 \
  --tier=db-f1-micro \
  --root-password="$(gcloud secrets versions access latest --secret=$ENGINE-pg-root-pw --project=$DEST_PROJECT)"

# Create the application DB
gcloud sql databases create ${ENGINE//-/_} \
  --instance=$ENGINE-pg --project=$DEST_PROJECT

# Create the app user
gcloud sql users create ${ENGINE//-/_} \
  --instance=$ENGINE-pg --project=$DEST_PROJECT \
  --password="$(gcloud secrets versions access latest --secret=$ENGINE-pg-app-pw --project=$DEST_PROJECT)"

# ──────────────────────────────────────────────────────────────────
# 5. Dump → Restore (in two terminals or sequentially)
# ──────────────────────────────────────────────────────────────────
# Terminal A: source proxy
cloud-sql-proxy $SOURCE_PROJECT:$REGION:$ENGINE-pg --port 5433 &
SOURCE_PROXY_PID=$!

# Terminal B: dest proxy
cloud-sql-proxy $DEST_PROJECT:$REGION:$ENGINE-pg --port 5434 &
DEST_PROXY_PID=$!

sleep 4

# Dump from source
SRC_PW="$(gcloud secrets versions access latest --secret=$ENGINE-pg-root-pw --project=$SOURCE_PROJECT)"
PGPASSWORD="$SRC_PW" pg_dump -h localhost -p 5433 -U postgres \
  -d ${ENGINE//-/_} \
  --format=custom \
  --file=/tmp/$ENGINE.dump

# Restore to dest
DST_PW="$(gcloud secrets versions access latest --secret=$ENGINE-pg-root-pw --project=$DEST_PROJECT)"
PGPASSWORD="$DST_PW" pg_restore -h localhost -p 5434 -U postgres \
  -d ${ENGINE//-/_} \
  --no-owner --no-acl \
  /tmp/$ENGINE.dump

# Verify row counts match between source + dest
PGPASSWORD="$SRC_PW" psql -h localhost -p 5433 -U postgres -d ${ENGINE//-/_} \
  -c "\dt+" | tee /tmp/src-tables.txt
PGPASSWORD="$DST_PW" psql -h localhost -p 5434 -U postgres -d ${ENGINE//-/_} \
  -c "\dt+" | tee /tmp/dst-tables.txt
diff /tmp/src-tables.txt /tmp/dst-tables.txt
# Differences should be ZERO except for owner column (which is fine — set --no-owner)

# Re-apply ALTER DEFAULT PRIVILEGES so future tables in this DB auto-grant to app user
PGPASSWORD="$DST_PW" psql -h localhost -p 5434 -U postgres -d ${ENGINE//-/_} <<SQL
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ${ENGINE//-/_};
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ${ENGINE//-/_};
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO ${ENGINE//-/_};
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT USAGE, SELECT ON SEQUENCES TO ${ENGINE//-/_};
SQL

kill $SOURCE_PROXY_PID $DEST_PROXY_PID
rm /tmp/$ENGINE.dump

# ──────────────────────────────────────────────────────────────────
# 6. Update repo's cloudbuild.yaml — change PROJECT_ID + SA reference
# ──────────────────────────────────────────────────────────────────
cd ~/Documents/GitHub/$ENGINE
git checkout -b chore/migrate-to-gigaton-platform
# Edit cloudbuild.yaml:
#   - $PROJECT_ID will resolve to gigaton-platform when deploy runs there
#   - --service-account=$RUNTIME_SA@$DEST_PROJECT.iam.gserviceaccount.com
#   - --add-cloudsql-instances=$DEST_PROJECT:$REGION:$ENGINE-pg
git commit -am "chore: migrate $ENGINE to gigaton-platform"
git push -u origin chore/migrate-to-gigaton-platform
gh pr create --title "chore: migrate $ENGINE to gigaton-platform" --body-file ./migration-pr-body.md
# Don't auto-merge yet — verify with manual gcloud builds submit first

# ──────────────────────────────────────────────────────────────────
# 7. Manual deploy to gigaton-platform (parallel to old service still serving)
# ──────────────────────────────────────────────────────────────────
gcloud builds submit --project=$DEST_PROJECT --config=cloudbuild.yaml .

# Verify new Cloud Run service is healthy
NEW_URL=$(gcloud run services describe $ENGINE --project=$DEST_PROJECT --region=$REGION --format='value(status.url)')
curl -s -o /dev/null -w "HTTP %{http_code}\n" $NEW_URL/health \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)"
# Expect HTTP 200

# ──────────────────────────────────────────────────────────────────
# 8. Cutover: update gateway routing_table.py
# ──────────────────────────────────────────────────────────────────
cd ~/Documents/GitHub/gigaton-gateway
git checkout -b chore/route-$ENGINE-to-gigaton-platform
# Edit api/routing_table.py:
#   - Change $ENGINE entry from https://$ENGINE-$SOURCE_URL_SUFFIX-uc.a.run.app
#                              to https://$ENGINE-$DEST_URL_SUFFIX-uc.a.run.app
git commit -am "chore: route $ENGINE to gigaton-platform"
git push -u origin chore/route-$ENGINE-to-gigaton-platform
gh pr create --title "chore: route $ENGINE to gigaton-platform" --body-file ./route-pr-body.md
gh pr merge --rebase --auto --delete-branch

# Gateway auto-deploys via GHA → traffic now hits new $ENGINE in gigaton-platform

# ──────────────────────────────────────────────────────────────────
# 9. Smoke after cutover
# ──────────────────────────────────────────────────────────────────
# Use the 5-command chain from [[onboarding_workflow_v1_completion_verified_2026_05_22]]
# Plus engine-specific smokes (Penrose scoreboard, doc ingest bundle, etc.)

# ──────────────────────────────────────────────────────────────────
# 10. Soak — leave OLD service running for 7 days
# ──────────────────────────────────────────────────────────────────
# Tag old Cloud Run service with deprecation marker
gcloud run services update $ENGINE \
  --project=$SOURCE_PROJECT --region=$REGION \
  --update-labels=deprecated-replaced-by=gigaton-platform-$ENGINE,deprecation-date=$(date +%Y-%m-%d)

# Set min-instances=0 on the old service so it doesn't keep warm idle (cost saving)
gcloud run services update $ENGINE \
  --project=$SOURCE_PROJECT --region=$REGION \
  --min-instances=0

# ──────────────────────────────────────────────────────────────────
# 11. After 7-day soak, decommission OLD infrastructure
# ──────────────────────────────────────────────────────────────────
# Cloud Run service
gcloud run services delete $ENGINE \
  --project=$SOURCE_PROJECT --region=$REGION --quiet

# Cloud SQL instance (after final backup confirmed)
gcloud sql backups create --instance=$ENGINE-pg --project=$SOURCE_PROJECT --description="pre-decommission-$(date +%Y%m%d)"
gcloud sql instances delete $ENGINE-pg --project=$SOURCE_PROJECT --quiet

# Secrets
for SECRET in db-app-pw db-root-pw; do
  gcloud secrets delete $ENGINE-pg-$SECRET --project=$SOURCE_PROJECT --quiet
done

# Runtime SA (carmen-beach-properties side; only after confirming nothing references it)
gcloud iam service-accounts delete $ENGINE-runtime@$SOURCE_PROJECT.iam.gserviceaccount.com \
  --project=$SOURCE_PROJECT --quiet
```

## Engine-specific addenda

### gigaton-engine (FIRST — Day 1 morning, ~1 hour)

- No application DB (pricing is read-only against shared state)
- Simplest migration; tests the pattern
- Only the runtime SA + Cloud Run cutover needed
- Validates that ppeme + decision-engine pricing-bridge calls still work after URL flip

### intelligence-silo (Day 1 afternoon, ~2 hours)

- Cloud SQL `intelligence-silo-pg` migrates with migrations 001 (EO) + 030 (doc ingest)
- Plus the SQLite self-applied tables for onboarding_workflow_state — these don't migrate (they're per-Cloud-Run-instance ephemeral); the new instance will auto-create on first request, same way the old one did
- **Carries connector OAuth tokens** in `oauth_tokens` table — operators won't need to re-connect Drive after migration since the tokens migrate with the DB
- Gateway route update: `intel-silo` entry
- Documentation Ingest UI at `/connectors/documentation` should continue working

### sales-operating-system (Day 2 morning, ~1.5 hours)

- Cloud SQL (if exists — check the repo)
- Sales catalog + intake flows
- Gateway route + any direct callers (operator-api in Carmen-Beach-Properties calls this)

### decision-engine (Day 2 afternoon, ~2.5 hours — HIGHEST FAN-IN)

- Cloud SQL `decision-engine-pg` migrates with 001+002+003+004
- **drift_history.db** file in the Docker image needs special handling — the file is baked into image at build time, so deploying to gigaton-platform builds a fresh image that pulls drift history from... actually that's already baked into the image per CLAUDE.md. Just confirm.
- **Cloud Run Job: drift-sentinel-scan** — currently lives in carmen-beach-properties. Re-create in gigaton-platform:

```bash
gcloud run jobs create drift-sentinel-scan \
  --project=gigaton-platform \
  --region=us-central1 \
  --image=gcr.io/gigaton-platform/decision-engine:latest \
  --service-account=decision-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
  --task-timeout=900s \
  --command=python --args=cli.py,drift-sentinel-scan
```

- **Cloud Scheduler triggers** for codification + override + drift sweeps — re-point to new URLs (or recreate as new Scheduler entries in gigaton-platform)
- **PPEME `PENROSE_SCOREBOARD_URL`** env var — must update on ppeme Cloud Run service AFTER decision-engine cutover

```bash
gcloud run services update ppeme \
  --project=gigaton-platform --region=us-central1 \
  --update-env-vars=PENROSE_SCOREBOARD_URL=https://decision-engine-sqatlxhlza-uc.a.run.app
```

## Rollback procedure (per engine, 30 seconds each)

The cutover happens at the gateway routing_table layer. To roll back:

```bash
cd ~/Documents/GitHub/gigaton-gateway
git revert <route-cutover-commit-sha>
git push
# Gateway auto-redeploys; traffic flips back to OLD service in carmen-beach-properties
```

Plus for decision-engine specifically:

```bash
gcloud run services update ppeme \
  --project=gigaton-platform --region=us-central1 \
  --update-env-vars=PENROSE_SCOREBOARD_URL=https://decision-engine-rjmcrtvuzq-uc.a.run.app
```

Since OLD services + DB stay alive for 7 days, rollback at any point during soak is one revert + 60-second redeploy.

## Critical risks + mitigations

| Risk | Mitigation |
|---|---|
| Operator-onboarding flow breaks mid-cutover | Smoke chain runs after each engine; rollback in <60 seconds |
| Documentation Ingest jobs in-flight when intel-silo cuts over | The `documentation_ingest_jobs` row carries `status='running'`; the worker is per-Cloud-Run-instance ephemeral. Jobs that were in-flight at cutover get orphaned → operator clicks "Sync now" again. Not catastrophic. |
| Cross-project IAM grants (during dual-running) | Verify `decision-engine-runtime@gigaton-platform` has been granted same Pub/Sub `gignet-orchestrator` publisher role that `decision-engine-runtime@carmen-beach-properties` has. Otherwise gignet events stop. |
| Cloud SQL data divergence during dump→restore window | Window is ~30 min; during this time, writes go to SOURCE only (since gateway still routes to old service). Restore captures a consistent point-in-time snapshot. No divergence. |
| Migration fatigue → mistakes at hour 10 | Strict per-engine pause-and-verify discipline. Don't start the next engine until previous one's smoke is green AND you've taken a 15-min break. |
| Drift sentinel breaks during migration | Drift_history.db is image-baked. New image carries it. The Cloud Run Job recreation is the only operational gesture. |
| `~/.claude/settings.json` allowlist may not include pg_dump | Add `Bash(pg_dump:*)` + `Bash(pg_restore:*)` to settings.json before starting. (cloud-sql-proxy + psql + gcloud secrets access already allowlisted.) |

## Per-day operator-attended checklist

Print this as a runbook. Cross off each item.

**Day 0 (preflight, evening of 2026-05-25 or whenever):**
- [ ] `gcloud auth login` + `gcloud auth application-default login`
- [ ] Add `Bash(pg_dump:*)` + `Bash(pg_restore:*)` to `~/.claude/settings.json` allowlist
- [ ] Trigger on-demand backup of both source Cloud SQL instances
- [ ] Verify backups completed (`gcloud sql backups list --instance=$INSTANCE`)
- [ ] Provision `decision-engine-pg` + `intelligence-silo-pg` in gigaton-platform (~10 min each, parallel)
- [ ] Create 4 runtime SAs in gigaton-platform with IAM grants
- [ ] Mirror 8 DB secrets (4 services × 2 secrets each)
- [ ] Mirror any other engine-specific secrets (LLM keys, scoreboard tokens)

**Day 1 (gigaton-engine + intel-silo, ~5 hours):**
- [ ] Engine 1: gigaton-engine — full migration + smoke + 2h soak
- [ ] Engine 2: intelligence-silo — pg_dump + restore + deploy + cutover + smoke
- [ ] Verify chat-first onboarding still works end-to-end (5-command chain)
- [ ] Verify Documentation Ingest UI loads + Drive account list returns

**Day 2 (sales-OS + decision-engine, ~5 hours):**
- [ ] Engine 3: sales-operating-system — migration + smoke
- [ ] Engine 4: decision-engine — pg_dump + restore + deploy + cutover
- [ ] Update ppeme `PENROSE_SCOREBOARD_URL` env var
- [ ] Re-create drift-sentinel-scan Cloud Run Job in gigaton-platform
- [ ] Re-point Cloud Scheduler triggers
- [ ] Full 5-command chain GREEN
- [ ] Penrose `drift_critical_count` metric still emits

**Day 3 (verification + repo updates, ~2 hours):**
- [ ] Update `[[repo_registry]]` URL suffixes
- [ ] Update each repo's CLAUDE.md if it references the old project
- [ ] Update each cloudbuild.yaml's `--project=` to gigaton-platform (PR each)
- [ ] Browser smoke at `https://gigaton-platform.web.app` — nothing should look different
- [ ] Open `[[gcp_project_organization_target_2026]]` and update status to MIGRATING

**Day 4-10 (automated soak):**
- [ ] Nightly Penrose scoreboard email/notification check
- [ ] Cloud Run error rate alert (set up in gigaton-platform monitoring)
- [ ] No regressions surface

**Day 11 (final decommission, ~30 min):**
- [ ] Delete 4 OLD Cloud Run services in carmen-beach-properties
- [ ] Delete 2 OLD Cloud SQL instances (after final backup)
- [ ] Delete 8 OLD secrets
- [ ] Update `[[gcp_project_organization_target_2026]]` status to COMPLETE
- [ ] Write `[[gcp_engine_migration_completed_2026_06_05]]` memory documenting final state
- [ ] Cost report: pre vs post Cloud Run + Cloud SQL spend

## Open prerequisites

- **gcloud auth** — `gcloud auth login` + `gcloud auth application-default login` must be fresh
- **GitHub Actions billing** — must be resolved (Wave 1's FE deploy failure was billing-related; same blocker affects every per-engine cloudbuild PR)
- **No active Claude sessions on any of the 4 source repos** — pre-flight `.cxguy-active-agent` check before each engine migration
- **User attended** — none of the cutover steps are safe for unattended automation

## Cross-references

- [[gcp_project_organization_target_2026]] — the 90-day plan this supersedes (status: superseded by this accelerated plan)
- [[repo_registry]] — anti-patterns #4 + #7 will be RESOLVED at end of this migration
- [[onboarding_workflow_v1_completion_verified_2026_05_22]] — 5-command verification chain used after each cutover
- [[session_handoff_2026_05_20_chat_first_onboarding]] — for the Dockerfile gotcha lesson (will recur during each cloudbuild.yaml change)
- [[feedback_directed_workflow_required_for_every_deploy]] — these are platform-internal migrations; operator-facing behavior should not change so no new directed workflow is needed
