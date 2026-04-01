# Webhook Verification

## Stripe
`stripe.webhooks.constructEvent(...)` is wired into the Stripe adapter and requires the raw request body plus `STRIPE_WEBHOOK_SECRET`.

## GoDaddy / Poynt
This package includes the auth/token scaffolding and normalized webhook path, but final production verification should be completed against your exact Poynt environment rules.
