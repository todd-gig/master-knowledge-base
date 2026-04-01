# Tenant Isolation Model

## Baseline rule
Every tenant-scoped API call must carry a tenant identifier and only operate on rows for that tenant.

## Enforcement layers
1. request header extraction
2. middleware validation
3. query filters at the persistence layer
4. audit logs with tenant ID
5. UI actions always scoped to current tenant

## Forbidden behavior
- cross-tenant namespace reads
- cross-tenant write-back actions
- tenantless billing event emission for tenant-scoped flows
