---
name: two-silos-carmen-vs-gigaton-platform-2026-05-28
description: "There are two intelligence-silo Cloud Run services. Gateway uses the carmen-beach-properties one (deployed on every main push); the gigaton-platform one is the deferred migration target. Don't confuse them when debugging."
metadata: 
  node_type: memory
  lifecycle_state: canonical
  type: reference
  established: 2026-05-28
  originSessionId: 531af6d3-63fd-43c2-a00f-95d7349257b6
promoted_from: two_silos_carmen_vs_gigaton_platform_2026_05_28.md
promoted_at: 2026-06-02T20:13:25Z
---

# Two intelligence-silo Cloud Run services — don't confuse them

Today's MKB → silo ingest spent ~30 minutes 401-ing against the wrong silo before the URL mismatch was caught. Saving so future sessions don't repeat.

## The active one (what gateway calls, what users hit)

- **Project:** `carmen-beach-properties`
- **URL:** `https://intelligence-silo-rjmcrtvuzq-uc.a.run.app`
- **Auto-deploys on every push to intel-silo `main`** via `.github/workflows/deploy-on-main.yml` → Cloud Build → `gcloud run deploy` in `carmen-beach-properties`. Confirmed by 5+ rev bumps on 2026-05-28 alone.
- **What gateway uses:** `gigaton-gateway`'s `INTELLIGENCE_SILO_URL` env var points here (verified via `gcloud run services describe gigaton-gateway --project=gigaton-platform`).
- **2026-05-28 state:** 3,656 MKB chunks ingested at `operator_id=gigaton`. Q&A returns grounded citations.

## The dormant one (migration target, do not seed yet)

- **Project:** `gigaton-platform`
- **URL:** `https://intelligence-silo-825651647756.us-central1.run.app`
- **Frozen:** revision `intelligence-silo-00001-kcf` from 2026-05-25 20:58 UTC — predates the transformers/sentence-transformers pin AND the FAISS train-defer fix. Ingest will 500 against it.
- **No auto-deploy.** Will only update when MIG-DEFER's silo session fires (gates per `.cxguy-active-migration` — currently DEFERRED until existing-system-completion trigger).

## Operational implications

- **Default `SILO_URL` for any ingest script must be the carmen-beach URL** until migration completes. The MKB scripts/launchagent already use it.
- **Both have invoker for `todd@gigaton.ai`** (granted 2026-05-28). Use `gcloud auth print-identity-token` (no `--audiences` — user creds reject it) to get a usable bearer.
- **When the migration session fires:** redeploy gigaton-platform silo from current main FIRST, re-run `scripts/ingest_mkb_to_silo.sh` against it, then flip gateway's `INTELLIGENCE_SILO_URL` env to the new URL. The decision-engine pattern (cloudbuild.yaml:52 hardcoded URL re-revert) likely applies — verify gateway's gcloud `--update-env-vars` sticks through subsequent gateway redeploys.

## Related

- [[migration_state_reconciled_and_functional_audit_2026_05_27]] — MIG-DEFER state + the decision-engine re-revert root cause
- [[qa_pipeline_phase2_shipped_2026_05_27]] — Q&A pipeline live on carmen-beach silo
