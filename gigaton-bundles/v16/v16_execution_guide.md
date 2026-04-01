# V16 Execution Guide

## Primary upgrades
1. Add real outbound HTTP execution scaffolding for Poynt token and transaction/order calls.
2. Add reconciliation logic to detect payment status drift between local records and provider state.
3. Add webhook replay tooling for operational recovery.
4. Add search and filter support in the payments UI.
5. Add provider health metrics and failure-rate dashboard views.

## Recommended rollout order
1. Merge V16 migrations into the main app migration chain.
2. Wire SQL repository plus telemetry endpoints.
3. Validate Poynt token exchange and request execution in a non-production environment.
4. Enable reconciliation job on a schedule.
5. Enable webhook replay tooling for operators.
6. Roll out payment search/filter UI and provider health dashboard.
