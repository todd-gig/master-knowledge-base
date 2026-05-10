---
title: Decision — Unified context bundle (Stage 3.5) + adaptive LLM selection (Stage 3.6)
date: 2026-05-09
decided-by: Todd (operator)
applied-by: Claude in Cowork session
status: ACTIVE — implementation underway in 5 slices (this commit lands slices 1–5 as scaffolds)
companion: 2026-05-09_routing_scorer_high_stake_detection.md (high-stake routing tiers; depends on this doc's bundle)
---

# Problem

Stage 4 of the operator-api `/intelligence/query` pipeline calls the LLM with whatever context Stage 3 (cxguy-methodology shape) built. Stage 3 only consults `memory-service`. There are 18 other substrate sources (silo's 4-tier memory, ontology, processes, 300-EXPERT registry, decision history, calibration weights, Process catalog, transcripts, braintrust KB, master KB, user/org/client context, queue items, recent events, policies, tenant config) that should also be in the prompt. Without them, the LLM hallucinates or under-uses the operator's accumulated structured history.

Separately: there is no logic that **chooses which LLM** based on the input characteristics + user's available providers. `intel_router.py` does a small subset of this (multimodal → gemini, structured → openai, longform → anthropic) but does not consider context size, cost, calibration history, stake, or user key availability.

# Decision

Insert two new stages between Stage 3 and Stage 4:

```
Stage 3   cxguy-shape           (existing)
Stage 3.5 ContextBundler        (NEW) — pull from all 19 substrate sources, rank, trim to budget
Stage 3.6 LLMSelector           (NEW) — choose provider+model from user's available options
Stage 4   LLM call              (existing) — now receives the full bundle
Stage 5   store + cert chain    (existing)
```

Both new stages run inside operator-api. They produce a single `ContextBundle` dataclass that flows into Stage 4 and a separate `LLMCandidates` ranked list. Audit row written on every call.

# Why

1. **The substrate exists; the LLM doesn't see it.** The operator has 1,202 KB docs, 13 braintrust sessions, a 300-EXPERT registry, a Process catalog (G0.1), entity ontology, decision history, calibration weights — but the chat-path LLM never gets handed any of this beyond what Stage 3's narrow memory recall surfaces.

2. **LLM selection is currently a hard-coded heuristic.** Cost, latency, capability, context size, and outcome history should drive routing — not just intent type. With per-user BYOK keys (`/operator/intelligence/user-keys`) and per-org defaults (migration 024), routing must respect what each user has configured.

3. **Closed learning loop is missing without an audit row.** calibration-service can only learn from the chat path if every call records: which substrate slices were in the bundle, which LLM was chosen, what reasons drove the choice, and what outcome resulted (thumbs feedback). New `context_bundle_audit` table provides this.

4. **High-stake routing (the prior decision) needs a richer bundle.** The prior `RoutingScorer` design (`2026-05-09_routing_scorer_high_stake_detection.md` — pending) determines whether to fire single-LLM, silo, committee, or committee+critic. Each of those modes consumes the same bundle. Build the bundle once; route N ways.

# Architecture

## Stage 3.5 — ContextBundler

Single function `assemble_context_bundle(user_input, user_id, intent, routing_score)` runs **asyncio.gather across 19 substrate fetches**:

| Source | Endpoint / call | Returns |
|---|---|---|
| memory.working | silo `/memory/query` (class=working) | tensor-backed current-session attention |
| memory.episodic | memory-service `/memory/retrieve_similar` (class=episodic, k=10) | recent experiences (90d default) |
| memory.semantic | memory-service `/memory/retrieve_similar` (class=semantic, k=10) | persistent facts |
| memory.procedural | silo `/memory/query` (class=procedural, k=5) | what worked before |
| ontology.entities | entity-resolution `/resolve` + ontology `/entities` | canonical entities mentioned |
| ontology.neighbors | ontology `/relationships` (hops=2) | related entities + edges |
| processes | operator `/processes` (match by intent) | matching Process catalog entries |
| experts | operator `/experts/match` | personas from 300-EXPERT registry |
| similar_decisions | decision-engine `/decisions/similar` (k=5) | past decisions on similar topics + outcomes |
| applicable_policies | decision-engine `/policy/applicable` | policies that apply to this operator + intent |
| calibration | calibration-service `/state` (operator_id, org_id) | weight versions for value/trust |
| queue_context | operator `/queue/decisions?status=pending&filter=relevant` | pending SIE items relevant to topic |
| transcripts | transcript-knowledge-base recent (30d, semantic match) | recent call transcripts |
| braintrust | braintrust-knowledge-base relevant | strategic-sync sessions |
| master_kb | master-knowledge-base search (k=3) | framework / decision docs |
| user_profile | Firebase Auth + Firestore user doc | identity + role + RBAC |
| org_context | ontology `/org` + Firestore org doc | tenant defaults + policies |
| client_context | if client_id in scope | per-client substrate (Carmen Beach, Liquefex) |
| recent_events | feedback-service `/events?operator=&limit=20` | last N outcomes for this operator |

Every fetch is wrapped in try/except — failures return `None` and are logged but don't block the bundle assembly. The bundle's `substrate_completeness` field reflects how many sources contributed.

Ranking uses cxguy-methodology's `rank_evidence(items, query)` which applies Trust × Value × Priority weighting. Result is a single ordered list across all sources.

Budget management: `trim_to_budget(ranked_bundle, target_provider)` drops lowest-priority items until the bundle fits the chosen LLM's context window minus a `RESERVE_FOR_OUTPUT` slack (default 16k).

## Stage 3.6 — LLMSelector

Single function `compute_llm_candidates(intent, bundle, user_keys, routing_score)` returns a ranked list of `LLMCandidate(provider, model, score, reasons)` tuples.

Scoring criteria:

- **Bundle size fit**: prefers high-context-window models when bundle > 100k tokens (claude-opus-4-7 1M, gemini-2.5-pro 1M)
- **Capability match**: multimodal → gemini, structured-output → openai, longform → anthropic
- **Stake**: high stake (routing_score ≥ 6) → most capable available; low stake → silo (zero cost)
- **Cost sensitivity**: per-org `cost_preference` config — `cheap` biases silo, `quality` biases anthropic
- **Latency sensitivity**: per-org `latency_preference` — `fast` biases sonnet over opus
- **User key availability**: candidates filtered to providers the user has BYOK keys for, OR org default keys, OR silo (always available)
- **Compliance**: per-org `pii_policy` — e.g. `silo_only` excludes cloud providers
- **Calibration history**: providers that produced higher outcome_score for similar past prompts get boosts (cold-start: equal weight)

Output ranked list — Stage 4 picks `[0]` as primary, retains `[1]` and `[2]` as fallback chain.

## Stage 4 — LLM call (modified)

The call now passes `bundle` into the LLM as structured context. Provider-specific format:

- **Anthropic**: XML tags in system prompt
  ```xml
  <memory>...</memory>
  <entities>...</entities>
  <experts>EXP-077, EXP-189</experts>
  <similar_decisions>...</similar_decisions>
  <applicable_policies>...</applicable_policies>
  ```
- **OpenAI**: structured system message + JSON schema for tool use
- **Gemini**: structured `parts` array
- **Silo (gigaton-local)**: bundle is local-redundant (silo already accesses these tiers); pass intent + query only

If primary LLM fails (rate limit, error, timeout), Stage 4 retries on `[1]` then `[2]`. Each attempt logged to `context_bundle_audit`.

## Migration 028 — context_bundle_audit

```sql
CREATE TABLE context_bundle_audit (
    bundle_id              VARCHAR(64) PRIMARY KEY,
    operator_id            VARCHAR(255),
    org_id                 VARCHAR(255),
    user_query_hash        VARCHAR(128),
    intent                 JSONB,
    routing_score          INT,
    substrate_sources      JSONB,        -- which sources contributed + token weights
    substrate_completeness NUMERIC(3,2),
    llm_candidate_chosen   TEXT,
    llm_candidate_score    INT,
    llm_candidate_reasons  JSONB,
    llm_candidates_full    JSONB,        -- full ranked list
    estimated_input_tokens INT,
    actual_input_tokens    INT,
    actual_output_tokens   INT,
    latency_ms             INT,
    cost_estimate_usd      NUMERIC(10,6),
    outcome_score          NUMERIC(3,2), -- updated when user rates
    outcome_updated_at     TIMESTAMPTZ,
    created_at             TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_bundle_audit_operator ON context_bundle_audit(operator_id);
CREATE INDEX idx_bundle_audit_outcome  ON context_bundle_audit(outcome_score DESC);
CREATE INDEX idx_bundle_audit_org      ON context_bundle_audit(org_id);
```

Doubles as the **license-attribution audit log** the prior `INTELLIGENCE_LLM_ENABLED` decision flagged as eventually needed for the 60/40 dual-ownership model.

## Calibration loop

After user rates the response (thumbs up/down on ChatPage):
1. `feedback-service` writes `outcome_records` row (existing)
2. New trigger: also UPDATE `context_bundle_audit.outcome_score` for matching `bundle_id`
3. calibration-service nightly job scans `context_bundle_audit` for the last 7 days
4. Computes per-LLM-candidate, per-substrate-source outcome rates
5. Updates LLMSelector scoring weights so future similar prompts route to historically-better LLMs
6. Updates ContextBundler ranking weights so historically-useful sources get higher cxguy-priority

# Implementation phases (5 slices)

| Slice | What | Files | Effort |
|---|---|---|---|
| 1 | ContextBundler core | `intelligence/context_bundler.py` | 1 day |
| 2 | LLMSelector ranking | `intelligence/llm_selector.py` | 1 day |
| 3 | SubstrateInspector min-gate (extends prior decision) | `intelligence/substrate_inspector.py` | 0.5 day |
| 4 | Migration 028 + Stage 4 integration hooks | `migrations/028_context_bundle_audit.sql`, `intelligence/integration_hooks.py` | 1 day |
| 5 | Provider formatters + tests + calibration writeback | `intelligence/formatters.py`, `tests/contract/test_context_bundler.py`, calibration nightly job extension | 1.5 days |

**Total ~5 days. This commit ships scaffolds for all 5.** Real-call wiring per slice fills in subsequent commits.

# Cost / risk

**Cost per request (est.):**
- ContextBundler: ~50ms wall-clock (asyncio.gather of 19 fetches), most local
- LLMSelector: ~1ms (pure Python)
- Bundle audit insert: ~5ms
- LLM call: provider-dependent (existing, unchanged)
- **Net added latency: ~60ms — negligible vs LLM call (500-2000ms)**

**Risk:**
- Bundle assembly failures cascade if asyncio.gather isn't fail-soft (mitigated by per-source try/except)
- Token over-budget if trim logic has off-by-one (mitigated by 16k reserve)
- LLMSelector picks wrong provider when calibration history is sparse (mitigated by cold-start equal weight + observability)

**Reversible**: every new module is additive. Disabling is one config flag.

# Acceptance criteria (per slice)

- **Slice 1**: `assemble_context_bundle("test query", "test_user", intent, routing_score=5)` returns ContextBundle with ≥10 of 19 sources contributing.
- **Slice 2**: `compute_llm_candidates(...)` returns ranked list with ≥1 candidate that passes user-key check; ordering deterministic given same inputs.
- **Slice 3**: when SUBSTRATE_MIN not met, sets `routing_hint="force_silo"` and emits log line.
- **Slice 4**: migration 028 applies cleanly; every Stage 4 call writes a row.
- **Slice 5**: contract tests pass; calibration nightly job updates LLMSelector weights based on last-7d outcomes.

# Companion decisions

- `2026-05-09_routing_scorer_high_stake_detection.md` (pending) — defines the 0–10 stake score this bundle is consumed by
- `2026-05-08_INTELLIGENCE_LLM_ENABLED_off_pending_tracking.md` (superseded) — bundle audit closes the original audit-log gap
- `2026-05-08_affiliate_centralization_at_gigaton.md` — chain 22 v2 endpoints can also use the bundle for proposal-shaping

# Rollback

Each new module is additive. To disable:
1. Set env `INTELLIGENCE_BUNDLE_ENABLED=0` on operator-api → Stage 4 falls back to current Stage 3-only context
2. Migration 028 stays applied (additive, no destructive change)
3. LLMSelector falls back to current `intel_router.py` heuristic if module fails to import
