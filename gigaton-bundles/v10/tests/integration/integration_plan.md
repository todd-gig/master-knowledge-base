# Integration test plan

## Target flows
1. GET `/api/health`
2. GET `/api/ready`
3. POST `/api/intake/generate-namespace` with tenant header
4. POST `/api/namespaces/promote` with tenant header
5. POST `/api/memory/transition` with tenant header
6. POST `/api/billing/events` with tenant header
7. GET `/api/namespaces` after promotion
8. GET `/api/approvals/queue`
9. GET `/metrics` after mutation traffic

## Expected assertions
- valid requests return 200
- invalid requests return 400
- tenant header is enforced
- correlation IDs are present
- promotion creates durable tenant-scoped namespace row
- billing events are recorded
- metrics counters increment
