---
title: Validation and Logging Layer
version: 3.1
status: active
category: runtime
tags: [validation, logging, sqlite, postgres]
---

# Objective
Enforce schema-valid decisions and persist auditable decision records.

# Rules
- never route or execute an invalid payload,
- validate incoming decision payloads against `machine/decision_schema.json`,
- validate outgoing audit records against `machine/audit_log_schema.json`,
- support SQLite by default and Postgres via environment variable,
- store prompt version and code version with every decision.

# Storage Strategy
## SQLite
Use for local development, prototypes, and low-to-medium throughput systems.

## Postgres
Use for concurrent writes, shared production services, and larger audit datasets.

# Strategic Note
Validation and logging are the control plane that makes the Claude-to-Python migration loop governable and profitable.
