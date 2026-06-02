---
name: context-completeness-doctrine-2026-05-26
description: "DOCTRINE — context completeness is a precondition of decision quality, not a byproduct. Every Gigaton surface that produces a decision/answer must measure coverage against the decision's required-categories and refuse below threshold. Launch defaults: 80% block, 60% caveat; per-operator adaptive drift. Operationalized in mkb PR #22 (spec + Q&A Phase 0.5 addendum)."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-26
  authority: locked unless explicitly revisited
  status: ACTIVE — applies to ALL future context-gathering and decision-producing surfaces
  originSessionId: 1f03d51f-3559-418d-b85d-2b270ad71ad8
promoted_from: context_completeness_doctrine_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# Doctrine: Context Completeness Is a Precondition of Decision Quality

## The rule

Every Gigaton surface that asks an operator for context (Documentation Ingest, onboarding chat, `/intelligence` query box, any future "tell us about your X" form) MUST measure how complete that context is against the decision or answer the operator is about to ask for, and MUST refuse to produce a decision below a configurable threshold.

**Why:** the user directive 2026-05-26 (verbatim, after the OAuth-publish smoke test surfaced a partial-success state): *"ensure all context possible > required to achieve decisions & answers to questions are completed."* That sentence is a precondition gate, not a retrieval improvement. A surface that produces a decision without measuring whether it had enough context is **lying about confidence** and incurs the much larger downstream cost of operator-trust loss + re-work.

**How to apply:** Whenever you find yourself building, reviewing, or extending a surface that takes operator input and produces a decision/answer:

1. Identify the decision-type the surface produces.
2. Verify there is a `decision_required_categories` row for it.
3. Verify the surface calls `POST /v1/context/coverage` before producing.
4. Verify the surface respects the returned `threshold_zone`:
   - `clean` (≥ 0.80) → produce clean.
   - `caveat` (0.60-0.80) → produce with caveat banner + elicitation prompt.
   - `block` (< 0.60) → refuse + open elicitation drawer with top-3 next questions.
5. Verify the surface emits a `qa_attempted_with_coverage` or equivalent event into `context_loop_events` for the recursive learning loop.

If the surface predates the layer (built before PR-1 of the implementation ships), add a TODO comment with the doctrine name. Do not retrofit silently; surface the gap.

## The four corollaries

1. **A surface that produces a decision without measuring context completeness is lying about confidence.** Trustworthy-tokens-on-complete-corpora > many-tokens-on-incomplete-corpora.
2. **Coverage is decision-relative, not corpus-relative.** A 100%-coverage corpus for one decision can be 12% coverage for another. Score against the decision's `required_categories`, not the corpus size.
3. **Operator self-report is weighted lower than corpus evidence** (60/40 in launch formula). Operators can game self-report but not corpus content.
4. **Thresholds are adaptive, not fixed.** Per-operator drift via observed outcome quality (EWMA, α = 0.05) bounded by ± 0.15 from launch defaults. Operators who consistently produce great decisions at lower coverage have demonstrated calibration; their threshold lowers. Operators who produce poor decisions at high coverage are over-confident; their threshold rises.

## Cross-links

- Spec: `master-knowledge-base/docs/architecture/2026_05_26_context_gathering_completeness_layer.md` (via [mkb PR #22](https://github.com/todd-gig/master-knowledge-base/pull/22)) — see spec §13.5 for the INTEL-3 seed registry: every threshold in this doctrine is a seed-with-bounds, not a fixed target
- INTEL-3 alignment: [[intel_3_no_static_weights_algorithmic_determination_2026_05_26]] — this layer ships INTEL-3-compliant at launch (seeds + bounds + WeightSourcedFromSeed emission); Phase 2 (week of 2026-06-02) replaces seed lookups with computed values
- Foundational goal: [[foundational_goal_maximize_human_superpowers]] — context completeness IS the gate that ensures every operator query taps the full intelligence stack instead of leaking chunks-with-citations
- Universal Acquisition Framework: [[universal_acquisition_framework_2026_05_26]] — every UAF stage consumes context completeness scores; signal capture + IDP profile + needs inference all generate coverage evidence
- Q&A Phase 0.5 addendum: `master-knowledge-base/runbooks/2026_05_25_intelligence_qa_on_ingested_files_phase_0_5_addendum.md` (same PR)
- Parent Q&A runbook: `master-knowledge-base/runbooks/2026_05_25_intelligence_qa_on_ingested_files.md` (merged in mkb PR #14)
- Wave 2 design: [[stage_5_variance_aware_self_healing_spec]] + `docs/architecture/2026_05_25_wave2_intelligence_layer_ti_agent_matrix.md` (this layer feeds the `/intelligence` surface)
- 7×7 schema origin: `chatgpt-conversations/gigaton-threads/ChatGPT MD -Proof of Action Influence Trust.md`
- Ethnographic frames: `~/.claude/skills/ethnographic-research/SKILL.md`
- Related foundational: [[foundational_goal_gigaton_engineered_brand_experience]] (PPIM); [[foundational_modular_replication_via_input_substitution]] (lazy expansion via PPIM multi-axis tags); [[universal_connector_hub_architecture]] (the source-palette this layer extends)

## Anti-patterns this doctrine kills

- Building a "smart" `/intelligence` query box that always answers regardless of corpus depth.
- Adding a new source connector without exposing the coverage score it raised.
- Producing a decision via LLM with confidence > 0.8 when corpus has < 5 chunks across only 1 category.
- Hand-tuning thresholds globally instead of per-operator-adaptive.
- "We'll add the coverage gate later" — this is the doctrine; it ships now (PR #22 spec; implementation PRs to follow).
