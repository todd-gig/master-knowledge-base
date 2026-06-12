---
name: intel-3-no-static-weights-algorithmic-determination-2026-05-26
description: "INTEL-3 doctrine LOCKED 2026-05-26 EOD by Todd. All decisions made by internal Gigaton systems logic. Very few static weights — effectively none. All weights determined as a function of algorithm with real-time adjustments. Extends INTEL-2 (decision-routing algorithmic) to INTEL-3 (decision-value algorithmic). Applies platform-wide: comp/payout %s, scoring weights, thresholds, allocations, attribution shares, retry params, etc."
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  status: "LOCKED — foundational doctrine, platform-wide"
  scope: "every operator, every event, every weight, indefinite"
  urgency: HIGH — invalidates static-weight scaffolds (PR
  originSessionId: b8909926-050d-414d-acfb-51bd96fca09c
promoted_from: intel_3_no_static_weights_algorithmic_determination_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# INTEL-3 — No static weights; algorithmic determination with real-time adjustment

## The directive (verbatim)

Todd, 2026-05-26 EOD:

> "all decisions will be made by internal gigaton systems logic with very very efw > no weights will be static and determined as a function of algorithm > real time adjustments"

(my read: "very very efw" = "very very few" — autocorrect)

## What this means

- **Scope:** every decision value across the platform — comp/payout %s, scoring weights, thresholds, allocation buckets, attribution shares, retry params, cadence intervals, ranking weights, classification confidences, anything that today exists as a `0.55` or `30%` or `$15k` baked into a doc, table, env var, or code constant.
- **Constraint:** these cannot be static. They must be computed by an algorithm at request/event time using real-time inputs.
- **Exception (very small):** rules that are *binary policy* (round UP vs DOWN, platform-absorbs-ACH-fee yes/no, human-in-loop gate yes/no) survive as static — they're not weights. Same with floors that are contractually-locked policy (e.g., $1k min payout per PAYOUT-1 — that's a floor, not a weight, and the user has locked it explicitly).

## Relationship to existing locks

- **INTEL-1** (Wave 2 = Intelligence Layer + Ti Agent Matrix + Self-Engineered HR) — UNCHANGED; this doctrine specifies HOW the Intelligence Layer governs weight computation.
- **INTEL-2 META-DOCTRINE** (all decisions made by system intelligence ASAP, route through memory → decisions log → doctrine → Ti Agent Matrix before escalating to user) — EXTENDED. INTEL-2 governed decision *routing*. INTEL-3 governs decision *values*.
- **PAYOUT-1 base + clarifications** ([[payout_1_min_threshold_1k_2026_05_26]], [[payout_1_and_intel_1_clarifications_locked_2026_05_26]]) — UNCHANGED for the binary/policy parts (round UP, bi-weekly Wed cadence, platform absorbs ACH fee, no first-time exception, $1k floor). These are rules, not weights.
- **INTEL-1 cosine thresholds 0.55 / 0.35** — these were already documented as "tunable post-real-data observation" via env vars. Now firmly under INTEL-3 — they should be computed by the algorithm per query context, not env-locked. Env values become initial seeds only.
- **§3 of PR #17 comp+payout structure doc** — INVALIDATED as written. Static % tables must be reframed as algorithmic policies + initial seeds + bounded ranges.

## How to apply

### Every existing static weight must move through this 3-step lifecycle:

1. **Identify** — every `0.X` / `XX%` / `$XX,XXX` / threshold constant gets cataloged in a master weight registry. Source of truth: master-knowledge-base.
2. **Bound** — each weight gets a `[min, max]` policy range + a `seed` value (initial). The range is binding; the seed is replaceable.
3. **Compute** — decision-engine emits a `WeightComputed(name, value, computed_at, inputs, model_version)` event for every weight resolution. UI/billing/scoring reads the computed value, never the seed.

### Inputs available to the weight-computation algorithm:

- Operator state (UAE.client_namespaces → tier, lifecycle_state, governance_overlays, history)
- Market conditions (industry-vertical baselines from intel-silo gigmcp pre-research)
- Performance signals (recent PPIM outcome data, conversion rates, dispute rates, satisfaction proxies)
- Variance from expected (Wave 2 variance display, INTEL-1 deviation signal)
- Time-of-event context (time of day, cadence position, contract anniversary)
- Cross-operator benchmarks (when authorized — depends on namespace governance per [[mcp_multi_tenant_namespace_blocker_2026_05_26]])

### Implementation phasing

- **Phase 1 (this week — PR #17):** ship seeds + bounded ranges + algorithm-pending markers. Status can go ACTIVE on the seeds only because there's no algorithm yet. Decision-engine billing module operates in seed-mode until Phase 2.
- **Phase 2 (revision window week of 2026-06-02):** algorithm spec PR — define the weight-computation function per weight category (comp routing, payout cadence, scoring weights, etc.). Replace seeds with `WeightComputed(...)` event emissions.
- **Phase 3 (Wave 2 maturity):** decision-engine `/v1/intelligence/classify` learns per-operator weight patterns; seeds become deprecated; INTEL-3 fully realized.

## Why this matters

Static weights are the SIE chain 22 brand-coherence anti-pattern (one-size-fits-all-operators). INTEL-3 makes the platform genuinely PPIM-aligned: every weight reflects the specific operator's specific event in specific market conditions. This is what "Gigaton engineered brand experience" means — the math itself bends to the operator's reality.

It also de-risks the comp+payout doc: Todd's "accept all" with mid-norm seeds is safe because seeds are temporary; the algorithm makes them right per-event.

## How to apply in current work

- **PR #17 comp+payout doc:** Will ship with `seed` values + `[min, max]` bounds + an explicit "algorithm-pending" footer. Status CAN flip to ACTIVE on seeds. Comments noted (next-week revision = algorithm spec, not number tweaks).
- **gigaton-engine billing module:** Stay in seed-mode until algorithm spec ships. Emit `WeightSourcedFromSeed(...)` events so we can see how often each seed fires without algorithm override.
- **decision-engine semantic_classifier cosine thresholds:** env-readable constants stay as seeds; thresholds become per-call computed values once Phase 2 ships.
- **Wave 2 PR3 variance display:** UI surfaces COMPUTED values + a tooltip showing seed-vs-computed if user requests transparency.
- **Future static weights flagged in PRs:** any new PR introducing a numeric weight must either (a) declare it explicitly as a binary/policy rule that's exempt from INTEL-3, or (b) ship it as a seed with bounds + a TODO marker for algorithm replacement.

## Related

- [[payout_1_and_intel_1_clarifications_locked_2026_05_26]] — INTEL-1 cosine thresholds (seeds under INTEL-3 going forward)
- [[payout_1_min_threshold_1k_2026_05_26]] — $1k floor (policy, exempt from INTEL-3)
- [[RESUME_HERE_2026_05_26_full_session_handoff]] §4 INTEL-2 META-DOCTRINE (extended by this)
- [[sibling_fleet_state_and_mig_cancel_conflict_2026_05_26]] — sibling work on Wave 2 build queue items 2-4 should incorporate INTEL-3 input-collection patterns
- master-knowledge-base PR #17 — first doc to ship under INTEL-3 phasing (seeds → algorithm)
