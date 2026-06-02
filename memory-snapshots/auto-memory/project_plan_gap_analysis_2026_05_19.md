---
name: project-plan-gap-analysis-2026-05-19
description: "Honest, dense gap analysis against the canonical Gigaton master_project_plan. Explicit named items not yet complete, implicit doctrine-to-code gaps, and concepts missing from the master plan itself. No sales rosiness."
metadata: 
  node_type: memory
  type: project
  priority: 1
  established: 2026-05-19
  status: ACTIVE — supersedes prior gap analyses
  serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
  ppim_interaction: meta — measures plan-to-reality drift
  ppim_economics: identifies ~$M of build-out work; quantified session-count estimates inform Tier-2/3/4 sprint planning
  ppim_predictability: "HIGH — empirical against today's deploy snapshot (operational_state_snapshot_2026_05_19)"
  ppim_brand_dimension: coherence (honesty in the plan-vs-reality delta)
  lifecycle_state: canonical
  state_set_at: 2026-05-19
  state_set_by: gap-analysis-author
  originSessionId: cc574db0-93f4-4776-b0fe-dc7253ec52fc
promoted_from: project_plan_gap_analysis_2026_05_19.md
promoted_at: 2026-06-02T20:13:25Z
---

# Project Plan Gap Analysis — 2026-05-19

> Pace benchmark: today's session shipped ~50 PRs across 11+ repos with 8 engines deployed twice, 2 net-new services scaffolded (connector-api, mimi-whatsapp), and one doctrine win (empirical 4-operator modular replication validation). That is ONE strong session. Session-count estimates below assume that pace.

> Method: cross-referenced `master_project_plan.md` §1-10, `standalone_bundle_net_new_concepts.md` (10 concepts), `assessment_and_improvement_plan_2026_05_19.md` (Tier 1-5), `operational_state_snapshot_2026_05_19.md` (empirical health), `penrose_falsification_doctrine.md` (8-metric scoreboard), `universal_connector_hub_architecture.md` (the product), `gignet_local_node_capability_ladder.md` (7 tiers), `user_influence_vs_cost_dashboard_spec.md` (PPIM observability), and the active work registry.

---

## Section 1 — Specifically-named project-plan items NOT YET COMPLETE

Items the master plan explicitly names and that have NOT cleared their DONE bar.

### 1.1 Phase 0 close — Constitution ratification ceremony
- **State**: ~80% done. `master-knowledge-base/CONSTITUTION.md` exists as `v1.0.0-draft`; Axiom Registry shipped (20 axioms); Memory Lifecycle State Machine migration tagged 244 files.
- **What completion looks like**: Triad sign-off ceremony flips `Status: DRAFT` → `RATIFIED`; suffix `-draft` removed; v1.0.0 frozen; small follow-up PR.
- **Blocker**: Triad sign-off ceremony (Todd alone, Matt + Bella assumed window expired 2026-05-24 — see `triad_signoff_assumed_window.md`).
- **Effort**: 1 session.
- **Cite**: `master_project_plan.md §4 item 10`, `standalone_bundle_net_new_concepts.md CONCEPT 10`.

### 1.2 Phase 2 close — Decision Execution Engine deployed to production
- **State**: Concept 1 PR #57 MERGED to `decision-engine`. Module + table schema + 3 action types (`email.send`, `task.create_clickup`, `notification.slack`) exist on `main`. NOT deployed; migration `_decision_execution_engine.py` NOT applied to Cloud SQL.
- **What completion looks like**: every `decision_records` row writes a paired `execution_records` row with `outcome_event_id` link; OVS-Calibration replay closes the loop; first 50 decision→execution pairs verified.
- **Blocker**: gcloud auth expiry + waiting for next decision-engine deploy window; PR #51/52/54 also queued behind the same SA-bootstrap.
- **Effort**: 1 session to deploy + apply migration; 2-3 sessions to instrument 50 real execution traces (requires production decision traffic, which is currently 0).
- **Cite**: `master_project_plan.md §5 Phase 2`, `standalone_bundle_net_new_concepts.md CONCEPT 1`.

### 1.3 Phase 1 deepening — EO System hydration
- **State**: Concept 3 PR #21 MERGED to `intelligence-silo`. Schema (`ethnographic_objects`, `eo_research_tasks`, `eo_router_decisions`) on main; code present. Zero EOs hydrated.
- **What completion looks like**: 100 EOs hydrated from existing Source Registry transcripts (Carmen Beach owner-call summaries, operator interviews); first EO cluster publishes a `research_task` automatically.
- **Blocker**: Source Registry is wired but EMPTY (per snapshot: 0 episodes, 0 patterns, daemon NOT running). Need ingest before hydration. Drive OAuth is live but no documents flowing through.
- **Effort**: 3-4 sessions (1 to ingest Source Registry, 1 to hydrate, 1-2 to wire self-healing research-task loop).
- **Cite**: `master_project_plan.md §5 Phase 1`, `standalone_bundle_net_new_concepts.md CONCEPT 3`.

### 1.4 Phase 3 — Revenue Engine MVP (productized offers)
- **State**: ~25% done. `sales-operating-system` shipped with PricingClient bridge; Carmen Beach Phase 3 partial. ZERO productized offers with intake → namespace → offer → payment → fulfillment running end-to-end.
- **What completion looks like**: 3-5 productized offers live with paid intake forms + automated fulfillment + revenue dashboard rows; first 10 paid intakes complete.
- **Blocker**: No payment connector deployed (Stripe is a roadmap card on `/connectors`); Carmen Beach Phase 4 blocked on UAE capability seed; no Experience Engineering Equation runtime path (Concept 5 merged but not deployed).
- **Effort**: 8-12 sessions. This is the largest single block of business work in the plan.
- **Cite**: `master_project_plan.md §5 Phase 3`, `predictably_profitable_experience_management_engine.md §How sub-engine 4`.

### 1.5 Phase 4 — Client Namespace System wired
- **State**: ~40% done. Concept 7 PR #23 MERGED to `gigaton-gateway`. 5 namespaces seeded. **PR #23 deliberately did NOT wire `NamespaceMiddleware` into the main app router.** No request currently carries `X-Client-Namespace`.
- **What completion looks like**: `app.add_middleware(NamespaceMiddleware)` lands; every cross-engine call carries the header; per-namespace memory + retrieval policies enforce isolation; ≥2 namespaces operate concurrently with disjoint outputs.
- **Blocker**: middleware wiring follow-up PR; First Principles Variable Registry (Concept 2) consumer wiring; client_namespaces table migration not yet applied.
- **Effort**: 2-3 sessions to wire + 1 session to validate cross-namespace isolation.
- **Cite**: `master_project_plan.md §5 Phase 4`, `standalone_bundle_net_new_concepts.md CONCEPT 7`.

### 1.6 Phase 5 — Operator Dashboard (full surface)
- **State**: ~35% done. `gigaton-ui-system /dashboard` + `/founder/*` + `/owner/*` partially shipped. Connector Hub grid renders 8 cards (2 live, 6 roadmap). Penrose widget present (2/8 with live data). NO approval queue with deployment status. NO real-time Universal Cost telemetry rollup. NO per-operator Penrose card.
- **What completion looks like**: operator sees approval queue, connector status, cost rollup, Penrose card, Initiative pipeline ALL in one page in "dashboard-driven daily operating" mode.
- **Blocker**: `third_party_call_cost` table doesn't exist yet (LLM costs only); 6 connectors are roadmap; Penrose substrate has 6 metrics at zero; HME GIXG L7c queue exists but isn't aggregated into the operator dashboard surface.
- **Effort**: 6-8 sessions.
- **Cite**: `master_project_plan.md §5 Phase 5`, `user_influence_vs_cost_dashboard_spec.md §Dashboard surfaces`.

### 1.7 Phase 6 — Repeatable Productization (second operator onboarded via templates only)
- **State**: ~30%. Modular replication EMPIRICALLY validated today via 4-operator × 4-engine matrix (`empirical_modular_replication_validation_2026_05_19.md`). But the validated operators are `surf-school-costa-rica` SYNTHETIC + `liquefex`/`incontekst` REGISTRATION-ONLY placeholders. No second operator is operating against the platform in production.
- **What completion looks like**: a second real operator (Liquefex or other) onboarded using ONLY templates — no engine code change — and serves traffic for 30 days.
- **Blocker**: `gigaton-engine`'s template system (`bin/emit-client.sh` in `platform-master` repo) is v0.0.1 scaffold; no productized SOPs / offer catalogs / implementation kits exist.
- **Effort**: 10+ sessions. This is gated on (1) finishing Carmen Beach Phase 4 (proves first vertical works end-to-end) AND (2) deciding which second operator goes first.
- **Cite**: `master_project_plan.md §5 Phase 6`.

### 1.8 Phase 7 — Commercial Scale (contribution + affiliate + licensing)
- **State**: ~10%. Concept 4 (Value of Human Contribution Matrix) PR #31 MERGED to HME (the migration that caused tonight's P0 incident — `0008_contribution_records.py`). Contribution table exists in HME DB but no contributions recorded. No affiliate payout cycle. No SDK. No machine-readable licensing schemas.
- **What completion looks like**: contributor compensation runs on the Matrix; first affiliate payout cycle executes; SDK published; licensing contracts use machine-readable schemas.
- **Blocker**: ALL OF PHASE 6 + Carmen Beach Phase 3 must complete first (need real revenue + real contributors to compensate). Multi-tenant billing infrastructure doesn't exist.
- **Effort**: 15-20 sessions. Truly aspirational.
- **Cite**: `master_project_plan.md §5 Phase 7`, `standalone_bundle_net_new_concepts.md CONCEPT 4`.

### 1.9 §8 top-of-mind item — Connector Catalog hydration to ~30 connectors
- **State**: ~15%. Catalog exists as 8 FE cards; only WhatsApp + Drive are LIVE; other 6 are roadmap-labeled. Backend `/v1/connectors/catalog` endpoint planned but not shipped (page uses `connectorsCatalogFallback.ts`).
- **What completion looks like**: ~30 connectors with YAML seeds in `data/connectors/{connector_id}.yaml`; loader hydrates `connectors_catalog` at deploy; FE renders from BE.
- **Blocker**: each connector requires its own adapter; current pattern (mimi-whatsapp + connector-api) is canonical but connector-api is BLOCKED on `@carmen/db` TS build issue (see session handoff §"Connector-api deploy attempt — blocked").
- **Effort**: 1 session to fix connector-api TS build, then ~1 session per 3-5 connectors. ~7-8 sessions total.
- **Cite**: `master_project_plan.md §8 item 5`, `universal_connector_hub_architecture.md §A`.

### 1.10 §8 top-of-mind item — Universal cost telemetry `third_party_call_cost` table
- **State**: 0%. Pub/Sub topic exists; the table does not exist. LLM costs are captured (`llm_call_cost` migration 030); Stripe/Twilio/Slack/OTA/Drive costs are INVISIBLE.
- **What completion looks like**: table created via Alembic migration; `shared/third_party_cost.py` helper imported by every connector adapter; every external call writes a row.
- **Blocker**: connector-api deploy must land first (it owns credential vault that drives connector adapters); SIE-owned migration must apply.
- **Effort**: 2-3 sessions (one for migration + helper; one for wrapping first 3 high-volume vendors; one to validate cost telemetry flowing).
- **Cite**: `master_project_plan.md §8 item 6`, `user_influence_vs_cost_dashboard_spec.md §Data backbone gaps`.

### 1.11 Carmen Beach Phase 4 (the perennial blocker)
- **State**: Per `carmen_beach_phase_4_preflight_findings_2026_05_12.md`, plan targets wrong role enum (UserRole 5-role is dead code; actual prod is AuthRole OWNER/AFFILIATE/OPERATOR); UAE capability seed missing all carmen-beach.* policies. UAE PR #14 (today) seeded `capabilities_catalog` with `operator_id` + tags JSONB — partial unblock. Phase 4 not yet kicked off.
- **What completion looks like**: 7-step remediation in preflight findings runs; new role enum applied; capability policies seeded; Carmen Beach FE/BE consume `operator_context: carmen-beach` end-to-end.
- **Blocker**: gcloud auth + UAE redeploy with new seed + Carmen Beach apps reading from the new endpoints.
- **Effort**: 3-4 sessions.
- **Cite**: `master_project_plan.md §3 "What's deployed but unfinished"`, `assessment_and_improvement_plan_2026_05_19.md Tier 3.3`.

### 1.12 GHA auto-deploy bootstrap (decision-engine + ppeme)
- **State**: Workflows merged (`decision-engine` PR #53, `ppeme` PR #23) but require one-time SA bootstrap per `docs/AUTO_DEPLOY_SETUP.md`. Four merged PRs (DE #51/#52/#54, PPEME #22) sit in main but unshipped.
- **What completion looks like**: SA created, secrets installed, next merge auto-ships.
- **Blocker**: user-side one-time terminal commands.
- **Effort**: <1 session (≤30 min user time).
- **Cite**: `session_handoff_2026_05_19_master.md §8 MEDIUM item 5`.

### 1.13 Penrose alerts wiring (data → policies → channels)
- **State**: 2 of 8 metrics emit LIVE data (decision_velocity #3, memory_substrate_growth #8). YAML policies exist in `decision-engine/monitoring/penrose_alerts.runbook.md` but NOT applied to Stackdriver. No notification channels created.
- **What completion looks like**: 2 monitoring notification channels created, 3 alert policies applied; first alert fires on a real degradation.
- **Blocker**: user-side gcloud commands (Section 8 item 3 of session handoff).
- **Effort**: <1 session.
- **Cite**: `session_handoff_2026_05_19_master.md §7 + §8`.

---

## Section 2 — Implicit gaps: concepts in doctrine, no implementation

### 2.1 Penrose metrics 4-7 — engine wiring exists, data substrate empty
- **Status**: Metrics #4 counterfactual_uplift, #5 brand_consistency_score, #6 operator_onboarding_cost, #7 predictability_bound all have engine wiring + formula. None have flowing data. Per snapshot: ALL 8 scoreboard signals currently `neutral`; only `drift_critical_count = 0` is a real value.
- **What's missing**: pilot traffic + the monitoring channel setup. Specifically: PPEME RPO-01 counterfactual sim (PR #22) is merged but not deployed; brand_dimensions table seeded only with 5 originals (system-proposed not wired); operator_onboarding_cost has empirical measurement (60/120/0 LoC) but no scheduled emit; predictability_bound awaits BFT state-vector samples.
- **Effort to first real data**: 4-6 sessions.
- **Effort to scoreboard meaningfulness**: 10+ sessions (requires real production decision traffic).

### 2.2 Universal Connector Hub — 6 of 8 cards are roadmap
- **Status**: WhatsApp (`wired:false` until connector-api deploys) + Google Drive LIVE. Stripe, Gmail, Calendar, GitHub, Airbnb, Google Analytics are roadmap-labeled cards with no adapter code.
- **What's missing**: 6 adapters following the WhatsApp pattern (operator_credentials row + `/connect /test /disconnect /status` endpoints + FE setup wizard + gamification hook).
- **Effort**: ~1.5 sessions per connector once connector-api lands; 9-12 sessions total.

### 2.3 Gignet Local Node Tiers 2-7 (only Tier 1 is shipping)
- **Status**: Per assessment Tier 4.2: gignet-local-node + installer FROZEN 11 days at v0.1.0 scaffold. Tier 0 (Installed) maybe done; Tier 1 (Reading Eyes — fs.list/read/search) NOT shipped end-to-end. Tiers 2-7 have ZERO code.
- **Specific missing tiers**: Tier 2 Local Mind (SLM hardware probe + slm.classify/summarize/draft/embed/cache.warm); Tier 3 Writing Hand (fs.write/move/delete_to_trash + audit.review); Tier 4 Connected Tools (Outlook/Word/Excel/Browser/QuickBooks dynamic MCP discovery); Tier 5 User-Identity Comms (slack.send/email.send/calendar.write MFA-gated); Tier 6 Autonomous Loops (loop.schedule/budget/review/pause); Tier 7 Mesh Node (multi-machine dispatch).
- **Effort**: Tier 1 close ~2 sessions; Tier 2 ~4 sessions; Tier 3-7 ~20+ sessions.

### 2.4 LiquiFex + InContekst real pilots
- **Status**: REGISTRATION-ONLY per Tier 5.3. Both have rows in `gigaton-engine operator_defaults`, UAE `capabilities_catalog`, gateway `operator_quotas.yaml`. ZERO code surface; ZERO vertical apps; placeholder zeros for economics fields (`_v0_placeholder: true`).
- **What's missing for Liquefex**: real economics fill-in (note_issuance_usd / cagr_target / coupon_rate); Life Settlement OS vertical scope; financial-instrument product class added to GigatonDAG.
- **What's missing for InContekst**: real economics (mrr_usd / cac_usd / monthly_churn_rate / target_acv); MMM SaaS scope; SaaS_subscription product class.
- **Effort**: 8-12 sessions per vertical for v0 pilot. Largely blocked on user input + product-class schema decisions.

### 2.5 Persona-engine v1 (currently v0.5 scaffold)
- **Status**: `persona-engine-00005-mqc` LIVE but v0 scaffold. 4 commits in 5 days. SLO file landed today (PR #6). No consumers wired beyond UAE responsibility client. BFT mirror present but no operator_context at API.
- **What's missing for v1**: longitudinal persona store (interaction history with time-weighted decay); per-user BFT 9-var time-series; PUT /persona endpoint enforcing the sovereign-ownership boundary per SMEN doctrine (humans OWN, platform LEASES read-models); HumanPersona ↔ OrgPersona linkage; per-tenant isolation.
- **Effort**: 4-6 sessions.

### 2.6 User Influence-vs-Cost dashboard (8-week build plan; ~Week 1 partial)
- **Status**: `llm_call_cost` (migration 030) + `context_bundle_audit` + `operator_events` + `decision_records` + `outcome_records` + `me-intelligence/rate-response` LIVE. `third_party_call_cost` NOT created. `vw_action_trace` materialized view NOT created. Level 1 atomic dashboard route NOT shipped. Level 2 cards NOT shipped. Level 3 PPIM verdict scorecard NOT shipped. Counterfactual baseline NOT shipped.
- **Effort**: full 8-week plan = ~10-12 sessions.

### 2.7 Codification flywheel — partial; 8-gate self-governance stashed
- **Status**: Codification Engine v0.6 LIVE (LLM proposer + simulator + sweep chain in `decision-engine`). 8-gate self-governance gate-8 stash WAS DISCARDED today (per session). Needs re-implementation.
- **What's missing**: gate 8 (the recursive engine-governs-decisions-about-itself B-02 feedback loop) at full strength; codification rate measurement (Penrose #1) currently 0.0/90 days because no decision-logic patterns have been promoted Claude→Python yet.
- **Effort**: 2 sessions to re-implement gate 8; 5+ sessions of production traffic for codification rate to become a meaningful number.

### 2.8 Mimi v1 — defer items
- **Status**: mimi-whatsapp v0 deployed `00005-t5k`; `wired:false`. Per `assessment Tier 5.2`: defer items = media handling (images/audio/video attachments), threading (conversation context), group chats, scheduled sends.
- **Effort**: 6-8 sessions for v1.

### 2.9 SMEN end-state (Symbiotic Memory Exchange Network)
- **Status**: Framework 5.18 promoted to canonical doctrine 2026-05-08. Engine architecture map exists. But the doctrinal claim that "humans+agents+TI experts+Gigaton entities form network; humans OWN their intelligence + personal agent; LEASE platform intelligence" is NOT enforced in code. Read-model lifecycle on user departure: undefined. Metering / exchange-currency: undefined. Personal-agent identity protocol: undefined. TI expert classification: undefined. Mathematical metrics (joint entropy, network density × correlation, compression ratio): not measured.
- **Effort**: this is the eventual goal of the entire platform. 50+ sessions to a defensible v0.

### 2.10 Decision Routing Framework v3.2 maturity
- **Status**: v1→v3.2 ladder exists in doctrine. Today: hybrid for most production paths. No automatic Claude→Python codification after 50+ stable executions. LLM router lives in `gateway` but `(input_structure, logic_clarity, latency_sensitivity, error_cost)` selection is rule-based, not learned. 
- **What's missing**: production decision-class telemetry showing where each route is in the maturity ladder; automatic promotion triggers.
- **Effort**: 4-6 sessions.

### 2.11 BFT 9-var consumption (PPEME emits; what consumes for decisions?)
- **Status**: PPEME canonical emitter LIVE (`/v1/interactions/catalog` returns Business-Field-Theory deltas for `homepage_refresh`, `sales_call`, ... across 9 state variables). decision-engine does NOT consume these for routing. HME does NOT consume these for coaching. UAE does NOT consume these for capability resolution.
- **What's missing**: at least one consumer wired to PPEME `/v1/forecasts/scenario` for a real-time decision check.
- **Effort**: 2-3 sessions per consumer; 6-9 sessions for meaningful coverage.

### 2.12 Codification simulator (LLM proposer + simulator + sweep chain)
- **Status**: LIVE v0.6 in decision-engine. Engine wiring complete; sweep chain functional. Zero production patterns promoted (codification_rate = 0.0).
- **What's missing**: production decision traffic; the sweep results need to flow into a "promote to Python" PR.
- **Effort**: 3-4 sessions once traffic exists.

### 2.13 Drift sentinel rules count
- **Status**: Current rule count per `DRIFT_RULES.yaml`: MIN-010 (catalog tags JSONB) shipped today; CRIT-003/007 verified; ~20 axioms loaded. Baseline (2026-05-05) found 8 critical drift sites; today's critical_count = 0. **Rule total not currently audited**; rough count = 18-22 active rules.
- **What's missing**: rules 23+ — specifically: PPIM signature absence rule (MAJ), namespace middleware absence (MAJ), `third_party_call_cost` write absence (MAJ), BFT consumer absence per decision (MIN), Constitution amendment without sign-off (CRIT), connector adapter without secret_ref param (CRIT), persona row write without operator_context (MAJ).
- **Effort**: 1-2 sessions to author the next 10 rules + add detection logic.

---

## Section 3 — Honest: what's MISSING from the master project plan itself

Concepts that surface in chat / drift but are NOT captured (or are under-specified) in `master_project_plan.md`. Naming these so they enter the plan.

### 3.1 Tax / regulatory compliance per operator (platform-wide)
Mentioned in Carmen Beach Phase 4 (Mexican STR tax, RFC validation, IVA). NEVER spec'd platform-wide. LiquiFex is FINANCIAL SERVICES with SEC implications (note offerings); InContekst handles customer marketing data with GDPR/CCPA scope. There is no `compliance_engine` and no per-operator `regulatory_regime` enforcement layer. The `regime` tag on JSONB is the placeholder — no logic consumes it.

### 3.2 Payment processing connector (Stripe roadmap card with no spec)
The Stripe card on `/connectors` is roadmap-labeled. The architecture says "every booking writes a Stripe row in `third_party_call_cost`" — that table doesn't exist. There is NO Stripe adapter, NO webhook receiver, NO refund/dispute flow, NO Mexican peso processor variant for Carmen Beach, NO Stripe Connect for multi-tenant marketplace topology. This is the keystone connector for Phase 3 (Revenue Engine MVP) and it's a card on a page.

### 3.3 Email connector (Gmail roadmap, no spec)
Gmail card with no spec. Drive OAuth pattern provides the template (OAuth + per-user creds in connector-api), but Gmail adds: inbound webhook for new mail, outbound `email.send` (currently lives in SendGrid integration paths in SIE), threading model, label management, attachment handling. The Tier 5 Gignet capability (`email.send` from user identity) depends on this.

### 3.4 Calendar connector
Google Calendar / Outlook / iCal cards. STVR scheduling, sales-call booking (sales-operating-system), Gignet Tier 5 `calendar.write` all depend. No adapter exists.

### 3.5 A1 / agents.json / MCP standard adoption
Gigaton has Gignet Local Node as an MCP peer pattern. Does Gigaton publish a `/.well-known/agents.json` declaring its public agent endpoints? Per gateway snapshot: NO. The interop surface is Cloud Run + JWT-at-edge; no public agent-discovery standard. This matters for SMEN's claim that external agents (TI experts' agents, customer agents) should be able to discover + transact with Gigaton.

### 3.6 The Mtheory math layer (Framework 5.19 BFT) — Simulation Layer / Transformation Engine deployment
PPEME is the SIMULATION LAYER. The Master Calculator is one module within PPEME. The 4-layer execution stack (State Model / Interaction Model / Transformation Engine / Simulation Layer) is documented in `mtheory_business_field_theory.md` but only PPEME exposes endpoints. The "Transformation Engine" (the layer that converts interactions into state-vector deltas) lives implicitly in PPEME's catalog response — it is not separately deployed, not separately monitored, not separately calibrated. Per `bft_package_integration_plan.md` 4-phase rollout, Carmen Beach is supposed to be the first vertical consumer — that integration is not wired.

### 3.7 Cross-operator network effects topology
SMEN doctrine claims humans + entities form a network with Metcalfe-like scaling. Today: ZERO cross-operator data flow. Carmen Beach data does not influence Liquefex decisions. The Network Intelligence Layer in decision-engine has the SPEC but no production cross-operator pattern detection. There is no topology — only registration in a flat operator_defaults table.

### 3.8 Per-user persona memory longitudinal store
Persona-engine has BFT snapshot endpoint but no longitudinal time-series. There is no "show me this user's BFT state across the last 90 days" query. Without this, calibration cannot detect when a user's trust/clarity is degrading. This is the foundational substrate for the SMEN Experience Layer claim ("state tracking, preference modeling, relationship graphs, contextual continuity").

### 3.9 Cross-vendor identity resolution
`universal_connector_hub_architecture.md §F` notes: a single customer shows up as guest_id in Airbnb, email in Stripe, phone in Twilio, record_id in HubSpot, Instagram username in DMs. The intelligence layer needs Customer Identity Resolution to join these. NO ENGINE owns this. The master plan does not list it as a Phase deliverable. It will block Phase 5 Operator Dashboard once 2+ connectors are live with overlapping customer data.

### 3.10 Multi-tenant billing / metering infrastructure
Phase 7 names "multi-tenant billing" but no spec exists. How does an operator pay Gigaton for usage? Per-call? Per-decision? Per-namespace flat? Tied to the SMEN "lease intelligence" doctrine — but no metering exists. Without this, commercial scale is not just unreached but architecturally undefined.

### 3.11 Frontend split resolution
`gigaton-ui-system` (17 commits, deployed primary) vs `bella-byte/Gigaton-UI-Platform` (371 commits, active dev surface, NOT separately deployed). The plan acknowledges this as Tier 4.3 but doesn't pick a path. Two possible resolutions (a) deploy bella-byte to its own Firebase target, or (b) periodic merge. No decision. This is silent organizational debt.

### 3.12 Disaster recovery + backup posture
`backup_disaster_recovery_plan.md` exists as a memory but the master plan does not name DR as a Phase. RPO/RTO undefined per service. No exercise has been run. Cloud SQL backups assumed but not validated.

### 3.13 Founder-approval gate enforcement at boot path
P0 incident tonight: AX-010 doctrine ("financial-impact migrations require founder approval") was encoded in docstring only — `start.sh` ran `alembic upgrade head` unconditionally, applied migration 0008, and broke HME. New memory `feedback_enforce_doctrine_gates_at_boot.md` proposed but NOT YET enforced. The master plan does not name "doctrine gate enforcement" as a cross-cutting requirement.

### 3.14 connector-api deploy unblock (TS package build chain)
Today's failure: `@carmen/db` ships raw TS; connector-api builds itself but not its dep. Cross-package compile coordination is a missing item from the plan — it's session-specific tech debt that blocks Phase 5 because connector-api gates 6 of 8 connector cards.

---

## Completion estimates (honest, no rosiness)

**Plan completion as defined by master_project_plan.md §5 (8 phases):**
- Phase 0: ~95% (Constitution ratification ceremony pending)
- Phase 1: ~70% (intelligence-silo substrate alive, 0 data flowing; EO System code merged, 0 hydrated)
- Phase 2: ~50% (Decision Engine MVP shipped; Execution Engine merged not deployed; 0 paired execution rows)
- Phase 3: ~25% (sales-os + pricing partial; 0 productized offers; 0 paid intakes)
- Phase 4: ~40% (5 namespaces seeded; middleware not wired; 0 cross-namespace requests)
- Phase 5: ~35% (some dashboard surfaces; 6 of 8 Penrose metrics no data; no approval queue rollup)
- Phase 6: ~30% (modular replication empirically proven; 0 real second operators)
- Phase 7: ~10% (contribution matrix merged; 0 contributions; no billing; no SDK)

**Implicit doctrine completion**: ~30% (SMEN end-state aspirational; Gignet Tiers 2-7 = 0; cross-operator topology = 0)

**Aggregate (weighted by Phase importance to PPIM north star)**:

> **If we did nothing else, we have ~38% of the plan.**
> The next 2 weeks of focused work (Tier 1+2+3 from `assessment_and_improvement_plan_2026_05_19.md`) would get us to **~52%**.
> The next 3 months (Carmen Beach Phase 4 close + connector-api unblock + 8 connectors live + Penrose alerts firing + Decision Execution loop closed + first 10 paid intakes + first real second operator) gets us to **~70%**.
> **Truly aspirational beyond 3 months**: full SMEN ownership/leasing model with metered intelligence exchange; Gignet Local Node Tiers 5-7 with cross-machine mesh; cross-operator network effects measurable in Metcalfe-like scaling; Mtheory Transformation Engine separately deployed and calibrated; A1/agents.json adoption with external agents transacting against Gigaton; tax/regulatory compliance engine spanning STR + financial-services + B2B SaaS regimes; multi-tenant billing infrastructure operational. That last 30% is a multi-quarter, multi-doctrine-promotion effort and currently exists as memory not code.

ppim_signature: substrate.gap_analysis.v1
