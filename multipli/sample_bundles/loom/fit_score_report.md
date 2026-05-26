# Loom — Multipli Vendor Financing Fit Score Report

```ppim-signature
interaction: prospect_outreach_evidence_attachment
economics: scoring_function_inputs_drive_take_rate_scenarios_in_deal_economics_model
predictability: deterministic_8_component_weighted_sum_with_explicit_reason_codes_and_missing_field_list
brand_dimension: vendor_growth_acquisition_intelligence
lifecycle: acquisition_stage_second_artifact_of_six_file_bundle
```

**Vendor.** Loom (Atlassian subsidiary) (`loom_v1`)
**Vertical.** `software_saas` (Multipli declared top segment)
**Generated.** 2026-05-26T15:30:00Z
**Generator.** `gigaton_multipli_vendor_growth_engine_manual_v0` (hand-driven; no engine state)
**Status.** Internal-readiness draft. NOT for Ben Cahir without Todd review per Assumption 1.

---

## Headline

| Metric | Value |
|---|---|
| **Fit Score** | **77 / 100** |
| **Label** | **`high_fit`** (threshold: 70-100) |
| **Confidence** | 0.60 (capped — public-source-derived inputs; 2 points below Calendly due to Atlassian post-acquisition pricing uncertainty) |
| **Recommended Next Action** | Invite Loom (likely routing through Atlassian finance) into the Multipli SaaS-financing pilot workflow as a Business+AI / Enterprise-tier design partner. Validate inputs against Loom's actual contract data before committing pricing language. Recognize that decision authority on third-party financing may now sit at Atlassian rather than at the Loom BU. |

---

## Component Scores (8-component weighted, per `07_prompts/beta_execution_prompt.md`)

| # | Component | Max | Awarded | Reason Codes |
|---|---|---|---|---|
| 1 | Deal size suitability | 20 | **15** | `reason:deal_size_mid_upper_range` — $22k blended ACV lands inside Multipli's $28k baseline assumption (closer than Calendly's $18k) due to AI addon uplift and enterprise tier weight. Still below the SaaS example $62k vendor payout. Eligible and reasonably headline-worthy. |
| 2 | Payment friction | 20 | **14** | `reason:compound_annual_prepay_plus_ai_addon_friction` — score 68/100 reflects documented mid-market resistance to annual prepay PLUS AI addon stacking effect that lifts ACV 15-40% above baseline. Higher friction than Calendly. |
| 3 | Vendor segment fit | 15 | **14** | `reason:top_declared_segment` — Multipli explicitly names `software_saas` as a top vertical (alongside IT/telco, clean energy, commercial equipment). Loom is a canonical async-collaboration SaaS. |
| 4 | Buyer urgency | 10 | **6** | `reason:cost_optimization_pressure_moderate_plus_ai_skepticism` — 2025-2026 CFO cost-rationalization environment increases procurement scrutiny; AI addon line item draws extra finance attention. Not a forcing function for financing adoption. |
| 5 | Bundleable services | 10 | **9** | `reason:multiple_service_lines_documented_plus_atlassian_integration_consulting` — onboarding, SSO/SCIM, data residency setup, AI governance configuration, and Atlassian integration consulting are all distinct service lines that can be folded into a financed total contract value. Slightly richer than Calendly's bundleable surface. |
| 6 | Sales-cycle improvement | 10 | **9** | `reason:enterprise_cycle_75_to_120_days_compressible` — financing at point of sale historically shortens enterprise procurement cycles by 20-40% by removing the annual-prepay budget-cycle objection. Loom's video data residency + AI training disclosure adds 15-30 days vs non-video SaaS, giving financing more room to compress. |
| 7 | Margin/discount protection | 10 | **8** | `reason:discount_displaced_by_financing_option_plus_atlassian_bundle_pressure` — Loom is observed offering 15-25% discount to close at quarter end PLUS Atlassian-bundle co-term concessions; financing converts that margin loss into a buyer-paid financing fee, preserving vendor margin. |
| 8 | Data confidence | 5 | **2** | `reason:confidence_below_0_65_threshold_atlassian_uncertainty` — all input values are LLM-modeled from public sources; no Loom- or Atlassian-confirmed data. Post-acquisition pricing evolution adds extra uncertainty. Subtracts 3 points (vs. 2 for Calendly). |
| | **TOTAL** | **100** | **77** | |

---

## Reason Code Summary (top contributors)

**Strongest positives.**
1. `reason:top_declared_segment` (+14) — Loom is a textbook match for Multipli's `software_saas` segment declaration.
2. `reason:compound_annual_prepay_plus_ai_addon_friction` (+14) — Two stacked friction signals: annual-prepay norm AND the AI addon lift, creating a buyer-side budget-cycle squeeze that financing directly relieves. Slightly higher leverage than Calendly's single annual-prepay friction.
3. `reason:enterprise_cycle_75_to_120_days_compressible` (+9) — Video data residency + AI training data disclosure stretches the enterprise procurement cycle beyond Calendly's 60-90 days, giving Multipli more cycle to compress and more buyer pain to relieve.
4. `reason:multiple_service_lines_documented_plus_atlassian_integration_consulting` (+9) — Atlassian integration consulting is a net-new bundleable service line beyond what Calendly offers, expanding financed contract value ceiling.

**Strongest negatives.**
1. `reason:confidence_below_0_65_threshold_atlassian_uncertainty` (-3 vs. max) — Until Loom- or Atlassian-confirmed data is loaded, fit score is provisional. The Atlassian acquisition introduces additional uncertainty about future pricing/packaging that capped confidence below the Calendly baseline.
2. `reason:cost_optimization_pressure_moderate_plus_ai_skepticism` (-4 vs. max) — AI addon line items currently attract disproportionate CFO scrutiny in the 2025-2026 cost-rationalization environment.

---

## Missing-Information List (gate items before Ben Cahir-facing language)

1. Loom actual ARR breakdown by tier (Starter Free / Business / Business+AI / Enterprise).
2. Loom actual mid-market and enterprise close rates.
3. Loom actual AI addon attach rate at Business and Enterprise tiers.
4. Loom actual discount percentage realized at close vs. list (and how that interacts with Atlassian co-term bundle discounting).
5. Loom actual annual-vs-monthly-vs-quarterly payment term distribution.
6. Loom internal POV on top 3 buyer objections (vs. inferred from G2/Capterra).
7. Loom's appetite to introduce a third-party financing option (Multipli) at point of sale — note this **decision authority likely shifted to Atlassian finance post-acquisition**; identifying the right counterparty is part of the GO/NO-GO question.
8. Atlassian finance policy on third-party financing attached to subsidiary product revenue.
9. Competitive displacement rate against Microsoft Stream, Zoom Clips, Google Meet Recording, Vidyard, Free­Cam.
10. Loom's existing payment-plan or PO-based extended-term offering (if any) and its uptake rate.
11. Whether Loom is being repackaged as part of an Atlassian premium tier (would change deal-size base entirely).

---

## Recommended Sales Angle

> "Loom's Business+AI and Enterprise motion already gives 15-25% discount at quarter end to close annual prepay deals — and post-Atlassian acquisition, those buyers increasingly stack Loom onto Jira/Confluence co-terms with additional bundle concessions. Multipli's vendor financing converts those discount losses into a buyer-paid financing fee — preserving Loom (and Atlassian) margin, accelerating procurement cycles by 20-40% on a 75-120 day enterprise cycle (longer than Calendly's, with more room to compress), and turning bundled onboarding + SSO/SCIM + data residency + Atlassian integration consulting into a single financed contract. The fit score is `high_fit` (77/100) on declared-segment match, compound payment friction (annual-prepay + AI addon stacking), and richest bundleable-services surface of the 3 sample vendors. Recommended next step: a 30-minute design-partner conversation with Loom AND with Atlassian finance (parallel) to validate inputs against Loom's actual contract data and explore a 90-day Business+AI / Enterprise-tier pilot."

(Compliance note per package §9: no guaranteed close rate, no firm financing terms, no dollar promise. All ranges are scenario-derived. Reviewed by Todd before any Loom-, Atlassian-, or Ben-facing send.)

---

## Engine-Routing Trace (what would have run if Phase A-B endpoints existed)

| Step | Engine | Endpoint (planned per runbook §4-5) | Status |
|---|---|---|---|
| 1 | intelligence-silo | `POST /v1/multipli/vendor-intake` | NOT YET DEPLOYED — migration 033 not landed; eo_type enum does not include `vendor`. Used manual LLM extraction. |
| 2 | decision-engine | `POST /v1/multipli/vendor-fit-score` | NOT YET DEPLOYED — used the package's 8-component rubric by hand. |
| 3 | decision-engine (DEE) | `Decision record emit` | NOT YET WIRED — would have written to `decisions/record` once vendor EO was persisted. |
| 4 | ppeme | `POST /v1/multipli/deal-economics` | NOT YET DEPLOYED — see file 3 `deal_economics_model.json` for the modeled output. |

When Phase A-B PRs ship (Sat 5/30 → Mon 6/1 latest, given the holiday-week slip), this bundle will be regenerable end-to-end via curl rather than by hand.
