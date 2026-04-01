---
title: Decision Routing Framework
version: 1.0.0
status: active
tags: [routing, hybrid, architecture]
---

# Routing Classes
## Python-First
Use when:
- inputs are structured,
- rules are explicit,
- output is deterministic,
- decision volume is high,
- latency sensitivity is high,
- auditability is required.

## Claude-First
Use when:
- inputs are ambiguous,
- interpretation is required,
- context matters heavily,
- rules are incomplete,
- edge cases are frequent,
- exploration value is high.

## Hybrid
Use when:
- Claude can convert unstructured input into structured variables,
- Python can score or execute downstream logic,
- exceptions can be isolated,
- deployment speed matters,
- long-term codification is expected.

# Preferred Hybrid Patterns
1. Python default -> Claude fallback
2. Claude parse -> Python decide
3. Claude parse -> Python score -> Claude review exceptions
4. Claude decide -> Python execute
5. Claude supervise -> Python workers

# Decision Variables
- input structure
- logic clarity
- rule stability
- decision volume
- latency sensitivity
- auditability requirement
- error cost
- compliance exposure
- exception frequency
- codification readiness
