# Execution Guide v12

## Architecture rule
Everything above the adapter layer must consume normalized payment objects only.

## Default routing policy
- `stripe` for online hosted checkout and online card flows
- `godaddy_poynt` for secondary adapter coverage where that environment is required
- `auto` resolves to Stripe by default unless a tenant override is present

## Implementation sequence
1. Configure provider secrets in `.env.example`
2. Wire `PaymentService` into the main backend
3. Persist normalized payment sessions and events
4. Expose tenant-aware payment endpoints
5. Verify Stripe webhooks
6. Implement Poynt webhook verification when credentials are finalized
7. Route successful normalized payment events into billing events
8. Expose payment status in the dashboard
