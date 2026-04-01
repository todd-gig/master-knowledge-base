---
title: Codification Candidate Scoring
version: 3.1
status: active
category: scoring
tags: [codification, scoring, roi]
---

# Objective
Quantify which decision paths should migrate from Claude to Python first.

# Default Scoring Interpretation
- 0.80-1.00 -> codify now
- 0.60-0.79 -> prepare codification design
- 0.40-0.59 -> continue logging and observation
- below 0.40 -> keep in Claude or Hybrid

# ROI Formula
`priority = expected_monthly_savings * confidence_in_stability * implementation_feasibility`
