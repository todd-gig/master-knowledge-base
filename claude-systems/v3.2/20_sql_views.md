---
title: Dashboard SQL Views
version: 3.2
status: active
category: analytics
tags: [sql, dashboards, views, bi]
---

# Objective
Expose dashboard-ready SQL views for BI, ops review, and codification prioritization.

# Core Views
- `vw_exception_summary`
- `vw_prompt_performance`
- `vw_codification_backlog`
- `vw_cost_quality_comparison`

# BI Use Cases
- prompt version health,
- exception trend tracking,
- routing mix over time,
- codification backlog ranking,
- Claude vs Python cost/quality tradeoff review.

# Rule
Views should prefer stable column names and be safe for downstream dashboards.
