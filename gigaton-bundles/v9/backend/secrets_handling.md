# Secrets Handling

## Baseline rule
Do not commit real secrets to source control.

## Recommended pattern
- local dev: `.env` from `.env.example`
- production: orchestrator secrets, vault, or parameter store
- CI: repository or org secret injection only
