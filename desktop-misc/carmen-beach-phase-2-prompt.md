# Carmen Beach Properties — Phase 2 Claude Code Prompt

## Optional execution constraints assumed
- Before writing code, inspect the existing repo and infer Phase 1 implementation details. Then continue Phase 2 in a way that preserves current architectural patterns, naming conventions, linting rules, and package boundaries. Where existing patterns are weak, improve them minimally rather than rewriting the system.
- Reject shallow scaffolding. Prefer working vertical slices with real schema, routes, services, and admin screens over placeholder files.

## Prompt

You are continuing development of the Carmen Beach Properties monorepo.

Phase 1 already established:
- monorepo structure
- public web app
- admin app
- database schema
- listings and property detail pages
- inquiry capture
- basic tracking
- basic affiliate tracking

Now implement **Phase 2**.

This phase adds:
1. AI enrichment
2. automation workflows
3. pricing / occupancy intelligence
4. media ingestion pipeline
5. lead scoring and routing
6. operational dashboards
7. data pipelines for future optimization

Do **not** re-architect the repo unless necessary.
Extend the existing system cleanly.
Prefer modular packages and service boundaries.
Do not produce placeholder strategy notes. Implement.

==================================================
BUSINESS GOAL
==================================================

Build an intelligence and automation layer that turns Carmen Beach Properties into an acquisition, conversion, and revenue optimization engine for a small geographic market.

The system must:
- enrich listing quality automatically
- operationalize media ingestion
- improve lead handling speed
- support revenue optimization for short-term rental inventory
- build a foundation for AI-assisted growth and decision making

==================================================
PHASE 2 MODULES
==================================================

1. AI CONTENT ENRICHMENT
2. AUTOMATION WORKFLOWS
3. PRICING + OCCUPANCY ENGINE
4. MEDIA INGESTION + NORMALIZATION
5. LEAD SCORING + ROUTING
6. INTERNAL DASHBOARDS
7. BACKGROUND JOBS + EVENT PIPELINE
8. FUTURE-READY INTEGRATION SURFACES

==================================================
1. AI CONTENT ENRICHMENT
==================================================

Implement an AI enrichment service for property listings.

Goals:
- improve quality and completeness of listing data
- standardize property descriptions
- generate multilingual marketing copy
- extract structured data from raw notes
- produce SEO assets

Create package/service:
- /packages/ai

Implement capabilities:

### A. Listing description generation
Input:
- property facts
- amenities
- neighborhood / proximity data
- style / positioning tags

Output:
- short description
- long description
- headline
- meta title
- meta description
- key selling points
- lifestyle framing

### B. Multilingual support
Generate content for:
- English
- Spanish

### C. Structured extraction
Input:
- freeform notes from admin
- owner notes
- media captions

Output structured suggestions for:
- amenities
- property type
- occupancy hints
- condition / renovation status
- nearby attractions
- target guest profile

### D. Content confidence / approval workflow
AI-generated content must be stored as:
- draft
- approved
- rejected

Admin must be able to approve or override.

Database additions:
- ai_content_generations
- ai_content_versions
- ai_extraction_suggestions

Each record should include:
- source inputs hash
- model name
- generated_at
- status
- reviewer
- approved_at

Expose admin actions:
- Generate AI copy
- Regenerate
- Approve
- Reject
- Promote approved copy to live listing

Do not hardcode a provider.
Abstract provider behind interface:
- generateListingContent()
- extractStructuredListingData()

Stub adapter can be implemented first.

==================================================
2. AUTOMATION WORKFLOWS
==================================================

Implement an internal automation engine for operational workflows.

Create:
- /packages/automation

Use event-driven triggers from existing system actions.

Required workflows:

### A. New inquiry automation
When inquiry created:
- create lead activity record
- assign score
- assign route based on rules
- queue follow-up task
- optionally send notification event

### B. New property automation
When new property created:
- validate completeness
- generate missing content suggestions
- mark missing media requirements
- queue AI enrichment
- queue SEO readiness check

### C. Media upload automation
When new media ingested:
- generate derivatives
- classify media type
- attach to property
- queue alt text generation
- queue quality validation

### D. Affiliate attribution automation
When attributed session converts:
- link affiliate to inquiry / lead
- write attribution record
- calculate commissionable event marker

Implement:
- job table
- job runner abstraction
- retry support
- dead-letter status
- event log

Database additions:
- jobs
- workflow_events
- lead_activities
- attribution_records

Include a local dev runner and a clean interface for future Cloud Run jobs or Pub/Sub workers.

==================================================
3. PRICING + OCCUPANCY ENGINE
==================================================

Implement a pricing intelligence module focused on short-term rental optimization.

Create:
- /packages/pricing

This is not a full dynamic pricing engine yet.
Build a rules + signal framework that can evolve.

Core goals:
- estimate recommended nightly rate bands
- estimate occupancy scenarios
- support manual overrides
- record assumptions

Inputs:
- property characteristics
- bedroom/bathroom count
- guest capacity
- location / zone
- amenities
- seasonality period
- day of week
- target occupancy
- historical performance data if available
- competitor comps if available later
- owner constraints (minimum acceptable rate, blackout preferences)

Outputs:
- recommended_base_rate
- recommended_weekend_rate
- recommended_peak_rate
- occupancy_target_low
- occupancy_target_base
- occupancy_target_high
- confidence_score
- assumptions array
- rationale summary

Database additions:
- pricing_profiles
- pricing_recommendations
- pricing_inputs
- occupancy_snapshots

Admin UI requirements:
- pricing tab on property
- manual override controls
- view rationale and assumptions
- scenario compare view

Initial implementation:
- rule-based engine
- seasonality profiles
- configurable multipliers by:
  - zone
  - bedroom count
  - amenity tier
  - season
  - stay length
  - weekend vs weekday

Also implement import-ready support for future performance data.

Do not fake market data.
Use explicit seeded assumptions and label them as assumptions.

==================================================
4. MEDIA INGESTION + NORMALIZATION
==================================================

Implement a media pipeline for images, video references, drone assets, and future Matterport support.

Create:
- /packages/media

Supported media concepts:
- image
- video
- drone
- floorplan
- matterport_link
- brochure_pdf
- document

Goals:
- normalize metadata
- attach media to properties
- generate derivatives
- classify content
- support ordered galleries
- support featured media
- support AI-generated alt text / captions

Core features:

### A. Ingestion sources
- admin upload
- external URL
- batch import manifest
- future Google Drive sync surface

### B. Processing
For images:
- validate dimensions
- create thumbnails
- create optimized web sizes
- extract EXIF if present
- compute blurhash or placeholder
- classify orientation

For videos / drone:
- save metadata
- store thumbnail reference
- allow embed / hosted URL mode

For Matterport:
- store and validate external tour URL
- present as virtual tour asset type

### C. Media quality signals
Track:
- resolution
- aspect ratio
- blur / sharpness heuristic placeholder
- missing caption
- missing alt text
- duplicate detection hash

### D. Property media completeness scoring
Example:
- has hero image
- has at least N gallery images
- has location-context media
- has lifestyle media
- has virtual-tour asset
- has captions

Database additions:
- media_assets (extend if exists)
- media_derivatives
- media_analysis
- property_media_scores

Admin UI:
- reorder gallery
- mark featured media
- edit captions / alt text
- see completeness issues
- ingest from URL
- attach Matterport link

Implement storage abstraction.
Use local storage adapter for now with future cloud object storage compatibility.

==================================================
5. LEAD SCORING + ROUTING
==================================================

Implement a lead intelligence module.

Create:
- /packages/leads

Goals:
- score leads for sales readiness
- distinguish rental vs purchase intent
- prioritize high-value opportunities
- route leads by rules

Signals to use:
- inquiry source
- affiliate source
- viewed properties count
- viewed property price bands
- return visits
- session duration
- proximity of inquiry to high-intent actions
- preferred contact method
- budget fields if available
- booking dates if available
- rental vs sale flags
- lead completeness

Output:
- lifecycle_stage
- intent_type
- score
- priority
- routing_queue
- explanation

Suggested lifecycle stages:
- new
- qualified
- high_intent
- nurture
- disqualified

Intent types:
- rental
- purchase
- owner_supply
- affiliate
- unknown

Admin requirements:
- lead queue
- filters
- score view
- explanation / why scored
- manual override

Database additions:
- leads
- lead_scores
- lead_routes
- lead_notes

Routing engine:
- configurable rules
- assign by geography
- assign by intent type
- assign by score threshold

==================================================
6. INTERNAL DASHBOARDS
==================================================

Implement internal dashboards in admin.

Required dashboards:

### A. Inventory dashboard
- total properties
- active listings
- draft listings
- missing content
- missing media
- AI approval backlog

### B. Lead dashboard
- inquiries by day
- leads by source
- leads by intent
- leads by priority
- affiliate-attributed leads
- response SLA placeholder

### C. Pricing dashboard
- properties with pricing profiles
- properties missing rates
- recommendation confidence distribution
- override rate count

### D. Media dashboard
- properties with incomplete galleries
- assets missing alt text
- assets missing captions
- virtual-tour coverage

### E. Attribution dashboard
- sessions by source / medium / campaign
- inquiries by source
- affiliate conversion counts

Use server-rendered admin pages where practical.
Use simple chart components.
No unnecessary charting complexity.

==================================================
7. BACKGROUND JOBS + EVENT PIPELINE
==================================================

Implement a lightweight event + job architecture.

Requirements:
- domain events emitted from app actions
- durable event records in database
- job scheduler / runner
- retry with backoff
- idempotency key support

Example events:
- inquiry.created
- property.created
- property.updated
- media.ingested
- session.converted
- ai.content.requested
- ai.content.approved
- pricing.recommendation.generated

Provide:
- event emitter abstraction
- job dispatch API
- worker entrypoint
- local development mode

This must be designed so future migration to:
- Pub/Sub
- Cloud Tasks
- Cloud Run jobs
is straightforward.

==================================================
8. FUTURE-READY INTEGRATION SURFACES
==================================================

Prepare clean interfaces for future integrations, even if not fully implemented yet.

Interfaces required for:
- Google Drive media source sync
- Google Sheets/CSV property import
- WhatsApp follow-up messaging
- email notification provider
- external AI provider
- PMS/calendar sync
- pricing comp ingestion
- Matterport enrichment
- CRM export

Implement adapters/interfaces with no-op or mock local providers if needed.

==================================================
DATABASE CHANGES
==================================================

Update Prisma schema with all new models required for:
- ai_content_generations
- ai_content_versions
- ai_extraction_suggestions
- jobs
- workflow_events
- lead_activities
- attribution_records
- pricing_profiles
- pricing_recommendations
- pricing_inputs
- occupancy_snapshots
- media_derivatives
- media_analysis
- property_media_scores
- leads
- lead_scores
- lead_routes
- lead_notes

Maintain clean relations and indexes.

==================================================
API REQUIREMENTS
==================================================

Add APIs for:

AI:
- POST /api/ai/listings/:id/generate
- POST /api/ai/listings/:id/extract
- POST /api/ai/content/:id/approve
- POST /api/ai/content/:id/reject

Media:
- POST /api/media/upload
- POST /api/media/import-url
- PATCH /api/media/:id
- POST /api/media/:id/feature
- POST /api/media/reorder

Pricing:
- POST /api/pricing/:propertyId/recommend
- PATCH /api/pricing/:propertyId/override
- GET /api/pricing/:propertyId

Leads:
- GET /api/leads
- GET /api/leads/:id
- POST /api/leads/:id/score
- POST /api/leads/:id/route
- PATCH /api/leads/:id

Automation:
- POST /api/workflows/run/:workflowName
- GET /api/jobs
- POST /api/jobs/:id/retry

==================================================
ADMIN UI REQUIREMENTS
==================================================

Add or extend admin screens for:
- AI content review
- media ingestion and gallery management
- pricing tab and recommendations
- lead queue and scoring
- dashboards
- workflow/job monitor

UI should prioritize:
- speed
- clarity
- operational usefulness

==================================================
SEED DATA
==================================================

Add realistic seed data for:
- properties
- property owners
- inquiries
- sessions
- affiliates
- media assets
- pricing assumptions
- AI drafts
- lead scores

Use Playa del Carmen style sample content, but clearly mark all sample data as fictional.

==================================================
TESTING
==================================================

Add tests for:
- pricing rules engine
- lead scoring logic
- workflow triggers
- AI content state transitions
- media completeness scoring
- attribution linkage

At minimum include:
- unit tests for packages
- integration tests for critical API flows

==================================================
IMPLEMENTATION ORDER
==================================================

Build in this sequence:
1. Prisma schema changes
2. shared packages:
   - ai
   - automation
   - pricing
   - media
   - leads
3. background event/job system
4. API routes
5. admin UI surfaces
6. seed data
7. tests

==================================================
OPERATING CONSTRAINTS
==================================================

- Keep TypeScript strict
- Keep architecture modular
- Do not add unnecessary third-party SaaS dependencies
- Favor first-party/local abstractions
- Keep Google Cloud compatibility in mind
- Prefer deterministic, reviewable workflows over black-box automation
- Do not use fake external market data
- Clearly label assumptions where data is synthetic

==================================================
DELIVERABLE
==================================================

Implement the full Phase 2 code incrementally.
When making assumptions, encode them as configuration, not prose.

Do not stop at planning.
Write the code.
