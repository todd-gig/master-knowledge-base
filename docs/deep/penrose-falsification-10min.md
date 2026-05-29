# Penrose Falsification Scoreboard — Deep Dive (10-minute read)

This deep dive covers the **Penrose Falsification Scoreboard** — the grading layer that scores every decision-engine recommendation against operator-declared targets, falsifies projections when reality disagrees, and updates the model. It assumes you've read the `why_1min` and `what_3min` documents for Stage 4.

---

## 1. What Penrose is

Penrose is the **falsification scoreboard** that sits between the decision-engine's recommendations and the operator's outcomes. Its full canonical name in the platform is the **Penrose Falsification Scoreboard**.

The name carries two structural commitments:

- **Penrose** — after Roger Penrose, whose work on falsifiability and conditional reasoning informs the model. Penrose treats projections as falsifiable claims, not predictions.
- **Falsification** — the engine looks for evidence that the projection was wrong, not evidence it was right. A projection that "succeeded" by accident (north star went up for unrelated reasons) is treated as unsupported until the projection mechanism can be falsified against it.
- **Scoreboard** — outcomes are tracked at the per-recommendation level, not at aggregate. Every recommendation has a Penrose score.

Penrose lives in the decision-engine and is loaded into every recommendation cycle.

## 2. What Penrose needs from Stage 4

Stage 4 supplies three classes of input to Penrose:

- **North star metric** — the single primary target.
- **Supporting metrics (≥3)** — counterweights against gaming the north star.
- **Constraints (≥1)** — hard guardrails enforced as inviolable.

Without all three, Penrose has no falsifiable target distribution and the decision-engine cannot grade its own recommendations. The Stage 4 activation gate enforces this by predicate.

## 3. The grading mechanism

Each candidate recommendation flows through this sequence:

1. **Projection** — the decision-engine projects the action's impact on the north star + each supporting metric, decomposed by ICP segment (from Stage 3).
2. **Constraint check** — every constraint predicate is evaluated against the action. A single violation blocks the recommendation; it never reaches surfacing.
3. **Penrose grading** — the projection is converted to a Penrose score. The score is a weighted aggregate of: expected north-star lift, expected impact on each supporting metric, confidence interval width, projection time horizon, and historical-falsification rate for this projection class.
4. **Surfacing** — recommendations above a per-operator threshold are surfaced; below-threshold recommendations are logged and dropped.

After the action is taken (or simulated in shadow mode), the **outcome attribution** loop runs:

5. **Outcome capture** — the actual movement of north star + supporting metrics is captured over the projection horizon.
6. **Falsification check** — Penrose compares actual to projected. If the projection was within the confidence interval, the projection mechanism gains weight; if outside, it loses weight.
7. **Drift signal** — when projection mechanisms systematically miss in the same direction, `drift_warning` or `drift_critical` fires. Stage 9's graduation gate uses `drift_critical_count == 0` as one of its four verification dimensions.

## 4. Why counterweights matter — gaming and how to prevent it

A decision-engine optimizing against a single metric will find the path of least resistance to that metric — and that path often runs through actions that hurt other dimensions. Examples:

- Optimize only for revenue → recommend aggressive upsells that hurt NPS.
- Optimize only for NPS → recommend over-generous refunds that hurt revenue.
- Optimize only for conversion → recommend lead-magnet tactics that hurt retention.

Penrose treats each supporting metric as a **constraint on the gradient**: a recommendation whose projection includes a degradation in any supporting metric is graded down. Three supporting metrics is the empirical floor — below three, gaming remains possible; at three, the operator-declared front becomes wide enough that gaming requires lifting all three simultaneously, which is structurally hard.

The verbatim purpose of supporting metrics per the manifest is **"counterweights against gaming the north star"** — Penrose enforces that purpose at the grading layer.

## 5. Constraints — hard guardrails, not soft preferences

Constraints are **hard guardrails**, not weighted preferences. A candidate action that violates a constraint is blocked at the engine. The block is independent of projected value: even an action with a $1M projected lift is blocked if it violates an acknowledged constraint.

The manifest's stated examples are illustrative of the kind of rule that belongs in a constraint:

- "never email opt-outs" — a hard rule against re-engaging recipients who have explicitly opted out. The projected value of re-engagement is irrelevant; the constraint is inviolable.
- "never undercut floor price" — a hard rule against discounts below a declared floor. The projected conversion lift is irrelevant; the floor is inviolable.

Constraints differ from preferences (which are weighted in the projection model). A preference like "we prefer Stripe over PayPal for payment routing" is not a constraint — it's a tie-breaker. A constraint is a hard "never."

Operators are encouraged to register constraints they would not want any human on their team to violate. If a human violation would trigger an escalation, the rule belongs in the constraint set.

## 6. North-star quality and the predictability tag

The Stage 4 PPIM signature lists predictability as HIGH. That tag depends on north-star quality. A well-chosen north star has three properties:

- **Measurable** — there is an unambiguous metric definition the platform can compute.
- **Attributable** — there is a credible causal path from platform actions to movement in this metric.
- **Aligned with operator outcomes** — moving this metric reflects the operator's intended success state, not a proxy.

Penrose's confidence intervals tighten when all three hold. Operators who pick vanity metrics (followers, page views) see wide confidence intervals on every projection — Penrose can't falsify or confirm because the attribution path is too noisy.

The orchestrator nudges operators toward attributable metrics; for the rare operator who insists on a vanity north star, Penrose still works but predictability degrades to MEDIUM until the metric is replaced.

## 7. The Decision Execution Engine handoff

Constraints are enforced by the **Decision Execution Engine** specifically — the layer that decides whether to surface, queue, or auto-execute a recommendation. The DEE runs the constraint predicates at decision time, independent of the original projection.

This separation matters because the DEE's constraint check happens at the moment of execution, not at the moment of projection. An action that was projection-safe but becomes constraint-violating in the meantime (e.g., the recipient opts out between projection and execution) is still blocked.

## 8. Misaligned automation — the $30k+/yr risk

The PPIM signature quantifies Stage 4's economic value as **prevents misaligned automation (avg $30k+/yr risk avoided)**. Misaligned automation is the silent killer of platform value:

- A platform that optimizes against the wrong north star produces actions that don't move the real one.
- A platform that lacks supporting-metric counterweights produces actions that game the declared metric.
- A platform that lacks constraints produces actions that cross lines the operator would never cross.

Each pattern degrades platform value differently — opportunity cost, recovery cost, active damage. Across operators the average is $30k+/year. Stage 4 prevents it by structuring the engine's target before automation is enabled.

## 9. Why persona-engine is the secondary engine

Penrose's grading is **per-ICP-segment**, not aggregate. A recommendation that lifts the north star by 5% is graded differently if the lift is concentrated in Segment A (an ICP) vs Segment B (a non-ICP). Per-segment decomposition requires the ICP segments declared in Stage 3 + the BFT-classified people from Stage 2 — both supplied by the **persona-engine**.

The manifest lists `secondary_engines: [persona-engine]` for that reason. decision-engine owns Stage 4's actions and activation gate; persona-engine supplies the grading substrate. **True**: persona-engine is a secondary engine on Stage 4.

## 10. Edge cases

- **Operator wants to update the north star after Stage 4 completes.** Supported via `NorthStarUpdated`. Penrose re-grades any pending recommendations against the new metric. Historical projections retain their as-of-the-time grading for audit; the active grade refreshes.
- **Operator wants to retire a constraint.** Supported via `ConstraintRetired`. Constraints retain their history; the engine stops enforcing the retired constraint going forward. Recommendations that were blocked under the retired constraint are NOT automatically re-evaluated — the operator must explicitly request re-evaluation.
- **Supporting metric goes stale** (instrumentation breaks). Penrose flags the metric as `stale: true`; the grading model widens confidence intervals for projections that depended on the metric, and a `drift_warning` fires if staleness persists more than 7 days.
- **Two constraints conflict** (constraint A says "never email opt-outs" and constraint B says "always confirm receipt by email" — and an opt-out recipient also requires receipt confirmation). The engine emits a `ConstraintConflict` event for human review. Pending recommendations in the conflict domain are paused.

## 11. Stage 4's role in the tier ladder

Stage 4 partially opens `tier_3_recommend`. The full tier requires Stages 5 + 6 also complete. The split exists because Stage 4 supplies the *grading* substrate; Stages 5 + 6 supply the *content* substrate (industry processes + org processes). Both are required for the engine to draft recommendations that are graded AND grounded.

`tier_4_costs` (Influence vs Cost) and `tier_5_live` (auto-execute) are downstream; both depend on `tier_3_recommend` being closed first.

## 12. The PPIM signature, restated

- **interaction**: all later recommendations now graded against your targets
- **economics**: prevents misaligned automation (avg $30k+/yr risk avoided)
- **predictability**: HIGH
- **brand_dimension**: coherence + accountability

"Accountability" is the second-order benefit: every recommendation has a Penrose score, every constraint enforcement is logged, every projection is falsified or confirmed. The audit trail extends through Stage 9 and beyond — when the operator (or a stakeholder) asks "why did the platform recommend this?", the answer is a specific Penrose score, projection mechanism, and constraint evaluation. The accountability is structural; it can't be retrofit.
