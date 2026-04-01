---
title: Implementation Plan - Python and React
created: 2026-03-25
tags: [implementation, fastapi, react, roadmap]
status: draft
---

# Implementation Plan - Python and React

## Phase 0 - Repo Bootstrap
- create monorepo
- configure Python app, worker, React app
- add linting, formatting, env management
- initialize SQLite + migrations

## Phase 1 - Core Data Layer
- implement schema tables
- seed product catalog
- seed bundles
- seed need states
- seed upsell/cross-sell rules
- create CRUD endpoints

## Phase 2 - Frontend Workspaces
- Dashboard
- Master Catalog table
- Need-State mapping view
- Recommendation workspace
- Bundle editor
- Agent deployment console

## Phase 3 - Recommendation Engine
- deterministic scoring engine
- bundle expansion logic
- dependency checker
- need-state recommendation resolver
- suggestion explanations

## Phase 4 - Google Integrations
- OAuth setup
- Sheets import
- Sheets export
- Drive artifact export
- Docs generation
- Gmail drafts

## Phase 5 - Agent Runtime
- agent templates CRUD
- deployment engine
- workflow runs
- tool policy enforcement
- execution logs

## Phase 6 - Artifact Builders
- proposal builder
- deck outline builder
- lead magnet spec builder
- follow-up email builder
- implementation plan builder

## Phase 7 - Adaptation Pipeline
- run history capture
- correction capture
- evaluation dashboard
- optional lightweight classifier training

## Backend Directory Proposal
```text
apps/api/
  app/
    api/
    core/
    db/
    models/
    schemas/
    services/
    engines/
    agents/
    google/
    workflows/
    builders/
```

## Frontend Directory Proposal
```text
apps/web/src/
  app/
  components/
  features/
    dashboard/
    catalog/
    bundles/
    recommendations/
    clients/
    agents/
    integrations/
  lib/
  hooks/
  api/
```

## Key Python Services
- `catalog_service.py`
- `recommendation_service.py`
- `bundle_service.py`
- `opportunity_service.py`
- `google_sync_service.py`
- `agent_runtime_service.py`
- `artifact_builder_service.py`

## Key React Views
- `/dashboard`
- `/catalog`
- `/clients`
- `/opportunities/:id`
- `/recommendations`
- `/bundles`
- `/agents`
- `/integrations/google`

## Recommended First API Endpoints
- `GET /catalog`
- `POST /catalog/import-sheet`
- `POST /catalog/export-sheet`
- `GET /opportunities/{id}/recommendations`
- `POST /workflow/run`
- `POST /agents/deploy`
- `GET /agents/deployments`
- `POST /google/docs/proposal`
- `POST /google/gmail/draft-followup`

## Priority MVP Workflow
1. import current spreadsheet
2. normalize catalog
3. create or select client
4. classify client needs
5. generate recommendations
6. create bundle path
7. deploy proposal agent
8. export outputs to Google Docs + Sheets

## Recommended Testing
- schema tests
- scoring tests
- rules engine tests
- Google adapter mocks
- agent output schema tests
- workflow integration tests
