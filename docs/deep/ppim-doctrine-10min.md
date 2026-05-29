# PPIM Doctrine — Deep Dive (10-minute read)

This deep dive explains the PPIM doctrine that Stage 3 makes operational: what the acronym means in full, how brand voice and ICP become Penrose-scoreable target distributions, how the Experience Engineering Equation projects revenue from interaction-quality lift, and the edge cases that determine whether an operator's PPIM signature actually compounds. It assumes you have read the `why_1min` and `what_3min` documents for Stage 3.

---

## 1. The full PPIM expansion

PPIM expands to: **"predictably profitable interaction management of a gigaton engineered brand experience."**

Each word is load-bearing:

- **predictably** — outcomes have to be projectable, not just attainable. The Penrose Falsification Scoreboard exists to enforce predictability: a recommendation that produces a positive outcome by accident is treated as unsupported until the projection model can be falsified against it.
- **profitable** — outcomes have to be net-positive in dollar terms. Stage 8 (Tech Stack + Costs) backfills the cost side so "profitable" is a real measurement, not a claim.
- **interaction management** — the unit of work is the interaction (person ↔ operator). Stage 2 establishes the people; Stage 3 establishes the voice and target.
- **gigaton engineered brand experience** — the brand experience is the engineered output. "Gigaton" is the scale signal: the platform engineers for compound effect across the operator's entire interaction surface, not per-interaction polish.

The doctrine names every later platform behavior. A feature that doesn't trace back to PPIM is, by definition, off-doctrine.

## 2. Brand voice variables as Variable Registry instances

The six brand voice variables — **tone, formality, languages, archetypes, taboos, response cadence** — are stored as instances in the persona-engine's **Variable Registry**, all tagged `brand_voice`.

The Variable Registry is the platform's first-principles substrate for declared values. Each variable carries:

- a canonical name (e.g., `brand_voice.tone`)
- a value (operator-supplied or inferred)
- a confidence score
- a bounded range (INTEL-3 doctrine — every value is a seed within bounds, not a target)
- a provenance pointer (which source doc or operator input filled this)

Downstream platform actions read from the Variable Registry, not from any per-stage cache. That decoupling is why the same brand voice powers every later capability: drafted communications in Stage 5-7, customer-facing copy in Stage 9, all referenced documentation in chat.

## 3. ICP as `org_persona.icp_attributes` JSONB

ICP segments are stored in **persona-engine's `org_persona.icp_attributes` JSONB**. The JSONB shape, simplified:

```
{
  "segments": [
    {
      "segment_id": "...",
      "name": "Boutique hospitality 5-25 rooms LATAM",
      "attributes": {
        "industry": "hospitality",
        "sub_vertical": "boutique",
        "size_band": "5-25 rooms",
        "geo": ["MX", "CR", "PA"],
        "lifecycle_focus": ["first-contact", "qualified"],
        "buying_triggers": ["...", "..."]
      },
      "positive_examples_persona_ids": ["...", "..."],
      "negative_examples_persona_ids": ["...", "..."]
    },
    ...
  ]
}
```

JSONB instead of normalized tables is intentional: ICP segment shape varies per operator. A consultancy's ICP looks nothing like a SaaS company's ICP. JSONB lets each operator's schema evolve without migration.

## 4. ICP becomes Penrose's target distribution

Penrose Falsification Scoreboard (covered in depth in `/docs/deep/penrose-falsification-10min.md`) requires a **target distribution** to score recommendations against. ICP segments are that target distribution.

The mechanism: each Stage 4 recommendation is projected to move the operator's north star metric. Penrose decomposes the projection by ICP segment — "this action lifts conversion in Segment A by X, has no effect on Segment B." A recommendation that lifts the north star by accidentally over-indexing on a non-ICP segment is flagged as low-quality, even though the north-star number went up.

Without ICP, Penrose treats every persona as equally weighted, and the falsification signal collapses to "did the number go up?" which is not a falsifiable claim.

## 5. The Experience Engineering Equation

The PPIM signature for Stage 3 explicitly calls it "foundational for revenue forecasting via the **Experience Engineering Equation**." The equation is the framework the platform uses to project revenue from interaction-quality lift.

In schematic form:

```
ΔRevenue = Σ_segments  ( population_in_segment
                       × interaction_volume_per_member
                       × Δquality_per_interaction
                       × monetization_per_quality_unit )
```

Each term is supplied by a specific stage:

- `population_in_segment` — Stage 3 (ICP segments)
- `interaction_volume_per_member` — Stage 7 (assignments, automation throughput)
- `Δquality_per_interaction` — Stage 2 (BFT-personalization lift) + Stage 3 (brand-voice lift)
- `monetization_per_quality_unit` — Stage 8 (unit economics)

Without Stage 3, two of the four terms are undefined and the equation is unprojectable. That's the structural reason Stage 3 is "foundational for revenue forecasting."

## 6. Why brand voice is six variables and not five or seven

The six variables — tone, formality, languages, archetypes, taboos, response cadence — cover the **necessary-and-sufficient surface** for personalized compose. Each addresses a distinct failure mode:

- Without **tone**, generated copy reads like a press release.
- Without **formality**, copy mismatches the recipient's expectation (a casual "hey" to a regulator is a problem).
- Without **languages**, the platform may answer in the wrong language for the recipient's locale.
- Without **archetypes**, copy lacks voice consistency across communications.
- Without **taboos**, the platform may use phrasing the brand has explicitly disowned.
- Without **response cadence**, the platform can't gate when to draft vs queue.

A seventh variable (e.g., "humor level") was considered and dropped — it correlated too tightly with archetype + tone to be independent. A fifth (e.g., dropping languages) underspecifies multilingual operators. Six is the empirical floor for non-degenerate personalized compose.

The Stage 3 activation gate requires all six. Operators can extend the brand_voice category with operator-specific variables (color palette, prohibited claims, signature sign-offs), but the six are non-negotiable.

## 7. Lifecycle stages — defaults and customizations

The default lifecycle is:

```
prospect → first-contact → qualified → converted → renewed → champion
```

It's a reasonable starting point for most B2B operators. Many operators stay on the defaults; some customize:

- **Simpler operators** (small consumer brand, single product) collapse to `prospect → converted → renewed`.
- **Complex enterprise operators** expand to `prospect → SQL → demo → trial → POC → converted → expanded → renewed → champion`.
- **Subscription operators** add explicit `at_risk` and `churned` stages between `renewed` and `champion` to track recovery flows.

The lifecycle drives:

- HME workflow routing (Stage 6-7) — a "first-contact" person is routed to outreach workflows; a "converted" person is routed to delivery workflows.
- Penrose grading — Stage 4 north-star and supporting metrics often have per-lifecycle-stage variants (conversion rate, retention rate, expansion rate).
- Stage 9 live-mode automation — the auto-execute classes are constrained per lifecycle stage (the platform may auto-respond to prospects but not auto-renew customers without human confirmation).

## 8. Brand dimension — coherence + voice integrity

The PPIM signature lists Stage 3's brand dimension as **coherence + voice integrity**. This is what readers (recipients of the operator's communications) experience:

- **Coherence** — the operator sounds like themselves across channels. A Slack message, an email, a chat reply, and a marketing landing page all share the brand voice.
- **Voice integrity** — the operator never says things they would not say in person. Taboos are honored. Archetype is consistent.

Coherence + voice integrity compound with Stage 2's responsiveness + relevance. The combined effect is what high-quality interaction management feels like from outside the operator. Operators with strong PPIM signatures across Stages 2-3 are typically perceived as "professional, fast, and on-message" by their counterparties.

## 9. Predictability — HIGH after ICP defined

Stage 3's PPIM signature lists **predictability: HIGH after ICP defined**. The conditional matters. Before Stage 3 completes, predictability is MEDIUM (Stage 2 quality). After Stage 3 completes, predictability is HIGH because:

- ICP segments give Penrose a falsifiable target distribution.
- Brand voice variables give the Variable Registry the inputs every later compose action depends on.
- Lifecycle stages give HME a routing key per person.

The three together close the predictability loop. Subsequent stages (4 onward) can produce graded recommendations because Stage 3 supplied the grading substrate.

## 10. Edge cases

- **Operator has multiple brands.** Supported via multiple `org_persona` records per operator. Each brand carries its own brand_voice variables and ICP segments. Stage 3 then iterates per brand. The chat orchestrator surfaces a brand picker before the actions open.
- **Operator's brand voice changes over time.** The Variable Registry supports versioning per variable. A new value supersedes the prior; the prior is retained for audit. Communications drafted under the prior version remain correct as-of-the-time-of-draft.
- **Operator has no idea what their archetype is.** The orchestrator offers a guided selector: "look at three sample messages your operator has sent — which one feels most you?" The selection seeds the archetype variable; the operator can refine later.
- **Operator declares an ICP segment with zero positive examples.** Allowed but warned. The chat surface shows "this segment has no positive examples — Penrose grading will be weaker. Want to mark some Stage 2 people as positive examples?"
- **Operator wants to update ICP after Stage 4+ completes.** Supported; ICP updates fire `ICPSegmentUpdated`. Penrose re-runs grading for any pending recommendations. The decision-engine flags any prior-graded recommendation whose grade would change under the new ICP, so the operator can re-review.

## 11. The capability-tier handoff

Stage 3 closes `tier_2_personalized`. The tier grants:

- `gigaton.communication.personalized_compose` — drafts in your voice, targeted at your ICP.
- `gigaton.persona.read_bft_snapshot` — already on from Stage 2; remains on.

`tier_3_recommend` requires Stages 4, 5, 6. None of those can grade their outputs without the brand-voice + ICP substrate Stage 3 supplies. The dependency is one-directional and structural.

## 12. The PPIM signature, restated

- **interaction**: every comm now in operator's voice to defined ICP
- **economics**: foundational for revenue forecasting via Experience Engineering Equation
- **predictability**: HIGH after ICP defined
- **brand_dimension**: coherence + voice integrity

Stage 3 is the entry point of the PPIM doctrine becoming operational. Every later stage compounds against the substrate Stage 3 supplies: voice variables, ICP segments, lifecycle stages. The downstream economics — projected via the Experience Engineering Equation — depend on Stage 3's quality. Operators who skim Stage 3 typically under-deliver on Stage 4-8 economics; operators who invest in it see compounding returns.
