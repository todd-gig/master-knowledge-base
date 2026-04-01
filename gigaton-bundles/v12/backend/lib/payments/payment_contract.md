# Payment Contract

Only the unified orchestration layer may be called by the rest of the app.

## Required methods
- createSession(input)
- createIntent(input)
- handleWebhook(provider, body, headers)

## Output rule
All returned objects must be normalized before leaving the payment layer.
