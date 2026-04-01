---
title: Database Migrations
version: 3.2
status: active
category: database
tags: [database, migrations, sqlite, postgres]
---

# Objective
Version database changes explicitly so audit infrastructure can evolve without uncontrolled schema drift.

# Rules
- every schema change must ship with a numbered migration,
- migrations must be forward-readable and reversible where practical,
- prompt releases and DB migrations should be traceable to the same release cycle,
- production rollout must apply migrations before new runtime code writes incompatible records.

# Strategy
This package uses an Alembic-style approach:
- ordered migration files,
- migration manifest,
- runtime migration helper,
- explicit SQL for SQLite and Postgres compatibility.

# Required Tables
- `decision_audit`
- `prompt_releases`
- `release_approvals`
- `benchmark_runs`

# ROI Note
Migration discipline is required once the audit store becomes a system of record.
