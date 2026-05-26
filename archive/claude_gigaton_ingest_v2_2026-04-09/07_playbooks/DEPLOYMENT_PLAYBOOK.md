# Deployment Playbook

## Environments
- local
- staging
- production

## Release Gates
- tests pass
- env vars documented
- migration reviewed
- rollback path defined
- approval granted

## Production-Changing Actions Require Approval
- auth changes
- database migrations
- billing/payment changes
- production deploys
- destructive operations

## Release Sequence
1. Local validation
2. Staging deploy
3. Smoke tests
4. Approval
5. Production deploy
6. Post-deploy monitoring
7. Rollback if needed
