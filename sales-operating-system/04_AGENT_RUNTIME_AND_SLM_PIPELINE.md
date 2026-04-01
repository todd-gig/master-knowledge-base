---
title: Agent Runtime and Small Language Model Pipeline
created: 2026-03-25
tags: [agents, slm, orchestration, training]
status: draft
---

# Agent Runtime and Small Language Model Pipeline

## Design Goal
Build a framework that can deploy independent task agents automatically, while keeping the implementation grounded.

## Agent Strategy

### Layer 1: Prompt-Specialized Agents
These are the default.
Examples:
- Proposal Agent
- Sales Deck Agent
- Bundle Recommendation Agent
- Client Need Analyzer
- Follow-Up Draft Agent
- Google Sheet Sync Agent

These use:
- a strong base model API
- structured prompts
- narrow tool access
- deterministic schemas

### Layer 2: Retrieval-Specialized Agents
These add:
- context packs
- local knowledge bundles
- source-specific retrieval
- client-specific memory

### Layer 3: Small Model Adaptation Pipeline
Only after repeated stable workloads.

Use cases:
- bundle classification
- need-state detection
- recommendation reranking
- templated copy drafting
- artifact labeling

## Independent Task Agent Contract
Each agent must define:
- mission
- inputs
- tools
- constraints
- output schema
- retry policy
- escalation policy
- approval policy

## Suggested Agent Templates

### proposal_agent
**Mission:** turn an opportunity + selected products into a proposal draft

### deck_agent
**Mission:** create slide outline + slide copy from a bundle and client need state

### discovery_agent
**Mission:** classify client symptoms into need states

### recommendation_agent
**Mission:** generate ranked upsell/cross-sell outputs

### followup_agent
**Mission:** produce next-step email, summary, and CRM notes

### sync_agent
**Mission:** write approved outputs to Google Sheets/Docs/Drive

## Agent State Machine
```text
draft -> ready -> running -> awaiting_approval -> completed
                           -> failed
                           -> canceled
```

## Auto-Deployment Rules
Agents may be deployed automatically when:
- a workflow template calls for one
- an opportunity enters a defined stage
- a user requests artifact generation
- a Google Sheet sync job completes
- a client need classification is saved

## Context Pack Model
A context pack may include:
- product subset
- bundle subset
- client notes
- opportunity details
- style guide
- approved templates
- past recommendations

## Small Model Pipeline

### Practical Path
1. Capture successful runs
2. Normalize to training examples
3. Evaluate for consistency
4. Distill into task-specific datasets
5. Fine-tune or train lightweight classifiers or generation heads
6. Gate deployment behind evaluation thresholds

### Recommended SLM Categories
- classification model for need states
- reranker for recommendation ordering
- extraction model for structured meeting notes
- drafting model for repetitive asset copy

### Data Capture Needed
- input prompt/context
- selected tools
- human corrections
- final approved output
- latency/cost
- quality score

## Do Not Do Initially
- auto-train generative models on every run
- deploy unreviewed fine-tunes automatically
- let agents create external-facing artifacts without approval in early versions

## Safe Default
Auto-deploy **agent instances**, not auto-train **models**, unless evaluation thresholds are met.

## Evaluation Framework
For every agent or SLM:
- schema pass rate
- acceptance rate
- correction distance
- hallucination incidence
- time saved
- business impact score
