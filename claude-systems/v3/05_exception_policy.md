---
title: Exception Policy
version: 3.0
status: active
category: policy
tags: [exceptions, governance]
---

# Exception Classes
- missing_data
- conflicting_data
- ambiguous_intent
- threshold_conflict
- policy_gap
- out_of_distribution_input
- compliance_risk
- irreversible_action_risk

# Default Policy
- standard cases -> normal route
- exception cases -> Claude or Hybrid review path
- high-risk exceptions -> human escalation

# Required Actions
1. assign exception class
2. log triggering variables
3. record decision path
4. capture resolution
5. tag for recurrence analysis
6. evaluate for codification later

# Escalation Rule
Escalate when:
- confidence is below threshold,
- action is irreversible,
- compliance risk is medium or higher,
- external stakeholder impact is material,
- failure cost exceeds tolerance.
