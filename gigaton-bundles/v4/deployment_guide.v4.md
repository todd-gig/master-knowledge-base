# Deployment Guide v4

## Objective
Deploy a Claude project with:
- global doctrine memory
- client-specific overlays
- calibrated retrieval
- lifecycle-governed memory operations
- a starter ops dashboard

## Deployment flow
1. Upload root JSON and markdown files into the Claude project.
2. Set `system_prompt_contract.v4.md` as the main instruction layer.
3. Use `claude_bootstrap.v4.md` as the startup layer.
4. Generate client namespaces from `client_intake_form.schema.json` + `automated_namespace_generator.json`.
5. Store retrieval feedback using `retrieval_feedback_dataset.template.json`.
6. Review and promote weight changes only after holdout evaluation.
7. Use lifecycle states to manage memory maturity and retirement.

## High-ROI operating model
- Standardize onboarding.
- Reduce retrieval drift.
- Govern memory quality.
- Create operator visibility through the dashboard scaffold.
