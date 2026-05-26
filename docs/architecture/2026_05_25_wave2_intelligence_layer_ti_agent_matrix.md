---
type: architecture-design
established: 2026-05-25
status: ACTIVE — Wave 2 master design; doctrine-locked per INTEL-1 + INTEL-2
authority: locked unless explicitly revisited
serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
supersedes: stage_5_variance_aware_self_healing_spec (now sub-task §7 Week 6)
ppim_interaction: meta — governs every operator query + every system-initiated dispatch
ppim_economics: estimated 60-80% reduction in operator-to-engine routing latency + LLM cost
ppim_predictability: HIGH — every dispatch carries confidence + provenance
ppim_brand_dimension: coherence + intelligence-utilization
applies_to:
  - gigaton-ui-system (rename + rebrand)
  - decision-engine (dispatch brain)
  - intelligence-silo (skill catalog + EO + recruiting JD slots)
  - persona-engine (role identities)
  - gigaton-gateway (CLI surface routing)
  - human-management-engine (recruiting loops + utilization tracking)
  - gignet-orchestrator (task fan-out)
  - connector-api (3rd-party tool registry)
cross_refs:
  - decisions/2026-05-25_architecture_decisions_log.md (INTEL-1, INTEL-2, ARCH-1, ARCH-2, PAYOUT-1, all EF-*)
  - foundational_goal_gigaton_engineered_brand_experience (PPIM)
  - foundational_modular_replication_via_input_substitution
  - gignet_auto_trigger_orchestration
  - universal_connector_hub_architecture
  - master_project_plan (Chapter 11 — Gignet affiliate network)
  - standalone_bundle_net_new_concepts (concept 5 EEE + concept 4 Contribution Matrix)
  - onboarding_workflow_v1_completion_verified_2026_05_22
---

# Wave 2 — Intelligence Layer + Ti Agent Matrix + Self-Engineered HR

> **Wave 2 redefinition (INTEL-1):** The foundational autonomous-intelligence layer. Variance-aware self-healing for Stage 5 is now a sub-task (§7 Week 6) — the LLM-router calibration loop within this larger frame.

---

## 1. Goal + scope

**Goal.** Every operator interaction with Gigaton flows through ONE intelligence surface — `/intelligence` — that dispatches each query to the best-matched ensemble of expert roles from the Ti Agent Matrix, returns qualified answers (confidence + provenance + citations + next-step), coaches the operator in real time, and closes the loop by self-engineering its own HR when role-level utilization or quality drifts.

**Scope.**
- **User-facing surface**: `/intelligence` (renames `/chat`, gigaton-ui-system) — CLI-style chat + raw-command modes.
- **Routing brain**: decision-engine, extended with Ti Agent Matrix dispatch (skill-vector × availability × cost-inverse).
- **Role catalog**: intel-silo `agent_roles` + `skill_vectors` (multi-axis JSONB per modular-replication doctrine).
- **Role identities**: persona-engine (one OrgPersona per role, BFT-snapshotted).
- **Fan-out**: gignet-orchestrator (existing Phases A-G LIVE).
- **CLI controls**: all 11 engines + 3rd-party LLMs + connectors + Stripe + Gmail + WhatsApp + listings + inquiries.
- **HR closed loop**: HME owns utilization tracking; recruiting JD slot = 9th product type in Gignet affiliate network (Chapter 11).
- **Variance-aware self-healing**: relegated to LLM-router calibration sub-task, Week 6.

---

## 2. The `/intelligence` page UX

**Replaces** `/chat`. Same component tree (`pages/ChatPage.tsx` → `pages/IntelligencePage.tsx`); route alias `/chat` → 301 to `/intelligence` for one release.

**Icon.** `Brain` from `lucide-react@^0.562` (already in `package.json`). Doctrine-derived: PPIM `ppim_brand_dimension: coherence` + `intelligence-utilization` — `Brain` is the unambiguous representational glyph in the existing icon library. No new dep, no brand pipeline blocker. Fallback to `Sparkles` only if downstream theming requires a non-anatomical mark.

**Layout (two modes, toggleable).**
- **Conversational mode (default).** ChatGPT-style. Streaming SSE. EngineInsightBadge stays; renamed `DispatchBadge` to show routed role ensemble.
- **CLI mode.** Monospace, prompt-style `gigaton>`. Raw commands: `:engines status`, `:dispatch CFO "model pricing for vendor X"`, `:llm route haiku4.5`, `:source refresh airbnb-ical`, `:hr utilization`, `:approve <task_id>`. Toggle: `Cmd-K`.

**Real-time coaching.** As operator types: debounced (350ms) call to decision-engine `/v1/intelligence/classify` returns `{intent, required_skills[], routed_roles[], confidence, est_cost_usd, est_latency_ms}`. Surfaces inline above input as a `CoachingHint` chip. Operator can edit before submit.

**Information qualification.** Every response renders four fields beside the message body: `confidence (0-1)` · `provenance (source IDs)` · `citations (URLs/refs)` · `next_step (one-line recommendation)`. Sourced from decision-engine response envelope (new field set; additive).

**Routing indicator.** `DispatchBadge` shows the primary role + advisor roles (e.g. `CFO · CRO advisor · 0.83 conf`). Click expands to the dispatch decision record.

---

## 3. The Ti Agent Matrix

**Source.** CLAUDE.md org structure: CEO → 9 executives (CTO, CXOO, CISO, CDO, second-CTO, CFO, CMO, CRO, CPO) × ≤7 reports each = up to **63 roles**. Skill axes (CLAUDE.md): `technical, commercial, creative, analytical, operational, interpersonal, environmental, political`.

**Per-role shape** (intel-silo `agent_roles`):
```
role_id (slug)         e.g. cfo, cfo.fpa_lead, cto.platform_eng
title                  display
parent_role_id         FK → agent_roles (CEO is root)
skill_vector           jsonb {technical: 0.0-1.0, commercial: …, …} 8 axes
specialization_tags    jsonb multi-axis (per modular-replication doctrine)
cost_tier              enum: claude_haiku|sonnet|opus|gpt-4o|gemini|human_review|deterministic
availability_state     enum: active|throttled|idle|hiring|deprecated
ppim_signature         jsonb
persona_id             FK → persona-engine OrgPersona
lifecycle_state        canonical|active|proposed|archived
```

**Dispatch logic** (decision-engine `dispatch/router.py`).
1. Classify query → required-skill-vector + ppim_brand_dimension.
2. Cosine-match required-skill-vector vs each role's `skill_vector`.
3. Score = `0.6 * cosine + 0.25 * availability + 0.15 * (1 - normalized_cost)`.
4. Pick top-1 primary; if score gap top-1 vs top-2 < 0.1 OR `error_cost == high`, add top-2 + top-3 as advisors (ensemble).
5. Complex multi-axis tasks (e.g. pricing-strategy = financial+commercial+analytical) → multi-stage ensemble: CFO leads, CRO + CMO comment, CTO sanity-checks unit economics.

**Lazy expansion.** Per modular-replication doctrine: Week 1 seeds the **9 executives only**. Reports under each executive instantiate on first dispatch demand (matching score < threshold AND no existing report covers the gap). No 63-role bigbang.

**Implementation surface.**
- intel-silo: `agent_roles`, `skill_vectors` tables + REST.
- persona-engine: 9 OrgPersona rows seeded Week 1; reports added lazily.
- decision-engine: dispatch router + scoring formula + dispatch_decisions log.
- gignet-orchestrator: emits `dispatch.routed.<role_id>` events; fan-out triggers next-task.

---

## 4. CLI orchestration

**The `/intelligence` page IS the CLI.** Two modes, one surface.

**Flow.** Operator input → gigaton-gateway `/v1/intelligence/dispatch` → decision-engine routes via Ti Agent Matrix → primary role + advisors execute (each role mapped to an engine + LLM tier per its `cost_tier`) → results aggregated by decision-engine into the response envelope → streamed back via SSE.

**Controls (all via CLI commands, all via Pub/Sub fabric).**
- 3rd-party LLMs: `:llm route <task_class> <model>` — wraps gigaton-gateway `app/llm_router/` (Phase D LIVE).
- Source updates: `:source refresh <connector_id>` — intel-silo connectors (Documentation Ingest pattern already shipped).
- Alt AI tools: `:tool register <connector_id>` — connector-api catalog (Pattern A storage).
- Human approvals: `:approve <task_id>` — UAE sign-off matrix.
- Stripe: `:stripe payouts <entity_id>` — gigaton-engine (PAYOUT-1 Connect/ACH paths).
- Messaging: `:msg send <channel> <recipient>` — mimi-whatsapp + connector-api Gmail (per EMAIL-1 + SUPPORT-3).
- Inquiries / listings: `:cbp inquiries|listings` — Carmen-Beach-Properties `apps/web` (L1 surface per ARCH-2).

All commands carry the operator's `X-Client-Namespace` + JWT; namespace middleware (UAE) gates per-tenant scope.

---

## 5. Real-time coaching loop

**On every keystroke** (debounced 350ms): decision-engine `/v1/intelligence/classify` returns intent + routed roles + memory hits (retrieved via intel-silo memory_items search using current query + last 5 turns) + a one-line hint. Renders as `CoachingHint` chip.

**On every system output**: response envelope carries `confidence (0-1)`, `provenance` (array of source_ids from intel-silo Source Registry), `citations` (URLs / doc paths), `next_step` (recommended follow-up command). Operator sees all four inline.

**Feedback loop**: each rendered output has accept/edit/reject buttons. Click writes to `coaching_feedback` (intel-silo) with `{dispatch_id, role_id, verdict, edited_text, ts}`. Decision-engine retrains dispatch weights nightly (gradient-free: bumps role-match score on accepts, penalizes on rejects).

**Codification trigger**: per gignet Phase D, when a (intent → role → accept) tuple recurs 50× the LLM router auto-emits a `codification.candidate.*` event → Python deterministic rule replaces the LLM call (per master plan §6 + `04_codification_thresholds.md`).

---

## 6. Self-Engineered HR

**Trigger.** HME nightly job scans `agent_roles.availability_state` + `dispatch_decisions` last-30d. A role enters `hiring` state when:
- Utilization > 90% sustained ≥ 7 days, OR
- Quality (accept-rate) < 60% sustained ≥ 14 days, OR
- Operator-reported gap (`/intelligence`: `:hr gap <skill>`) crosses 3-distinct-operators threshold.

**Recruiting flow** (closed loop, all PPIM-signed, all audited):
1. **JD auto-gen** from role's `skill_vector` + recent task volume + ppim signature → JD lives as a Gignet affiliate-network **9th product type** (Chapter 11 — slot reserved alongside the 8 existing).
2. **Multi-channel sourcing**: LinkedIn API + Indeed MCP (`mcp__claude_ai_Indeed__*` available) + Gignet affiliate-network internal referrals + outbound bundles in the Multipli pattern.
3. **Automated screening**: decision-engine classifies application → persona-engine verifies identity → candidate receives a Multipli-style bundle as a skills assessment (deterministic eval rubric).
4. **Interview booking**: mimi + Google Calendar (`mcp__claude_ai_Google_Calendar__*`) auto-suggests slot windows for the human reviewer.
5. **Offer**: gigaton-engine compensation model (carmen-beach-agent-costing.md pattern + CLAUDE.md skills matrix); compensation rate = function of skill_vector match × market benchmark.
6. **Onboarding**: extends the existing 10-stage operator flow (`onboarding_workflow_v1`) with an `agent-of-gigaton` operator type — new entity_type row, no engine rewrite (modular replication).

Every decision audited; every interaction PPIM-signed; recruiting loop logged in `recruiting_loops` table.

---

## 7. Build sequence — 6-week arc

**Week 1 (2026-05-26 → 2026-06-01) — Scaffolding.**
- Rename `/chat` → `/intelligence` (route + page + nav).
- `Brain` icon swap, `DispatchBadge` component, `CoachingHint` placeholder.
- Load decisions log + canonical memory files into the chat context (system prompt extension).
- Seed 9 executive OrgPersonas in persona-engine.
- First Ti role pilot: **CTO** end-to-end (dispatch → execute → return). Validates the loop.
- intel-silo migration: `agent_roles` + `skill_vectors` tables.

**Week 2 — 5-role dispatch.**
- Skill-vector cosine scoring + dispatch_decisions table in decision-engine.
- Seed top-5 most-needed reports under each exec (5 × 9 = 45-role intermediate state — but only those that fire on actual operator queries).
- `:dispatch <role> <query>` CLI command live.

**Week 3 — Full matrix + coaching MVP.**
- Lazy-expand to full 63 roles via on-demand instantiation.
- Ensemble logic (primary + advisors).
- Real-time `CoachingHint` chip + response envelope (confidence/provenance/citations/next_step).
- `coaching_feedback` table + accept/edit/reject UI.

**Week 4 — CLI for all 11 engines + 3rd-party LLM control.**
- All `:engines`, `:llm`, `:source`, `:tool`, `:approve`, `:stripe`, `:msg`, `:cbp` commands.
- gigaton-gateway `/v1/intelligence/dispatch` aggregator route.
- 3rd-party LLM router fully wired to dispatch (Anthropic + OpenAI + Gemini via LLM router).

**Week 5 — Self-Engineered HR MVP.**
- HME nightly utilization scan + `hiring` state transitions.
- JD auto-gen → Gignet affiliate-network 9th product type registered.
- One end-to-end recruit (likely `cfo.fpa_lead` — already showing utilization signal in dispatch sims).

**Week 6 — Scale + variance-aware self-healing sub-task.**
- All 11 engines fully addressable; all 63 roles instantiated on-demand.
- **Variance-aware self-healing absorbed** as LLM-router calibration loop: dispatch model nightly retraining + Stage 5 variance check against intel-silo baseline catalogs (the original Wave 2 framing now a calibration sub-routine).

---

## 8. Existing infrastructure leveraged vs net-new

**Leveraged (no rewrite).**
- gignet-orchestrator Phases A-G LIVE (registry + topic + trigger map + LLM router + local node + drift + observability).
- decision-engine Penrose scoreboard + Axiom Registry + Decision Execution Engine.
- intel-silo Source Registry + EO System + memory_items + Documentation Ingest connectors.
- persona-engine OrgPersona + HumanPersona + First Principles Variable Registry + BFT snapshot.
- gigaton-ui-system `/chat` component tree (rebrand, not rebuild).
- gigaton-gateway edge + namespace middleware + LLM router + webhook routes.
- HME initiative lifecycle + Framework 5.18 Learning Loop + Contribution Matrix.
- connector-api credential storage (Pattern A) + 15 provider probes.
- mimi-whatsapp + Gmail-API+Workspace (EMAIL-1 lock) for recruiting comms.
- Onboarding 10-stage manifest (extends to `agent-of-gigaton` operator type).
- Gignet affiliate network (Chapter 11) — JD slot = 9th product.

**Net-new (intel-silo unless noted).**
- 6 tables: `agent_roles`, `skill_vectors`, `role_assignments`, `dispatch_decisions` (decision-engine), `recruiting_loops` (HME), `coaching_feedback`.
- ~14 endpoints: `/v1/intelligence/{classify, dispatch, feedback}`, `/v1/agent_roles`, `/v1/dispatches`, `/v1/recruiting/*`, plus CLI command-router on gateway.
- 2 FE components: `DispatchBadge`, `CoachingHint`.
- 1 nightly HME job: `utilization_sweep`.

---

## 9. Decisions made by the design (vs escalated)

Per INTEL-2 doctrine. Each row: decision + the doctrine/memory that drove it.

| # | Decision needed | Locked answer | Driven by |
|---|---|---|---|
| 1 | Icon for `/intelligence` | `Brain` (lucide-react, already in package.json) | universal_connector_hub_architecture brand_dimensions extensibility + ppim coherence; no new dep |
| 2 | Build all 63 roles upfront vs lazy | Lazy: 9 execs Week 1, reports on demand | foundational_modular_replication_via_input_substitution (engine catalog is data-driven, instantiated by need) |
| 3 | Where does recruiting JD-template live | Gignet affiliate-network 9th product type | master_project_plan Chapter 11 (25 certs × 5 tiers × 8 products); doctrine: extend existing taxonomy, don't fork |
| 4 | Skill vector dimensionality | 8 axes per CLAUDE.md (technical, commercial, creative, analytical, operational, interpersonal, environmental, political) | master-knowledge-base/CLAUDE.md "Org Structure Assumption" |
| 5 | Where dispatch logic lives | decision-engine (the routing brain by definition) | master_project_plan §3.1 (decision-engine role = Doctrine + Trust/Value/Authority matrix + Penrose) + gignet_auto_trigger_orchestration Component 5 (LLM router pattern) |
| 6 | Role-storage repo | intel-silo (catalog discipline, multi-axis tags) | foundational_modular_replication_via_input_substitution §1+§2 (every catalog → JSONB tags); intel-silo already hosts brand_dimensions on identical shape |
| 7 | Role identity store | persona-engine (already owns HumanPersona+OrgPersona) | master_project_plan §3.1 + standalone_bundle_net_new_concepts concept 2 (First Principles Variable Registry already there) |
| 8 | Coaching debounce window | 350ms | Universal UX heuristic; INTEL-2 says "make the call" |
| 9 | Ensemble size | 1 primary + 0-2 advisors; bigger only on multi-axis tasks | gignet_auto_trigger_orchestration §5 Multi-model second opinion gate pattern |
| 10 | Scoring weights `0.6*cosine + 0.25*avail + 0.15*(1-cost)` | These weights; revisit Week 6 calibration | decision_routing_framework + Penrose calibration doctrine; gradient-free retrain on coaching_feedback |
| 11 | Recruiting comms vendor | Gmail + Workspace (NOT SendGrid); WhatsApp via Twilio | decisions log EMAIL-1 + SUPPORT-* lineage |
| 12 | Compensation model source | gigaton-engine carmen-beach-agent-costing.md pattern × skill_vector match | master-knowledge-base knowledge-extracts/carmen-beach-agent-costing.md |
| 13 | New operator type `agent-of-gigaton` for HR onboarding | Extends 10-stage manifest, new entity_type row | onboarding_workflow_v1_completion_verified_2026_05_22 + EF-4 (distinct entity types where defaults differ) |
| 14 | Variance-aware self-healing scope | Sub-task §7 Week 6 (LLM router calibration), not Wave 2 itself | INTEL-1 explicit redefinition |
| 15 | Codification threshold (LLM → Python) | 50-call streak (existing Phase D rule) | gignet_auto_trigger_orchestration §Component 5 + claude-systems/v3.2 codification rule |
| 16 | Bypass direct LLM calls from FE | Never; all via gateway/decision-engine | gigaton-ui-system CLAUDE.md Architecture Contract + CRIT-007 |
| 17 | Per-dispatch cost logging | Existing `llm_call_cost` + new `dispatch_decisions.cost_usd` | universal_connector_hub_architecture §C universal cost telemetry |
| 18 | Multi-tenant scoping | `X-Client-Namespace` middleware (UAE) on every CLI command | ARCH-1 + ARCH-2 (gateway is the choke; tenants are FEs) |
| 19 | Where does `/chat` route redirect | 301 to `/intelligence` for one release; remove next | gigaton-ui-system convention + decisions log INTEL-1 |
| 20 | When to escalate to human reviewer in dispatch | `error_cost==high AND confidence<0.65` OR ensemble disagreement >0.3 | gignet_auto_trigger_orchestration §Component 5 second-opinion gate |

**Pre-locked: 20.** Genuinely escalated (§10): **3**.

---

## 10. Open decisions that need user (max 3)

Each: recommended default + fallback if user doesn't respond by Week 1 close (2026-06-01).

### Q1 — Skill-vector seed values for the 9 executives
**Decision.** Initial numeric weights for each of 9 execs across 8 skill axes (72 values total).
**Recommended default.** Symmetric seed per the title's primary axis (e.g. CFO = `{commercial:0.9, analytical:0.9, operational:0.7, …, creative:0.3}`) — agent generates from CLAUDE.md + carmen-beach-agent-costing.md and presents a JSON for user to ratify or amend in 5 minutes.
**Fallback.** Use the agent-generated table verbatim; calibrate via `coaching_feedback` over Weeks 2-3.

### Q2 — Recruiting human-in-the-loop gate
**Decision.** Does the self-engineered HR loop send the final offer **autonomously** or **after Todd's one-click approve**?
**Recommended default.** One-click approve on first 10 hires; switch to autonomous Week 8+ if accept-rate > 80% and zero compliance flags. Honors PPIM "facilitate, not autonomous-without-human" doctrine + ARCH-1 sunset of operator-local actions only after gigaton-platform proves stable.
**Fallback.** One-click approve indefinitely; revisit as data accrues.

### Q3 — Coaching opt-out at operator level
**Decision.** Can a tenant operator turn off real-time coaching for privacy/UX preference, or is it mandatory (always-on for PPIM observability)?
**Recommended default.** Always-on for system telemetry (we need the data); UI affords *visual minimization* (collapse the chip) but the dispatch + envelope writes never pause.
**Fallback.** Always-on, chip-collapsible.

---

## 11. Risks + doctrine mitigations

| Risk | Doctrine mitigation |
|---|---|
| **63-role bigbang collapses under its own complexity** | Lazy expansion (modular-replication §3+§4); seed only 9 execs Week 1 |
| **Dispatch model overfits early operator quirks** | Codification threshold = 50-call streak before deterministic; nightly retrain on `coaching_feedback`; Penrose drift_critical metric surfaces overfit |
| **Self-engineered HR makes a compliance-bad hire** | Q2 default = human-in-the-loop offer approval; PPIM "Facilitate" parses "co-pilot for a human owner, not autonomous action" |

---

## 12. Cross-reference table

| Reference | Why it matters here |
|---|---|
| `decisions/2026-05-25_architecture_decisions_log.md` | INTEL-1 + INTEL-2 + ARCH-1/2 lock the frame; PAYOUT-1 governs HR offer/compensation |
| `[[foundational_goal_gigaton_engineered_brand_experience]]` | Every dispatch must carry PPIM signature; envelope mirrors PPIM atomic schema |
| `[[foundational_modular_replication_via_input_substitution]]` | All catalogs (roles, skills, JDs) use multi-axis JSONB tags |
| `[[gignet_auto_trigger_orchestration]]` | Phases A-G LIVE substrate; Wave 2 sits on top |
| `[[universal_connector_hub_architecture]]` | Connector catalog + cost telemetry pattern reused for `agent_roles` + `dispatch_decisions` |
| `[[master_project_plan]]` Chapter 11 | Gignet affiliate-network 9th product = JD slot |
| `[[standalone_bundle_net_new_concepts]]` concept 2/3/5 | First Principles Variable Registry + EO System + Experience Engineering Equation feed dispatch features |
| `[[onboarding_workflow_v1_completion_verified_2026_05_22]]` | Reused for `agent-of-gigaton` operator type; verification chain extended |
| `gigaton-ui-system/CLAUDE.md` | Architecture Contract — no FE bypass of backend; CRIT-007 provider+model on every LLM call |
| `master-knowledge-base/CLAUDE.md` | Org structure + 8 skill axes seed the matrix |
