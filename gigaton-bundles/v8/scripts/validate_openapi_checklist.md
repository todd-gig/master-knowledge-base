# OpenAPI validation checklist

Use this checklist before release:
- every implemented route exists in `openapi/openapi.yaml`
- request payloads match declared schemas
- health and readiness endpoints are documented
- mutation routes specify request bodies
- breaking changes trigger spec version updates
