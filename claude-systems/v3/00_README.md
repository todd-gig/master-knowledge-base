---
title: Claude System Package v3
version: 3.0
status: active
created: 2026-03-26
owner: CxGuy
package_type: human-plus-machine
purpose: Obsidian-ready and runtime-ready package for routing work between Claude, Python, and hybrid execution paths.
tags:
  - claude
  - obsidian
  - system-prompt
  - machine-readable
  - routing
  - roi
---

# Overview
This package is a full **human + machine** operating system for decision routing.

It is designed to do two things at once:
1. give humans a clean, modular, Obsidian-ready governance layer,
2. give software a machine-readable runtime layer that can validate, route, log, and migrate decisions from Claude to Python.

# Core Principle
> Claude discovers logic. Python scales it profitably.

# Package Goals
- maximize long-term ROI,
- minimize recurring reasoning cost,
- preserve decision quality,
- create a fast path from ambiguity to codified execution,
- support auditability and controlled escalation.

# Folder Structure
```md
/claude-system-v3/
  ├── 00_README.md
  ├── CLAUDE.md
  ├── 01_routing_rubric.md
  ├── 02_decision_variables.md
  ├── 03_scoring_weights.md
  ├── 04_codification_thresholds.md
  ├── 05_exception_policy.md
  ├── 06_audit_log_schema.md
  ├── 07_decision_state_machine.md
  ├── 08_hybrid_execution_patterns.md
  ├── 09_python_interface_spec.md
  ├── 10_output_contract.md
  ├── 11_confidence_policy.md
  ├── 12_test_case_templates.md
  ├── 13_migration_loop.md
  ├── 14_runtime_integration.md
  ├── /machine/
  │   ├── routing_config.json
  │   ├── decision_schema.json
  │   ├── audit_log_schema.json
  │   ├── state_machine.json
  │   ├── test_cases.json
  │   ├── exception_registry.json
  │   ├── output_contract.schema.json
  │   ├── sample_payloads.json
  │   └── scoring_weights.yaml
  └── /python/
      ├── router.py
      └── README.md
```

# How To Use
## Human layer
- Put these Markdown files into Obsidian or a repo docs folder.
- Use `CLAUDE.md` as the root project instruction.
- Treat linked companion files as the governing logic layer.

## Machine layer
- Use `machine/decision_schema.json` to validate Claude outputs.
- Use `machine/routing_config.json` and `machine/scoring_weights.yaml` to drive routing.
- Use `python/router.py` as the starter runtime.

# Deployment Sequence
1. Deploy `CLAUDE.md` into the Claude project or repo root.
2. Version the `machine/` directory.
3. Log every decision against `machine/audit_log_schema.json`.
4. Review exception frequency and confidence drift.
5. Codify stable paths into Python aggressively.

# Business Logic
The target end-state is not maximum LLM usage.
The target end-state is **maximum profitable automation with controlled reasoning spend**.
