# V14 Test Plan

## Required checks
- Stripe raw-body webhook route verifies valid signature and rejects invalid signature
- SQL repository persists payment records and events
- tenant policy repository reads and writes policy documents
- payment service emits telemetry for attempt/success/failure/failover
- provider failover uses tenant policy by use case
- dashboard live refresh only polls when enabled
