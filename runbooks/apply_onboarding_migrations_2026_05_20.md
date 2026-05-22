# Apply Onboarding Workflow Migrations — 2026-05-20

> **Operator-execute runbook.** Three schema migrations shipped today (2026-05-20)
> as part of the chat-first 10-stage operator onboarding workflow. All three
> are **committed but NOT auto-applied** per axiom **AX-010** (founder
> sign-off required for schema changes). The corresponding service endpoints
> currently fall back to in-process stubs; applying these migrations promotes
> them to durable persistence.
>
> Canonical context: `[[onboarding_workflow_v1_shipped_2026_05_20]]`
> (`/Users/admin/.claude/projects/-Users-admin/memory/onboarding_workflow_v1_shipped_2026_05_20.md`).
> Cloud SQL decisions: `[[decisions_2026_05_20_resume_here_a1_a2_a3]]` §A.3.

---

## ⚠ Critical pre-flight (read first)

```
┌────────────────────────────────────────────────────────────────────────┐
│  ORDERING IS NOT LOAD-BEARING.                                         │
│                                                                        │
│  All three migrations are PURE schema additions (new tables + new     │
│  NULLABLE / defaulted columns). The existing services keep working    │
│  identically pre- AND post-migration; they fall back to in-process    │
│  stubs when the columns/tables are absent. No service redeploy is     │
│  required to "activate" the migration — the schema check is dynamic.  │
│                                                                        │
│  Recommended order is UAE → intel-silo → decision-engine because that │
│  matches the data-flow direction (gateway resolver reads UAE overlays │
│  first), but any order works.                                         │
└────────────────────────────────────────────────────────────────────────┘
```

### Pre-flight checklist

Confirm each before executing any step:

- [ ] **Founder sign-off acknowledged** — AX-010 sign-off captured (see
      `decisions_2026_05_20_resume_here_a1_a2_a3.md` §A.3; covers all three
      migrations as part of the chat-first onboarding bundle).
- [ ] **Cloud SQL instances all `RUNNABLE`:**
      ```bash
      gcloud sql instances list \
        --filter="name~user-access-engine-pg OR name~decision-engine-pg OR name~intelligence-silo-pg" \
        --format="table(project_id,name,state,databaseVersion)"
      ```
      Expected:
      ```
      PROJECT_ID                  NAME                    STATE     DATABASE_VERSION
      gigaton-platform            user-access-engine-pg   RUNNABLE  POSTGRES_15
      carmen-beach-properties     decision-engine-pg      RUNNABLE  POSTGRES_15
      carmen-beach-properties     intelligence-silo-pg    RUNNABLE  POSTGRES_15
      ```
- [ ] **gcloud authenticated as `todd@gigaton.ai`** (canonical, per
      `canonical_gcloud_account.md`):
      ```bash
      gcloud auth list --filter="status:ACTIVE" --format="value(account)"
      # expected: todd@gigaton.ai
      ```
      If not:
      ```bash
      gcloud auth login todd@gigaton.ai
      gcloud config set account todd@gigaton.ai
      ```
- [ ] **`cloud-sql-proxy` v2 on PATH** (`cloud-sql-proxy --version` → `2.x.x`).
      Install if missing:
      ```bash
      brew install cloud-sql-proxy
      ```
- [ ] **Migration files present locally** (sanity):
      ```bash
      ls -la \
        /Users/admin/Documents/GitHub/user-access-engine/alembic/versions/0007_onboarding_workflow_columns.py \
        /Users/admin/Documents/GitHub/intelligence-silo/migrations/031_onboarding_workflow_state.sql \
        /Users/admin/Documents/GitHub/decision-engine/migrations/002_onboarding_activation_gates.sql
      ```
      All three should report sizes > 0 bytes.
- [ ] **Backups (optional)** — automated daily backups exist; changes are
      additive + idempotent so out-of-band backups are not required. Force
      one per instance with `gcloud sql backups create --instance=<name> --project=<project>` if desired.

---

## Step 1 — UAE Alembic 0007 (user-access-engine)

**Target:** Cloud SQL `user-access-engine-pg` in project `gigaton-platform`.
**Migration:** `0007_onboarding_workflow_columns` (down_revision `0006_documentation_capabilities`).
**Adds:** `workflow_overlays JSONB`, `nav_tier_state JSONB`,
`scope_contract_signed_at TIMESTAMPTZ` to `client_namespaces`; **3 new tables**
`legal_entity_records`, `scope_contracts`, `axiom_acknowledgements`.

### 1a. Open Cloud SQL Auth Proxy (terminal A)

```bash
cloud-sql-proxy \
  --port 5432 \
  gigaton-platform:us-central1:user-access-engine-pg
```

Expected first lines:
```
2026/05/20 ... INFO Authorizing with Application Default Credentials
2026/05/20 ... INFO [gigaton-platform:us-central1:user-access-engine-pg] Listening on 127.0.0.1:5432
2026/05/20 ... INFO The proxy has started successfully and is ready for new connections!
```

Leave this terminal running. If port 5432 is busy locally, swap to `--port 5433`
and adjust the connection string below.

### 1b. Get the DB password (terminal B)

```bash
export PGPASSWORD="$(gcloud secrets versions access latest \
  --secret=user-access-engine-db-password \
  --project=gigaton-platform)"
```

Sanity-check it bound:
```bash
test -n "$PGPASSWORD" && echo "ok: password loaded" || echo "FAIL: empty"
```

### 1c. Verify connectivity (terminal B)

```bash
psql "host=127.0.0.1 port=5432 dbname=user_access_engine user=user_access_engine sslmode=disable" \
  -c "SELECT version();"
```

Expected: a single row printing `PostgreSQL 15.x ...`.

### 1d. Run the migration

```bash
cd /Users/admin/Documents/GitHub/user-access-engine

# Confirm current head BEFORE
DATABASE_URL="postgresql://user_access_engine:${PGPASSWORD}@127.0.0.1:5432/user_access_engine" \
  alembic current
# Expected: 0006_documentation_capabilities (head)

# Apply 0007
DATABASE_URL="postgresql://user_access_engine:${PGPASSWORD}@127.0.0.1:5432/user_access_engine" \
  alembic upgrade head
```

Expected output (tail):
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 0006_documentation_capabilities -> 0007_onboarding_workflow_columns, ...
```

Confirm new head:
```bash
DATABASE_URL="postgresql://user_access_engine:${PGPASSWORD}@127.0.0.1:5432/user_access_engine" \
  alembic current
# Expected: 0007_onboarding_workflow_columns (head)
```

### 1e. Verify schema landed

```bash
psql "host=127.0.0.1 port=5432 dbname=user_access_engine user=user_access_engine sslmode=disable" <<'SQL'
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'client_namespaces'
  AND column_name IN ('workflow_overlays','nav_tier_state','scope_contract_signed_at')
ORDER BY column_name;
SQL
```

Expected: exactly 3 rows.
```
         column_name         |          data_type
-----------------------------+-----------------------------
 nav_tier_state              | jsonb
 scope_contract_signed_at    | timestamp with time zone
 workflow_overlays           | jsonb
(3 rows)
```

Verify the 3 new tables:
```bash
psql "host=127.0.0.1 port=5432 dbname=user_access_engine user=user_access_engine sslmode=disable" <<'SQL'
SELECT table_name FROM information_schema.tables
WHERE table_schema='public'
  AND table_name IN ('legal_entity_records','scope_contracts','axiom_acknowledgements')
ORDER BY table_name;
SQL
```

Expected: 3 rows — `axiom_acknowledgements`, `legal_entity_records`, `scope_contracts`.

### 1f. Production smoke

Get an identity token first:
```bash
export ID_TOKEN="$(gcloud auth print-identity-token)"
```

Hit a known operator's namespace (existing rows get `workflow_overlays = '{}'`
by default — that's the expected post-migration value):
```bash
curl -s -H "Authorization: Bearer $ID_TOKEN" \
  https://user-access-engine-rjmcrtvuzq-uc.a.run.app/v1/admin/namespaces/carmen-beach \
  | jq '{operator_id, workflow_overlays, nav_tier_state, scope_contract_signed_at}'
```

Expected (defaults — these are CORRECT for an existing namespace not yet
re-onboarded):
```json
{
  "operator_id": "carmen-beach",
  "workflow_overlays": {},
  "nav_tier_state": {},
  "scope_contract_signed_at": null
}
```

If the keys are missing entirely (not just `null` / `{}`), the deployed
revision predates the schema-aware response model — that's fine, the column
data is durable; the response surface will pick it up on the next UAE deploy.

### 1g. Rollback (only if needed)

```bash
cd /Users/admin/Documents/GitHub/user-access-engine
DATABASE_URL="postgresql://user_access_engine:${PGPASSWORD}@127.0.0.1:5432/user_access_engine" \
  alembic downgrade -1
```

After rollback, expect `alembic current` → `0006_documentation_capabilities`.

**Dependency impact of rollback:** the gateway resolver's per-operator
overlay fetch (`GET /v1/resolver/overlay/{operator_id}` on UAE) will return
404 → gateway falls back to the canonical onboarding manifest. Chat-first
onboarding still works; just no per-operator overlays. Stages 0/2/3/6/7/9
behaviors silently revert to canonical defaults.

### 1h. Cleanup (after Step 1 confirmed)

Close the proxy in terminal A with `Ctrl+C`, and:
```bash
unset PGPASSWORD
```

---

## Step 2 — intel-silo SQL migration 031

**Target:** Cloud SQL `intelligence-silo-pg` in project `carmen-beach-properties`.
**Migration:** `031_onboarding_workflow_state.sql`.
**Adds:** `onboarding_workflow_state` (one row per operator, aggregator) +
`onboarding_action_completions` (append-only ledger).

intel-silo uses **plain SQL migrations** (no alembic). The file is idempotent
(every statement guards with `IF NOT EXISTS`), so re-apply is a safe no-op.

### 2a. Open Cloud SQL Auth Proxy (terminal A)

```bash
cloud-sql-proxy \
  --port 5432 \
  carmen-beach-properties:us-central1:intelligence-silo-pg
```

Expected: `Listening on 127.0.0.1:5432 ... ready for new connections!`

### 2b. Load DB password (terminal B)

```bash
export PGPASSWORD="$(gcloud secrets versions access latest \
  --secret=intelligence-silo-db-password \
  --project=carmen-beach-properties)"
test -n "$PGPASSWORD" && echo "ok" || echo "FAIL"
```

### 2c. Apply the migration

```bash
psql "host=127.0.0.1 port=5432 dbname=intelligence_silo user=intelligence_silo sslmode=disable" \
  -v ON_ERROR_STOP=1 \
  -f /Users/admin/Documents/GitHub/intelligence-silo/migrations/031_onboarding_workflow_state.sql
```

Expected output (tail):
```
BEGIN
CREATE TABLE
CREATE INDEX
CREATE TABLE
CREATE INDEX
COMMIT
```

(On re-apply, the `CREATE TABLE` / `CREATE INDEX` lines become `NOTICE:
relation ... already exists, skipping` — also success.)

### 2d. Verify schema

```bash
psql "host=127.0.0.1 port=5432 dbname=intelligence_silo user=intelligence_silo sslmode=disable" <<'SQL'
SELECT table_name FROM information_schema.tables
WHERE table_schema='public'
  AND table_name IN ('onboarding_workflow_state','onboarding_action_completions')
ORDER BY table_name;

SELECT count(*) AS state_rows FROM onboarding_workflow_state;
SELECT count(*) AS completion_rows FROM onboarding_action_completions;
SQL
```

Expected:
```
         table_name
------------------------------
 onboarding_action_completions
 onboarding_workflow_state
(2 rows)

 state_rows
------------
          0

 completion_rows
-----------------
               0
```

### 2e. Production smoke

```bash
export ID_TOKEN="$(gcloud auth print-identity-token)"

curl -s -H "Authorization: Bearer $ID_TOKEN" \
  "https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/v1/onboarding/state?operator_id=carmen-beach" \
  | jq .
```

Expected (autocreate-on-first-read for an operator with no prior state):
```json
{
  "operator_id": "carmen-beach",
  "manifest_version": "1.0.0",
  "current_stage_id": "stage-0-trust-scope",
  "stages_completed": [],
  "current_stage_actions_completed": [],
  "predicted_influence_to_date_usd": 0.0,
  "shadow_mode_enabled": false,
  "shadow_mode_started_at": null,
  "live_recommend_activated_at": null,
  "live_auto_execute_activated_at": null
}
```

Confirm the row landed in Postgres (not just the stub):
```bash
psql "host=127.0.0.1 port=5432 dbname=intelligence_silo user=intelligence_silo sslmode=disable" \
  -c "SELECT operator_id, current_stage_id, predicted_influence_to_date_usd, created_at FROM onboarding_workflow_state;"
```

Expected: 1 row with `operator_id = carmen-beach` and a recent `created_at`.

> If you see 0 rows after the smoke, the deployed revision is still using the
> in-process stub (the on-disk SQLite fallback). Trigger a deploy via the
> repo's normal release path; the schema is present and ready.

### 2f. Rollback

```bash
psql "host=127.0.0.1 port=5432 dbname=intelligence_silo user=intelligence_silo sslmode=disable" <<'SQL'
BEGIN;
DROP TABLE IF EXISTS onboarding_action_completions;
DROP TABLE IF EXISTS onboarding_workflow_state;
COMMIT;
SQL
```

**Dependency impact:** the gateway resolver activation-gate check (whether
`carmen-beach` is allowed into shadow / live-recommend / live-auto-execute)
will return the stub default `current_stage_id = 'stage-0-trust-scope'`,
`shadow_mode_enabled = false`. Stages already completed in-session before
rollback will need to be re-recorded post re-apply (the append-only ledger
is also dropped).

### 2g. Cleanup

`Ctrl+C` the proxy in terminal A, then `unset PGPASSWORD`.

---

## Step 3 — decision-engine SQL migration 002

**Target:** Cloud SQL `decision-engine-pg` in project `carmen-beach-properties`.
**Migration:** `002_onboarding_activation_gates.sql`.
**Adds:** `axiom_acknowledgements_local` (Stage 0 axiom acks, local mirror
until cross-engine UAE sync lands) + `operator_targets` (Stage 4 north-star
+ supporting + constraints).

### 3a. Open Cloud SQL Auth Proxy (terminal A)

```bash
cloud-sql-proxy \
  --port 5432 \
  carmen-beach-properties:us-central1:decision-engine-pg
```

### 3b. Load DB password (terminal B)

```bash
export PGPASSWORD="$(gcloud secrets versions access latest \
  --secret=decision-engine-db-password \
  --project=carmen-beach-properties)"
test -n "$PGPASSWORD" && echo "ok" || echo "FAIL"
```

### 3c. Apply the migration

```bash
psql "host=127.0.0.1 port=5432 dbname=decision_engine user=decision_engine sslmode=disable" \
  -v ON_ERROR_STOP=1 \
  -f /Users/admin/Documents/GitHub/decision-engine/migrations/002_onboarding_activation_gates.sql
```

Expected output:
```
CREATE TABLE
CREATE INDEX
CREATE INDEX
CREATE UNIQUE INDEX
CREATE TABLE
```

(Re-apply yields `NOTICE: relation ... already exists, skipping` lines.)

### 3d. Verify schema

```bash
psql "host=127.0.0.1 port=5432 dbname=decision_engine user=decision_engine sslmode=disable" <<'SQL'
SELECT table_name FROM information_schema.tables
WHERE table_schema='public'
  AND table_name IN ('axiom_acknowledgements_local','operator_targets')
ORDER BY table_name;

\d axiom_acknowledgements_local
\d operator_targets
SQL
```

Expected: both tables listed; `axiom_acknowledgements_local` shows the
`UNIQUE (operator_id, axiom_id, acknowledged_by_user_id)` constraint;
`operator_targets` shows `operator_id` as PRIMARY KEY.

### 3e. Production smoke

```bash
export ID_TOKEN="$(gcloud auth print-identity-token)"

curl -s -H "Authorization: Bearer $ID_TOKEN" \
  "https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/operators/carmen-beach/targets-readiness" \
  | jq .
```

Expected (same response shape as stub — but writes now persist):
```json
{
  "operator_id": "carmen-beach",
  "north_star_metric_key": null,
  "target_value": null,
  "supporting_metrics": [],
  "constraints": [],
  "ready": false
}
```

Optional: write a target and confirm round-trip:
```bash
curl -s -X POST -H "Authorization: Bearer $ID_TOKEN" -H "Content-Type: application/json" \
  "https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/operators/carmen-beach/targets" \
  -d '{"north_star_metric_key":"net_revenue_per_property_per_month","target_value":4500,"units":"USD"}' \
  | jq .

# Read back from DB directly:
psql "host=127.0.0.1 port=5432 dbname=decision_engine user=decision_engine sslmode=disable" \
  -c "SELECT operator_id, north_star_metric_key, target_value, units FROM operator_targets;"
```

Expected: 1 row, `north_star_metric_key = 'net_revenue_per_property_per_month'`,
`target_value = 4500.0000`.

### 3f. Rollback

```bash
psql "host=127.0.0.1 port=5432 dbname=decision_engine user=decision_engine sslmode=disable" <<'SQL'
BEGIN;
DROP TABLE IF EXISTS axiom_acknowledgements_local;
DROP TABLE IF EXISTS operator_targets;
COMMIT;
SQL
```

**Dependency impact:** Stage 0 axiom-ack persistence reverts to in-process
stub (acks are durable for the lifetime of the Cloud Run instance only).
Stage 4 target reads/writes return defaults; the gateway resolver's Stage 4
gate stays open as `ready: false` regardless of writes. No downstream
breakage; PPEME + HME unaffected.

### 3g. Cleanup

`Ctrl+C` terminal A, `unset PGPASSWORD`.

---

## Post-migration end-to-end smoke

This script exercises the full chat-first onboarding loop across the gateway
+ all three migrated services. Save and run from anywhere with `gcloud` set up.

```bash
#!/usr/bin/env bash
# /tmp/onboarding_e2e_smoke.sh
# Post-migration end-to-end smoke for the chat-first onboarding workflow.
set -u  # do NOT set -e — we want to surface every failure, not bail on first
GATEWAY="https://gigaton-gateway-rjmcrtvuzq-uc.a.run.app"
INTEL="https://intelligence-silo-rjmcrtvuzq-uc.a.run.app"
HME="https://human-management-engine-rjmcrtvuzq-uc.a.run.app"
DE="https://decision-engine-rjmcrtvuzq-uc.a.run.app"
OPERATOR="carmen-beach"

PASS=0
FAIL=0
RESULTS=()

note() { echo; echo "── $1 ──"; }
record() {
  if [[ "$2" == "ok" ]]; then
    PASS=$((PASS+1)); RESULTS+=("✅ $1")
  else
    FAIL=$((FAIL+1)); RESULTS+=("❌ $1 — $2")
  fi
}

note "0. Fetch identity token"
ID_TOKEN="$(gcloud auth print-identity-token 2>/dev/null)"
if [[ -z "$ID_TOKEN" ]]; then
  echo "FATAL: no identity token. Run: gcloud auth login todd@gigaton.ai"
  exit 1
fi
echo "token length: ${#ID_TOKEN}"
record "0. identity token" "ok"

note "1. Gateway: onboarding manifest"
MANIFEST="$(curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "$GATEWAY/v1/onboarding/manifest")"
STAGES="$(echo "$MANIFEST" | jq -r '.stages | length')"
echo "manifest stages: $STAGES"
if [[ "$STAGES" == "10" ]]; then
  record "1. gateway manifest (10 stages)" "ok"
else
  record "1. gateway manifest" "expected 10 stages, got $STAGES"
fi

note "2. Gateway: per-operator onboarding state"
STATE="$(curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "$GATEWAY/v1/onboarding/state?operator_id=$OPERATOR")"
CUR_STAGE="$(echo "$STATE" | jq -r '.current_stage_id')"
echo "current stage: $CUR_STAGE"
if [[ -n "$CUR_STAGE" && "$CUR_STAGE" != "null" ]]; then
  record "2. gateway state" "ok"
else
  record "2. gateway state" "no current_stage_id in response"
fi

note "3. POST sample intent — stage-0 declare-legal-entity button_click"
INTENT_RESP="$(curl -fsS -X POST \
  -H "Authorization: Bearer $ID_TOKEN" \
  -H "Content-Type: application/json" \
  "$GATEWAY/v1/onboarding/intent" \
  -d @- <<JSON
{
  "operator_id": "$OPERATOR",
  "stage_id": "stage-0-trust-scope",
  "action_id": "declare-legal-entity",
  "intent_type": "button_click",
  "payload": {
    "legal_entity_name": "Carmen Beach Properties LLC",
    "jurisdiction": "MX-QR"
  }
}
JSON
)"
HTTP_OK="$(echo "$INTENT_RESP" | jq -r '.status // empty')"
echo "$INTENT_RESP" | jq .
if [[ "$HTTP_OK" == "ok" || "$HTTP_OK" == "accepted" ]]; then
  record "3. intent POST" "ok"
else
  record "3. intent POST" "unexpected status: $HTTP_OK"
fi

note "4. HME: confirm event emitted"
sleep 2  # let the async emitter flush
HME_EVENTS="$(curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "$HME/v1/events?operator_id=$OPERATOR&event_type=onboarding.intent.captured&limit=5")"
COUNT="$(echo "$HME_EVENTS" | jq -r '.events | length')"
echo "HME events found: $COUNT"
if [[ "$COUNT" -ge 1 ]]; then
  record "4. HME event recorded" "ok"
else
  record "4. HME event recorded" "no onboarding.intent.captured event in HME"
fi

note "5. Re-read state — action should be in completed list"
STATE2="$(curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "$GATEWAY/v1/onboarding/state?operator_id=$OPERATOR")"
COMPLETED="$(echo "$STATE2" | jq -r '.current_stage_actions_completed | join(",")')"
echo "completed actions: $COMPLETED"
if echo "$COMPLETED" | grep -q "declare-legal-entity"; then
  record "5. state reflects completion" "ok"
else
  record "5. state reflects completion" "declare-legal-entity not in completed list"
fi

note "6. decision-engine: targets-readiness still 200"
DE_READY="$(curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "$DE/v1/operators/$OPERATOR/targets-readiness")"
DE_OP="$(echo "$DE_READY" | jq -r '.operator_id')"
if [[ "$DE_OP" == "$OPERATOR" ]]; then
  record "6. decision-engine targets-readiness" "ok"
else
  record "6. decision-engine targets-readiness" "operator_id mismatch: $DE_OP"
fi

note "7. UAE overlay fetch (post-migration)"
UAE_NS="$(curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "https://user-access-engine-rjmcrtvuzq-uc.a.run.app/v1/admin/namespaces/$OPERATOR")"
HAS_OVERLAY_KEY="$(echo "$UAE_NS" | jq 'has("workflow_overlays")')"
echo "has workflow_overlays key: $HAS_OVERLAY_KEY"
if [[ "$HAS_OVERLAY_KEY" == "true" ]]; then
  record "7. UAE overlay column present" "ok"
else
  record "7. UAE overlay column present" "key missing — UAE response model not updated; data is durable but response shape lags. Schedule UAE redeploy."
fi

echo
echo "═══════════════════════════════════════════════════════════════════"
echo "  SUMMARY"
echo "═══════════════════════════════════════════════════════════════════"
for r in "${RESULTS[@]}"; do echo "  $r"; done
echo "───────────────────────────────────────────────────────────────────"
echo "  pass: $PASS   fail: $FAIL"
if [[ "$FAIL" -gt 0 ]]; then
  echo "  STATUS: 🔴 RED — investigate the ❌ lines above"
  exit 1
else
  echo "  STATUS: 🟢 GREEN — onboarding workflow live end-to-end"
fi
```

Run:
```bash
chmod +x /tmp/onboarding_e2e_smoke.sh
/tmp/onboarding_e2e_smoke.sh
```

Expected at full success: 7/7 green, exit 0.

---

## Telemetry to watch (during + 30 minutes after each step)

### Cloud Run health checks

```bash
for svc in user-access-engine intelligence-silo decision-engine; do
  PROJECT=$( [[ "$svc" == "user-access-engine" ]] && echo "gigaton-platform" || echo "carmen-beach-properties" )
  URL="https://${svc}-rjmcrtvuzq-uc.a.run.app/healthz"
  echo "── $svc ($PROJECT) ──"
  curl -fsS -H "Authorization: Bearer $(gcloud auth print-identity-token)" "$URL" | jq -c .
done
```

Expected: each prints `{"status":"ok",...}`.

### decision-engine drift_sentinel — AX-010 signal

The drift_sentinel flags AX-010 (un-applied schema migration) as a MAJ drift
item. Once all three migrations are applied, that signal should clear on the
next nightly sweep (or run it manually):

```bash
ID_TOKEN="$(gcloud auth print-identity-token)"
curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/drift/open" \
  | jq '[.items[] | select(.rule_id | startswith("AX-010"))]'
```

Expected after apply: `[]` (empty array) or items unrelated to these three
migrations.

### Operator-visible: tier promotion

For any operator who has actually completed the Stage 0 + Stage 4 + Stage 9
gates, the gateway state should return `tier` > `"always"`:

```bash
curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  "$GATEWAY/v1/onboarding/state?operator_id=$OPERATOR" \
  | jq '{operator_id, current_stage_id, tier: (.shadow_mode_enabled // false), live_recommend_activated_at, live_auto_execute_activated_at}'
```

Pre-onboarding-completion this stays `false` / `null` — that's expected.
Watch for `shadow_mode_enabled: true` (or non-null `live_recommend_activated_at`)
as the first operator actually walks through the chat-first flow.

### Penrose scoreboard

The two newly-instrumented metrics (`codification_rate` and `decision_velocity`)
should not regress post-apply. Spot-check:
```bash
curl -fsS -H "Authorization: Bearer $ID_TOKEN" \
  https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/penrose/scoreboard \
  | jq '{codification_rate: .codification_rate.value, decision_velocity: .decision_velocity.value, drift_critical_count: .drift_critical_count.value}'
```

`drift_critical_count` should remain `0`.

---

## Rollback plan — at a glance

| Step | Reverse command | What breaks                                                                                          |
|------|-----------------|------------------------------------------------------------------------------------------------------|
| 1    | `alembic downgrade -1` in `user-access-engine`             | Gateway resolver overlay fetch returns 404 → falls back to canonical onboarding manifest. Chat-first still works; no per-operator overlays. |
| 2    | `DROP TABLE` the two intel-silo tables (see §2f)          | `/v1/onboarding/state` reverts to in-process stub. Action ledger lost. Activation gates stuck at `tier=always`. |
| 3    | `DROP TABLE` the two decision-engine tables (see §3f)     | Stage 0 axiom acks ephemeral (per-instance), Stage 4 targets non-persistent. PPEME / HME unaffected. |

All rollbacks are safe to perform individually — no cross-migration coupling.

---

## Post-completion

- [ ] Update memory `[[onboarding_workflow_v1_shipped_2026_05_20]]` status line:
      `migrations applied at YYYY-MM-DDTHH:MM:SS-CT`.
- [ ] Confirm `drift/open` no longer reports AX-010 for these three files.
- [ ] (Optional) Trigger UAE + intel-silo + decision-engine redeploys at the
      next scheduled 19:00 CT window to clear any stub-fallback code paths
      and pick up the new response-model fields. Not load-bearing — schema
      is detected dynamically — but cleaner observability.
- [ ] Emit `task_completed` on Pub/Sub topic `gignet-orchestrator`:
      ```bash
      gcloud pubsub topics publish gignet-orchestrator \
        --project=gigaton-platform \
        --message='{"task_id":"apply-onboarding-migrations-2026-05-20","status":"completed","artifacts":["uae-0007","intel-silo-031","decision-engine-002"]}'
      ```

---

*Runbook authored 2026-05-20. Source spec:
`/Users/admin/.claude/projects/-Users-admin/memory/onboarding_workflow_v1_shipped_2026_05_20.md`.
Cloud SQL provisioning decisions:
`decisions_2026_05_20_resume_here_a1_a2_a3.md` §A.3.*
