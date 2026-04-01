# Provider Strategy

## Core decision
Stripe is the default online rail because it supports hosted Checkout Sessions and PaymentIntents directly.

## Secondary rail
GoDaddy/Poynt remains the secondary adapter so you can support that ecosystem without contaminating the rest of the app with provider-specific request/response shapes.

## Internal product rule
Never let UI, billing, approval workflows, or tenant logic depend directly on Stripe or Poynt object models.
