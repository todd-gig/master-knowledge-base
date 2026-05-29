# What you'll do in Stage 5 — Industry Processes (3-minute walkthrough)

Stage 5 is owned by the **decision-engine**. Secondary engine is **persona-engine** (it supplies the ICP segments that condition catalog filtering). Stage 5 consists of **two actions**:

1. `select-industry`
2. `triage-catalog`

## Action 1 — `select-industry`

You select your primary **industry + sub-vertical**. The selection drives which process catalog loads. Examples:

- industry: hospitality / sub_vertical: vacation rental
- industry: hospitality / sub_vertical: hotel
- industry: real-estate / sub_vertical: residential brokerage
- industry: real-estate / sub_vertical: short-term-rental management
- industry: services / sub_vertical: marketing agency
- industry: services / sub_vertical: management consulting

The chat affordance is `multiple_choice` (button group). **The action inherits from Stage 0 declarations where present** — if you declared an industry in Stage 0's `declare-legal-entity` action, that value pre-fills here. You confirm, override, or refine the sub-vertical.

The action emits `IndustrySelected` and auto-completes on first emit.

## Action 2 — `triage-catalog`

The decision-engine loads the catalog filtered to your selected industry + sub_vertical. Each entry is a canonical process definition: name, description, typical inputs, typical outputs, escalation triggers.

For each catalog entry, you choose **one of three triage outcomes**:

- **Applies** — adopt as-is. The process inherits the canonical workflow definition; HME tracks it in Stage 6 as a known org workflow.
- **Doesn't Apply** — mark irrelevant. The platform skips this process; no HME workflow created.
- **Modify** — partially relevant. **The entry forks into Stage 6** as a starting point for org-specific codification. The operator-modifications happen in Stage 6, not here.

The chat affordance is `multiple_choice` per entry. Each triage emits `IndustryProcessTriaged` with a payload `{ catalog_entry_id, outcome }`. The action auto-completes when **every catalog entry has been triaged** — the manifest expresses this as `min_count_predicate: all_catalog_entries`.

The typical catalog size per (industry, sub_vertical) is 30-40 entries. Triaging takes 10-15 minutes for an operator who knows their operation; longer for new founders still discovering what their operator actually does.

## The activation gate

`GET {decision_engine_base}/v1/operators/{operator_id}/industry-process-triage` with predicate:

```
$.uncategorized_count == 0
```

The gate flips when every catalog entry has a triage outcome attached. **The required uncategorized_count value is `0`.**

## Events emitted

- `StageStarted`
- `IndustrySelected` (fires once)
- `IndustryProcessTriaged` (fires per entry)
- `StageCompleted`

## What unlocks at completion

Stage 5 contributes to **`tier_3_recommend`** — partially. The full tier closes after Stage 6 also completes. The `org-processes` nav circle illuminates after Stage 6.

## Streak eligibility

Stage 5 is **streak-eligible**. The catalog refreshes occasionally (new industry templates, updated sub-vertical entries), and operators are nudged to re-triage when new entries appear. Sustained re-triage is rewarded as a streak. The badge slug is `industry-mapped`.

## Predicted outcomes

Fallback predicted influence is **$9,500**. The PPIM signature highlights the structural value: **avg 12-30 hours of consulting equivalent** saved by triaging a curated catalog instead of running fresh org-process discovery.

## What you can't do

You cannot advance to Stage 6 with un-triaged catalog entries. The gate predicate `uncategorized_count == 0` is strict. If you encounter an entry you don't recognize, the orchestrator offers a "Skip with reason" affordance that records the entry as `outcome: deferred` with an operator-supplied note — that still counts as categorized for the gate.

## How Modify routes forward

The **Modify** outcome is the structural bridge to Stage 6 (Org Processes). When you mark an entry as Modify, the platform forks the canonical workflow definition into a per-operator draft and queues it for review in Stage 6. The orchestrator preserves the operator's note about *why* it needs modification, so Stage 6 has context for the codification.
