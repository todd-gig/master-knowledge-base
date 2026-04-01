# Secrets Handling

## Baseline rule
Do not commit real secrets to source control.

## Expected secret classes
- JWT secret
- database credentials or DB path access tokens
- observability API keys if external sinks are used

## Recommended pattern
- local dev: `.env` from `.env.example`
- production: external secrets manager or orchestrator secret mounts
- CI: repository or org secrets, injected only into runtime
