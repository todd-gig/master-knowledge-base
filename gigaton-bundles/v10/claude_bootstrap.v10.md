# Claude Bootstrap v10

## Canonical files
- memory_registry.v10.json
- source_catalog.v10.json
- client_intake_form.schema.json
- namespace_generator.config.json
- retrieval_scoring_calibration.json
- memory_lifecycle_state_machine.json
- governance_promotion_pipeline.json
- openapi/openapi.yaml
- billing/billing_model.json
- tenancy/tenant_isolation_model.md

## Execution defaults
- Use weighted retrieval.
- Use lifecycle state gating.
- Use namespace generation from intake data.
- Require approval-gated write-back for production changes.
- Require strict validation and transactions for all mutations.
- Require tenant isolation, billing hooks, and deployment automation for commercial paths.
- Prefer runnable and testable artifacts over static specs.
