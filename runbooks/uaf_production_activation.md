# UAF Production Activation Runbook

> **Goal:** turn the Universal Acquisition Framework substrate ON in production with **5–10 minutes of operator attention** on deploy day.
> **Audience:** Todd (single operator). Copy-paste-ready.
> **Project:** `gigaton-platform` (GCP). **Region:** `us-central1`.
> **Status:** Activation runbook for Phase A → Phase C merged code on `main`.
> **Authored:** 2026-05-28

If anything in steps 3 / 4 / 5 fails, do **Rollback** (§7) — code stays deployed, only the activation pieces revert.

---

## 1. Preconditions

### 1.1 Code on `main`

All of the following PRs must be merged before running this runbook. Verify with `git log --oneline -20` in each repo and confirm the commit appears on `origin/main`.

| Repo | PR # | Title | Status |
|---|---|---|---|
| master-knowledge-base | [#27](https://github.com/todd-gig/master-knowledge-base/pull/27) | docs(uaf): shared SignalEvent + IDPProfile schemas for Phase A | MERGED |
| master-knowledge-base | [#28](https://github.com/todd-gig/master-knowledge-base/pull/28) | docs(uaf): land parent runbook for Universal Acquisition Framework | MERGED |
| gigaton-gateway | [#69](https://github.com/todd-gig/gigaton-gateway/pull/69) | feat(acquisition): POST /v1/acquisition/signal — UAF Phase A signal capture | MERGED |
| gigaton-gateway | [#70](https://github.com/todd-gig/gigaton-gateway/pull/70) | feat(acquisition): Pub/Sub publish on signal capture — UAF Phase B (publisher side) | MERGED |
| user-access-engine | [#48](https://github.com/todd-gig/user-access-engine/pull/48) | feat(idp): idp_profiles table + resolve/get endpoints — UAF Phase A | MERGED |
| user-access-engine | [#49](https://github.com/todd-gig/user-access-engine/pull/49) | feat(idp): Pub/Sub subscriber + 5 privacy items — UAF Phase B (UAE side) | MERGED |
| user-access-engine | [#52](https://github.com/todd-gig/user-access-engine/pull/52) | feat(idp): periodic decay-and-write job for provisional_category_vector — UAF Phase C | MERGED |
| intelligence-silo | [#55](https://github.com/todd-gig/intelligence-silo/pull/55) | feat(qa): persist EOResearchTask through Q&A backfill + operator scoping + cost + retry-ready fields | MERGED |
| intelligence-silo | [#58](https://github.com/todd-gig/intelligence-silo/pull/58) | feat(qa): NeedsProfile inference + real LLM cost + retry worker — UAF Phase B (silo side) | MERGED |
| intelligence-silo | [#63](https://github.com/todd-gig/intelligence-silo/pull/63) | feat(intelligence): real NeedsProfile inference — Phase C (ethnographic frames + dimensions + latent needs + inferred intent) | MERGED |

> Phase D (the acquisition manifest loader that reads the 4 category manifests added in [mkb #35](https://github.com/todd-gig/master-knowledge-base/pull/35)) is **not yet built** and not required for activation — the Phase A–C substrate stands alone until the loader lands.

### 1.2 Cloud Run services exist on `gigaton-platform`

```bash
gcloud run services list --project=gigaton-platform --region=us-central1
```

Expected (all `✔`):
- `intelligence-silo`            → `https://intelligence-silo-825651647756.us-central1.run.app`
- `gigaton-gateway`              → `https://gigaton-gateway-825651647756.us-central1.run.app`
- `user-access-engine`           → `https://user-access-engine-825651647756.us-central1.run.app`

If any are missing, **stop** — the migration in [[gcp_engine_migration_accelerated_2026_05_25]] must complete first.

### 1.3 Pub/Sub topic exists

```bash
gcloud pubsub topics describe gignet-orchestrator --project=gigaton-platform
```

Should print metadata (no error). The topic is pre-existing per the Gignet orchestration fabric.

### 1.4 Operator-side: create the Anthropic key secret (one-time)

If `silo-anthropic-key` does **not** exist (check with the gcloud command below), create it from your Anthropic API key before Step 2. The silo retry-sweep + needs-inference paths fail-soft without it, but you will not get real LLM-grounded NeedsProfiles until it's set.

```bash
gcloud secrets describe silo-anthropic-key --project=gigaton-platform 2>&1 || \
echo -n "sk-ant-..." | gcloud secrets create silo-anthropic-key \
  --project=gigaton-platform \
  --replication-policy=automatic \
  --data-file=-

# Grant intel-silo runtime SA access to the secret
gcloud secrets add-iam-policy-binding silo-anthropic-key \
  --project=gigaton-platform \
  --member=serviceAccount:intel-silo-runtime@gigaton-platform.iam.gserviceaccount.com \
  --role=roles/secretmanager.secretAccessor
```

---

## 2. Step 1 — Deploy current `main`

Each service has a Cloud Build pipeline that builds + pushes + deploys. Submit one at a time. Each takes ~5-15 min (silo is slowest due to PyTorch CPU wheel).

```bash
# 1. intelligence-silo (~15 min) — substitutions baked in cloudbuild.yaml (project=carmen-beach-properties for the image registry; deploy target is gigaton-platform)
cd ~/Documents/GitHub/intelligence-silo
gcloud builds submit --config=cloudbuild.yaml \
  --project=gigaton-platform \
  --substitutions=_REGION=us-central1,_SERVICE_NAME=intelligence-silo .

# 2. user-access-engine (~5 min)
cd ~/Documents/GitHub/user-access-engine
gcloud builds submit --config=cloudbuild.yaml \
  --project=gigaton-platform .

# 3. gigaton-gateway (~5 min)
cd ~/Documents/GitHub/gigaton-gateway
gcloud builds submit --config=cloudbuild.yaml \
  --project=gigaton-platform .
```

Sanity-check revisions are healthy after each build:

```bash
gcloud run services describe intelligence-silo \
  --project=gigaton-platform --region=us-central1 \
  --format='value(status.latestReadyRevisionName,status.url)'

gcloud run services describe user-access-engine \
  --project=gigaton-platform --region=us-central1 \
  --format='value(status.latestReadyRevisionName,status.url)'

gcloud run services describe gigaton-gateway \
  --project=gigaton-platform --region=us-central1 \
  --format='value(status.latestReadyRevisionName,status.url)'
```

---

## 3. Step 2 — Set env vars on each Cloud Run service

These flip the runtime behaviour without redeploying. `--update-env-vars` is additive; `--update-secrets` is additive for secret refs.

### 3.1 `intelligence-silo`

```bash
gcloud run services update intelligence-silo \
  --project=gigaton-platform \
  --region=us-central1 \
  --update-secrets=ANTHROPIC_API_KEY=silo-anthropic-key:latest \
  --update-env-vars=SEMANTIC_REQUIRE_OPERATOR=true,QA_RESEARCH_MODEL=claude-sonnet-4-6-20250514
```

Notes:
- `ANTHROPIC_API_KEY` → Secret Manager ref to the `silo-anthropic-key` secret created in §1.4. The retry worker + qa_synthesizer + self_heal executor all read `os.environ["ANTHROPIC_API_KEY"]` (see `intelligence-silo/core/eo/retry_worker.py`, `core/orchestrator/qa_synthesizer.py`, `core/eo/self_heal.py`).
- `QA_RESEARCH_MODEL` (optional) overrides the default in `core/eo/self_heal.py:31`. Default is `claude-sonnet-4-6-20250514`. Set explicitly here so the runtime is auditable.
- `SEMANTIC_REQUIRE_OPERATOR=true` is **production posture**. It gates `/memory/semantic-search`, the Q&A retry-sweep, and a few Q&A endpoints to require an `operator_id` (multi-tenant). Set this for production. Tests run with it unset.

### 3.2 `user-access-engine`

```bash
gcloud run services update user-access-engine \
  --project=gigaton-platform \
  --region=us-central1 \
  --update-env-vars=NEEDS_INFERENCE_URL=https://intelligence-silo-825651647756.us-central1.run.app/v1/intelligence/needs-inference,IDP_CATEGORY_VECTOR_HALFLIFE_DAYS=14
```

Notes:
- `NEEDS_INFERENCE_URL` — the webhook handler at `api/routers/webhooks.py::webhook_signal_received` reads this env var. When unset, the handler still 204's; when set, it fire-and-forget POSTs anonymised candidates to the silo and writes back `provisional_category_vector` (fail-soft, 2s timeout, never blocks the webhook). See PR #49.
- `IDP_CATEGORY_VECTOR_HALFLIFE_DAYS=14` — the decay-and-write job's half-life. Default fallback is 14 days. Setting it explicitly makes the runtime auditable.

### 3.3 `gigaton-gateway`

```bash
# This should already be set; the explicit update is a no-op safety net.
gcloud run services update gigaton-gateway \
  --project=gigaton-platform \
  --region=us-central1 \
  --update-env-vars=GCP_PROJECT_ID=gigaton-platform
```

Notes:
- `app/acquisition/signal_pubsub.py::_resolve_project_id` falls back to `os.environ["GCP_PROJECT_ID"]` then to `GOOGLE_CLOUD_PROJECT`. Setting it explicitly avoids the silent fallback path.
- Override hook (do **not** set in production): `GIGNET_ORCHESTRATOR_TOPIC`. Default `gignet-orchestrator` is what production uses.

---

## 4. Step 3 — Create the Pub/Sub push subscription

The gateway's `/v1/acquisition/signal` BackgroundTask publishes to the `gignet-orchestrator` topic with attribute `task=acquisition.signal_received` (constant from `app/acquisition/signal_pubsub.py:55`). The UAE subscriber consumes that exact attribute and pushes to its `/webhooks/signal-received` route. Filter ensures only the UAF acquisition messages hit UAE — other tasks on the same topic (orchestrator fan-out, dashboard stream, etc.) are ignored.

```bash
gcloud pubsub subscriptions create acquisition-signal-to-uae \
  --project=gigaton-platform \
  --topic=gignet-orchestrator \
  --push-endpoint=https://user-access-engine-825651647756.us-central1.run.app/webhooks/signal-received \
  --message-filter='attributes.task = "acquisition.signal_received"' \
  --push-auth-service-account=user-access-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
  --ack-deadline=60 \
  --message-retention-duration=86400s
```

Notes:
- `--push-auth-service-account` — UAE's own runtime SA (verified from `user-access-engine/cloudbuild.yaml:46` and `gcloud iam service-accounts list --project=gigaton-platform`: `user-access-engine-runtime@gigaton-platform.iam.gserviceaccount.com`). Push sub uses this SA to obtain an OIDC token for the push request, which Cloud Run's IAM rules can accept directly (the SA is the service's own runtime SA).
- `--message-filter` syntax: Pub/Sub uses `attributes.task = "..."` (with a space around the `=`, single quotes around the literal). The publisher sets `task` exactly per `app/acquisition/signal_pubsub.py:246` (`"task": SIGNAL_RECEIVED_TASK`).
- `--ack-deadline=60` — UAE's handler does an IDP resolve + (optional) fan-out POST; 60s is comfortable.

If the push SA needs explicit `roles/run.invoker` on the UAE service (it should via the deploy, but if Pub/Sub push 403s, this fixes it):

```bash
gcloud run services add-iam-policy-binding user-access-engine \
  --project=gigaton-platform \
  --region=us-central1 \
  --member=serviceAccount:user-access-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
  --role=roles/run.invoker
```

---

## 5. Step 4 — Create the Cloud Scheduler retry-sweep job(s)

The silo retry worker is exposed at `POST /v1/qa/research/retry-sweep` (see `intelligence-silo/core/eo/retry_worker.py:237`). In production (`SEMANTIC_REQUIRE_OPERATOR=true`) the endpoint **requires** `operator_id` in the body — so per-tenant scheduling = **one job per ACTIVE tenant**.

### 5.1 Job per active tenant

Replace `OPERATOR_ID` and re-run for each active tenant. Initial setup ships **one job per known active tenant**; add more as tenants activate. There is no admin token gate — auth is the OIDC token Cloud Scheduler attaches via `--oidc-service-account-email`.

```bash
# Template — replace OPERATOR_ID below and run once per active tenant.
OPERATOR_ID="gigaton"   # ← change per tenant

gcloud scheduler jobs create http qa-research-retry-sweep-${OPERATOR_ID} \
  --project=gigaton-platform \
  --location=us-central1 \
  --schedule="*/5 * * * *" \
  --time-zone="UTC" \
  --uri="https://intelligence-silo-825651647756.us-central1.run.app/v1/qa/research/retry-sweep" \
  --http-method=POST \
  --headers="Content-Type=application/json" \
  --message-body="{\"operator_id\":\"${OPERATOR_ID}\"}" \
  --oidc-service-account-email=intel-silo-runtime@gigaton-platform.iam.gserviceaccount.com \
  --oidc-token-audience=https://intelligence-silo-825651647756.us-central1.run.app
```

### 5.2 Known active tenants (initial seed list)

Run §5.1 once for each. Add new tenants here as they activate.

| operator_id | Status | Notes |
|---|---|---|
| `gigaton` | Cohort #0 (self) | Always-active. Create job. |
| `multipli` | Cohort #1 | Create job once Multipli onboards. |
| `liquefex` | Cohort #2 | Create job once LiqueFex onboards. |
| `carmen-beach-properties` | Cohort #3 (CBP) | Create job once CBP onboards. |

> If you'd rather start with **only** `gigaton` for the first 24h soak, do that — add the others once you've verified counters in §6.

### 5.3 Optional `X-Admin-Token` posture

If you later add an admin-token gate to `/v1/qa/research/retry-sweep` (currently absent — verified by grepping `core/eo/retry_worker.py` and `core/eo/qa_research_endpoints.py`), append `--headers="X-Admin-Token=<token>"` to the job above. Until then, the OIDC token + strict-mode operator_id are the auth posture.

---

## 6. Step 5 — Smoke tests

Run these immediately after §5 to prove each path works end-to-end. All commands use the production hostnames.

### 6.1 Gateway signal capture

```bash
curl -X POST https://gigaton-gateway-825651647756.us-central1.run.app/v1/acquisition/signal \
  -H "Content-Type: application/json" \
  -d '{
        "event_type": "page_view",
        "channel": "web",
        "page_url": "https://gigaton.ai/test-smoke",
        "referrer": "https://example.com",
        "device_fingerprint": "smoke-test-fp-001",
        "language": "en"
      }'
```

**Expected:** HTTP 200 with body shape `{"signal_id": "<uuid>", "accepted_at": "<iso8601>"}`. Capture the `signal_id` for the next checks.

### 6.2 Pub/Sub fan-out succeeded

```bash
# Pull stats on the new subscription. Look at the ack counter — it should be >= 1 by now.
gcloud pubsub subscriptions describe acquisition-signal-to-uae --project=gigaton-platform

# Or check via Monitoring (the bigger lens):
gcloud monitoring metrics list --project=gigaton-platform \
  --filter='metric.type="pubsub.googleapis.com/subscription/ack_message_count"' \
  --format='value(metric.type)' | head -3
```

If `ack_message_count` for `acquisition-signal-to-uae` is 0 after the curl, see §6.5.

### 6.3 IDP profile created by the webhook

```bash
# The smoke signal in §6.1 used device_fingerprint=smoke-test-fp-001.
# UAE creates an IDPProfile with primary_identity="device:smoke-test-fp-001".
curl -s "https://user-access-engine-825651647756.us-central1.run.app/v1/idp/profile?primary_identity=device:smoke-test-fp-001" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

**Expected:** 200 with an `IDPProfile` row (matching the schema in `runbooks/uaf_phase_a_shared_schemas.md` §3). If 404, the Pub/Sub push hasn't propagated yet — wait 30s and retry.

Variation: if you used an `email:` in §6.1 add `?primary_identity=email:test@example.com`.

### 6.4 Retry-sweep counters

```bash
curl -X POST https://intelligence-silo-825651647756.us-central1.run.app/v1/qa/research/retry-sweep \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
  -H "Content-Type: application/json" \
  -d '{"operator_id":"gigaton","max_attempts":3,"min_age_seconds":60,"batch_size":10}'
```

**Expected:** 200 with a `RetrySweepOut` payload — counters for tasks examined / requeued / completed / failed. The first sweep typically returns zeros; that's fine — it proves the endpoint is reachable and strict-mode operator gating is working.

### 6.5 If §6.2 or §6.3 fails — diagnostics

- **Pub/Sub fan-out 0 acks:** check `gigaton-gateway` logs for `[acquisition-signal-pubsub] publish failed` (fail-soft warning). Cause is usually missing `GCP_PROJECT_ID` env (re-run §3.3) or missing `roles/pubsub.publisher` on the gateway runtime SA:

  ```bash
  gcloud pubsub topics add-iam-policy-binding gignet-orchestrator \
    --project=gigaton-platform \
    --member=serviceAccount:gigaton-gateway-runtime@gigaton-platform.iam.gserviceaccount.com \
    --role=roles/pubsub.publisher
  ```

- **Push delivery 403 / IDP not created:** UAE rejected the push. Either re-run the `roles/run.invoker` binding in §4 or check the push SA has `roles/iam.serviceAccountTokenCreator` on itself:

  ```bash
  gcloud iam service-accounts add-iam-policy-binding \
    user-access-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
    --project=gigaton-platform \
    --member=serviceAccount:user-access-engine-runtime@gigaton-platform.iam.gserviceaccount.com \
    --role=roles/iam.serviceAccountTokenCreator
  ```

- **Scheduler job not firing:** check the Scheduler UI's "Last status". If 401, the OIDC audience must exactly match the silo URL — re-create the job with the URL above.

---

## 7. Rollback

Activation pieces revert without touching code. The 3 services keep running the latest revisions; only Pub/Sub fan-out + retry-sweep cron go dark. Signal capture continues to write to Firestore (the publisher is fail-soft).

```bash
# 7.1 Disable the Pub/Sub push subscription
#     (preferred over delete — keeps the resource for re-enable)
gcloud pubsub subscriptions update acquisition-signal-to-uae \
  --project=gigaton-platform \
  --push-endpoint=""   # blank push endpoint = effectively paused

# Alternative: delete the subscription outright
# gcloud pubsub subscriptions delete acquisition-signal-to-uae --project=gigaton-platform

# 7.2 Pause the retry-sweep job(s)
gcloud scheduler jobs pause qa-research-retry-sweep-gigaton \
  --project=gigaton-platform --location=us-central1

# Repeat 7.2 for any other per-tenant jobs created in §5.
# To resume: gcloud scheduler jobs resume qa-research-retry-sweep-<operator_id>
#            --project=gigaton-platform --location=us-central1
```

To revert env-var flips from §3:

```bash
gcloud run services update intelligence-silo \
  --project=gigaton-platform --region=us-central1 \
  --remove-env-vars=SEMANTIC_REQUIRE_OPERATOR,QA_RESEARCH_MODEL \
  --remove-secrets=ANTHROPIC_API_KEY

gcloud run services update user-access-engine \
  --project=gigaton-platform --region=us-central1 \
  --remove-env-vars=NEEDS_INFERENCE_URL,IDP_CATEGORY_VECTOR_HALFLIFE_DAYS
```

After rollback, `/v1/acquisition/signal` still 200's and still persists to Firestore (decoupled by design — see `app/acquisition/endpoints.py` docstring). Activation can be re-attempted later without code changes.

---

## 8. Verification window — first 24 h

Watch these and act on the named thresholds. Each surface is already wired by prior PRs — this runbook does not add observability.

| Metric | Surface | Healthy band | Action if breached |
|---|---|---|---|
| **Signal capture rate** (req/s on `POST /v1/acquisition/signal`) | Cloud Run metrics for `gigaton-gateway` | Anything ≥ 0 during traffic; 429 rate < 1% | If 429 rate > 1%, raise per-IP rate-limit window (currently 60 req / 60s in `app/acquisition/endpoints.py`). |
| **Pub/Sub `ack_message_count` on `acquisition-signal-to-uae`** | `gcloud pubsub subscriptions describe …` + Cloud Monitoring | Tracks the signal rate ± 5%; **no unacked backlog growth** | If backlog growing — UAE webhook is failing. Check UAE logs for `webhook_signal_received` 5xx. |
| **IDP creation rate** (rows added to `idp_profiles`) | UAE Postgres + Cloud Logging | Roughly == signal rate × identified-fraction (typically 20–60%) | If 0 with non-zero signals — Pub/Sub filter wrong or UAE handler erroring. Re-check §4 filter syntax. |
| **`provisional_category_vector` populated** | Inspect a sample of `idp_profiles` rows post-Phase-B | ≥ 30% of newly-created rows within first hour | If ≈ 0, the `NEEDS_INFERENCE_URL` env is unset or silo is 5xx'ing — check silo logs for `needs_inference` errors. |
| **Q&A retry-sweep success counters** | `RetrySweepOut.tasks_requeued + tasks_completed` per cron tick | Most ticks return 0; first non-zero proves real backfill path works | If `tasks_failed > 0` persistently, check silo logs for `ANTHROPIC_API_KEY` errors → re-verify §1.4 + §3.1. |
| **Penrose 8-metric scoreboard** (existing) | decision-engine `/v1/penrose/scoreboard` | Tracks pre-UAF baseline ± 5% | If drift critical breaches go up, freeze new activation and inspect via standard Penrose runbook. |

Observability cross-refs:
- Gignet dashboards: `runbooks/gignet-orchestrator-dashboard.json`
- Alert policies: `runbooks/gignet-alert-policies.yaml`
- Orchestrator fabric ops: `runbooks/orchestrator_fabric_ops.md`
- Penrose scoreboard: decision-engine service.

---

## 9. Cross-links

- **Parent runbook:** [`runbooks/2026_05_26_universal_acquisition_framework.md`](./2026_05_26_universal_acquisition_framework.md)
- **Phase A shared schemas:** [`runbooks/uaf_phase_a_shared_schemas.md`](./uaf_phase_a_shared_schemas.md)
- **Phase D manifests (declarative, loader pending):** [`manifests/acquisition/*.yaml`](../manifests/acquisition/) (landed via [mkb #35](https://github.com/todd-gig/master-knowledge-base/pull/35))
- **Auto-memory:** `[[universal_acquisition_framework_2026_05_26]]`
- **Doctrine:**
  - `[[foundational_goal_gigaton_engineered_brand_experience]]` — PPIM
  - `[[foundational_goal_maximize_human_superpowers]]` — applies the full intelligence stack to every UAF surface
  - `[[context_completeness_doctrine_2026_05_26]]` — refuse-below-threshold (applies to alt-user intelligence queries via this substrate)
  - `[[intel_3_no_static_weights_algorithmic_determination_2026_05_26]]` — algorithmic weights; bound to Phase C dimension scoring
  - `[[mcp_multi_tenant_namespace_blocker_2026_05_26]]` — scoped to UAF substrate via `operator_id` strict mode
- **Migration spine:** `[[gcp_engine_migration_accelerated_2026_05_25]]`

---

## Appendix — quick reference

Hostnames (gigaton-platform, us-central1):
- silo:    `https://intelligence-silo-825651647756.us-central1.run.app`
- UAE:     `https://user-access-engine-825651647756.us-central1.run.app`
- gateway: `https://gigaton-gateway-825651647756.us-central1.run.app`

Runtime service accounts:
- silo:    `intel-silo-runtime@gigaton-platform.iam.gserviceaccount.com`
- UAE:     `user-access-engine-runtime@gigaton-platform.iam.gserviceaccount.com`
- gateway: `gigaton-gateway-runtime@gigaton-platform.iam.gserviceaccount.com`

Pub/Sub:
- Topic:        `projects/gigaton-platform/topics/gignet-orchestrator`
- Subscription: `projects/gigaton-platform/subscriptions/acquisition-signal-to-uae`
- Filter:       `attributes.task = "acquisition.signal_received"`

Secrets:
- `silo-anthropic-key` — create in §1.4 (one-time)
