# gigmcp-industry-sync — Runbook

**Service type:** Cloud Run Job (batch) + Cloud Scheduler (trigger)
**Project:** `gigaton-platform`
**Region:** `us-central1`
**Job name:** `gigmcp-industry-sync`
**Scheduler name:** `gigmcp-industry-sync-daily`
**Schedule:** `0 3 * * *` UTC (= 22:00 / 21:00 CT prior day depending on DST)
**Code home:** `master-knowledge-base/gigmcp/`
**Wave:** Stage 5 variance-aware self-healing — Wave 2 PR2 (depends on PR1 = decision-engine commit `a7f0d7b`)

## What this job does

Pulls canonical industry knowledge from the gigmcp-export Cloud Run service and upserts rows into `decision-engine`'s Postgres `industry_catalogs` table (Wave 1 migration 004). Those rows are the **baseline** that variance computation (PR1) compares operator submissions against — without this sync, operators get classified as "anomaly" against an empty/static seed catalog.

Per-run flow:

```
[03:00 UTC] Cloud Scheduler
        │ OIDC-signed POST
        ▼
[gigmcp-industry-sync Cloud Run Job]
        │
        ├─→ GET  {GIGMCP_EXPORT_URL}/industries        (index)
        ├─→ For each industry:
        │     GET  {GIGMCP_EXPORT_URL}/industries/{tag}
        │     validate + translate
        │     UPSERT into industry_catalogs
        │           (favor-newer on etag + source_updated_at;
        │            operator-submitted rows never overwritten)
        │
        ├─→ Emit metrics: custom.googleapis.com/gigmcp/sync/*
        └─→ Emit HME event: GigmcpSyncCompleted
```

## Verify-before-first-deploy items

1. **`gigmcp-export` Cloud Run service** must exist in `gigaton-platform`:
   ```bash
   gcloud run services list --project=gigaton-platform --filter='metadata.name:gigmcp' --format='value(metadata.name,status.url)'
   ```
   **As of 2026-05-25 it does NOT exist.** Stand it up (out of scope for this PR — design lives in `master-knowledge-base/gigmcp/export_service/` per spec) before flipping Cloud Scheduler to ENABLED.

2. **`gigmcp-sync-runtime` service account** must exist with these grants:
   ```bash
   PROJECT=gigaton-platform
   SA=gigmcp-sync-runtime@${PROJECT}.iam.gserviceaccount.com

   gcloud iam service-accounts create gigmcp-sync-runtime \
     --display-name="gigmcp industry-sync runtime" \
     --project=${PROJECT}

   # Read decision-engine PG password
   gcloud secrets add-iam-policy-binding decision-engine-pg \
     --member="serviceAccount:${SA}" \
     --role="roles/secretmanager.secretAccessor" \
     --project=${PROJECT}

   # Connect to Cloud SQL
   gcloud projects add-iam-policy-binding ${PROJECT} \
     --member="serviceAccount:${SA}" \
     --role="roles/cloudsql.client"

   # Invoke gigmcp-export (when it exists)
   gcloud run services add-iam-policy-binding gigmcp-export \
     --region=us-central1 \
     --member="serviceAccount:${SA}" \
     --role="roles/run.invoker" \
     --project=${PROJECT}

   # Emit custom metrics
   gcloud projects add-iam-policy-binding ${PROJECT} \
     --member="serviceAccount:${SA}" \
     --role="roles/monitoring.metricWriter"

   # Publish HME events (only if HME_EVENT_TOPIC is set on the job)
   gcloud pubsub topics add-iam-policy-binding gignet-orchestrator \
     --member="serviceAccount:${SA}" \
     --role="roles/pubsub.publisher" \
     --project=${PROJECT}
   ```

3. **`cloud-scheduler-runner` service account** must exist with `run.invoker` on the Job:
   ```bash
   PROJECT=gigaton-platform
   SCHED_SA=cloud-scheduler-runner@${PROJECT}.iam.gserviceaccount.com

   # (create if needed — already exists if AX-008 sweep is wired)
   gcloud iam service-accounts create cloud-scheduler-runner \
     --display-name="Cloud Scheduler invoker" \
     --project=${PROJECT}

   gcloud run jobs add-iam-policy-binding gigmcp-industry-sync \
     --region=us-central1 \
     --member="serviceAccount:${SCHED_SA}" \
     --role="roles/run.invoker" \
     --project=${PROJECT}
   ```

4. **Cloud SQL `gigaton-engine-pg`** must be in `gigaton-platform`. Pre-accelerated-migration it lives in `carmen-beach-properties`; the `_CLOUD_SQL_INSTANCE` substitution in `cloudbuild.yaml` must change with the migration window.

## Schedule rationale

| UTC | CT (DST) | CT (STD) | Job |
|---|---|---|---|
| 03:00 | 22:00 prior day | 21:00 prior day | **gigmcp-industry-sync (this job)** |
| 09:00 | 04:00 | 03:00 | AX-008 nightly drift sweep |

03:00 UTC was chosen to leave a 6-hour gap before AX-008 so the variance baselines are fresh by the time the drift sweep reads them. No production operator-facing peak overlaps either window.

## Idempotency + conflict resolution

- **Same etag re-run = zero writes.** The sync re-fetches the full payload but the favor-newer check no-ops when `source.etag` matches.
- **Operator submissions are sacred.** Rows with `submitted_by_user_id != GIGMCP_SENTINEL_UUID` (no `source` block in `catalog_json`) are NEVER overwritten. Counted as `preserved_operator`.
- **Older gigmcp snapshot loses to newer.** Compared on `source.source_updated_at` (string ISO timestamps — UTC required).

## Operating commands

### Trigger an ad-hoc run (smoke / backfill)

```bash
gcloud run jobs execute gigmcp-industry-sync \
  --region=us-central1 \
  --project=gigaton-platform \
  --wait
```

### Read sync metrics in Cloud Monitoring

Metric path: `custom.googleapis.com/gigmcp/sync/{key}` where key ∈ `{fetched, upserted, unchanged, preserved_operator, skipped_malformed, failed_industries, duration_sec}`.

```bash
gcloud monitoring time-series list \
  --filter='metric.type="custom.googleapis.com/gigmcp/sync/fetched"' \
  --interval-end-time=$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ) \
  --interval-start-time=$(date -u -v-25H +%Y-%m-%dT%H:%M:%SZ) \
  --project=gigaton-platform
```

### Inspect last-run rows

```bash
# Connect via cloud-sql-proxy first (same pattern as decision-engine migrations):
cloud_sql_proxy -instances=gigaton-platform:us-central1:gigaton-engine-pg=tcp:5432 &

psql "postgresql://decision_engine@localhost:5432/decision_engine" -c "
SELECT industry_slug,
       sub_vertical,
       (catalog_json->'source'->>'etag')           AS source_etag,
       (catalog_json->'source'->>'source_updated_at') AS source_updated_at,
       (catalog_json->'source'->>'fetched_at')     AS last_fetched_at,
       process_count,
       confidence_score
  FROM industry_catalogs
 WHERE operator_id = 'gigmcp:canonical'
 ORDER BY (catalog_json->'source'->>'fetched_at') DESC NULLS LAST
 LIMIT 20;
"
```

### Pause / resume Scheduler (most common rollback step)

```bash
gcloud scheduler jobs pause  gigmcp-industry-sync-daily --location=us-central1 --project=gigaton-platform
gcloud scheduler jobs resume gigmcp-industry-sync-daily --location=us-central1 --project=gigaton-platform
```

## Failure triage

| Symptom | First check | Likely cause | Remediation |
|---|---|---|---|
| Exit code 2 | Job env vars | `GIGMCP_EXPORT_URL` unset | Redeploy with substitution or set on the Job directly |
| Exit code 3 | Job logs `DB connect failed` | Cloud SQL connector / SA grant / secret | Verify SA has `cloudsql.client` + `secretmanager.secretAccessor` on `decision-engine-pg` |
| Exit code 4 | Job logs `index fetch failed` | gigmcp-export is down or wrong URL | `gcloud run services describe gigmcp-export --region=us-central1` |
| Exit code 1 (clean) | metric `fetched=0`, `failed_industries>0` | gigmcp returning 5xx per industry | Open gigmcp-export logs; pause Scheduler until resolved |
| `skipped_malformed>0` | HME `GigmcpSyncMalformed` events | gigmcp wire format drift | Update `translators/v1_to_industry_catalog.py` or add v2 translator |
| `preserved_operator > 0` (large fraction) | Expected if operators have hand-curated catalogs | not an error | None — confirm via `seed_for_industry` flag distribution |

## Rollback

1. **Pause Scheduler** (zero-blast-radius): `gcloud scheduler jobs pause gigmcp-industry-sync-daily ...`
2. **Roll back code:** revert the PR in `master-knowledge-base`, redeploy with the prior `$COMMIT_SHA` tag.
3. **Roll back bad data:** Wave 1 baselines are static; truncate gigmcp rows + replay Wave 1 seed:
   ```sql
   BEGIN;
   DELETE FROM industry_catalogs WHERE operator_id = 'gigmcp:canonical';
   COMMIT;
   ```
   Operator-submitted rows are untouched (different `operator_id`).
4. **Full teardown:** `gcloud run jobs delete gigmcp-industry-sync ...` + `gcloud scheduler jobs delete gigmcp-industry-sync-daily ...`. PR1 (variance) and PR3 (FE) continue working against the Wave 1 static seed.

## Beta-MVP acceptance

1. Cloud Run Job `gigmcp-industry-sync` deployed in `gigaton-platform`; manual `gcloud run jobs execute` exits 0.
2. First sync run produces non-zero rows: `SELECT count(DISTINCT industry_slug) FROM industry_catalogs WHERE operator_id = 'gigmcp:canonical' AND catalog_json->'source'->>'etag' IS NOT NULL` ≥ 3.
3. Cloud Scheduler `gigmcp-industry-sync-daily` exists, status = ENABLED, next-run-time within 24h.
4. All `gigmcp/tests/` tests pass in CI; HME `GigmcpSyncCompleted` event observed in HME event store after the manual smoke run.

## Cross-links

- Wave 1 schema: `decision-engine/migrations/004_industry_catalogs.sql`
- Wave 2 PR1 consumer: `decision-engine/engine/onboarding/variance/compute.py` (reads via `industry_catalog_row_id` soft ref)
- Wave 2 PR3 (FE): `gigaton-ui-system` — depends on at least one successful sync run before deploying
- Wave 2 spec: `~/.claude/projects/-Users-admin/memory/stage_5_variance_aware_self_healing_spec.md`
- Accelerated migration risk: `~/.claude/projects/-Users-admin/memory/gcp_engine_migration_accelerated_2026_05_25.md` (if migration moves `gigaton-engine-pg` mid-rollout, update `_CLOUD_SQL_INSTANCE` substitution + redeploy)
