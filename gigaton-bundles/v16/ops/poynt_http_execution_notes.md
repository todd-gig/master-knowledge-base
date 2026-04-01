# Poynt HTTP Execution Notes

## Execution structure
1. Generate JWT-bearer assertion
2. POST to `/token`
3. Use returned bearer token with `Api-Version: 1.2`
4. POST to `/businesses/{businessId}/orders` or `/businesses/{businessId}/transactions`
5. Normalize response inside adapter only

## Operational rule
Do not expose raw provider payloads above the adapter layer.
