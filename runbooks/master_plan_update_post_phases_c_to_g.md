# Master Plan Update — Phases C-G Complete

**Apply this AFTER** `ship_phases_c_to_g.sh` runs cleanly + smoke test passes.
**Reason:** AX-016 doctrine-claim ≠ committed code — don't claim "done" in the canonical plan until live.

**Files to edit (keep in sync per master plan §16):**
- `/Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md` (primary)
- `/Users/admin/Documents/Gigaton-NotebookLLM/02_Master_Project_Plan/00_MASTER_PROJECT_PLAN.md` (mirror — `cp` after primary updated)

---

## §3.1 Live Cloud Run engines — bump gigaton-gateway row

CURRENT:
```
| 5 | **gigaton-gateway** | gigaton-platform | Edge router (`api.gigaton.ai` DNS = NXDOMAIN; use `gigaton-gateway-sqatlxhlza-uc.a.run.app`) + per-engine timeout/retry + rate-limit + budget cap + Client Namespace System | v0.5.0 | self |
```

REPLACE WITH:
```
| 5 | **gigaton-gateway** | gigaton-platform | Edge router at `api.gigaton.ai` + per-engine timeout/retry + rate-limit + budget cap + Client Namespace System + **Phase C webhooks** (`/webhooks/{github,cloudbuild,twilio}` → orchestrator) + **Phase D LLM router** (`POST /v1/llm/call`, Vertex AI Claude+Gemini, OpenAI w/ key, Firestore cost log, second-opinion gate, codification trigger) | v0.6.0 | self |
```

## §3.3 Gignet orchestration substrate — bump from A+B to A-G

CURRENT:
```
### 3.3 Gignet orchestration substrate — LIVE
- **Phase A**: Pub/Sub topic ... + IAM grants on 5 platform SAs + gignet-coordination Python package (25/25 tests pass)
- **Phase B**: 10 trigger rows in Firestore orchestrator_triggers + Cloud Function orchestrator-trigger-fan-out ACTIVE + e2e smoke PASS in 1.7s
- **Net effect:** any agent emits task_completed → within 2s a task_registry row is auto-created for the next downstream task; no duplicate work; no missed handoffs
```

REPLACE WITH:
```
### 3.3 Gignet orchestration substrate — LIVE (Phases A-G)
- **Phase A**: Pub/Sub topic + 2 subs + Firestore Native + IAM grants on 5 platform SAs + `gignet-coordination` Python package (25/25 tests pass)
- **Phase B**: 10 trigger rows in Firestore `orchestrator_triggers` + Cloud Function `orchestrator-trigger-fan-out` ACTIVE us-central1 + e2e smoke PASS in 1.7s
- **Phase C (NEW 2026-05-20)**: 4 external-source adapters → orchestrator events:
  - `/webhooks/github` on gigaton-gateway (PR merged + push + release → `code.merged.*` / `code.pushed.*` / `release.published.*`)
  - `/webhooks/cloudbuild` on gigaton-gateway (build SUCCESS/FAILURE → `deploy.completed.*` / `deploy.failed.*`)
  - `/webhooks/twilio` on gigaton-gateway (messaging status + inbound → `communication.*`)
  - `gignet-activity-emitter` Cloud Function (Firestore `users/{uid}/activity` → `user.action.*`)
- **Phase D (NEW 2026-05-20)**: LLM router in gigaton-gateway `app/llm_router/` — multi-model routing table (8 task classes), Vertex AI Claude/Gemini + OpenAI providers, Firestore `llm_call_cost` telemetry, Jaccard second-opinion gate, codification trigger (50-call streak → `codification.candidate.*`)
- **Phase E (NEW 2026-05-20)**: gignet-local-node v0.3.0 — Pub/Sub subscriber + 15-min heartbeat timer + FastAPI localhost:7878 dashboard + Claude Code hooks (`gignet-session-claim.sh` + `gignet-session-release.sh` at `~/.claude/hooks/`)
- **Phase F (NEW 2026-05-20)**: drift sentinel rules AX-021 (agent commit missing task_id trailer) + AX-022 (orphan task_completed event) + AX-023 (stale claim no heartbeat). Axiom registry now at 23 axioms.
- **Phase G (NEW 2026-05-20)**: Cloud Monitoring dashboard "Gignet Orchestrator Fabric" (8 widgets) + 3 active alert policies (backlog >100 / fan-out errors >5% / gateway 5xx >1%) + 1 inactive pending custom metric (abandoned tasks >5/hr)
- **Net effect:** every external source (GitHub / Cloud Build / Twilio / Firestore activity) emits orchestrator events; every LLM call is cost-tracked + can be routed across models with second-opinion verification; local Claude CLI claims tasks via Firestore lease (no two instances duplicate work); drift sentinel auto-flags doctrine violations on every commit; observability dashboards prove the fabric is alive in real-time
```

## §3.6 Registry drift to reconcile — resolve drift #4 + add 2 new

CHANGES:
- **Drift #4** (api.gigaton.ai NXDOMAIN): mark RESOLVED 2026-05-20 (DNS provisioned + Cloud Run domain mapping live + SSL cert issued)
- **NEW rows to add at end of table:**

```
| 9 | `gignet-activity-emitter-fn` exists on GitHub (new 2026-05-20) but NOT in repo_registry.md | Add row to registry §Cloud Functions |
| 10 | `gignet-local-node` exists on GitHub (v0.3.0 with Phase E integration) but registry says only v0.1.0-installer was on disk | Update registry §Local-node, bump version, note hooks at ~/.claude/hooks/ |
```

## §8.D Edge + Coordination — add 2 new rows

ADD after the existing "Gignet orchestration fabric" row:

```
| gigaton-gateway — Phase C webhooks (NEW) | `/webhooks/{github,cloudbuild,twilio}` + Cloud Function `gignet-activity-emitter` for Firestore activity | "Every external event becomes a first-class orchestrator trigger" | Auto-chained work from every system the operator integrates; no manual relay |
| gigaton-gateway — Phase D LLM router (NEW) | Multi-model routing (Vertex AI Claude+Gemini, OpenAI) + per-call cost log + second-opinion gate + codification trigger | "Right model for the right task, with cost visibility per call" | Defensible LLM spend + falsifiable model-quality claims |
```

## §9 Status — move 4 items from partial to working + add Phase C-G working entries

WORKING — add to existing list:
- **Orchestrator fabric end-to-end** — GitHub PR merge → webhook → Pub/Sub event → fan-out → task_registry row spawned within 2s
- **LLM call cost telemetry** — every `/v1/llm/call` writes to Firestore `llm_call_cost` (queryable via Cloud Console + dashboard widget)
- **Local Claude CLI lease** — `~/.claude/hooks/gignet-session-claim.sh` auto-claims tasks from Firestore on session start (requires gignet-coordination installed on system Python OR venv wrapper)
- **Drift detection** — `pip install -e .[drift-firestore]` activates AX-022 + AX-023 in any scheduled drift scan
- **Orchestrator observability** — Cloud Monitoring dashboard "Gignet Orchestrator Fabric" + 3 alert policies firing to todd@gigaton.ai

PARTIALLY WORKING — UPDATE:
- "WhatsApp self-serve connector" → no change, still pending `activate-connector-api.sh`
- "Client Namespace System" → no change, still pending UAE migration
- **REMOVE** "6 Penrose metrics" line — Phase D cost log activates `revenue_per_human_touch` once first paid intakes complete
- **REMOVE** "Carmen Beach Phase 4" line if it's been closed (verify before applying)

## §10 Waves — flip Wave 1 + Wave 2 status

WAVE 1 (Close the Doctrine Layer / Phase 0 close):
- AX-021/022/023 drift rules ✅ landed 2026-05-20 via PR todd-gig/decision-engine#62

WAVE 2 (Activate the Connector Hub):
- ✅ Phase C webhook routes — GitHub + Cloud Build + Twilio shipped
- ✅ Phase C-4 Firestore-activity emitter shipped
- ✅ Phase D LLM router shipped
- ⏳ Stripe / Gmail / Calendar self-serve wizards — STILL PENDING (Phase C scoped to vendor events not full self-serve)
- ⏳ Connector Catalog bulk hydration — STILL PENDING
- ⏳ Universal cost telemetry `third_party_call_cost` — PARTIALLY DONE (LLM cost log shipped; non-LLM vendor cost log still pending)

NEW WAVE 1.5 — Orchestration Fabric Build-out (slot between Wave 1 and Wave 2):
```
### Wave 1.5 — Orchestration Fabric (Phases A-G of gignet_auto_trigger_orchestration)
- ✅ Phase A (2026-05-20T02:15Z): Pub/Sub topic + task_registry Firestore + gignet-coordination package
- ✅ Phase B (2026-05-20T03:51Z): orchestrator_triggers Firestore + orchestrator-trigger-fan-out Cloud Function
- ✅ Phase C (2026-05-20 EVE): 4 external source adapters (GitHub + Cloud Build + Twilio + Firestore activity)
- ✅ Phase D (2026-05-20 EVE): LLM router + cost telemetry + second-opinion + codification
- ✅ Phase E (2026-05-20 EVE): gignet-local-node integration + Claude Code hooks + localhost dashboard
- ✅ Phase F (2026-05-20 EVE): 3 new drift rules AX-021/022/023
- ✅ Phase G (2026-05-20 EVE): Cloud Monitoring dashboard + 3 alert policies
- **Fabric net effect**: any external event (PR merge, build complete, payment, message, user activity) becomes a first-class orchestrator trigger; any LLM call is cost-tracked + routed; any local Claude session claims work via Firestore lease; doctrine drift auto-detected; observability proves the fabric is alive.
```

## §13 Active decisions — strike all 3

A.1 / A.2 / A.3 are all RESOLVED per session_handoff_2026_05_20_a1_gixg_bugs_b1.md. Strike this section or move to a §13.x Historical decisions appendix.

## §14 Reconciliation record — add new entry

Add:
```
### Phases C-G shipped — 2026-05-20 EVE
4 PRs merged across 3 repos + 1 new Cloud Function repo + 1 follow-up cloudbuild fix + 1 cosmetic cleanup PR. All 201 new tests passing. See [[session_handoff_2026_05_20_phases_c_to_g]] for the full implementation report.
```

## Apply commands (after ship_phases_c_to_g.sh runs cleanly)

```bash
# 1. Verify the deploy is healthy
curl -sI https://api.gigaton.ai/v1/healthz | head -3
gcloud functions describe gignet-activity-emitter --region=us-central1 --project=gigaton-platform --format='value(state)'
gcloud monitoring dashboards list --project=gigaton-platform --format='value(displayName)' | grep -i orchestrator

# 2. Apply the §3-§14 edits above to:
#    /Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md
# (use Edit tool with the exact OLD → NEW snippets above)

# 3. Mirror to NotebookLM (per master plan §16 update protocol):
cp /Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md \
   /Users/admin/Documents/Gigaton-NotebookLLM/02_Master_Project_Plan/00_MASTER_PROJECT_PLAN.md

# 4. Update repo_registry.md to add gignet-activity-emitter-fn + bump gignet-local-node entry

# 5. Bump auto-memory MEMORY.md description of session_handoff_2026_05_20_phases_c_to_g.md
#    from "4 PRs OPEN" → "4 PRs MERGED + Phases C-G LIVE in prod"
```
