# Q&A Pipeline Phase 0.5 Addendum — Context Completeness Gate

**Parent runbook:** `runbooks/2026_05_25_intelligence_qa_on_ingested_files.md` (merged via mkb PR #14, 2026-05-26 18:03Z)
**Authored:** 2026-05-26 evening
**Authority:** locked unless explicitly revisited
**Companion spec:** `docs/architecture/2026_05_26_context_gathering_completeness_layer.md`

---

## What this addendum changes

Inserts **Phase 0.5** between Phase 0 (silo Q&A endpoint exists, classifier wired) and Phase 1 (chat → silo wiring) of the parent runbook. Phase 0.5 makes the Q&A endpoint **decision-quality-bounded** instead of "best-effort RAG with citations."

## Why this addendum exists

The parent runbook's Phase 1 surfaces a `POST /v1/qa/ask` endpoint that runs Society-of-Minds reasoning over the operator's ingested corpus and returns `{answer, citations[], society_trace, confidence, principles_check, research_backfill[]}`. That endpoint is well-designed for **answering well from whatever is there**. It is *not* designed for **knowing when the corpus is insufficient to answer well**.

Per the 2026-05-26 user directive (verbatim in §1 of the companion spec): *"ensure all context possible > required to achieve decisions & answers to questions are completed."* That sentence is a precondition gate, not a retrieval improvement. The Q&A pipeline must therefore route every incoming question through a coverage check **before** running Society-of-Minds.

Without Phase 0.5, an operator with a thin corpus (e.g., 6 PDFs uploaded, no elicitation answers) and a complex decision (e.g., "should I expand to Mexico City?") gets a fluent-sounding answer that the silo has no basis for. With Phase 0.5, that same operator gets routed to elicitation first, then the question runs against a corpus that has crossed the coverage threshold for that decision-type.

---

## Phase 0.5 — Coverage gate

### 0.5.a — Inbound Q&A interception

`POST /v1/qa/ask` accepts an optional `bypass_coverage_gate: bool = false` (admin/debug only). Default flow:

1. Receive `(operator_id, question_text)`.
2. Call the classifier (built in Phase 0) → `(decision_type, required_skills, routed_roles, confidence)`.
3. Call `POST /v1/context/coverage` (built in companion spec PR-1) with `(operator_id, decision_type)` → `{coverage_score, breakdown, threshold_zone, next_questions, next_sources}`.
4. Branch on `threshold_zone`:

| Zone | Action |
|---|---|
| `clean` (≥ 0.80 by default) | Proceed to Phase 1 Society-of-Minds reasoning. Stamp `coverage_score` on the response. |
| `caveat` (0.60–0.80) | Run Society reasoning **AND** include in response: `caveat: { reason, coverage_score, next_questions[3], next_sources[3] }`. UI renders a non-blocking banner. |
| `block` (< 0.60) | Do NOT run Society. Return `{ blocked: true, coverage_score, top_gaps: { questions[3], sources[3] }, elicitation_drawer_payload }`. UI opens elicitation drawer. |

### 0.5.b — Coverage event emission

For every `/v1/qa/ask` call, emit a `qa_attempted_with_coverage` event into `context_loop_events` (table from companion spec §4):
```
{ operator_id, decision_type, coverage_score, threshold_zone, blocked, emitted_at }
```

Feeds the monthly re-rank job (§10.2 of companion spec) — which questions correlate with which Q&A outcomes.

### 0.5.c — Response stamping

The `EngineInsight` envelope that Phase 1 will eventually assemble at the chat gateway gets two new fields:
```
coverage_score: float            # 0.0-1.0
coverage_zone: "clean"|"caveat"  # never "block" — those don't reach here
```

These ride through to the FE so the chat UI can render the caveat banner.

---

## Sequencing — when does Phase 0.5 ship?

| Dependency | Status |
|---|---|
| Companion spec PR-1 (silo schema + endpoints + scorer + elicitation engine) | Must land first |
| Companion spec PR-2 (gateway route) | Must land first (so coverage call routes correctly) |
| Companion spec PR-3 (FE coverage panel + drawer) | Can land in parallel — FE consumes from same endpoints |
| Companion spec PR-5 (decision-engine precondition) | Lands in parallel; covers non-Q&A decisions too |

**Phase 0.5 ships as the FIRST commit on the Q&A pipeline branch** — before any Society-of-Minds wiring. That way every subsequent commit on the Q&A branch builds on a bounded foundation.

---

## What does NOT change in the parent runbook

- Phases 1-5 sequence and content remain valid.
- The 5 open questions (the user's response captured in PR #14 stated all 5 are decided autonomously) are unaffected; coverage gate is orthogonal to them.
- Society-of-Minds reasoning, ethnographic frame projection, principles filter, web-research backfill — all unchanged.

The only change to Phase 1's `POST /v1/qa/ask` is: it now starts with a coverage check, branches on the zone, and stamps the response. Society-of-Minds and everything downstream are unchanged.

---

## Test plan (additions to Phase 1 acceptance)

- [ ] `POST /v1/qa/ask` for operator with 0 corpus + 0 elicitation → returns `blocked: true`, no Society call made.
- [ ] Same operator after answering 3 high-quality elicitation questions → coverage rises, response unblocks.
- [ ] Operator with rich corpus (50+ chunks across 5 categories) → returns `clean`, full Society response.
- [ ] Operator in caveat zone → response includes both Society answer AND caveat payload.
- [ ] `bypass_coverage_gate=true` (admin) → skips gate but logs `bypass_used` event.
- [ ] `qa_attempted_with_coverage` event appears in `context_loop_events` for every call.

---

## Cross-references

- Companion spec: `docs/architecture/2026_05_26_context_gathering_completeness_layer.md`
- Parent runbook: `runbooks/2026_05_25_intelligence_qa_on_ingested_files.md`
- Doctrine memory: `[[context_completeness_doctrine_2026_05_26]]` (forthcoming)
- INTEL-1 + INTEL-2: `decisions/2026-05-25_architecture_decisions_log.md`
