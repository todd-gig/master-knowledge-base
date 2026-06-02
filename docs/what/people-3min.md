# What you'll do in Stage 2 — People & Human Data (3-minute walkthrough)

Stage 2 is owned by the **persona-engine**. Secondary engines are **intelligence-silo** (sources the proposals) and **human-management-engine** (binds people to org workflows in later stages). Stage 2 consists of **three actions**:

1. `review-proposed-people`
2. `capture-initial-intent`
3. `classify-internal-external`

The chat orchestrator surfaces them in that order. You can interleave (review three people, capture three intents, classify three people, repeat) — the activation gate only cares that all three actions reach min_count 3.

## Action 1 — `review-proposed-people`

Before the stage opens, intelligence-silo scans your Stage 1 sources (meeting notes, email signatures, shared documents, contracts) and proposes the people who appear most often. The chat affordance is `proposed_review_cards` — a carousel of cards, each one a candidate person with auto-extracted attributes (name, role hint, frequency of appearance, source examples). For each card you choose **Accept**, **Edit**, or **Reject**.

Each Accept emits `PersonaCreated`. The action auto-completes after `min_count: 3` PersonaCreated events. The orchestrator's opening message tells you what to expect: "I've scanned your sources and pulled out the people who appear most often. Let's confirm who they are and what they do for your operator."

## Action 2 — `capture-initial-intent`

For each accepted person you write a single sentence answering: **what is this relationship FOR?** Examples:

- "Anna is our primary venue contact in Tulum; we book her property monthly."
- "Carlos is the contractor who handles all maintenance escalations within 24 hours."
- "Sandra is our state regulator; we file quarterly compliance reports to her office."

The chat affordance is `free_text` — a conversational input. The persona-engine parses the sentence into BFT scoring features (relationship type, cadence implied, escalation pattern, asymmetric power dynamic, etc.). That parsing drives the BFT snapshot.

Each captured intent emits `PersonaIntentCaptured`. The action auto-completes after `min_count: 3`.

The one-sentence-per-person constraint is intentional. Longer descriptions push the operator into writing essays; shorter ones produce ambiguous parses. One sentence is the sweet spot, and the orchestrator nudges if the operator skips this step.

## Action 3 — `classify-internal-external`

For each person, you classify them as one of:

- **internal** — on the operator's team
- **customer** — buys from the operator
- **vendor** — sells to the operator
- **regulator** — has authority over the operator's compliance
- **prospect** — potential customer, not yet converted

The chat affordance is `multiple_choice` (button group in chat). Each classification emits `PersonaClassified`. The action auto-completes after `min_count: 3`.

**Each classification routes differently downstream.** An internal person becomes eligible for Stage 7 (Assignments) workflow ownership. A customer flows into Stage 3's ICP segment computation. A vendor flows into Stage 8's tech-stack inventory pre-fill. A regulator triggers extra compliance routing in every later send.

## The activation gate

`GET {persona_base}/v1/operators/{operator_id}/persona-count` with predicate:

```
all_of:
  - $.human_persona_count >= 3
  - $.bft_snapshots_available_count >= 3
```

A BFT snapshot becomes available once a person has been created AND intent captured AND classified. The three actions chain into BFT availability per person.

## Events emitted

- `StageStarted` — fires when the stage opens.
- `PersonaCreated` — fires per accepted person.
- `PersonaIntentCaptured` — fires per intent sentence.
- `PersonaClassified` — fires per classification.
- `StageCompleted` — fires when the activation gate flips.

## What unlocks at completion

Stage 2 **partially opens `tier_2_personalized`** — the second half closes when Stage 3 (Brand & Customer Lens) completes. Specifically:

- `gigaton.communication.personalized_compose` turns on after Stage 3 (it depends on both BFT snapshots and brand voice variables).
- `gigaton.persona.read_bft_snapshot` turns on now.

The `people` and `brand` nav circles illuminate after Stage 3.

## Streak eligibility

Stage 2 is **streak-eligible**. Sustained PersonaCreated cadence (new people added regularly) is rewarded — operators with a living people graph see compounding personalization quality across every later stage.

## Predicted outcomes

Fallback predicted influence is **$11,000**. PPEME's live prediction may be higher for operators with larger contact surfaces.

## Predictability is MEDIUM — and why that matters

The PPIM signature for Stage 2 lists **predictability: MEDIUM (depends on BFT snapshot quality)**. Other stages are HIGH. The MEDIUM tag is honest: the value of Stage 2 depends on how good the BFT snapshots are, which depends on how thoughtful the one-sentence intents are, which depends on the operator. Skipping the intent capture or writing vague intents ("Carlos is helpful") produces low-quality snapshots that under-deliver on the $2-5k/month payoff.
