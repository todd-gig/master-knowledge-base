# Gigaton Claude Project Bundle v6

This is the productionization-oriented v6 package.

## What changed from v5
- Added API routes and persistent storage schema
- Added auth/RBAC model
- Added write-back flows from dashboard actions
- Added governed promotion pipeline for namespaces and calibrated weights
- Added migration + environment templates
- Added backend service scaffold and upgraded dashboard integration contract

## Production objective
Move from local execution artifacts to a governed application stack that can:
1. ingest intake forms,
2. generate client namespaces,
3. calibrate retrieval,
4. manage memory lifecycle transitions,
5. write approved changes back into the registry,
6. expose operator workflows through authenticated APIs and dashboard actions.

## Fast path
1. Review `system_prompt_contract.v6.md`
2. Review `deployment_guide.v6.md`
3. Review `backend/README.md`
4. Review `dashboard_app/README.md`
5. Use `database/schema.sql` + `database/seed.json` as the persistence baseline
