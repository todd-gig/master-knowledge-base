# Claude Bootstrap v9

## Canonical files
- memory_registry.v9.json
- source_catalog.v9.json
- client_intake_form.schema.json
- namespace_generator.config.json
- retrieval_scoring_calibration.json
- memory_lifecycle_state_machine.json
- governance_promotion_pipeline.json
- openapi/openapi.yaml

## Execution defaults
- Use weighted retrieval.
- Use lifecycle state gating.
- Use namespace generation from intake data.
- Require approval-gated write-back for production changes.
- Require strict validation and transactions for all mutations.
- Require healthcheck, observability, alerting, and cutover gates for launch paths.
- Prefer runnable and testable artifacts over static specs.
