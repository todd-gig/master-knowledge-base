# Deployment Guide v6

## Stack target
- Claude project for reasoning/instructions
- Backend service for write-back, auth, and governed workflows
- Persistent database for registry, namespaces, calibration data, lifecycle state, and audit logs
- Dashboard as the operator control plane

## Deployment flow
1. Upload core JSON and markdown artifacts into the Claude project.
2. Deploy backend service scaffold.
3. Provision database with `database/schema.sql`.
4. Seed baseline data using `database/seed.json`.
5. Configure environment variables from `.env.example`.
6. Deploy dashboard and point it at the backend API.
7. Enable approval workflows for namespace promotion and calibration promotion.

## High-ROI operating model
- Standardize onboarding with automated intake processing.
- Tighten retrieval quality via feedback + calibration.
- Govern every production mutation with auditability and rollback.
- Give operators a single control plane for client overlays and registry health.
