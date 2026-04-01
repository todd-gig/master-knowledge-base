# Gigaton V14 Real Provider Execution Package

This package completes the next logical production step after v13 by moving from provider scaffolding toward real provider execution architecture.

## What v14 adds
- SQL migrations for payments tables
- production-grade raw-body Stripe webhook route pattern
- real Poynt token exchange and request scaffolding
- retry + failover telemetry model
- tenant-level provider policy admin model
- operational notes for production implementation

## Core architecture
- one orchestration layer
- Stripe as the default online rail
- GoDaddy/Poynt as the secondary provider adapter
- no provider-specific leakage into app code
