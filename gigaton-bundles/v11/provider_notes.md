# Provider Notes

## Stripe
Use Checkout Sessions for hosted checkout and PaymentIntents when you need lower-level control.

## GoDaddy
This package assumes the developer-facing integration path is GoDaddy Poynt cloud APIs rather than consumer-only UI flows.

## Internal rule
Your app should never depend on provider-specific object shapes outside the adapter layer.
