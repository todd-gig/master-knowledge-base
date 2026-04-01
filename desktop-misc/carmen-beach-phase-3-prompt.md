# Carmen Beach Properties — Phase 3 Claude Code Prompt

## Optional execution constraints assumed
- Do not generate broad speculative architecture documents. Inspect the existing codebase first, then implement the smallest production-safe changes that unlock the required Phase 3 capabilities.
- Prefer Google-native services and workflows whenever the tradeoff is reasonable. Default to Google Cloud, Google Drive, Google Sheets, Google Docs, Gmail-compatible interfaces, and Cloud Run operational patterns.

## Prompt

You are continuing development of the Carmen Beach Properties monorepo.

Phase 3 objective:
Productionize the platform for real-world operations on Google Cloud, integrate Google Drive and Google Workspace surfaces, and harden the system for reliability, security, observability, and maintainability.

You must extend the existing implementation, not restart it.

Assume:
- Phase 1 delivered the core apps, DB, listings, admin, API, and tracking foundations
- Phase 2 delivered AI, automation, pricing, media pipeline, lead scoring, dashboards, and jobs/event architecture
- The codebase already exists and should be inspected before changes are made

Before writing code:
1. Inspect the repo
2. Infer the current architecture
3. Preserve naming, package boundaries, and conventions where sensible
4. Improve weak areas incrementally, not by rewriting the system

Do not stop at planning.
Implement production-ready code, configuration, deployment files, scripts, abstractions, and operational safeguards.

==================================================
PHASE 3 GOALS
==================================================

This phase must deliver:
1. Google Cloud deployment architecture
2. production infrastructure configs
3. Google Drive sync for media and docs
4. Google Workspace integration surfaces
5. secrets/config management
6. auth/security hardening
7. observability and alerting foundations
8. backup/recovery and data durability strategy
9. CI/CD and environment promotion
10. operational hardening for a small but serious production deployment

The system should be optimized for:
- Playa del Carmen real estate + tourism operations
- small geographic market dominance
- high operational leverage
- low-maintenance deployment
- future scale without premature complexity

==================================================
1. GOOGLE CLOUD DEPLOYMENT ARCHITECTURE
==================================================

Design and implement a practical Google Cloud deployment target.

Preferred runtime direction:
- Cloud Run for web/admin/api/services
- Cloud SQL for PostgreSQL
- Cloud Storage for media objects
- Secret Manager for secrets
- Artifact Registry for container images
- Cloud Build or GitHub Actions for deployment
- Cloud Logging and Cloud Monitoring for observability
- Pub/Sub or Cloud Tasks ready interfaces where appropriate

You must create infrastructure and deployment support for:
A. Public web app
B. Admin app
C. API / worker services
D. Background job runner
E. Scheduled jobs / cron-compatible workflows

If the repo currently uses a monolith, preserve it unless splitting is operationally necessary.
If separate services already exist, deploy them cleanly.

Required deliverables:
- Dockerfiles
- .dockerignore files
- Cloud Run service configs or deployment scripts
- environment variable templates
- service startup scripts
- production-ready health endpoints
- readiness/liveness checks where relevant

Create:
- /infra/gcp
- /scripts/deploy
- /scripts/ops

Include:
- dev
- staging
- prod environment strategy

==================================================
2. INFRASTRUCTURE-AS-CODE / DEPLOYMENT SUPPORT
==================================================

Implement infrastructure support using a pragmatic approach.

If Terraform is not present, add Terraform under:
- /infra/gcp/terraform

Provision or template support for:
- Cloud Run services
- Cloud SQL instance references
- Cloud Storage buckets
- service accounts
- IAM role bindings
- Secret Manager secrets references
- Artifact Registry repos
- logging/monitoring basics
- optional Pub/Sub topics/subscriptions for future use

Do not overbuild a massive enterprise platform.
Build a lean, production-usable stack.

Include:
- README for infra usage
- variable templates
- environment-specific tfvars examples
- safe naming conventions

If Terraform is too disruptive to add fully, at minimum provide:
- deploy scripts
- gcloud command wrappers
- environment configuration system
- clear separation between runtime and build configuration

==================================================
3. GOOGLE DRIVE SYNC
==================================================

Implement Google Drive sync capabilities for media and document ingestion.

Goals:
- ingest assets from Google Drive
- map Drive folders/files to properties or content objects
- sync metadata safely
- avoid duplicate imports
- support future background sync jobs

Create package/service:
- /packages/google-drive

Required capabilities:

### A. Authentication abstraction
Support service-account-friendly architecture where possible.
Design for secure OAuth/service integration later if required.

### B. Drive ingestion modes
- one-time import by folder/file ID
- recurring sync job
- metadata refresh
- dry-run mode

### C. Supported import types
- images
- PDFs
- brochures
- floorplans
- docs references
- videos via linked metadata if practical

### D. File mapping model
Track:
- drive_file_id
- drive_folder_id
- checksum/hash if available
- mime type
- file name
- modified time
- sync status
- linked property ID
- last imported asset ID

### E. Duplicate prevention
Do not re-import unchanged files.
Use file IDs + checksums + modified timestamps where appropriate.

### F. Import workflow
For each supported file:
- fetch metadata
- download or stream file if needed
- pass through media/document ingestion pipeline
- attach to relevant entity
- log sync result

Database additions if needed:
- drive_sync_connections
- drive_sync_jobs
- drive_sync_items
- external_file_links

Admin UI requirements:
- connect/configure sync source placeholder
- import by Drive folder ID
- view sync job history
- view per-file sync status
- relink unmatched files to properties
- dry-run preview

API requirements:
- POST /api/google-drive/import
- POST /api/google-drive/sync/:jobId/run
- GET /api/google-drive/jobs
- GET /api/google-drive/items
- PATCH /api/google-drive/items/:id/link

Keep the adapter abstraction clean so later extension to:
- shared drives
- user OAuth
- Docs/Sheets content extraction
is straightforward.

==================================================
4. GOOGLE WORKSPACE INTEGRATION SURFACES
==================================================

Implement practical integration surfaces for Google Workspace.

Create:
- /packages/google-workspace

Required integration targets:

### A. Google Sheets import/export
Use case examples:
- property import
- owner list import
- pricing assumptions import
- lead export
- reporting export

Capabilities:
- import rows from Sheet
- validate columns
- map columns to domain models
- export reports to Sheets
- dry-run validation before import

### B. Google Docs / document linking
Do not overbuild document editing.
Support:
- storing links
- associating Docs with properties, owners, campaigns, or workflows
- optionally extracting lightweight metadata

### C. Gmail-ready notification interface
Do not require full Gmail send unless easy to support cleanly.
At minimum build:
- notification provider interface
- Google Workspace/Gmail adapter stub
- templated email structure
- event-triggered notification hooks

### D. Google Calendar integration surface
Provide abstraction and placeholder adapter for:
- property viewing scheduling
- follow-up reminders
- booking-related blocks in future

Admin UI requirements:
- import/export center
- Sheets import history
- download validation errors
- Docs link management
- notification template preview

API examples:
- POST /api/workspace/sheets/import
- POST /api/workspace/sheets/export
- GET /api/workspace/import-jobs/:id
- POST /api/workspace/docs/link
- POST /api/workspace/notifications/test

==================================================
5. STORAGE MIGRATION TO GOOGLE CLOUD STORAGE
==================================================

If media storage is still local/dev-based, implement cloud storage support.

Create or extend:
- storage adapter abstraction

Support:
- local storage adapter for dev
- Google Cloud Storage adapter for staging/prod

Required capabilities:
- upload asset
- delete asset
- generate signed URL or public URL strategy
- manage derivative paths
- bucket path conventions by entity/type/date
- metadata attachment

Implement:
- robust path normalization
- content-type handling
- object naming strategy
- duplicate-safe writes
- configurable public/private buckets or prefixes

Update media ingestion pipeline to use the adapter cleanly.

==================================================
6. AUTHENTICATION AND SECURITY HARDENING
==================================================

Harden access and security across the platform.

Requirements:
- secure admin authentication
- role-based access control
- route protection
- API authorization checks
- least-privilege service boundaries
- CSRF/XSS-safe patterns where relevant
- secure cookie/session settings
- rate limiting on sensitive endpoints
- audit logging for admin actions

Roles should support at minimum:
- super_admin
- admin
- editor
- operations
- viewer

Sensitive actions to audit:
- property publish/unpublish
- pricing override
- AI approval/rejection
- lead reassignment
- media deletion
- sync job execution
- workflow/manual job retry

Add:
- audit_logs table if not present
- middleware for auth checks
- permission utilities
- admin session hardening

If auth is weak or absent, implement a practical production-safe auth system consistent with current stack.
Do not bolt on unnecessary complexity.

==================================================
7. CONFIGURATION, SECRETS, AND ENVIRONMENT MANAGEMENT
==================================================

Implement production-safe configuration handling.

Requirements:
- typed environment validation
- separate configs for dev/staging/prod
- Secret Manager compatible loading strategy
- no secrets committed
- startup failure on invalid configuration
- config docs for operators

Create:
- shared config package if not present
- environment schema validation
- .env.example files
- secrets mapping docs

Support configs for:
- database
- storage
- AI provider
- Google integrations
- auth/session
- logging
- notifications
- deployment environment
- public base URLs

==================================================
8. OBSERVABILITY AND MONITORING
==================================================

Add production-grade operational visibility.

Implement:
- structured application logging
- request correlation IDs
- trace-friendly logging hooks
- job execution logs
- sync logs
- auth/audit logs
- error capture boundary
- health endpoints
- metrics-friendly counters where practical

Create:
- /packages/observability

Requirements:
- JSON logs in production
- human-readable logs in dev
- consistent logger interface
- request_id propagation
- session_id logging where appropriate
- workflow/job IDs attached to logs
- external sync provider errors captured clearly

Admin operational surfaces:
- job monitor
- sync monitor
- recent failures view
- audit log view

Prepare system for:
- Cloud Logging
- Cloud Monitoring dashboards
- alert policies later

If practical, include sample alertable conditions for:
- repeated job failures
- sync failures
- elevated 5xx rate
- failed AI generation spikes
- storage upload failures

==================================================
9. BACKUPS, DURABILITY, AND RECOVERY SUPPORT
==================================================

Implement operational support for resilience.

Requirements:
- backup strategy documentation
- DB backup/restore workflow docs
- media durability assumptions
- sync idempotency
- retry-safe jobs
- migration safety scripts
- seed separation from production data handling

Provide:
- operational README
- runbooks for common issues
- scripts for:
  - migration
  - rollback guidance
  - seed in non-prod
  - integrity checks

If code changes are needed:
- add backup-related config surfaces
- add data integrity verification jobs where useful
- ensure critical write paths are idempotent

==================================================
10. CI/CD AND RELEASE MANAGEMENT
==================================================

Implement a practical delivery pipeline.

Preferred direction:
- GitHub Actions if repo is on GitHub
- Cloud Build compatible deployment support if useful

Requirements:
- install/test/build workflow
- lint/typecheck/test gates
- database migration step strategy
- image build and push
- environment-specific deploy workflow
- branch/environment mapping
- safe production deploy steps
- manual approval point for production if appropriate

Create:
- .github/workflows/*

Suggested workflows:
- ci.yml
- deploy-staging.yml
- deploy-prod.yml

Include:
- caching
- monorepo-aware build targeting if practical
- secrets/env expectations documentation

==================================================
11. SCHEDULED JOBS / OPERATIONS AUTOMATION
==================================================

Implement support for recurring operational jobs.

Examples:
- nightly Drive sync
- pricing refresh job
- stale lead review job
- media integrity check
- AI content backlog processor
- analytics rollup job

Support:
- cron-triggered execution surface
- Cloud Scheduler compatibility
- lock/idempotency protection
- job history recording

API or worker entrypoints should make scheduled jobs easy to invoke.

==================================================
12. ADMIN OPERATIONS CENTER
==================================================

Extend admin with a real operations center.

Required sections:
- deployment/environment info summary
- recent job runs
- recent sync runs
- recent failures
- audit logs
- config health checks
- storage status summary
- integration status summary
- background queue health

This should help an operator quickly identify:
- what is broken
- what is delayed
- what needs attention

Do not make it decorative.
Make it operationally useful.

==================================================
13. DATA MODEL EXTENSIONS
==================================================

Add or extend models as required for:
- audit_logs
- drive_sync_connections
- drive_sync_jobs
- drive_sync_items
- external_file_links
- import_jobs
- import_job_rows
- export_jobs
- integration_status_records
- deployment_events (optional if useful)
- config_validation_snapshots (optional if useful)

Maintain:
- indexes
- foreign keys
- clear naming
- sane timestamps
- status enums where helpful

==================================================
14. API AND INTERNAL SERVICE REQUIREMENTS
==================================================

Add or extend APIs for:

Deployment / ops:
- GET /api/ops/health
- GET /api/ops/readiness
- GET /api/ops/status
- GET /api/ops/audit-logs
- GET /api/ops/failures

Google Drive:
- POST /api/google-drive/import
- POST /api/google-drive/sync/run
- GET /api/google-drive/jobs
- GET /api/google-drive/items
- PATCH /api/google-drive/items/:id/link

Workspace:
- POST /api/workspace/sheets/import
- POST /api/workspace/sheets/export
- GET /api/workspace/import-jobs/:id
- POST /api/workspace/docs/link
- POST /api/workspace/notifications/test

Jobs / schedules:
- POST /api/jobs/run/:jobName
- GET /api/jobs/history
- POST /api/jobs/:id/retry

All sensitive routes must be protected.

==================================================
15. TESTING AND HARDENING
==================================================

Add tests for:
- config validation
- auth guards / RBAC
- storage adapter behavior
- Drive sync deduplication logic
- Sheets import validation
- audit logging
- job retry/idempotency behavior
- health/readiness routes

At minimum include:
- unit tests for packages
- integration tests for critical flows
- smoke checks for deployment entrypoints

==================================================
16. DOCUMENTATION
==================================================

Create or update docs for:
- local development
- staging deployment
- production deployment
- environment setup
- secret setup
- Google Cloud setup
- Drive sync setup
- Sheets import usage
- storage configuration
- operations runbook
- incident response basics
- backup/restore guidance

Create concise operator-facing docs.
Do not bury essential setup in vague prose.

==================================================
17. IMPLEMENTATION ORDER
==================================================

Build in this order:
1. inspect existing repo and identify current architecture
2. config and env validation
3. storage abstraction and GCS adapter
4. auth/security hardening and audit logs
5. Google Drive package and sync pipeline
6. Google Workspace package and Sheets import/export
7. observability/logging package
8. ops APIs and admin operations center
9. deployment infra, Dockerfiles, scripts, and CI/CD
10. scheduled job support
11. docs and tests

==================================================
18. CONSTRAINTS
==================================================

- Keep TypeScript strict
- Prefer incremental hardening over rewrites
- Keep deployment lean and practical
- Avoid unnecessary managed services unless they materially improve operations
- Preserve local development ergonomics
- Keep Google Cloud as the primary production target
- Avoid fake production claims; if something is stubbed, label it clearly in code/config
- Favor interfaces and adapters over vendor lock-in at the domain layer
- Design for a small high-performance team

==================================================
DELIVERABLE
==================================================

Implement the full Phase 3 code incrementally.

For every major system added, include:
- real code
- config
- tests where appropriate
- docs
- operational guardrails

Do not stop at planning.
Write the code.
