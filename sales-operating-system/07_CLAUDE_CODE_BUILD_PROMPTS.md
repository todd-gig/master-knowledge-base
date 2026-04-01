---
title: Claude Code Build Prompts
created: 2026-03-25
tags: [claude-code, prompts, implementation]
status: draft
---

# Claude Code Build Prompts

## Prompt 1 - Repo Scaffold
Build a monorepo named `sales-operating-system-agentic` with:
- React + TypeScript + Vite frontend
- FastAPI backend
- Python worker service
- shared package structure
- SQLite database and Alembic migrations
- Docker dev environment

Follow the architecture in `02_SYSTEM_ARCHITECTURE.md` and the schema in `03_DATA_MODEL_SQLITE_GOOGLE.md`.

## Prompt 2 - Core Schema + CRUD
Implement the SQLite schema defined in `03_DATA_MODEL_SQLITE_GOOGLE.md`.
Generate:
- SQLAlchemy or SQLModel models
- Pydantic request/response schemas
- CRUD routes for catalog, bundles, need states, opportunities, and recommendations
- migration scripts
- seed scripts for initial data

## Prompt 3 - Recommendation Engine
Implement a deterministic recommendation engine that:
- accepts an opportunity plus detected need states
- returns ranked upsell recommendations
- returns ranked cross-sell recommendations
- expands valid bundles
- explains each recommendation with reason codes
- persists results to the `recommendations` table

## Prompt 4 - React UI
Build React views for:
- dashboard
- master catalog
- bundles
- opportunities
- recommendation workspace
- agents console
- Google integrations settings

Use a clean admin-app pattern. Include filters, search, modals, and optimistic refresh where appropriate.

## Prompt 5 - Google Sheets Sync
Implement Google OAuth and a Google Sheets adapter that can:
- import tabs from a source sheet
- normalize rows into the SQLite schema
- export the current DB state into a generated Google Sheet with tabs:
  - Master_Catalog
  - Upsell_Matrix
  - Cross_Sell_Matrix
  - Bundles
  - Scoring_Model
  - Client_Needs_Mapping
  - Source_Index

## Prompt 6 - Agent Runtime
Implement an agent runtime with:
- agent templates
- deployable agent instances
- execution logging
- approval modes
- input/output schemas
- workflow attachment

Start with these templates:
- proposal_agent
- deck_agent
- recommendation_agent
- followup_agent
- sync_agent

## Prompt 7 - Artifact Builders
Implement Python services that generate:
- proposal drafts
- sales deck outlines
- follow-up email drafts
- implementation checklists
- lead magnet specs

These services should consume catalog, recommendation, and opportunity data.

## Prompt 8 - SLM Readiness
Implement logging and dataset capture required for later lightweight model adaptation:
- prompt/context capture
- approved final outputs
- correction delta
- quality score fields
- export scripts for training data preparation

Do not implement automatic model training yet. Build the data capture layer first.

## Prompt 9 - Deployment
Add Dockerfiles and a docker-compose setup for:
- web
- api
- worker

Make local development and single-host deployment straightforward.

## Prompt 10 - Hard Rule
Optimize for reliability and business utility over experimental autonomy. Every external write action should be auditable and optionally approval-gated.
