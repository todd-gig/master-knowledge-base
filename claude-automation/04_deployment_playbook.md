---
title: Deployment Playbook
version: 1.0.0
status: active
tags: [deployment, fastapi, postgres, docker]
---

# Recommended Deployment Path
The highest-ROI deployment target from this thread is:

> **FastAPI + Postgres + Docker + CI + dashboard-ready SQL views**

# Minimal Production Stack
- API: FastAPI
- DB: Postgres
- Runtime: Python
- Packaging: Docker
- CI: GitHub Actions
- Analytics: SQL views + BI tool
- Governance: prompt registry + approvals

# Deployment Sequence
1. Put this package into a repo.
2. Install dependencies.
3. Apply migrations.
4. Run tests.
5. Launch FastAPI app.
6. Connect Postgres.
7. Publish SQL views.
8. Point dashboard tool to Postgres.
9. Enforce release approvals before prompt activation.

# Strategic Note
You do not deploy Markdown alone.
You deploy:
- runtime code,
- migrations,
- database,
- API layer,
- registry,
- analytics views.
Markdown remains the governance and instruction layer.
