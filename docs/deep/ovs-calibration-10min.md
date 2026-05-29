# OVS-Calibration → Live Mode — Deep Dive (10-minute read)

This deep dive is the highest-leverage document in the education catalog. It covers the **v1.1.0 amendment doctrine** that replaced the calendar-clock predicate in Stage 9's graduation gate with an **evidence-based four-dimension verification**; explains what each dimension measures; defines what "monitor more closely" means post-graduation; and details why a `drift_critical` regression **auto-suspends** `tier_5_live` capability instead of just emitting a warning. It assumes you have read the `why_1min` and `what_3min` documents for Stage 9.

---

## 1. The v1.1.0 amendment — no calendar clock

The original manifest (v1.0) included a calendar-based predicate in the Stage 9 graduation gate:

```
shadow_days_elapsed >= 30
```

That predicate said: regardless of how well-calibrated the substrate is, the operator must wait 30 calendar days before graduating. The intent was protective — give the calibration loop time to surface drift.

The **v1.1.0 amendment** removed that predicate. The reasoning:

- A well-prepared operator who clears all evidence dimensions in 12 days was being penalized by a clock that didn't reflect calibration quality.
- A less-prepared operator who needed 60 days was being graduated at day 30 even with weak evidence.
- The clock was a proxy for calibration confidence, not a measure of it.

The amendment replaced `shadow_days_elapsed >= 30` with `education_tests_passed_all == true` as the fourth verification dimension. The graduation gate is now **evidence-based** — the platform looks at whether the substrate is actually calibrated, not at how long it's been waiting.

The verbatim shift: the predicate that v1.1.0 removed is **`shadow_days_elapsed`**; the kind of gate that replaced it is **evidence-based**. **False**: a 30-day calendar elapsed period is NOT still required for Stage 9 graduation even when all evidence dimensions are green.

## 2. The four verification dimensions

The v1.1.0 evidence-based graduation gate evaluates exactly four verification dimensions:

1. **`drift_critical_count == 0`** — no critical drift events outstanding.
2. **`interactions_logged_count >= threshold`** — sufficient calibration sample size (algorithm-pending, INTEL-3-bounded; seed value 30).
3. **`shadow_reviews_completed >= threshold`** — sufficient operator review cadence (algorithm-pending, INTEL-3-bounded; seed value 4).
4. **`education_tests_passed_all == true`** — every required (stage, tier) education test has a passing event.

All four must hold. A single dimension failure keeps the gate closed regardless of the other three.

The fourth dimension — **`education_tests_passed_all == true`** — is the one this education-test catalog provides the operand for. Without paired tests for the existing education modules, dimension 4 had no operand; the v1.1.0 amendment without this catalog would have been structurally incomplete.

## 3. INTEL-3 bounding on the dimensions

Per the INTEL-3 doctrine (no static weights; algorithmic real-time determination), the threshold values for dimensions 2 and 3 are **seeds within bounded ranges**, not fixed targets. The runtime grader (separate engine-side PR) adjusts thresholds based on operator-cohort behavior:

- `interactions_logged_count` seed = 30, bounded range to be set per algorithm.
- `shadow_reviews_completed` seed = 4, bounded range to be set per algorithm.
- `drift_critical_count` is binary (0 or >0) — exempt from algorithmic drift.
- `education_tests_passed_all` is binary — exempt from algorithmic drift.

Binary policy rules are inviolable; threshold rules are INTEL-3-bounded. The runtime never relaxes a binary; it may adjust a threshold within bounds based on observed drift_critical correlation.

## 4. The three subsystems during shadow

Three subsystems collaborate during Stage 9's shadow period: **PPEME simulates, decision-engine recommends, OVS-Calibration scores attribution.**

- **PPEME** (predictive-platform engineering matrix engine) generates what-if simulations against the operator's substrate. PPEME's projections are the baseline against which actual outcomes are measured.
- **decision-engine** produces real-world recommendations based on the operator's live context. These are the recommendations that would have been surfaced to humans (and eventually executed) in live mode.
- **OVS-Calibration** (Outcome Variance Score Calibration) scores attribution — for each shadow recommendation, it compares projected impact to actual impact and decomposes the variance by input source.

The three together generate the per-interaction telemetry that powers all four verification dimensions.

## 5. What "monitor more closely" means post-graduation

Post-graduation, the doctrine phrase **"monitor more closely"** specifically refers to **tighter drift thresholds and elevated cadence**. Concretely:

- The Penrose scoreboard cadence shifts from weekly (shadow) to continuous (live). Drift signal is computed against every executed decision, not against weekly batch reviews.
- The drift-threshold sensitivity tightens. A pre-graduation drift threshold of, say, 20% projection-vs-actual divergence might shift to 10% post-graduation. The platform expects tighter alignment once auto-execute is on.
- The drift_sentinel runs at elevated cadence — checking for drift signals continuously rather than per-review.

**True**: after graduation, the Penrose scoreboard cadence and drift-threshold sensitivity tighten relative to the shadow period.

The semantics matter because operators sometimes expect "graduation" to mean "the platform stops watching as carefully." The opposite is true: graduation is when the platform's monitoring obligations *increase*, because the consequences of misfire — auto-executed decisions on the operator's behalf — are higher.

## 6. drift_critical regression → auto-suspend

When `drift_critical` regresses post-graduation, **the first system action is**: `tier_5_live` (live auto-execute) is **auto-suspended**. This happens before any email, before any warning, before any operator review.

**Why auto-suspend instead of warn?** The reasoning is structural and traceable to the trust model:

- The platform graduated the operator to tier_5_live on the **premise** that drift_critical_count was 0. When drift_critical regresses, **the premise is revoked.** Continuing to auto-execute under a revoked premise would be acting outside the trust the operator granted.
- Auto-execute is **inviolable scope** — the operator authorized it for specific classes under specific evidence conditions. When the evidence conditions fail, the authorization fails with them. Continuing to act would be operating outside the scope contract.
- A warning-only model leaves a window of risk between detection and operator response. For high-volume auto-execute classes, that window may include dozens of decisions made under a known-broken model. Auto-suspend eliminates the window.

The single-sentence answer to "why auto-suspend rather than warn?": **the evidence was the premise of trust; when the evidence regresses, the premise is revoked and continuing to auto-execute would be acting outside the operator's authorization.**

The auto-suspend behavior:

1. `Tier5SuspensionTriggered` event fires immediately on `drift_critical` regression.
2. All auto-execute classes for the affected operator pause within 60 seconds. Pending auto-executions complete; new auto-executions are blocked.
3. Live recommend (the tier_3 capability) continues — humans can still review recommendations, the engine still drafts them. Only auto-execute is suspended.
4. The operator is notified in chat, in the calibration panel, and via the configured escalation channel.
5. The operator (or their delegated authority per the sign-off matrix) reviews the drift signal, addresses the root cause, and re-runs the four-dimension verification.
6. When all four dimensions pass again, `Tier5SuspensionLifted` fires and auto-execute resumes.

The suspension is not a punishment; it's a structural consequence of the trust model. The platform stops doing the thing the evidence no longer supports.

## 7. The Stage 9 graduation gate evaluation, end-to-end

```
education_tests_passed_all := for every (stage, tier) in INDEX.md,
                              an EducationTestPassed event exists for this operator

graduation_eligible := (
  drift_critical_count == 0
  AND interactions_logged_count >= threshold_2
  AND shadow_reviews_completed >= threshold_3
  AND education_tests_passed_all == true
)
```

If any required (stage, tier) is missing or has no passing event, dimension 4 fails and the gate stays closed. If `drift_critical_count` is nonzero, dimension 1 fails and the gate stays closed. Each dimension is independently gating.

## 8. Why the catalog's pass_criteria are seeds, not targets

Per INTEL-3, the per-tier `min_score_pct` and `attempts_allowed` values in the education-test catalog are seeds within bounded ranges:

| Tier | `min_score_pct` seed | Bounded range | `attempts_allowed` seed |
|---|---|---|---|
| `why` | 80 | 70 – 95 | 3 |
| `what` | 80 | 70 – 95 | 3 |
| `deep_dive` | 90 | 70 – 95 | 3 |

The runtime grader (separate PR) adjusts:

- `min_score_pct` per cohort based on observed drift_critical correlation. If operators who pass the `why` tier at 80% show no different drift outcomes than operators who pass at 70%, the threshold drifts toward 70%. If 90% correlates with materially fewer drift_critical events, the threshold drifts toward 90%.
- `attempts_allowed` per operator based on retry-success curves.

Neither value exceeds the bounded range without explicit governance change. The lower bound (70%) is **inviolable** — the runtime never drops below it under any algorithmic adjustment.

## 9. Edge cases

- **Operator has all four dimensions green but no live-mode confidence.** The graduation is **operator-initiated**, not automatic. Even when the gate is open, the operator must explicitly take the `graduate-to-live-execute` action. Some operators sit at "gate open, not graduated" for weeks while they ramp internal confidence; that's a legitimate state.
- **Operator graduates, drift stays clean for 90 days, then regresses.** Standard auto-suspend behavior. The 90-day clean history doesn't grandfather the operator out of the auto-suspend rule.
- **Drift_critical regression caused by an external event** (e.g., a market shock that breaks the cost model). Same auto-suspend behavior. Root cause is investigated post-suspension; auto-suspend is event-driven, not cause-driven.
- **Operator wants to re-take an education test after passing.** Supported via the `/calibration` UI. The new attempt's score replaces the prior; if the new score drops below `min_score_pct`, the prior pass remains in effect (no retroactive removal). The Stage 9 gate cares only that *a* passing event exists per (stage, tier).
- **A new stage is added to the manifest after operator graduation.** The INDEX.md update introduces new (stage, tier) pairs. Existing graduated operators retain their tier_5_live status, but the new dimension-4 evaluation now considers the additional pairs; passes are required within a runtime-defined grace period or auto-suspend triggers.

## 10. Post-graduation operating state

Post-graduation, the operator is in what the manifest calls the **compounding regime**:

- Every executed decision feeds back into the drift_sentinel and OVS-Calibration.
- Every Penrose-graded outcome refines the projection model.
- Every BFT-snapshot interaction updates the persona-engine's confidence on that person.
- Every workflow execution updates HME's automation-likelihood scoring.

The platform learns from every outcome. Compounding is the structural reward for clearing Stage 9 — the substrate keeps improving as the operator keeps operating.

The PPIM signature reflects this:

- **interaction**: platform now produces decisions on your behalf
- **economics**: full PPIM loop closed — operator is in compounding regime
- **predictability**: continuously falsified by Penrose scoreboard
- **brand_dimension**: full coherence + autonomy

"Continuously falsified" is the live-mode equivalent of Stage 4's "graded against your targets." The grading never stops; the falsification loop never closes; the model keeps refining. Stage 9 graduation is not an end-state; it's an entry to the compounding regime.

## 11. The events catalog and the auto-suspend hook

The events emitted across the Stage 9 lifecycle:

- `StageStarted` — operator enters Stage 9.
- `ShadowModeEnabled` — action 1 completes.
- `ShadowReviewCompleted` — fires per weekly review (4 required to satisfy action 2).
- `LiveRecommendActivated` — action 3 completes (tier_5 live_recommend on).
- **`LiveAutoExecuteActivated`** — action 4 completes (tier_5 live_auto_execute on). This is the event that signals **tier_5_live is granted** at the end of Stage 9.
- `StageCompleted` — gate predicate becomes true.
- `Tier5SuspensionTriggered` — post-graduation drift_critical regression auto-suspend.
- `Tier5SuspensionLifted` — drift resolved, four dimensions re-pass.

The auto-suspend hook is the operational expression of the trust model. The platform commits to acting on the operator's behalf only under conditions the operator authorized; when those conditions fail, the platform stops acting.

## 12. The lesson, distilled

The v1.1.0 doctrine is built on three commitments:

1. **No clock.** Calibration confidence, not calendar time, governs graduation.
2. **Four evidence dimensions.** Drift, sample size, review cadence, education comprehension.
3. **Trust is conditional.** Auto-execute lives under an evidence premise; when the premise fails, the authorization fails with it.

The result: a graduation gate that protects the operator without penalizing them for being well-prepared, and a post-graduation monitoring regime that protects the operator from misfire under a known-broken model. Operators who internalize the doctrine — and pass the deep_dive test that verifies they have — are the operators best equipped to use tier_5_live well.
