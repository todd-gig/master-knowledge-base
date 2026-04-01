---
title: System Architecture
created: 2026-03-25
tags: [architecture, python, react, sqlite, google]
status: draft
---

# System Architecture

## Architecture Summary
Use a pragmatic monorepo with:
- **React** frontend
- **Python FastAPI** backend
- **Python worker** for background jobs
- **SQLite** as the source-of-truth operational database
- **Google APIs** for productivity integrations
- **Optional vector index** later
- **Agent orchestration service** inside Python API + worker

## High-Level Components
1. Web App
2. API Server
3. Job Worker
4. SQLite DB
5. Google Integration Layer
6. Agent Runtime
7. Recommendation Engine
8. Artifact Generator
9. Evaluation/Logging Layer

## Recommended Stack

### Frontend
- React
- TypeScript
- Vite
- TanStack Query
- Zustand or Redux Toolkit
- Tailwind CSS
- shadcn/ui

### Backend
- Python 3.12
- FastAPI
- SQLModel or SQLAlchemy
- Pydantic
- Alembic
- httpx
- google-api-python-client
- google-auth
- celery or arq or dramatiq
- jinja2 for templated artifacts

### Storage
- SQLite for MVP
- optional Postgres later
- file storage for generated artifacts
- optional GDrive mirror export

## Logical Diagram
```text
React UI
  -> FastAPI
      -> SQLite
      -> Recommendation Engine
      -> Agent Runtime
      -> Google Service Adapters
      -> Job Queue
            -> Worker
                -> Artifact Builders
                -> Sync Jobs
                -> Agent Tasks
```

## Frontend Modules
- Dashboard
- Catalog Explorer
- Client Need Mapper
- Recommendation Workspace
- Bundle Builder
- Workflow Console
- Agent Console
- Integrations Settings
- Run History / Audit

## Backend Services

### API Service
Responsibilities:
- auth/session
- CRUD for core entities
- workflow initiation
- recommendation queries
- agent deployment requests
- Google integration endpoints

### Worker Service
Responsibilities:
- run queued tasks
- create deliverables
- sync data to Google
- execute agent jobs
- process training/adaptation jobs

### Recommendation Engine
Responsibilities:
- rules-based scoring
- dependency validation
- bundle expansion
- upsell ranking
- cross-sell ranking

### Agent Runtime
Responsibilities:
- create agent instances from templates
- attach prompt profile + tools + context packs
- manage state and runs
- log inputs/outputs
- enforce approval policies

## Agent Deployment Model

### Agent Template
A reusable blueprint with:
- name
- purpose
- prompt system
- allowed tools
- required context
- output schema
- approval mode

### Agent Deployment
A runnable instance with:
- tenant/client scope
- workflow scope
- assigned data pack
- state
- execution logs

## Google Services Integration
Use adapter classes:
- `GoogleSheetsAdapter`
- `GoogleDriveAdapter`
- `GoogleDocsAdapter`
- `GoogleGmailAdapter`
- `GoogleCalendarAdapter`

## Security Controls
- OAuth token encryption at rest
- least-privilege scopes
- signed session cookies or JWT
- audit log for all write actions
- approval gate for external actions

## Deployment Plan
- local docker compose for dev
- single VM or container platform for MVP
- mounted persistent volume for SQLite + artifacts
- environment-variable managed Google credentials
