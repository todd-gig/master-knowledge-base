# V15 Test Plan

## Required checks
- Poynt token scaffolding emits correct token endpoint, grant type, and headers
- Stripe webhook harness forwards and triggers local events
- SQL migrations can be inserted into the main app migration chain without collisions
- recent payments API returns latest rows ordered by created_at desc
- payment events API returns latest rows ordered by created_at desc
- UI tables refresh after create actions and during live refresh polling
