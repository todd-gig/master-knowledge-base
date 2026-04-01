---
title: Confidence Policy
version: 3.0
status: active
category: policy
tags: [confidence, risk]
---

# Confidence Bands
- 0.90-1.00 -> high confidence
- 0.75-0.89 -> moderate confidence
- 0.60-0.74 -> low confidence
- below 0.60 -> insufficient confidence

# Rules
- high confidence + low risk -> proceed
- moderate confidence + medium risk -> proceed with logging
- low confidence + medium/high risk -> exception review
- insufficient confidence -> human escalation or defer action

# Mandatory Downgrades
Reduce confidence when:
- inputs conflict,
- source quality is weak,
- decision is novel,
- exception class exists,
- reversibility is low,
- compliance exposure is medium or higher.
