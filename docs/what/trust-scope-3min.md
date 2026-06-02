# What you'll do in Stage 0 — Trust & Scope Anchor (3-minute walkthrough)

Stage 0 is the first stage of onboarding and is always open as the entry point. It consists of **four actions, executed in this exact order**:

1. `declare-legal-entity`
2. `select-jurisdictions`
3. `acknowledge-axioms`
4. `sign-scope-contract`

You will complete each one inside the chat orchestrator. The owning engine is the **user-access-engine (UAE)**; the secondary engine is the **decision-engine** (it owns the axiom-acknowledgement table).

## Action 1 — `declare-legal-entity`

You name the legal entity, the jurisdiction(s) of incorporation, and any regulated frameworks that apply (HIPAA / GDPR / FINRA / etc.). The chat affordance is an `inline_form` (per the manifest's `chat_orchestration.affordance_resolution`). On submit, the orchestrator emits a `ScopeIdentityDeclared` event. The action auto-completes when UAE writes a non-null `legal_entity_record` for your operator.

## Action 2 — `select-jurisdictions`

You pick the jurisdictions you operate in. This is **not the same as where you're incorporated** — it's where you serve customers, where data may reside, and which regulator footprints apply. Stage 0 uses this list to scope every later compliance check and every data-residency choice. The action auto-completes on the `ScopeJurisdictionsSelected` event.

## Action 3 — `acknowledge-axioms`

You open the Gigaton **Axiom Registry** — 20 inviolable rules the platform enforces — and walk through them one at a time. For each axiom in scope you click **Acknowledge**; for any that conflict with your context, you click **Flag conflict** and write a one-line reason. The chat affordance is `multiple_choice` (button group inside the chat bubble). The action auto-completes only when:

- Every CRIT-severity axiom has an acknowledgement row, **and**
- Every MAJ-severity axiom has an acknowledgement row.

The activation gate predicate is `min_count_per_severity: { CRIT: all, MAJ: all }`. Lower-severity axioms (MIN, INFO) are recommended but not required to advance.

The education reference for this action is `/docs/axiom-registry`. If you want the long version of *why* an axiom exists before acknowledging it, that's where to look.

## Action 4 — `sign-scope-contract`

The final action collapses everything into a cryptographic acknowledgement: a signed copy stored in your operator namespace that says "the declarations above are accurate, and the operator agrees to operate within the acknowledged axioms." The chat affordance is `free_text` (you type your full name as confirmation). The action auto-completes on the `ScopeContractSigned` event.

## How the stage closes

The Stage 0 **activation gate** is `GET {uae_base}/v1/operators/{operator_id}/scope-contract`, with the JSON predicate `$.signed_at is_not_null`. When all four actions are done, that endpoint returns a non-null `signed_at`, the gate flips, and the stage advances to Stage 1.

On completion the stage emits `StageCompleted` and **partially unlocks `tier_1_data`** — the second half closes when Stage 1 (Sources) completes. You'll see the `chat` and (after Stage 1) the `sources` and `dashboard` nav circles illuminate.

## What you can't do

A per-operator `workflow_overlays` JSONB **cannot** remove Stage 0 from the sequence. It is listed in `overlay_schema.inviolable_stage_ids` alongside Stage 9. Any overlay that tries to `hide: ['stage-0-trust-scope']` is rejected by the resolver at request time.

## Predicted outcomes

The PPIM signature for Stage 0 predicts approximately **$4,500 in influence** (avg $12k compliance retrofit cost avoided × probability of incident). You'll see this number, and your real-time predicted-influence-to-date, in the chat side panel.
