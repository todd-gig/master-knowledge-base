# Webhook Verification

## Stripe
Verify signatures using `STRIPE_WEBHOOK_SECRET` before trusting event payloads.

## GoDaddy / Poynt
Implement provider-authenticity verification using the finalized production credential flow once your environment is confirmed.

## Rule
Do not let unverified webhook bodies mutate billing or order state in production.
