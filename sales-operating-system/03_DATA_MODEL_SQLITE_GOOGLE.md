---
title: Data Model and SQLite + Google Strategy
created: 2026-03-25
tags: [data-model, sqlite, google-sheets, schema]
status: draft
---

# Data Model and SQLite + Google Strategy

## Data Source Strategy
The spreadsheet is an import/export surface. The app database is the operating source of truth.

## Core Tables

### product_catalog
```sql
CREATE TABLE product_catalog (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  category TEXT,
  subcategory TEXT,
  description TEXT,
  primary_goal TEXT,
  core_value TEXT,
  interaction_value INTEGER DEFAULT 1,
  marketing_influence INTEGER DEFAULT 1,
  score_multiplier REAL DEFAULT 0,
  funnel_stage TEXT,
  primary_channel TEXT,
  automation_potential TEXT,
  source_reference TEXT,
  is_active INTEGER DEFAULT 1,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### bundles
```sql
CREATE TABLE bundles (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  description TEXT,
  value_proposition TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### bundle_items
```sql
CREATE TABLE bundle_items (
  id TEXT PRIMARY KEY,
  bundle_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  sequence_order INTEGER DEFAULT 0,
  required INTEGER DEFAULT 1,
  FOREIGN KEY(bundle_id) REFERENCES bundles(id),
  FOREIGN KEY(product_id) REFERENCES product_catalog(id)
);
```

### need_states
```sql
CREATE TABLE need_states (
  id TEXT PRIMARY KEY,
  problem_name TEXT NOT NULL,
  detected_signal TEXT,
  severity TEXT,
  description TEXT
);
```

### need_state_products
```sql
CREATE TABLE need_state_products (
  id TEXT PRIMARY KEY,
  need_state_id TEXT NOT NULL,
  product_id TEXT NOT NULL,
  priority_order INTEGER DEFAULT 1,
  recommendation_reason TEXT,
  FOREIGN KEY(need_state_id) REFERENCES need_states(id),
  FOREIGN KEY(product_id) REFERENCES product_catalog(id)
);
```

### upsell_rules
```sql
CREATE TABLE upsell_rules (
  id TEXT PRIMARY KEY,
  primary_product_id TEXT NOT NULL,
  trigger_event TEXT,
  client_need_state_id TEXT,
  recommended_product_id TEXT NOT NULL,
  upsell_type TEXT,
  expected_impact TEXT,
  dependency_product_id TEXT,
  FOREIGN KEY(primary_product_id) REFERENCES product_catalog(id),
  FOREIGN KEY(recommended_product_id) REFERENCES product_catalog(id)
);
```

### cross_sell_rules
```sql
CREATE TABLE cross_sell_rules (
  id TEXT PRIMARY KEY,
  product_id TEXT NOT NULL,
  paired_product_id TEXT NOT NULL,
  reason TEXT,
  bundle_strength INTEGER DEFAULT 3,
  FOREIGN KEY(product_id) REFERENCES product_catalog(id),
  FOREIGN KEY(paired_product_id) REFERENCES product_catalog(id)
);
```

### clients
```sql
CREATE TABLE clients (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  segment TEXT,
  status TEXT,
  notes TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### opportunities
```sql
CREATE TABLE opportunities (
  id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  title TEXT NOT NULL,
  stage TEXT,
  detected_need_summary TEXT,
  owner_user_id TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(client_id) REFERENCES clients(id)
);
```

### recommendations
```sql
CREATE TABLE recommendations (
  id TEXT PRIMARY KEY,
  opportunity_id TEXT NOT NULL,
  recommendation_type TEXT NOT NULL,
  target_product_id TEXT NOT NULL,
  confidence_score REAL,
  rationale TEXT,
  status TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(opportunity_id) REFERENCES opportunities(id),
  FOREIGN KEY(target_product_id) REFERENCES product_catalog(id)
);
```

### agent_templates
```sql
CREATE TABLE agent_templates (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  purpose TEXT NOT NULL,
  system_prompt TEXT NOT NULL,
  tool_policy_json TEXT,
  output_schema_json TEXT,
  approval_mode TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

### agent_deployments
```sql
CREATE TABLE agent_deployments (
  id TEXT PRIMARY KEY,
  agent_template_id TEXT NOT NULL,
  name TEXT NOT NULL,
  scope_type TEXT,
  scope_id TEXT,
  status TEXT,
  config_json TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  FOREIGN KEY(agent_template_id) REFERENCES agent_templates(id)
);
```

### workflow_runs
```sql
CREATE TABLE workflow_runs (
  id TEXT PRIMARY KEY,
  workflow_type TEXT NOT NULL,
  status TEXT NOT NULL,
  input_json TEXT,
  output_json TEXT,
  started_at TEXT,
  finished_at TEXT,
  error_text TEXT
);
```

### google_sync_jobs
```sql
CREATE TABLE google_sync_jobs (
  id TEXT PRIMARY KEY,
  job_type TEXT NOT NULL,
  target_google_id TEXT,
  status TEXT NOT NULL,
  payload_json TEXT,
  result_json TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);
```

## Google Sheets Mapping
The app should export and optionally round-trip these tabs:
- Master_Catalog
- Upsell_Matrix
- Cross_Sell_Matrix
- Bundles
- Scoring_Model
- Client_Needs_Mapping
- Source_Index

## Import Strategy
1. Upload or connect a Sheet
2. Parse tabs into staging tables
3. Normalize names and IDs
4. Validate dependencies
5. Persist into core tables
6. Keep a sync snapshot

## Export Strategy
- export current DB state to a generated Google Sheet
- attach metadata row/version stamp
- preserve human-readable formatting
- never rely on sheet formulas as source of truth

## ID Strategy
Use UUIDv7 or ULID for sortable identifiers.

## Notes on SQLite
SQLite is fine for:
- single-tenant or low-concurrency deployments
- local-first workflows
- background job driven execution

Move to Postgres when:
- multiple concurrent users write frequently
- many long-running jobs update state simultaneously
- multitenancy becomes core
