# V13 Test Plan

## Required checks
- Stripe webhook verification rejects invalid signatures
- Stripe webhook verification accepts valid raw-body flow
- Poynt token scaffolding generates JWT-bearer assertion payload
- SQL repository persists and reloads tenant-scoped payments
- live refresh UI polls only when enabled
- failover rules apply by tenant and use case
