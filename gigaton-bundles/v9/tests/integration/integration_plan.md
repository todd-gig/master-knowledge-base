# Integration test plan

## Target flows
1. GET `/api/health`
2. GET `/api/ready`
3. POST `/api/intake/generate-namespace` with valid payload
4. POST `/api/namespaces/promote` with valid payload
5. POST `/api/memory/transition` with valid payload
6. GET `/api/namespaces` after promotion
7. GET `/metrics` after mutation traffic

## Expected assertions
- valid requests return 200
- invalid requests return 400
- correlation IDs are present
- promotion creates durable namespace row
- transition writes durable transition row
- audit logs are created
- metrics counters increment
