---
title: Queue Execution Spec
tags: [queues, workers, execution]
status: spec
---

# Queue Execution Spec

## Queue Roles
- ingest_queue
- workflow_queue
- agent_queue
- artifact_queue
- sync_queue
- retry_queue
- dead_letter_queue

## Execution Pattern
1. event received
2. event normalized
3. job placed on queue
4. worker consumes job
5. worker logs result
6. completion event emitted

## Retry Policy
- max retries: 3
- exponential backoff
- non-retryable errors go to dead letter queue
- repeated failures trigger alert

## Worker Contract
Each job must contain:
- job_id
- event_id
- job_type
- payload
- created_at
- retry_count
- correlation_id
