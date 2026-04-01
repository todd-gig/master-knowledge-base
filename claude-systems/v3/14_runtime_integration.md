---
title: Runtime Integration Guide
version: 3.0
status: active
category: runtime
tags: [runtime, integration, machine-layer]
---

# Objective
Bridge the human governance layer and the machine execution layer.

# Runtime Flow
1. Claude receives a task under `CLAUDE.md`.
2. Claude emits a structured decision payload matching `machine/decision_schema.json`.
3. Runtime validates the payload.
4. Runtime scores the payload using `machine/scoring_weights.yaml`.
5. Runtime routes the task using `machine/routing_config.json`.
6. Python executes deterministic logic or Claude handles reasoning.
7. Runtime logs the outcome against `machine/audit_log_schema.json`.
8. Codification analysis checks whether the path should migrate to Python.

# Integration Rules
- never execute unvalidated payloads,
- version prompts and schemas together,
- log every exception,
- separate parsing from execution,
- keep Python interfaces schema-bound.

# Recommended System Topology
- Claude: interpretation and exception handling
- Python: scoring, rules, execution, logging
- Data store: audit logs and codification candidates
- Review layer: human escalation for low confidence or high risk
