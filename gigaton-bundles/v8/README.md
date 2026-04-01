# Gigaton Claude Project Bundle v8

This is the production-readiness-oriented v8 package.

## What v8 adds
- OpenAPI 3.1 spec
- Stricter JSON-schema-style request validation rules
- Integration test scaffold
- Secrets handling patterns
- Observability stack scaffolds
- Blue-green deployment support
- Readiness and liveness healthchecks
- Deployment promotion and rollback playbooks

## Objective
Move the v7 hardening package into a more production-ready operating baseline with clearer contracts, safer deployments, better diagnostics, and stronger validation.

## Fast path
1. Review `deployment_guide.v8.md`
2. Review `openapi/openapi.yaml`
3. Review `backend/lib/validation_schemas.js`
4. Run migrations and tests
5. Use `deploy/docker-compose.observability.yml` for local observability
6. Use `deploy/blue-green/` for staged production rollout patterns
