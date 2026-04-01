---
title: Agent Message Contracts
tags: [agents, contracts, messaging]
status: spec
---

# Agent Message Contracts

## Required Fields
- message_id
- correlation_id
- sender_agent
- target_agent
- message_type
- payload
- timestamp

## Message Types
- task_request
- task_result
- schema_error
- escalation
- approval_request
- approval_result

## Example
```json
{
  "message_id": "msg_1",
  "correlation_id": "run_123",
  "sender_agent": "pricing_agent",
  "target_agent": "proposal_agent",
  "message_type": "task_result",
  "payload": {
    "recommended_price": 2500,
    "gross_margin": 0.62
  },
  "timestamp": "2026-03-25T12:00:00Z"
}
```
