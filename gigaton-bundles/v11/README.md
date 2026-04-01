# Gigaton V11 Payments Abstraction Package

This package is the next implementation step for supporting payments through either Stripe or GoDaddy with the least possible integration churn.

## Goal
Create one internal payment orchestration layer with:
- a single payment interface
- provider adapters for Stripe and GoDaddy
- a normalized payment object model
- consistent webhook handling
- consistent tenant scoping
- provider-specific env templates
- low-friction provider switching at runtime

## Recommended rollout
1. Start with the unified `backend/lib/payments/` layer.
2. Use Stripe first for online checkout if speed matters.
3. Use the GoDaddy adapter when your GoDaddy/Poynt environment is ready.
4. Keep your app talking only to the unified service contract, never directly to provider SDK details.
