# Carmen-Beach → Gigaton-Platform Migration — Day-by-Day Runbook

**Authored:** 2026-05-25 Sun evening (Day 0)
**Operator:** todd@gigaton.ai
**Source plan:** [[gcp_engine_migration_accelerated_2026_05_25]] (in MEMORY.md)
**Day-0 snapshots:** `/Users/admin/Documents/GitHub/master-knowledge-base/runbooks/migration_day0_snapshots/`

## Scope

Migrating 4 engines: `decision-engine`, `intelligence-silo`, `gigaton-engine`, `sales-operating-system`.
NOT migrating: `connector-api` + `mimi-whatsapp` (tied to carmen-beach OAuth/Twilio per memory).

## Day 0 — TONIGHT 2026-05-25 (COMPLETE)

**Preflight: receiving infrastructure provisioned in gigaton-platform. Zero data/traffic impact.**

### Provisioned (all in `gigaton-platform`)

| Resource | Name | State (post-provision) |
| --- | --- | --- |
| Cloud SQL | `decision-engine-pg` | PENDING_CREATE → ~5min RUNNABLE |
| Cloud SQL | `intelligence-silo-pg` | PENDING_CREATE → ~5min RUNNABLE |
| Cloud SQL | `gigaton-engine-pg` | PENDING_CREATE → ~5min RUNNABLE (mirror of empty carmen instance) |
| Service Account | `decision-engine-runtime@gigaton-platform.iam.gserviceaccount.com` | CREATED |
| Service Account | `intel-silo-runtime@gigaton-platform.iam.gserviceaccount.com` | CREATED |
| Service Account | `gigaton-engine-runtime@gigaton-platform.iam.gserviceaccount.com` | CREATED |
| Service Account | `sales-os-runtime@gigaton-platform.iam.gserviceaccount.com` | CREATED |
| Secret | `decision-engine-pg-app-pw` (v1, mirrored) | CREATED |
| Secret | `intelligence-silo-pg-app-pw` (v1, mirrored) | CREATED |
| Secret | `google-drive-oauth-client` (v1, mirrored) | CREATED |
| Secret | `oauth-state-secret` (v1, mirrored) | CREATED |

**SQL instance config (matches carmen-beach):** POSTGRES_15, db-f1-micro, us-central1, 10GB SSD, backup-start 07:00 UTC, no deletion protection.

**Rollback Day 0:** delete the 3 new SQL instances + 4 SAs + 4 secrets. No traffic change occurred, so rollback is purely a clean-up exercise. Approx commands:
```
gcloud sql instances delete decision-engine-pg --project=gigaton-platform
gcloud sql instances delete intelligence-silo-pg --project=gigaton-platform
gcloud sql instances delete gigaton-engine-pg --project=gigaton-platform
for sa in decision-engine-runtime intel-silo-runtime gigaton-engine-runtime sales-os-runtime; do
  gcloud iam service-accounts delete ${sa}@gigaton-platform.iam.gserviceaccount.com --project=gigaton-platform
done
for s in decision-engine-pg-app-pw intelligence-silo-pg-app-pw google-drive-oauth-client oauth-state-secret; do
  gcloud secrets delete $s --project=gigaton-platform
done
```

---

## Day 1 — Tue 2026-05-26 evening (post-beta-launch) — decision-engine cutover

**Pre-req:** Multipli sprint shipped, beta launch validated, gateway healthy.

### Steps

1. **Verify new SQL ready + apply schema** (15 min)
   ```
   gcloud sql instances describe decision-engine-pg --project=gigaton-platform --format="value(state)"  # RUNNABLE
   # create app role + db inside the new instance
   gcloud sql users create decision_engine --instance=decision-engine-pg --project=gigaton-platform \
     --password="$(gcloud secrets versions access latest --secret=decision-engine-pg-app-pw --project=gigaton-platform)"
   gcloud sql databases create decision_engine --instance=decision-engine-pg --project=gigaton-platform
   ```
2. **Dump + restore data** (10 min for current decision-engine DB size)
   ```
   gcloud sql export sql decision-engine-pg gs://gigaton-migration-staging/decision-engine-pg-$(date -u +%Y%m%dT%H%M%SZ).sql.gz \
     --database=decision_engine --project=carmen-beach-properties
   gcloud sql import sql decision-engine-pg gs://gigaton-migration-staging/decision-engine-pg-<timestamp>.sql.gz \
     --database=decision_engine --project=gigaton-platform
   ```
   Note: bucket `gigaton-migration-staging` must exist in gigaton-platform with both SA's `objectAdmin` (see Day-N0 prep below).
3. **Grant SA permissions** (5 min)
   ```
   gcloud secrets add-iam-policy-binding decision-engine-pg-app-pw \
     --member=serviceAccount:decision-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
     --role=roles/secretmanager.secretAccessor --project=gigaton-platform
   gcloud projects add-iam-policy-binding gigaton-platform \
     --member=serviceAccount:decision-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
     --role=roles/cloudsql.client
   ```
4. **Deploy new Cloud Run service** in gigaton-platform pointed at new SQL, **but with no traffic** (5 min)
   - Copy image from carmen-beach Artifact Registry into gigaton-platform AR or grant cross-project pull.
   - Update `INSTANCE_CONNECTION_NAME=gigaton-platform:us-central1:decision-engine-pg`.
   - Keep `INTELLIGENCE_SILO_URL` pointed at carmen-beach until Day 2.
5. **Smoke test** the new revision via Cloud Run URL (`*-uc.a.run.app`) — `/healthz`, sample read, sample write. (10 min)
6. **Flip gateway routing** in gigaton-gateway (env var `DECISION_ENGINE_URL` or aggregator config) → new gigaton-platform URL. Deploy gateway revision. (5 min)
7. **Soak 30 min** — watch logs + Penrose dashboard. If green: keep going. If red: rollback (step 8).
8. **Rollback recipe** — flip gateway env back to carmen-beach decision-engine URL, redeploy gateway. ~3 min recovery. New gigaton-platform service stays in place but cold.

**Owner:** todd. **ETA:** ~75 min including soak.

---

## Day 2 — Wed 2026-05-27 evening — intelligence-silo cutover

**Pre-req:** Day 1 green, 12h soak passed.

### Steps

1. **GCS bucket plan — BLOCKER #1**: `gigaton-silo-index` does NOT exist in carmen-beach today (verified 2026-05-25). intel-silo likely creates it lazily OR `GCS_SYNC_PATH=semantic-index` refers to a path inside another bucket. Resolve before cutover by reading intel-silo source code. Two options:
   - **(a)** Create `gigaton-silo-index` bucket in gigaton-platform now (empty). Old data was never persisted; nothing to migrate. Acceptable if vector index can re-build from SQL.
   - **(b)** If data exists somewhere, `gcloud storage cp -r` to gigaton-platform.
2. **Move `gigaton-experiences-prod` bucket** (in carmen-beach, US-CENTRAL1, has data):
   ```
   gcloud storage buckets create gs://gigaton-experiences-prod-v2 --location=us-central1 --project=gigaton-platform
   gcloud storage cp -r gs://gigaton-experiences-prod gs://gigaton-experiences-prod-v2 --project=carmen-beach-properties
   ```
   Update intel-silo env `EXPERIENCE_ASSEMBLY_BUCKET=gigaton-experiences-prod-v2` (can't reuse name — bucket names are global).
3. SQL dump + restore for `intelligence-silo-pg` (same pattern as Day 1).
4. SA permissions: secretAccessor on 3 secrets (DB pw, drive-oauth, oauth-state) + cloudsql.client + storage.objectAdmin on the 2 buckets.
5. **OAuth quirk — BLOCKER #2**: `google-drive-oauth-client` JSON contains redirect URIs registered with the carmen-beach Cloud Run host (`*-rjmcrtvuzq-uc.a.run.app`). When intel-silo moves to gigaton-platform, the host changes to `*-uc.a.run.app` under a new project hash. The OAuth client needs new redirect URIs added in Google Cloud Console → APIs & Services → Credentials BEFORE the new revision is exposed.
6. Deploy new Cloud Run in gigaton-platform, no traffic.
7. Smoke: `/healthz`, search query, Drive OAuth roundtrip end-to-end.
8. Flip gateway `INTELLIGENCE_SILO_URL` → new URL. ALSO flip decision-engine env (deployed Day 1) `INTELLIGENCE_SILO_URL` → new URL.
9. Soak 30 min.
10. Rollback: revert both env flips. ~5 min.

**Owner:** todd. **ETA:** ~120 min (OAuth registration adds time).

---

## Day 3 — Thu 2026-05-28 evening — gigaton-engine cutover

**Pre-req:** Day 1+2 green, 24h combined soak passed.

### Decision required — BLOCKER #3 (canonical instance)

`gigaton-engine-pg` exists in BOTH projects after Day 0. **Decision needed before Day 3 kickoff: which is canonical?**
- **Recommended:** the gigaton-platform instance is canonical going forward. Carmen-beach instance was provisioned 2026-05-22 but never had post-provision (`gigaton_engine` user/DB never created — confirmed in memory). Abandon carmen instance; delete on Day 7.
- **Alternative:** do post-provision on carmen instance first, then migrate. Adds 1h and zero value.

### Steps

1. Decide canonical (above). Proceed assuming gigaton-platform instance.
2. Post-provision on gigaton-platform `gigaton-engine-pg`:
   ```
   PW=$(openssl rand -base64 32)
   gcloud secrets create gigaton-engine-pg-app-pw --project=gigaton-platform --replication-policy=automatic
   echo -n "$PW" | gcloud secrets versions add gigaton-engine-pg-app-pw --data-file=- --project=gigaton-platform
   gcloud sql users create gigaton_engine --instance=gigaton-engine-pg --project=gigaton-platform --password="$PW"
   gcloud sql databases create gigaton_engine --instance=gigaton-engine-pg --project=gigaton-platform
   ```
3. Current Cloud Run service has NO DB binding (verified Day 0). Migration is essentially a Cloud Run image-copy + redeploy in new project. No data to move (DB was empty).
4. Image copy to gigaton-platform AR. Deploy. No traffic.
5. Smoke `/healthz`. Flip gateway `GIGATON_ENGINE_URL` → new URL.
6. Soak 30 min.
7. Rollback: gateway env flip back. ~3 min.

**Owner:** todd. **ETA:** ~60 min.

---

## Day 4 — Fri 2026-05-29 evening — sales-operating-system cutover

**Pre-req:** Day 1-3 green, 24h+ combined soak.

### Surprise — BLOCKER #4 (SQLite ephemeral)

sales-operating-system uses `DATABASE_PATH=/data/sales_os.db` — **SQLite on the Cloud Run container's local filesystem**, which is ephemeral. Either:
- The service is stateless in practice (DB is empty each cold-start)
- OR there is a Cloud Storage FUSE mount we missed
- OR the service is actually broken and nobody noticed

Investigation needed BEFORE Day 4. Quickest test: `curl <url>/health` then trigger some write, redeploy/scale-to-zero/back-up, check if data persists. If data does persist, find the volume mount.

### Steps (assuming truly ephemeral)

1. Image copy.
2. Deploy in gigaton-platform with `sales-os-runtime` SA, same env (only need to update `DECISION_ENGINE_URL` → already migrated Day 1).
3. Smoke.
4. Flip gateway `SALES_OPERATING_SYSTEM_URL` (or similar).
5. Soak 30 min.
6. Rollback: gateway env flip back.

**Owner:** todd. **ETA:** ~45 min (assuming SQLite-is-ephemeral hypothesis confirmed).

---

## Day 5-7 — Sat 2026-05-30 → Mon 2026-06-01 — Soak + rollback window

- **Daily:** check Penrose scoreboard, Cloud Run error rate per migrated engine, gateway logs for 4xx/5xx spikes per upstream.
- **Day 5 (Sat 5/30)**: 24h soak checkpoint. If any engine showing >1% error rate increase vs baseline, rollback that engine's gateway env to carmen-beach.
- **Day 6 (Sun 5/31)**: 48h soak. Begin draft of decommission plan (do NOT execute).
- **Day 7 (Mon 6/1)**: 72h soak. Decision: extend soak or proceed to Day 8+ decommission.

### Day 8+ — Decommission carmen-beach engines (NOT IN SCOPE OF THIS RUNBOOK)

After 7-day soak proves stable, separate runbook will cover:
- Delete carmen-beach Cloud Run services (decision-engine, intelligence-silo, gigaton-engine, sales-operating-system)
- Delete carmen-beach Cloud SQL instances (decision-engine-pg, intelligence-silo-pg, gigaton-engine-pg)
- Revoke carmen-beach runtime SAs
- Delete mirror source secrets in carmen-beach
- Update DNS, docs, monitoring

---

## Cross-cutting

### Gateway routing-table-based rollback

Per the accelerated plan, the gateway aggregator config is the rollback switch. Any per-engine cutover must be reversible with a single gateway env var flip + redeploy. ~3-5 min instant rollback per engine.

### Image transfer (carmen-beach AR → gigaton-platform AR)

Two options:
- **Recommended:** trigger a fresh GitHub Actions deploy from each repo's `main` branch with `--project=gigaton-platform`. Cleanest; builds new image in new project.
- **Quick:** grant cross-project AR reader on the source images, deploy gigaton-platform Cloud Run with `gcr.io/carmen-beach-properties/<engine>:<tag>` reference. Works but couples projects.

### Staging bucket prerequisite

Before Day 1: `gcloud storage buckets create gs://gigaton-migration-staging --location=us-central1 --project=gigaton-platform` + grant both SQL instance service accounts (`p-<num>-<region>@gcp-sa-cloud-sql.iam.gserviceaccount.com`) the `objectAdmin` on it for export/import.

### Per-engine status checklist

| Engine | Day | Has SQL | Has GCS | Has OAuth | Image source |
| --- | --- | --- | --- | --- | --- |
| decision-engine | 1 | YES | no | no | gcr.io/carmen-beach-properties |
| intelligence-silo | 2 | YES | YES (2) | YES (Google Drive) | us-central1-docker.pkg.dev/carmen-beach-properties |
| gigaton-engine | 3 | NO (empty) | no | no | gcr.io/carmen-beach-properties |
| sales-operating-system | 4 | NO (SQLite ephemeral?) | no | no | gcr.io/carmen-beach-properties |

---

## Blocker questions for user (resolve BEFORE Day 1)

1. **intel-silo Cloud SQL — RESOLVED**: YES it uses Cloud SQL (`INSTANCE_CONNECTION_NAME=carmen-beach-properties:us-central1:intelligence-silo-pg` confirmed). `intelligence-silo-pg` provisioned tonight in gigaton-platform.
2. **Canonical `gigaton-engine-pg` — PENDING**: Memory says carmen-beach instance is empty (post-provision never completed). Recommend gigaton-platform instance becomes canonical; abandon carmen one on Day 7.
3. **connector-api + mimi-whatsapp — RESOLVED**: stay in carmen-beach per memory. Not in this runbook scope.
4. **`gigaton-silo-index` bucket — PENDING**: env var points to a bucket that doesn't exist in carmen-beach. Either lazy-creation or env-typo. Must read intel-silo code before Day 2.
5. **sales-OS SQLite ephemeral — PENDING**: `/data/sales_os.db` on Cloud Run local disk. Validate whether the service is actually stateful or genuinely ephemeral before Day 4.
6. **Carmen-beach Cloud Run hash + OAuth redirect URIs — PENDING**: Google Drive OAuth redirect URIs registered against carmen-beach hostname; need new URIs registered in Google Cloud Console for gigaton-platform hostname BEFORE Day 2 cutover.

---

## ETA confidence — "migration done + 7-day soak finished by Mon 2026-06-08"

**YELLOW**. Day-0 preflight is GREEN (complete tonight). Days 1-4 are well-scoped (~5h operator time total) but depend on:
- (a) GHA billing fixed (per memory, blocked since 2026-05-22)
- (b) Multipli sprint not slipping past 2026-05-26 EOD
- (c) Beta launch on existing infrastructure proves stable Tue 5/26
- (d) The 4 PENDING blockers above resolved by Day 1 start

If any of (a)-(d) slips, migration completes by 6-08 becomes RED. If all green, GREEN by 6-05 with 3 days slack.
