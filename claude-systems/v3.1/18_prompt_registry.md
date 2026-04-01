---
title: Prompt and Version Registry
version: 3.1
status: active
category: registry
tags: [prompts, versions, governance]
---

# Objective
Maintain versioned control over prompts, schemas, and runtime logic.

# Rules
- every production prompt must have a stable id,
- every audit record must reference prompt id + version,
- schema changes must be versioned,
- code releases must be linked to prompt releases,
- deprecated prompts must remain queryable for audit history.
