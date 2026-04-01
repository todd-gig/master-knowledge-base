# Payment Contract

## Required interface
Each provider adapter must implement:
- `createSession(input)`
- `createIntent(input)`
- `handleWebhook(body, headers)`
- `normalizeStatus(providerStatus)`
- `mapBillingEvent(input)`

## Rule
Everything outside this folder must only consume normalized payment objects.
