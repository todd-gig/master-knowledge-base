# V14 Execution Guide

## Objective
Turn the provider abstraction into a production-capable payments subsystem.

## Primary upgrades
1. SQL-backed persistence with migrations
2. raw-body Stripe webhook verification route separation
3. Poynt OAuth/JWT exchange scaffolding plus signed request flow structure
4. retry and failover telemetry emission
5. tenant policy admin surface for provider routing

## Recommended implementation order
1. Apply payment migrations
2. Wire SQL repository into your main backend
3. Put Stripe webhook route before JSON parsing middleware
4. Configure Stripe signing secret and test verified webhook handling
5. Configure Poynt credentials and validate token exchange
6. Enable retry/failover logs and counters
7. Expose tenant provider policy editing in the admin UI
