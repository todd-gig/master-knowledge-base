# Payment Abstraction Test Plan

## Required tests
- selector returns Stripe by default
- selector can switch to GoDaddy/Poynt
- normalized result shape is identical across providers
- Stripe webhook normalizes into internal event
- GoDaddy/Poynt webhook normalizes into internal event
- billing mapping emits consistent commercial events
