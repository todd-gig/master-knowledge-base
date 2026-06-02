# What you'll do in Stage 3 — Brand & Customer Lens (3-minute walkthrough)

Stage 3 is owned by the **persona-engine**. It consists of **three actions**, completed in the chat orchestrator:

1. `fill-brand-voice-variables`
2. `declare-icp-segments`
3. `define-lifecycle-stages`

## Action 1 — `fill-brand-voice-variables`

You fill **six brand voice variables** seeded from the `brand_voice` tag in the Variable Registry. The six are:

- **tone** — warm/professional/playful/etc.
- **formality** — terse/balanced/elaborate
- **languages** — primary and supported languages
- **archetypes** — Hero / Caregiver / Explorer / etc. (operator's voice persona)
- **taboos** — words, topics, or phrasing the brand never uses
- **response cadence** — expected SLA from first contact to first response

The chat affordance is `inline_form`. The form is **pre-populated** from your Stage 1 sources where possible — if the orchestrator finds an existing brand guide in your bundle, it pre-fills the form from that doc. You confirm, edit, or override.

Each filled variable emits `VariableInstanceFilled` (tagged `brand_voice`). The action auto-completes after `min_count: 6` — all six brand_voice category seed variables.

The variables are bound to the persona-engine's **Variable Registry** under the `brand_voice` category. That binding is what every later platform action that produces voiced output reads from.

## Action 2 — `declare-icp-segments`

You declare your **Ideal Customer Profile segments**. At least one is required; more is better. The chat affordance is `inline_form` per segment. Each segment captures:

- segment name
- attributes (industry, sub-vertical, geo, size, lifecycle position, buying triggers)
- positive examples (people from your Stage 2 graph classified as customer)
- negative examples (people who explicitly do not fit)

ICP segment data is stored in **persona-engine's `org_persona.icp_attributes` JSONB**. That JSONB is the target distribution Penrose scores against in Stage 4.

Each segment emits `ICPSegmentDeclared`. The action auto-completes after `min_count: 1`.

The PPIM signature is honest about why one is the floor and more is better: a single ICP segment lets the platform start optimizing; multiple segments let it tune per-segment messaging, lifecycle, and economics. Operators with one segment hit a soft ceiling on personalization that operators with three+ segments don't.

## Action 3 — `define-lifecycle-stages`

You define the customer lifecycle stages. The platform pre-populates the **default sequence**:

```
prospect → first-contact → qualified → converted → renewed → champion
```

You confirm, edit, reorder, or add/remove stages to match your operator's actual model. Many operators use the defaults; some collapse them (prospect → converted → renewed), some expand them (prospect → SQL → demo → trial → converted → renewed → champion).

The chat affordance is `inline_form`. The action emits `CustomerLifecycleDefined` and auto-completes on first emit.

## The activation gate

`GET {persona_base}/v1/operators/{operator_id}/brand-readiness` with predicate:

```
all_of:
  - $.brand_voice_variables_filled >= 6
  - $.icp_segments_defined >= 1
```

Both must hold. CustomerLifecycleDefined doesn't appear in the gate predicate because it's not a hard prerequisite — the platform uses the default lifecycle if the operator hasn't customized.

## Events emitted

- `StageStarted`
- `VariableInstanceFilled` (tagged `brand_voice`, fires per variable)
- `ICPSegmentDeclared` (fires per segment)
- `CustomerLifecycleDefined` (fires once)
- `StageCompleted`

## What unlocks at completion

Stage 3 **closes `tier_2_personalized`** (the tier Stage 2 partially opened). Specifically:

- `gigaton.communication.personalized_compose` — drafts in your voice, targeted at your declared ICP segments. This is the second-half close.
- `gigaton.persona.read_bft_snapshot` was already on after Stage 2; it remains on.

The `brand` nav circle illuminates after Stage 3.

## Streak eligibility

Stage 3 is **not streak-eligible**. Brand voice and ICP are not properties you update daily — they're declared, then refined occasionally. The badge slug is `brand-aligned`.

## Predicted outcomes

Fallback predicted influence is **$14,500**. The PPIM signature explicitly calls this stage **foundational for revenue forecasting via the Experience Engineering Equation** — the framework Stage 4 onward uses to project revenue from interaction-quality lift.

## What you can't do

You cannot complete Stage 3 with zero declared ICPs. The platform will not let the gate flip with `icp_segments_defined == 0`. This is intentional — the manifest's `predictability: HIGH after ICP defined` signature explicitly conditions HIGH-predictability decision-making on ICP existence.
