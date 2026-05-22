# Storage Flip Plan — DEE + EO System (in-memory v0 → Cloud SQL)

**Date.** 2026-05-22
**Owner.** todd@gigaton.ai (approval); Claude (implementation)
**Status.** PROPOSED — awaiting approval to execute
**Risk class.** MEDIUM (touches production data path on two engines, but both have fail-soft contracts + reversible Alembic migrations).
**Reversibility.** HIGH (each migration has a downgrade path; in-memory v0 still works if Cloud SQL is unreachable).

---

## 0. Why this work, why now

Both engines were merged on 2026-05-20 with in-memory v0 storage as a stopgap. Cloud SQL instances `decision-engine-pg` and `intelligence-silo-pg` were provisioned on 2026-05-21 and are RUNNABLE. The flip is the final step to make Decision Execution Engine (DEE) and Ethnographic Object (EO) records durable across container restarts — required for Penrose `decision_velocity` to leave `null`, for the orchestrator's lease semantics to survive cold starts, and for the Memory Lifecycle State Machine to operate on real history.

Per `decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md` §4, this is one of the genuine remaining gaps the ADR accepts.

---

## 1. Scope (what this plan covers)

- **DEE — Decision Execution Engine** at `decision-engine` repo, table family: `execution_records`, `decision_records`, plus the 5 module-specific tables (codification / ovs_calibration / human_override / ai_router / penrose).
- **EO System — Ethnographic Object** at `intelligence-silo` repo, table family: `ethnographic_objects`, `eo_research_tasks`, `eo_router_decisions`.

**Out of scope (explicit):**
- The GCP project migration of these engines from `carmen-beach-properties` → `gigaton-platform`. That is `gcp_project_organization_target_2026` and is a separate 3-phase plan. The storage flip happens **in the current project**; the project migration happens later, on top of the flipped state.
- SQLAlchemy ORM adoption for either engine. Both stay on raw psycopg2 for this flip (Phase 2 debt; non-blocking).
- Any net-new fields or schema changes to existing tables. We are flipping storage, not redesigning data.
- Memory Manager (`decision-engine/engine/memory_manager.py`). That stays as YAML-frontmatter markdown — it's intentionally not Postgres.

---

## 2. The canonical pattern (user-access-engine)

UAE completed this exact flip. Both engines copy its structure. Critical patterns to inherit:

1. **Alembic env config:** `transaction_per_migration=True` — without this, a single failing migration rolls back ALL prior ones. (UAE learned this 2026-05-20 when 0008 rolled back 0001-0007 on prod.)
2. **Widen `alembic_version.version_num`:** UAE's `_widen_alembic_version_num()` prerun hook widens the default VARCHAR(32) to TEXT before any migration runs. Long revision slugs silently truncate otherwise.
3. **Fail-soft boot:** `start.sh` runs `alembic upgrade head` with retry, then `exec uvicorn` even if migration fails. Container always boots; health degrades visibly via aggregator.
4. **Lazy connection:** module-level `_engine = None`, opened on first request, never at import time. Lets the container start without Postgres.
5. **Tests run without env vars:** if `INSTANCE_CONNECTION_NAME` is unset, all Postgres writes are no-ops. Existing test fixtures already follow this contract in both repos.

These five patterns are the contract. Everything else is wiring.

---

## 3. Pre-flight (must hold before any change)

| Check | Command | Pass criteria |
|---|---|---|
| Cloud SQL instances exist + RUNNABLE | `gcloud sql instances list --project carmen-beach-properties --filter='name~^(decision-engine\|intelligence-silo)-pg$' --format='value(name,state)'` | Both `RUNNABLE` |
| Cloud SQL app users + DBs exist | `gcloud sql users list --instance=decision-engine-pg --project=carmen-beach-properties` and same for `intelligence-silo-pg` | `decision_engine` user + `decision_engine` DB; `intelligence_silo` user + `intelligence_silo` DB |
| Secret Manager has app passwords | `gcloud secrets versions list decision-engine-pg-app-pw --project carmen-beach-properties` and same for `intelligence-silo-pg-app-pw` | At least 1 ENABLED version each |
| Cloud Run service accounts have `roles/cloudsql.client` | `gcloud projects get-iam-policy carmen-beach-properties --flatten='bindings[].members' --filter='bindings.role=roles/cloudsql.client'` | Both engine runtime SAs present |
| Both engines deployable from current `main` | `gh run list --repo todd-gig/decision-engine --limit 5` and same for intelligence-silo | Latest deploy run green |

If any check fails, stop and surface — do NOT begin the flip.

---

## 4. Phase A — DEE (decision-engine)

### Current state (from research pass)
- 6 Alembic migrations already exist in `alembic/versions/`: `0001_baseline`, `0002_penrose`, `0003_ai_router`, `0004_codification`, `0005_ovs_calibration`, `0006_human_override`. **All hand-written, NOT yet applied to prod.**
- `start.sh` already runs `alembic upgrade head` with retry + exec uvicorn.
- `cloudbuild.yaml` already wires `--add-cloudsql-instances`, `--set-secrets`, `--set-env-vars` for the DB.
- `engine/execution/postgres_recorder.py` already has the Postgres write-through layer. `engine/execution/router.py` `_make_recorder()` picks PostgresOutcomeRecorder if env vars are present.
- 5 other modules (codification, ovs_calibration, human_override, ai_router, penrose) each have their own `storage.py` with raw psycopg2 — already env-gated.

### What's missing
1. `alembic_version` widening guard (or confirm UAE's revision slug length is matched). DEE's slugs (`0001_baseline`, etc.) are short — **column width is NOT a problem for DEE.** Verify and skip the widening migration.
2. `transaction_per_migration=True` in `alembic/env.py` — verify present; add if missing.
3. Verification that DEE's first deploy after the flip will actually apply all 6 migrations on an empty `decision-engine-pg` (since instance is RUNNABLE but never received a migration).

### File-level changes — DEE

| File | Change | Lines | Risk |
|---|---|---|---|
| `decision-engine/alembic/env.py` | Verify `transaction_per_migration=True` is set in `run_migrations_online()`. Add if missing. | ~1 | LOW |
| `decision-engine/alembic/versions/0001_baseline.py` | Read; confirm idempotency (`IF NOT EXISTS` on each `CREATE TABLE`). If any table lacks the guard, add it. | 0-30 | LOW |
| `decision-engine/start.sh` | Verify retry loop already exists. If `alembic upgrade head` is currently single-attempt, wrap in 3-retry × 5s sleep. | ~5 | LOW |
| `decision-engine/tests/test_alembic_smoke.py` (NEW) | Boot the migration sequence against an in-memory SQLite or testcontainer; assert head reaches `0006_human_override`. | ~60 | LOW |
| `decision-engine/api/routes.py` | Add `GET /v1/healthz/db` endpoint that returns `{"db": "ok", "head_revision": "<rev>"}` if `SELECT 1` + alembic head match expected; degrades to 503 otherwise. The existing `GET /health` stays as a Cloud Run liveness probe (always 200). | ~20 | LOW |
| `decision-engine/cloudbuild.yaml` | No change — wiring already present. Verify only. | 0 | NONE |

### Deployment sequence — DEE

1. Open PR `chore(decision-engine): finalize alembic env + healthz/db endpoint`.
2. Merge after CI green.
3. Deploy via existing GHA workflow.
4. On boot:
   - `alembic upgrade head` runs against empty `decision-engine-pg`.
   - All 6 migrations apply in sequence (each in its own transaction).
   - uvicorn starts.
5. Verify:
   ```
   curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/healthz/db
   ```
   Expect `{"db": "ok", "head_revision": "0006_human_override"}`.
6. Exercise: POST a decision + execution via `/v1/decisions/.../executions`, confirm it persists across a container restart (`gcloud run services update decision-engine --region us-central1 --no-traffic --tag canary` then route 1% traffic, then back).
7. Confirm Penrose `decision_velocity` starts emitting non-null values within ~24h (data substrate now exists).

### Rollback — DEE

- Each migration has a `downgrade()` path. To roll back: `alembic downgrade -1` in a one-shot Cloud Run job, then `gcloud run deploy` previous revision tag.
- In-memory v0 still works without env vars — if Cloud SQL becomes unreachable, the engine falls back to in-memory writes (existing fail-soft behavior).
- Worst case: `gcloud run services update-traffic decision-engine --to-revisions <prior-rev>=100` flips back in ~30s.

---

## 5. Phase B — EO System (intelligence-silo)

### Current state (from research pass)
- 4 raw `.sql` files in `migrations/` directory (`001_ethnographic_objects.sql`, `030_documentation_ingest.sql`, `031_onboarding_workflow_state.sql`, `032_memory_items.sql`). **NOT integrated into Alembic. NO `alembic.ini`, NO `alembic/env.py`, NO `alembic/versions/`.**
- `core/eo/persistence.py` has working write-through code + lazy psycopg2 connection.
- `core/eo/persistence.py` calls `ensure_schema()` at module import — this is the current "migration" mechanism and must be retired.
- `Dockerfile` runs `uvicorn` directly with no boot-time migration.
- `cloudbuild.yaml` does NOT currently wire `--add-cloudsql-instances` for `intelligence-silo-pg`. (Service is LIVE but Postgres has never been attached.)
- `hydrate()` function in `persistence.py` loads existing rows into the in-memory dicts on startup — this is the bridge that keeps reads fast after the flip.

### What's missing
The whole Alembic stack + the Cloud Run socket wiring + a `start.sh`.

### File-level changes — EO

| File | Change | Lines | Risk |
|---|---|---|---|
| `intelligence-silo/alembic.ini` (NEW) | Standard Alembic config. Copy from DEE; change `sqlalchemy.url = ` placeholder. | ~30 | LOW |
| `intelligence-silo/alembic/env.py` (NEW) | Standard env. Pattern from DEE: env-var DSN resolution, `transaction_per_migration=True`, `target_metadata = None`. | ~80 | LOW |
| `intelligence-silo/alembic/versions/0001_baseline.py` (NEW) | Hand-written migration that recreates the union of the 4 existing `.sql` files using `IF NOT EXISTS` guards. Captures: `ethnographic_objects`, `eo_research_tasks`, `eo_router_decisions`, `source_documentation`, `documentation_bundles`, `onboarding_workflow_state`, `memory_items`. Each `CREATE TABLE IF NOT EXISTS`. Indexes also guarded. | ~250 | MEDIUM |
| `intelligence-silo/alembic/versions/0002_widen_alembic_version.py` (NEW) | UAE-style prerun hook widening `alembic_version.version_num` to TEXT. Belt-and-braces — even if current slugs are short, future slugs might not be. | ~25 | LOW |
| `intelligence-silo/start.sh` (NEW) | Mirror DEE: retry loop on `alembic upgrade head`, then `exec uvicorn core.api:app --host 0.0.0.0 --port 8080 --workers 1`. | ~25 | LOW |
| `intelligence-silo/Dockerfile` | Change `CMD ["uvicorn", "core.api:app", ...]` → `CMD ["/app/start.sh"]`. Add `RUN chmod +x /app/start.sh`. | ~2 | LOW |
| `intelligence-silo/cloudbuild.yaml` | Add `--add-cloudsql-instances=carmen-beach-properties:us-central1:intelligence-silo-pg`, `--set-secrets=DB_PASSWORD=intelligence-silo-pg-app-pw:latest`, `--set-env-vars=INSTANCE_CONNECTION_NAME=carmen-beach-properties:us-central1:intelligence-silo-pg,DB_USER=intelligence_silo,DB_NAME=intelligence_silo`. | ~6 | LOW |
| `intelligence-silo/core/eo/persistence.py` | Remove or no-op `ensure_schema()` call. Schema is now Alembic's responsibility. Keep `hydrate()` — it remains useful. | ~20 | MEDIUM |
| `intelligence-silo/core/api.py` (or equivalent) | Add `GET /v1/healthz/db` mirroring DEE's endpoint. | ~20 | LOW |
| `intelligence-silo/tests/test_alembic_smoke.py` (NEW) | Boot Alembic against in-memory SQLite or testcontainer; assert head reaches `0002_widen_alembic_version`. | ~60 | LOW |
| `intelligence-silo/migrations/README.md` (NEW or MODIFIED) | Note that the raw `.sql` files in this directory are now historical; Alembic in `alembic/versions/` is canonical. Do not run `.sql` files manually after `0001_baseline` has been applied. | ~15 | NONE |

### Deployment sequence — EO

1. Open PR `feat(intelligence-silo): adopt Alembic + Cloud SQL wiring`.
2. **First**, in PR review, confirm `0001_baseline.py` captures every table currently in the 4 `.sql` files — diff the SQL files against the migration. Single most error-prone step.
3. Merge after CI green.
4. Deploy.
5. On boot, since `intelligence-silo-pg` has never had any migration, `alembic upgrade head` runs `0001_baseline` (creating all tables) + `0002_widen_alembic_version`.
6. `hydrate()` then reads empty tables into in-memory dicts → no-op since the DB is fresh.
7. Verify:
   ```
   curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/v1/healthz/db
   ```
8. Exercise: POST an EO via `/v1/eo`, restart the container, GET it back. Must persist.

### Rollback — EO

- If `0001_baseline` fails (most likely cause: a typo or missing `IF NOT EXISTS`), Cloud Run container reaches the retry limit, then continues with uvicorn boot (fail-soft). EO endpoints keep working from in-memory dicts. Diagnose, fix migration, redeploy.
- If schema is partially applied and inconsistent: drop the database via `gcloud sql databases delete intelligence_silo --instance=intelligence-silo-pg --project=carmen-beach-properties`, recreate, redeploy. Acceptable because `intelligence-silo-pg` has no production data yet — flip is happening on an empty DB.
- After data exists: standard `alembic downgrade -1` path applies.

---

## 6. Phase C — Smoke + observability

After both engines flip:

1. **Penrose scoreboard.** Within 24h of DEE flip + first real decision execution, `decision_velocity` should leave `null`. Verify:
   ```
   curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
     https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/penrose/scoreboard | jq '.metrics.decision_velocity'
   ```
2. **Gateway aggregator.** Add `intelligence-silo` to `gigaton-gateway/api/health_aggregator.py` if not already listed. Drift item #3 in `master_project_plan.md` §3.6 mentions persona-engine + sales-OS as gaps; verify EO + DEE are tracked too. Aggregate verdict should go from `degraded` → `ok` once `connector-api/health` is also addressed (separate work).
3. **Cloud Monitoring.** Confirm the "Gignet Orchestrator Fabric" dashboard's existing widgets pick up the new DB connection metrics from both engines. Add 2 new widgets if not auto-populated: `decision-engine connections (active)`, `intelligence-silo connections (active)`.

---

## 7. Decision register (none required from user)

The storage flip has **no architectural decisions left open**. Every choice has a canonical answer from UAE's prior flip:

- Connection pooling: lazy single connection per process, autocommit (UAE pattern).
- Migration framework: Alembic with `transaction_per_migration=True` + `version_num` widened to TEXT.
- ORM: none — raw psycopg2 stays. SQLAlchemy adoption is Phase 2 debt.
- Health check: separate `/v1/healthz/db` for DB depth; existing `/health` stays as liveness probe.
- Fail-soft: container boots even if migration fails; reads/writes fall back to in-memory v0.

This plan does not require any approval gates beyond the top-level "go ahead with both phases as written."

---

## 8. Estimated effort + sequence

- **Phase A (DEE):** ~3-5h elapsed, single PR. Mostly verification + the healthz endpoint. Low surprise budget.
- **Phase B (EO):** ~8-12h elapsed, single PR. The `0001_baseline.py` translation from raw SQL is the main work. Medium surprise budget.
- **Phase C (smoke):** ~1h, no PR.

**Recommended sequence:** Phase A → ship → 24h soak → Phase B → ship → Phase C. Total elapsed ~3 days including the DEE soak window.

If you want them in parallel (no soak), it's ~2 days but you carry both risks at once. I'd recommend the serial path.

---

## 9. Approval gates

- [ ] Pre-flight checks (§3) all pass.
- [ ] Phase A file list approved.
- [ ] Phase A merged + healthz verifies.
- [ ] (24h soak)
- [ ] Phase B file list approved.
- [ ] Phase B `0001_baseline.py` reviewed line-by-line against the 4 raw SQL files.
- [ ] Phase B merged + healthz verifies.
- [ ] Penrose `decision_velocity` leaves null.
- [ ] Gateway aggregator goes `ok` (after connector-api/health is also addressed — separate work).

---

## 10. Cross-references

- `docs/architecture/CODEBASE_MAP.md` §2.3 (decision engine + Penrose) and §3.3 (production storage flip gap).
- `decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md` §4 (genuine remaining gaps).
- `memory/standalone_bundle_net_new_concepts.md` (DEE + EO concept origin).
- `memory/decisions_2026_05_20_resume_here_a1_a2_a3.md` (decision A.3: YES Cloud SQL for both engines).
- UAE reference: `/Users/admin/Documents/GitHub/user-access-engine/alembic/env.py` + `api/db.py`.
