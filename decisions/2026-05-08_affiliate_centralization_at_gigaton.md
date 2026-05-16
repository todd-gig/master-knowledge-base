---
title: Decision — Centralize affiliate management at Gigaton platform (SIE chain 22), tenants consume
date: 2026-05-08
decided-by: Todd
status: ACTIVE — implementation begins this deploy window
supersedes: per-tenant affiliate models in Carmen-Beach-Properties (deprecated, see "PDC migration plan" below)
---

# Architecture

```
gigaton (company)
  └── gigaton-platform (UI/UX, methodology, served at gigaton-platform.web.app / gigaton.app)
       ↑
       │ consumes affiliate APIs
       │
   gignet (the platform that affiliates plug INTO)
       │ owned by SIE chain 22 (affiliate-program)
       ↓
       └── tenants (PDC, Liquefex, future clients)
              └── attribute their bookings/conversions to gignet affiliates
              └── do NOT own affiliate state — they consume it
```

**Single source of truth for affiliate state lives in SIE.** Tenants attribute conversions; they don't own the affiliate.

# What canonicalizes at SIE chain 22

SIE already owns:
- `affiliate_codes` (migration 023) — per-user deterministic 8-char referral code
- `affiliate_invites` (migration 023) — invite lifecycle: sent → clicked → signed_up → onboarded → activated
- `contact_authorizations` (migration 023) — per-user × per-channel consent
- `runtime_chains/affiliate.py` (534 lines) + `runtime_chains/contact_auth.py` — the runtime
- 7 endpoints under `/operator/affiliate/*` and `/operator/contact-auth/*` (live in production)

SIE adds (migration 027, this deploy window):
- `affiliate_agreements` — proposal + signoff + content hash + KMS-signed metadata
- `affiliate_kyc` — Stripe Connect account ID + verification state per affiliate
- `affiliate_state` column on `affiliate_codes` — state machine: `pending → agreement_signed → kyc_verified → active`
- `affiliate_terms` — per-tenant, per-tier commission % and override rates (replaces the per-tenant local schema)

# What tenants own (per-tenant, NOT canonicalized at SIE)

Tenants like PDC own:
- **Attribution events** — "this booking on my platform was attributed to gignet affiliate `XYZ123`"
- **Tenant-specific commission events** — what THIS booking owes the affiliate
- **Tenant-specific payout records** — money that flowed FROM this tenant to the affiliate

Tenants do NOT own:
- The Affiliate identity (name, email, tier, KYC, agreement) — that's SIE
- The Affiliate's referral code — SIE issues one canonical code per affiliate
- Multi-tier ladder relationships — that's gignet network, lives in SIE
- Stripe Connect account — Gigaton platform owns the Stripe Connect platform; affiliates onboard once, get paid by all tenants

# The 6 deliverables in flight (per scope ask)

| # | Deliverable | Where | Estimate | This deploy window |
|---|---|---|---|---|
| 1 | ProposalGenerator service (template engine + KMS hash) | SIE: `runtime_chains/affiliate_signoff.py` + KMS adapter | 1 day | scaffold + endpoint contract live; KMS real-call deferred |
| 2 | SignoffCapture UI + backend endpoint | Gigaton-UI-Platform `/affiliate/onboarding` + SIE endpoint | 1 day | full UI; backend captures hash but skips KMS-sign in v1 |
| 3 | Stripe Connect Express onboarding wiring | SIE: `runtime_chains/affiliate_signoff.py` Stripe adapter | 0.5 day | endpoint contract live; returns mock URL; real Stripe SDK call in next deploy |
| 4 | Cloud Storage + KMS plumbing | SIE: `services/operator-api/src/integrations/gcs.py` + `kms.py` | 0.5 day | `gcs.py` + `kms.py` modules with TODO-real-call markers |
| 5 | Affiliate state machine | SIE migration 027 + `affiliate_signoff.py` transitions | 0.5 day | full DB + Python state-transition logic |
| 6 | Tests + docs | SIE `tests/contract/test_affiliate_signoff.py` + chain 22 v2 spec | 0.5 day | contract tests against the stubs; live-integration tests deferred |

**This deploy window ships:** state machine + DB + endpoint contracts + frontend UX. The integration with Stripe Connect API + Cloud KMS + Cloud Storage real calls happens in deploys over the next 4–5 days.

This means a non-Gigaton org CAN start the onboarding flow tonight, but real KYC + cryptographic signing + GCS-stored agreements activate as the integrations land.

# PDC migration plan

PDC's local affiliate models become a **thin attribution layer**. Existing models are deprecated, not deleted (preserves PR #4 / #3 work).

## Phase 1 (this deploy window — non-breaking)
- **Add deprecation marker** comments to PDC's `Affiliate`, `AffiliateOrganization`, `AffiliateInvite` models in `packages/db/prisma/schema.prisma`. They keep functioning, marked as transitional.
- Architecture doc landed (this file).

## Phase 2 (next 1–2 deploys)
- PDC `AttributionRecord` gains `gignet_affiliate_id` field — links to SIE's canonical code.
- PDC booking creation also writes a `commission_event` to SIE's `/operator/affiliate/commission/record` endpoint (new, ships with chain 22 v3).
- New PDC bookings start using gignet's affiliate IDs for new attribution.

## Phase 3 (PDC Wednesday deploy 2026-05-13 or later)
- Backfill: existing `Affiliate` rows in PDC migrate to gignet (or are abandoned if low volume).
- PDC's `Affiliate` / `AffiliateOrganization` / `AffiliateInvite` tables drop.
- `CommissionEvent` and `Payout` in PDC become tenant-scoped attribution records that reference gignet affiliate IDs by string FK (no relational FK to gignet — different DB).

## Phase 4 (post-multi-tenant)
- Liquefex onboards as tenant #2; consumes the same gignet affiliate IDs without writing any affiliate code.

# Decision tier

- **D-class**: D2 (reversible architectural shift; deprecation markers don't break tenant behavior)
- **T-class required**: T2 (architectural change)
- **Cert chain**: QC (data integrity through migration), VC (preserves all existing PR #3/#4 affiliate work), TC (PDC existing affiliates must not break)

# Open questions answered

| Q | Answer |
|---|---|
| What about existing PDC Affiliates with active referrals? | None known to be active in production yet. Phase 3 migration covers backfill if any exist by then. |
| Is the per-tenant commission rate moved to SIE? | Yes — `affiliate_terms` table at SIE keyed by `(tenant_id, tier)`. Tenants advertise their rates by writing terms; SIE enforces. |
| Can a non-Gigaton org sign up directly without an existing Gigaton invite? | Yes — that's the goal of this work. The new `/operator/affiliate/onboard/start` endpoint accepts any signed-in user; KYC happens via Stripe Connect Express; agreement happens in our UI. |
| Where does the agreement PDF live? | Cloud Storage bucket `gigaton-affiliate-agreements`, encrypted at rest, KMS-signed metadata. Object key: `agreements/{affiliate_id}/{agreement_version}.pdf`. |
| What jurisdiction's e-signature law applies? | Default to US ESIGN Act + UETA; affiliate's residency captured at signoff for jurisdictional override. |

# Rollback

Per-piece, all reversible:
- Migration 027 is additive — `DROP TABLE` reverts safely.
- Frontend route `/affiliate/onboarding` can be unmounted by removing one line in `App.tsx`.
- Chain 22 v2 endpoints can be unregistered without affecting v1 chain 22 (already in production).
- PDC deprecation comments are documentation-only; don't change behavior.
