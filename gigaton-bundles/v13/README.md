# Gigaton V13 Payments Production Package

This package upgrades v12 into a production-oriented payments execution layer with:

- real Stripe webhook signature verification
- real Poynt auth/token flow scaffolding
- persistent SQL-backed payment repository
- payment status UI with live refresh
- provider failover rules by tenant and use case

## Core architecture
- one orchestration layer
- Stripe as the default online rail
- GoDaddy/Poynt as the secondary provider adapter
- no provider-specific leakage into app code

## Recommended rollout
1. Stand up the SQL-backed payments repository.
2. Use Stripe for hosted online checkout first.
3. Configure Poynt token/auth flow in parallel.
4. Route all status changes through normalized payment events.
5. Enable tenant-level provider failover rules only inside the orchestration layer.
