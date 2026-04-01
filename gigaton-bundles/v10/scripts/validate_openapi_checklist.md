# OpenAPI validation checklist

Use this checklist before release:
- every implemented route exists in `openapi/openapi.yaml`
- request payloads match declared schemas
- tenant-scoped routes declare tenant header expectations
- billing event contract is documented
- breaking changes trigger spec version updates
