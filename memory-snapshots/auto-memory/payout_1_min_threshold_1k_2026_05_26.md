---
name: payout-1-min-threshold-1k-2026-05-26
description: "PAYOUT-1 amendment locked 2026-05-26 (Todd directive): platform-wide minimum payout threshold = $1,000 USD indefinitely. Applies to every Stripe Connect Express and ACH payout across every operator entity (Carmen Beach owners, Ti Solutions clients, Multipli vendors, Gigaton self, future entities)."
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  status: LOCKED — Todd directive
  scope: "every entity, every payment rail, indefinite"
  originSessionId: fc56c866-aa65-41d6-a729-1d21c8fe1dcb
promoted_from: payout_1_min_threshold_1k_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# PAYOUT-1 amendment — $1k min payout threshold (LOCKED 2026-05-26)

**Decision** (Todd, 2026-05-26 EOD):
> "Set minimum payout at 1k indefinitely"

## Scope

- **Threshold**: $1,000 USD minimum per payout
- **Duration**: indefinite (no sunset date)
- **Coverage**: every entity, every rail
  - Carmen Beach Properties owner payouts (Stripe Connect Express)
  - Ti Solutions retainer-client commission payouts
  - Multipli vendor-financing performance share payouts
  - Gigaton self payouts (rev share + equity)
  - Gignet affiliate payouts (when Gignet activates)
  - Any future operator entity

## How to apply

- **Stripe Connect Express config**: set `payout_schedule.minimum_amount = 1000_USD` (or equivalent currency-rounded threshold for non-USD operators per PAYOUT-1's currency-rounding rule).
- **ACH alternative path**: same $1k floor — accumulate balances below threshold; release on the next scheduled cadence when the running total clears.
- **Multi-currency**: convert $1k USD at payout time to operator's home currency, round per PAYOUT-1.
- **Sub-clients**: inherit parent operator's payout config unless explicitly overridden (e.g. CBP walking-tour DBA uses CBP's Stripe Connect Express account by default).

## Why $1k (interpretation)

The original PAYOUT-1 (2026-05-25) left "first-time exception" and "rounding direction" as open clarifications. Setting a floor at $1k:
- Removes ambiguity for the v1 Carmen Beach launch (owners with low monthly RevPAR don't get nuisance-volume micro-payouts)
- Standardizes Stripe payout fees relative to amount (the $1k floor keeps fees below ~1.5% of payout)
- Reduces audit/reconciliation overhead for Todd as the v1 sole operator (per OPS-1)
- Buyer-paid financing-fee model (Multipli) only generates net rev at higher transaction sizes anyway — $1k threshold doesn't suppress real flow

## Related decisions

- [[product_service_package_gigaton_ti_solutions]] — joint go-to-market (compensation routing)
- [[master_project_plan]] — Chapter 11 Gignet affiliate
- PAYOUT-1 (2026-05-25, original) — Stripe Connect Express + ACH alternative
- ARCH-1, ARCH-2 — gigaton-platform engines are the brain; entities consume the gateway
- OPS-1 — Todd does all v1 setup himself
