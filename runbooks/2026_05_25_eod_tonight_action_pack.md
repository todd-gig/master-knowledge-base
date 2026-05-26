# EOD 2026-05-25 — tonight action pack (pre-5-day-freeze)

> **Run order:** §0 (user) → §1 (verify) → §2 (revoke) → §3 (budget alerts) → §4 (strict namespace gate) → §5 (Penrose channels) → §6 (migration 004) → §7 (gigaton-engine-pg post-provision) → §8 (5-command onboarding verification) → §9 (deploys, if GHA fixed).

---

## §0 — User actions (no terminal — must be done first)

1. **GHA billing** — https://github.com/settings/billing/payment_information + /spending_limit. Set Actions to ≥ $20/mo. Confirm no "Failed" banner.
2. **EU operator policy decision** — for beta tomorrow, restrict signup to non-EU until `DELETE /v1/operators/{id}` exists. (Or accept GDPR risk explicitly.)
3. **Beta openness model decision** — invite-only with cap N ≤ 25, or open signup form? Audit recommended invite-only week-1.

## §1 — Reauth + sanity (run first in fresh terminal)

```bash
gcloud auth login
gcloud auth application-default login
gcloud config set account todd@gigaton.ai
gcloud auth list   # confirm * todd@gigaton.ai
```

Smoke gateway + verify it picks up our changes:
```bash
curl -sS https://gigaton-platform.web.app/v1/healthz | jq '.aggregate_status, .ok_count, .total_count'
```

## §2 — Revoke orphan persona-engine SA key `36679d3a…`

Per `[[persona_engine_sa_key_rotation_2026_05_22]]` the orphan key was kept active until +7d decision (2026-05-29). Beta launches before that. Revoke now:

```bash
# Identify the orphan key (should match prefix 36679d3a)
gcloud iam service-accounts keys list \
  --iam-account=persona-engine-gha-deployer@gigaton-platform.iam.gserviceaccount.com \
  --project=gigaton-platform \
  --format='table(name,validAfterTime,disabled)'

# Once confirmed prefix matches:
KEY_ID="36679d3a..."   # paste full key id from output above
gcloud iam service-accounts keys delete "$KEY_ID" \
  --iam-account=persona-engine-gha-deployer@gigaton-platform.iam.gserviceaccount.com \
  --project=gigaton-platform
```

Cancel the calendared decision event (`jd0oo089178epleb0v4i43ut40` for 2026-05-29) afterward.

## §3 — GCP billing budget alerts (both projects, 50/80/100%)

> Beta opens to potentially unknown N; without project-level cap, a runaway loop bills uncapped.

```bash
# Get the billing account
gcloud billing accounts list --format='value(name)' | head -1
# → e.g. billingAccounts/0XXXXX-YYYYYY-ZZZZZZ
BILLING_ACCT="billingAccounts/REPLACE-ME"

# Pick a monthly cap (USD); audit suggests starting at $500/mo while beta is small
MONTHLY_USD=500

for PROJ in gigaton-platform carmen-beach-properties; do
  gcloud billing budgets create \
    --billing-account="$BILLING_ACCT" \
    --display-name="beta-cap-$PROJ" \
    --budget-amount="${MONTHLY_USD}USD" \
    --threshold-rule=percent=0.5 \
    --threshold-rule=percent=0.8 \
    --threshold-rule=percent=1.0 \
    --filter-projects="projects/$PROJ" \
    --all-updates-rule-pubsub-topic="" \
    --notifications-rule-monitoring-notification-channels=""
done
```

Verify in console: https://console.cloud.google.com/billing/.../budgets

## §4 — Flip namespace admin gate strict (UAE env var)

```bash
# Set UAE_REQUIRE_CAPABILITIES=true (the audit'd "soft gate" → "strict")
gcloud run services update user-access-engine \
  --project=gigaton-platform --region=us-central1 \
  --update-env-vars=UAE_REQUIRE_CAPABILITIES=true

# Verify
gcloud run services describe user-access-engine \
  --project=gigaton-platform --region=us-central1 \
  --format='value(spec.template.spec.containers[0].env)' | grep UAE_REQUIRE
```

This restarts UAE on a new revision (~30s). Then smoke a cross-namespace probe expects 403:
```bash
TOKEN="<carmen-beach operator JWT>"
curl -sS -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Client-Namespace: nonexistent-operator" \
  https://gigaton-platform.web.app/v1/operators/nonexistent-operator/state
# expect 403
```

## §5 — Wire 2 Penrose alert notification channels

Per `monitoring/penrose_alerts.runbook.md` §9, channels still pending for: drift_critical, decision_velocity_p50.

```bash
# Create email channel (if not exists)
CHANNEL_ID=$(gcloud beta monitoring channels list \
  --project=gigaton-platform \
  --filter='labels.email_address=todd@gigaton.ai' \
  --format='value(name)' | head -1)

if [ -z "$CHANNEL_ID" ]; then
  gcloud beta monitoring channels create \
    --project=gigaton-platform \
    --display-name='todd email' \
    --type=email \
    --channel-labels=email_address=todd@gigaton.ai
fi
# Then update the 2 Penrose alert policies to attach $CHANNEL_ID via console or
# alpha monitoring policies update — exact policy IDs in monitoring/penrose_alerts.runbook.md
```

## §6 — Apply migration 004 to decision-engine-pg

```bash
cloud-sql-proxy carmen-beach-properties:us-central1:decision-engine-pg --port 5435 &
PROXY_PID=$!
sleep 4

PGPASSWORD="$(gcloud secrets versions access latest \
  --secret=decision-engine-pg-root-pw \
  --project=carmen-beach-properties)" \
psql -h localhost -p 5435 -U postgres -d decision_engine -w \
  -f /Users/admin/Documents/GitHub/decision-engine/migrations/004_industry_catalogs.sql

kill $PROXY_PID

# Smoke — should NOT return note:stub after migration
curl -sS "https://gigaton-platform.web.app/v1/operators/carmen-beach/industry-process-triage" | jq '.'
```

## §7 — gigaton-engine-pg post-provision (DB + user + secret)

Per `[[RESUME_HERE_2026_05_25_session_handoff]]` §2 — three commands still pending after Friday's Cloud SQL instance creation:

```bash
gcloud sql databases create gigaton_engine \
  --instance=gigaton-engine-pg \
  --project=carmen-beach-properties

APP_PW="$(openssl rand -base64 32)"
gcloud sql users create gigaton_engine \
  --instance=gigaton-engine-pg \
  --project=carmen-beach-properties \
  --password="$APP_PW"

gcloud secrets create gigaton-engine-pg-app-pw \
  --project=carmen-beach-properties \
  --replication-policy=automatic
printf "%s" "$APP_PW" | gcloud secrets versions add gigaton-engine-pg-app-pw \
  --project=carmen-beach-properties \
  --data-file=-
unset APP_PW

# Verify
gcloud sql databases list --instance=gigaton-engine-pg --project=carmen-beach-properties
gcloud sql users list --instance=gigaton-engine-pg --project=carmen-beach-properties
gcloud secrets versions list gigaton-engine-pg-app-pw --project=carmen-beach-properties
```

> Not on Multipli critical path; required prerequisite for billing build per ADR §B3.

## §8 — Re-run 5-command onboarding verification chain

Per `[[onboarding_workflow_v1_completion_verified_2026_05_22]]` — the canonical re-verify after any deploy. Replace `OPID` with a fresh test-operator id.

```bash
OPID="smoke-$(date +%s)"
GW="https://gigaton-platform.web.app/v1"

# 1. Manifest
curl -sS "$GW/onboarding/manifest" | jq '.version'
# expect: "1.1.0"

# 2. State for new operator (should bootstrap at stage 0)
curl -sS "$GW/operators/$OPID/onboarding/state" | jq '.current_stage'
# expect: 0 (or stage-0)

# 3. Scope-contract — expect 404 (no contract yet for fresh operator)
curl -sS -o /dev/null -w "%{http_code}\n" "$GW/operators/$OPID/scope-contract"
# expect: 404

# 4. Targets-readiness — must NOT include "note:stub" anywhere
curl -sS "$GW/operators/$OPID/targets-readiness" | jq 'tostring | contains("stub") | not'
# expect: true

# 5. Full intent emit chain — POST a stage-0 intent
curl -sS -X POST "$GW/operators/$OPID/onboarding/intents" \
  -H 'content-type: application/json' \
  -d '{"intent":"begin","stage":0}' | jq '.event_emitted'
# expect: true
```

If ANY step fails → DO NOT open beta.

## §9 — Deploy candidates for tonight (only if GHA billing fixed)

In priority order:

1. **gigaton-gateway** — incorporates the AX-024 secret-version fix + (if we author it tonight) the healthz aggregator fix (token error handling + 403→auth_failed status + remove dead `sie` entry).
2. **human-management-engine** — `IndustryCatalogSubmitted` event type (PR #40 merged, deploy blocked since 2026-05-22).
3. **gigaton-ui-system** — `IndustryCatalogFormAffordance` for Stage 5 (PR #35 merged, deploy blocked since 2026-05-22).

If GHA stays blocked but gcloud is up, fallback path is direct Cloud Build from local clones:
```bash
# From the relevant repo dir on `main`:
gcloud builds submit --config=cloudbuild.yaml --project=gigaton-platform .
```
(Bills to GCP, not GitHub Actions — bypasses the billing block. Per `[[session_handoff_2026_05_20_phases_c_to_g.md]]` §RESUME 2026-05-25.)

---

## Done = beta-launch tomorrow conditional GO criteria met

- [ ] §0 user actions complete
- [ ] §2 orphan key revoked
- [ ] §3 GCP budget alerts armed (both projects)
- [ ] §4 namespace gate strict + cross-namespace 403 smoke passes
- [ ] §5 Penrose channels wired
- [ ] §6 migration 004 applied (industry-process-triage no longer stub)
- [ ] §7 gigaton-engine-pg DB+user+secret in place
- [ ] §8 5-command onboarding chain all-pass
- [ ] §9 gateway + HME + UI deploys green (if GHA fixed); rev numbers logged

**Beta opens to:** invite-only, cap N ≤ 25 week-1, non-EU only, behind signup form.
