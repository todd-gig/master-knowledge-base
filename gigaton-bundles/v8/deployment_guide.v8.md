# Deployment Guide v8

## Stack target
- Claude project for reasoning and instruction layering
- Backend service for auth, validation, mutation control, and write-back
- Persistent SQL database managed by migrations
- Dashboard as the operator control plane
- CI pipeline for tests and deployment checks
- Observability stack for metrics and logs
- Blue-green deployment pattern for lower-risk releases

## Production-readiness flow
1. Apply SQL migrations from `database/migrations/`
2. Seed baseline data with `database/seed.json`
3. Run unit and integration tests
4. Validate API against `openapi/openapi.yaml`
5. Configure secrets via `.env.example` + secrets manager pattern
6. Run backend + observability stack locally using `deploy/docker-compose.observability.yml`
7. Promote releases with the blue-green workflow in `deploy/blue-green/`
8. Roll back using the rollback playbook if health or correctness degrades

## Risk reduction logic
- OpenAPI reduces interface ambiguity.
- Stricter schemas reduce bad writes.
- Integration tests reduce cross-layer regressions.
- Secrets patterns reduce accidental exposure.
- Observability reduces blind spots.
- Blue-green rollout reduces deployment blast radius.
