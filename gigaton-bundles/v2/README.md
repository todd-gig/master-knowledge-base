# Gigaton Claude Project Bundle v2

This bundle is the upgraded end-to-end project memory and operating layer for direct use in a Claude project.

## Core upgrade delta from v1
- Source provenance added
- Confidence scores added
- Supersession and deprecation logic added
- Client namespace overlay model added
- Governance and mutation rules added
- More explicit ingestion contract added

## Recommended upload order
1. `system_prompt_contract.v2.md`
2. `claude_bootstrap.v2.md`
3. `memory_registry.v2.json`
4. `memory_registry.v2.md`
5. `retrieval_policy.v2.json`
6. `project_operating_manual.v2.md`
7. `governance_policy.v2.md`
8. `client_namespace.template.json`

## Recommended Claude project setup
- Use `system_prompt_contract.v2.md` as the primary instruction layer.
- Use `claude_bootstrap.v2.md` as the startup primer.
- Keep `memory_registry.v2.json` as the canonical machine layer.
- Keep `memory_registry.v2.md` as the human audit and editing layer.
- Use the client namespace template to create per-client overlays without breaking global doctrine.
