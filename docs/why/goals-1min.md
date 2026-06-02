# Why Stage 4 — Goals, KPIs & Constraints (1-minute read)

**The decision-engine needs targets to score against — without them, it can recommend, but it cannot recommend predictably.** Stage 4 supplies the targets.

The **Penrose Falsification Scoreboard** is the grading layer between decision-engine recommendations and operator outcomes. It compares projected impact to actual outcome for every recommendation, falsifies the projection when reality disagrees, and updates the model. **Penrose needs operator-declared targets to score against.** Without a declared north star and supporting metrics, every recommendation is graded against a generic baseline that isn't this operator's baseline — and the falsification signal becomes meaningless.

Constraints declared in Stage 4 become **hard guardrails** the Decision Execution Engine enforces. Not soft preferences. Not warnings. The constraint "never email opt-outs" means the engine will not produce a recommendation that emails opt-outs even if the projected revenue lift is high. The constraint "never undercut floor price" means the engine will not recommend a discount below the floor regardless of conversion projections. These are **inviolable** within scope, same severity model as the Stage 0 axioms but operator-specific.

**Without a north star + 3 supporting metrics + at least 1 constraint, decision-engine cannot make graded recommendations.** The Stage 4 activation gate enforces all three predicates. Tier_3_recommend (the "draft recommendations" capability) does not unlock until Stage 4 closes.

Misaligned automation — automation that pursues the wrong target — costs operators an average **$30k+/year** in opportunity cost, recovery cost, or active damage. Stage 4 prevents that by requiring the operator to declare the target explicitly before automation is enabled.

The supporting metrics exist as **counterweights** against gaming the north star. An operator who only declares revenue as a north star creates an incentive for the engine to recommend revenue-positive actions that hurt retention or NPS. Three supporting metrics force the engine to optimize across a balanced front; gaming any single metric becomes structurally hard.

If you only remember one thing: **Stage 4 is the moment the operator tells the decision-engine what to optimize for and what it must never do. Skipping it means the engine is firing without a target.**
