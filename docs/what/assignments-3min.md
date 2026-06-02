# What you'll do in Stage 7 — Human-assigned + Automated Processes (3-minute walkthrough)

Stage 7 is owned by the **human-management-engine (HME)**. Secondary engine is **decision-engine** (it scores automation candidates). Stage 7 consists of **two actions**:

1. `assign-human-owners`
2. `score-automation-candidates`

## Action 1 — `assign-human-owners`

You **drag-and-drop your Stage 2 people onto Stage 6 workflows**. That's the verbatim UX description from the manifest. The chat surface renders a workflow-on-the-left, people-on-the-right layout with drag-and-drop affordance. Multiple owners per workflow are allowed — many real workflows are co-owned.

Each assignment emits `InitiativeOwnerAssigned`. The action auto-completes when every human-eligible workflow has at least one owner — the manifest expresses this as `min_count_predicate: all_human_eligible_initiatives`.

"Human-eligible" means the workflow has not yet been queued or approved as an automation candidate. The two paths are mutually exclusive at the workflow level: a workflow is either human-owned OR automation-scored, not both. This is the structural reason the activation gate is `unassigned_initiative_count == 0` (the unassigned count drops as workflows route to either path).

**True**: a single workflow may have multiple human owners assigned. Co-ownership is common for cross-functional work.

## Action 2 — `score-automation-candidates`

For each workflow that hasn't been human-owner-assigned, the decision-engine's automation scorer runs. The scorer produces a per-workflow automation-likelihood score on three dimensions:

- **Repetitiveness** — how often the workflow runs (high repetitiveness → strong automation candidate)
- **Determinism** — how rule-driven the workflow is (high determinism → strong automation candidate)
- **Risk profile** — what's the blast radius if automation gets it wrong (low blast radius → strong automation candidate)

For each scored candidate, **you do one of three things**: **Approve** (queue for automation in tier_5_live), **Reject** (mark not-a-real-automation-candidate; routes back to human ownership), or **Queue for human** (acknowledge automation potential but assign a human owner for now).

Each scoring action emits `AutomationCandidateScored`. The action auto-completes when every automation-eligible workflow has a scoring outcome — `min_count_predicate: all_automation_eligible_initiatives`.

The chat affordance is `multiple_choice` per candidate.

## The activation gate

`GET {hme_base}/v1/operators/{operator_id}/assignment-readiness` with predicate:

```
$.unassigned_initiative_count == 0
```

**The required value is `0`** — every codified workflow has been routed to either human ownership or automation scoring (with an explicit operator outcome).

## Events emitted

- `StageStarted`
- `InitiativeOwnerAssigned` (fires per assignment)
- `AutomationCandidateScored` (fires per candidate scoring)
- `StageCompleted`

## What unlocks at completion

Stage 7 **partially opens `tier_4_costs`** — the second half closes when Stage 8 (Tech Stack + Costs) completes. The full `Influence vs Cost` dashboard turns on after Stage 8. The `assignments` nav circle illuminates.

## Streak eligibility

Stage 7 is **not streak-eligible**. Assignments are made once per workflow and revised when the org changes. The badge slug is `ownership-clear`.

## Predicted outcomes

Fallback predicted influence is **$25,000**. The PPIM signature quantifies the recovered value as **avg $40k+/yr work-falls-through-cracks recovered** — the structural value of closing the ownership loop.

## Predictability is HIGH

Stage 7 is HIGH predictability. The operator's choices are unambiguous (who owns this; should this be automated), and the downstream consequences are deterministic (the owner runs the workflow; or the engine does).

## What you can't do

You cannot advance to Stage 8 with any workflow left unassigned. The gate is strict — `unassigned_initiative_count` must be exactly `0`. If you encounter a workflow you're genuinely unsure how to route, the orchestrator offers "Queue for human review" as a safe fallback — the workflow is assigned to you (the operator) as default owner, and you can revisit later.
