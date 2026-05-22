# Multipli Vendor Growth Engine — 4-day sprint to EOD Tuesday 2026-05-26

**Date.** 2026-05-22 (Friday)
**Deadline.** EOD Tuesday 2026-05-26
**Owner.** todd@gigaton.ai (approval); Claude (implementation)
**Status.** PLAN — awaiting 3 blocking-question answers, then execute.
**Risk class.** MEDIUM (new prospect-facing surface; 4-day window is tight; reuses existing engines so blast radius bounded).
**Source package.** `~/Downloads/multipli_claude_beta_package/` — 14 docs, version 1.0.0, ingested 2026-05-22.

---

## 0. What this is

A **Vendor Growth Engine for prospect Multipli** (vendor-financing company, CEO NA+EU = Ben Cahir; $650M financed across 23k contracts; SaaS/IT-telco/clean-energy/equipment public segments). Gigaton's pitch: build the performance infrastructure (vendor education, ROI calculators, buyer objection handling, fit scoring, proposal generation, attribution) around Multipli's existing financing product. Not a replacement; an augmentation layer.

By EOD Tuesday: the engine produces, for each of 3 sample vendors captured manually Tuesday afternoon, the 6 deliverable files:

1. `vendor_opportunity_profile.json`
2. `fit_score_report.md`
3. `deal_economics_model.json`
4. `proposal_recommendation.md`
5. `dashboard_event_payload.json`
6. `beta_test_summary.md`

That output bundle is what gives the Ben Cahir outreach a concrete demonstration to point at.

## 0.1 Critical context — this sprint is downstream of a bigger launch

Discovered 2026-05-22 evening: there is a parallel sprint shipping the **Gigaton + Ti Solutions Product & Service Package** with **beta launch Monday 2026-05-25** ([[product_service_package_gigaton_ti_solutions]]). That package is the **GTM wrapper** — a joint Gigaton (SaaS) + Ti Solutions (managed-service) offering covering the full lifecycle: **Acquisition → Marketing → Sales → Integrated Brand Experience + Interaction Management**.

**The Multipli sprint is the first concrete use case of that package.** Sequence:
- **Mon 5/25** — Package beta LAUNCHES (internal readiness; engines × wrapper bundled).
- **Tue 5/26 EOD** — Multipli vendor-growth output bundle = first prospect-ready instantiation of the package.

**Assumption 1 REVISED.** Tuesday output IS Ben-facing (or near-Ben-facing). Polish level: **prospect-demonstration quality**, not internal readiness. The output bundle gets attached to the outreach email Ben Cahir receives.

**This sprint must NOT duplicate package engine work.** The package already maps the 4 lifecycle stages to the existing engines (intel-silo / decision-engine + ppeme + HME / sales-operating-system + decision-engine / UAE + gateway + persona-engine + HME). My distribution per §1 below matches the package mapping exactly — by design, not coincidence. Reinforces "do not create new module."

**Operator-context driven, no hardcoded `gigaton-internal` IDs.** Per the package's anti-hardcoding rule. Multipli's prospect work uses `prospect_id=multipli` tag throughout; the same routes will accept `operator_id` once they sign and become a real client_namespace.

---

## 1. Critical architectural decision — distribute, do not create new module

The package proposes a module named `vendor_financing_growth_engine`. **This plan rejects that and distributes the work across existing engines per concern.** Reasons:

1. The package's own non-negotiable instruction is "do not create duplicate systems / contradictory data models / redundant dashboards."
2. Every function the package asks for already has a home in an existing engine.
3. Creating a 10th engine for one prospect violates [[universal_connector_hub_architecture]] and the Gigaton anti-pattern doctrine.

### Engine assignment

| Multipli function | Lives in | Why |
|---|---|---|
| Vendor intake schema + form | **gigaton-ui-system** (FE) + **intelligence-silo** (EO) | Extends EO System with `eo_type=vendor` enum; form follows existing onboarding form patterns |
| Vendor as EO record | **intelligence-silo** `eo` table | Multi-axis JSONB tags handle vertical/geo/segment; no new table |
| Fit scoring (8-component weighted) | **decision-engine** | Doctrine scoring with reason codes is decision-engine's purpose |
| Deal economics modeling (6 take-rate scenarios) | **ppeme** | Profitability modeling is ppeme's purpose; aligns with BFT calculator + Experience Engineering Equation |
| Proposal recommendation generation | **decision-engine** (Decision Execution Engine) + **gigaton-ui-system** (rendering) | DEE produces the recommendation; FE renders it |
| Attribution event | **decision-engine** (Execution Record) + **ppeme** (Penrose `super_additive_network_value`) | Already exists; just emit |
| Dashboard event payload | **Pub/Sub `gignet-orchestrator`** + **HME** (event types) | Phases A-G fabric is the canonical way; add `vendor.financing.assessed.*` event type |
| Multipli as a prospect (not yet operator) | **NEW lightweight table** in intel-silo or decision-engine | Do NOT add to UAE `client_namespaces` yet — they haven't signed |

### What this means

- **Zero new repos.** Zero new Cloud Run services. One new shared module concept distributed as endpoints on existing engines.
- Each engine that participates exposes one new route + one Pydantic model + one service method.
- The "Multipli Vendor Growth Engine" is a *workflow* across engines, not an *engine*. Documented in this runbook + tracked as a Gignet orchestrator task chain.

---

## 2. Assumptions I'm making in Auto Mode (call them out, redirect if wrong)

1. **Tuesday EOD = internal readiness deadline.** Demo to Ben happens later; Tuesday is when the system runs end-to-end against real captured data. Polish level: demonstration-quality, not production launch.
2. **Multipli is a PROSPECT, not yet an operator.** They have not signed. Do NOT seed `client_namespaces` for them. Carry `prospect_id=multipli` as a tag on records. Convert to operator namespace if/when they sign.
3. **Manual capture method = both UI form AND Google Sheet upload.** Build the form (extends existing intake patterns); also accept CSV upload at the same endpoint. Lowest friction for whoever captures the data.
4. **GCP project**: every engine that participates is already deployed in its existing project (`carmen-beach-properties` for decision-engine + intel-silo; `gigaton-platform` for HME + ppeme + gateway). Do NOT entangle with the long-term migration ([[gcp_project_organization_target_2026]]).
5. **Output bundle delivery**: the 6 files for each test vendor land in a GCS bucket `gs://gigaton-platform-multipli-beta/vendor_<id>/` plus a one-shot zip download from a gigaton-ui-system page. Plus emitted to `gignet-orchestrator` event for HME ingestion.
6. **No live Multipli CRM integration.** Manual data only. CRM hook is a Phase 2 item if/when Ben signs.

If any of those is wrong, redirect now — re-planning is cheap before Saturday.

---

## 3. Timeline (Fri 5/22 evening → Tue 5/26 EOD)

| Day | Work |
|---|---|
| **Fri 5/22 evening (TODAY)** | Plan committed. 3 blocking questions answered. Cloud SQL provisioning completes. Multipli + Ben Cahir captured in entity_ecosystem_registry as PROSPECT. |
| **Sat 5/23** | Phase A: intel-silo EO schema extension + intake endpoint + form scaffolding. |
| **Sun 5/24** | Phase B: decision-engine fit scoring endpoint + ppeme deal economics endpoint. Both with stubbed data tests. |
| **Mon 5/25** | Phase C: gigaton-ui-system intake page + proposal rendering + bundle download. Dashboard event emission wiring. End-to-end smoke against 3 synthetic vendors. |
| **Tue 5/26 morning** | Phase D: any rough-edge fixes from Sunday/Monday smoke. Final manual data capture by user (real vendor opportunities). |
| **Tue 5/26 afternoon** | Phase E: run beta against the 3 real vendors. Produce 6 output files per vendor. Land in GCS + zip download + dashboard event. |
| **Tue 5/26 EOD** | Bundle ready. `beta_test_summary.md` produced. Ready for Ben outreach attachment. |

---

## 4. Phase A — intel-silo EO schema + intake endpoint (Sat 5/23, ~5h)

| File | Change |
|---|---|
| `intelligence-silo/migrations/033_vendor_eo_extension.sql` (NEW) | Extends `ethnographic_objects.eo_type` enum with `vendor`. Adds `vendor_opportunity` JSONB column to capture the manual-intake fields (deal size / margin / friction score / objections / etc.) per `vendor_opportunity.schema.json`. Idempotent `IF NOT EXISTS`. |
| `intelligence-silo/core/eo/models.py` | Add Pydantic `VendorOpportunity` model matching the package schema (vendor_id / vendor_name / vertical enum / geography / product_service / average_deal_size / gross_margin_estimate / current_close_rate / sales_cycle_days / payment_friction_score / discounting_to_close / extended_terms_requested / implementation_services_bundleable / buyer_objections / confidence / notes). |
| `intelligence-silo/core/eo/endpoints.py` | Add `POST /v1/multipli/vendor-intake` — accepts JSON body or CSV upload, validates, creates EO row with `eo_type=vendor`, returns `vendor_id`. Add `GET /v1/multipli/vendor-intake/{vendor_id}` for retrieval. |
| `intelligence-silo/tests/test_multipli_intake.py` (NEW) | Schema validation + CSV upload + retrieval. 3 sample vendor fixtures from `04_beta_test/manual_capture_template.md`. |

**Deploy:** auto-deploy GHA on main merge (workflow already exists per PR #28).

---

## 5. Phase B — decision-engine fit scoring + ppeme deal economics (Sun 5/24, ~6h)

### decision-engine

| File | Change |
|---|---|
| `decision-engine/api/services/multipli_fit_scoring.py` (NEW) | `compute_fit_score(vendor_opportunity)` returns `(score, reason_codes, missing_fields)`. 8-component weighted scoring per `07_prompts/beta_execution_prompt.md`: deal_size 20 + payment_friction 20 + segment_fit 15 + buyer_urgency 10 + bundleable_services 10 + sales_cycle 10 + margin_protection 10 + data_confidence 5. Returns reason codes (`reason:high_deal_size`, `reason:bundleable`, etc.) for each contribution. |
| `decision-engine/api/routes/multipli.py` (NEW) | `POST /v1/multipli/vendor-fit-score` — body: `{vendor_id}`. Fetches EO from intel-silo (via existing cross-engine HTTP pattern), computes score, emits Decision record (DEE) for audit, returns `{score, label, reason_codes, missing_fields, confidence}`. Score-to-label: 0-49 low_fit / 50-69 medium_fit / 70-100 high_fit. |
| `decision-engine/tests/test_multipli_fit_scoring.py` (NEW) | Score boundaries, reason code emission, missing-field handling. |

### ppeme

| File | Change |
|---|---|
| `ppeme/app/services/multipli_deal_economics.py` (NEW) | `compute_scenarios(vendor_opportunity)` returns deal economics across 6 take-rate scenarios (0.03 / 0.05 / 0.08 / 0.10 / 0.12 / 0.16 per `06_data_models/deal_economics_model.json`). Outputs: `incremental_funded_volume`, `estimated_net_revenue_{low,mid,high}`, `gross_spread_pool`, `draw_repayment_projection`, `performance_share_projection`. Includes the package's warnings array verbatim. |
| `ppeme/app/routes/multipli.py` (NEW) | `POST /v1/multipli/deal-economics` — body: `{vendor_id, take_rate_overrides?}`. Fetches EO + fit score, computes scenarios, returns model + warnings. |
| `ppeme/tests/test_multipli_deal_economics.py` (NEW) | Scenario math, override handling, warning emission. |

**Deploy:** auto-deploy GHA on main merge for each repo.

---

## 6. Phase C — FE intake + rendering + dashboard wiring (Mon 5/25, ~7h)

| File | Change |
|---|---|
| `gigaton-ui-system/src/pages/multipli/IntakePage.tsx` (NEW) | At `/operators/multipli/intake`. Form mirrors `manual_capture_template.md` sections (Vendor Profile / Deal Economics / Financing Fit / Buyer Objections / Sales Process / Multipli Opportunity / Notes). Also offers "Upload CSV" button (single file or 3-row batch). Submits to intel-silo intake endpoint. |
| `gigaton-ui-system/src/pages/multipli/VendorListPage.tsx` (NEW) | At `/operators/multipli/vendors`. Lists captured vendors + their fit score + status. Action: "Run Beta Analysis" triggers decision-engine + ppeme + bundle. |
| `gigaton-ui-system/src/pages/multipli/ProposalPage.tsx` (NEW) | At `/operators/multipli/proposal/:vendor_id`. Renders fit score + reason codes + deal economics scenarios + proposal-ready language. Action: "Download Bundle" → zip of 6 output files. |
| `gigaton-ui-system/src/services/multipli.ts` (NEW) | Thin client for the new endpoints across intel-silo + decision-engine + ppeme. |
| `gigaton-ui-system/src/router.tsx` | Add 3 routes (intake / vendors / proposal). Founder + admin gated. |
| Pub/Sub `gignet-orchestrator` topic | New event types via existing schema: `vendor.financing.captured.v1`, `vendor.financing.assessed.v1`, `vendor.financing.proposed.v1`. Wired into existing fan-out (Phase B). |
| `human-management-engine/api/events.py` | Register the 3 new event types. |
| GCS bucket `gigaton-platform-multipli-beta` (NEW) | Holds the 6-file output bundles per vendor. Lifecycle: archive after 90d. |

**The recommended sales angle + objection responses** are generated by a small LLM-mediated step in `decision-engine/api/services/multipli_fit_scoring.py` using the LLM router (gateway POST `/v1/llm/call` per Phase D infrastructure). Prompt template baked in; output schema enforced.

---

## 7. Phase D-E — Tuesday execution

### Tue 5/26 morning
- Smoke run the end-to-end flow against 3 synthetic vendors. Fix any breakage from Mon evening.
- User completes final manual capture for 3 real vendor opportunities.

### Tue 5/26 afternoon
- Capture data lands via intake form or CSV upload.
- Run "Run Beta Analysis" for each vendor.
- 6 output files per vendor produced + bundled.
- `beta_test_summary.md` generated (executive summary + recommended next actions).
- HME emits dashboard event for each vendor.

### Tue 5/26 EOD
- Bundle accessible at `/operators/multipli/vendors` → "Download Beta Outputs" (all 18 files = 6 per vendor × 3 vendors).
- Penrose `super_additive_network_value` metric ticks up.
- Ben Cahir outreach can attach the bundle.

---

## 8. What's NOT in scope for the 4-day sprint

- Live Multipli CRM / `My Multipli` integration. Phase 2.
- Multipli as a billable Gigaton operator. Separate ADR; depends on Ben signing.
- Co-branded landing page / vendor acquisition campaign. The proposal_structure deliverable; needs Multipli sign-off.
- Real attribution rules (UTM / CRM source / workflow ID). Phase 2 with real campaigns.
- Compliance review by Multipli of financing claims. The package explicitly says no financing claims without Multipli review — proposal_recommendation.md text uses configurable assumptions only.
- Production polish for prospect-facing surfaces. Tuesday output is internal-readiness; Ben sees the bundle, not the FE.

---

## 9. Risk register

| Risk | Mitigation |
|---|---|
| 4-day window slips | Cut scope ruthlessly: the 6 output files are the deliverable; everything else is supporting |
| LLM-generated proposal language makes financing claims | Hard prompt constraint + post-generation regex strip for `guaranteed`, `approved`, `will receive`, dollar amounts not in scenarios. Reviewed by user before sending to Ben. |
| Manual capture data is incomplete | Schema accepts incomplete with confidence scoring; flags missing critical fields. Returns "missing information list" per beta_execution_prompt. |
| Cross-engine HTTP calls add latency | Tuesday afternoon is offline batch; ~5s per vendor is fine. Optimize only if needed. |
| Distributing across 5 repos = 5 PRs to coordinate | Sequenced Sat→Mon per phase. Each PR independently deployable. Worst case: one PR slips, the affected feature degrades gracefully. |
| Compliance: package §9 explicit "no guaranteed profit / no firm financing terms" | Output bundle text uses scenarios + ranges only. Reviewed by user before any Ben-facing send. |

---

## 10. Approval gates

- [ ] **Assumption 1 — Tuesday = internal readiness, not Ben-facing.** Confirm or redirect.
- [ ] **Assumption 2 — Multipli is a PROSPECT, not yet an operator.** Confirm; if signed already, add to UAE `client_namespaces` instead.
- [ ] **Assumption 3 — Manual capture method = form + CSV upload.** Confirm or specify where data will arrive (Google Sheet? Email? Other?).
- [ ] **Assumption 4-6** — GCP project, output delivery method, no-CRM-integration — confirm tacitly by not objecting.
- [ ] **Distribute-across-engines decision** — confirm (the package proposed a new module; this plan rejects).
- [ ] **Begin Phase A on Saturday 5/23.** Confirm.

## 11. Cross-references

- Package source: `~/Downloads/multipli_claude_beta_package/` (14 files, v1.0.0).
- Related: `docs/architecture/CODEBASE_MAP.md`, `decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md`, `decisions/2026-05-22_billing_architecture_choices.md`.
- Entity to add: `entity_ecosystem_registry` gets Multipli (prospect) + Ben Cahir (executive contact).
