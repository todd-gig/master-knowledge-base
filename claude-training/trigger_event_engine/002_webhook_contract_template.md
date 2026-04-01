---
title: Webhook Contract Template
tags: [webhooks, api]
status: template
---

# Webhook Contract Template

## Identity
- Webhook Name:
- Source System:
- Destination Endpoint:

## Security
- Auth Method:
- Signature Header:
- Replay Protection:
- IP Allowlist:

## Payload
- Event Type:
- Required Fields:
- Optional Fields:

## Processing Rules
- Validate Signature:
- Parse Payload:
- Normalize Event:
- Enqueue Job:
- Respond Fast:

## Response Contract
- Success Status:
- Failure Status:
- Retry Conditions:

## Idempotency
- Event ID Field:
- Dedup Window:
