# Auth and RBAC

## Roles
- `admin`: full access including promotion, billing event submission, and state transitions
- `reviewer`: approval workflows, state transitions, promotions
- `operator`: intake generation, read access, proposal submission

## Commercial baseline
All tenant-scoped actions must require a tenant identifier and only act within that tenant boundary.
