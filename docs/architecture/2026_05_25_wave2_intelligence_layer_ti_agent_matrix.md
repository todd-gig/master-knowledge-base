---
type: architecture-design
established: 2026-05-25
reconstructed: 2026-05-26 (originally authored 2026-05-25 22:23 CT on branch `feat/runbooks-oauth-qa-and-legacy-scope-sunset` commit `7e68935` but never merged to `main`)
status: ACTIVE — Wave 2 master design; doctrine-locked per INTEL-1 + INTEL-2
authority: locked unless explicitly revisited
serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
supersedes: stage_5_variance_aware_self_healing_spec (now sub-task §7 Week 6)
ppim_interaction: meta — governs every operator query + every system-initiated dispatch
ppim_economics: estimated 60-80% reduction in operator-to-engine routing latency + LLM cost
ppim_predictability: HIGH — every dispatch carries confidence + provenance
ppim_brand_dimension: coherence + intelligence-utilization
ppim_outcome_quality: a unified, attributable, real-time-coached interaction surface for every operator
applies_to:
  - gigaton-ui-system (rename + rebrand: `/chat` → `/intelligence`)
  - decision-engine (dispatch brain; `/v1/intelligence/classify` lives here)
  - intelligence-silo (skill catalog + EO + recruiting JD slots; owns `agent_roles` + `skill_vectors`)
  - persona-engine (role identities; one OrgPersona per Ti Agent Matrix role)
  - gigaton-gateway (CLI surface routing + attribution_chain stamping + namespace alias)
  - human-management-engine (recruiting loops + utilization tracking)
  - gignet-orchestrator (task fan-out)
  - connector-api (3rd-party tool registry)
cross_refs:
  - decisions/2026-05-25_architecture_decisions_log.md (INTEL-1, INTEL-2, ARCH-1, ARCH-2, PAYOUT-1, all EF-*, MIG-CANCEL)
  - foundational_goal_gigaton_engineered_brand_experience (PPIM doctrine)
  - foundational_modular_replication_via_input_substitution (lazy expansion + JSONB multi-axis tags)
  - gignet_auto_trigger_orchestration (Phases A-G LIVE substrate)
  - universal_connector_hub_architecture (catalog + cost telemetry pattern)
  - master_project_plan (Chapter 11 — Gignet affiliate network = HR loop substrate)
  - standalone_bundle_net_new_concepts (concept 2 First Principles Variable Registry + concept 4 Contribution Matrix + concept 5 EEE)
  - onboarding_workflow_v1_completion_verified_2026_05_22 (extended for `agent-of-gigaton` operator type)
---

# Wave 2 — Intelligence Layer + Ti Agent Matrix + Self-Engineered HR

> **Wave 2 redefinition (INTEL-1):** The foundational autonomous-intelligence layer. Variance-aware self-healing for Stage 5 is now a sub-task (§7 Week 6) — the LLM-router calibration loop within this larger frame.

---

## 0. TL;DR

Wave 2 is redefined as the **Intelligence Layer**: one operator-facing surface (`/intelligence`, renamed from `/chat`) that classifies every query, dispatches it to the best-matched ensemble of expert roles from the **Ti Agent Matrix** (up to 63 specialized roles derived from CLAUDE.md's CEO → 9 executives × ≤7 reports org structure), returns qualified responses with `confidence + provenance + citations + next_step`, coaches the operator in real time, and closes the loop via **Self-Engineered HR** when role-level utilization or quality drifts beyond threshold. Variance-aware self-healing (the original Wave 2 framing per `[[stage_5_variance_aware_self_healing_spec]]`) is relegated to a Week 6 sub-task — it becomes the LLM-router calibration loop *within* this larger Intelligence Layer frame. As of 2026-05-26 the substrate is live across **4 merged PRs** (intel-silo #41, persona-engine #12, decision-engine #85, gigaton-gateway #57 + #58); the full 6-week build sequence proceeds from CTO-role pilot to full 63-role lazy expansion + Self-Engineered HR MVP + variance-aware sub-task by 2026-07-06.

---

## 1. The two locked decisions that frame this work (verbatim)

### INTEL-1 — Wave 2 redefinition: Intelligence Layer + Ti Agent Matrix + Self-Engineered HR

*Source: user 2026-05-26 ~03:00 UTC. Verbatim from `decisions/2026-05-25_architecture_decisions_log.md`.*

- **Wave 2 (previously variance-aware self-healing for Stage 5)** is now the foundational **Intelligence Layer**. Variance-aware self-healing relegates to a sub-task within Wave 2 (specifically: the LLM-router calibration loop).
- **Concept rename:** `chat` page → **`intelligence`** page. Iconography: representative-of-intelligence symbol (TBD by the design pipeline; default: brain / neural / lightning glyph until brand pipeline picks). All existing references to `/chat` in `gigaton-ui-system` route to `/intelligence`.
- **Goal:** all 11 platform services operating + user can interact with all of them through the Intelligence page = a unified CLI-style chat surface.
- **Objective:** give user a CLI for all Gigaton systems via the intelligence page + create real-time coaching + feedback + intelligence-utilization-to-qualify-information environment.
- **Ti Agent Matrix:** the intelligence layer dispatches each query/task to a multi-expert ensemble derived from the locked org structure (CEO → 9 executives [CTO/CXOO/CISO/CDO/CTO/CFO/CMO/CRO/CPO] × up to 7 reports each = up to 63 specialized roles). Skill matrix axes per CLAUDE.md: technical, commercial, creative, analytical, operational, interpersonal, environmental, political. Matching = task → required-skills × available-experts × resource-availability → optimal agent ensemble.
- **CLI controls everything:** all 3rd-party LLMs (Anthropic + OpenAI + Google), source updates (intel-silo connectors), alt AI tools (any tool registered in the connector catalog), all through gignet-orchestrator Pub/Sub fabric.
- **Self-Engineered HR:** the intelligence layer performs automated analysis → identifies human-entity/talent requirements → triggers recruiting & staff management through automated human management systems engineered BY gigaton intelligence itself. Closed feedback loop: platform's own talent gaps surface from its own performance data; recruitment is platform-driven.

**What this supersedes.** The earlier `[[stage_5_variance_aware_self_healing_spec]]` (2026-05-25 ~18:00 CT) framed Wave 2 as Gigaton-pre-researches-industry baselines → operator submission scored as variance against our model. That work is preserved verbatim and lands as the **§7 Week 6 sub-task** (LLM-router calibration loop). Its 3 originally-planned PRs (decision-engine migration 005 + variance computation, gigmcp integration, FE variance display) are now sequenced behind the Intelligence Layer scaffolding.

### INTEL-2 — Decision-making protocol (META-DOCTRINE)

*Source: user 2026-05-26 ~03:00 UTC. Verbatim.*

- **Rule:** ALL decisions should be made by system intelligence ASAP. Questions to the user are the FALLBACK, not the default.
- **Before escalating any choice to user, route through:**
  1. Existing memory files at `~/.claude/projects/-Users-admin/memory/` (look for prior decisions on similar topics)
  2. The decisions log at `decisions/2026-05-25_architecture_decisions_log.md` (the rolling source of truth)
  3. Doctrine docs: `[[foundational_goal_gigaton_engineered_brand_experience]]`, `[[foundational_modular_replication_via_input_substitution]]`, `[[universal_connector_hub_architecture]]`, `[[gignet_auto_trigger_orchestration]]`
  4. The master plan: `[[master_project_plan]]`
  5. The Ti Agent Matrix (when implemented): dispatch to the appropriate expert role(s) for the decision
  6. Custom language + symbology logic: PPIM signatures, multi-axis JSONB tags, modular replication input-substitution patterns
- **Only escalate to user when:** (a) the decision is genuinely novel + outside doctrine scope, (b) the cost of a wrong autonomous decision exceeds the cost of waiting for user input, or (c) the user has explicitly tagged a topic as user-only (e.g. legal entity decisions, personnel ownership, brand identity).

**This doc's own demonstration of INTEL-2.** §9 below tabulates **20 decisions** the design self-locked via the doctrine chain; only **3 questions** (§10) are escalated to the user, each with a doctrine-derived default that fires automatically if no response by 2026-06-01.

---

## 2. Architecture — request flow + feedback loops

```
                                  ┌──────────────────────────────────────┐
                                  │     OPERATOR / USER INTENT           │
                                  │  (typed query OR :cli command OR     │
                                  │   system-initiated dispatch event)   │
                                  └──────────────┬───────────────────────┘
                                                 │  X-Client-Namespace + JWT
                                                 ▼
                            ┌────────────────────────────────────────────┐
                            │  gigaton-gateway                            │
                            │  - PR #57: PPIM attribution_chain stamping  │
                            │  - PR #58: slug-alias resolver              │
                            │  - existing: NamespaceMiddleware (UAE)      │
                            └──────────────┬─────────────────────────────┘
                                           │  POST /v1/intelligence/classify
                                           ▼
                  ┌────────────────────────────────────────────────────────┐
                  │  decision-engine                                        │
                  │  PR #85: /v1/intelligence/classify stub                 │
                  │  → returns {intent, required_skills[],                  │
                  │     routed_roles[], confidence, est_cost_usd,           │
                  │     est_latency_ms}                                     │
                  │  (today: keyword-heuristic stub; Week 3: cosine match)  │
                  └────┬────────────────────────────────┬─────────────────┘
                       │ skill_vector cosine match       │ persona lookup
                       ▼                                 ▼
        ┌────────────────────────────┐    ┌──────────────────────────────┐
        │ intelligence-silo          │    │ persona-engine               │
        │ PR #41: agent_roles +      │    │ PR #12: 9 executive          │
        │   skill_vectors tables     │    │   OrgPersonas seeded (CEO    │
        │   (multi-axis JSONB tags)  │    │   + CTO/CXOO/CISO/CDO/CFO/   │
        │                            │    │   CMO/CRO/CPO)               │
        └────────────┬───────────────┘    └────────────┬─────────────────┘
                     │                                  │
                     └──────────────┬───────────────────┘
                                    ▼
                  ┌────────────────────────────────────────┐
                  │  Dispatch (decision-engine router)      │
                  │  score = 0.6*cos + 0.25*avail +         │
                  │          0.15*(1-norm_cost)             │
                  │  → primary role + 0-2 advisors          │
                  └────────────┬───────────────────────────┘
                               │  dispatch.routed.<role_id> event
                               ▼
                  ┌────────────────────────────────────────┐
                  │  gignet-orchestrator (Phases A-G LIVE)  │
                  │  fans out → engine(s) per role          │
                  │  cost_tier → LLM router (Haiku/Sonnet/  │
                  │  Opus/4o/Gemini/human_review/det)       │
                  └────────────┬───────────────────────────┘
                               │
                ┌──────────────┼──────────────────────────┐
                ▼              ▼                          ▼
        ┌───────────┐  ┌──────────────┐         ┌─────────────────┐
        │ 11 engines│  │ 3rd-party    │         │ connector-api   │
        │ (gigaton- │  │ LLMs via     │         │ (Stripe, Gmail, │
        │  engine,  │  │ llm_router   │         │  WhatsApp,      │
        │  HME, …)  │  │              │         │  Airbnb, GA4…)  │
        └─────┬─────┘  └──────┬───────┘         └────────┬────────┘
              │               │                          │
              └───────────────┼──────────────────────────┘
                              ▼
              ┌──────────────────────────────────────────┐
              │  Response envelope (back through gateway) │
              │  { body, confidence, provenance[],         │
              │    citations[], next_step,                 │
              │    dispatch_id, attribution_chain }        │
              └────────────┬─────────────────────────────┘
                           │  SSE stream
                           ▼
              ┌──────────────────────────────────────────┐
              │  /intelligence page (gigaton-ui-system)   │
              │  DispatchBadge · CoachingHint · 4 fields  │
              │  Accept / Edit / Reject buttons           │
              └────────────┬─────────────────────────────┘
                           │  feedback events
                           ▼  (debounced + on-submit)
   ┌──────────────────────────────────────────────────────────────────┐
   │  FEEDBACK LOOPS (close the system on itself)                      │
   │                                                                    │
   │  → coaching_feedback (intel-silo)                                  │
   │       nightly retrain → dispatch weights                           │
   │                                                                    │
   │  → dispatch_decisions (decision-engine) → utilization sweep        │
   │       (HME nightly) → role.availability_state ∈ {hiring, …}        │
   │                                                                    │
   │  → if hiring → JD auto-gen → Gignet affiliate-network 9th product  │
   │       (master_project_plan Chapter 11) → multi-channel sourcing    │
   │       → screen → interview → offer → onboard (extends 10-stage     │
   │       manifest with `agent-of-gigaton` operator type)              │
   │                                                                    │
   │  → if (intent → role → accept) tuple recurs 50× → codification     │
   │       (Phase D auto-trigger) → Python deterministic rule replaces  │
   │       the LLM call                                                 │
   └──────────────────────────────────────────────────────────────────┘
```

Every arrow honors `[[foundational_modular_replication_via_input_substitution]]`: the dispatch router, the role catalog, the skill vectors, and the JD templates are all **data-driven** (JSONB multi-axis tags). The same engine serves any future operator/tenant by swapping `operator_context`.

---

## 3. Today's substrate — the 4 ratified PRs (2026-05-26)

These are the concrete commits that make the diagram in §2 real (vs aspirational). Each PR merged 2026-05-26 between 16:50 and 17:01 UTC.

| Repo | PR | Title | Merge SHA | What it gives us |
|---|---|---|---|---|
| **intelligence-silo** | [#41](https://github.com/todd-gig/intelligence-silo/pull/41) | feat(schema): Wave 2 — agent_roles + skill_vectors tables (Ti Agent Matrix substrate) | `3316bce8` | The catalog substrate. Two tables with JSONB multi-axis tags per `[[foundational_modular_replication_via_input_substitution]]`. Empty today — Week 1 seeds 9 executive rows. |
| **persona-engine** | [#12](https://github.com/todd-gig/persona-engine/pull/12) | feat(personas): Wave 2 — seed 9 executive OrgPersonas (Ti Agent Matrix foundation) | `35e6d36c` | 9 OrgPersona rows for CEO + CTO + CXOO + CISO + CDO + CFO + CMO + CRO + CPO. Each carries BFT snapshot + PPIM signature. Reports under each exec are NOT seeded (lazy expansion per §3 doctrine). |
| **decision-engine** | [#85](https://github.com/todd-gig/decision-engine/pull/85) | feat(intelligence): stub /v1/intelligence/classify endpoint (Wave 2 routing seam) | `daaf5e22` | The routing seam. **Honest status: keyword-heuristic stub**, not a real semantic classifier. Returns the expected envelope shape so FE + gateway + gignet can be wired ahead of the Week 3 cosine-matching implementation. |
| **gigaton-gateway** | [#57](https://github.com/todd-gig/gigaton-gateway/pull/57) | feat(gateway): PPIM attribution_chain + license-check middleware | `f8ccfe17` | Every request now carries an `attribution_chain` header stamped at the edge. Required for the Self-Engineered HR loop's audit trail + the §5 coaching feedback writebacks. |
| **gigaton-gateway** | [#58](https://github.com/todd-gig/gigaton-gateway/pull/58) | feat(namespace): slug alias map + load_seed UAE-mode bugfix | `1e050bcb` | Namespace alias resolution: `/chat` requests resolve to the same backend as `/intelligence` during the one-release deprecation window. Also fixes a UAE-mode load_seed bug that was blocking namespace seeding. |

**Honest status of the substrate:**
- The 4 PRs land the *seams*, not the brain. The router is a stub. The skill_vector table is empty. The 9 OrgPersonas are seeded but not yet wired to dispatch.
- This is intentional — `[[gignet_auto_trigger_orchestration]]` Phases A-G + the existing Penrose scoreboard + the codification thresholds mean we can dispatch through the seams while the brain matures.

---

## 4. The `/intelligence` page UX

**Replaces** `/chat`. Same component tree (`pages/ChatPage.tsx` → `pages/IntelligencePage.tsx`); route alias `/chat` → 301 to `/intelligence` for one release. The route alias is implemented client-side in gigaton-ui-system [PR #41](https://github.com/todd-gig/gigaton-ui-system/pull/41) (awaiting merge as of this writing) and backed by gateway PR #58's slug alias map.

**Icon.** `Brain` from `lucide-react@^0.562` (already in `package.json`). Doctrine-derived: PPIM `ppim_brand_dimension: coherence` + `intelligence-utilization` — `Brain` is the unambiguous representational glyph in the existing icon library. No new dep, no brand pipeline blocker. Fallback to `Sparkles` only if downstream theming requires a non-anatomical mark.

**Layout (two modes, toggleable).**
- **Conversational mode (default).** ChatGPT-style. Streaming SSE. `EngineInsightBadge` stays; renamed `DispatchBadge` to show routed role ensemble.
- **CLI mode.** Monospace, prompt-style `gigaton>`. Raw commands: `:engines status`, `:dispatch CFO "model pricing for vendor X"`, `:llm route haiku4.5`, `:source refresh airbnb-ical`, `:hr utilization`, `:approve <task_id>`. Toggle: `Cmd-K`.

**Real-time coaching.** As operator types: debounced (350ms) call to decision-engine `/v1/intelligence/classify` (PR #85) returns `{intent, required_skills[], routed_roles[], confidence, est_cost_usd, est_latency_ms}`. Surfaces inline above input as a `CoachingHint` chip. Operator can edit before submit.

**Information qualification.** Every response renders four fields beside the message body: `confidence (0-1)` · `provenance (source IDs)` · `citations (URLs/refs)` · `next_step (one-line recommendation)`. Sourced from decision-engine response envelope (new field set; additive).

**Routing indicator.** `DispatchBadge` shows the primary role + advisor roles (e.g. `CFO · CRO advisor · 0.83 conf`). Click expands to the dispatch decision record.

---

## 5. The Ti Agent Matrix

**Source.** `master-knowledge-base/CLAUDE.md` org structure: CEO → 9 executives (CTO, CXOO, CISO, CDO, second-CTO, CFO, CMO, CRO, CPO) × ≤7 reports each = up to **63 roles**. Skill axes (CLAUDE.md): `technical, commercial, creative, analytical, operational, interpersonal, environmental, political`.

**Per-role shape** (intel-silo `agent_roles`, PR #41 schema):
```
role_id (slug)         e.g. cfo, cfo.fpa_lead, cto.platform_eng
title                  display
parent_role_id         FK → agent_roles (CEO is root)
skill_vector           jsonb {technical: 0.0-1.0, commercial: …, …} 8 axes
specialization_tags    jsonb multi-axis (per modular-replication doctrine)
cost_tier              enum: claude_haiku|sonnet|opus|gpt-4o|gemini|human_review|deterministic
availability_state     enum: active|throttled|idle|hiring|deprecated
ppim_signature         jsonb
persona_id             FK → persona-engine OrgPersona (PR #12 rows)
lifecycle_state        canonical|active|proposed|archived
```

**Dispatch logic** (decision-engine `dispatch/router.py`, target Week 3 — today it's the PR #85 stub).
1. Classify query → required-skill-vector + ppim_brand_dimension.
2. Cosine-match required-skill-vector vs each role's `skill_vector`.
3. Score = `0.6 * cosine + 0.25 * availability + 0.15 * (1 - normalized_cost)`.
4. Pick top-1 primary; if score gap top-1 vs top-2 < 0.1 OR `error_cost == high`, add top-2 + top-3 as advisors (ensemble).
5. Complex multi-axis tasks (e.g. pricing-strategy = financial+commercial+analytical) → multi-stage ensemble: CFO leads, CRO + CMO comment, CTO sanity-checks unit economics.

**Lazy expansion.** Per `[[foundational_modular_replication_via_input_substitution]]`: Week 1 seeds the **9 executives only** (delivered by persona-engine PR #12). Reports under each executive instantiate on first dispatch demand (matching score < threshold AND no existing report covers the gap). No 63-role bigbang.

**Implementation surface.**
- intel-silo: `agent_roles`, `skill_vectors` tables + REST. **Schema landed in PR #41.**
- persona-engine: 9 OrgPersona rows. **Landed in PR #12.** Reports added lazily Weeks 2-4.
- decision-engine: dispatch router + scoring formula + dispatch_decisions log. **Stub landed in PR #85; full router Week 3.**
- gignet-orchestrator: emits `dispatch.routed.<role_id>` events; fan-out triggers next-task. **Already LIVE (Phases A-G).**

---

## 6. CLI orchestration

**The `/intelligence` page IS the CLI.** Two modes, one surface.

**Flow.** Operator input → gigaton-gateway `/v1/intelligence/dispatch` (Week 4) → decision-engine routes via Ti Agent Matrix → primary role + advisors execute (each role mapped to an engine + LLM tier per its `cost_tier`) → results aggregated by decision-engine into the response envelope → streamed back via SSE.

**Controls (all via CLI commands, all via Pub/Sub fabric).**
- 3rd-party LLMs: `:llm route <task_class> <model>` — wraps gigaton-gateway `app/llm_router/` (Phase D LIVE).
- Source updates: `:source refresh <connector_id>` — intel-silo connectors (Documentation Ingest pattern already shipped).
- Alt AI tools: `:tool register <connector_id>` — connector-api catalog (Pattern A storage).
- Human approvals: `:approve <task_id>` — UAE sign-off matrix.
- Stripe: `:stripe payouts <entity_id>` — gigaton-engine (PAYOUT-1 Connect/ACH paths).
- Messaging: `:msg send <channel> <recipient>` — mimi-whatsapp + connector-api Gmail (per EMAIL-1 + SUPPORT-3).
- Inquiries / listings: `:cbp inquiries|listings` — Carmen-Beach-Properties `apps/web` (L1 surface per ARCH-2).

All commands carry the operator's `X-Client-Namespace` + JWT; namespace middleware (UAE) gates per-tenant scope. Gateway PR #57 stamps `attribution_chain` on every command for the audit trail.

---

## 7. Real-time coaching loop

**On every keystroke** (debounced 350ms): decision-engine `/v1/intelligence/classify` returns intent + routed roles + memory hits (retrieved via intel-silo `memory_items` search using current query + last 5 turns) + a one-line hint. Renders as `CoachingHint` chip.

**On every system output**: response envelope carries `confidence (0-1)`, `provenance` (array of source_ids from intel-silo Source Registry), `citations` (URLs / doc paths), `next_step` (recommended follow-up command). Operator sees all four inline.

**Feedback loop**: each rendered output has accept/edit/reject buttons. Click writes to `coaching_feedback` (intel-silo) with `{dispatch_id, role_id, verdict, edited_text, ts}`. Decision-engine retrains dispatch weights nightly (gradient-free: bumps role-match score on accepts, penalizes on rejects).

**Codification trigger**: per gignet Phase D, when a (intent → role → accept) tuple recurs 50× the LLM router auto-emits a `codification.candidate.*` event → Python deterministic rule replaces the LLM call (per `[[master_project_plan]]` §6 + `04_codification_thresholds.md`).

---

## 8. Self-Engineered HR

**Trigger.** HME nightly job scans `agent_roles.availability_state` + `dispatch_decisions` last-30d. A role enters `hiring` state when:
- Utilization > 90% sustained ≥ 7 days, OR
- Quality (accept-rate) < 60% sustained ≥ 14 days, OR
- Operator-reported gap (`/intelligence`: `:hr gap <skill>`) crosses 3-distinct-operators threshold.

**Recruiting flow** (closed loop, all PPIM-signed, all audited):
1. **JD auto-gen** from role's `skill_vector` + recent task volume + ppim signature → JD lives as a Gignet affiliate-network **9th product type** (`[[master_project_plan]]` Chapter 11 — slot reserved alongside the 8 existing).
2. **Multi-channel sourcing**: LinkedIn API + Indeed MCP (`mcp__claude_ai_Indeed__*` available) + Gignet affiliate-network internal referrals + outbound bundles in the Multipli pattern.
3. **Automated screening**: decision-engine classifies application → persona-engine verifies identity → candidate receives a Multipli-style bundle as a skills assessment (deterministic eval rubric).
4. **Interview booking**: mimi + Google Calendar (`mcp__claude_ai_Google_Calendar__*`) auto-suggests slot windows for the human reviewer.
5. **Offer**: gigaton-engine compensation model (`knowledge-extracts/carmen-beach-agent-costing.md` pattern + CLAUDE.md skills matrix); compensation rate = function of skill_vector match × market benchmark. Payouts via PAYOUT-1 (Stripe Connect Express OR scheduled ACH).
6. **Onboarding**: extends the existing 10-stage operator flow (`[[onboarding_workflow_v1_completion_verified_2026_05_22]]`) with an `agent-of-gigaton` operator type — new entity_type row, no engine rewrite (modular replication).

Every decision audited via gateway PR #57's `attribution_chain`; every interaction PPIM-signed; recruiting loop logged in `recruiting_loops` table.

---

## 9. Build sequence — 6-week arc

**Week 1 (2026-05-26 → 2026-06-01) — Scaffolding.**

Per resume handoff §6 Week 1 build queue. Status as of this writing:

1. ✅ Action #1: `/intelligence` route alias — **gigaton-ui-system PR #41 OPEN, awaiting merge.**
2. ✅ Action #2: intel-silo migration `agent_roles` + `skill_vectors` tables — **intel-silo PR #41 MERGED (`3316bce8`).**
3. ✅ Action #3: persona-engine seed 9 executive OrgPersonas — **persona-engine PR #12 MERGED (`35e6d36c`).**
4. ✅ Action #4: decision-engine stub `POST /v1/intelligence/classify` — **decision-engine PR #85 MERGED (`daaf5e22`).** Honest: keyword-heuristic stub, not semantic.
5. ⏳ Action #5: Pilot CTO role end-to-end (validates full Ti Agent Matrix circuit before fan-out) — **in flight.**

Also Week 1, parallel supporting infrastructure:
- Load decisions log + canonical memory files into the chat context (system prompt extension).
- `Brain` icon swap, `DispatchBadge` component, `CoachingHint` placeholder.
- Gateway substrate (PR #57 attribution_chain, PR #58 slug alias) — **both MERGED.**

**Week 2 — 5-role dispatch.**
- Skill-vector cosine scoring + `dispatch_decisions` table in decision-engine (replaces PR #85 stub heuristic with real cosine match).
- Seed top-5 most-needed reports under each exec (5 × 9 = 45-role intermediate state — but only those that fire on actual operator queries; lazy).
- `:dispatch <role> <query>` CLI command live.
- Skill embeddings backfill begins (offline batch job populating `skill_vectors.embedding` for each of the 9 execs from CLAUDE.md + carmen-beach-agent-costing.md + the first week of dispatch logs).

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
- **Variance-aware self-healing absorbed** as LLM-router calibration loop: dispatch model nightly retraining + Stage 5 variance check against intel-silo baseline catalogs (the original Wave 2 framing per `[[stage_5_variance_aware_self_healing_spec]]` now lands as a calibration sub-routine within the Intelligence Layer).
- decision-engine migration 005 (variance computation) — the originally-planned Wave 2 PR1, sequenced here.
- gigmcp 3-day analysis loop integration — the originally-planned Wave 2 PR2.
- FE variance display in `DispatchBadge` — the originally-planned Wave 2 PR3.

---

## 10. Existing infrastructure leveraged vs net-new

**Leveraged (no rewrite).**
- gignet-orchestrator Phases A-G LIVE (registry + topic + trigger map + LLM router + local node + drift + observability).
- decision-engine Penrose scoreboard + Axiom Registry + Decision Execution Engine.
- intel-silo Source Registry + EO System + memory_items + Documentation Ingest connectors.
- persona-engine OrgPersona + HumanPersona + First Principles Variable Registry + BFT snapshot.
- gigaton-ui-system `/chat` component tree (rebrand, not rebuild).
- gigaton-gateway edge + namespace middleware + LLM router + webhook routes (+ PR #57 attribution_chain + PR #58 alias).
- HME initiative lifecycle + Framework 5.18 Learning Loop + Contribution Matrix.
- connector-api credential storage (Pattern A) + 15 provider probes.
- mimi-whatsapp + Gmail-API+Workspace (EMAIL-1 lock) for recruiting comms.
- Onboarding 10-stage manifest (extends to `agent-of-gigaton` operator type).
- Gignet affiliate network (`[[master_project_plan]]` Chapter 11) — JD slot = 9th product.

**Net-new (intel-silo unless noted).**
- 6 tables: `agent_roles`, `skill_vectors` (both landed in PR #41), `role_assignments`, `dispatch_decisions` (decision-engine, Week 2), `recruiting_loops` (HME, Week 5), `coaching_feedback` (Week 3).
- ~14 endpoints: `/v1/intelligence/{classify, dispatch, feedback}` (classify stub LIVE via PR #85), `/v1/agent_roles`, `/v1/dispatches`, `/v1/recruiting/*`, plus CLI command-router on gateway (Week 4).
- 2 FE components: `DispatchBadge`, `CoachingHint` (Week 1-3).
- 1 nightly HME job: `utilization_sweep` (Week 5).

---

## 11. Decisions made by the design (vs escalated)

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
| 14 | Variance-aware self-healing scope | Sub-task §9 Week 6 (LLM router calibration), not Wave 2 itself | INTEL-1 explicit redefinition |
| 15 | Codification threshold (LLM → Python) | 50-call streak (existing Phase D rule) | gignet_auto_trigger_orchestration §Component 5 + claude-systems/v3.2 codification rule |
| 16 | Bypass direct LLM calls from FE | Never; all via gateway/decision-engine | gigaton-ui-system CLAUDE.md Architecture Contract + CRIT-007 |
| 17 | Per-dispatch cost logging | Existing `llm_call_cost` + new `dispatch_decisions.cost_usd` | universal_connector_hub_architecture §C universal cost telemetry |
| 18 | Multi-tenant scoping | `X-Client-Namespace` middleware (UAE) on every CLI command + attribution_chain (gateway PR #57) | ARCH-1 + ARCH-2 (gateway is the choke; tenants are FEs) |
| 19 | Where does `/chat` route redirect | 301 to `/intelligence` for one release; remove next | gigaton-ui-system convention + decisions log INTEL-1 + gateway alias PR #58 |
| 20 | When to escalate to human reviewer in dispatch | `error_cost==high AND confidence<0.65` OR ensemble disagreement >0.3 | gignet_auto_trigger_orchestration §Component 5 second-opinion gate |

**Pre-locked: 20.** Genuinely escalated (§12): **3**.

---

## 12. Open decisions that need user (max 3)

Each: recommended default + fallback if user doesn't respond by Week 1 close (**defaults fire 2026-06-01**).

### Q1 — Skill-vector seed values for the 9 executives
**Decision.** Initial numeric weights for each of 9 execs across 8 skill axes (72 values total).
**Recommended default.** Symmetric seed per the title's primary axis (e.g. CFO = `{commercial:0.9, analytical:0.9, operational:0.7, …, creative:0.3}`) — agent generates from CLAUDE.md + carmen-beach-agent-costing.md and presents a JSON for user to ratify or amend in 5 minutes.
**Fallback (fires 2026-06-01).** Use the agent-generated table verbatim; calibrate via `coaching_feedback` over Weeks 2-3.

### Q2 — Recruiting human-in-the-loop gate
**Decision.** Does the self-engineered HR loop send the final offer **autonomously** or **after Todd's one-click approve**?
**Recommended default.** One-click approve on first 10 hires; switch to autonomous Week 8+ if accept-rate > 80% and zero compliance flags. Honors PPIM "facilitate, not autonomous-without-human" doctrine + ARCH-1 sunset of operator-local actions only after gigaton-platform proves stable.
**Fallback (fires 2026-06-01).** One-click approve indefinitely; revisit as data accrues.

### Q3 — Coaching opt-out at operator level
**Decision.** Can a tenant operator turn off real-time coaching for privacy/UX preference, or is it mandatory (always-on for PPIM observability)?
**Recommended default.** Always-on for system telemetry (we need the data); UI affords *visual minimization* (collapse the chip) but the dispatch + envelope writes never pause.
**Fallback (fires 2026-06-01).** Always-on, chip-collapsible.

---

## 13. Risks + doctrine mitigations

| Risk | Doctrine mitigation |
|---|---|
| **63-role bigbang collapses under its own complexity** | Lazy expansion (modular-replication §3+§4); seed only 9 execs Week 1 — already enforced by persona-engine PR #12 scope |
| **Dispatch model overfits early operator quirks** | Codification threshold = 50-call streak before deterministic; nightly retrain on `coaching_feedback`; Penrose `drift_critical` metric surfaces overfit |
| **Self-engineered HR makes a compliance-bad hire** | Q2 default = human-in-the-loop offer approval; PPIM "Facilitate" parses "co-pilot for a human owner, not autonomous action" |
| **PR #85 classify stub leaks heuristic results as if semantic** | Response envelope MUST carry `classifier_version: "stub-keyword-v0"` until cosine match lands Week 3; FE renders a "stub" pill when this version is in effect |
| **attribution_chain (gateway PR #57) becomes a PII vector** | Chain stamps role + dispatch_id + entity_id only; never raw operator identifiers; license-check middleware in the same PR gates cross-tenant reads |

---

## 14. Cross-reference table

| Reference | Why it matters here |
|---|---|
| `decisions/2026-05-25_architecture_decisions_log.md` | INTEL-1 + INTEL-2 + ARCH-1/2 lock the frame; PAYOUT-1 governs HR offer/compensation; MIG-CANCEL means engines stay where they are (no reshuffle blocking Wave 2) |
| `[[foundational_goal_gigaton_engineered_brand_experience]]` | Every dispatch must carry PPIM signature; envelope mirrors PPIM atomic schema |
| `[[foundational_modular_replication_via_input_substitution]]` | All catalogs (roles, skills, JDs) use multi-axis JSONB tags; lazy expansion is doctrine-mandated |
| `[[gignet_auto_trigger_orchestration]]` | Phases A-G LIVE substrate; Wave 2 sits on top — every dispatch becomes a gignet event |
| `[[universal_connector_hub_architecture]]` | Connector catalog + cost telemetry pattern reused for `agent_roles` + `dispatch_decisions` |
| `[[master_project_plan]]` Chapter 11 | Gignet affiliate-network 9th product = JD slot (the HR loop substrate) |
| `[[standalone_bundle_net_new_concepts]]` concept 2/3/5 | First Principles Variable Registry + EO System + Experience Engineering Equation feed dispatch features |
| `[[onboarding_workflow_v1_completion_verified_2026_05_22]]` | Reused for `agent-of-gigaton` operator type; verification chain extended |
| `[[stage_5_variance_aware_self_healing_spec]]` | Original Wave 2 framing — now lands as Week 6 sub-task per INTEL-1 |
| `gigaton-ui-system/CLAUDE.md` | Architecture Contract — no FE bypass of backend; CRIT-007 provider+model on every LLM call |
| `master-knowledge-base/CLAUDE.md` | Org structure + 8 skill axes seed the matrix |

---

## 15. PPIM signature (this doc)

```yaml
ppim_axis: meta/intelligence-layer
ppim_priority: P0 — foundational substrate for all Wave 2+ work
ppim_outcome_quality: every operator interaction becomes attributable, qualified, real-time-coached, self-healing
ppim_economics: estimated 60-80% reduction in operator-to-engine routing latency + LLM cost via skill_vector cosine + cost_tier match
ppim_predictability: HIGH — every dispatch records {dispatch_id, role_id, confidence, provenance, citations, attribution_chain}; nightly retrain + codification thresholds keep the dispatch model bounded
ppim_brand_dimension: coherence + intelligence-utilization
ppim_interaction_class: meta (governs every operator query + every system-initiated dispatch event)
```
