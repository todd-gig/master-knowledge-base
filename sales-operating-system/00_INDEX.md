---
title: Sales Operating System - Markdown Spec Pack
created: 2026-03-25
tags:
  - sales-operating-system
  - python
  - react
  - sqlite
  - google-services
  - agent-runtime
  - slm
status: draft
project: Ti Solutions
objective: Convert the spreadsheet-driven sales operating system into an implementation-ready markdown pack for Claude Code.
---

# Sales Operating System - Markdown Spec Pack

## Purpose
This pack translates the spreadsheet artifact into an implementation-ready system design that Claude Code can use to build a deployable product using:
- **Python** backend
- **React** frontend
- **SQLite** core datastore
- **Google services** for auth, Sheets sync, Drive import/export, and optional Gmail/Calendar workflows
- **Agent runtime** for independent task agents
- **Small language model pipeline** for specialized task agents

## Deliverables
1. `01_PRODUCT_REQUIREMENTS.md`
2. `02_SYSTEM_ARCHITECTURE.md`
3. `03_DATA_MODEL_SQLITE_GOOGLE.md`
4. `04_AGENT_RUNTIME_AND_SLM_PIPELINE.md`
5. `05_IMPLEMENTATION_PLAN_PYTHON_REACT.md`
6. `06_API_AND_EVENT_CONTRACTS.md`
7. `07_CLAUDE_CODE_BUILD_PROMPTS.md`

## Build Intent
The target system is not just a spreadsheet replacement. It is a **sales operating system** that:
- ingests catalog, client need states, bundles, and cross-sell logic
- operationalizes that data through workflows
- spins up specialized task agents on demand
- supports optional training or adaptation of lightweight models for narrow tasks
- can publish outputs back to Google Sheets, Docs, Drive, Gmail, and Calendar

## Important Engineering Note
“Automatically develop multiple small language models” should be interpreted pragmatically:
- **Tier 1:** prompt-specialized agents with deterministic tools
- **Tier 2:** retrieval-augmented task agents with narrow context windows
- **Tier 3:** optionally train or distill lightweight models for specific repetitive workflows

Tier 1 and Tier 2 are realistic for an initial release. Tier 3 should be treated as a controlled pipeline, not a first-release dependency.

## Recommended Repo Name
`sales-operating-system-agentic`

## Recommended Monorepo Structure
```text
sales-operating-system-agentic/
  apps/
    web/
    api/
    worker/
  packages/
    ui/
    prompts/
    agent-sdk/
    data-models/
    google-connectors/
  infra/
    docker/
    scripts/
  docs/
```

## Success Condition
Claude Code should be able to use these documents to scaffold and implement a working MVP without needing the spreadsheet as the primary source of truth.
