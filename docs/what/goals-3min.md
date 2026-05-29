# What you'll do in Stage 4 — Goals, KPIs & Constraints (3-minute walkthrough)

Stage 4 is owned by the **decision-engine**. The secondary engine is **persona-engine** (it supplies brand voice + ICP from Stage 3 as inputs to grading). Stage 4 consists of **three actions**:

1. `declare-north-star`
2. `pick-supporting-metrics`
3. `register-constraints`

## Action 1 — `declare-north-star`

You declare **one metric** that, if it goes up, your operator wins. Valid example north star metrics include **revenue, retention, NPS — your call.** The platform doesn't constrain the choice; it constrains the shape (single metric, measurable, attributable to platform actions).

The chat affordance is `inline_form`. The form asks: name, units, current value (optional, for baseline), target value (optional, for projection horizon). On submit, `NorthStarDeclared` fires. The action auto-completes on first emit.

A common new-operator mistake is declaring a vanity metric (e.g., "social-media followers") with no real business reflection. The orchestrator nudges back: "this metric — if it doubled, would your operator be measurably better off?" Operators are encouraged to pick a metric that connects directly to operator outcomes.

## Action 2 — `pick-supporting-metrics`

You pick **at least 3 supporting metrics**. These are **counterweights against gaming the north star** — that is the verbatim purpose-statement the manifest uses. Penrose tracks all of them; a recommendation that lifts the north star at the cost of a supporting metric is graded as low-quality and surfaced to the operator with the trade-off explicit.

Examples:

- North star: weekly bookings revenue. Supporting metrics: average daily rate, occupancy rate, repeat-guest rate, refund rate.
- North star: monthly net-new ARR. Supporting metrics: gross retention, churn rate, sales-cycle length, CAC.
- North star: NPS. Supporting metrics: response rate, escalation-to-resolution time, repeat-customer rate.

The chat affordance is `inline_form` per metric. Each addition fires `SupportingMetricAdded`. The action auto-completes after `min_count: 3`.

## Action 3 — `register-constraints`

You register **at least one hard constraint** — something the platform must never do regardless of expected value. The manifest's stated examples: **never email opt-outs, never undercut floor price.** Constraints are inviolable within scope; they bind at the engine, not at human review.

The chat affordance is `inline_form` per constraint. Each constraint captures: name, predicate (the logical test the engine runs against any candidate action), domain (which engine + which decision class it applies to). On submit, `ConstraintRegistered` fires. The action auto-completes after `min_count: 1`.

The Decision Execution Engine treats constraints as **hard guardrails** — a candidate action that violates an acknowledged constraint is blocked at the engine, not surfaced to human review. This is the same treatment as a Stage 0 acknowledged axiom, scoped to this operator.

## The activation gate

`GET {decision_engine_base}/v1/operators/{operator_id}/targets-readiness` with predicate:

```
all_of:
  - $.north_star_defined == true
  - $.supporting_metrics_count >= 3
  - $.constraints_count >= 1
```

All three must hold.

## Events emitted

- `StageStarted`
- `NorthStarDeclared` (fires once)
- `SupportingMetricAdded` (fires per metric)
- `ConstraintRegistered` (fires per constraint)
- `StageCompleted`

## What unlocks at completion

Stage 4 unlocks **`tier_3_recommend`** — partially. Specifically:

- `gigaton.decision.draft_recommendations_read_only` — the decision-engine starts drafting recommendations for the operator to review, scored by Penrose against the declared targets and filtered by the registered constraints. Read-only means the operator reviews; the engine does not yet act.

The full `tier_3_recommend` closes after Stages 5 + 6. The `goals` nav circle illuminates.

## Streak eligibility

Stage 4 is **not streak-eligible**. Goals and constraints are declared once and revised occasionally — not a daily cadence. The badge slug is `goal-set`.

## Predicted outcomes

Fallback predicted influence is **$22,000**. The PPIM signature explicitly calls out: prevents misaligned automation, avg **$30k+/year risk avoided**. Misaligned automation is the silent killer of platform value — Stage 4 is the moment the operator pins the target so the platform doesn't optimize for the wrong thing.

## Predictability is HIGH

Unlike Stage 2's MEDIUM, Stage 4 is HIGH. The operator declared the target; the engine grades against it. There's no quality-of-input ambiguity to discount for.
