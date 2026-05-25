---
type: decision-log
established: 2026-05-25
status: ACTIVE — running log of architecture decisions ratified during the EOD 2026-05-25 sprint planning + beta-launch + 30-day-arc work
authority: locked unless explicitly revisited
applies_to:
  - master-knowledge-base
  - all 11 Gigaton engines
  - all entity-creation flows
  - all 50/day automation work
---

# Architecture Decisions Log — 2026-05-25

Captures all decisions ratified during the 2026-05-25 session. Each entry: decision + rationale + source agent + applied scope.

---

## Already locked (prior sessions, restated here for cross-reference)

### B1-B5 — Billing architecture (locked 2026-05-22)
- **B1** Single platform Stripe account; entities are Customers within one Gigaton-owned Stripe
- **B2** Per-product-and-service-package billing model
- **B3** Billing logic lives inside `gigaton-engine`
- **B4** Per-deal-and-package cadence
- **B5** Stripe Tax (`automatic_tax: {enabled: true}`)
- Source: `decisions/2026-05-22_billing_architecture_choices.md`

### Modular replication doctrine
- Same engines + swap `operator_context`. Multi-axis JSONB tags on every datum.
- No hardcoded operator/entity names. Bespoke ≠ log-function improvement.
- Source: `[[foundational_modular_replication_via_input_substitution]]`

### Beta-launch openness model (selected EOD 2026-05-25)
- Beta opens AFTER consolidated deploy (migration + Wave 1 + ToS/Privacy complete) — "regardless of when"
- Invite-only, cap N ≤ 25 week-1
- **Non-EU operators only** until `DELETE /v1/operators/{id}` ships
- Source: production hardening audit + user confirmation

---

## Locked TONIGHT 2026-05-25

### IEB-1 — Multipli stays as example #1, NOT a sprint deliverable
- "Better to complete Multipli next week correctly than rush a one-off"
- Original Tue 5/26 EOD internal-readiness deadline = DROPPED
- Multipli "complete correctly" target = Week 3 (~6/15) as the first sample of the 50/day pipeline
- Calendly Phase A bundle (manual) remains as proof-of-concept
- Source: user message, agent: Multipli bundle producer

### IEB-6 — Bundle type taxonomy: ALL 3 TYPES UP-FRONT (Week 1)
- NOT phased (vendor_financing only Week 1, then expand)
- The 3 types: vendor_financing (Multipli-class), plus 2 more to be defined in the IEB architecture doc instantiation
- Source: user message 2026-05-25 evening

### IEB-7 — Self-serve gap-fill UI: parallel with first paid bundle; STABLE ENGINES FIRST
- Order: stable engines → first paid bundle → self-serve gap-fill UI in parallel
- "Ensure stable engines first then continue"
- Source: user message 2026-05-25 evening

### EF-1 (entity-flow #1) — Subdomain auto-provision: USER APPROVED DEFAULT
- Free auto-provision `<slug>.gigaton.ai` available to all entity types in v1 (zero-friction sign-up)
- Re-evaluate gating to paid tiers post-launch if abuse surfaces
- Source: agent recommendation, user "approve all" 2026-05-25

### EF-2 — Max entities per affiliate: 5 HARD CAP, 3 SOFT WARNING
- Hard cap 5 entities per affiliate human
- Soft warning at 3 (prompts affiliate to articulate distinct use cases)
- Manual review on appeal
- Combined with domain + business email ownership requirement = anti-sockpuppet
- Source: agent recommendation, user "approve all" 2026-05-25

### EF-3 — Domain verification: DNS TXT
- Verification = DNS TXT record (not email-WHOIS, not file-upload)
- Standard industry practice; works for both BYO domains and Gigaton subdomains
- Source: agent recommendation, user "approve all" 2026-05-25

### EF-4 — Marketing-agency + unified-real-estate kept as DISTINCT entity types
- NOT collapsed into property_management variant
- Their default integrations (paid-channel + creative for marketing; multi-property+agent+brand for real-estate) are different enough to warrant separate types
- Source: agent recommendation, user "approve all" 2026-05-25

### EF-5 — Direct signup NOT allowed in v1; AFFILIATE-GATED ONLY
- Every entity creation must originate from a Gignet affiliate code
- Aligns with "each human = affiliate" doctrine
- Re-evaluate for v1.1 once first-100 affiliates are seasoned
- Source: agent recommendation, user "approve all" 2026-05-25

### EF-6 — Stripe Customer granularity: PER ENTITY (not per affiliate)
- Each entity gets its own Stripe Customer record under platform Stripe account
- Affiliates can be linked via metadata, but billing-level isolation is per-entity
- Honors B1 (single Stripe) + B2 (per-package) + EF-2 (one affiliate, ≤5 entities each independently billable)
- Source: agent recommendation, user "approve all" 2026-05-25

### EE-1 (entity-ecosystem #1) — Ti = ALL DBAs under Todd (NOT separate LLCs)
- Ti Life + Ti Solutions + Total Interactions are all DBAs owned by Todd
- Maps cleanly to B1 single-Stripe platform account
- Source: user message 2026-05-25

### EE-2 — Carmen Beach FIRST paid entity (after Multipli + 50/day complete)
- ORDER CHANGE from earlier 30-day roadmap (which had Carmen Beach Week 2 Mon 6/02)
- New order: (1) Multipli proposals complete → (2) 50/day automation stable → (3) Carmen Beach launches as first paid revenue entity → (4) Gigaton SaaS + Ti DBAs follow
- "Ensure minimum value > product commitments achieved" — quality > date
- Source: user message 2026-05-25

### SEC-1 (security #1) — Orphan persona-engine SA key 36679d3a REVOKED
- Date: 2026-05-25T~20:00 UTC
- Reason: user lost off-disk per [[persona_engine_sa_key_rotation_2026_05_22]]; +7d hold expired by beta launch
- Remaining keys: 21a0cb32 (active, GHA secret) + 7f46371b (revoke attempt FAILED_PRECONDITION; under investigation)

### SEC-2 — Namespace admin gate FLIPPED STRICT
- UAE env `UAE_REQUIRE_CAPABILITIES=true` LIVE
- Rev `user-access-engine-00028-6wr` serving 100% traffic
- Date: 2026-05-25T~19:55 UTC
- Reverts if any onboarding flow breaks; smoke against carmen-beach + fresh operators all pass on relevant axes

### DB-1 (database #1) — Migration 004 (industry_catalogs) APPLIED to decision-engine-pg
- Date: 2026-05-25T~19:50 UTC
- Result: BEGIN / CREATE TABLE / 2× CREATE INDEX / GRANT / COMMIT all clean
- Wave 1 of Stage 5 self-healing now has its database substrate

### DB-2 — gigaton-engine-pg POST-PROVISION COMPLETE in carmen-beach-properties
- Created: `gigaton_engine` database + `gigaton_engine` user + `gigaton-engine-pg-app-pw` secret v1
- Date: 2026-05-25T~20:05 UTC
- Per ADR B3 (billing inside gigaton-engine)

### MIG-1 (migration #1) — carmen-beach → gigaton-platform migration PRIORITIZED + Day 0 COMPLETE
- 4 engines migrating: decision-engine, intelligence-silo, gigaton-engine, sales-operating-system
- Mirror created in gigaton-platform: 3 Cloud SQL instances (decision-engine-pg, intelligence-silo-pg, gigaton-engine-pg) + 4 runtime SAs + 4 secrets
- Day 1-7 runbook at `runbooks/2026_05_25_carmen_to_gigaton_migration_day_by_day.md`
- 7-day soak target completion: Mon 2026-06-08
- Confidence: YELLOW (depends on 4 blockers — GHA billing now ✅, OAuth redirect URIs pending, sales-OS persistence ambiguity, phantom gigaton-silo-index bucket)
- Source: user direction "prioritize carmen-beach → gigaton centralized intelligence + database"

### MIG-1.1 — carmen-beach-properties scope NARROWED (not abandoned)
- Carmen Beach Properties KEEPS its GCP project + becomes a SCOPED TENANT
- Scope: real-estate-business-specific resources only (the actual property bookings, OTA connectors, host accounting, property dashboards)
- ALL intelligence + systems (decision-engine, intel-silo, gigaton-engine, sales-OS, gateway, UAE, HME, ppeme, persona-engine, connector-api) consolidate to gigaton-platform
- Carmen Beach engines stop being co-owners of platform infrastructure → become tenants/consumers of it
- This is the cleanest model: Carmen Beach gets first-class real-estate features in the platform; doesn't share project-level resources with other tenants
- Source: user message 2026-05-25 evening — "do not want to abandon carmen beach, but that entity with only be for real estate activities and all intelligence / systems should be managed by gigaton"

### MIG-3 RESOLVED — gigaton-silo-index bucket created empty as precaution
- Intel-silo cloudbuild.yaml references `GCS_BUCKET=gigaton-silo-index` but no Python code uses the value — likely dead env var
- Created empty bucket in gigaton-platform tonight as belt-and-suspenders before Day 2 migration
- Week 2 audit: confirm dead, drop env var
- Source: user "Yes — create empty bucket"

### MIG-4 RESOLVED — sales-OS gets dedicated Cloud SQL instance
- sales-OS currently SQLite on Cloud Run local disk = ephemeral data loss every revision
- User decision: data MATTERS, must persist
- Provisioned `sales-os-pg` Cloud SQL in gigaton-platform tonight (db-f1-micro POSTGRES_15)
- Day 4 migration includes: provision sales_os DB+user+secret, run alembic migrations against new DB, flip DATABASE_URL env var, cutover traffic
- Adds ~$10/mo + ~10min of Day 4 work
- Source: user "Yes — needs persistence"

### MIG-2 — gigaton-engine-pg canonical instance: gigaton-platform (pending user confirm)
- Per user direction MIG-1.1: all intelligence/data systems migrate to gigaton-platform
- Therefore canonical `gigaton-engine-pg` = gigaton-platform instance (provisioned tonight)
- Carmen-beach `gigaton-engine-pg` (also provisioned tonight) deprecates on Day 7 / migration complete

### SEC-1.1 — 7f46371b SA key remains active (revoke blocked)
- gcloud `keys delete` returns FAILED_PRECONDITION even with auth
- Hypothesis: key bound to a Cloud Build trigger or similar dependency we haven't traced
- Not beta-blocking: current GHA secret on persona-engine uses `21a0cb32` (verified 2026-05-22T18:58Z); 7f46371b appears inert
- Re-investigate post-migration (Week 2+) when system surface stabilizes; if still revoke-resistant, may need to delete the SA itself + recreate

### LAUNCH-1 — ONE CONSOLIDATED DEPLOY before beta opens
- Doctrine: "Assume 1 more deployment with migration complete prior to beta launch regardless of when that is to ensure minimum value > product commitments achieved"
- That single deploy bundles: migration completion + Wave 1 + ToS/Privacy + gateway healthz fix
- Beta opens AFTER that single deploy + 7-day migration soak
- Replaces earlier "freeze starts EOD tonight" framing
- Source: user message 2026-05-25 evening

---

## Final batch ratified 2026-05-25 EOD

### IEB-8 RESOLVED — Python compliance classifier: BUILD IT
- Week 2: collect human-labeled bundle samples (~100 examples target)
- Week 3: train + ship Python classifier alongside regex+Haiku gate
- ~3-5 days ML investment, reduces false-negative rate significantly
- Source: user ratification 2026-05-25 EOD

### IEB-9 RESOLVED — Ti Solutions branding: brand_dimensions catalog row per DBA
- Each Ti DBA (Ti Life / Ti Solutions / Total Interactions) = a row in intel-silo's `brand_dimensions` catalog
- Same engine swaps brand_context per request — honors modular replication doctrine
- Zero net-new repos, zero forks
- Source: user ratification 2026-05-25 EOD

### IEB-10 LOCKED-BY-DEFAULT — Stripe metering: per-bundle
- One Stripe usage record per delivered bundle
- Aligns with locked B2 ADR (per-product-and-service-package)
- Simplest reconciliation surface
- User did not override default; locked

### 30D-3 RESOLVED — Ti DBA domains: subdomains under ti.gigaton.ai
- `life.ti.gigaton.ai`, `solutions.ti.gigaton.ai`, `total.ti.gigaton.ai`
- Fastest setup; no extra DNS or domain purchases
- Easy upgrade to BYO apex (e.g. tisolutions.co) per DBA later if brand-driven
- Honors entity-creation flow EF-1 (free auto-subdomain) for Ti as a "platform tenant"
- Source: user ratification 2026-05-25 EOD

### 30D-4 RESOLVED — Carmen Beach Stripe Connect: IMMEDIATELY (not manual)
- Set up Stripe Connect Express accounts per property owner from Day 1
- Bookings auto-split: platform fee + owner share at booking-time
- Adds 2-3 days of setup + KYC per owner
- **CRITICAL prerequisite for Carmen Beach launch (Week 5 per EE-2 reorder)** — must start in Week 1 design phase
- Scales cleaner than manual invoicing; eliminates monthly reconciliation overhead
- Source: user ratification 2026-05-25 EOD

## Support BETA-1 design completed — see separate doc
- `docs/architecture/2026_05_25_omnichannel_support_design.md`
- 5 channels: email + SMS + WhatsApp + platform chat + Slack (team triage)
- 12 net-new endpoints across 5 existing engines; ZERO new services
- 5 sub-decisions emerged (email vendor / Slack workspace strategy / default reply channel / AI pre-draft UX / resolution detection) — queue for Week 1 design

### Support omnichannel sub-decisions ratified 2026-05-25 EOD
- **Slack workspace:** `gigaton-ai.slack.com` CREATED + initial members `todd@gigaton.ai` (admin), `bella@gigaton.ai`, `matt@gigaton.ai`. Per-operator `#support-{op_id}` channels auto-create during entity onboarding. Source: user 2026-05-25 EOD
- **Email vendor:** **Gmail API + Google Workspace** (NOT SendGrid). Honors Google-stack preference + native Pub/Sub inbound (aligns with Gignet orchestrator) + existing intel-silo Gmail OAuth pattern. `support@gigaton.ai` Workspace group with collaborative inbox; outbound via gmail-support-relay SA with domain-wide delegation. WhatsApp + SMS still via Twilio (no Google equivalent). Source: user 2026-05-26 ~00:00 UTC override of SendGrid recommendation
- **WhatsApp:** Meta Business verification for `gigaton-ai` entity initiated this week (3-7 day Meta review). Per-DBA + per-affiliate WhatsApp Senders provisioned on-demand. Source: user 2026-05-25 EOD
- **DNS:** User confirmed admin access at gigaton.ai's DNS provider. Auto-subdomain flow `<slug>.gigaton.ai` viable for entity creation. Source: user 2026-05-25 EOD

## Still OPEN (low-priority follow-ups, Week 1-2)

- 5 omnichannel support sub-decisions (see design doc §10)
- Paralegal engagement for v0 legal scaffold review (~$8-24K, 2-3 weeks elapsed)
- 7f46371b SA key revoke investigation (deferred Week 2+ per SEC-1.1)
- Multipli Phase B-E engine code (per LAUNCH-1 sequencing: Week 2 onwards)

### From migration Day 0
- **MIG-2** — `gigaton-engine-pg` canonical: new gigaton-platform instance, abandon carmen-beach? (recommended yes)
- **MIG-3** — phantom `gigaton-silo-index` GCS bucket — was the bucket name a typo, or lazy-created at runtime, or genuinely never existed?
- **MIG-4** — sales-OS DATABASE_PATH=/data/sales_os.db — ephemeral or hidden volume mount?

### From beta openness
- **BETA-1 RESOLVED** — Support is OMNICHANNEL (not single channel): customers can request via email, chat, SMS, WhatsApp; platform users (team + operators) respond via any. **SMS + WhatsApp are REQUIREMENTS, not v1.1.** Slack integration for team-side triage; platform-integrated chat for operator dashboard. Design doc at `docs/architecture/2026_05_25_omnichannel_support_design.md` (in flight). Source: user message 2026-05-25 evening

### From SA key cleanup
- **SEC-3** — 7f46371b key cannot be revoked (FAILED_PRECONDITION). Investigate binding before next attempt.

---

## Architecture lock 2026-05-26 ~01:30 UTC

### ARCH-2 — Three access layers locked 2026-05-26 ~02:00 UTC

- **L1 — Customer/public surface** (anonymous + customer-tier auth): per-entity domain. Carmen Beach Properties customer surface = `playadelcarmen.homes` (the PDC-branded platform). Future tenants: their own customer-facing surfaces (Ti DBA subdomains, future entity domains, etc.). All consume gigaton-platform engines via gateway.
- **L2 — Operator/founder/affiliate portal** (Gignet platform user tier): `https://gigaton-platform.web.app/#/founder`. Where each entity OWNER manages their entity (leads, billing, integrations, Stripe Connect setup, etc.). One operator portal, multi-tenant via UAE namespace.
- **L3 — Backend engines** (gigaton-platform brain): stays in current GCP projects (gigaton-platform + carmen-beach-properties). The carmen-beach-properties hosted engines are NOT migrating per MIG-CANCEL — they remain for billing + licensing + security segmentation purposes.
- **CBP `apps/web`** = the playadelcarmen.homes platform (L1). Calls gigaton-platform engines for ALL business logic; local Prisma DB used for tenant-vertical-specific catalog (property listings, owner messaging metadata, etc.) where appropriate.
- Source: user 2026-05-26 ~02:00 UTC

### ARCH-1 — Gigaton platform = the BRAIN; all entities are tenant FEs
- **Locked direction:** "focusing on gigaton logic + platform etc to complete the rest for all carmenbeach properties & clients, etc"
- Gigaton platform engines (gateway + 10 backend services) hold ALL business logic: leads, decisions, identity, intel, billing, comms (SMS/WhatsApp), Stripe, connectors, audit
- Every entity (Carmen Beach, Ti DBAs, future operators, Gignet affiliates) is a TENANT FE that calls gigaton-platform engines via the gateway. They do NOT deploy parallel backend services.
- Tenant FEs may have their own UI codebase (e.g. Carmen-Beach-Properties `apps/web`) but ZERO business logic beyond render + form submit + redirect
- **Implications for consolidation:** any operator-local backend services that duplicate gigaton-platform engines are SUNSET candidates — DO NOT DEPLOY:
  - CBP local `services/connector-api` → use gigaton-platform `connector-api` instead
  - CBP local `services/mimi` → use gigaton-platform `mimi-whatsapp`
  - CBP `packages/leads/scorer.ts` → use gigaton-platform `decision-engine`
  - Any future operator-local Stripe / OAuth / scoring → use gigaton-platform equivalents
- **Wiring pattern for ALL tenant FEs:**
  - Auth: redirect to `https://gigaton-platform.web.app/#/login`, get JWT
  - All data + actions: call `https://gigaton-platform.web.app/v1/operators/{tenant_id}/*` with X-Client-Namespace + JWT
- Source: user 2026-05-26 ~01:30 UTC

## Late-evening additions 2026-05-26 ~00:30 UTC

### EMAIL-1 — Gmail+Workspace LOCKED INDEFINITELY for all email
- ALL email (support / marketing / transactional / platform) uses Gmail API + Google Workspace
- No SendGrid, no Postmark, no other vendors — even at scale
- Rationale: Google-stack alignment + native Pub/Sub inbound + existing intel-silo OAuth pattern + Workspace SPF/DKIM/DMARC already managed
- Source: user 2026-05-26 ~00:30 UTC explicit lock

### OPS-1 — Setup ownership: Todd does ALL v1 setup himself
- No delegation to bella / matt / external for the v1 Tier 1 + Tier 2 actions
- Re-evaluate post-beta when team has operational handoff candidates
- Source: user 2026-05-26 ~00:30 UTC

### MIG-CANCEL — Migration cutover NOT EXECUTED (2026-05-26 ~01:00 UTC)
- User direction: "assume we don't do migrations if things are working"
- Status check: 11/11 engines healthy, gateway aggregate_status ok, Wave 1 fully deployed clean — things ARE working
- Migration parallel deploys in gigaton-platform STAY as warm-standby / DR posture (~$50/mo total Cloud SQL + Cloud Run idle)
- Cutover scripts shelved; LAUNCH-1 consolidated-deploy framing dissolved — beta can open as soon as Tier 1 setup + Wave 2 ship
- Saves ~5h operator-attended cutover work + 7-day soak window
- Re-evaluate if any engine degrades; warm standby allows fast cutover-by-script if needed

### DNS-1 — DNS scope NARROWED to playadelcarmen.homes only
- User direction: "do not do anything with dns other than on playadelcarmen.homes"
- Ti DBA subdomain plan under ti.gigaton.ai is DEFERRED (not canceled — re-evaluate Week 2+)
- Maximum-activation pattern locked for playadelcarmen.homes: apex + www + 5 subdomains (tour/chat/shop/book/api) + Workspace MX + SPF + DMARC
- All subdomains route to gigaton-platform.web.app; Firebase site rewrites split product surfaces
- Source: user 2026-05-26 ~01:00 UTC

### SUPPORT-3 — Reply default channel: RICHEST-AVAILABLE
- Auto-reply prefers email > WhatsApp > SMS regardless of inbound channel
- Better fidelity for complex responses; accepts surprise risk for SMS-originated customers
- Overrides earlier "channel-preserving" recommendation in omnichannel design doc
- Source: user 2026-05-26 ~01:00 UTC

### SUPPORT-4 — AI pre-drafted-reply UX: SEPARATE BOT MESSAGE WITH "USE THIS DRAFT" BUTTON
- Inbound message lands in Slack thread → bridge bot follows up with LLM-drafted reply + "Use this draft" insert button
- Operator can edit before sending; AI assistance is opt-in via button click
- Source: user 2026-05-26 ~01:00 UTC

### SUPPORT-5 — Thread resolution: AUTO-INFER + EXPLICIT /resolve
- Auto-mark resolved on "thanks!" / "got it" / 7-day silence
- Operator can also `/resolve` explicitly via slash command
- Source: user 2026-05-26 ~01:00 UTC

### INBOX-1 through INBOX-5 — Platform Inbox sub-decisions (auto-defaults locked)
- **INBOX-1:** Gmail OAuth client = single platform-wide (recommended; one client manages all entities)
- **INBOX-2:** Multi-mailbox = auto-watch all (operator filters in UI)
- **INBOX-3:** Initial sync depth = 30 days at connect + on-demand deeper-sync up to 365 days
- **INBOX-4:** Send pattern = send-on-behalf via tenant OAuth (vs delegated send-as)
- **INBOX-5:** KMS keys = per-entity (reuses 2026-05-22 keyring, ~$1/mo/entity for at-rest encryption)
- Source: agent recommendations + user "as much deployed/functional/generating value as possible" direction

### FEAT-1 — Platform Inbox feature (per-entity Gmail surfaced in Gigaton UI)
- **Requirement:** after an entity owner / Gignet affiliate connects their domain to their Gignet organization (entity-creation flow Step 3-4), Gigaton platform UI displays + lets them READ + RESPOND to all email for that entity's mailbox(es) — without leaving the platform
- **Architecture pieces:** per-entity Gmail OAuth tokens (same secret pattern as existing carmen-beach `oauth-gmail-*` secrets); operator dashboard surface in gigaton-ui-system displays threads/labels/search/reply; replies sent via Gmail API; threading unified with SMS/WhatsApp/chat via persona-engine identity matching
- **Extends:** `[[entity_creation_flow_n_wide]]` Step 9 (default connector wiring) + `[[omnichannel_support_design]]` (from support@ inbox triage to full per-entity inbox UI)
- **Build sequence:** Week 1 — design refinement in both feeder docs; Week 2-3 — implementation alongside Slack bridge + Pub/Sub watch wiring
- Source: user 2026-05-26 ~00:30 UTC

## Decision-velocity stats
- 21 decisions ratified in single session (the EOD 5/25 sprint)
- 6 decisions still open (most are low-impact follow-ups + 1 P0 feature spec)
- ALL user-facing blockers either resolved or in progress (GHA billing ✅, gcloud reauth ✅, GCP budgets ✅, OAuth URIs ✅ verified HTTP 302, Slack ✅; remaining: Gmail Workspace setup + WhatsApp Meta + DNS CNAMEs)

## Cross-references
- `[[product_service_package_gigaton_ti_solutions]]`
- `[[multipli_vendor_growth_engine_sprint_2026_05_22]]`
- `[[gcp_engine_migration_accelerated_2026_05_25]]`
- `docs/architecture/2026_05_25_interactive_experience_builder_architecture.md`
- `docs/architecture/2026_05_25_30_day_gigaton_company_launch_roadmap.md`
- `docs/architecture/2026_05_25_entity_creation_flow_n_wide.md`
- `runbooks/2026_05_25_carmen_to_gigaton_migration_day_by_day.md`
- `runbooks/2026_05_25_eod_tonight_action_pack.md`
- `runbooks/2026_05_26_to_2026_06_01_deploy_freeze_operating_playbook.md` (now superseded by LAUNCH-1)
- `runbooks/2026_05_25_multipli_bundle_manual_production_recipe.md`
- `legal/v0_drafts/` (templates pending agent completion)
