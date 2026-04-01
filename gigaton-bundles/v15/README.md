# Gigaton V15 Payments Real Calls Package

This package completes the next practical step after v14.

## Scope
- real outbound HTTP client scaffolding for Poynt token exchange and orders/transactions APIs
- real Stripe webhook endpoint test harness notes and local test scripts
- SQL migrations shaped to merge into a main app migration chain
- payments UI table for recent payments and payment events

## Core architecture
- one orchestration layer
- Stripe as the default online rail
- GoDaddy/Poynt as the secondary provider adapter
- no provider-specific leakage into app code
