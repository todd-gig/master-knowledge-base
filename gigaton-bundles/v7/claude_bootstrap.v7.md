# Claude Bootstrap v7

## Canonical files
- memory_registry.v7.json
- source_catalog.v7.json
- client_intake_form.schema.json
- namespace_generator.config.json
- retrieval_scoring_calibration.json
- memory_lifecycle_state_machine.json
- governance_promotion_pipeline.json

## Execution defaults
- Use weighted retrieval.
- Use lifecycle state gating.
- Use namespace generation from intake data.
- Require approval-gated write-back for production changes.
- Require validation and transactions for all mutations.
- Prefer runnable and testable artifacts over static specs.
