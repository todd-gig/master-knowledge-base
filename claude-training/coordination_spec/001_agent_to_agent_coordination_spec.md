---
title: Agent-to-Agent Coordination Spec
tags: [agents, orchestration, coordination]
status: spec
---

# Agent-to-Agent Coordination Spec

## Objective
Define how multiple specialized agents collaborate without conflicting responsibilities or duplicating work.

## Agent Roles
- Discovery Agent
- Recommendation Agent
- Pricing Agent
- Proposal Agent
- Sync Agent
- QA / Review Agent

## Coordination Model
- One workflow supervisor
- Multiple specialized workers
- Clear input/output contracts
- Shared event log
- Approval checkpoints

## Handoff Contract
Each agent must emit:
- `run_id`
- `agent_name`
- `input_summary`
- `output_summary`
- `output_schema`
- `confidence`
- `next_recommended_agent`
- `requires_human_review`

## Example Handoff
```json
{
  "run_id": "run_123",
  "agent_name": "discovery_agent",
  "output_summary": "Detected low conversion and weak trust signals",
  "next_recommended_agent": "recommendation_agent",
  "requires_human_review": false
}
```

## Conflict Rules
- No agent may overwrite another agent's approved output.
- Shared state updates must be append-first, then reconcile.
- Proposal and pricing outputs require final approval gates if external-facing.

## Supervisor Responsibilities
- route tasks
- validate schema outputs
- prevent duplicate execution
- escalate failures
- log full sequence history
