# Stripe Webhook Test Harness

## Local flow
1. Run backend on port 3002.
2. Run Stripe CLI listen with `--forward-to localhost:3002/api/payments/webhooks/stripe`.
3. Capture the webhook signing secret from CLI output.
4. Put that secret into `STRIPE_WEBHOOK_SECRET`.
5. Trigger events with Stripe CLI.

## Expected result
- verified webhook payload accepted
- normalized payment event persisted
- failed signatures rejected
