---
name: payout-1-and-intel-1-clarifications-locked-2026-05-26
description: "7 clarifications LOCKED 2026-05-26 EOD (Todd accepted defaults): 4 PAYOUT-1 + 3 INTEL-1. Resolves all open architectural-decision-log clarifications dated 2026-05-25. Defaults no longer auto-fire 2026-06-01."
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  status: LOCKED — Todd accepted defaults; supersedes 6/01 auto-fire
  scope: "every operator, every interaction, indefinite"
  originSessionId: fc56c866-aa65-41d6-a729-1d21c8fe1dcb
promoted_from: payout_1_and_intel_1_clarifications_locked_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# 7 clarifications LOCKED — 2026-05-26 EOD (Todd accepted)

## PAYOUT-1 clarifications (4)

### Rounding direction
**LOCKED: Round UP** — favor recipient.
- **Why**: Trust-builder; sub-$1 impact per payout; aligns PPIM brand-coherence axis.
- **How to apply**: every payout calculation `math.ceil(amount_cents)`; document on payout receipts.

### ACH cadence
**LOCKED: Bi-weekly (every other Wednesday)**.
- **Why**: Matches Mexican payroll norm for CBP owners + gives Stripe a 2-day clearing window; reduces operator-side reconciliation overhead.
- **How to apply**: Stripe Connect Express `payout_schedule.interval='weekly'` + `weekly_anchor='wednesday'` + skip every other week via internal scheduler. ACH alternative same cadence.

### ACH fee bearer
**LOCKED: Platform absorbs**.
- **Why**: Recipients see clean amounts; Gigaton's payout volume justifies aggregating the fee in our cost line rather than fragmenting recipient experience.
- **How to apply**: Stripe Connect Express config `application_fee` = 0 on the payout side; ACH fee added to gigaton-engine billing module COGS line, not recipient deduction.

### First-time payout exception
**LOCKED: No exception**.
- **Why**: $1k floor is the contract; first-timer accumulates normally; predictability > one-time-friendliness.
- **How to apply**: No special case logic in payout engine. First payout uses identical threshold + cadence as steady-state.

## INTEL-1 clarifications (3)

### Skill-vector seed values (cosine thresholds for classifier)
**LOCKED: 0.55 primary / 0.35 secondary**.
- **0.55**: cosine similarity threshold above which a skill is considered a PRIMARY match (drives `primary_role_key`)
- **0.35**: cosine similarity threshold above which a skill is considered a SECONDARY match (drives `routed_roles[]` entries, not primary)
- **Why**: Standard sentence-transformers/all-MiniLM-L6-v2 heuristic for technical-text similarity; tunable post-real-data observation
- **How to apply**: env-readable constants in `decision-engine/engine/intelligence/semantic_classifier.py` — `COSINE_PRIMARY_THRESHOLD=0.55` + `COSINE_SECONDARY_THRESHOLD=0.35`. Override per-deploy via env.

### HR offer human-in-loop gate
**LOCKED: YES — every HR offer requires human pre-review**.
- Self-Engineered HR auto-drafts offer (job ad, comp package, equity offer, etc.) → routed to operator pre-send approval queue
- **Why**: Per CRIT-001 ("automation requires human override"); HR offers carry legal + retention consequences
- **How to apply**: persona-engine HR module emits `OfferDrafted` event → human-management-engine queues for operator approval → operator clicks "send" or "edit & send" → only then does it leave the platform

### Coaching graduation (REVISED 2026-05-26 EOD — supersedes opt-out)

**LOCKED: NO opt-out toggle. Coaching is automatically REMOVED or CHANGED based on operator-demonstrated competence.**

- **Mechanism**: coaching nudges fire by default for every operator. As the operator demonstrates understanding of system functionality through (a) correct actions in the UI and (b) accurate prompts when interacting with the chat interface, the corresponding coaching nudges are auto-suppressed for that operator.
- **Per-nudge graduation**: each coaching nudge category (e.g. "how to connect a Drive folder", "how to interpret variance display", "how to use the prompt suggestor") graduates independently — operator can have advanced status on connectors but still receive nudges on, say, the affiliate dashboard.
- **Graduation criteria** (per nudge category):
  - **Correct actions**: operator completed the corresponding UI flow without error N times (default N=3)
  - **Accurate prompts**: operator's chat prompts in that domain hit the relevant intent classifier with confidence ≥ 0.55 (matches our primary cosine threshold) M times (default M=2)
  - Both criteria must be met to graduate
- **Re-emergence**: if operator regresses (errors return, or chat prompts drop below 0.35 accuracy), coaching for that category re-activates
- **No opt-out toggle**: explicitly removed — this was Todd's revision 2026-05-26 EOD
- **Why**: opt-out lets operators turn off the system's only built-in onboarding correction; the graduation model preserves the autonomy intent (no nag once competent) without the regression risk (operator turns it off + never gets help when they need it)
- **How to apply**:
  - `agent_roles.coaching_categories` jsonb list per role defining the nudge categories that role emits
  - new table `coaching_graduation_state` per (operator_id, nudge_category) tracking correct_action_count + accurate_prompt_count + graduated_at + last_regression_at
  - persona-engine emits nudge → checks `coaching_graduation_state` → suppresses if graduated → else delivers
  - decision-engine intelligence/classify confidence scores feed `accurate_prompt_count` increments
  - UI flow completions emit `CoachingProgressEvent` to HME → updates `correct_action_count`
  - Spec follow-on (separate PR) to define every nudge category + its criteria thresholds; ship behind a `coaching.v2_graduation` feature flag

## Cross-references

- [[payout_1_min_threshold_1k_2026_05_26]] — $1k min threshold (base PAYOUT-1 amendment)
- [[compensation_payout_structure_thursday_5_28_deadline]] — Thursday 5/28 docs deadline (incorporates these locked clarifications)
- [[product_service_package_gigaton_ti_solutions]] — go-to-market compensation framing
- `master-knowledge-base/decisions/2026-05-25_architecture_decisions_log.md` — original PAYOUT-1 + INTEL-1 entries (these clarifications supersede the "defaults fire 2026-06-01" notes)
