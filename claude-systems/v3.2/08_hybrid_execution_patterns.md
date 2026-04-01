---
title: Hybrid Execution Patterns
version: 3.0
status: active
category: patterns
tags: [hybrid, architecture]
---

# Pattern 1 — Claude Parse -> Python Decide
Use when unstructured input can be converted into variables that feed deterministic business logic.

# Pattern 2 — Claude Decide -> Python Execute
Use when final judgment is contextual but downstream action is mechanical.

# Pattern 3 — Claude Parse -> Python Score -> Claude Review Exceptions
Use when the main path is routinizable but outliers need contextual treatment.

# Pattern 4 — Python Default -> Claude Fallback
Use when stable logic covers most volume and only anomalies require reasoning.

# Pattern 5 — Claude Supervisor -> Python Workers
Use when Claude governs orchestration while Python services perform bounded tasks.

# Preference Order
1. Python Default -> Claude Fallback
2. Claude Parse -> Python Decide
3. Claude Parse -> Python Score -> Claude Review Exceptions
4. Claude Decide -> Python Execute
5. Pure Claude
