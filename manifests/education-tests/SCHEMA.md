# Education Test Catalog — Schema v0.1.0

This directory holds the **paired education tests** for every stage in `manifests/onboarding_v1.yaml`.
Each test verifies that an operator (or proxy reviewer) has read + understood the corresponding
`why_1min` / `what_3min` / `deep_dive_10min` source markdown.

The Stage 9 evidence-based graduation gate (`education_tests_passed_all == true`) is what consumes
these — graders + scoring engines are out of scope here. This catalog is **pure declarative data**
in the same spirit as `onboarding_v1.yaml`. No business logic. No grader. No runtime.

---

## Why this catalog exists

The onboarding manifest (v1.1.0, master-knowledge-base PR #29) replaced the calendar-based
"30 shadow days" rule in Stage 9 with an **evidence-based** graduation gate over four
verification dimensions:

1. drift_critical_count == 0
2. interactions_logged_count ≥ threshold (algorithm-pending, INTEL-3-bounded)
3. shadow_reviews_completed ≥ threshold (algorithm-pending, INTEL-3-bounded)
4. **education_tests_passed_all == true** ← this catalog

Without paired tests for the existing education modules, dimension 4 has no operand. This
catalog provides the operand without prescribing how it is graded.

---

## File layout

```
manifests/education-tests/
  SCHEMA.md                          ← this file
  INDEX.md                           ← table mapping stage → test files → question count → pass criteria
  stage-0-trust-scope.yaml
  stage-1-sources.yaml
  stage-2-people.yaml
  stage-3-brand-customer-lens.yaml
  stage-4-goals-kpis.yaml
  stage-5-industry-processes.yaml
  stage-6-org-processes.yaml
  stage-7-assignments.yaml
  stage-8-tech-stack-costs.yaml
  stage-9-calibration-live.yaml
```

One YAML file per stage. Each file contains a `tests:` array — one entry per education tier
that the parent manifest references in that stage's `education:` block. If the manifest does
NOT reference a `deep_dive_*` for a stage, no `deep_dive` test is authored for that stage.
Do not fabricate tests for tiers that don't exist upstream.

---

## YAML schema

Each stage file follows this shape:

```yaml
stage_id: stage-N-<slug>            # MUST match a stage id in onboarding_v1.yaml
manifest_education_block:           # echo of the parent manifest's education: block, for traceability
  why_1min: /docs/why/...md
  what_3min: /docs/what/...md
  deep_dive_10min: /docs/deep/...md # omit if not in manifest

tests:
  - tier: why                       # enum: why | what | deep_dive
    source_doc: /docs/why/...md     # MUST match the corresponding manifest education ref
    pass_criteria:
      min_score_pct: 80             # see "Pass-criteria conventions" below
      attempts_allowed: 3
    questions:
      - id: <slug>                  # unique within this tier
        prompt: |
          ...
        type: multiple_choice       # enum: multiple_choice | short_answer | true_false
        options:                    # only when type=multiple_choice
          - id: a
            text: ...
          - id: b
            text: ...
        correct: a                  # option id (multiple_choice) | bool (true_false)
        accepted_patterns:          # only when type=short_answer — keep simple for v0
          - keyword: "north star"
          - keyword: "constraint"
          - regex: "(?i)penrose"
        weight: 1.0                 # float, default 1.0
        references_action: declare-north-star  # optional, ties back to an action id in the stage
```

### Field reference

| Field | Type | Required | Notes |
|---|---|---|---|
| `stage_id` | string | yes | Must match a stage id in `onboarding_v1.yaml`. |
| `manifest_education_block` | object | yes | Echo of the parent manifest's `education:` block for traceability. |
| `tests` | array | yes | One entry per tier the manifest references. |
| `tests[].tier` | enum | yes | `why` \| `what` \| `deep_dive`. |
| `tests[].source_doc` | string | yes | Path to the markdown that this test verifies comprehension of. |
| `tests[].pass_criteria.min_score_pct` | int | yes | INTEL-3 seed (see below). |
| `tests[].pass_criteria.attempts_allowed` | int | yes | INTEL-3 seed (see below). |
| `tests[].questions` | array | yes | 3–5 questions per tier. |
| `tests[].questions[].id` | slug | yes | Unique within the tier. |
| `tests[].questions[].prompt` | string | yes | What the operator is asked. |
| `tests[].questions[].type` | enum | yes | `multiple_choice` \| `short_answer` \| `true_false`. |
| `tests[].questions[].options` | array | conditional | Required when type=multiple_choice. Each item: `{id, text}`. |
| `tests[].questions[].correct` | mixed | yes | Option id (mc), bool (true_false), unused for short_answer. |
| `tests[].questions[].accepted_patterns` | array | conditional | Required when type=short_answer. Each item: `{keyword: "..."}` or `{regex: "..."}`. |
| `tests[].questions[].weight` | float | no | Default 1.0. |
| `tests[].questions[].references_action` | string | no | Stage action id. |

---

## Pass-criteria conventions

Per the **INTEL-3 doctrine** (no static weights; algorithmic real-time determination), every
threshold in this catalog is a **seed within a bounded range**, not a target. The runtime
grader (separate engine-side PR) will adjust within bounds based on operator cohort
behavior. Until that algorithm ships, the runtime uses the seeded value.

| Tier | `min_score_pct` seed | INTEL-3 bounded range | `attempts_allowed` seed | Notes |
|---|---|---|---|---|
| `why` | 80 | 70 – 95 | 3 | Comprehension of motivation. |
| `what` | 80 | 70 – 95 | 3 | Comprehension of mechanism. |
| `deep_dive` | 90 | 70 – 95 | 3 | Comprehension of doctrine; highest leverage. |

Both `min_score_pct` and `attempts_allowed` are **algorithm-pending**. The runtime grader
(out of scope for this PR) will:

- adjust `min_score_pct` per cohort based on observed drift_critical correlation
- adjust `attempts_allowed` per operator based on retry-success curves
- never exceed the bounded range above without an explicit governance change

The `$1k payout floor` style binary policy rules and the `min_score_pct ≥ 70` lower bound are
**exempt from algorithmic drift** — they are inviolable.

---

## Events emitted

When a test passes (`score_pct >= min_score_pct` in any allowed attempt), the grader emits:

```yaml
event_type: EducationTestPassed
payload:
  operator_id: string
  stage_id: string
  tier: enum [why, what, deep_dive]
  source_doc: string
  score_pct: number
  attempts_used: int
  emitted_at: ISO-8601
```

The Stage 9 graduation gate evaluates:

```
education_tests_passed_all := for every (stage, tier) in INDEX.md,
                              an EducationTestPassed event exists for this operator
```

If any required (stage, tier) is missing or has no passing event, the gate stays closed.

---

## Authoring rules

1. **Questions derive from the stage**, not the doc. The source-of-truth for question content
   is each stage's `name` + `short_description` + `why_this_stage` + per-action `description`
   in `onboarding_v1.yaml`. (The doc markdown files referenced in `source_doc` may not yet
   exist; tests must be authored against the manifest's intent, not against doc prose.)
2. **3–5 questions per tier**, mixing all three `type` values across each stage file (at
   least one of each across the file).
3. **Stage 9 deep_dive is the highest-leverage test** — it specifically verifies the v1.1.0
   amendment (no calendar clock; evidence-based gate), the four verification dimensions,
   what "monitor more closely" means post-graduation, and why a drift_critical regression
   auto-suspends capability.
4. **No fabricated tiers** — if the manifest's `education:` block omits a tier, omit the test.
5. **`references_action` is encouraged** wherever a question maps cleanly to one of the
   stage's actions.

---

## Out of scope for this PR

- The grader/scoring engine (engine-side, separate PR)
- The chat surface that renders the questions (gigaton-ui-system, separate PR)
- The persistence of `EducationTestPassed` events (HME, separate PR)
- The actual doc markdown at `/docs/why/...`, `/docs/what/...`, `/docs/deep/...` (separate
  content PRs; tests authored against manifest intent so they remain valid once docs land)

---

## Version

`schema_version: 0.1.0` — first cut. Bump on any breaking field rename.
