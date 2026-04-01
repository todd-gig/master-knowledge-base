# Webhook Replay Tooling

Use `/api/payments/webhook-replay` with:
- `event_id`
- `operator_note`

## Purpose
Recover from transient downstream failures by replaying a stored normalized event through the orchestration path.
