# Calendly Multipli Beta Test Summary

```ppim-signature
interaction: prospect_outreach_evidence_attachment_executive_summary
economics: aggregates_fit_score_plus_scenario_band_plus_next_action_for_executive_consumption
predictability: explicit_listing_of_what_ran_versus_what_was_substituted_versus_what_is_missing
brand_dimension: vendor_growth_acquisition_intelligence
lifecycle: acquisition_stage_sixth_and_final_artifact_of_six_file_bundle
```

**Vendor.** Calendly LLC (`calendly_v1`)
**Beta run.** Sample bundle #1 of 3 planned (Calendly / Loom / Notion).
**Beta date.** 2026-05-25 (Mon).
**Sprint deadline.** EOD Tue 2026-05-26 — internal readiness only per Assumption 1.
**Status.** Internal-readiness draft. Do not forward externally without Todd review.

---

## Executive Summary (60 seconds)

Calendly scores **75/100 → `high_fit`** against the Multipli vendor-financing scoring rubric. The three strongest fit signals are (1) Calendly is a textbook `software_saas` match for Multipli's top declared segment, (2) Calendly's mid-market motion has documented annual-prepay payment friction (the highest-leverage objection for Multipli financing), and (3) Calendly's enterprise tier has clearly bundleable services (onboarding, SSO, premium support) that expand financed contract value beyond seat licenses.

At an 8% take-rate mid-scenario on a conservative 200-financed-deal Year-1 pilot ($3.6M incremental funded volume), Multipli estimated net revenue band is **$288k Year 1**, with a $108k-$576k range across the full 3-16% take-rate scenario span. Confidence on Calendly-specific inputs is capped at **0.62** because every numeric value is LLM-modeled from public sources rather than Calendly-confirmed.

**Recommended next action.** A 30-minute Calendly design-partner conversation to validate inputs. If aligned, a 90-day enterprise-tier financing pilot covering ~50 financing-eligible opportunities, with quarterly review.

---

## 1. What this beta tested

The Multipli sprint runbook (`runbooks/2026_05_22_multipli_vendor_growth_engine_4day_sprint.md`) calls for a 6-file output bundle per sample vendor. This document is the 6th file. The other 5:

1. `vendor_opportunity_profile.json` — Calendly fact pack mapped to the package's `vendor_opportunity` schema, with per-field provenance and confidence.
2. `fit_score_report.md` — 8-component weighted score, reason codes, missing-info gate list.
3. `deal_economics_model.json` — Six take-rate scenarios × conservative + optimistic financed-volume bands.
4. `proposal_recommendation.md` — Internal-draft 90-day pilot pitch with compliance-disciplined language.
5. `dashboard_event_payload.json` — `vendor.financing.assessed.v1` event payload for HME / Pub/Sub ingestion.

## 2. What ran via live engines vs. what was hand-substituted

| Layer | Planned route | Live? | What ran |
|---|---|---|---|
| Vendor EO capture | `POST intel-silo /v1/multipli/vendor-intake` | NO — migration 033 not landed; `eo_type=vendor` rejected by current enum (confirmed via curl probe 2026-05-25T19:48Z) | Manual LLM extraction grounded in public sources (Calendly pricing page, G2/Capterra reviews, SaaS procurement research) |
| Fit scoring | `POST decision-engine /v1/multipli/vendor-fit-score` | NO — endpoint not yet built | Hand-applied 8-component rubric from `07_prompts/beta_execution_prompt.md` |
| Decision record emission | `decisions/record` via DEE | NO — depends on EO persistence | Substituted by `fit_score_report.md` documentation of reason codes |
| Deal economics modeling | `POST ppeme /v1/multipli/deal-economics` | NO — endpoint not yet built | Hand-applied scenario math from `06_data_models/deal_economics_model.json` baseline |
| Proposal language generation | DEE + LLM router via gateway `/v1/llm/call` | LLM router IS live (`openai-api-key` version 1 ACTIVE since 2026-05-22) but the DEE proposal-language route not yet wired | Composed manually with compliance discipline (no guarantees, scenarios only) |
| Dashboard event emission | Pub/Sub `gignet-orchestrator` topic | Topic exists; `vendor.financing.assessed.v1` event type not yet registered in HME | JSON payload written to bundle file for later HME ingestion |
| Engine health verification | gateway `/v1/healthz` | YES (`aggregate_status: ok, 11/11 engines`) | Confirmed at 2026-05-25T19:48Z |

**Net result.** Zero engine code shipped for this sprint; bundle produced entirely by hand. The 6 deliverables faithfully follow the package's schemas + scoring rubric + compliance constraints. When Phase A-B PRs land (slipped beyond the 4-day window — see §5), the bundle is regenerable end-to-end via curl.

## 3. Key Calendly findings

| Finding | Implication for Multipli |
|---|---|
| Calendly publishes 16% annual-vs-monthly discount; sales reps observed offering additional 15-25% concessions at quarter end | Financing can REPLACE that discount with a buyer-paid financing fee, preserving Calendly margin |
| Mid-market buyers commonly request monthly or quarterly billing instead of annual prepay | Direct match to Multipli's core financing thesis |
| Enterprise tier has 60-90 day sales cycles with procurement-induced friction | Financing historically compresses such cycles 20-40% |
| Bundleable services (onboarding, SSO provisioning, admin setup, premium support) | Expands financed contract value beyond raw seat license |
| Competitive pressure from Microsoft Bookings + Google Appointment Schedule (free with productivity suites) | Increases Calendly's incentive to offer differentiated buying experience (e.g., financing) |
| 2025-2026 CFO cost-rationalization environment | Increases buyer side payment-friction → favorable Multipli demand environment |

## 4. Key gaps / what to validate before Calendly- or Ben-Cahir-facing language

(Same list appears in `vendor_opportunity_profile.json` `missing_information` field; reproduced here for executive summary.)

1. Calendly actual ARR breakdown by tier (Team / Enterprise / Free).
2. Calendly actual close rates by segment and motion type.
3. Calendly actual blended ACV (this bundle models $18k — could be off by 2x in either direction).
4. Calendly actual discount % realized at close.
5. Calendly actual payment-term distribution (annual vs. monthly vs. quarterly).
6. Calendly internal POV on top 3 buyer objections.
7. **GO/NO-GO question:** Calendly appetite to introduce a third-party financing option (Multipli) at point of sale.
8. Multipli's actual realized take-rate on software/SaaS segment historically.
9. Multipli's actual realized default rate on software/SaaS segment.
10. Gigaton × Multipli commercial rev-share percentage (currently placeholder).

## 5. Sprint status vs. Tuesday deadline

**Phase A (engine code, Sat 5/23).** NOT STARTED. Zero engine code shipped.
**Phase B (engine code, Sun 5/24).** NOT STARTED.
**Phase C (FE + dashboard, Mon 5/25).** NOT STARTED.
**Phase D-E (Tue 5/26).** Sample bundles produced by hand (this artifact + Loom + Notion to follow).

**Interpretation.** The 4-day engine-build path slipped — likely because the parallel beta-launch sprint (16 PRs merged 2026-05-22) absorbed bandwidth. The runbook anticipated this risk in §9: "4-day window slips → cut scope ruthlessly: the 6 output files are the deliverable; everything else is supporting." That guidance was followed. The 6-file bundle exists and is internal-readiness-grade by EOD Tue 5/26. The engines that would generate it programmatically come later — recommend re-planning Phase A-B for week of 2026-06-01 once the GCP migration kickoff (planned Wed 5/27 evening per `[[gcp_engine_migration_accelerated_2026_05_25]]`) settles.

## 6. Implementation issues discovered

1. **`intel-silo` `eo_type` enum lacks `vendor`.** Confirmed via curl 2026-05-25T19:48Z. Migration 033 per runbook §4 needs to land before any programmatic vendor EO capture works.
2. **No `prospect_id` first-class tag yet.** The current intel-silo EO model accepts arbitrary JSONB tags, so `prospect_id=multipli` works as a tag, but it's not validated or queryable as a first-class field. Phase A migration should consider promoting it.
3. **No `vendor_opportunity` JSONB column on `ethnographic_objects`.** Per runbook §4, this is a planned migration. Until landed, vendor_opportunity data lives only in bundle artifact files.
4. **DEE proposal-language route not wired into LLM router.** The router is alive (OpenAI key live since 2026-05-22), but no decision-engine endpoint composes vendor-financing pitch language via the router. Phase C scope.
5. **HME does not register `vendor.financing.assessed.v1` event type.** Phase C scope.

## 7. Recommended immediate next actions

| Priority | Action | Owner | When |
|---|---|---|---|
| P0 | Todd reviews this bundle for compliance + factual accuracy + tone | Todd | Tue 2026-05-26 morning |
| P0 | Produce sample bundle #2 (Loom) and #3 (Notion) using the recipe at `runbooks/2026_05_25_multipli_bundle_manual_production_recipe.md` | Claude or sibling agent | Tue 2026-05-26 afternoon |
| P1 | Decide whether the 3-bundle hand-produced set is sufficient for the planned Ben Cahir outreach (per Assumption 1, polish level is internal-readiness — Ben sees nothing Tuesday) | Todd | Tue 2026-05-26 EOD |
| P1 | Replan Phase A-B engine work for week of 2026-06-01 after Wed 5/27 GCP migration kickoff settles | Todd + Claude | Wed-Thu 2026-05-28 |
| P2 | If Calendly conversation goes ahead, validate the 10 missing-info items in §4 before second draft of `proposal_recommendation.md` | Todd or sales agent | Post Calendly call |
| P2 | If Multipli/Ben outreach goes ahead, redact performance-share placeholders (Gigaton 15% of Multipli net revenue) from any external version | Todd | Pre-outreach |

## 8. Confidence and final compliance check

**Bundle confidence.** 0.62 (capped by public-source-only data). Acceptable for internal readiness; insufficient for external commitment language.

**Compliance check (package §9).** This bundle:
- Uses **scenario ranges** for all economic projections.
- Uses **"estimated", "modeled", "illustrative"** qualifiers throughout.
- Contains **NO guaranteed close-rate language.**
- Contains **NO firm financing terms** ("you will be approved for $X at Y% over Z months").
- Contains **NO specific buyer commitment language** ("Calendly buyer Acme Co. will close at $50k financed").
- Reviewed by author for `guaranteed | approved | will receive | will be funded | commit to` patterns — none present in any external-candidate section.

**Status.** Ready for Todd review. Not ready for Calendly. Not ready for Ben Cahir.
