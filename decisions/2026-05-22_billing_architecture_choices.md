---
adr_id: 2026-05-22-billing_architecture_choices
title: Gigaton platform billing — architecture choices required before any code
status: PARTIALLY ACCEPTED — 4/5 gates locked; B5 (tax) pending confirmation
date: 2026-05-22
accepted_at: 2026-05-22
accepted_by: todd@gigaton.ai
authors:
  - Claude (architecture intelligence pass)
reviewers:
  - todd@gigaton.ai
serves: foundational_goal_gigaton_engineered_brand_experience
ppim_economics: this ADR governs how the platform turns intelligence into revenue
related:
  - "[[master_project_plan]]"
  - "[[universal_connector_hub_architecture]]"
  - "docs/architecture/CODEBASE_MAP.md"
  - "decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md"
---

> **DECISIONS LOCKED 2026-05-22 by todd@gigaton.ai:**
>
> - **B1 = Single platform Stripe account.** Operators are Stripe Customers within one Gigaton account.
> - **B2 = Per-product-and-service-package.** Billing model is NOT a global choice — each product/service package carries its own billing model. The platform supports flat-tier, usage-metered, hybrid, and (eventually) profit-influence-attributed pricing simultaneously, parameterized by the package.
> - **B3 = Inside `gigaton-engine`.** Cross-entity economics service becomes the home. Promotes gigaton-engine from lightly-used to substantively-used.
> - **B4 = Per-deal-and-package.** Invoice cadence is NOT global — each deal carries its locked-in cadence (auto-charge / net-30 / prepaid). Aligns with B2.
> - **B5 = Stripe Tax (PROPOSED per recommendation; awaiting user confirmation).** Auto Mode call: lowest-friction default. 0.5% volume cost; Mexico + US + EU well-covered.
>
> The B2/B4 meta-pattern means the implementation has TWO layers:
> 1. A **product/service catalog** (defines what is sold, on what model, on what cadence).
> 2. A **deal/subscription engine** (binds operator → package → locked terms).
>
> Stripe's native Products + Prices + Subscriptions data model already supports this. We mirror it into gigaton-engine Postgres for fast reads + cross-references + Penrose attribution hooks.


# ADR — Gigaton platform billing: architecture choices

## Context

Per `decisions/2026-05-22_claude_gigaton_ingest_reconciliation.md` §4, **platform-level billing is a genuine missing gap.** The user selected billing as one of two next priorities. Before writing any code, this ADR locks the architectural choices.

A read-only investigation across all 14 active repos confirmed:

### What exists already

- **Stripe credential connector** (`Carmen-Beach-Properties/apps/connector-api/src/lib/providers.ts` + `gigaton-ui-system/pages/ConnectorStripePage.tsx`, LIVE 2026-05-22): operators paste Stripe API keys; the platform validates via `GET /v1/account` and stores via Pattern A (`<operator_id>--stripe--<purpose>:latest` in Secret Manager). **This is for cost-reading attribution, not payment processing.**
- **Budget cap middleware** (`gigaton-gateway/api/middleware/budget_cap.py`, LIVE): per-operator daily USD ceiling; returns HTTP 402 when exhausted. **In-memory accumulator, no invoice.**
- **Affiliate payout schema stub** (`Carmen-Beach-Properties/packages/db/prisma/schema.prisma`): `Payout.stripeTransferId` field exists; explicit comment "Stripe Connect is wired into the schema but the actual transfer is manual until Sprint 7." **Operator-level, not platform-level.**
- **Booking financials** (Carmen Beach `Booking` model): `totalAmount`, `depositPaid`, `netToOwner` — all manual decimal fields. **No payment processor wired.**
- **Cost-attribution telemetry** (`ppeme/app/experience_engineering/models.py`): Stripe is one of several cost sources in the profitability model. **Read-only analytics.**

### What does NOT exist (verified by grep across all 14 repos)

- No `/webhooks/stripe` route.
- No charge / payment-intent / subscription creation code.
- No invoice generation service.
- No `STRIPE_PUBLISHABLE_KEY` env var.
- No `billing_profile` field on any seeded `client_namespace` (the field was referenced in the now-archived ingest package schema but never made it into production code).
- No platform-level invoice or revenue table.
- No tax / sales-tax / VAT calculation logic.
- No dispute / refund / chargeback handler.

### Two billing layers (must keep distinct)

| Layer | Who pays whom | Example | Owns it |
|---|---|---|---|
| **Platform** | Operator pays Gigaton | Carmen Beach pays Gigaton $X/mo for platform access | THIS ADR |
| **Operator** | Operator's customers pay operator | Guest pays Carmen Beach for a stay | Each vertical's own concern (Carmen Beach via Airbnb/VRBO payouts; not Gigaton's billing system) |

**This ADR addresses platform-level only.** Operator-level billing is out of scope: the existing affiliate payout schema + booking financial fields are owned by the vertical and remain there. Gigaton does NOT become a guest-payment intermediary.

---

## The 5 architectural decisions required

Each gate is a binary or short-list choice with downstream consequences. **No code is written until all 5 are answered.**

---

### Gate B1 — Stripe Connect or single platform account?

**Choice.**

| Option | What it means | Pros | Cons |
|---|---|---|---|
| **B1.a — Single platform Stripe account** | Gigaton has one Stripe account. Each operator is a Customer in that account. Gigaton bills operators directly. | Simplest. Fastest to ship. Standard SaaS pattern. No KYC complexity passed to operators. | Gigaton holds all the money briefly; tax/1099 obligations centralized on Gigaton; no clean separation per operator. |
| **B1.b — Stripe Connect (Standard accounts)** | Each operator creates/links their own Stripe account via OAuth. Gigaton takes a platform fee on top via `application_fee_amount`. | Clean fiduciary separation. Operators see their own payments. 1099 burden lighter for Gigaton. Future-proof for marketplace. | More setup friction. OAuth flow + onboarding required per operator. Gigaton must handle Connect-account events. |
| **B1.c — Stripe Connect (Custom/Express)** | Gigaton manages the underlying Stripe accounts on operators' behalf. | Lowest operator friction. Gigaton owns the UX entirely. | Gigaton becomes a regulated money-services-business in some jurisdictions. KYC/AML burden grows. Heavy. |

**Recommendation.** **B1.a (single platform account).** Reasons: (1) the current 4 operators are first-party (Carmen Beach is Todd's, etc.) — Connect's fiduciary separation is overkill; (2) the existing Stripe credential connector reads operator-owned Stripe accounts for cost attribution, which is a separate concern from billing; (3) you can migrate to Connect later if/when third-party operators are onboarded — single-account → Connect is a known migration path. Start simple.

**Open sub-questions if B1.a is chosen:** none — it's the simplest path.

**Open sub-questions if B1.b/c is chosen:** Standard vs Express? OAuth scope? How does Connect interact with the existing per-operator credential connector?

---

### Gate B2 — What is the billing model?

**Choice.**

| Option | What it means | Pros | Cons |
|---|---|---|---|
| **B2.a — Flat monthly subscription tier** | Operator pays $X/month. Tier determines feature ceiling (rate limit, engines unlocked, support level). | Predictable revenue. Simple invoice. Standard SaaS. | Doesn't capture variable cost (LLM calls, storage, message volume). |
| **B2.b — Pure usage-based metering** | Operator pays per API call / per LLM token / per WhatsApp message. Invoice generated monthly from accumulated meters. | Aligns cost with value. Existing `budget_cap` + `llm_call_cost` telemetry are already metering. | Invoice unpredictability scares operators. Hard to forecast cash flow. |
| **B2.c — Hybrid: base tier + usage overage** | $X/mo base (includes N calls) + $Y per call over N. | Best of both. Operators get predictability AND aligned cost on growth. Industry standard for AI/SaaS hybrids. | More complex invoice. Two meters per operator. Slightly higher implementation cost. |
| **B2.d — % of revenue influence** | Gigaton takes X% of measured profit influence (Penrose attribution). | Maximally aligned. Operator only pays when Gigaton produces measurable value. | Hard to defend the attribution math externally. Cash flow lumpy. Audit-heavy. Only works once attribution is rock-solid. |

**Recommendation.** **B2.c (hybrid: base + usage).** Reasons: (1) `budget_cap` + LLM `cost_telemetry` + the 4-operator presets already give us the metering substrate — we'd build on existing data; (2) the base tier covers cost-of-service even for a slow month; (3) operators understand the model intuitively; (4) it migrates cleanly to B2.d later if/when Penrose attribution is defensible.

**Open sub-questions if B2.c is chosen:** what are the tiers ($/mo + included N)? Where does the overage rate come from? Who sets these — Todd directly, or codify into `gigaton-engine` per-operator preset?

---

### Gate B3 — Where does the billing service live?

**Choice.**

| Option | What it means | Pros | Cons |
|---|---|---|---|
| **B3.a — Inside `user-access-engine` (UAE)** | UAE already owns operator/tenant/`client_namespace`. Billing is a natural extension of identity. | Single source of truth for who-can-do-what AND who-pays-what. Reuses UAE's Cloud SQL + Alembic + auth. | Couples auth changes to billing changes. Larger blast radius per deploy. |
| **B3.b — New `billing-engine` service** | Net-new Cloud Run service, own repo, own Postgres. | Clean separation. Independent deploy cadence. Standard microservice pattern. | Net-new repo + GCP plumbing. 9 engines → 10. Adds an integration surface. |
| **B3.c — Inside `gigaton-gateway`** | Gateway already does rate-limit + budget cap. Adding invoice generation extends that. | Co-located with the meters that feed invoice. Minimal new infra. | Gateway becomes a fat service. Mixing routing concerns with billing concerns. |
| **B3.d — Inside `gigaton-engine`** | Cross-entity economics already lives here. Billing is the operator-Gigaton economic edge. | Conceptually correct — `gigaton-engine` is the economics engine. | Currently lightly used; would need significant build-out. |

**Recommendation.** **B3.a (UAE).** Reasons: (1) billing is fundamentally an identity-adjacent concern (who is this entity? what tier? what payment method? what invoice address?); (2) UAE already has Cloud SQL + Alembic + the sign-off matrix that gates approval-required actions (billing changes are an approval category); (3) the existing `client_namespaces` table is the natural anchor for `billing_profile` — and the ingest package's schema already hints at this co-location even if the field was never built; (4) adds 2-3 tables to UAE instead of standing up a new service.

**Open sub-questions if B3.a is chosen:** does the meter aggregation (LLM cost, request count) get periodically rolled up from `gigaton-gateway`'s Firestore `llm_call_cost` collection into UAE Postgres, or does UAE query Firestore directly at invoice-generation time?

---

### Gate B4 — Invoice trigger + cadence?

**Choice.**

| Option | What it means | Pros | Cons |
|---|---|---|---|
| **B4.a — Monthly invoice generated 1st of month, due net-30** | Standard B2B SaaS cadence. | Predictable. Operator-friendly. | Lumpy cash flow. Up to 60-day collection lag. |
| **B4.b — Monthly auto-charge to stored card on 1st of month** | Stripe Customer + saved payment method; auto-debit. | Fastest cash. Lower DSO. | Requires card on file; less B2B-friendly for larger operators. |
| **B4.c — Prepaid credits topped up via invoice or auto-recharge** | Operator buys $X credits up-front; usage debits the balance; low-balance auto-tops up via Stripe. | Excellent cash flow. Operators self-manage. Aligns with budget_cap pattern. | Operators must front cash. Refunds get complex. |

**Recommendation.** **B4.b (auto-charge monthly)** for current first-party operators, with **B4.c (prepaid credits)** as the option for any future self-serve operator. B4.b mirrors Anthropic/OpenAI's own pattern. The current budget_cap middleware is already a soft preview of credit-bucket logic.

**Open sub-questions if B4.b is chosen:** what happens on a failed charge — degrade service immediately, or grace period?

---

### Gate B5 — Tax + compliance scope?

**Choice.**

| Option | What it means | Pros | Cons |
|---|---|---|---|
| **B5.a — Stripe Tax handles it** | Stripe automatically calculates sales tax / VAT based on operator's billing address. We collect; we remit (or Stripe remits in supported jurisdictions). | Lowest implementation cost. Stripe is a Merchant of Record in many jurisdictions. | Costs 0.5% of transaction volume. Not all jurisdictions covered. |
| **B5.b — Manual jurisdiction-by-jurisdiction** | Gigaton calculates + remits taxes itself. | Cheaper at scale. | Massive compliance burden. Not viable for a 2-person company. |
| **B5.c — Use a Merchant of Record (Paddle, LemonSqueezy)** | They become the seller-of-record; they handle all tax + invoicing. | Zero tax burden on Gigaton. Operators see Paddle/LS, not Stripe. | Higher fees (5-8%). Branding awkward. Can't easily migrate off. |

**Recommendation.** **B5.a (Stripe Tax).** Reasons: (1) you're already planning to use Stripe (per B1); (2) 0.5% on early-stage volume is rounding error; (3) Mexico (Carmen Beach is in MX), US, and most early customer jurisdictions are well-supported; (4) you can migrate to B5.c later if compliance scope explodes, but you can't easily migrate the other way.

**Open sub-questions if B5.a is chosen:** 1099 reporting for affiliates (Carmen Beach's payout schema) is a SEPARATE concern, not blocked by this gate — that's operator-level and stays with the Carmen Beach vertical.

---

## Decision template (fill in to unblock)

```
Gate B1 (Connect vs single): _____
Gate B2 (billing model):     _____
Gate B3 (where it lives):    _____
Gate B4 (invoice cadence):   _____
Gate B5 (tax + compliance):  _____

Notes / overrides: _____
```

---

## File-level implementation plan (REVISED for locked decisions)

Locked: **B1.a single + B2 package-driven + B3 gigaton-engine + B4 deal-driven + B5 Stripe Tax (pending confirm).** This reframes the plan around a **catalog + deal** architecture inside `gigaton-engine`, with Stripe as the source-of-truth for Products/Prices/Subscriptions, mirrored locally for fast reads + Penrose attribution hooks.

### Critical pre-requisite — gigaton-engine adopts Cloud SQL

gigaton-engine currently has **NO Postgres instance**. Implementing billing there requires provisioning + adopting Alembic *first*. This becomes a third storage adoption alongside DEE + EO. It runs in parallel with EO (different repo, no dependency).

| Step | Detail |
|---|---|
| Provision `gigaton-engine-pg` Cloud SQL | In `carmen-beach-properties` GCP project (matches current engine placement; do NOT mix with the gigaton-platform migration which is a separate ADR). `db-custom-1-3840`, same shape as DEE. |
| Bootstrap Alembic + `start.sh` + Cloud SQL wiring | Mirror the EO Phase B pattern exactly (see `runbooks/2026_05_22_storage_flip_dee_eo_plan.md` §5). |
| `0001_baseline.py` | Empty baseline — no pre-existing tables to capture. |

**Important caveat.** gigaton-engine lives in `carmen-beach-properties` GCP project (historical drift; anti-pattern #4/7 in `[[repo_registry]]`). Building billing on top of misplaced infra is acceptable for now — the project migration ([[gcp_project_organization_target_2026]]) handles relocation later as a separate work item. Do NOT entangle the two.

### Phase 1 — gigaton-engine catalog data layer (~1.5 days)

| File | Change |
|---|---|
| `gigaton-engine/alembic/versions/0002_billing_catalog.py` (NEW) | Catalog tables: `product` (product_id PK, slug, name, description, stripe_product_id, status, ppim_brand_dimension, created_at). `package` (package_id PK, product_id FK, slug, name, billing_model ENUM {flat, usage_metered, hybrid, profit_attributed}, description, status). `price` (price_id PK, package_id FK, stripe_price_id, unit_amount NUMERIC, currency, interval ENUM {month, year, one_time, usage}, usage_type ENUM nullable {metered, licensed}, tier_definition JSONB nullable, status). Indexes on stripe_product_id, stripe_price_id, slug. |
| `gigaton-engine/alembic/versions/0003_billing_deals.py` (NEW) | Deal tables: `deal` (deal_id PK, operator_id, package_id FK, price_id FK, cadence ENUM {auto_charge_monthly, invoice_net_30, prepaid_credits, custom}, status ENUM {draft, active, paused, terminated}, stripe_subscription_id nullable, effective_from, effective_to, signed_by, signed_at, terms_overrides JSONB, ppim_signature JSONB). `deal_term_override` (deal_id FK, key, value JSONB) — for one-off custom terms outside the package defaults. Indexes on operator_id, stripe_subscription_id, status. |
| `gigaton-engine/alembic/versions/0004_billing_meters_invoices.py` (NEW) | Runtime tables: `meter_event` (event_id PK UUID, operator_id, deal_id FK, package_id FK, meter_kind {llm_tokens, api_calls, whatsapp_messages, profit_attribution, custom}, units NUMERIC, source ENUM {gateway, ppeme, manual}, source_ref, occurred_at). `invoice` (invoice_id PK, operator_id, deal_id FK, period_start, period_end, subtotal NUMERIC, tax NUMERIC, total NUMERIC, currency, status ENUM {draft, open, paid, void, uncollectible}, stripe_invoice_id, created_at, finalized_at, paid_at). `invoice_line_item` (line_id PK, invoice_id FK, price_id FK, description, quantity NUMERIC, unit_amount NUMERIC, amount NUMERIC, meter_event_window JSONB). `payment_method` (payment_method_id PK, operator_id, stripe_payment_method_id, brand, last4, exp_month, exp_year, is_default, created_at). Indexes on operator_id, deal_id, status, stripe_invoice_id, occurred_at. |
| `gigaton-engine/api/models/billing/__init__.py` (NEW) | Pydantic shapes mirroring all of the above. Separate request/response models per route. |
| `gigaton-engine/api/services/billing/catalog.py` (NEW) | `CatalogService` — CRUD on Product / Package / Price; writes go to Stripe first (`stripe.Product.create`, `stripe.Price.create`), then mirrored to Postgres. Reads from Postgres for speed. Webhook re-syncs handle drift. |
| `gigaton-engine/api/services/billing/deals.py` (NEW) | `DealService` — `create_deal(operator_id, package_id, price_id, cadence, terms_overrides)` creates the Stripe Subscription (or schedules first invoice for non-subscription cadences) and persists the deal row. `terminate_deal`, `pause_deal`, `list_deals_for_operator`. |
| `gigaton-engine/api/services/billing/meters.py` (NEW) | `MeterService` — `record(meter_kind, operator_id, units, source, source_ref)`. Idempotent on `source_ref`. For `usage_metered` and `hybrid` packages, also pushes the meter to `stripe.SubscriptionItem.create_usage_record`. |
| `gigaton-engine/api/services/billing/invoices.py` (NEW) | `InvoiceService` — `generate_for_deal(deal_id, period_end)` reads deal terms + accumulated meters, computes line items, creates Stripe Invoice (or charges via auto-charge cadence). |

### Phase 2 — Stripe adapter + webhooks (~1 day)

| File | Change |
|---|---|
| `gigaton-engine/api/integrations/stripe_client.py` (NEW) | Thin wrapper around the Stripe Python SDK. Single entry point that reads `STRIPE_SECRET_KEY` from env (Secret Manager-mounted). Includes retry + idempotency-key support. |
| `gigaton-engine/api/routes/webhooks_stripe.py` (NEW) | `POST /v1/webhooks/stripe` — handles `product.*`, `price.*`, `customer.subscription.*`, `invoice.*`, `payment_method.*`, `charge.dispute.created`. Verifies signature against `STRIPE_WEBHOOK_SIGNING_SECRET`. Idempotent on Stripe `event_id` (store in a `stripe_event` ledger table; if seen, ack and skip). |
| `gigaton-engine/tests/test_stripe_adapter.py` (NEW) | Mocked Stripe client; verifies signature verification + idempotency + each event-handler branch. |
| `gigaton-engine/tests/test_billing_e2e.py` (NEW) | Spins up testcontainer Postgres; exercises catalog → deal → meter → invoice flow end-to-end with Stripe mocked. |
| Secret Manager `gigaton-platform`: `stripe-secret-key` (NEW empty slot — Pattern A) | Operator pastes key after slot exists; AX-024 mitigation. |
| Secret Manager `gigaton-platform`: `stripe-webhook-signing-secret` (NEW empty slot — Pattern A) | Same. Operator gets signing secret from Stripe dashboard after webhook endpoint is registered. |
| `gigaton-engine/cloudbuild.yaml` | Add `--update-secrets=STRIPE_SECRET_KEY=stripe-secret-key:latest,STRIPE_WEBHOOK_SIGNING_SECRET=stripe-webhook-signing-secret:latest`. **Deploy in two passes:** first pass creates the slots (above) WITHOUT binding; operator pastes; second pass adds the bindings + redeploys. |

### Phase 3 — Catalog + Deal CRUD endpoints (~0.5 day)

| File | Change |
|---|---|
| `gigaton-engine/api/routes/catalog.py` (NEW) | `GET/POST/PATCH /v1/catalog/products`, `GET/POST/PATCH /v1/catalog/packages`, `GET/POST/PATCH /v1/catalog/prices`. Gated by UAE sign-off matrix `category=billing` for mutations. |
| `gigaton-engine/api/routes/deals.py` (NEW) | `POST /v1/deals` (create), `GET /v1/operators/{id}/deals`, `GET /v1/deals/{id}`, `POST /v1/deals/{id}/pause`, `POST /v1/deals/{id}/terminate`. Sign-off-gated for mutations. |
| `gigaton-engine/api/routes/invoices.py` (NEW) | `GET /v1/operators/{id}/invoices`, `GET /v1/invoices/{id}`, `POST /v1/invoices/{id}/refund` (sign-off-required). |
| `gigaton-engine/api/routes/meters.py` (NEW) | `POST /v1/meters` (internal — called by gateway rollup + ppeme attribution job), `GET /v1/operators/{id}/meters?from=&to=`. |

### Phase 4 — Cross-engine wiring (~0.5 day)

| File | Change |
|---|---|
| `gigaton-gateway/api/services/meter_emitter.py` (NEW or MODIFIED if exists) | Daily Cloud Scheduler `meter-rollup-from-gateway-daily` reads `gateway` Firestore `llm_call_cost` for prior day → POSTs to `gigaton-engine /v1/meters` with `meter_kind=llm_tokens`. |
| `ppeme/api/services/profit_attribution_emitter.py` (NEW) | When ppeme finalizes a Penrose profit-attribution event, POSTs to `gigaton-engine /v1/meters` with `meter_kind=profit_attribution` for packages using `profit_attributed` billing model. |
| `user-access-engine/api/services/clients/billing_client.py` (NEW thin client) | UAE reads gigaton-engine `/v1/operators/{id}/deals?status=active` to determine which capabilities are unlocked. Cached 5min. |
| `decision-engine/drift_sentinel/axioms.yaml` | Add **AX-024 (proposed)**: operator with NO `active` deal → `gigaton-engine` services return 402 Payment Required. Add **AX-025 (proposed)**: operator with active deal but `invoice.status=uncollectible` → degrade to read-only after 14d grace. Drift sentinel flags violations. |

### Phase 5 — Cloud Scheduler jobs (~0.25 day)

| Job | Schedule | Purpose |
|---|---|---|
| `meter-rollup-from-gateway-daily` | `0 6 * * *` UTC | Pull prior day's LLM costs from Firestore → meters. |
| `meter-rollup-from-ppeme-daily` | `30 6 * * *` UTC | Pull prior day's profit attributions → meters (for profit_attributed packages). |
| `invoices-generate-billing-period` | `0 7 * * *` UTC | For each active deal, check if billing period closed today; if yes, generate invoice. Cadence-aware (monthly deals close 1st of month; weekly close on day-of-week; etc.). |
| `invoices-collect-overdue` | `0 8 * * *` UTC | Retry failed auto-charge invoices on day +1/+3/+7; after +14d mark `uncollectible` + emit AX-025-triggering signal. |

### Phase 6 — FE: catalog admin + operator billing surface (~1 day)

| File | Change |
|---|---|
| `gigaton-ui-system/src/pages/AdminCatalogPage.tsx` (NEW) | At `/admin/catalog`. Founder/admin only. CRUD on Products + Packages + Prices. Live preview of Stripe representation. |
| `gigaton-ui-system/src/pages/AdminDealsPage.tsx` (NEW) | At `/admin/deals`. Create + sign deals per operator. Picks package + price + cadence + overrides. Surfaces sign-off matrix. |
| `gigaton-ui-system/src/pages/BillingPage.tsx` (NEW) | At `/billing`. Operator view: active deals + next invoice estimate + invoice history + payment method. |
| `gigaton-ui-system/src/pages/BillingPaymentMethodPage.tsx` (NEW) | Stripe Elements for adding card. |
| `gigaton-ui-system/src/api/billing.ts` (NEW) | Client for gigaton-engine billing endpoints. |
| Nav rail | Add `/billing` to the appropriate tier-gated circle (per `onboarding_v1.yaml`); `/admin/catalog` + `/admin/deals` to founder rail. |

### Phase 7 — HME event types + governance (~0.25 day)

| File | Change |
|---|---|
| `human-management-engine/api/events.py` | Add 8 event types: `ProductCreated`, `PackageCreated`, `PriceCreated`, `DealCreated`, `DealActivated`, `InvoiceFinalized`, `InvoicePaid`, `InvoicePaymentFailed`. |
| `decision-engine/drift_sentinel/axioms.yaml` | AX-024 + AX-025 as described in Phase 4. |

### Stripe Tax (B5) — pending user confirmation

If confirmed: enable Stripe Tax in the Stripe dashboard; set `automatic_tax: {enabled: true}` on every invoice creation in `gigaton-engine/api/integrations/stripe_client.py`. No additional Gigaton-side code beyond that flag. Register Stripe Tax in operating jurisdictions (US, Mexico, EU as needed).

If rejected — fall back: add `tax_amount` field to `invoice` + a manual tax-rule table; we calculate ourselves. Estimated +2 days, ongoing compliance burden.

### Out of scope (for this build)

- Stripe Connect / marketplace flows (deferred until third-party operators arrive).
- Refund/dispute UX beyond the basic `POST /v1/invoices/{id}/refund` route (handle case-by-case via Stripe dashboard initially).
- Coupons / promo codes / discounts (extend `price` table later with `discount_id` FK).
- Affiliate revenue share — operator-level concern; Carmen Beach `Payout` schema stays untouched.
- The `gigaton-engine` GCP project migration to `gigaton-platform` ([[gcp_project_organization_target_2026]]) — separate work item.

### Estimated total (revised)

- **gigaton-engine SQL adoption (prerequisite)**: ~0.5 day (mostly copy-paste from EO Phase B pattern; empty baseline). 
- **Phase 1** (catalog data layer): ~1.5 days.
- **Phase 2** (Stripe adapter + webhooks, two-pass deploy): ~1 day.
- **Phase 3** (CRUD endpoints): ~0.5 day.
- **Phase 4** (cross-engine wiring): ~0.5 day.
- **Phase 5** (Cloud Scheduler): ~0.25 day.
- **Phase 6** (FE): ~1 day.
- **Phase 7** (HME events + axioms): ~0.25 day.
- **TOTAL**: ~5.5 elapsed days (up from ~3.5 in the original recommendation stack — the catalog + deal layer + gigaton-engine SQL adoption add 2 days).
- **~9 PRs** across gigaton-engine + gigaton-ui-system + gigaton-gateway + ppeme + decision-engine + HME.
- **2 net-new Secret Manager slots** + **1 net-new Cloud SQL instance** + **4 net-new Cloud Scheduler jobs**.

---

## Consequences

- **Positive.** Gigaton becomes capable of collecting platform revenue. The 9-engine fleet starts paying for itself rather than running on operator-funded infra. Unlocks B2 metric of "predictably profitable" in PPIM.
- **Negative.** Operators see their first Gigaton invoice — a UX moment that needs to be smooth or it undermines trust. Stripe Tax adds 0.5% to costs (acceptable). UAE grows by ~4 tables and ~10 routes.
- **Risk.** Empty-secret-slot deploy failures (AX-024 / gateway PR #37 lesson). Mitigation: never bind `STRIPE_SECRET_KEY` to UAE Cloud Run until the operator has actually pasted the key; deploy in two passes.

## Rollback

- All Phase 1 migrations have `downgrade()`. Stripe Customer records persist (cleanup manual via dashboard if needed). Webhooks idempotent — replaying is safe.
- Cloud Scheduler jobs can be paused without code change.

## Approval gates

- [x] **B1** — Single platform Stripe account. **LOCKED 2026-05-22.**
- [x] **B2** — Per-product-and-service-package (not a global model; each package carries its own). **LOCKED 2026-05-22.**
- [x] **B3** — Inside `gigaton-engine`. **LOCKED 2026-05-22.**
- [x] **B4** — Per-deal-and-package (not a global cadence). **LOCKED 2026-05-22.**
- [ ] **B5** — Stripe Tax. **PROPOSED per recommendation; awaiting user confirm.**
- [ ] **First product catalog entry** — what does the first Product/Package look like? (Open for input. Suggest defining one default package per active operator: Carmen Beach STR, LiquiFex, InContekst, Ti Solutions consulting.)
- [ ] **First operator to bill** — Carmen Beach, or one of the others, or a synthetic test customer first?
- [ ] User approves the revised file-level implementation plan above.
- [ ] User approves provisioning `gigaton-engine-pg` Cloud SQL instance in `carmen-beach-properties` project.
