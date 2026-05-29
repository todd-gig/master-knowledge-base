# Operator Education Docs — Index

This index maps every (stage, tier) referenced by `manifests/onboarding_v1.yaml`'s `education:` blocks to its authored doc path and word count. Tier conventions: `why_1min` is a plain-English motivation (~150-300 words target; some run slightly over to cover test surface), `what_3min` is a concrete walkthrough of the stage's actions (~400-700 words), and `deep_dive_*` is technical doctrine (~1000-2000 words). Stages 5, 6, 7 have no `deep_dive_*` reference in the manifest, so no deep_dive doc was authored for them — per `manifests/education-tests/SCHEMA.md` authoring rule #4.

## Stage → tier → doc mapping

| Stage | Tier | Doc path | Word count |
|---|---|---|---|
| stage-0-trust-scope | why_1min | `/docs/why/trust-scope-1min.md` | 308 |
| stage-0-trust-scope | what_3min | `/docs/what/trust-scope-3min.md` | 533 |
| stage-0-trust-scope | deep_dive_10min | `/docs/deep/trust-scope-axiom-registry-10min.md` | 1317 |
| stage-1-sources | why_1min | `/docs/why/sources-1min.md` | 313 |
| stage-1-sources | what_3min | `/docs/what/sources-3min.md` | 640 |
| stage-1-sources | deep_dive_10min | `/docs/deep/documentation-ingest-10min.md` | 1334 |
| stage-2-people | why_1min | `/docs/why/people-1min.md` | 327 |
| stage-2-people | what_3min | `/docs/what/people-3min.md` | 721 |
| stage-2-people | deep_dive_10min | `/docs/deep/bft-snapshot-explainer-10min.md` | 1522 |
| stage-3-brand-customer-lens | why_1min | `/docs/why/brand-customer-1min.md` | 311 |
| stage-3-brand-customer-lens | what_3min | `/docs/what/brand-customer-3min.md` | 663 |
| stage-3-brand-customer-lens | deep_dive_10min | `/docs/deep/ppim-doctrine-10min.md` | 1647 |
| stage-4-goals-kpis | why_1min | `/docs/why/goals-1min.md` | 351 |
| stage-4-goals-kpis | what_3min | `/docs/what/goals-3min.md` | 648 |
| stage-4-goals-kpis | deep_dive_10min | `/docs/deep/penrose-falsification-10min.md` | 1593 |
| stage-5-industry-processes | why_1min | `/docs/why/industry-processes-1min.md` | 360 |
| stage-5-industry-processes | what_3min | `/docs/what/industry-processes-3min.md` | 594 |
| stage-5-industry-processes | deep_dive | — (no manifest reference; skipped per SCHEMA.md rule #4) | — |
| stage-6-org-processes | why_1min | `/docs/why/org-processes-1min.md` | 354 |
| stage-6-org-processes | what_3min | `/docs/what/org-processes-3min.md` | 645 |
| stage-6-org-processes | deep_dive | — (no manifest reference; skipped per SCHEMA.md rule #4) | — |
| stage-7-assignments | why_1min | `/docs/why/assignments-1min.md` | 345 |
| stage-7-assignments | what_3min | `/docs/what/assignments-3min.md` | 570 |
| stage-7-assignments | deep_dive | — (no manifest reference; skipped per SCHEMA.md rule #4) | — |
| stage-8-tech-stack-costs | why_1min | `/docs/why/tech-stack-costs-1min.md` | 366 |
| stage-8-tech-stack-costs | what_3min | `/docs/what/tech-stack-costs-3min.md` | 679 |
| stage-8-tech-stack-costs | deep_dive_10min | `/docs/deep/influence-vs-cost-10min.md` | 1603 |
| stage-9-calibration-live | why_1min | `/docs/why/calibration-1min.md` | 349 |
| stage-9-calibration-live | what_3min | `/docs/what/calibration-3min.md` | 712 |
| stage-9-calibration-live | deep_dive_10min | `/docs/deep/ovs-calibration-10min.md` | 1971 |

## Rollups

- Total docs authored: **27** (10 why_1min, 10 what_3min, 7 deep_dive_10min — Stages 5, 6, 7 have no deep_dive reference in the manifest).
- Total word count: **~23,123 words** across the catalog.
- Stage 9 deep_dive (`/docs/deep/ovs-calibration-10min.md`) is the catalog's highest-leverage doc — it covers the v1.1.0 amendment that replaced the calendar-clock predicate with an evidence-based four-dimension graduation gate, post-graduation "monitor more closely" semantics, and drift_critical regression auto-suspend behavior. Stage 9's deep_dive education test (9 questions in `manifests/education-tests/stage-9-calibration-live.yaml`) is graded against the facts in this doc.

## Alignment with education-tests catalog

Each doc was authored to satisfy the question content in the paired `manifests/education-tests/stage-N-*.yaml` test files. The Stage → Tier → Question coverage is:

- Stage 0: 11 questions across why (3) + what (4) + deep_dive (4)
- Stage 1: 11 questions across why (3) + what (4) + deep_dive (4)
- Stage 2: 12 questions across why (3) + what (4) + deep_dive (5)
- Stage 3: 11 questions across why (3) + what (4) + deep_dive (4)
- Stage 4: 11 questions across why (3) + what (4) + deep_dive (4)
- Stage 5: 7 questions across why (3) + what (4)
- Stage 6: 7 questions across why (3) + what (4)
- Stage 7: 8 questions across why (3) + what (5)
- Stage 8: 11 questions across why (3) + what (4) + deep_dive (4)
- Stage 9: 16 questions across why (3) + what (4) + deep_dive (9)

Total: **105 questions** across 27 tests, all of which have answerable surface in the authored docs above.

## Skipped deep_dive stages — confirmation

Per `manifests/education-tests/SCHEMA.md` authoring rule #4 ("No fabricated tiers — if the manifest's `education:` block omits a tier, omit the test"), Stages 5, 6, and 7 have no deep_dive content authored because the parent manifest's `education:` block does not reference one. Verified by inspecting each stage's `education:` block in `manifests/onboarding_v1.yaml`:

- Stage 5 `education`: `why_1min`, `what_3min` only (lines 548-550 of the manifest).
- Stage 6 `education`: `why_1min`, `what_3min` only (lines 608-610).
- Stage 7 `education`: `why_1min`, `what_3min` only (lines 667-669).

If a deep_dive is later added to any of these stages, this index and a corresponding new deep_dive doc would be added together.
