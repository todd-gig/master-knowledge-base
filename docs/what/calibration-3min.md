# What you'll do in Stage 9 — Calibration → Live Mode (3-minute walkthrough)

Stage 9 is owned by the **decision-engine**. Secondary engines are **PPEME** and **human-management-engine**. Stage 9 consists of **four actions**, executed in this exact order:

1. `enable-shadow-mode`
2. `review-shadow-recommendations`
3. `graduate-to-live-recommend`
4. `graduate-to-live-execute`

The order is enforced; you cannot graduate to live recommend before reviewing shadow recommendations, and you cannot graduate to live execute before live recommend is on.

## Action 1 — `enable-shadow-mode`

You flip a single toggle: shadow mode on. The decision-engine starts recommending in parallel with your existing process. **No actions taken — observation only.** The recommendations are logged, scored by Penrose, and surfaced in the calibration panel. Your team continues running the operator's actual work; the platform watches and produces what-it-would-have-recommended logs.

The chat affordance is `shadow_mode_toggle`. The action emits `ShadowModeEnabled` and auto-completes on first emit.

## Action 2 — `review-shadow-recommendations`

You review the shadow log weekly. Each review compares what the platform would have recommended to what actually happened. The review produces three signals per recommendation: drift detection (did projected diverge from actual), outcome attribution (which inputs drove the result), and variance scoring (how predictable was this class of recommendation).

The chat affordance is `confirmation_only` (the operator reviews a panel and acknowledges). Each review emits `ShadowReviewCompleted`. **The action auto-completes after 4 ShadowReviewCompleted events.**

Four reviews is the floor — below four, the calibration sample is too small to confidently say "drift_critical_count == 0." Above four, the OVS-Calibration scorer has enough data to grade attribution reliably.

## Action 3 — `graduate-to-live-recommend`

You graduate the platform to live recommend. Recommendations now surface to your team in real workflows — the assignment surface in `/assignments`, the chat surface for relevant people, the workflow tools your operator already uses. **Still no auto-execute.** Humans review every recommendation before action.

The chat affordance is `confirmation_only`. The action emits `LiveRecommendActivated`.

## Action 4 — `graduate-to-live-execute`

The terminal action. tier_5_live capability unlocks. The platform now executes low-risk decisions autonomously, surfaces high-risk ones to humans. Each auto-execute class requires the sign-off matrix at `/founder/signoff` to be cleared for that class before the auto-execute path opens.

The action emits **`LiveAutoExecuteActivated`** — that is the event that signals tier_5_live is granted at the end of Stage 9.

## The difference between "live recommend" and "live auto-execute"

This is a frequent source of confusion. The key difference: live recommend surfaces a recommendation to a human, who decides whether to act on it. Live auto-execute **lets the platform act autonomously** on classes the operator has signed off on. Auto-execute classes are scoped narrowly (one workflow type, one risk band) and explicitly approved per class via the sign-off matrix.

## The activation gate (v1.1.0 evidence-based)

`GET {decision_engine_base}/v1/operators/{operator_id}/calibration-status` with predicate:

```
all_of:
  - $.drift_critical_count == 0
  - $.interactions_logged_count >= 30
  - $.shadow_days_elapsed >= 30
```

Note: the `shadow_days_elapsed` predicate appears in the v1.0 manifest you may be reading. The **v1.1.0 amendment** removes the calendar predicate in favor of `education_tests_passed_all == true` as the fourth verification dimension. See `/docs/deep/ovs-calibration-10min.md` for the full v1.1.0 doctrine.

## Events emitted

- `StageStarted`
- `ShadowModeEnabled`
- `ShadowReviewCompleted` (fires per weekly review)
- `LiveRecommendActivated`
- `LiveAutoExecuteActivated`
- `StageCompleted`

## What unlocks at completion

Stage 9 unlocks **`tier_5_live`** — the autonomy tier. Specifically:

- `gigaton.decision.live_recommend` — recommendations surface to your team in live workflows.
- `gigaton.decision.live_auto_execute` — the platform acts autonomously on signed-off classes.

The `calibration` and `founder` nav circles illuminate. (The `founder` circle has an additional gate — `@gigaton.ai` email domain — for Gigaton-internal founders.)

## Streak eligibility

Stage 9 is **not streak-eligible** — it's a one-shot graduation. The badge slug is `live-mode-graduate`; the success celebration message is "You are live. Every decision is now grounded in your doctrine, ICP, goals, processes, ownership, and economics — and the platform learns from every outcome."

## Predicted outcomes

Fallback predicted influence is **$85,000** — the highest of any stage. The PPIM signature describes Stage 9's interaction as **platform now produces decisions on your behalf** and the economic state as **full PPIM loop closed — operator is in compounding regime.**

## What you can't do

You cannot skip Stage 9 via a `workflow_overlays` configuration. The `overlay_schema.inviolable_stage_ids` list includes Stage 9 — server-enforced. **False**: an operator cannot skip Stage 9 and jump straight to tier_5_live by configuring a workflow_overlay.
