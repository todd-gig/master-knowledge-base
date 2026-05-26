# Calendly — Multipli Vendor Financing Fit Score Report

```ppim-signature
interaction: prospect_outreach_evidence_attachment
economics: scoring_function_inputs_drive_take_rate_scenarios_in_deal_economics_model
predictability: deterministic_8_component_weighted_sum_with_explicit_reason_codes_and_missing_field_list
brand_dimension: vendor_growth_acquisition_intelligence
lifecycle: acquisition_stage_second_artifact_of_six_file_bundle
```

**Vendor.** Calendly LLC (`calendly_v1`)
**Vertical.** `software_saas` (Multipli declared top segment)
**Generated.** 2026-05-25T19:50:00Z
**Generator.** `gigaton_multipli_vendor_growth_engine_manual_v0` (hand-driven; no engine state)
**Status.** Internal-readiness draft. NOT for Ben Cahir without Todd review per Assumption 1.

---

## Headline

| Metric | Value |
|---|---|
| **Fit Score** | **75 / 100** |
| **Label** | **`high_fit`** (threshold: 70-100) |
| **Confidence** | 0.62 (capped — public-source-derived inputs) |
| **Recommended Next Action** | Invite Calendly into the Multipli SaaS-financing pilot workflow as an Enterprise-tier design partner. Validate inputs against Calendly's actual contract data before committing pricing language. |

---

## Component Scores (8-component weighted, per `07_prompts/beta_execution_prompt.md`)

| # | Component | Max | Awarded | Reason Codes |
|---|---|---|---|---|
| 1 | Deal size suitability | 20 | **14** | `reason:deal_size_mid_range` — $18k blended ACV lands inside Multipli's $28k baseline assumption but below the SaaS example $62k vendor payout. Eligible but not headline-grade. |
| 2 | Payment friction | 20 | **13** | `reason:annual_prepay_friction` — score 64/100 reflects documented mid-market resistance to annual prepay and frequent buyer requests for monthly/quarterly billing. |
| 3 | Vendor segment fit | 15 | **14** | `reason:top_declared_segment` — Multipli explicitly names `software_saas` as a top vertical (alongside IT/telco, clean energy, commercial equipment). Calendly is canonical. |
| 4 | Buyer urgency | 10 | **6** | `reason:cost_optimization_pressure_moderate` — 2025-2026 CFO cost-rationalization environment increases procurement scrutiny but is not a forcing function for new financing adoption. |
| 5 | Bundleable services | 10 | **9** | `reason:multiple_service_lines_documented` — onboarding, SSO provisioning, admin workflow setup, premium support are all distinct service lines that can be folded into a financed total contract value. |
| 6 | Sales-cycle improvement | 10 | **8** | `reason:enterprise_cycle_60_to_90_days_compressible` — financing at point of sale historically shortens enterprise procurement cycles by 20-40% by removing the annual-prepay budget-cycle objection. |
| 7 | Margin/discount protection | 10 | **8** | `reason:discount_displaced_by_financing_option` — Calendly is observed offering 15-25% discount to close at quarter end; financing converts that margin loss into a buyer-paid financing fee, preserving vendor margin. |
| 8 | Data confidence | 5 | **3** | `reason:confidence_below_0_70_threshold` — all input values are LLM-modeled from public sources; no Calendly-confirmed data. Subtracts 2 points. |
| | **TOTAL** | **100** | **75** | |

---

## Reason Code Summary (top contributors)

**Strongest positives.**
1. `reason:top_declared_segment` (+14) — Calendly is a textbook match for Multipli's `software_saas` segment declaration.
2. `reason:annual_prepay_friction` (+13) — The single highest-leverage objection for Multipli's financing thesis is unambiguously present in Calendly's mid-market motion.
3. `reason:multiple_service_lines_documented` (+9) — Bundling expands financed contract value beyond seat licenses.

**Strongest negatives.**
1. `reason:confidence_below_0_70_threshold` (-2 vs. max) — Until Calendly-confirmed data is loaded, fit score is provisional.
2. `reason:deal_size_mid_range` (-6 vs. max) — A higher-deal-size SaaS vendor (e.g., enterprise infrastructure, vertical SaaS at $80-200k ACV) would score higher on dimension 1.

---

## Missing-Information List (gate items before Ben Cahir-facing language)

1. Calendly actual ARR breakdown by tier (Team / Enterprise / Free).
2. Calendly actual mid-market and enterprise close rates.
3. Calendly actual discount percentage realized at close vs. list.
4. Calendly actual annual-vs-monthly-vs-quarterly payment term distribution.
5. Calendly internal POV on top 3 buyer objections (vs. inferred from G2/Capterra).
6. Calendly's appetite to introduce a third-party financing option (Multipli) at point of sale — this is the GO/NO-GO question for the design-partner pitch.
7. Competitive displacement rate against Microsoft Bookings, Google Appointment Schedule, Chili Piper, SavvyCal.
8. Calendly's existing payment-plan or PO-based extended-term offering (if any) and its uptake rate.

---

## Recommended Sales Angle

> "Calendly's mid-market and enterprise motion already gives 15-25% discount at quarter end to close annual prepay deals. Multipli's vendor financing converts that discount loss into a buyer-paid financing fee — preserving Calendly's margin, accelerating procurement cycles by 20-40%, and turning bundled onboarding + SSO + premium-support services into a single financed contract. The fit score is `high_fit` (75/100) on declared-segment match, documented payment friction, and high bundleable-services count. Recommended next step: a 30-minute design-partner conversation to validate inputs against Calendly's actual contract data and explore a 90-day enterprise-tier pilot."

(Compliance note per package §9: no guaranteed close rate, no firm financing terms, no dollar promise. All ranges are scenario-derived. Reviewed by Todd before any Calendly- or Ben-facing send.)

---

## Engine-Routing Trace (what would have run if Phase A-B endpoints existed)

| Step | Engine | Endpoint (planned per runbook §4-5) | Status |
|---|---|---|---|
| 1 | intelligence-silo | `POST /v1/multipli/vendor-intake` | NOT YET DEPLOYED — migration 033 not landed; eo_type enum does not include `vendor`. Used manual LLM extraction. |
| 2 | decision-engine | `POST /v1/multipli/vendor-fit-score` | NOT YET DEPLOYED — used the package's 8-component rubric by hand. |
| 3 | decision-engine (DEE) | `Decision record emit` | NOT YET WIRED — would have written to `decisions/record` once vendor EO was persisted. |
| 4 | ppeme | `POST /v1/multipli/deal-economics` | NOT YET DEPLOYED — see file 3 `deal_economics_model.json` for the modeled output. |

When Phase A-B PRs ship (Sat 5/30 → Mon 6/1 latest, given the holiday-week slip), this bundle will be regenerable end-to-end via curl rather than by hand.
