---
adr_id: 2026-05-22-billing_architecture_choices
title: Gigaton platform billing — architecture choices required before any code
status: AWAITING DECISION — 5 gates open
date: 2026-05-22
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

## What gets built once all 5 are answered

Conditional on B1.a + B2.c + B3.a + B4.b + B5.a (my recommendation stack), here is the file-level implementation plan that will follow. **Not committed to until the gates are answered** — if the user picks a different stack, the plan changes accordingly.

### Phase 1 — UAE billing data layer (~1 day)

| File | Change |
|---|---|
| `user-access-engine/alembic/versions/00NN_billing.py` (NEW) | Tables: `billing_profile` (1:1 with `client_namespace`), `billing_meter` (rollup of `gigaton-gateway` Firestore meters; period_start/period_end/operator_id/meter_kind/units/unit_cost), `invoice` (operator_id/period/subtotal/tax/total/status/stripe_invoice_id), `invoice_line_item`, `payment_method` (operator_id/stripe_pm_id/last4/brand/is_default). |
| `user-access-engine/api/models/billing.py` (NEW) | Pydantic shapes for above. |
| `user-access-engine/api/services/billing/__init__.py` (NEW) | `BillingService` — `get_billing_profile`, `upsert_billing_profile`, `record_meter`, `generate_invoice`, `list_invoices`. |
| `user-access-engine/api/routes/billing.py` (NEW) | Endpoints: `GET/PATCH /v1/operators/{id}/billing-profile`, `POST /v1/operators/{id}/payment-methods`, `GET /v1/operators/{id}/invoices`, `GET /v1/invoices/{id}`. All gated by UAE sign-off matrix for `category=billing`. |

### Phase 2 — Stripe integration adapter (~1 day)

| File | Change |
|---|---|
| `user-access-engine/api/integrations/stripe.py` (NEW) | Thin adapter — `create_customer`, `attach_payment_method`, `create_invoice`, `finalize_invoice`, `pay_invoice`. Reads `STRIPE_SECRET_KEY` from Secret Manager. |
| `user-access-engine/api/routes/webhooks_stripe.py` (NEW) | `POST /v1/webhooks/stripe` — handles `invoice.paid`, `invoice.payment_failed`, `customer.updated`, `charge.dispute.created`. Idempotent via Stripe event_id. |
| `user-access-engine/tests/test_stripe_adapter.py` (NEW) | Mocked Stripe client; verifies idempotency + retry. |
| Secret Manager: `stripe-secret-key`, `stripe-webhook-signing-secret` (NEW) | Two new secret slots in `gigaton-platform` GCP project. **Pattern A storage — create slot empty, operator pastes key, only then re-deploy.** Avoids the AX-024 empty-slot deploy failure from gateway PR #37. |
| Cloud Run env: `--update-secrets=STRIPE_SECRET_KEY=stripe-secret-key:latest,STRIPE_WEBHOOK_SIGNING_SECRET=stripe-webhook-signing-secret:latest` on UAE | After paste. |

### Phase 3 — Meter rollup from gateway (~0.5 day)

| File | Change |
|---|---|
| `user-access-engine/api/services/billing/meter_rollup.py` (NEW) | Cloud Scheduler job runs daily at 06:00 UTC; queries `gateway` Firestore `llm_call_cost` for prior day; aggregates per operator; writes `billing_meter` rows. |
| `master-knowledge-base/runbooks/` | Add `billing_meter_rollup_failure.md` — what to do when daily rollup fails. |

### Phase 4 — Invoice generation cron (~0.5 day)

| File | Change |
|---|---|
| `user-access-engine/api/services/billing/invoice_generator.py` (NEW) | Cloud Scheduler job runs 1st of month 06:00 UTC; for each `client_namespace` with `billing_profile.status='active'`, calculates base + overage from `billing_meter`, calls Stripe to create+finalize invoice. |
| Cloud Scheduler: `billing-generate-invoices-monthly` (NEW) | `0 6 1 * *` |
| Cloud Scheduler: `billing-rollup-meters-daily` (NEW) | `0 6 * * *` |

### Phase 5 — FE: billing settings + invoice list (~0.5 day)

| File | Change |
|---|---|
| `gigaton-ui-system/src/pages/BillingPage.tsx` (NEW) | At `/billing`. Shows tier, current-period usage, next invoice estimate, payment method, invoice history. |
| `gigaton-ui-system/src/pages/BillingPaymentMethodPage.tsx` (NEW) | Stripe Elements for adding card. |
| `gigaton-ui-system/src/api/billing.ts` (NEW) | Thin client for UAE billing endpoints. |
| Nav rail | Add `/billing` to the appropriate tier-gated circle (per `onboarding_v1.yaml`). |

### Phase 6 — HME event types + governance (~0.25 day)

| File | Change |
|---|---|
| `human-management-engine/api/events.py` | Add 4 event types: `InvoiceCreated`, `InvoicePaid`, `InvoicePaymentFailed`, `PaymentMethodAttached`. |
| `decision-engine/drift_sentinel/axioms.yaml` | Consider adding axiom AX-024: "operator with `billing_profile.status=delinquent` must NOT receive new gigaton-engine work" (drift sentinel auto-flags violations). |

### Out of scope (for this build)

- Stripe Connect / marketplace flows (deferred to a future ADR if/when third-party operators arrive).
- Refund/dispute UX (handle case-by-case via Stripe dashboard for now; webhook just records state).
- Coupons / promo codes.
- Affiliate revenue share — operator-level concern; the existing `Payout` schema in Carmen Beach stays untouched.

### Estimated total

- ~3.5 elapsed days under the recommendation stack.
- ~5 PRs across UAE + gigaton-ui-system + (potentially) decision-engine for AX-024.
- 2 net-new Cloud Scheduler jobs.
- 2 net-new Secret Manager slots.

---

## Consequences

- **Positive.** Gigaton becomes capable of collecting platform revenue. The 9-engine fleet starts paying for itself rather than running on operator-funded infra. Unlocks B2 metric of "predictably profitable" in PPIM.
- **Negative.** Operators see their first Gigaton invoice — a UX moment that needs to be smooth or it undermines trust. Stripe Tax adds 0.5% to costs (acceptable). UAE grows by ~4 tables and ~10 routes.
- **Risk.** Empty-secret-slot deploy failures (AX-024 / gateway PR #37 lesson). Mitigation: never bind `STRIPE_SECRET_KEY` to UAE Cloud Run until the operator has actually pasted the key; deploy in two passes.

## Rollback

- All Phase 1 migrations have `downgrade()`. Stripe Customer records persist (cleanup manual via dashboard if needed). Webhooks idempotent — replaying is safe.
- Cloud Scheduler jobs can be paused without code change.

## Approval gates (binary)

- [ ] **B1** — Stripe Connect or single account? (Recommend: **B1.a single**)
- [ ] **B2** — Billing model? (Recommend: **B2.c hybrid base + usage**)
- [ ] **B3** — Where does it live? (Recommend: **B3.a inside UAE**)
- [ ] **B4** — Invoice cadence? (Recommend: **B4.b auto-charge monthly**)
- [ ] **B5** — Tax + compliance? (Recommend: **B5.a Stripe Tax**)
- [ ] **Tiers + pricing** for B2.c — what are the tier names, base prices, included quantities, overage rates? (Open for input.)
- [ ] **First operator to bill** — Carmen Beach, or one of the others, or a synthetic test customer first?
- [ ] User approves committing this ADR.
