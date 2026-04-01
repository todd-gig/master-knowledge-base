# Claude Bootstrap v3

This project uses weighted retrieval and namespace overlays.

## Mandatory behavior
- Treat `memory_registry.v3.json` as the canonical memory layer.
- Treat `source_catalog.v3.json` as the provenance registry.
- Use `retrieval_policy.v3.json` for ranking.
- Use `namespace_inheritance_examples.json` as the overlay pattern reference.
- Use `client_onboarding_generator.json` to build new client overlays.

## Output default
Produce structured, reusable, machine-ingestible markdown and JSON artifacts.
