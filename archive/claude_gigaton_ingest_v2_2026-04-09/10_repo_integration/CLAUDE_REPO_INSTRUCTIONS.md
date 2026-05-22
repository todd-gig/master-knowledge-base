# Claude Repo Integration Instructions

## Before Code
Run a full repo inspection.

## Generate These Files Internally Before Implementation
- repo_map.md
- current_architecture.md
- env_var_inventory.md
- route_inventory.md
- data_model_inventory.md
- integration_inventory.md
- gap_matrix.md
- first_pr_plan.md

## Code Rules
- Follow existing style.
- Use existing libraries when adequate.
- Avoid duplicate frameworks.
- Do not introduce unnecessary dependencies.
- Add adapters for external providers.
- Preserve stable APIs unless migration is documented.

## Git Rules
- One coherent change per PR.
- Include tests or validation notes.
- Include rollback notes for risky changes.
