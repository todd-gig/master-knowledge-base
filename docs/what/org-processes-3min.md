# What you'll do in Stage 6 — Organization Processes (3-minute walkthrough)

Stage 6 is owned by the **human-management-engine (HME)**. Secondary engines are **intelligence-silo** (source extraction) and **decision-engine** (workflow-type tagging). Stage 6 consists of **two actions**:

1. `review-proposed-workflows`
2. `define-escalation-paths`

## Action 1 — `review-proposed-workflows`

Before the stage opens, intelligence-silo + HME jointly extract candidate workflows from two sources:

- **Stage 1 sources** — your canonical documentation bundle. Process descriptions in SOPs, README files, internal wiki pages.
- **Meeting transcripts** — if you connected meeting-transcript sources (Zoom, Granola, etc.) during Stage 1.

The platform then surfaces the candidate workflows in chat as `proposed_review_cards` (carousel of cards, each with Accept / Edit / Reject). Each card carries the proposed workflow's:

- name
- description
- inputs and outputs (extracted from the source)
- proposed step sequence
- proposed escalation triggers
- source citation (which document or transcript chunk this was extracted from)

For each card you choose Accept (adopt as-is), Edit (modify before adoption), or Reject (mark not-a-real-workflow). Each Accept emits `InitiativeIdentified` with `workflow_type: org_process`. The action auto-completes after **`min_count: 10`** such events.

The 10-workflow floor is intentional. Below 10, the Stage 7 assignment surface is sparse; above 10, HME has enough work to populate the assignment + automation-candidate scoring with reasonable signal.

## Action 2 — `define-escalation-paths`

You define **at least three escalation paths**. An escalation path captures: when does a workflow escalate to a human, and to whom. Examples:

- "Any guest refund request > $200 escalates to Bella."
- "Any vendor invoice > $5,000 escalates to Todd."
- "Any regulator inquiry escalates to legal counsel within 1 business hour."

The chat affordance is `confirmation_only` per escalation path (the orchestrator surfaces a panel of HME-proposed escalations based on the codified workflows; the operator confirms, edits, or adds new ones). Each definition emits `EscalationPathDefined`. The action **auto-completes after 3 EscalationPathDefined events** (`min_count: 3`).

Three is the floor because most operators have at least three escalation classes (financial, customer, compliance) — anything fewer typically signals that the operator hasn't thought through their actual escalation policy.

## The activation gate

`GET {hme_base}/v1/operators/{operator_id}/org-process-readiness` with predicate:

```
$.org_initiatives_with_workflow_type >= 10
```

Note the predicate gates on `InitiativeIdentified` count — not on EscalationPathDefined count. Escalation paths are required to satisfy the action's auto-complete predicate, but the stage-level gate is the workflow count.

## Events emitted

- `StageStarted`
- `InitiativeIdentified` (fires per accepted workflow)
- `EscalationPathDefined` (fires per defined escalation)
- `StageCompleted`

## What unlocks at completion

Stage 6 closes **`tier_3_recommend`** (the tier Stage 4 and Stage 5 partially opened). The full draft-recommendations capability is now available, grounded in operator-specific workflows. The `org-processes` nav circle illuminates.

## Streak eligibility

Stage 6 is **streak-eligible**. Operators who continue extracting org processes from new documents or transcripts (as their org evolves) are rewarded for sustained cadence. The badge slug is `processes-codified`.

## Predicted outcomes

Fallback predicted influence is **$16,500**. The PPIM signature claims Stage 6 is **foundational for Stage 7 automation candidates** — HME's automation-likelihood scorer in Stage 7 reads the codified workflows from Stage 6.

## Predictability is MEDIUM — and why

The PPIM signature lists Stage 6 as **predictability: MEDIUM (depends on source quality)**. Same honest tag as Stage 2. The platform's extracted workflows are only as good as the source documentation and transcripts they were extracted from:

- Operators with comprehensive, current SOPs see high-quality proposed workflows.
- Operators with stale or thin documentation see weaker proposals and must do more Edit work.

The orchestrator handles weak proposals gracefully: low-confidence extractions are flagged with "I'm not sure about this one — review carefully before accepting."

## What you can't do

You cannot advance to Stage 7 with fewer than 10 codified workflows. The orchestrator nudges if the operator stalls below 10: "you can add a workflow directly from this chat, or connect a meeting-transcript source so I can extract more candidates."
