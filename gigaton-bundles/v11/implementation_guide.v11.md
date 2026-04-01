# Implementation Guide v11

## Architecture decision
Use a provider-agnostic payment service with pluggable adapters.

## Why this is the right next step
If you wire your product directly to Stripe or directly to GoDaddy-specific request shapes, you create switching cost, duplicated webhook logic, and future refactor tax.

This package reduces that by creating:
- one internal payment intent model,
- one checkout/session creation interface,
- one billing event emission path,
- one webhook normalization path.

## Recommended default
- Use `StripeAdapter` for online checkout and cards first.
- Use `GoDaddyPoyntAdapter` for GoDaddy-connected payment flows.
- Use the provider selector in `payment_provider_registry.json`.

## Integration sequence
1. Fill out `.env.example` values.
2. Implement `/api/payments/create-session`.
3. Implement `/api/payments/webhooks/:provider`.
4. Persist normalized payment events in the database.
5. Route commercial lifecycle events into billing hooks.
