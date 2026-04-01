---
title: Codification Thresholds
version: 3.0
status: active
category: codification
tags: [codification, migration]
---

# Codify When
- the decision repeats frequently,
- inputs become structurally consistent,
- output classes stabilize,
- exception patterns become enumerable,
- confidence stays high,
- reviewers agree with outcomes,
- savings justify implementation effort.

# Default Thresholds
- repeated >= 100 instances
- agreement >= 95% on reviewed cases
- exception rate <= 10%
- schema completeness >= 90%
- business rules expressible explicitly
- payback justified within target window

# Payback Logic
```text
(claude_recurring_cost - python_recurring_cost) * expected_volume > codification_cost + maintenance_cost
```

# Do Not Codify When
- semantics drift constantly,
- judgment remains irreducibly contextual,
- edge cases dominate,
- the process is still changing materially.
