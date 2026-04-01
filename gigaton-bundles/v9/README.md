# Gigaton Claude Project Bundle v9

This is the launch-readiness-oriented v9 package.

## What v9 adds
- Generated client SDK stubs from the OpenAPI contract
- Real request-schema validator wiring in backend middleware
- Runnable integration test script scaffold
- Correlation IDs for request tracing
- Alert rule manifests
- Automated blue-green cutover gate scripts
- Release checklist and launch playbook

## Objective
Move from production readiness to launch readiness by reducing manual release risk and tightening interface, test, and observability discipline.

## Fast path
1. Review `launch_guide.v9.md`
2. Review `openapi/openapi.yaml`
3. Review `backend/lib/request_validation_middleware.js`
4. Run `scripts/init_db_from_migrations.py`
5. Run `scripts/run_integration_tests.py`
6. Review `deploy/blue-green/cutover_gate.py`
7. Use `sdk/` stubs for client integration
