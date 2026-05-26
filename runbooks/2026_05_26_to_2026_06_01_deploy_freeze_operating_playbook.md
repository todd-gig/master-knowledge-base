---
title: Deploy Freeze Operating Playbook — Tue 2026-05-26 → Mon 2026-06-01
audience: Todd (operator mode), any on-call human
window: 5 business days starting 09:00 CT Tue 2026-05-26, ending 17:00 CT Mon 2026-06-01
re_entry: Tue 2026-06-02 09:00 CT
status: ACTIVE
ppim_signature: surface.docs.runbook.deploy_freeze_2026_05_26.v1
serves: foundational_goal_gigaton_engineered_brand_experience
cross_refs:
  - operator_runbook_2026_05_19.md
  - api_reference_2026_05_19.md
  - user_influence_vs_cost_dashboard_spec.md
  - session_handoff_2026_05_22_beta_launch_sprint_complete.md
  - session_handoff_2026_05_25_migration_plan_and_wave2_spec.md
---

# Deploy Freeze Operating Playbook — 2026-05-26 → 2026-06-01

**Goal.** Operate the platform at production quality during the 5-business-day deploy freeze that starts the same day beta operators first arrive. Monitor it. Gather signal. Respond to issues *without* shipping code. Arrive at Tue 6/2 09:00 CT with a ranked queue of what to ship first.

**One-line doctrine for the week:** *Observe first. Roll back before you fix forward. Capture every operator signal. Do not ship.*

---

## 1. The freeze rules

### 1.1 What MAY NOT ship (default: blocked)

- **Features** — no new endpoints, no new affordances, no new manifest stages, no new event types.
- **Refactors** — no "harmless cleanup," no rename PRs, no `requirements.txt` reorderings.
- **Dependency bumps** — no `pip-compile`, no `npm update`, no Docker base-image tag bumps, no Cloud Run runtime version changes.
- **Config touching auth / routing / cost-caps** — no JWT settings, no `routing_table.py` edits, no `operator_quotas.yaml` edits, no KMS key rotations, no Secret Manager version pins outside the exception process, no CORS allowlist edits.
- **DB migrations** — no `alembic upgrade head` against prod. Migrations sitting on `main` from prior weeks stay un-applied unless the exception process is invoked.
- **GHA workflow edits** — no `.github/workflows/*.yml` changes (any edit forces a re-deploy by reference).
- **Docs that change runtime behavior** — e.g., editing `manifests/onboarding_v1.yaml` is a no-go (it ships into the gateway bundle).

### 1.2 What MAY ship (P0 hotfix exception process)

A P0 hotfix is justified only when **all four** of the following are true:

1. Production is producing wrong/unsafe answers (not slow, not ugly — *wrong*).
2. The blast radius affects ≥1 paying or beta-pilot operator *right now*.
3. **Rollback to a prior revision does not resolve it** (see §5 — rollback-first preference).
4. A single-file ≤30-LoC change provably fixes it, with a green CI run.

**Exception process (30-min minimum):**

1. Write the P0 ticket: symptom + affected operator(s) + the failing curl + the proposed diff.
2. Self-review the diff. Confirm no auth/routing/cost-cap surface is touched (if it is — this is not a freeze hotfix, this is an incident response, see §5).
3. Post the ticket + diff to the on-call channel (§3.3). Wait 15 min for any sibling-agent activity flagging conflict.
4. Pin the **current live revision** to 100% on the affected service so auto-deploy does NOT replace it mid-fix:
   ```bash
   gcloud run services update-traffic <service> \
     --to-revisions=<current-live-rev>=100 \
     --project=<project>
   ```
5. Merge the PR. The auto-deploy creates a new revision but with 0% traffic.
6. Smoke the new revision via direct URL (`<rev>---<svc>-<suffix>.a.run.app`).
7. Shift 100% to the new revision.
8. Add the ticket to the 6/2 re-entry queue with `hotfix: applied 5/2X` so we audit the bypass.

If steps 1–4 take longer than 15 min, you are not in P0 territory. Roll back instead.

### 1.3 What MAY ALWAYS ship

- Cloud Monitoring alert policy edits + dashboard JSON edits (observability is not the runtime path).
- Runbook (this file) + memory edits.
- Email replies to operators, Notion docs, Drive uploads.

---

## 2. Daily morning checklist — 09:00 CT, ~10 min

Open a fresh terminal. Run top-to-bottom. Copy any anomaly into the daily log at `master-knowledge-base/runbooks/freeze_daily_log_2026_05_26.md` (create on Day 1).

### 2.1 Aggregate health

```bash
curl -s https://gigaton-platform.web.app/v1/healthz \
  | jq '{status: .aggregate_status, ok: .ok_count, total: .total_count}'
```

Expected: `{"status":"ok","ok":11,"total":11}`. Anything else → §5 incident response.

### 2.2 Per-engine drill if degraded

```bash
TOKEN=$(gcloud auth print-identity-token)
curl -s -H "Authorization: Bearer $TOKEN" \
  https://gigaton-gateway-sqatlxhlza-uc.a.run.app/v1/healthz \
  | jq '.engines[] | select(.status != "ok") | {name, status, http_code, latency_ms}'
```

### 2.3 Penrose scoreboard — doctrine check

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  https://gigaton-gateway-sqatlxhlza-uc.a.run.app/v1/penrose/scoreboard \
  | jq '{drift_critical: .metrics.drift_critical_count.value, decision_velocity: .metrics.decision_velocity.value, override_rate: .metrics.human_override_rate.value, ovs_variance: .metrics.ovs_variance.value, memory_growth: .metrics.memory_substrate_growth.value}'
```

Red flags:

- `drift_critical > 0` → log; do NOT fix (that's a deploy). Note the rule_id for the 6/2 queue.
- `decision_velocity p50 > 10s` for 30m sustained → investigate per §5 P1.
- `human_override_rate` > 2× yesterday → operators are disagreeing with the system. Capture per §3.3.

### 2.4 Cost-to-date (run every morning, both projects)

```bash
# Current-month spend, gigaton-platform
gcloud billing accounts list  # confirms billing account is healthy
# Replace BILLING_ACCT below with the actual ID
gcloud beta billing projects describe gigaton-platform --format=json | jq '.billingAccountName'

# Per-project current-month run-rate via Cloud Console:
open "https://console.cloud.google.com/billing/linkedaccount?project=gigaton-platform"
open "https://console.cloud.google.com/billing/linkedaccount?project=carmen-beach-properties"
```

LLM spend (the cost line that moves fastest with usage):

```bash
# Per-operator LLM cost yesterday — depends on operator-api / llm_call_cost table
# If a direct view exists, prefer it; otherwise scan logs:
gcloud logging read \
  'resource.type=cloud_run_revision AND jsonPayload.event="llm_call_cost"
   AND timestamp>="'$(date -u -v-1d +%Y-%m-%dT00:00:00Z)'"
   AND timestamp<"'$(date -u +%Y-%m-%dT00:00:00Z)'"' \
  --project=gigaton-platform --limit=1000 --format=json \
  | jq '[.[].jsonPayload | {operator: .operator_id, cost: .cost_usd}]
        | group_by(.operator)
        | map({operator: .[0].operator, total: (map(.cost) | add)})'
```

**Target ceiling for v0 beta**: <$25/day total LLM spend across all operators. Spike > 3× yesterday's number → §3.3 capture + flag.

### 2.5 GHA failure scan (catches sibling agents or auto-cron failures)

```bash
gh run list --limit=20 --json status,conclusion,name,workflowName,createdAt \
  -R todd-gig/gigaton-gateway \
  | jq '.[] | select(.conclusion=="failure" or .status=="failure")'

# Repeat for the active repos:
for repo in human-management-engine decision-engine intelligence-silo user-access-engine \
            ppeme persona-engine gigaton-ui-system master-knowledge-base; do
  echo "=== $repo ==="
  gh run list --limit=10 -R todd-gig/$repo --json conclusion,name,createdAt \
    | jq '.[] | select(.conclusion=="failure")'
done
```

Any failures during freeze are interesting (because nobody should be merging). Log them, investigate the source. Could be: a cron-fired sweep, a scheduled report, a sibling agent making un-coordinated changes (raise immediately in §3.3).

### 2.6 Scheduled job health

```bash
gcloud scheduler jobs list --project=gigaton-platform --format=json \
  | jq '.[] | {name, state, schedule, lastAttemptTime}'

gcloud scheduler jobs list --project=carmen-beach-properties --format=json \
  | jq '.[] | {name, state, schedule, lastAttemptTime}'
```

Expected fired-clean: `weekly-initiative-report-fire` (Sun 20:00 CT), AX-008 nightly sweep (`sweep-executions-job`, 04:00 CT), gignet `orchestrator-trigger-fan-out`.

### 2.7 Dashboards (open the tabs, eyeball)

- Storage/retrieval observability: <https://console.cloud.google.com/monitoring/dashboards/builder/bba97b25-e2b5-48b1-aea6-d92342777d29?project=gigaton-platform>
- Cloud Run service list (gigaton-platform): <https://console.cloud.google.com/run?project=gigaton-platform>
- Cloud Run service list (carmen-beach-properties): <https://console.cloud.google.com/run?project=carmen-beach-properties>
- GHA actions (todd-gig): <https://github.com/todd-gig?tab=repositories&q=&type=&language=&sort=>

What you're looking for: error-rate panel showing < 1% across all engines; p99 latency < 1500ms gateway, < 800ms per-engine; revision counts stable (a new revision appearing during freeze = anomaly).

---

## 3. Daily evening checklist — 17:00 CT, ~10 min

Goal: capture today's usage signal + customer signal + any error trends. Append to daily log.

### 3.1 Usage report — active operators

```bash
# Active operators today (any /v1/* request)
TOKEN=$(gcloud auth print-identity-token)
gcloud logging read \
  'resource.type=cloud_run_revision
   AND resource.labels.service_name=gigaton-gateway
   AND jsonPayload.operator_id!=null
   AND timestamp>="'$(date -u +%Y-%m-%dT00:00:00Z)'"' \
  --project=gigaton-platform --limit=5000 --format=json \
  | jq '[.[] | .jsonPayload.operator_id] | unique | length'

# Decisions processed today
gcloud logging read \
  'resource.type=cloud_run_revision
   AND resource.labels.service_name=decision-engine
   AND jsonPayload.event="decisions.process.complete"
   AND timestamp>="'$(date -u +%Y-%m-%dT00:00:00Z)'"' \
  --project=carmen-beach-properties --limit=2000 --format=json \
  | jq 'length'
```

### 3.2 Connector usage

```bash
# Drive ingest jobs today
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/v1/documentation/jobs?operator_id=__all__&limit=50" \
  | jq '[.jobs[] | select(.started_at > "'$(date -u +%Y-%m-%dT00:00:00Z)'")] | length'

# Outbound WhatsApp sends today (proxy via gateway)
gcloud logging read \
  'resource.type=cloud_run_revision
   AND resource.labels.service_name=mimi-whatsapp
   AND jsonPayload.event="customer.contact.sent"
   AND timestamp>="'$(date -u +%Y-%m-%dT00:00:00Z)'"' \
  --project=carmen-beach-properties --limit=500 --format=json \
  | jq 'length'
```

### 3.3 Error report — 5xx + p99 drift

```bash
# 5xx count last 24h, per-service
for svc in gigaton-gateway decision-engine intelligence-silo user-access-engine \
           ppeme persona-engine human-management-engine; do
  proj=gigaton-platform
  [[ "$svc" == "decision-engine" || "$svc" == "intelligence-silo" ]] && proj=carmen-beach-properties
  cnt=$(gcloud logging read \
    "resource.type=cloud_run_revision
     AND resource.labels.service_name=$svc
     AND httpRequest.status>=500
     AND timestamp>=\"$(date -u -v-1d +%Y-%m-%dT00:00:00Z)\"" \
    --project=$proj --limit=1 --format=json | jq 'length // 0')
  echo "$svc: $cnt 5xx"
done
```

**Target ceiling**: 0 5xx per service per day for v0 beta. >5 in any one service → §5 P2 investigation.

### 3.4 Customer signal capture

**Where issues land (publish these to every beta operator BEFORE 5/26):**

| Channel | URL/handle | Who triages |
|---|---|---|
| Primary: email | `support@gigaton.ai` (forwards to todd@) | Todd, same-day |
| Slack (beta-ops shared workspace) | `#gigaton-beta` | Todd, same-day |
| In-app feedback button (FE shell) | POST → HME `/v1/events` event_type `OperatorFeedbackSubmitted` | Auto-logs to HME |
| WhatsApp number (Carmen ops only) | `+1...` (Twilio sandbox) | mimi-whatsapp inbox |

**Daily capture process**:

1. Triage inbox at 17:00. Each item gets a row in the daily log: `[timestamp] [operator] [channel] [severity P0/P1/P2/P3] [summary] [reproducible? Y/N] [action: reply | rollback | queue-for-6/2]`.
2. P0 → §5 + §1.2 exception process (rare; only if blocking interaction integrity).
3. P1/P2 → reply within 4 business hours with "we see this, root cause TBD, fix planned for 6/2". Capture the curl that reproduces it.
4. P3 → ack within 24h.

### 3.5 End-of-day write-up

Three lines in the daily log:

```
2026-05-2X — Day N of freeze
Health: <ok|degraded> | Active ops: X | Decisions: Y | Cost: $Z | 5xx: N | Errors of note: <list>
Customer signal: <count> P0, <count> P1, <count> P2, <count> P3 | New: <bulleted summaries>
Queued for 6/2: <bulleted items to add to the re-entry queue>
```

---

## 4. Weekly synth — Friday 2026-05-29 EOD

Combine Days 1-4 of the daily log into a single ranked deploy queue for 6/1 morning prep + 6/2 deploy day.

### 4.1 The synthesis output

Create `master-knowledge-base/runbooks/freeze_synth_2026_05_29.md` with:

```
| Rank | Item | Repo(s) | Type (fix/feature/refactor) | Business impact (H/M/L) | Risk (H/M/L) | Reversibility (Y/N — single revision rollback works?) | Source signal (which daily-log entry) |
|------|------|---------|------------------------------|--------------------------|--------------|--------------------------------------------------------|----------------------------------------|
```

### 4.2 Ranking heuristic (impact ÷ risk × reversibility)

1. **First** to ship 6/2: H-impact + L-risk + Y-reversibility fixes (e.g., a copy fix, a missing capability seed row).
2. **Second**: H-impact + M-risk + Y-reversibility (e.g., a Wave 2 PR that's been queued).
3. **Third**: M-impact + L-risk + Y-reversibility.
4. **DEFER** to next week: anything H-risk OR N-reversibility (these need pre-deploy soak + rollback rehearsal).

### 4.3 Hard-stops on the 6/2 queue

Even a top-ranked item is held if:

- Touches auth/routing/cost-caps without a paired rollback rehearsal.
- Carries a DB migration without a written down-migration.
- Is being worked by a sibling agent (check `.cxguy-active-agent` files + open-PR diff for collisions).
- Has not been smoke-tested in a dev/staging env (per [[onboarding_workflow_v1_completion_verified_2026_05_22]] 5-command chain).

### 4.4 Pre-stage the merge order

For each ranked item: identify the dependency chain (e.g., "decision-engine PR #X depends on UAE migration Y"). Write the merge order. Confirm with the team Sun 5/31 EOD that the 6/2 morning queue is locked.

---

## 5. Incident response during freeze

### 5.1 Triage matrix

| Severity | Definition | First response | Time-to-respond |
|---|---|---|---|
| **P0** | Production producing wrong/unsafe data; affected operators cannot use a core surface (chat, /decisions/process, OAuth login, outbound send). | §5.2 rollback first; §1.2 exception process only if rollback can't restore. | 15 min |
| **P1** | Degraded performance (p99 latency > 2× baseline, error rate 1-5%, partial engine unhealthy in `/v1/healthz`). | §5.3 diagnose; capture for 6/2 queue; only rollback if pinned to a recent revision change. | 1 hour |
| **P2** | Cosmetic / UX bug; specific narrow feature broken (one connector failing while others ok); customer-reported but workaround exists. | Reply with workaround; queue for 6/2. | 4 hours |
| **P3** | Feature request; documentation gap; "would be nice." | Ack within 24h; queue for backlog (not 6/2 unless impact is high). | 24 hours |

### 5.2 Rollback-first preference (P0/P1)

**Always check this before considering an exception-process hotfix**:

```bash
# 1. Find the affected service
curl -s -H "Authorization: Bearer $TOKEN" \
  https://gigaton-gateway-sqatlxhlza-uc.a.run.app/v1/healthz \
  | jq '.engines[] | select(.status != "ok")'

# 2. List recent revisions
SVC=<affected-service>
PROJ=<gigaton-platform-or-carmen-beach-properties>
gcloud run revisions list --service=$SVC --project=$PROJ --limit=5 \
  --format="table(name,active,createdTime,deployedRevisionName)"

# 3. Identify the last KNOWN-GOOD (compare against the live-revisions table in operator_runbook_2026_05_19 §10)
# 4. Pin traffic
LAST_GOOD=<rev-from-step-3>
gcloud run services update-traffic $SVC \
  --to-revisions=$LAST_GOOD=100 --project=$PROJ

# 5. Verify
curl -s https://gigaton-platform.web.app/v1/healthz | jq
```

**KNOWN cascade gotcha** (per `operator_runbook_2026_05_19.md` §7): if the broken revision ran `alembic upgrade head` on cold start, the DB version may have advanced. Rolling back may fail with `Can't locate revision identified by '<rev>'`. In that case: do NOT roll back blindly. Either (a) shut the service to its prior image AND write a down-migration, or (b) §1.2 exception-process a fix-forward.

### 5.3 P1 diagnose flow

Per `operator_runbook_2026_05_19.md` §6:

1. `curl /v1/healthz` → identify unhealthy engine.
2. `gcloud run revisions list` → check if the latest revision was recently created (during freeze, this should be NONE; if there's a new one, that itself is anomalous and the answer is rollback).
3. `gcloud logging read ... severity>=ERROR` → root-cause symptom.
4. Hit engine `/health` directly → confirm gateway vs engine layer.
5. Hit Cloud SQL via proxy if DB-suspected.
6. Document: do NOT deploy a fix; log for 6/2 unless P0.

### 5.4 On-call

- **Primary**: Todd. Phone + email + Slack alerts on for the full window.
- **Backup**: explicitly none for this freeze week (beta is small). If Todd is offline: degraded mode is acceptable. P0 escalation = SMS Todd directly.

### 5.5 When is breaking the freeze justified?

Strict gate (all four required):

1. P0 per §5.1, AND
2. Rollback path tried and failed (or cannot apply due to migration cascade), AND
3. Single-file ≤30-LoC fix with provable correctness, AND
4. Affected operator(s) have a contractual SLA we'd breach by waiting until 6/2.

Anything weaker → roll back if possible, otherwise inform the operator + queue for 6/2.

---

## 6. New-user onboarding during freeze

Beta operators arrive Mon 5/25 — Mon 6/1. The platform should *handle* them without code changes.

### 6.1 Where to send new operators

- **Primary URL**: `https://gigaton-platform.web.app/chat?onboarding=stage-0` (the chat-first 10-stage flow shipped 5/20).
- **Login**: Google OAuth at `/v1/oauth/google/login` (Domain-restricted for `@gigaton.ai`; external operators need an admin-issued invite token per `operator_runbook_2026_05_19.md` §3).
- **Backup URL** (until api.gigaton.ai DNS lands): same — `gigaton-platform.web.app` is the beta URL.

### 6.2 Intake (capture BEFORE issuing the invite token)

Required fields (use a Google Form or Notion table — DO NOT build an in-app surface during freeze):

| Field | Why |
|---|---|
| operator name + legal entity | UAE seed row + invoicing |
| contact (email + WhatsApp E.164) | Support routing |
| industry/sub-vertical | Multi-axis tag for [[foundational_modular_replication_via_input_substitution]] |
| geo (country/region) | Multi-axis tag + currency |
| expected use case (1-2 sentences) | Which engines they'll exercise |
| expected daily volume (decisions/messages) | Rate-limit + budget cap seeding |
| current tools (Stripe? Twilio? Drive?) | Connector roadmap signal |
| acceptable feedback channel | Where to triage their issues |
| Penrose target — what does "predictably profitable" mean for them in 30 days? | PPIM signature for their tenant |

Store the form responses in a Drive folder named `Beta intake 2026-05-25/`. The 6/2 deploy queue should reflect what real operators are saying matters.

### 6.3 Admin steps per new operator (manual during freeze)

Per the 4-step pattern in `operator_runbook_2026_05_19.md` §2 — but **DO NOT** ship the gigaton-engine preset PR or UAE catalog PR until 6/2. Instead, on freeze week:

1. Issue invite token via `POST /v1/invites` (UAE).
2. Set rate-limit + budget cap manually via Cloud Run env-var override (NOT a PR) — `gcloud run services update gigaton-gateway --update-env-vars=OPERATOR_<id>_RATE_LIMIT=...` — and revert after 6/2 when the PR'd config lands.
3. Add their namespace via `POST /v1/namespaces` (UAE admin endpoint, runtime call, no deploy).
4. Capture the seed-data requirements for the 6/2 PR queue.

### 6.4 Support channel

Beta operators get one canonical address: `support@gigaton.ai`. Forward to Todd. SLA: 4 business hours for P1-P2, 24h for P3. P0 routes via §5.

---

## 7. KPIs to track during freeze

Five PPIM-grounded metrics. Each has: definition, query, target range, action if out-of-range.

### 7.1 Interaction volume — "is anyone using it?"

- **Definition**: `count(distinct operator_id, request_id)` per day across `/v1/decisions/process`, `/v1/onboarding/intent`, `/v1/messages`, `/v1/memory/search`.
- **Query**: see §3.1 — `decisions today` + sum of intent/message endpoints from gateway logs.
- **Target**: ≥1 active operator/day from Tue onward; ≥10 interactions/operator/day by Friday.
- **Out-of-range low**: nobody's using it — capture signal from §3.4 channels (UX dead-end? login broken?). Out-of-range high: a single operator pinning the platform — rate-limit check + intake-fields review.

### 7.2 Economics — `cost_per_interaction_usd`

- **Definition**: sum(`llm_call_cost` + `third_party_call_cost` if instrumented + Cloud Run egress) ÷ count(interactions) per operator per day. Per [[user_influence_vs_cost_dashboard_spec]] §3 (data backbone — `llm_call_cost` exists; `third_party_call_cost` doesn't yet — for freeze week, LLM-only is acceptable but flag the gap for 6/2).
- **Query**: §2.4 LLM-cost scan ÷ §3.1 interaction count.
- **Target**: <$0.05/interaction averaged across all operators; <$0.50/interaction for the worst single operator.
- **Out-of-range**: investigate `qualification_cost` per [[user_influence_vs_cost_dashboard_spec]] — usually a wrong-model pick (Opus where Sonnet would do). Log; do NOT change selector in flight.

### 7.3 Predictability — `ovs_variance`

- **Definition**: from `/v1/penrose/scoreboard` — 90th-percentile gap between PPEME forecast and actual outcome.
- **Query**: §2.3 jq selector.
- **Target**: variance staying flat or decreasing day-over-day. Step-changes upward signal calibration broke.
- **Out-of-range**: capture the decision_ids that drove the spike; queue for OVS-Calibration replay 6/2.

### 7.4 Brand consistency — `brand_consistency_score` (Penrose #5)

- **Definition**: lower = more coherent voice across channels. Spikes usually correlate with persona-engine edits or chat persona changes.
- **Query**: `curl /v1/penrose/scoreboard/brand_consistency_score`.
- **Target**: hold within ±10% of the Mon 5/25 baseline.
- **Out-of-range**: identify which channel/persona is drifting; capture; no in-flight fix.

### 7.5 Decision velocity — `decision_velocity` (Penrose #3)

- **Definition**: rps + p50/p99 latency for the decision pipeline.
- **Query**: §2.3.
- **Target**: p50 < 3s, p99 < 10s sustained.
- **Out-of-range**: per `operator_runbook_2026_05_19.md` §6 diagnose flow.

### 7.6 BONUS — `operator_onboarding_progress`

- **Definition**: per-operator count of stages_completed (0-10) from `/v1/onboarding/state`.
- **Query**:
  ```bash
  for op in $(gcloud logging read 'jsonPayload.event="OnboardingStageStarted"' --limit=100 --format=json | jq -r '.[].jsonPayload.operator_id' | sort -u); do
    curl -s -H "Authorization: Bearer $TOKEN" \
      "https://gigaton-platform.web.app/v1/onboarding/state?operator_id=$op" \
      | jq "{op: \"$op\", stage: .current_stage_id, tier: .current_tier, realized_usd: .predicted_influence_usd_realized}"
  done
  ```
- **Target**: every new operator advances ≥1 stage in their first 24h. A stuck operator after 48h = signal to capture (§3.4) — UX dead-end in our chat-first workflow.

### 7.7 BONUS — `human_override_rate` (Penrose #2-equivalent)

- **Definition**: count(overrides via `POST /v1/overrides`) ÷ count(decisions auto-executed).
- **Target**: <15% for the first week (expected high while operators recalibrate to the system's choices). Step-changes upward day-over-day = signal.

---

## 8. Anti-patterns to avoid during freeze

Each is a real foot-gun observed in prior sessions or doctrine.

1. **"Just bump the dependency."** Even a patch-version `requirements.txt` change re-pins the Docker image and triggers a new revision. That re-runs migrations. That re-cold-starts every Cloud Run pod. **Don't.**
2. **"Add a feature flag."** A flag is code. A flag's default value is code. A flag's presence in the manifest is a manifest change. **Don't.** If you need behavior off, override via env-var at the Cloud Run service level (runtime call, not a PR).
3. **"Temporarily change Twilio rate config."** Anything touching `operator_quotas.yaml` is auth/routing/cost-caps surface. Per §1.1 — blocked.
4. **"Just one alembic migration — it's IF NOT EXISTS."** No. Migrations make schema bigger or smaller; both directions are risky on a live tenant. Queue for 6/2 and apply via the runbook at `master-knowledge-base/runbooks/apply_onboarding_migrations_2026_05_20.md`.
5. **"Roll forward to fix the rollback."** This is how the 2026-05-19 P0 cascade happened — alembic_version had advanced; rolling back failed; the team tried to fix-forward without writing the down-migration. Pin the latest GOOD revision FIRST, write the down-migration, THEN roll back.
6. **"Suppress the alert — it's noisy."** Penrose alerts that fire during freeze are exactly what we need to capture. Silence = lost signal. Investigate; don't mute.
7. **"Run a sweep manually to test."** AX-008 sweep auto-fires at 04:00 CT. Don't fire a second one during peak operator hours; it competes for Cloud SQL connections.
8. **"Edit the canonical manifest — it's just YAML."** The manifest at `master-knowledge-base/manifests/onboarding_v1.yaml` ships into the gateway bundle at build time. Editing it changes runtime behavior. **Don't.** Per §1.1.
9. **"Add a new operator preset PR — it's just a registry row."** Even a 1-row registry change re-deploys gigaton-engine. Use the runtime path (§6.3) during freeze.
10. **"Touch the KMS key just to rotate one secret."** KMS rotation triggers all Cloud Run services that mount the secret to fail cold-start once they fetch the new version + the consumer hasn't been redeployed. Defer.

---

## 8.5 — Design work to ship during the freeze (parallel track, no deploys)

The freeze is not only an "operate what we have" week — it is *also* the spec/design window for the 30-day product+sales launch arc that begins the same morning the freeze begins. Pure design, content, spec, and Stripe-test-mode work happens in parallel; **none of it touches production deploys** and **none of it falls under §1.1's blocked list** because none of it ships code to Cloud Run.

### 8.5.1 — 30-day macro framing

The 30-day macro goal (starts Tue 2026-05-26, ends ~Wed 2026-06-24) is to build the systems that allow **~50 Multipli-class interactive-experience bundles to be produced + sold + delivered per day**, across all Gigaton companies — Gigaton self-serve SaaS, Ti Solutions managed-service, and any additional operator entities productized as standalone revenue streams. Multipli (per `[[multipli_vendor_growth_engine_sprint_2026_05_22]]`) becomes example #1 of a repeatable product, **not** a one-off engagement. The freeze week's design output (ICPs + pricing + landing pages + customer-journey diagrams + baseline catalogs) is the spec that the 6/2-onward deploy track executes against. If we exit the freeze without this spec, the 50/day automation target slips by a week per missing deliverable.

### 8.5.2 — Spec deliverables checklist by Fri 2026-05-29 EOD

| Day | Deliverable | Output location | Done-when |
|---|---|---|---|
| Tue 5/26 | **ICP definitions per launching entity** — Gigaton SaaS ICP + Ti Solutions managed-service ICP + any additional entity ICPs (one per productized standalone). Each ICP: firmographics, psychographics, trigger events, disqualifiers, "won-when" definition. | `master-knowledge-base/docs/launch/2026_05_26_icp_definitions_per_entity.md` | All entities from `[[entity_ecosystem_registry]]` have a row; the joint Gigaton+Ti Solutions package (per `[[product_service_package_gigaton_ti_solutions]]`) has both delivery-model ICPs separated. |
| Wed 5/27 | **Pricing model per entity, per package** (ADR B2 locked: one price per package — no bespoke per-prospect pricing). Stripe **test-mode** products + prices created (NOT live mode). | `master-knowledge-base/docs/launch/2026_05_27_pricing_model_per_entity.md` + Stripe test-mode dashboard (export the product JSON into the same folder) | Each entity has ≥1 package with a locked price + Stripe test-mode `price_id` recorded; no live-mode product touched. |
| Thu 5/28 | **Landing page copy + page wireframes per entity.** Headline + sub + 3-section body + social proof + CTA. Wireframes can be Figma links or ASCII boxes — the copy is the load-bearing artifact. | `master-knowledge-base/docs/launch/2026_05_28_landing_copy_and_wireframes/<entity>/` | One copy doc + one wireframe artifact per entity. Reviewed against the PPIM signature ("predictably profitable interaction management of an engineered brand experience"). |
| Fri 5/29 | **End-to-end customer journey diagrammed per entity** — signup → payment (Stripe test) → fulfillment (which engines run + which manual steps) → support (where does P0/P1/P2 land for *this entity*). | `master-knowledge-base/docs/launch/2026_05_29_customer_journey_per_entity.md` (one Mermaid diagram per entity, embedded) | Every entity has a single-page diagram naming each step + the system or human that owns it. Hand-offs are explicit (no "magic happens here" boxes). |

EOD Fri the four artifacts are the input to Mon 6/1 launch-prep + the Tue 6/2 deploy queue.

### 8.5.3 — Content production during the freeze

Beyond the four spec deliverables, the freeze is the week to produce the **content substrate** the 50/day pipeline will consume:

- **Industry baseline catalogs — top-10 verticals.** Each is a structured JSON describing the typical operator in that vertical: KPI ranges, common tools, baseline interaction patterns, baseline price points, expected `cost_per_interaction_usd`. These feed Wave 2 variance-aware self-healing (per `[[stage_5_variance_aware_self_healing_spec]]`) so an incoming operator's Stage-5 submission becomes a **variance check** against our model. Without baselines, Wave 2 ships with no comparison surface. **Target: 10 catalogs in `master-knowledge-base/docs/baselines/<vertical>.json` by Fri EOD.**
- **Sample bundle artifacts** — using the manual recipe at `master-knowledge-base/runbooks/2026_05_25_multipli_bundle_manual_production_recipe.md`, produce 3 fully worked example bundles for 3 sample vendors per the Multipli sprint. Output: `master-knowledge-base/launch/sample-bundles/<vendor>/<6-file-set>`. These are the "look what the system produces" attachments for sales outreach.
- **Sales collateral** — one-pager per entity (PDF or Markdown→PDF) summarizing what the entity sells + price + outcome promise + sample bundle link. Lives in `master-knowledge-base/docs/launch/collateral/<entity>/`.

### 8.5.4 — Cross-references

- `[[product_service_package_gigaton_ti_solutions]]` — the joint Gigaton + Ti Solutions go-to-market wrapper; defines the two delivery models (SaaS + managed) that the ICPs + pricing must mirror.
- `[[entity_ecosystem_registry]]` — the canonical list of launching entities; the deliverables checklist iterates this registry.
- `[[universal_connector_hub_architecture]]` — the product surface every entity is selling access to; the landing page copy must align with this single-product framing.
- `[[gignet_auto_trigger_orchestration]]` — the fabric that makes the 50/day automation possible; the customer-journey diagrams must show where orchestrator hand-offs occur.
- `master-knowledge-base/docs/architecture/2026_05_25_interactive_experience_builder_architecture.md` — the architecture doc being written by a parallel agent today; will define the producer pipeline behind the 50/day target. Reference this as the upstream design for the customer-journey "fulfillment" boxes.
- `master-knowledge-base/docs/architecture/2026_05_25_30_day_gigaton_company_launch_roadmap.md` — the 30-day launch roadmap being written in parallel today; the freeze-week design deliverables are its Week-1 inputs.
- `[[multipli_vendor_growth_engine_sprint_2026_05_22]]` — the first concrete bundle use case; freeze-week sample bundles extend this.
- `[[stage_5_variance_aware_self_healing_spec]]` — Wave 2 consumes the industry baseline catalogs produced in §8.5.3.

### 8.5.5 — Anti-pattern: do NOT try to ship the automation during freeze

**Allowed** during freeze week (does not touch Cloud Run, does not violate §1.1):

- Markdown spec files, Mermaid diagrams, ICP docs, pricing docs, baseline JSON catalogs.
- Figma wireframes, Notion drafts, Google Doc copy drafts.
- **Stripe test-mode** products + prices (live mode is OFF-LIMITS — see below).
- Landing page HTML/copy in a static draft folder *not yet wired into any deployed surface*.
- Email outreach drafts queued in Gmail (do not send to live prospects from a system-attached domain yet).

**Blocked** during freeze week (would violate §1.1 even though it feels "just prep"):

- Production code in any repo that, when merged, triggers a Cloud Run redeploy. Even a "tiny" pricing-table seed PR against gigaton-engine = blocked.
- Stripe **live-mode** product/price creation (live mode = auth/cost-caps surface per §1.1; the Stripe API key is a runtime secret in production).
- Wiring the new landing pages into `gigaton-platform.web.app` routing — that's a Firebase Hosting deploy, which is a deploy.
- Editing `master-knowledge-base/manifests/onboarding_v1.yaml` to add a new entity's onboarding stages — per §1.1 the manifest ships into the gateway bundle.
- DNS changes to add a new entity subdomain (e.g., `tisolutions.gigaton.ai`) — defer until 6/2.
- Sending live outbound to prospects from `mimi-whatsapp` or any production-instrumented channel.

The discipline: **design + content + Stripe-test-mode + draft copy ALL FINE; anything that needs a Cloud Run revision or a live-mode credential touches NOT FINE.** When in doubt, ask: "does the next step require pushing to main or rotating a prod secret?" If yes → queue for 6/2 per §4.

---

## 9. Re-entry — Tue 2026-06-02 09:00 CT

Goal: smoke-then-deploy, not deploy-then-smoke.

### 9.1 09:00-09:30 — Pre-deploy smoke (no code changes)

1. Run the full §2 morning checklist. Snapshot of healthz + Penrose + cost.
2. Run the 5-command verification chain from [[onboarding_workflow_v1_completion_verified_2026_05_22]]: manifest + state + scope-contract + targets-readiness no-stub + full intent emit chain.
3. Re-read the Friday synth (§4) + the 5 daily logs. Confirm the ranked queue.
4. Confirm sibling-agent activity: `gh pr list -R todd-gig/<each-repo>` + check `.cxguy-active-agent` files.

### 9.2 09:30-10:00 — First deploy back: ONE PR

Pick the #1-ranked item from the Friday synth. Single PR. Smallest possible scope. The criteria for the first one back:

- **H impact, L risk, Y reversibility** (per §4.2 heuristic)
- Touches exactly **one** repo
- No DB migration
- No auth/routing/cost-cap surface
- Has a green CI run

Merge it. Watch the GHA deploy. Smoke immediately:

```bash
# Aggregate health
curl -s https://gigaton-platform.web.app/v1/healthz | jq '.aggregate_status'

# Specific surface that the PR touched
# e.g. for an HME PR:
curl -s -H "Authorization: Bearer $TOKEN" \
  https://gigaton-gateway-sqatlxhlza-uc.a.run.app/v1/users/<smoke-user>/events?limit=5 | jq
```

### 9.3 10:00-10:30 — Soak window

Watch logs + Penrose for 30 min. Confirm:

- No new 5xx
- No drift_critical step-change
- No latency p99 step-change

### 9.4 10:30+ — Next deploys

Only proceed to PR #2 if #1's 30-min soak is clean. Repeat the smoke-soak loop per PR. **Do NOT** batch-merge the freeze queue. Each PR gets its own smoke + soak.

### 9.5 Migrations come LAST

Any DB migration queued during the freeze (e.g., decision-engine migration 004 per the 5/25 handoff) ships after all non-migration items have cleared. Apply per `master-knowledge-base/runbooks/apply_onboarding_migrations_2026_05_20.md`. Confirm AX-010 founder sign-off recorded BEFORE running.

### 9.6 Post-mortem entry to MEMORY.md

By 17:00 CT 6/2, write a memory: `session_handoff_2026_06_02_freeze_exit.md`. Cover:

- What the freeze week's daily logs surfaced (top 5 signals)
- What shipped on 6/2 + soak results
- What's queued for 6/3-6/6
- Any new doctrine learned from the freeze week (e.g., "manual operator-onboarding env-var override pattern worked / didn't")

---

## Cross-references

- `master-knowledge-base/runbooks/apply_onboarding_migrations_2026_05_20.md` — the canonical migration apply procedure
- `master-knowledge-base/manifests/onboarding_v1.yaml` — canonical onboarding contract (DO NOT EDIT DURING FREEZE)
- `master-knowledge-base/dashboards/storage_retrieval_observability.json` — the JSON for the obs dashboard
- [[operator_runbook_2026_05_19]] — day-to-day ops (this playbook layers on top)
- [[api_reference_2026_05_19]] — endpoint inventory
- [[user_influence_vs_cost_dashboard_spec]] — the surface we'll eventually build to make this checklist a real product
- [[foundational_goal_gigaton_engineered_brand_experience]] — PPIM doctrine; the KPIs in §7 derive from this
- [[session_handoff_2026_05_22_beta_launch_sprint_complete]] — what shipped going into beta
- [[session_handoff_2026_05_25_migration_plan_and_wave2_spec]] — Wave 2 + migration both DEFERRED out of freeze
- [[onboarding_workflow_v1_completion_verified_2026_05_22]] — 5-command verification chain (use at §9.1)

---

*Closing note.* The hardest part of a deploy freeze is not the "don't ship" rule — it's the "capture signal you'd normally fix by shipping" discipline. Every customer complaint, every spike, every degraded curl is a *gift*: it tells you what to ship on 6/2 with the highest possible certainty. Write it down. Don't fix it. The week ends with a ranked queue; the queue is the value.
