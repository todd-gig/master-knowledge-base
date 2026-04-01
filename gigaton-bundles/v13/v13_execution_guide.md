# V13 Execution Guide

## What changed from v12
- Stripe adapter now includes real webhook verification wiring pattern.
- Poynt adapter now includes JWT-bearer token acquisition scaffolding.
- Repository moved from in-memory placeholder to SQL repository contract.
- Dashboard supports polling-based live refresh for payment lookup.
- Failover policy is now tenant-aware and use-case aware.

## Business rule
The rest of the product must still only talk to `PaymentService`.
No UI, billing, approval, or tenant code may depend directly on Stripe or Poynt request/response shapes.

## Recommended deployment order
1. Set Stripe secret + webhook secret.
2. Set Poynt application ID, private key PEM, business ID, and base URL.
3. Initialize SQL schema for payments.
4. Run backend.
5. Run payments dashboard.
6. Test Stripe webhook verification locally.
7. Test Poynt token acquisition against your credentials.
