---
title: Prompt Release Governance
version: 3.2
status: active
category: governance
tags: [prompts, releases, approvals, diffing]
---

# Objective
Control prompt changes like code changes.

# Required Controls
- stable prompt id,
- semantic prompt version,
- machine-readable diff summary,
- approval records,
- linked test results,
- linked schema and code versions.

# Release Gate
A prompt release should not move to active until:
1. diff is recorded,
2. tests pass,
3. approvals meet policy,
4. registry is updated,
5. rollback target is defined.

# Canonical Principle
Prompt changes are production changes.
