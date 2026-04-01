---
title: API and Event Contracts
created: 2026-03-25
tags: [api, contracts, events]
status: draft
---

# API and Event Contracts

## REST API Contracts

### POST /catalog/import-sheet
Imports a Google Sheet into staging and normalizes it.

#### Request
```json
{
  "google_sheet_id": "string",
  "tabs": ["Master_Catalog", "Upsell_Matrix", "Cross_Sell_Matrix"]
}
```

#### Response
```json
{
  "import_job_id": "string",
  "status": "queued"
}
```

### GET /opportunities/{opportunity_id}/recommendations
Returns ranked upsell/cross-sell and bundle suggestions.

#### Response
```json
{
  "opportunity_id": "opp_123",
  "need_states": [
    {"id": "need_1", "name": "Low conversion", "confidence": 0.92}
  ],
  "recommendations": [
    {
      "type": "upsell",
      "product_id": "prod_landing_page",
      "product_name": "Landing Page",
      "confidence_score": 0.88,
      "rationale": "Lead magnet present but conversion infrastructure missing"
    }
  ]
}
```

### POST /agents/deploy
Deploys an agent instance.

#### Request
```json
{
  "agent_template_id": "proposal_agent",
  "scope_type": "opportunity",
  "scope_id": "opp_123",
  "config": {
    "approval_mode": "human_required"
  }
}
```

### POST /workflow/run
Runs a defined workflow.

#### Request
```json
{
  "workflow_type": "build_proposal_package",
  "opportunity_id": "opp_123",
  "selected_product_ids": ["prod_case_study", "prod_sales_presentation"]
}
```

## Event Contracts

### opportunity.created
```json
{
  "event_type": "opportunity.created",
  "opportunity_id": "opp_123",
  "client_id": "client_1",
  "timestamp": "2026-03-25T12:00:00Z"
}
```

### need_state.detected
```json
{
  "event_type": "need_state.detected",
  "opportunity_id": "opp_123",
  "need_state_id": "need_low_conversion",
  "confidence": 0.91
}
```

### recommendations.generated
```json
{
  "event_type": "recommendations.generated",
  "opportunity_id": "opp_123",
  "recommendation_count": 6
}
```

### agent.deployed
```json
{
  "event_type": "agent.deployed",
  "deployment_id": "dep_123",
  "agent_template_id": "proposal_agent",
  "scope_type": "opportunity",
  "scope_id": "opp_123"
}
```

### google.sync.completed
```json
{
  "event_type": "google.sync.completed",
  "job_id": "sync_123",
  "target_google_id": "sheet_abc",
  "status": "completed"
}
```

## Output Schema Example - Proposal Agent
```json
{
  "title": "Proposal title",
  "executive_summary": "string",
  "recommended_bundle": ["string"],
  "statement_of_work_outline": ["string"],
  "pricing_notes": ["string"],
  "next_steps": ["string"]
}
```
