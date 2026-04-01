# Blue-Green Deployment

## Pattern
- deploy new version as green
- run healthchecks and smoke tests against green
- shift traffic from blue to green only after passing checks
- keep blue available for immediate rollback

## Minimum checks before cutover
- `/api/health`
- `/api/ready`
- namespace promotion smoke test
- memory transition smoke test
