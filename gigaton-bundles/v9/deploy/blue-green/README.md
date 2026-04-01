# Blue-Green Deployment

## Pattern
- deploy new version as green
- run healthchecks, integration checks, and gate script against green
- shift traffic from blue to green only after passing checks
- keep blue available for immediate rollback
