---
title: Release Governance
version: 1.0.0
status: active
tags: [releases, approvals, prompts, diffs]
---

# Objective
Treat prompt changes like production changes.

# Release Gate
A prompt release does not become active until:
1. diff is generated,
2. tests pass,
3. required approvals are recorded,
4. registry is updated,
5. rollback target is defined.

# Required Artifacts
- prompt id
- prompt version
- diff summary
- release approval records
- linked schema version
- linked code version
- release notes

# Canonical Principle
> Prompt changes are production changes.
