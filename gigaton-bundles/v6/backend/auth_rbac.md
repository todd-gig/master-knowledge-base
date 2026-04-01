# Auth and RBAC

## Roles
- `admin`: full access including promotion and state transitions
- `reviewer`: approval workflows, state transitions, promotions
- `operator`: intake generation, calibration proposals, read access

## Minimum production controls
- JWT or session auth
- role-based middleware on all mutation routes
- audit logging for every write-back action
- approval requirement for production promotion paths
