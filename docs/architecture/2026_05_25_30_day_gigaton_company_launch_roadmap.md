---
title: 30-Day Gigaton Company Launch Roadmap
date: 2026-05-25
horizon: 2026-05-26 → 2026-06-24
author: Todd Nelson (Founder/Architect)
status: DESIGN — pending Founder + Owner sign-off (see §"User decisions needed")
serves: PPIM (Predictably Profitable Interaction Management)
honors:
  - B1: single platform Stripe account; entities are Customers
  - B2: per-product-and-service-package billing
  - B3: billing logic lives in `gigaton-engine`
  - B4: per-deal-and-package cadence
  - B5: Stripe Tax `automatic_tax: {enabled: true}`
related:
  - entity_ecosystem_registry.md
  - product_service_package_gigaton_ti_solutions.md
  - foundational_goal_gigaton_engineered_brand_experience.md
  - universal_connector_hub_architecture.md
  - master_project_plan.md (Chapter 11)
  - multipli_vendor_growth_engine_sprint_2026_05_22.md
---

# 30-Day Gigaton Company Launch Roadmap (2026-05-26 → 2026-06-24)

## 0. Scope clarification — what is and is not a "Gigaton company"

From `entity_ecosystem_registry.md` reconciled against `product_service_package_gigaton_ti_solutions.md`:

| Entity | Classification | Standalone revenue in this 30-day window? |
|---|---|---|
| **Gigaton AI** | PARENT-PLATFORM (multi-tenant SaaS spine; owner of the single Stripe account per B1) | **YES** — productized self-serve SaaS |
| **Ti Solutions** | MANAGED-SERVICE-DELIVERY arm (sells the same engines, Ti operates them on customer's behalf) | **YES** — managed-service wrapper |
| **Carmen Beach Properties** | OPERATOR (Gigaton tenant; STVR property mgmt in Playa del Carmen) | **YES** — guest-facing booking + operator demo case |
| **LiquiFex** | OPERATOR (Gigaton tenant; life-settlement OS; Todd is contractor, not equity owner) | **NO** — platform-ready but pre-pilot. Defer to v1.1. |
| **InContekst** | OPERATOR (Gigaton tenant; MMM SaaS; Sergei Veinberg is founder, not Todd) | **NO** — partner-engagement; not Todd's product to sell. Defer. |
| Multipli | PROSPECT — Ti Solutions CUSTOMER, not a Gigaton company | N/A — buys, doesn't sell |

**Entities launching as standalone revenue in this 30-day window: Gigaton AI, Ti Solutions, Carmen Beach Properties** (3 entities, not 5).

LiquiFex and InContekst remain platform-ready but **do not** get their own Stripe products, landing pages, or fulfillment SLAs in this window. Reasoning: (a) Todd is not the owner of either commercial relationship — selling them under the Gigaton Stripe account would be a fiduciary/contractual mess until pilot agreements convert; (b) per [[feedback_verify_production_state_before_planning]], shipping commerce ahead of contractual clarity is an anti-pattern.

---

## 1. Per-entity launch pages

### Entity #1 — Gigaton AI (parent-platform / self-serve SaaS)

| Field | Value |
|---|---|
| **Classification** | Parent-platform; multi-tenant SaaS; owner of the single platform Stripe account (B1) |
| **ICP** | (a) Solo operators or 1–5-person SMB teams running interaction-heavy businesses (STVR hosts, boutique sales orgs, single-property concierge brands, financial advisors); (b) triggering event: they just lost a $5–25K deal to a competitor because they couldn't respond fast enough or coherently across channels; (c) annual revenue $250K–$5M, willing to spend $200–$2K/mo on AI tooling, comfortable connecting OAuth |
| **Product** | "Gigaton SaaS" — universal-connector subscription. The Interactive Experience Builder bundle (designed today) is the headline output: operator describes their brand → Gigaton generates a deployable interactive brand experience (chat + WhatsApp + landing page) + the connector hub + Penrose scoreboard + persona engine + decision engine routing |
| **Pricing model** | Hybrid subscription + per-deal (B2 + B4 compliant). **Starter** $99/mo — 1 brand, 5 connectors, 50 bundles/mo. **Operator** $499/mo — 3 brands, unlimited connectors, 250 bundles/mo, WhatsApp on. **Scale** $1,999/mo — 10 brands, unlimited everything, custom domain, SLA. Plus per-deal $5/bundle for overages above tier cap |
| **Sales motion** | Self-serve signup; Stripe Checkout (test mode wk 1, live wk 2); product-led onboarding via the existing 10-stage chat-first manifest |
| **Landing page** | `https://gigaton.ai` (apex) and `https://app.gigaton.ai` (signup). Hero: *"The universal connector + intelligence layer for any brand that lives by interactions."* Demo asset: 60-sec Loom of an operator generating an interactive experience bundle in <3 min. Pricing: 3-tier table. CTA: "Start free trial" → Stripe Checkout |
| **Stripe products (test mode wk 1)** | `prod_gigaton_saas_starter` ($99/mo recurring), `prod_gigaton_saas_operator` ($499/mo), `prod_gigaton_saas_scale` ($1999/mo), `prod_gigaton_bundle_overage` ($5 metered), `prod_gigaton_custom_domain` ($49/mo add-on). Price IDs follow convention `price_<entity>_<sku>_<currency>_<cadence>` |
| **Fulfillment SLA** | Signup → tenant provisioned in <2 min (gateway + UAE namespace + decision-engine operator preset auto-created). Bundle generation: median <60s; p95 <3 min. SLA miss → automatic 1-week service credit posted to Stripe wallet |
| **Support channel** | In-app chat (Gigaton chat surface itself — dogfood) routes to Slack `#gigaton-support`; secondary `support@gigaton.ai` |
| **T&C / privacy minimum** | (1) ToS at `/legal/tos`, (2) Privacy at `/legal/privacy` (GDPR + CCPA baseline), (3) DPA available on request, (4) Acceptable Use Policy, (5) Stripe Tax enabled per B5, (6) cookie consent banner. Use Termly or Iubenda templates and have a paralegal review before live-mode |
| **KPIs** | **Leading**: signup-to-first-bundle conversion (target ≥40% within 24h), trial-to-paid (target ≥10%), connector activation rate (target ≥2 connectors/user/wk). **Lagging**: MRR (target $2K by 2026-06-24), gross churn (target <8% monthly), bundles/day (target 25 by 2026-06-15, 50 by 2026-06-22). Query method: BigQuery sink of HME events + Stripe webhook table joined in dashboard |

### Entity #2 — Ti Solutions (managed-service delivery arm)

| Field | Value |
|---|---|
| **Classification** | Managed-service-delivery arm of the joint Gigaton+Ti package. CxGuy is the brand persona. Operates Gigaton on customers' behalf |
| **ICP** | Mid-market companies ($5M–$100M revenue) running outbound sales / B2B financing / vendor programs / BPO operations that want the Gigaton outcome WITHOUT operating it themselves. Triggering event: failed in-house build, or sales-ops leader leaving, or vendor-growth target missed two quarters in a row. **First named target: Multipli** (vendor-financing, prospect since 2026-05-22) |
| **Product** | "Vendor Growth Engine" / "Outbound Operating System" / "Interaction Management as a Service" — Gigaton platform + Ti operators running it + monthly strategy reviews + custom integration work + outcome guarantees on funded-contract / qualified-meeting volume |
| **Pricing model** | Hybrid per-package + per-deal performance (B2 + B4 compliant). Setup package $40K (one-time, Stripe Invoice). Monthly retainer $8K–$25K based on scope. Performance: $500–$1,500 per incremental funded contract OR 5–10% incremental net revenue for 18mo |
| **Sales motion** | Sales-assisted; Todd (or designate) runs discovery → scoping → contract → kickoff. Stripe Invoices, not Checkout, for the $40K setup. Recurring monthly via Subscription Invoice |
| **Landing page** | `https://tisolutions.co` (or `https://ti.gigaton.ai` as cheap alt — see User decisions §3). Hero: *"Predictably profitable interaction management — operated for you."* Demo asset: the Multipli vendor-growth-engine bundle (6-file deliverable) as a sanitized case study. Pricing: "Custom — book a call". CTA: "Book a 30-min scoping call" → Calendly |
| **Stripe products (test mode wk 1)** | `prod_ti_setup_package` ($40,000 one-time), `prod_ti_retainer_starter` ($8000/mo), `prod_ti_retainer_growth` ($15000/mo), `prod_ti_retainer_scale` ($25000/mo), `prod_ti_performance_funded_contract` ($1000 unit metered). Invoice-based (not Checkout) |
| **Fulfillment SLA** | Kickoff within 7 days of contract signature; first deliverable within 14 days; monthly cadence calls on a fixed weekday; outcome reports within 5 business days of month-end. SLA miss → next-month retainer prorated credit |
| **Support channel** | Dedicated Slack Connect channel per customer; named Ti operator; weekly standup; `cxguy@tisolutions.co` for async |
| **T&C / privacy minimum** | Master Services Agreement template (DocuSign), per-engagement Statement of Work, Mutual NDA, DPA. Stripe Tax per B5. Same `/legal/*` stack as Gigaton if served from `ti.gigaton.ai`; otherwise standalone legal pages on `tisolutions.co` |
| **KPIs** | **Leading**: scoping calls/wk (target ≥3), proposals out/wk (target ≥1), avg deal cycle (target <30 days). **Lagging**: signed MRR (target $8K by 2026-06-24), avg contract value (target ≥$60K with performance), customer count (target ≥1 paid by 2026-06-08, ≥2 by 2026-06-22). Query method: HubSpot + Stripe Invoice webhook + manual deal-log Sheet until automation lands |

### Entity #3 — Carmen Beach Properties (operator / first paying tenant + demo case)

| Field | Value |
|---|---|
| **Classification** | Operator (Gigaton tenant); STVR property management; serves both as first paying Gigaton tenant AND as the public reference case |
| **ICP** | (a) Guests booking STVR in Playa del Carmen ($150–$800/night, 2–7 night stays, US/Canada/EU origin); (b) property owners considering letting Carmen Beach manage inventory (10–40% commission on net revenue) |
| **Product** | **Guest-side**: vacation stays at managed properties (existing). **Owner-side**: property management service (acquisition, marketing, dynamic pricing, talent costing, dashboards — all powered by Gigaton). The Interactive Experience Builder generates the per-property landing page + WhatsApp concierge bundle |
| **Pricing model** | **Guest**: per-night rate × stay length + cleaning fee + Stripe Tax (B5). Per-deal cadence (B4). **Owner**: 20% commission on net booking revenue, invoiced monthly. Both via Stripe under the platform account using `application_fee_amount` or Stripe Connect-style accounting (see User decisions §3) |
| **Sales motion** | **Guest**: self-serve via direct.carmenbeach.com (cuts OTA commission); SEO + paid + WhatsApp inbound. **Owner**: sales-assisted; Todd/Ti rep walks owner through property economics model |
| **Landing page** | `https://carmenbeach.com` (consumer-facing booking) + `https://owners.carmenbeach.com` (owner acquisition). Hero (guest): *"Stay in Playa del Carmen — concierge-managed, instantly responsive."* Demo asset: per-property Matterport 3D tour + the interactive WhatsApp experience generated by the Builder. CTA: "Check availability" → direct booking flow |
| **Stripe products (test mode wk 1)** | `prod_cbp_stay_<property_slug>` (per-property, variable price), `prod_cbp_cleaning_fee` (one-time $80), `prod_cbp_damage_deposit` ($300 auth/release), `prod_cbp_owner_commission` (metered — 20% of monthly net revenue). Use Stripe Checkout + Customer Portal |
| **Fulfillment SLA** | Booking confirmation email + WhatsApp within 5 min; check-in instructions 24h pre-arrival; in-stay issue response <30 min during business hours; refund decisions within 48h. Owner monthly report by the 5th of following month. SLA miss → goodwill credit (guest) or 10% commission discount that month (owner) |
| **Support channel** | WhatsApp Business primary (Twilio + mimi-whatsapp); `concierge@carmenbeach.com` secondary; Spanish + English |
| **T&C / privacy minimum** | Guest booking terms (cancellation, damage, conduct), Spanish-language lease contract (existing), privacy + cookie banner, Stripe Tax for Mexican VAT + US guest jurisdictions per B5, payment processing disclosure |
| **KPIs** | **Leading**: direct-booking inquiry/wk (target ≥10), inquiry-to-booking conversion (target ≥25%), WhatsApp response time (target <5 min median). **Lagging**: direct-channel revenue/mo (target $5K by 2026-06-24), occupancy rate (target ≥65%), owner NPS (target ≥40). Query method: Stripe + Penrose decision-engine scoreboard + HME events |

---

## 2. Four-week macro roadmap

### Week 1 — 2026-05-26 → 2026-06-01 (DEPLOY FREEZE; design + test mode + landing + content)

**Theme:** No production deploys. All commerce work done in Stripe TEST mode, landing pages on staging subdomains, contracts in draft.

| Item | Owner | Definition of Done |
|---|---|---|
| Stripe account confirmed live + Stripe Tax enabled (B5) | Todd | Single platform Stripe account active under Gigaton legal entity; Tax registered for US + MX + EU baseline; webhook endpoint pointing at gigaton-engine staging |
| All 14 Stripe products + price IDs created in test mode (5 Gigaton + 5 Ti + 4 CBP) | Gigaton agent fleet | All 14 products visible in Stripe Test dashboard; price IDs committed to `gigaton-engine/config/stripe_test_catalog.yaml` |
| Billing module scaffolded in gigaton-engine (B3) | Gigaton agent fleet | `gigaton-engine/billing/` module with Stripe client, product catalog loader, webhook handler skeleton; tests passing in CI |
| 3 landing pages drafted on staging subdomains (`staging.gigaton.ai`, `staging.tisolutions.co`/`staging-ti.gigaton.ai`, `staging.carmenbeach.com`) | Gigaton UI agent + Todd copy review | Each page renders hero + demo placeholder + pricing + CTA; CTA goes to Stripe test Checkout |
| Legal scaffold v0 — ToS, Privacy, AUP, DPA template for each entity | Todd + paralegal review | Pages live at `/legal/*` on each staging domain; reviewed by counsel before going live wk 2 |
| Interactive Experience Builder bundle (designed in parallel today) integrated as the demo asset on each entity's landing | Bundle workstream + UI agent | One generated bundle embedded as the public demo on `staging.gigaton.ai/demo` and linked from Ti + CBP pages |
| DNS for `gigaton.ai`, `tisolutions.co` (if separate), `carmenbeach.com` confirmed + apex routes published | Todd | `dig +short` returns expected A/AAAA/CNAME; SSL certs issued on all 3 apex domains |
| Founder + Owner sign-off on launch order + pricing (see User decisions §3) | Todd + Matt | Decisions recorded in `master-knowledge-base/decisions/2026_05_27_launch_order_signoff.md` |
| Content: 1 case study (Carmen Beach), 1 pitch deck (Ti Solutions managed service), 1 product walkthrough video (Gigaton SaaS) | Todd + Bella | Drafts in Drive; reviewed by Matt; published end of week |

**Risks + mitigations:**
- Risk: deploy-freeze breached because a sibling agent pushes during the week → Mitigation: gate the `production` GitHub environment to require Todd manual approval for all 3 entities' repos until 2026-06-02.
- Risk: Stripe Tax registration takes longer than 1 week for some jurisdictions → Mitigation: launch wk 2 with US + MX only; add EU progressively.
- Risk: Legal scaffold not reviewed in time → Mitigation: use Termly/Iubenda templates as v0; paralegal review can land mid-wk 2 without blocking test-mode launches.

### Week 2 — 2026-06-02 → 2026-06-08 (deploy resume; entity #1 paid live; first paid customer)

**Theme:** Carmen Beach goes first (lowest legal complexity, real recurring inquiries already flowing) — first revenue lands here. Gigaton SaaS Starter goes live in test→prod toggle mid-week.

| Item | Owner | DoD |
|---|---|---|
| Stripe test → live mode flip for Carmen Beach products + webhook signing keys rotated to live | Todd + Gigaton agent | Live mode products mirror test; first $1 test charge succeeds end-to-end; rollback playbook documented |
| `carmenbeach.com` direct-booking flow live with Stripe Checkout + WhatsApp confirmation hook | Gigaton UI + mimi-whatsapp | Real guest can book without OTA intermediary; booking event emits to HME; Penrose `direct_channel_revenue` metric increments |
| Gigaton SaaS Starter live in production (test → live) for the first 5 invited beta operators | Gigaton agent + Todd | 5 OAuth-completed signups, all 5 reach first generated bundle, ≥1 converted to paid Starter ($99) |
| Ti Solutions outbound campaign launched (Multipli #1, plus 2 lookalikes) | Todd (CxGuy) | Outreach sent; ≥3 scoping calls booked for wk 3 |
| Support channels wired: Slack `#gigaton-support`, `support@gigaton.ai` autoforward, WhatsApp Business for CBP | Gigaton agent + Bella | First-response SLA monitoring live in HME `supervisor_alerts` |
| KPI dashboard v0 live | Gigaton agent | Dashboard at `https://app.gigaton.ai/admin/kpis` shows MRR / signups / bundles/day / direct-booking revenue, refreshed hourly |

**Risks + mitigations:**
- Risk: Live-mode webhook signature verification fails → Mitigation: validate the signature loop end-to-end on Friday wk 1 in test mode using `stripe trigger` CLI.
- Risk: First paying customer hits an SLA bug on bundle generation → Mitigation: keep wk 2 paid signups invite-only (5 cap); manual escalation channel.

### Week 3 — 2026-06-09 → 2026-06-15 (scale entity #1; entity #2 launches; first 25/day bundles)

| Item | Owner | DoD |
|---|---|---|
| Gigaton SaaS public signup open (remove invite gate) | Gigaton agent | Public `app.gigaton.ai/signup`; ≥10 self-serve trials; ≥3 paid conversions |
| Ti Solutions first signed contract executed | Todd | DocuSign returned-complete; $40K setup invoice paid in Stripe; kickoff scheduled |
| Bundle generation throughput hits 25/day sustained | Gigaton agent fleet | Penrose `bundles_per_day` ≥25 for 3 consecutive days |
| Per-entity dashboards split out + cross-entity revenue dashboard live | Gigaton agent | `/admin/kpis?entity=gigaton|ti|carmen-beach` filters work; cross-entity revenue rollup live |
| Customer-success runbook executed for first 5 paying customers (NPS check at day 7) | Bella | NPS responses logged; first churn-risk flag (if any) raised; product-improvement issues filed |

**Risks + mitigations:**
- Risk: Bundle 25/day throughput requires LLM cost > budget cap → Mitigation: drift sentinel rule on `llm_call_cost`; downgrade to gpt-4o-mini above cap; user-visible budget bar.
- Risk: First Ti customer kicks off but Gigaton platform tenant provisioning has gaps → Mitigation: dry-run the tenant provisioning sequence for a "ti-demo" operator in wk 2.

### Week 4 — 2026-06-16 → 2026-06-22 (50/day bundles; multi-entity revenue; SLA tracking live; ≥1 sale per entity)

| Item | Owner | DoD |
|---|---|---|
| Bundle generation 50/day sustained | Gigaton agent | Penrose `bundles_per_day` ≥50 for 5 consecutive days |
| ≥1 paid customer for each of the 3 entities | Todd + Bella | Stripe revenue ≥$1 from each entity-Customer-tagged record |
| SLA tracking automated — auto-credit on SLA miss | Gigaton agent | Test SLA-miss scenario triggers automatic Stripe credit_note within 24h |
| Multi-entity revenue dashboard published to Founder + Owner weekly | Gigaton agent | Monday-morning auto-email with last-7-day revenue per entity, MRR delta, churn, NPS |
| First retro: what slipped, what to defer to v1.1 (LiquiFex + InContekst commercial launches) | Todd + Matt | Retro doc committed at `master-knowledge-base/retros/2026_06_22_30_day_retro.md`; v1.1 backlog seeded |
| Beta-launch graduation: move from "beta" to "v1.0 generally available" labeling on landing pages if KPI gates met | Todd | Hero copy update; press post; first batch of public testimonials |

**Risks + mitigations:**
- Risk: 50/day breaks LLM cost ceiling → Mitigation: cap per-operator daily bundle quota; offer "bundle pack" Stripe SKU for overage.
- Risk: Only 1–2 of 3 entities have paid customers by 2026-06-22 → Mitigation: not a launch-blocker; document honestly in retro; carry to month 2.

---

## 3. Top 5 user decisions needed (Founder + Owner)

1. **Is Ti Solutions a separate LLC or DBA under Turtle Island Solutions?** This determines whether `tisolutions.co` runs on its own Stripe sub-account (rejected by B1) or whether Ti Solutions is invoiced AS the Gigaton Stripe Customer that receives revenue and remits Ti's share to Todd. Recommended: DBA under Gigaton AI legal entity to honor B1 single-Stripe-account.
2. **Which entity launches first as easiest revenue — Carmen Beach (real existing inquiry flow) or Gigaton SaaS (most prepared codebase)?** Recommendation: **Carmen Beach first** (wk 2 Mon), then Gigaton SaaS (wk 2 Wed), then Ti Solutions (wk 3). Rationale: CBP has live demand; Gigaton needs trial-to-paid conversion which takes days.
3. **Domain strategy for Ti Solutions** — own apex (`tisolutions.co`, ~$15/yr but separate brand) or subdomain (`ti.gigaton.ai`, free but blurs the dual-brand positioning). Recommendation: **standalone apex** because the product+service-package memo deliberately keeps both brands distinct.
4. **Stripe Connect vs application_fee on Carmen Beach owner payouts** — owners take 80% of net booking revenue. Do we use Stripe Connect (each owner becomes a Connect account, automatic split) or run owners as suppliers and pay them out manually monthly? Connect is more correct but adds setup friction per owner. Recommendation: **manual payouts via Stripe Invoice for the first 3 owners**, migrate to Connect in v1.1 once SLA + volume justify it.
5. **LiquiFex + InContekst — do we hold them at "platform-ready" or do we cut them in?** They're currently registered as operators but not commercialized by Todd. Recommendation: **hold to v1.1 (post-2026-06-24)** until pilot agreements are signed AND the commercial relationship with their respective principals (Kevin Marston / Sergei Veinberg) is contractually clear. Selling either under the Gigaton Stripe account without that contract = fiduciary risk.

---

## 4. Top 3 blockers to address NOW

1. **Legal scaffold not yet drafted.** No ToS / Privacy / AUP / DPA exists on any of the 3 entity domains. Cannot take external customer payment without ToS + Privacy at minimum. **Action this week:** use Termly or Iubenda to draft v0 for all 3 domains; queue a paralegal review for wk 1 Fri.
2. **Single platform Stripe account (B1) status uncertain.** Memory does not confirm whether the Gigaton AI legal entity has a verified, Tax-registered Stripe account today, or whether it is still in onboarding. **Action this week (Monday 2026-05-26 first thing):** verify state at <https://dashboard.stripe.com/account>; complete identity verification; enable Stripe Tax in US + MX baseline.
3. **DNS + apex domain ownership** for `gigaton.ai`, `tisolutions.co`, `carmenbeach.com` is partially complete per [[session_handoff_2026_05_22_beta_launch_sprint_complete]] (api.gigaton.ai still pending Search Console verification per RESUME_HERE_2026_05_23), and `tisolutions.co` + `carmenbeach.com` apex strategy is unconfirmed. **Action this week:** GoDaddy/Cloudflare audit on all 3 apexes; confirm A/AAAA + SSL; resolve any pending verifications before Stripe Checkout pages are linked from these domains.

---

## 5. Compliance with locked architectural decisions

- **B1 honored:** all 14 Stripe products live under one platform Stripe account; entities are Stripe Customer records tagged with `entity_id ∈ {gigaton, ti_solutions, carmen_beach}`.
- **B2 honored:** every product is either a package (subscription) or a deal (one-time/metered) — no blended multi-product pricing units.
- **B3 honored:** billing module scaffolded in `gigaton-engine/billing/` wk 1; no billing logic anywhere else.
- **B4 honored:** per-deal Stripe events (booking, bundle overage, performance bonus) emit to HME on each transaction; per-package events emit on subscription create/update/cancel.
- **B5 honored:** every Checkout Session + Invoice creation call sets `automatic_tax: {enabled: true}`; Stripe Tax registered in jurisdictions per launch order.

---

## 6. Out of scope for this 30-day window (carry to v1.1)

- LiquiFex commercial launch (Stripe products, landing, pricing)
- InContekst commercial launch (same)
- Gignet affiliate-network platform (Chapter 11) — separate workstream, ≥90 days
- Multipli commercial close (subject to wk 1 Tue beta deliverable acceptance) — Ti revenue flows through this but does not require a separate entity launch
- Stripe Connect rollout to Carmen Beach owners (manual payouts wk 4 until volume justifies)
- Public press / launch announcement (queue for wk 4 if KPIs hold)
