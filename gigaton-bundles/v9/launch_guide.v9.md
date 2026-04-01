# Launch Guide v9

## Launch readiness flow
1. Apply migrations and seed baseline data.
2. Run backend unit tests.
3. Run integration test runner against the target environment.
4. Validate OpenAPI contract alignment.
5. Confirm alerts are loaded and observability is healthy.
6. Generate or refresh SDK clients from the OpenAPI contract.
7. Run blue-green cutover gate checks.
8. Cut traffic only if all launch gates pass.
9. Preserve rollback readiness for immediate reversal.

## Minimum launch gates
- health and readiness green
- integration tests green
- no critical validation errors
- no cutover gate failure
- alert rules active
- rollback plan ready
