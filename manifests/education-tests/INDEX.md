# Education Test Catalog — INDEX v0.1.0

This index maps every onboarding stage to its paired education tests. It is the file the
Stage 9 graduation gate's resolver reads to determine **which** (stage, tier) pairs are
required for `education_tests_passed_all == true`.

- **Schema**: `manifests/education-tests/SCHEMA.md`
- **Parent manifest**: `manifests/onboarding_v1.yaml` (referenced as `education_tests_catalog`)
- **Pass-criteria seeds**: INTEL-3-bounded (range 70–95); `why` / `what` seed 80%, `deep_dive` seed 90%
- **Attempts seed**: 3 per tier (INTEL-3 algorithm-pending)
- **Catalog totals**: 10 stage files · 27 tests · 105 questions

---

## Stage → tests mapping

| Stage | File | Tiers (questions) | min_score_pct seeds | attempts | Notes |
|---|---|---|---|---|---|
| stage-0-trust-scope | [stage-0-trust-scope.yaml](stage-0-trust-scope.yaml) | why (3), what (4), deep_dive (4) | 80 / 80 / 90 | 3 | Axiom Registry + scope contract |
| stage-1-sources | [stage-1-sources.yaml](stage-1-sources.yaml) | why (3), what (4), deep_dive (4) | 80 / 80 / 90 | 3 | Documentation ingest |
| stage-2-people | [stage-2-people.yaml](stage-2-people.yaml) | why (3), what (4), deep_dive (5) | 80 / 80 / 90 | 3 | BFT snapshot foundation |
| stage-3-brand-customer-lens | [stage-3-brand-customer-lens.yaml](stage-3-brand-customer-lens.yaml) | why (3), what (4), deep_dive (4) | 80 / 80 / 90 | 3 | PPIM doctrine entry point |
| stage-4-goals-kpis | [stage-4-goals-kpis.yaml](stage-4-goals-kpis.yaml) | why (3), what (4), deep_dive (4) | 80 / 80 / 90 | 3 | Penrose Falsification Scoreboard |
| stage-5-industry-processes | [stage-5-industry-processes.yaml](stage-5-industry-processes.yaml) | why (3), what (4) | 80 / 80 | 3 | No deep_dive in manifest |
| stage-6-org-processes | [stage-6-org-processes.yaml](stage-6-org-processes.yaml) | why (3), what (4) | 80 / 80 | 3 | No deep_dive in manifest |
| stage-7-assignments | [stage-7-assignments.yaml](stage-7-assignments.yaml) | why (3), what (5) | 80 / 80 | 3 | No deep_dive in manifest |
| stage-8-tech-stack-costs | [stage-8-tech-stack-costs.yaml](stage-8-tech-stack-costs.yaml) | why (3), what (4), deep_dive (4) | 80 / 80 / 90 | 3 | Influence vs Cost dashboard |
| stage-9-calibration-live | [stage-9-calibration-live.yaml](stage-9-calibration-live.yaml) | why (3), what (4), deep_dive (9) | 80 / 80 / 90 | 3 | **Highest leverage** — v1.1.0 amendment doctrine |

---

## Required (stage, tier) pairs for `education_tests_passed_all`

The graduation gate considers `education_tests_passed_all == true` IFF an
`EducationTestPassed` event has been emitted for every row below for the operator:

```
(stage-0-trust-scope,         why)
(stage-0-trust-scope,         what)
(stage-0-trust-scope,         deep_dive)
(stage-1-sources,             why)
(stage-1-sources,             what)
(stage-1-sources,             deep_dive)
(stage-2-people,              why)
(stage-2-people,              what)
(stage-2-people,              deep_dive)
(stage-3-brand-customer-lens, why)
(stage-3-brand-customer-lens, what)
(stage-3-brand-customer-lens, deep_dive)
(stage-4-goals-kpis,          why)
(stage-4-goals-kpis,          what)
(stage-4-goals-kpis,          deep_dive)
(stage-5-industry-processes,  why)
(stage-5-industry-processes,  what)
(stage-6-org-processes,       why)
(stage-6-org-processes,       what)
(stage-7-assignments,         why)
(stage-7-assignments,         what)
(stage-8-tech-stack-costs,    why)
(stage-8-tech-stack-costs,    what)
(stage-8-tech-stack-costs,    deep_dive)
(stage-9-calibration-live,    why)
(stage-9-calibration-live,    what)
(stage-9-calibration-live,    deep_dive)
```

Stages 5, 6, 7 have no `deep_dive_*` reference in the parent manifest's `education:`
block; per SCHEMA.md authoring rule #4, no `deep_dive` tier is required for those stages.

---

## INTEL-3 reminder

Every `min_score_pct` and `attempts_allowed` in the catalog is a **seed within a bounded
range**, not a target. The runtime grader (engine-side, separate PR) will adjust within
the range. Until that algorithm ships, the seeded values apply.

| Tier | Seed `min_score_pct` | Bounded range | Seed `attempts_allowed` |
|---|---|---|---|
| `why` | 80 | 70 – 95 | 3 |
| `what` | 80 | 70 – 95 | 3 |
| `deep_dive` | 90 | 70 – 95 | 3 |

---

## Out of scope (do NOT block this PR on these)

- The grader engine (separate PR)
- The chat surface rendering of questions (gigaton-ui-system, separate PR)
- The persistence of `EducationTestPassed` events (HME, separate PR)
- The doc markdown at `/docs/why/...`, `/docs/what/...`, `/docs/deep/...` (separate content PRs)
