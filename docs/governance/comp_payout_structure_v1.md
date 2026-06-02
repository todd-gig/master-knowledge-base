---
type: governance-scaffold
established: 2026-05-26
status: ACTIVE (v1.1) — ratified by Todd 2026-05-27 (v1.0); §3.5 Gignet tiers ratified by Todd 2026-06-02 (v1.1 — Conservative model). Binding policy for all money-out-of-platform events. Deferred (non-blocking): §3.4/§3.6 v1-promotion calibration triggers → Day-30 window
version: v1.1
authority: Todd sign-off granted 2026-05-27 on §3 v0 locks, §5 retry policy, and the §6 checklist (non-deferred items); 2026-06-02 on §3.5 Gignet tier table (Conservative model). Now binding.
serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
ppim_interaction: meta — governs every money-out-of-platform event for every operator entity
ppim_economics: directly determines net rev share routing across CBP / Ti Solutions clients / Multipli / Gignet / Gigaton-self
ppim_predictability: HIGH — every payout is rule-driven (no per-event discretion); $1k floor + bi-weekly Wed cadence are deterministic
ppim_brand_dimension: trust + transparency (recipients see clean amounts; platform absorbs ACH fees; round-up favors recipient)
ppim_outcome_quality: a single ratified source-of-truth for "who gets paid what, when, via which rail" across every entity in the hierarchy
applies_to:
  - gigaton-engine (billing module — payout scheduler + Stripe Connect Express config)
  - gigaton-gateway (attribution_chain stamping → routes commission events to correct entity)
  - user-access-engine (client_namespaces.governance_overlays.compensation JSONB shape — follow-on)
  - persona-engine (HR offer human-in-loop gate per INTEL-1)
  - decision-engine (semantic_classifier cosine thresholds per INTEL-1)
  - intelligence-silo (skill-vector seed values for talent routing)
  - gigaton-ui-system (operator-facing Settings → Payouts; coaching surfaces auto-graduate via competence — no opt-out toggle)
cross_refs:
  - decisions/2026-05-25_architecture_decisions_log.md (PAYOUT-1, INTEL-1, OPS-1, ARCH-1, ARCH-2)
  - /Users/admin/.claude/projects/-Users-admin/memory/payout_1_min_threshold_1k_2026_05_26.md
  - /Users/admin/.claude/projects/-Users-admin/memory/payout_1_and_intel_1_clarifications_locked_2026_05_26.md
  - /Users/admin/.claude/projects/-Users-admin/memory/compensation_payout_structure_thursday_5_28_deadline.md
  - /Users/admin/.claude/projects/-Users-admin/memory/product_service_package_gigaton_ti_solutions.md
  - /Users/admin/.claude/projects/-Users-admin/memory/entity_hierarchy_for_namespace_seed_2026_05_26.md
  - master_project_plan.md (Chapter 11 — Gignet affiliate tier compensation reference)
  - master-knowledge-base/manifests/onboarding_v1.yaml (consuming stage — follow-on PR)
---

# Compensation + Payout Structure — v1 Scaffold

> **Document state.** ACTIVE as of **2026-05-27** (v1.0, ahead of the Thursday 2026-05-28 EOD deadline). **v1.1 ratified 2026-06-02** — §3.5 Gignet tier table filled (Conservative model: T1 5% / T2 10% / T3 15% / T4 25% / T5 35%; 12-month declining tail). Gignet affiliate payouts now LIVE (no longer dry-run). All v0 locked decisions remain binding policy. Deferred, non-blocking: §3.4/§3.6 v1-promotion calibration triggers (→ Day-30 window).

---

## 1. TL;DR

This document is the single ratified source-of-truth for **who gets paid what, when, and via which rail** across every entity in the Gigaton hierarchy (Carmen Beach Properties + sub-clients, Ti Solutions + 5 retainer clients, Multipli prospect, Gignet affiliates, Gigaton-self). It captures the **8 locked decisions** ratified 2026-05-26 EOD (the `$1,000` minimum payout threshold + 4 PAYOUT-1 clarifications + 3 INTEL-1 clarifications governing HR / coaching / classifier-routing) and scaffolds the per-entity compensation tables that Todd will fill in by **Thursday 2026-05-28 EOD**. Until the §3 percentages and §5 retry policy are ratified, the gigaton-engine billing module and the operator-facing Settings → Payouts surface should treat this doc as DRAFT and refuse to execute any payout that does not satisfy the LOCKED §2 constraints. Cross-references the entity hierarchy seed ([[entity_hierarchy_for_namespace_seed_2026_05_26]]) and the joint Gigaton + Ti Solutions go-to-market wrapper ([[product_service_package_gigaton_ti_solutions]]).

**Hybrid strawman fill (2026-05-26)**: 29 TBDs reduced to 8 strategic %s pending Todd's business judgment (Multipli rev share + Ti Solutions 5-client retainer/uplift splits + Gignet 5-tier commission table + recurring-revenue tail). All cost-of-doing-business defaults pre-filled with industry-norm strawmen marked `(_strawman; override if needed_)`.

**The 8 locked decisions** (memory-backed, do not re-litigate without an explicit Todd directive):

1. **Min payout threshold** = `$1,000 USD`, indefinite, every entity, every rail. Source: [[payout_1_min_threshold_1k_2026_05_26]].
2. **Rounding direction** = round UP (favor recipient). Source: [[payout_1_and_intel_1_clarifications_locked_2026_05_26]].
3. **Cadence** = bi-weekly Wednesday (every other Wed). Same source.
4. **ACH fee bearer** = platform absorbs (recipients see clean amounts). Same source.
5. **First-time payout exception** = NO exception (steady-state cadence applies to first payout). Same source.
6. **HR offer human-in-loop gate** = YES — every HR offer requires human pre-review (operator approval queue). Same source.
7. **Coaching graduation** (REVISED 2026-05-26 EOD) = NO opt-out toggle. Coaching nudges auto-suppress per-category as the operator demonstrates competence (correct UI actions + accurate chat prompts). Same source.
8. **Skill-vector cosine thresholds** = `0.55` primary / `0.35` secondary (drives downstream Ti Agent Matrix routing per INTEL-1). Same source.

---

## 2. LOCKED — Payout structure (concrete, do not modify without explicit Todd directive)

These are deterministic rules. The gigaton-engine billing module and Stripe Connect Express config MUST honor each one.

| Rule | Value | Source memory | Implementation pointer |
|---|---|---|---|
| Minimum payout | **`$1,000 USD`** (indefinite, every entity, every rail) | [[payout_1_min_threshold_1k_2026_05_26]] | `payout_schedule.minimum_amount = 100000` (cents) in Stripe Connect Express + ACH alternative same floor |
| Cadence default | **Bi-weekly Wednesday** (every other Wed) | [[payout_1_and_intel_1_clarifications_locked_2026_05_26]] | Stripe `payout_schedule.interval='weekly'` + `weekly_anchor='wednesday'` + internal scheduler skips alternating weeks |
| Rounding direction | **Round UP** (favor recipient) | Same | `math.ceil(amount_cents)` on every payout calculation; document on receipts |
| ACH fee bearer | **Platform absorbs** | Same | Stripe `application_fee = 0` on payout side; fee aggregates to gigaton-engine COGS line, not recipient deduction |
| First-time payout exception | **No exception** | Same | No special-case logic; first payout uses identical threshold + cadence as steady-state |
| Default rail | **Stripe Connect Express** | [[payout_1_min_threshold_1k_2026_05_26]] | Operator onboarding (Stage 8 `stage-8-tech-stack-costs` — Tech Stack + Unit Economics + Financial Audit) collects KYC + bank via Stripe Connect Express hosted flow (action `connect-billing`) |
| Alternative rail | **ACH** (same $1k floor, same cadence) | Same | For operators who cannot or will not use Stripe Connect Express; accumulate balances below threshold; release on next scheduled cadence when running total clears |
| Multi-currency | Convert `$1k USD` to operator's home currency at payout time; round per the LOCKED round-up rule | Same | Currency conversion at payout-emit time (not at accrual); store both USD-equivalent and home-currency amounts in payout record |
| Sub-clients | Inherit parent operator's payout config unless explicitly overridden | [[payout_1_min_threshold_1k_2026_05_26]] | E.g. `cbp_walking_tour` uses CBP's Stripe Connect Express account by default; override via `client_namespaces.governance_overlays.payout_override` JSONB key |
| **Failed-payout retry policy** | **3 retries × 24h delay → pause + notify operator** (_strawman: standard Stripe + ACH norm; tracks all 3 attempts in `payout_log` for audit; override if needed_) | — | Lives in gigaton-engine billing module retry worker; config: `max_retries=3, backoff_hours=24, on_exhaust='pause_and_notify'` |

> **Why these are locked.** The 4 PAYOUT-1 clarifications + the $1k floor closed the open clarifications dated 2026-05-25 EOD (which were originally scheduled to auto-fire as defaults on 2026-06-01). Todd ratified all 4 PAYOUT-1 + 3 INTEL-1 on 2026-05-26. They are no longer "defaults" — they are policy.

---

## 3. PLACEHOLDER — Compensation routing per entity

> **Todd: this is where you write the actual percentages.** Every TBD below carries a one-line industry-norm guidance comment so you have a defensible starting range. Do NOT auto-fire defaults — these are human-judgment-required fields.

### 3.1 Carmen Beach Properties (operator: `cbp`)

Entity type: operator (hospitality / short-term rental).
Source: [[entity_hierarchy_for_namespace_seed_2026_05_26]] §1.
Revenue model: per-booking GMV → split across owner / cleaning ops / Gigaton platform / (optionally) Ti Solutions managed-service fee.

**Ordering rule (PRE-FILLED)**: **OTA fees come off the top FIRST** (_strawman: standard industry pattern; gross booking → net after OTA → splits below apply to net; avoids paying %s on phantom revenue; override if needed_).

| Component | % of net (after OTA fee) | Cadence | Rail | Guidance |
|---|---|---|---|---|
| Owner rev share | **78% of net with Ti / 81% direct-managed (no Ti)** ✅ LOCKED v0 2026-05-26 (math-backed) | per-booking (accrues; pays out bi-weekly Wed if ≥ $1k) | Stripe Connect Express | Top quartile vs Vacasa 65-75%; near Evolve 90% half-service. Owner-LTV + brand-experience axis dominant. |
| Cleaning ops (per-stay) | **Pass-through actual $ (~$50/stay PDC representative), itemized on booking line** ✅ LOCKED v0 | per-stay (accrues; pays out bi-weekly Wed if ≥ $1k) | ACH | Itemized > absorbed: transparency + cleanliness brand axis. PDC market: $40-$80/stay (Mexico labor, lower than US $145 avg). |
| Gigaton platform fee | **5.0% of net** ✅ LOCKED v0 (math-backed — replaces 2.5% strawman) | per-transaction | Internal credit (no external payout) | Cost-to-serve floor: $8.50/booking @ ~50 bookings/property/yr. 5% yields 65% gross margin (SaaS-healthy). 2.5% strawman left platform underwater on bookings <$1K. Reference: `carmen-beach-occupancy-roi.md`. |
| Ti Solutions service fee (only if owner elects managed-service tier; CBP is direct-managed = 0%) | **3.0% of net** ✅ LOCKED v0 (math-backed — replaces 5% strawman) | monthly | Internal credit | BPO-appropriate ~32% margin at 3% net. 5% strawman exceeded market-competitive ceiling once OTA + cleaning are already off-top. |
| Risk reserve (chargeback / damage cushion) | **1.5% of net** ✅ LOCKED v0 | per-transaction | Internal credit | Industry-norm hospitality reserve. |

**Sum-to-100 check (full-service with Ti)**: OTA off-top → then on net: cleaning pass-through (~12.5% absorbed-equivalent) + Gigaton 5.0% + Ti 3.0% + risk 1.5% + owner 78% = 100% of net ✓
**Sum-to-100 check (self-serve no Ti — CBP today)**: cleaning ~12.5% + Gigaton 5.0% + risk 1.5% + owner 81% = 100% of net ✓ (note: cleaning pass-through itemized = doesn't take from owner share if invoiced separately; the ~12.5% absorbed-equivalent is illustrative — actual cleaning is a flat per-stay $ ≈ 10% of net on the representative booking, see Math basis below)

### Math basis (v0 LOCKED 2026-05-26)

- Variable cost $25/occupied-night per `knowledge-extracts/carmen-beach-occupancy-roi.md`
- Fixed ops $6,000/yr/property, marketing $1,000/yr/property (canonical model)
- Representative booking: $200 ADR × 3 nights = $600 gross; OTA $93 (15.5% Airbnb) + Stripe $17.70 off-top → $489.30 net
- Gigaton 5% = $24.47/booking → margin = $15.97 = **65% gross margin** (SaaS-healthy)
- Owner-net (after cleaning + var + fixed + mktg): $268.40 = 44.7% of gross / 54.8% of net
- Reference benchmarks (2026-current): Airbnb 15.5% / VRBO 8% / Booking.com 15% / Stripe 2.9%+$0.30 / MasterHost PDC 12% / Vacasa 25-35% / Evolve 10%

### v1 calibration triggers (Day 30+)

- Actual cleaning vendor invoices replace $50 estimate
- Channel-mix-weighted OTA fee replaces 15.5% worst-case
- Stripe MX settlement fees confirmed
- Property-level fixed-cost variance (HOA, tax, insurance) tightens fixed-ops bucket
- Real ALOS replaces 4.4-night assumption
- Owner-acquisition A/B test 78% vs 81% confirms market-competitive ceiling

### Multi-objective (M-theory) justification

- **Brand-experience axis**: Cleaning pass-through itemized (transparency) + Ti optional (premium-tier signal)
- **Interaction-management axis**: Gigaton 5% funds decision-engine + LLM-driven guest comm (per `gigaton-playa-dag-model.md` +5% nightly + 10pp occupancy uplift)
- **Profitability axis**: Every line clears cost-to-serve floor with ≥30% margin headroom
- **Cost-to-serve axis**: $8.50/booking Gigaton cost (Cloud Run + Cloud SQL + LLM + customer success fraction)
- **Owner-LTV axis**: 78-81% sits at top quartile of PDC market comparables

### 3.2 CBP sub-clients (walking-tour + DMS marketing)

Entity types: DBA sub-clients of CBP.
- `cbp_walking_tour` — interactive experiences brand at `tour.playadelcarmen.homes`
- `cbp_dms_marketing` — direct marketing services brand at `services.playadelcarmen.homes`

Source: [[entity_hierarchy_for_namespace_seed_2026_05_26]] §3.1.

**Parent-pass-through rule.** Sub-client revenue flows through CBP's Stripe Connect Express account by default (sub-clients inherit parent payout config per the §2 locked rule). The `parent_operator_id` field in `client_namespaces` enables attribution rollup — `ppim_attribution_chain` will read `[cbp_walking_tour, cbp, gigaton-root]` so commission events stamp the full path.

**Sub-client-specific split** (only if Todd wants to carve out a different routing for sub-client revenue):

| Sub-client | % to sub-client owner | % to parent (CBP) | % to Gigaton platform | Cadence | Guidance |
|---|---|---|---|---|---|
| `cbp_walking_tour` | **Pass-through to CBP-parent payout config** (_strawman: single Stripe account for the entire CBP entity tree; override if needed_) | N/A (pass-through) | N/A (pass-through) | per-event | If sub-client is operationally independent (own staff, own GMV pool), might mirror §3.1; if pure CBP up-sell, parent-pass-through is sufficient |
| `cbp_dms_marketing` | **Pass-through to CBP-parent payout config** (_strawman: single Stripe account for the entire CBP entity tree; override if needed_) | N/A (pass-through) | N/A (pass-through) | per-engagement | Marketing-services revenue is typically retainer + outcome-based; structurally closer to §3.3 Ti Solutions clients than to §3.1 STR bookings |

**Per-component %s if split**: N/A (since pass-through chosen). If Todd later wants independent split-out per sub-client, populate the % columns above and remove the pass-through note.

### 3.3 ~~Ti Solutions retainer clients (5)~~ — DELETED 2026-05-26

**Status: DELETED.** Per Todd directive 2026-05-26 eve and `[[cohort-restructure-multipli-gigaton-branded-2026-05-26]]`, the 5 entities previously sketched here (Kollosche / McGrath / Medvidi / CareRev / Integra-CCS) are NOT active client deals. Reclassified:

- **Kollosche + McGrath** → knowledge-extraction sources for CBP real estate ops — see §3.7
- **Medvidi + CareRev** → knowledge-extraction sources for platform service / HR / acquisition doctrine — see §3.7
- **Integra-CCS** → dropped (no active deal, no knowledge-extraction value identified)

Ti Solutions brand is NOT killed by this directive — Ti DBA launches (Ti Life / Ti Solutions / Total Interactions) may return per entity launch order in `[[RESUME_HERE_2026_05_26_full_session_handoff]]`. But there are no active Ti client deals as of 2026-05-26, so no compensation rows.

The ONLY active proposed deal in flight is Multipli — moved to §3.4 under **Gigaton brand** (not Ti).

### 3.4 Multipli engagement (GIGATON-branded — beta cohort #1)

**Brand: GIGATON (NOT Ti)** per Todd directive 2026-05-26 eve.
**Status**: v0 LOCKED 2026-05-26 (math-backed by research agent; Day-30 calibration scheduled).
**Cohort**: beta cohort #1 — first paying operator.
**Contact owner**: Ben Cahir (CEO).
**Source**: `[[multipli_vendor_growth_engine_sprint_2026_05_22]]` ($650M financed, 23K vendor contracts) + 2 mkb runbooks + sample bundles `multipli/sample_bundles/{calendly,loom,notion}/deal_economics_model.json` + 2026-current channel-partner industry research.
**Revenue model**: performance share of Multipli net revenue per Gigaton-attributed funded contract.

| Term | Value | Math basis | PPIM axis |
|---|---|---|---|
| Performance share | **18% of Multipli net revenue** on Gigaton-attributed funded contracts ✅ LOCKED v0 | High end of 5-20% channel-partner band (Allbound / Magentrix / Kiflo / Scaleo norms); justified by Gigaton supplying full performance infrastructure (intel-silo + decision-engine + ppeme + FE + HME + governance) — closer to co-build than referral. ≈ 5.4% of Multipli gross spread (below their own 8% mid-scenario). | economics + LTV |
| Cadence | **Monthly, T+15** after Multipli funding-month close ✅ LOCKED v0 | Matches Multipli's portfolio funding cycle. | interaction (monthly settlement loop) |
| Rail | **Stripe Connect Express** ✅ LOCKED v0 | PAYOUT-1 default. | predictability |
| Min payout floor | **$1,000 USD** (accrue if below) ✅ LOCKED v0 | PAYOUT-1 platform rule per §2. | economics |
| Base retainer | **NO for beta cohort #1** (variable-only) ✅ LOCKED v0 | Aligns incentive; revisit at M4 if both sides want predictability. | predictability |
| Attribution | **First-touch + 180-day verified-handoff** ✅ LOCKED v0 | Vendor counts as Gigaton-attributed if (a) originated in Gigaton `vendor.financing.captured.v1` event AND (b) Multipli funding system confirms funded contract within 180d. | interaction + economics |
| Term | **6 months initial; auto-renew if either side exceeds 50 funded-contracts-from-Gigaton** ✅ LOCKED v0 | Both-sides off-ramp at small scale; renewal trigger ties to delivered value. | lifecycle |
| Y1 cap | **$250K max perf share** ✅ LOCKED v0 | = 465 funded contracts at $538/contract net. Floors Multipli downside if Gigaton over-delivers. | economics (partner predictability) |

### Per-funded-contract economics (SaaS canonical example)

| Line | $ |
|---|---|
| Customer total payment ($2K × 36mo) | $72,000 |
| Vendor upfront payout | $62,000 |
| Multipli gross spread pool | $10,000 |
| Less cost of funds (~5% × $62K × 1.5yr) | ($4,650) |
| Less credit-risk reserve (3% default) | ($1,860) |
| Less ops + servicing | ($500) |
| **Multipli net revenue** | **$2,990** |
| Gigaton perf share @ 18% of net | **$538** |
| Gigaton fully-loaded cost per qualified vendor | ~$1.80 |
| At 10% vendor→contract conversion, cost-to-serve per funded contract | ~$18 |
| **Gigaton contribution margin** | **$520 / 96.6%** |

### Multi-objective (M-theory) justification

- **Brand-experience axis**: Gigaton brand for Multipli signals platform-product (not bespoke-services)
- **Interaction-management axis**: 18% sustains the engine ensemble that produces vendor research → routed prospects → proposal bundles → onboarding automation
- **Profitability axis**: 96.6% contribution margin at scale; cost-to-serve floor at 3.3% perf share gives massive headroom
- **Cost-to-serve axis**: $1.80/qualified vendor LLM+infra cost amortized across full ensemble
- **LTV-as-operator axis**: Multipli is canary for entire vendor-finance vertical — successful delivery seeds playbook for cohort #2+

### Self-serve tokenized link onboarding architecture

**URL pattern**: `https://gigaton.ai/onboard/multipli/<jwt-token>`

**Token**: JWT (HS256), single-use via Redis/Firestore `jti` set, **14-day expiry**. Payload carries `prospect_id`, `contact`, `cohort`, `terms_template_version`, `perf_share_pct`, `min_payout_usd`, `rail`, `exp`, `jti`, `iat`.

**Server-side pre-provisioning (before link is sent):**

1. UAE `client_namespaces` row with `state=pending_acceptance`, `parent_operator_id=gigaton`, `cohort=beta_1`
2. Persona-engine seeds default vendor-finance B2B persona
3. Capability tier = `tier_0_onboarding`
4. UAE `workflow_overlays` JSONB seeded with `multipli_perf_share_v0` template
5. Decision-engine pre-creates Stripe Connect Express account in `pending_kyc` state
6. HME emits `prospect.onboard_link.issued.v1`

**Single-scroll landing page bundle**:

1. Co-branded hero (Gigaton + Multipli lockup)
2. Value-prop summary (vendor research pipeline / fit-scored opportunities / 6-file proposal bundles / dashboard)
3. Integration documentation (engine ensemble routing)
4. Commercial terms (renders from JWT payload — never hardcoded)
5. ToS + privacy + SLA
6. E-sign (**recommend in-app for beta cohort #1**; DocuSign upgrade path for cohort #2+)
7. Stripe Connect Express KYC + bank linking
8. Final confirmation → namespace flips `state=active`, capability tier → `tier_1_active`, Wave 2 dispatch enabled, HME `operator.activated.v1` fires

**Reuses (existing infrastructure)**: ChatOnboardingOrchestrator + UAE 10-stage manifest (`master-knowledge-base/manifests/onboarding_v1.yaml`) + gateway onboarding endpoints (live rev `00027-pb9`) + L2 access layer per ARCH-2 + HME event emission + Stripe Connect Express PAYOUT-1 rail.

**New work required (~23h ≈ 3 dev-days)**:

1. Token issuer + validator middleware — `POST /v1/onboard/issue-link` (admin-gated) + middleware (~6h)
2. Co-branded landing page `gigaton-ui-system/src/pages/onboard/MultipliOnboard.tsx` (~5h)
3. Commercial-terms template `master-knowledge-base/templates/commercial_terms/multipli_v0.md` (~2h)
4. Terms-acceptance HME event type + in-app e-sign capture (~4h)
5. Stripe Connect Express handoff (`accountLinks.create`) (~3h)
6. Acceptance → namespace-activate transition (UAE state machine + capability tier bump) (~3h)

**Send mechanism**: **Gmail-via-Workspace** from `todd@gigaton.ai` (primary; preserves audit trail in Workspace logs + HME `prospect.outreach.sent.v1`). Slack DM = redundant ack only ("check your email for the onboarding link" 5 min after Gmail send). **DO NOT send link in Slack alone** — Slack has weaker retention/audit posture for commercial terms acceptance.

### v1 calibration triggers

- Actual vendor→funded-contract conversion rate replaces 10% optimistic estimate
- Actual cost-of-funds + default-rate validate per-contract economics
- Multipli's actual channel-mix (Gigaton-attributed vs other) tightens attribution rules
- Y1 cap revisit at M6 based on actual delivered volume

### 3.5 Gignet affiliates (when active)

Entity type: cross-cutting affiliate network spanning all operators.
Source: [[master_project_plan]] Chapter 11 (Gignet affiliate-network platform — 18 affiliate pages × 25 certs × 5 tiers × 8 products).
Revenue model: tier-based per-conversion commission, paid out of the operator's Gigaton platform fee.

| Tier | Per-conversion rev share % | Cadence | Rail | Guidance |
|---|---|---|---|---|
| Tier 1 (entry — T1 CERTIFIED) | **5%** ✅ LOCKED v1.1 (Conservative) | per-conversion (accrues; pays bi-weekly Wed if ≥ $1k) | Stripe Connect Express | Bottom of master_plan Chapter 11 tier-1 range (5-10%). Conservative model preserves Gigaton platform margin (Ops 40 / R&D 35 / Reserves 25 per §3.6 LOCKED). |
| Tier 2 (T2 SENIOR — 7+ certs) | **10%** ✅ LOCKED v1.1 (Conservative) | Same | Same | Bottom of master_plan Chapter 11 tier-2 range (10-20%). |
| Tier 3 (T3 ORG_AFFILIATE — 12+ certs + sub-affiliate mgmt) | **15%** ✅ LOCKED v1.1 (Conservative) | Same | Same | Below master_plan Chapter 11 tier-3 range (20-30%) — Conservative model trades growth velocity for margin preservation. |
| Tier 4 (elite — high-volume + Advanced certs) | **25%** ✅ LOCKED v1.1 (Conservative) | Same | Same | Below master_plan Chapter 11 tier-4 range (30-40%) — same Conservative trade-off. |
| Tier 5 (top — Pascal certs / Expert-tier CERT-023/024/025 / high-volume) | **35%** ✅ LOCKED v1.1 (Conservative) | Same | Same | Below master_plan Chapter 11 tier-5 range (40-50%) — preserves Gigaton net for highest-payout tier. Tail-commission stacks per the row below. |
| Recurring-revenue tail policy (any tier) | **12 months declining** ✅ LOCKED v1.1 (Conservative) | 100% mo 1-6 → 50% mo 7-9 → 25% mo 10-12 → 0 after month 12 | (same rail as tier) | Bottom of affiliate-network norm (6-24 months); fast wind-down preserves operator economics on long-tail subscription revenue. Calibration trigger: revisit at M6 if affiliate-driven churn delta > 5pp vs direct-acquired customers. |

**Attribution rule**: Gignet affiliate commission is computed against the conversion's `ppim_attribution_chain`. If the chain is `[cbp_walking_tour, cbp, gigaton-root]` and an affiliate referred the customer, the affiliate's commission comes out of Gigaton's platform fee slice, not out of CBP's owner share. (Source: [[2026-05-08_affiliate_centralization_at_gigaton]] — SIE chain 22 owns the canonical affiliate state; tenants attribute, they do not own.)

### 3.6 Gigaton self (platform) — Option A LOCKED ✅ 2026-05-26

Entity type: platform-root (`gigaton`).
Revenue model: internal allocation of net rev after every operator entity is paid.
**Status**: v0 LOCKED 2026-05-26 (math-backed by research agent; Option A ratified; replaces 45/25/20/10 strawman).

| Internal bucket | % of Gigaton net rev | Floor | Ceiling | Cadence | PPIM axis |
|---|---|---|---|---|---|
| Operations (cloud infra, 3rd-party API costs, ACH fees absorbed per §2, Stripe processing fees, S&M, G&A) | **40%** ✅ LOCKED v0 | 28% | 55% | continuous (COGS line) | predictability |
| R&D (engineering, agent build-out, Wave 2 Intelligence Layer + Ti Agent Matrix expansion) | **35%** ✅ LOCKED v0 | 22% | 50% | continuous (engineering payroll) | brand_dimension (build-velocity) |
| Reserves (runway, regulatory, dispute / chargeback buffer) | **25%** ✅ LOCKED v0 (Option A — absorbs the 5% slice that would otherwise go to distribution) | 15% | 30% | continuous (treasury) | interaction (platform-survival) |
| Distribution to Todd / equity holders (post-reserves-floor) | **0%** ✅ LOCKED v0 (Option A — re-introduce at v1 once Multipli + Ti retainers contribute meaningful net rev) | 0% | 15% | quarterly or per-board-decision | outcome_quality |

**Sum-to-100 check**: ops (40%) + R&D (35%) + reserves (25%) + distribution (0%) = **100%** of Gigaton net rev ✓

### Reserves-floor activation (math-backed)

**Floor = $180,000** (= 12 months × $15K projected steady-state opex at cohort #0-3 stage)

```python
if treasury_balance < 180_000_USD:
    distribution_pct = 0
    reserves_pct = 25  # absorbs the 5% distribution slice
else:
    distribution_pct = 0  # locked 0% at v0 — re-introduce at v1
    reserves_pct = 25
```

**Auto-bump rule**: Floor recomputes monthly. Each new active cohort operator adds projected monthly opex delta (~$500-$2,000/mo per operator) to the floor.

### Why Option A (locked 2026-05-26)

At projected ~$1K/mo accrual rate (Premium-tier $499/mo + CBP 5% fee on 50 bookings × $600), time-to-clear $180K reserves floor from operations alone = **~144 months under Option A** (180 months under rejected Option B). Option A's 5%-redirect-to-reserves accelerates accrual by ~25% while honoring PPIM doctrine "platform-survival before founder-draws." Distribution can be re-introduced at v1 once Multipli + Ti retainers contribute meaningful net revenue.

### Math basis (v0 LOCKED 2026-05-26)

- Infra cost band $85-$130/mo from `cloudbuild.yaml` `min-instances=1` × 3 always-on services + scale-to-zero × 8 + 2 Cloud SQL + Firebase Hosting + Storage + DNS + Secret Manager
- LLM API band $150-$500/mo via gigaton-gateway `llm_call_cost` Firestore telemetry (no aggregate pulled yet — v1 trigger)
- Twilio WhatsApp ~$20/mo at cohort #0 volume
- Realistic steady-state opex band $1K-$15K/mo (15× spread reflects unknown payroll line — see v1 calibration)
- Reference benchmarks (2025): SaaS Capital R&D 22% median + Benchmarkit 26% + Lighter Capital early-stage 50%+ R&D + Rule-of-40 + Drivetrain 12-18mo bootstrapped runway floor

### v1 calibration triggers (Todd-only inputs)

- Confirm payroll/contractor monthly cash burn (no headcount file in repo today)
- Confirm cash on hand (drives feasibility of $180K floor target)
- Pull 30-day `llm_call_cost` aggregate from Firestore (replaces $300/mo midpoint estimate)
- Wire `cost-coverage` aggregator (`intelligence-silo/core/onboarding/endpoints.py:434` currently stub)
- Approve `monthly_opex_auto_bump` mechanism for floor recomputation

---

### 3.7 Knowledge-extraction sources (NEW 2026-05-26)

Replaces the dropped Ti 5-client compensation matrix (§3.3). **NOT compensation rows** — read-only registry of work-product origins that inform CBP and platform doctrine.

| Source | Vertical | Work-product captured | Applied to |
|---|---|---|---|
| **Kollosche** | AU luxury real estate | Pricing structures, contract templates, agent comp models, listing-quality patterns | CBP / `playadelcarmen.homes` real estate business model |
| **McGrath** | Real estate placement / sales | Listing pipelines, closing patterns, sales-process automation | CBP / `playadelcarmen.homes` real estate business model |
| **Medvidi** | Healthcare patient acquisition | Service-industry frameworks, human management systems, acquisition / process logic | Platform doctrine — services / HR / acquisition workflows |
| **CareRev** | Per-shift healthcare staffing marketplace | Supply-side acquisition patterns, matching algorithms, cadence models | Platform doctrine — services / HR / acquisition workflows |

**Out of scope**: Integra-CCS (no active deal, no knowledge-extraction value identified — dropped 2026-05-26).

**Provenance tracking**: every pattern derived from these sources and applied to platform doctrine or CBP must carry a `provenance.source` tag (e.g. `provenance.source: kollosche/pricing_template_v2_2024-Q4`) for audit trail. Tracked in `master-knowledge-base/knowledge-extracts/_provenance/` (follow-on PR to scaffold the registry).

**No payouts** — these sources do not receive compensation from this document. If any of the 4 becomes an active deal in the future, it gets its own §3.X compensation row at that time.

---

## 4. LOCKED — INTEL-1 / HR clarifications

These 3 clarifications were ratified 2026-05-26 EOD alongside the 4 PAYOUT-1 clarifications. They govern how the Intelligence Layer + Self-Engineered HR loops behave around money-adjacent decisions (offers, coaching nudges, talent routing).

### 4.1 HR offer human-in-loop gate

**Rule**: every HR offer requires human pre-review before it leaves the platform.

- Self-Engineered HR auto-drafts the offer (job ad copy, comp package, equity offer, retention adjustment, etc.).
- Drafted offer is routed to the operator's pre-send approval queue via `human-management-engine`.
- Operator clicks "send" or "edit & send" — only then does the offer leave the platform.
- **Why locked this way**: per `CRIT-001` ("automation requires human override") + HR offers carry legal + retention consequences that pure-LLM judgment cannot underwrite.
- **Implementation**: `persona-engine` HR module emits `OfferDrafted` event → `human-management-engine` enqueues for operator approval → gated send.

### 4.2 Coaching graduation (REVISED 2026-05-26 EOD — supersedes opt-out)

**Rule**: NO opt-out toggle. Coaching is automatically REMOVED or CHANGED per-nudge-category as the operator demonstrates competence through (a) correct UI actions and (b) accurate chat prompts.

- **Mechanism**: every operator receives coaching nudges by default. Each nudge category (e.g. "how to connect a Drive folder", "how to interpret variance display", "how to use the prompt suggestor") graduates independently as the operator demonstrates understanding.
- **Graduation criteria per nudge category**:
  - **Correct actions**: operator completed the corresponding UI flow without error `N` times (default `N=3`)
  - **Accurate prompts**: operator's chat prompts in the relevant domain hit the intent classifier with confidence `≥ 0.55` (matches our primary cosine threshold from §4.3) `M` times (default `M=2`)
  - Both criteria must be met to graduate
- **Re-emergence**: if the operator regresses (errors return, or chat prompts drop below `0.35` accuracy), coaching for that category re-activates automatically.
- **Why locked this way**: an opt-out toggle lets operators silence the system's only built-in onboarding correction; the graduation model preserves the autonomy intent (no nag once competent) without the regression risk (operator turns it off + never gets help when they need it).
- **Implementation**:
  - `agent_roles.coaching_categories` JSONB list per role defining nudge categories that role emits.
  - new table `coaching_graduation_state` per `(operator_id, nudge_category)` tracking `correct_action_count`, `accurate_prompt_count`, `graduated_at`, `last_regression_at`.
  - `persona-engine` emits nudge → checks `coaching_graduation_state` → suppresses if graduated → else delivers.
  - `decision-engine` `intelligence/classify` confidence scores feed `accurate_prompt_count` increments.
  - UI flow completions emit `CoachingProgressEvent` to `human-management-engine` → updates `correct_action_count`.
  - Spec follow-on (separate PR) to define every nudge category + its criteria thresholds; ship behind a `coaching.v2_graduation` feature flag.
- **No Settings UI**: there is NO operator-facing toggle. The Settings page will surface graduation STATUS (e.g. "You've graduated 3 of 12 coaching topics") as a transparency mechanism, but the operator cannot disable nudges directly. Regression auto-re-engages — operator's path to "no more nudges" is genuine competence, not a switch.

### 4.3 Skill-vector cosine thresholds (for downstream Ti Agent Matrix routing)

**Rule**: `0.55` primary / `0.35` secondary.

- `0.55` — cosine similarity threshold above which a skill is a PRIMARY match (drives `primary_role_key` in the agent ensemble).
- `0.35` — cosine similarity threshold above which a skill is a SECONDARY match (drives `routed_roles[]` entries, not primary).
- **Why locked this way**: standard sentence-transformers / `all-MiniLM-L6-v2` heuristic for technical-text similarity; tunable post-real-data observation.
- **Implementation**: env-readable constants in `decision-engine/engine/intelligence/semantic_classifier.py` — `COSINE_PRIMARY_THRESHOLD=0.55` + `COSINE_SECONDARY_THRESHOLD=0.35`. Override per-deploy via env. Compensation-relevance: drives which Ti Agent Matrix role earns attribution credit for a query — and downstream, any future per-role internal billing.

---

## 5. Implementation pointers

Where this document is **consumed**:

### 5.1 Stripe Connect Express config (gigaton-engine billing module)

Suggested config keys (illustrative — confirm exact field names against Stripe Connect Express docs at integration time):

```python
# pseudo-config, gigaton-engine/billing/stripe_connect.py
PAYOUT_CONFIG = {
    "minimum_amount_cents": 100_000,        # $1,000 USD floor per §2
    "schedule_interval": "weekly",          # Stripe field
    "weekly_anchor": "wednesday",            # Stripe field
    "biweekly_skip": True,                   # internal scheduler — skip every other Wed
    "rounding_mode": "ROUND_UP",             # math.ceil per §2
    "application_fee_bps": 0,                # platform absorbs per §2
    "first_payout_special_case": False,      # no exception per §2
    "retry_policy": {                        # PLACEHOLDER — needs Todd ratification per §2
        "max_retries": 3,
        "backoff_hours": 24,
        "on_exhaust": "pause_and_notify",
    },
}
```

### 5.2 Onboarding manifest reference (follow-on PR)

`master-knowledge-base/manifests/onboarding_v1.yaml` should add a link to this doc from **Stage 8 `stage-8-tech-stack-costs` (Tech Stack + Unit Economics + Financial Audit)** — payouts/KYC/billing rails are gathered here via the `connect-billing` action, NOT at Stage 7 (`stage-7-assignments` is "Human-assigned + Automated Processes" — process ownership, not payouts). Correction 2026-05-28: the earlier strawman labeled Stage 7 "Capability+Payouts," but the actual manifest at v1.0.0/v1.1.0 names Stage 7 `Human-assigned + Automated Processes` and gathers payout-relevant data at Stage 8. Note: this is a **follow-on PR**, not part of this scaffold.

### 5.3 gigaton-engine billing module (currently in development)

The billing module should:
1. Read §2 LOCKED rules at startup; refuse to start if any are missing.
2. Read §3 per-entity percentages from `client_namespaces.governance_overlays.compensation` JSONB (once Todd ratifies §3 → encode into UAE migration → seed per entity).
3. Emit `PayoutScheduled`, `PayoutAttempted`, `PayoutSucceeded`, `PayoutFailed` events to HME for observability.
4. Cross-reference `ppim_attribution_chain` from gigaton-gateway on every payout to ensure parent / sub-client routing per §3.2.

### 5.4 Operator-facing UI Settings (gigaton-ui-system)

Surfaces:
- **Settings → Payouts** — displays operator's configured Stripe Connect Express account, next scheduled payout date, accrued balance, $1k floor reminder, history.
- **Settings → Coaching graduation status** — transparency-only surface per §4.2 (graduation progress per nudge category); NO opt-out toggle.
- **Settings → Compensation** (admin-only, future) — displays the §3 percentages for the operator's entity; read-only for the operator.

### 5.5 user-access-engine (UAE) schema follow-on

Per [[entity_hierarchy_for_namespace_seed_2026_05_26]] §"NOT in PR #38": `compensation_terms` is NOT yet in the UAE schema. The §3 percentages, once ratified, need a home — either a new `compensation_terms` table or a `governance_overlays.compensation` JSONB key. **AUTHORIZED (PRE-FILLED)**: **YES — flag as follow-on PR; track separately** (_strawman: ship `compensation_terms` JSONB column on `client_namespaces` as a separate UAE schema PR; override if needed_). This doc does not block on it (the percentages can be source-of-truth here while UAE catches up).

---

## 6. Open items for Todd's review (FILL THESE IN)

Checklist Todd ticks off to promote this doc from DRAFT → ACTIVE. Each TBD from §3 + the §2 retry policy + the §5.2 manifest stage:

### Payout structure (§2)
- [x] Failed-payout retry policy — accept suggested default (3 retries × 24h delay → pause + notify) or specify alternative

### CBP (§3.1)
- [x] CBP owner rev share % (strawman: REMAINING after OTA + cleaning + Gigaton + Ti Solutions)
- [x] CBP cleaning ops % (strawman: pass-through per-stay)
- [x] CBP Gigaton platform fee % (strawman: 2.5% of net)
- [x] CBP Ti Solutions service fee % (strawman: 5% of net, managed-service tier only)
- [x] OTA fee ordering (strawman: off the top BEFORE split)

### CBP sub-clients (§3.2)
- [x] `cbp_walking_tour` — split or parent-pass-through? (strawman: pass-through)
- [x] `cbp_dms_marketing` — split or parent-pass-through? (strawman: pass-through)
- [x] If split: per-sub-client % to sub-client owner / parent CBP / Gigaton platform (N/A since pass-through chosen)

### Ti Solutions clients (§3.3) — **DELETED 2026-05-26**
- [x] §3.3 deleted; 4 of 5 entities reclassified as knowledge-extraction sources in §3.7; Integra-CCS dropped

### Multipli (§3.4 — under GIGATON brand)
- [x] **Performance share to Gigaton** = 18% of Multipli net rev on Gigaton-attributed funded contracts ✅ LOCKED v0 (math-backed)
- [x] Cadence = monthly T+15 / Rail = Stripe Connect Express / Min = $1k floor / Retainer = NO for beta ✅ LOCKED v0
- [x] Attribution = first-touch + 180-day verified-handoff ✅ LOCKED v0
- [x] Term = 6mo initial; auto-renew at 50 contracts; $250K Y1 cap ✅ LOCKED v0
- [x] Self-serve tokenized link architecture spec'd (URL pattern + bundle + reuses + ~23h new work)
- [ ] **v1 promotion**: Confirm 15/18/20 perf share final, base retainer yes/no, attribution window 90/180/365, Y1 cap, e-sign tool (in-app vs DocuSign), link expiry, co-branded hero approval gate, send timing

### Gignet affiliates (§3.5) — ✅ LOCKED v1.1 (Conservative model, 2026-06-02)
- [ ] Tier 1 per-conversion rev share %
- [ ] Tier 2 per-conversion rev share %
- [ ] Tier 3 per-conversion rev share %
- [ ] Tier 4 per-conversion rev share %
- [ ] Tier 5 per-conversion rev share %
- [ ] Recurring-revenue tail commission policy (any tier)

### Gigaton self (§3.6) — Option A LOCKED ✅ 2026-05-26
- [x] Operations % = **40%** ✅ LOCKED v0 (math-backed; replaces 45% strawman)
- [x] R&D % = **35%** ✅ LOCKED v0 (math-backed; replaces 25% strawman)
- [x] Reserves % = **25%** ✅ LOCKED v0 (Option A — absorbs distribution slice)
- [x] Distribution % = **0%** ✅ LOCKED v0 (Option A — re-introduce at v1)
- [x] Reserves-floor = **$180K** (12 × $15K opex; auto-bumps per cohort)
- [ ] **v1 promotion**: Confirm payroll/contractor cash burn + cash on hand + approve auto_bump mechanism + authorize cost-coverage aggregator wiring

### Implementation follow-ons (§5)
- [x] Confirm onboarding_v1.yaml stage number to link this doc from — **CORRECTED 2026-05-28**: Stage 8 `stage-8-tech-stack-costs` (Tech Stack + Unit Economics + Financial Audit), not Stage 7. Earlier strawman ("Stage 7 — Capability+Payouts") didn't match the actual manifest; payouts/KYC/billing live at Stage 8 via the `connect-billing` action.
- [x] Authorize UAE schema follow-on for `compensation_terms` (strawman: YES — flag as separate follow-on PR)

**v1.1 status (2026-06-02): all 29 §3 entries LOCKED.** v0.2 pre-filled 21 strawmen → v0.3 math-backed 21 + 2 enriched → v1.0 ratified non-deferred items → v1.1 ratifies the remaining 6 §3.5 Gignet tier entries (Conservative model) + 2 calibration-trigger placeholders. Strategic-only remaining = 0.

**Promotion gate (satisfied 2026-05-27)**: this doc promotes to `ACTIVE` once every *non-deferred* checkbox above is ticked + Todd updates the front-matter `status:`. Three boxes remain unticked **by design, not as blockers**: §3.5 Gignet tiers (no active affiliate deal → deferred to v1.1 / Day-30 calibration) and the two v1-promotion calibration lines in §3.4 Multipli + §3.6 Gigaton-self (calibration-trigger inputs, not v0 locks). All v0 locked values stand as binding policy. The gigaton-engine billing module runs live for any entity with §3 percentages set (CBP, Multipli, Gigaton-self) and stays in dry-run mode only for entities whose percentages remain unset (Gignet until v1.1). Strawmen are accepted by default; Todd un-ticks any line to revise.

---

## 7. Decisions-log mirror

Cross-reference table linking each section to the underlying memory file and architectural-decision-log entry.

| Section | Underlying decision | Memory file | Decisions-log entry |
|---|---|---|---|
| §2 min payout `$1k` | PAYOUT-1 amendment (Todd 2026-05-26) | `payout_1_min_threshold_1k_2026_05_26.md` | PAYOUT-1 amendment (`decisions/2026-05-25_architecture_decisions_log.md`) |
| §2 rounding round-up | PAYOUT-1 clarification 1 | `payout_1_and_intel_1_clarifications_locked_2026_05_26.md` | PAYOUT-1 clarification |
| §2 cadence bi-weekly Wed | PAYOUT-1 clarification 2 | Same | PAYOUT-1 clarification |
| §2 ACH fee bearer (platform) | PAYOUT-1 clarification 3 | Same | PAYOUT-1 clarification |
| §2 no first-time exception | PAYOUT-1 clarification 4 | Same | PAYOUT-1 clarification |
| §2 default rail Stripe Connect Express | PAYOUT-1 original (2026-05-25) | `payout_1_min_threshold_1k_2026_05_26.md` (cross-ref) | PAYOUT-1 original |
| §3 entity routing | requires Todd ratification | — | (open until §6 checklist ticked) |
| §3.5 Gignet attribution | SIE chain 22 affiliate centralization | — | `decisions/2026-05-08_affiliate_centralization_at_gigaton.md` |
| §4.1 HR human-in-loop | INTEL-1 clarification (HR offer gate) | `payout_1_and_intel_1_clarifications_locked_2026_05_26.md` | INTEL-1 clarification + CRIT-001 reference |
| §4.2 coaching graduation (NO opt-out, auto-suppress via competence) | INTEL-1 clarification (coaching) — REVISED 2026-05-26 EOD | Same | INTEL-1 clarification + competence-graduation model |
| §4.3 cosine thresholds 0.55 / 0.35 | INTEL-1 clarification (classifier) | Same | INTEL-1 clarification |
| §5 Wave 2 Intelligence Layer context | INTEL-1 / INTEL-2 Wave 2 redefinition | — | `docs/architecture/2026_05_25_wave2_intelligence_layer_ti_agent_matrix.md` |

---

## 8. Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 (this scaffold) | 2026-05-26 | Claude Opus 4.7 (1M context) — under Todd direction | Initial scaffold; §2 LOCKED + §4 LOCKED + §3 TBDs awaiting Todd ratification; deadline 2026-05-28 EOD |
| v0.2 (hybrid strawman fill) | 2026-05-26 | Claude Opus 4.7 (1M context) — under Todd direction | Pre-filled 21 of 29 TBDs with industry-norm strawmen marked `(_strawman; override if needed_)`; 8 strategic %s flagged `**STRATEGIC — Todd to fill in**` |
| v0.3 (math-backed v0) | 2026-05-26 eve | Claude Opus 4.7 (this session) — under Todd direction "ensure all math is completed as correctly as possible from start" | **3 research agents in parallel** derived math-backed v0 values from real artifacts (`carmen-beach-agent-costing.md` + `carmen-beach-occupancy-roi.md` + `gigaton-playa-dag-model.md` + `gigaton-company-valuation.md` + `multipli_research_brief.md` + `multipli/sample_bundles/*/deal_economics_model.json` + 11+ Cloud Run `cloudbuild.yaml` configs) + 2025-2026 industry benchmarks (Airbnb 15.5% / VRBO 8% / Vacasa 25-35% / Evolve 10% / MasterHost PDC 12% / SaaS Capital 2025 / Benchmarkit 2025 / Rule-of-40 / channel-partner 5-20% band). **§3.1 CBP** v0.2 strawmen replaced: Gigaton 2.5% → 5.0% (cost-to-serve math); Ti 5% → 3% (market-ceiling); cleaning pass-through itemized; owner 78%/81%; risk reserve 1.5% added. **§3.3 DELETED** (4 entities reclassified as knowledge-sources, 1 dropped). **§3.4 Multipli** repositioned under GIGATON brand with full math-backed terms (18% perf share + monthly T+15 + Stripe Connect + $1K floor + no retainer + 180d attribution + 6mo term + $250K Y1 cap) + self-serve tokenized link architecture spec'd (`gigaton.ai/onboard/multipli/<jwt>` + bundle + reuses + ~23h new dev work). **§3.6 Gigaton-self** Option A LOCKED (Ops 40 / R&D 35 / Reserves 25 / Distribution 0; $180K floor with auto-bump). **§3.7 NEW** knowledge-extraction sources catalog (Kollosche+McGrath for CBP RE; Medvidi+CareRev for service/HR/acquisition doctrine; Integra-CCS dropped). PPIM axis-weighted multi-objective (M-theory) justifications on every line. Logged to MASTER_PLAN.md §13 via `add_decision` MCP 21:42 + 22:03 UTC. Companion ratifications: D1 + D2 + MIG-DEFER. |
| v1.0 (RATIFIED) | 2026-05-27 | Todd (via Claude Opus 4.7 1M) | Promoted DRAFT → ACTIVE one day ahead of deadline. v0 math-backed values approved as locked/binding. Pre-flip fixes: §3.1 sum-to-100 cleaning figure corrected ~14% → ~12.5% (the prior "✓" overstated by 1.5pp); §6 promotion-gate text reconciled to acknowledge the 3 by-design deferrals (Gignet §3.5 → v1.1; §3.4 Multipli + §3.6 Gigaton-self v1-promotion calibration → Day-30) rather than requiring every box. Gignet §3.5 (5 tiers + tail policy) deferred to v1.1 (Day-30 calibration window). |
| **v1.1 (RATIFIED)** | **2026-06-02** | **Todd (via Claude Opus 4.7 — same-day Conservative pick post-Hub-ship)** | **§3.5 Gignet affiliate tier table LOCKED.** Conservative model: T1 entry 5% / T2 senior 10% / T3 org_affiliate 15% / T4 elite 25% / T5 top (Pascal certs / Expert tier) 35%. Recurring-revenue tail: 12 months declining (100% mo 1-6 → 50% mo 7-9 → 25% mo 10-12 → 0). Calibration trigger: revisit T5 + tail at M6 if affiliate-driven churn delta > 5pp vs direct-acquired customers. **Gignet affiliate payouts now LIVE (no longer dry-run).** Conservative model selected over Moderate / Aggressive Growth strawmen — preserves §3.6 Gigaton-self bucket targets (Ops 40 / R&D 35 / Reserves 25) when affiliate-attributed deals route through the Chapter 11 commission rail. Strategic-only TBDs remaining = 0. |

---

## PPIM signature

```
ppim_interaction:        meta — governs every money-out-of-platform event for every operator entity
ppim_economics:          directly determines net rev share routing across all entities
ppim_predictability:     HIGH — every payout is rule-driven; $1k floor + bi-weekly Wed cadence deterministic
ppim_brand_dimension:    trust + transparency (recipients see clean amounts; platform absorbs ACH fees; round-up favors recipient)
ppim_outcome_quality:    single ratified source-of-truth for "who gets paid what, when, via which rail"
ppim_attribution_chain:  [comp_payout_structure_v1, governance, master-knowledge-base, gigaton-root]
```
