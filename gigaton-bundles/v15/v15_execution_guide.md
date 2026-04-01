# V15 Execution Guide

## Primary upgrades
1. Add SQL migration files that can be merged into a larger application migration chain.
2. Replace the in-memory assumptions with a SQL-backed repository everywhere.
3. Add real HTTP scaffolding for Poynt token exchange and order/transaction routes.
4. Add a Stripe webhook test harness using local forwarding and event triggering.
5. Add a recent-payments table and payment-events table in the UI.

## Recommended rollout order
1. Merge migrations into your app migration runner.
2. Wire the SQL repository into the payments service.
3. Set Stripe webhook signing secret and run local webhook harness.
4. Set Poynt credentials and validate token exchange.
5. Validate event persistence and UI refresh.
