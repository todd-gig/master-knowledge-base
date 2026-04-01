# Deployment Guide v7

## Stack target
- Claude project for reasoning and instruction layering
- Backend service for auth, validation, mutation control, and write-back
- Persistent SQL database managed by migrations
- Dashboard as the operator control plane
- CI pipeline for tests and deployment checks

## Hardening flow
1. Apply SQL migrations from `database/migrations/`
2. Seed baseline data with `database/seed.json`
3. Run backend tests and validation tests
4. Run generator tests and transaction tests
5. Deploy backend using `deploy/docker-compose.yml` or `deploy/k8s/`
6. Deploy dashboard with environment-specific API base URL
7. Gate production promotion on passing tests and operator approval

## Risk reduction logic
- Migrations reduce schema drift.
- Validation reduces bad write inputs.
- Transactions reduce partial state corruption.
- Tests reduce regression risk.
- Manifests reduce deployment ambiguity.
