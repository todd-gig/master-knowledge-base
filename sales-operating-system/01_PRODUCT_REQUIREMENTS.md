---
title: Product Requirements Document
created: 2026-03-25
tags: [prd, sales, upsell, cross-sell, agents]
status: draft
---

# Product Requirements Document

## Product Name
Sales Operating System

## Product Summary
A system that converts a spreadsheet-driven sales catalog into an operational platform for:
- discovery
- qualification
- upsell
- cross-sell
- bundle recommendation
- content generation
- workflow automation
- agent deployment

## Primary Users
1. Sales strategist
2. Account manager
3. RevOps operator
4. Founder / operator
5. Marketing coordinator
6. AI workflow supervisor

## Core Jobs To Be Done
1. Maintain a master product-service-collateral catalog
2. Map client needs to products, bundles, and automation paths
3. Generate recommendations for upsell and cross-sell
4. Create deliverables and follow-up assets automatically
5. Spawn task-specific agents when a workflow requires them
6. Push structured outputs into Google services

## Functional Requirements

### FR-1 Master Catalog
The platform must store and manage:
- assets
- services
- bundles
- channels
- deliverables
- automation components
- dependencies
- scoring attributes
- pricing metadata
- owner metadata
- example links
- source lineage

### FR-2 Client Need Mapping
The platform must map client symptoms to:
- recommended products
- sequencing logic
- dependencies
- cross-sell opportunities
- upsell triggers
- bundle paths

### FR-3 Recommendation Engine
The platform must generate:
- ranked upsell suggestions
- ranked cross-sell suggestions
- bundle recommendations
- implementation next steps
- confidence scores
- reason codes

### FR-4 Workflow Execution
The platform must support execution flows such as:
- build proposal
- build sales deck
- build lead magnet
- launch nurture campaign
- generate follow-up summary
- create implementation checklist
- create project scope
- create content calendar

### FR-5 Agent Runtime
The platform must allow a user or workflow to deploy task agents such as:
- proposal agent
- deck agent
- outreach agent
- qualification agent
- CRM sync agent
- research agent
- bundle recommendation agent

### FR-6 Google Services Integration
The platform should support:
- Google OAuth
- Google Sheets read/write
- Google Drive import/export
- Google Docs content output
- Gmail draft generation
- Calendar event creation
- optional Forms ingestion

### FR-7 Small Model Pipeline
The platform should support progressive specialization:
- prompt profiles
- retrieval packs
- reusable tool policies
- task evaluation traces
- optional fine-tune or distillation pipeline for narrow tasks

## Non-Functional Requirements
- Local-first MVP using SQLite
- Deployable as containerized services
- Minimal ops burden
- Clear auditability
- Deterministic fallbacks for critical workflows
- Role-based access control
- Secure credential handling
- Job queue support for asynchronous tasks

## MVP Scope
- SQLite database
- React dashboard
- Python API
- Python worker
- Google Sheets import/export
- Rules-based recommendation engine
- Agent orchestration layer
- Prompt-based specialized agents
- Read/write activity log

## Post-MVP Scope
- vector retrieval layer
- evaluation system
- lightweight fine-tune pipeline
- auto-deployment templates for specialized agents
- billing and usage metering
- multitenant organization support

## Out of Scope for MVP
- end-to-end autonomous model training without human approval
- complex distributed training infrastructure
- custom GPU training orchestration
- full enterprise CRM replacement

## Success Metrics
- time to produce proposal reduced by 70%
- time to produce upsell path reduced by 80%
- percent of client records with recommended next action > 90%
- number of reusable task agents deployed per week
- recommendation acceptance rate
- asset reuse rate across clients

## Key Entities
- Product
- Service
- Asset
- Bundle
- NeedState
- Client
- Opportunity
- Recommendation
- WorkflowRun
- AgentTemplate
- AgentDeployment
- PromptProfile
- GoogleSyncJob

## Risks
- over-automation without review
- poor data hygiene from spreadsheet imports
- agent sprawl
- mixing product taxonomy with execution tasks
- assuming model training is needed when rules + retrieval would suffice

## Product Principle
Default to **operational leverage**, not novelty.
