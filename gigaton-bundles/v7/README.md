# Gigaton Claude Project Bundle v7

This is the hardening-oriented v7 package.

## What v7 adds
- Real SQL migrations
- Test coverage scaffolds for backend and generator logic
- Transactional write-back patterns
- API request validation
- Production deployment manifests
- CI workflow scaffolds
- Rollback and healthcheck patterns

## Objective
Move the v6 productionization package closer to an auditable, deployable, lower-risk operating system.

## Fast path
1. Review `deployment_guide.v7.md`
2. Initialize DB with `scripts/init_db_from_migrations.py`
3. Run backend tests in `tests/backend/`
4. Review deployment manifests in `deploy/`
5. Use validation middleware and transaction helpers as the default mutation path
