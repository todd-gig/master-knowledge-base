# Multipli Vendor Bundle — Manual Production Recipe

**Date.** 2026-05-25 (Mon)
**Author.** Claude (manual hand-driven production for sprint deadline 2026-05-26)
**Purpose.** Reproducible step-by-step recipe for generating one full 6-file Multipli vendor bundle by hand, used because Phase A-B engine endpoints (per `runbooks/2026_05_22_multipli_vendor_growth_engine_4day_sprint.md` §4-5) have NOT shipped before the EOD-Tuesday deadline.
**Reference output.** `master-knowledge-base/multipli/sample_bundles/calendly/` — produced via this recipe on 2026-05-25 ~14:45-16:15 CT (~90 min total).
**Out of scope.** This recipe is a stopgap. Once Phase A-B PRs land (revised target week of 2026-06-01), prefer the curl-driven engine path over the hand-driven path documented here.

---

## 0. Pre-flight (5 min)

Confirm engines are live and confirm the planned multipli endpoints are NOT yet deployed (so we know we still need the manual path).

```bash
# Confirm 11/11 engines healthy
curl -s -m 5 https://gigaton-platform.web.app/v1/healthz | python3 -c "import sys, json; d = json.load(sys.stdin); print(d['aggregate_status'], d['ok_count'], '/', d['total_count'])"
# Expected: "ok 11 / 11"

# Confirm vendor EO type still rejected (i.e., Phase A migration 033 not landed)
curl -s -m 5 -X POST -H "Content-Type: application/json" \
  -d '{"eo_type":"vendor","name":"probe","canonical_name":"probe"}' \
  https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/v1/eo \
  -w "\nHTTP:%{http_code}\n" | head -5
# Expected: 422 with literal_error citing the existing enum (no `vendor` value)
# If status is 200, the migration LANDED — switch to the engine path, not this recipe.
```

If both checks pass, proceed with the manual recipe below.

## 1. Pick the vendor (5 min)

Pick from the candidate set: **Loom**, **Notion**, **Calendly** (already done), or a new SaaS vendor with all of:
- Publicly disclosed pricing tiers
- Mid-market and enterprise motion (not pure-self-serve)
- Documented bundleable services (onboarding / training / SSO / premium support)
- Sales cycle in the 14-90 day range
- Annual prepay or extended-term payment pattern

**One-line justification.** Write one sentence explaining why this vendor fits the Multipli software_saas thesis. Save the sentence for the `notes` field in `vendor_opportunity_profile.json`.

## 2. Gather public sources (15 min)

Cite URL + observed-at for every input. Sources to consult (in priority order):

1. **Vendor pricing page** (e.g., `https://<vendor>.com/pricing`) — gives list price, tier names, discount disclosures, payment-term language.
2. **Vendor enterprise/business page** — gives bundleable service inventory (onboarding, SSO, premium support).
3. **G2 reviews** (`https://www.g2.com/products/<vendor>/reviews`) — gives buyer objections, perceived friction, competitive context.
4. **Capterra reviews** — same as G2.
5. **SEC filings if public** — gives actual ARR, ACV, segment breakdown, gross margin. Skip if vendor is private.
6. **Vendor blog or partner page** — sometimes discloses customer count, segment distribution, partner ecosystem.
7. **Industry benchmarks** (Gartner / Forrester / SaaStr) — for gross margin norms, close-rate norms, sales-cycle norms by SaaS segment.

Per doctrine `[[feedback_web_search_for_data_backfill]]`: default to authoritative public sources BEFORE asking the user. Cite URL + observed-at on every numeric input. Flag conflicts.

## 3. Build the `vendor_opportunity_profile.json` (15 min)

Start from the Calendly profile as a template. Schema reference: `~/Downloads/multipli_claude_beta_package/06_data_models/vendor_opportunity.schema.json`.

For each field, supply both the value AND a `_<field>_basis` sibling field documenting the public-source-derived reasoning. This is non-negotiable — without basis, the confidence score should be capped low and the field should appear in `missing_information`.

**Required fields** (from schema): `vendor_id`, `vertical`, `average_deal_size`, `payment_friction_score`.
**Optional fields**: `vendor_name`, `geography`, `product_service`, `gross_margin_estimate`, `current_close_rate`, `sales_cycle_days`, `discounting_to_close`, `extended_terms_requested`, `implementation_services_bundleable`, `buyer_objections`, `confidence`, `notes`.

**Multi-axis tenant tags** (per `[[foundational_modular_replication_via_input_substitution]]`): industry / sub_vertical / geo / regime / segment / lifecycle / provenance / modality.

**PPIM signature block** (per `[[foundational_goal_gigaton_engineered_brand_experience]]`): interaction / economics / predictability / brand_dimension / lifecycle.

**Compliance flag**: `do_not_quote_to_prospect_without_human_review: true`.

**Confidence cap**: 0.65 if all inputs are public-source-derived (no vendor confirmation). 0.85 only if vendor confirms at least 4 of: ARR, ACV, close rate, payment terms, top objections.

## 4. Compute the fit score (10 min)

Apply the 8-component rubric verbatim from `~/Downloads/multipli_claude_beta_package/07_prompts/beta_execution_prompt.md`:

| Component | Max | How to score |
|---|---|---|
| Deal size suitability | 20 | $28k+ ACV = 18-20; $15-28k = 10-17; $5-15k = 5-10; <$5k = 0-5 |
| Payment friction | 20 | `payment_friction_score / 100 * 20` (so 64/100 → 12.8, round 13) |
| Vendor segment fit | 15 | software_saas / it_telco / clean_energy / commercial_equipment = 13-15; "other" = 5-10 |
| Buyer urgency | 10 | Strong forcing-function (regulation / compliance / quarter-end) = 8-10; moderate (cost optimization) = 5-7; weak = 2-4 |
| Bundleable services | 10 | Multiple service lines documented = 8-10; one line = 5-7; none = 0-3 |
| Sales-cycle improvement | 10 | 60-90 day cycle = 8-10; 30-60 day = 6-8; 14-30 day = 4-6; <14 day = 0-3 |
| Margin/discount protection | 10 | `discounting_to_close=true` + observable discount pattern = 8-10; sometimes = 5-7; never = 0-3 |
| Data confidence | 5 | confidence >= 0.85 = 5; 0.70-0.85 = 4; 0.55-0.70 = 3; 0.40-0.55 = 2; <0.40 = 1 |

**Label thresholds**: 70-100 = `high_fit`, 50-69 = `medium_fit`, 0-49 = `low_fit`.

**Reason codes**: emit one per component, e.g. `reason:top_declared_segment`, `reason:annual_prepay_friction`, `reason:enterprise_cycle_60_to_90_days_compressible`, `reason:bundleable`, `reason:confidence_below_0_70_threshold`. Reason codes form the audit trail; never omit.

Write the `fit_score_report.md` using the Calendly file as a template. Include the engine-routing trace section ("what would have run if Phase A-B endpoints existed").

## 5. Compute deal economics (10 min)

Reference: `~/Downloads/multipli_claude_beta_package/06_data_models/deal_economics_model.json`.

**Baseline assumptions to carry forward verbatim** (do not modify):
- `package_baseline_average_funded_contract_value_usd: 28260`
- `package_conservative_average_funded_contract_value_usd: 28000`
- `package_saas_example_vendor_payout_usd: 62000`
- `package_saas_example_customer_payment_total_usd: 72000`
- `package_gross_spread_pool_per_deal_usd: 10000`
- Six take-rate scenarios: 3%, 5%, 8%, 10%, 12%, 16%

**Vendor-specific computation**:
1. `vendor_blended_acv` = your modeled value from §3.
2. `vendor_pilot_assumed_financed_deals_per_quarter` = pilot scale (default 50 conservative / 100 optimistic).
3. `incremental_funded_volume_year_1_conservative` = `vendor_blended_acv * 50 * 4`.
4. `incremental_funded_volume_year_1_optimistic` = `vendor_blended_acv * 100 * 4`.
5. For each take_rate in [0.03, 0.05, 0.08, 0.10, 0.12, 0.16]:
   - `estimated_net_revenue_conservative = incremental_funded_volume_conservative * take_rate`
   - `estimated_net_revenue_optimistic = incremental_funded_volume_optimistic * take_rate`
6. `gross_spread_pool_per_deal_modeled` = `10000 * (vendor_blended_acv / 28000)`, then reduce ~40% for thinner-spread categories (lower-ACV SaaS). Document the reduction reasoning.
7. `draw_repayment_projection`: avg term 12 months; modeled completion 0.90-0.95; default 0.02-0.05; prepay 0.03-0.08 depending on buyer credit assumption.
8. `performance_share_projection_to_gigaton`: 15% placeholder unless explicitly told otherwise. Mark redact-from-external.

**Carry the package warnings verbatim**, plus a vendor-specific warning that all numeric inputs are LLM-modeled from public sources.

## 6. Compose the proposal recommendation (15 min)

Use the Calendly `proposal_recommendation.md` structure:

1. One-sentence pitch
2. Why vendor fits the Multipli thesis (table mapping Multipli criterion ↔ vendor pattern ↔ source)
3. Pilot structure (90-day, ~50 financing-eligible opportunities, success metric bands)
4. Vendor economic upside (illustrative scenario)
5. Top buyer objections financing addresses
6. What Multipli gets out of the pilot
7. What vendor is asked to provide
8. Vendor-side risks
9. Asks of Ben Cahir (internal note — do not include in external version)
10. Status flags for internal review

**Compliance discipline (non-negotiable)**:
- NO `guaranteed | approved | will receive | will be funded | commit to` language anywhere.
- Use `estimated`, `modeled`, `illustrative`, `target band`, `pending validation`, `subject to pilot data`.
- Run a `grep -iE 'guarantee|approved|will receive|will be funded|commit to' proposal_recommendation.md` before declaring the file done.
- Flag performance-share figures (Gigaton 15% of Multipli net revenue) for redaction in any external version.

## 7. Build the dashboard event payload (5 min)

Schema reference: `~/Downloads/multipli_claude_beta_package/06_data_models/dashboard_event_payload.example.json`.

Add to that base:
- `event_schema_version: 1.0.0`
- `source_mode: manual_hand_driven_no_engine_emission_yet`
- `fit_score_components` object (the 8 component scores)
- `reason_codes_top` array (top 5)
- `estimated_incremental_funded_volume_usd` object with conservative + optimistic
- `estimated_net_revenue_scenarios_*` for both conservative and optimistic, all 6 take rates
- `prospect_id: multipli`, `operator_id: null`
- `attribution.ppim_action_chain` listing the 5 engine substitutions
- `ppim_signature_tags` (industry/sub_vertical/geo/regime/segment/lifecycle/provenance/modality)
- `_intended_consumers` array (HME / DEE / ppeme / FE)
- `_engine_routing_trace` (what would have emitted vs. what actually happened)
- `_compliance_flag: scenarios_only_no_guaranteed_outcomes_per_package_section_9_governance`

## 8. Write the beta test summary (10 min)

Use the Calendly `beta_test_summary.md` structure verbatim:

1. Executive summary (60 sec)
2. What this beta tested (list of 6 files)
3. What ran via live engines vs. what was hand-substituted (table)
4. Key vendor findings (table — finding ↔ implication for Multipli)
5. Key gaps to validate (mirror `missing_information` from profile)
6. Sprint status vs. Tuesday deadline (phase A/B/C status)
7. Implementation issues discovered (engine gaps observed)
8. Recommended immediate next actions (P0/P1/P2 table)
9. Confidence + final compliance check (run the grep)

## 9. Final pass (5 min)

For the entire bundle:

```bash
# Run compliance grep across all 6 files
cd /Users/admin/Documents/GitHub/master-knowledge-base/multipli/sample_bundles/<vendor>/
grep -iE 'guaranteed|approved|will receive|will be funded|commit to' *.json *.md
# Expected: no matches (or only inside compliance-discussion sentences that EXPLICITLY warn against them)

# Validate JSON files parse
for f in *.json; do python3 -m json.tool "$f" > /dev/null && echo "OK: $f" || echo "FAIL: $f"; done

# Verify each file has a PPIM signature block
for f in *.json *.md; do
  if grep -qE '_ppim_signature|ppim-signature' "$f"; then echo "OK: $f"; else echo "MISSING PPIM: $f"; fi
done
```

All three checks must pass.

## 10. Report to user

In ≤ 5 bullet points, report:
- Vendor chosen + 1-line justification
- 6 file paths
- Compliance grep result
- JSON validation result
- Time spent

---

## Quick reference: PPIM signature block template (use in every file)

For JSON:
```json
"_ppim_signature": {
  "interaction": "<role this artifact plays in the prospect interaction lifecycle>",
  "economics": "<what economic mechanism this artifact represents or measures>",
  "predictability": "<how the artifact's outputs are made auditable / explainable>",
  "brand_dimension": "vendor_growth_acquisition_intelligence",
  "lifecycle": "acquisition_stage_<n>th_artifact_of_six_file_bundle"
}
```

For Markdown:
````
```ppim-signature
interaction: <…>
economics: <…>
predictability: <…>
brand_dimension: vendor_growth_acquisition_intelligence
lifecycle: acquisition_stage_<n>th_artifact_of_six_file_bundle
```
````

## Estimated time for bundles 2 + 3

- Vendor selection + sources gathering: 20 min (some shared SaaS research carries across)
- Profile + scoring + economics: 35 min (uses Calendly as template — search/replace + recompute)
- Proposal + dashboard + summary: 25 min (same)
- Final pass: 5 min

**Total per vendor: ~85 min.** Two vendors: **~2h 50m.**

If a single agent runs both in sequence: schedule a 3-hour block. If two agents split the work: 90 min each in parallel.

## When to STOP using this recipe

The moment ANY of these become true:
1. Phase A migration 033 lands on intel-silo main (vendor EO type accepted). Re-run the §0 curl probe; if it returns 200, switch to the curl-driven engine path.
2. `decision-engine /v1/multipli/vendor-fit-score` endpoint deployed. Same — switch.
3. `ppeme /v1/multipli/deal-economics` endpoint deployed. Same — switch.

Once any one of these lands, retire the corresponding manual step and use the engine. The recipe should fully retire once all three are live.
