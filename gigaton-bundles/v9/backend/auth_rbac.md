# Auth and RBAC

## Roles
- `admin`: full access including promotion and state transitions
- `reviewer`: approval workflows, state transitions, promotions
- `operator`: intake generation, calibration proposals, read access

## Launch baseline
- JWT or session auth
- role-based middleware on all mutation routes
- audit logging for every write-back action
- secrets sourced from environment or external secrets manager, never committed
