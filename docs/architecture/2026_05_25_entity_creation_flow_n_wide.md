# Entity Creation Flow — N-Wide

**Date.** 2026-05-25
**Author.** Claude (design only — no code, no branches).
**Status.** DRAFT — design freeze target end of Week 1 (2026-06-01).
**Doctrine anchors.** [[foundational_goal_gigaton_engineered_brand_experience]] (PPIM) · [[foundational_modular_replication_via_input_substitution]] · [[universal_connector_hub_architecture]] · [[gignet_auto_trigger_orchestration]] · [[onboarding_workflow_v1_completion_verified_2026_05_22]] · [[product_service_package_gigaton_ti_solutions]].
**Related.**
- `master-knowledge-base/docs/architecture/2026_05_25_30_day_gigaton_company_launch_roadmap.md` (current 3-entity launch order)
- `master-knowledge-base/docs/architecture/2026_05_25_interactive_experience_builder_architecture.md` (assumes operator already exists)
- `master-knowledge-base/manifests/onboarding_v1.yaml` (10-stage canonical chat-first manifest)
- `master-knowledge-base/legal/v0_drafts/templates/` (legal-template workstream)

---

## 1. Goal & Non-Goals

### Goal
Support **N entity creations** as a first-class platform capability. Any qualified human (typically a Gignet affiliate, but also direct sign-ups, internal founder-led entities, and Ti Solutions managed customers) can:

1. Land in the wizard
2. Provide the minimum required inputs — domain + business-class email
3. Pick one of 7+ supported entity types
4. Have the platform auto-provision: UAE namespace, Stripe Customer, ToS/Privacy/AUP/DPA, PPIM signature anchor, brand_dimensions row, default connectors per type, default Penrose/KPI panels, default Gignet trigger-map subset, and a live landing page
5. Send/receive their first interaction within the entity-type-appropriate channel

The flow is the same engine across all entity types per **modular replication via input substitution** — only `operator_context` and the entity_type template differ. Adding a new entity_type = adding a YAML row + landing template, never editing the engine.

### Non-Goals (v1, 30-day window)
- Multi-human complex orgs with conflicting role matrices — v1 supports `creator_human = primary_admin` with optional `additional_admins` array; no RBAC trees, no compliance-officer separation-of-duties.
- EU-domiciled entities — GDPR DPA template not yet reviewed by counsel; flag-and-defer. v1 supports US + MX + global-non-EU.
- Custom legal review per entity — every entity instantiates from the templates as-is; bespoke clauses queue to v1.1.
- Stripe Connect splits (sub-accounts per entity) — single platform Stripe account per locked decision B1; entities are Stripe Customer records.
- Public marketplace where any human can spin up an entity unattended — v1 requires an affiliate code OR explicit Founder/Owner approval to create.

---

## 2. The 10-Step Entity-Creation Wizard

**Surface.** Chat-first by default (reuses `ChatOnboardingOrchestrator`), with a parallel form-first fallback at `/onboarding/entity-create` for users who explicitly prefer it (linked from chat as "switch to form view"). Both surfaces emit the same `Stage-N` events to HME.

**Blocking vs background.** Steps 1–5 are blocking (cannot proceed to next step without success). Steps 6–10 are best-effort background — the wizard can complete (entity reaches `status: provisioned`) with any of 6–10 in `pending`/`retry_scheduled` state, and the operator gets a live entity that finishes provisioning asynchronously.

| Step | Name | Blocking? | Inputs | Output artifact | Engine | Event emitted |
|---|---|---|---|---|---|---|
| 1 | Claim affiliate code / sign up | **B** | `affiliate_code` OR `direct_signup_consent` + Google OAuth identity | `human_id`, `affiliate_id` (or `null`), HumanPersona snapshot | persona-engine | `HumanIdentityClaimed` |
| 2 | Name entity + pick type | **B** | `entity_name`, `entity_type ∈ {7+ types}`, `legal_form` (LLC/DBA/SoleProp/Other), `country`, `state_or_region` | Draft `entity_id` (UUID, status `draft`) + provisional `operator_context` skeleton | UAE | `EntityDraftCreated` |
| 3 | Domain — BYO or auto-provision | **B** | `domain_mode ∈ {byo, gigaton_subdomain}`, `domain` (e.g. `carmenbeach.com` or `acme-mgmt`), optional DNS provider hint | Domain claimed in `entity_domains` table; verification token issued (DNS TXT for BYO, auto-verified for subdomain) | UAE + new domain-service module in UAE | `EntityDomainClaimed` |
| 4 | Business-class email — verify ownership | **B** | `business_email` (must be `<local>@<domain>` from step 3), inbox forward target | Email verified; magic-link confirmed clicked from the actual mailbox at the actual domain | UAE | `EntityBusinessEmailVerified` |
| 5 | ToS / Privacy / AUP / DPA acceptance | **B** | Affiliate clicks-through 4 template-instantiated docs; templated with entity name + domain + jurisdiction | 4 `legal_acceptance_record` rows (one per doc) with hash of accepted text + timestamp + IP | UAE (`/v1/entities/{id}/legal/accept`) | `EntityLegalAccepted` |
| 6 | Stripe Customer record creation | bg | entity_name, business_email, country | `stripe_customer_id` written to `entity_billing` table; default tax behavior per B5 | gigaton-engine (`billing/` module per B3) | `EntityStripeCustomerProvisioned` |
| 7 | UAE namespace registration | bg | entity_id, operator_context (tags from steps 2–4) | Row in `client_namespaces` with admin-token-gated CRUD; capabilities seeded per entity_type | UAE | `EntityNamespaceRegistered` |
| 8 | PPIM signature anchor + brand_dimensions row | bg | entity_id, entity_type, initial brand voice hints from step 2 | `ppim_signature` JSONB on entity; 5 seed `brand_dimensions` rows (responsiveness / quality / personalization / resolution / upgrade) tagged with entity_id | intel-silo (brand_dimensions catalog) + decision-engine (Penrose binding) | `EntityPpimAnchored` |
| 9 | Connector wiring — entity-type defaults | bg | entity_type template's `default_connectors` list | Per-connector OAuth-start links queued; for connectors with no OAuth (iCal, API key), `register-provider-credentials` action presented in chat | connector-api | `EntityConnectorDefaultsQueued` |
| 10 | First interaction (type-specific) | bg | entity_type template's `first_interaction` recipe | For tour-operator: WhatsApp business profile created + greeting message ready. For property-mgmt: landing page live + first guest inquiry form. For SaaS: signup link issued. Etc. | gigaton-ui-system (landing) + mimi-whatsapp (chat) + connector-api (varies) | `EntityFirstInteractionReady` |

**Event chain triggers** (per [[gignet_auto_trigger_orchestration]] trigger map):
- `EntityLegalAccepted` → fires steps 6+7+8 in parallel
- `EntityNamespaceRegistered` AND `EntityStripeCustomerProvisioned` → fires step 9
- `EntityConnectorDefaultsQueued` → fires step 10
- `EntityFirstInteractionReady` → flips entity `status: provisioned → status: live`

If any background step fails after 3 retries, `EntityProvisioningStalled` is emitted with a human-readable reason; the operator sees a banner in chat with the remediation action.

---

## 3. The 7+ Entity-Type Templates

Stored as `entity_types.yaml` (the file the parallel legal-agent workstream is generating at `master-knowledge-base/legal/v0_drafts/templates/entity_types.yaml`). Each row carries the full template; the wizard reads from this catalog, never hard-codes. New entity types = new YAML row + new landing template, zero engine changes.

| # | entity_type slug | Default landing template | Default connectors (queued in step 9) | Required Stripe products | Default Penrose / KPI panels | Default Gignet trigger-map subset |
|---|---|---|---|---|---|---|
| 1 | `saas_platform` | `/templates/landing/saas_self_serve.tsx` (hero + 3-tier pricing + signup) | OAuth: Google Workspace, Stripe (already platform), GA4; API key: OpenAI/Anthropic; Webhook: GitHub | starter+operator+scale subscription tiers + per-bundle overage SKU | MRR, trial-to-paid, signup-to-first-bundle, bundles/day | `user.signup.completed` → `notify-founder`; `subscription.created` → `provision-tenant`; `bundle.generated` → `meter-overage` |
| 2 | `managed_service_agency` | `/templates/landing/agency_book_call.tsx` (hero + case study + Calendly) | Slack Connect, HubSpot (or Salesforce), Stripe Invoices, DocuSign, Calendly | setup_package one-time + retainer_starter/growth/scale + performance_per_unit metered | scoping calls/wk, proposals out/wk, avg deal cycle, signed MRR | `calendar.meeting.booked` → `route-to-cxguy`; `invoice.paid` → `kickoff-checklist` |
| 3 | `property_management` | `/templates/landing/property_directory.tsx` (property grid + WhatsApp inquiry) | Airbnb iCal, Vrbo iCal, Booking.com iCal, Stripe Checkout, Twilio/WhatsApp, Matterport, Google Calendar | per-property stay SKU (variable) + cleaning_fee + damage_deposit + owner_commission (metered 20% of net) | direct-channel revenue, occupancy rate, WhatsApp response time, owner NPS | `booking.received` → `whatsapp-confirm`; `inquiry.received` → `respond-<5min`; `month.close` → `owner-payout-prep` |
| 4 | `marketing_media_agency` | `/templates/landing/agency_portfolio.tsx` (hero + portfolio grid + book-call) | Meta Ads, Google Ads, TikTok Ads, GA4, HubSpot, Stripe Invoices, Slack Connect | retainer (monthly) + project-based one-time + media-spend pass-through (metered) | MQL/wk, attributable revenue, blended CPA, retainer renewal rate | `lead.captured` → `attribute-and-route`; `campaign.published` → `monitor-spend`; `month.close` → `client-report` |
| 5 | `unified_real_estate_operator` | `/templates/landing/real_estate_marketshare.tsx` (multi-property + agent + brand) | Same as property_management PLUS MLS adapter + CRM (HubSpot/Salesforce) + e-signature (DocuSign) + Stripe Invoices for agent commissions | listing-fee + closing-commission + agent-split-payout (Stripe Connect candidate v1.1) | market share %, listings/agent, days-on-market, closed-volume/mo | `listing.created` → `mls-sync`; `offer.received` → `route-to-agent`; `deal.closed` → `agent-payout` |
| 6 | `virtual_walking_tour_marketplace` | `/templates/landing/tour_marketplace.tsx` (interactive 5th Ave map + shop directory + chat) | WhatsApp, Instagram, Matterport, Stripe Checkout (shop transactions), Google Maps, Twilio voice | tour-booking + shop-transaction-fee (small %) + featured-listing (subscription) + voice-minutes (metered) | inquiries/shop/wk, tour completion rate, shop-conversion rate, avg basket size | `shop.message.received` → `voice-or-chat-route`; `tour.completed` → `nps-prompt`; `transaction.success` → `attribute-to-tour` |
| 7 | `solo_affiliate_operator` | `/templates/landing/solo_card.tsx` (single-page card + contact + 1 CTA) | Google Workspace, Stripe Checkout, optionally one channel (WhatsApp OR Instagram OR email) | per-deal one-time (variable) + optional retainer | revenue/mo, deals/mo, gross margin, response time | `deal.captured` → `affiliate-revenue-share-calc`; `payout.window.open` → `affiliate-paid` |
| 8+ | (future) | extensible | extensible | extensible | extensible | extensible |

**Per-template additional fields the wizard reads:**
- `legal_template_set` — pointer to ToS/Privacy/AUP/DPA template files used in step 5
- `required_compliance_signatures` — e.g. `property_management` needs Spanish-language lease addendum; `unified_real_estate_operator` needs broker-of-record attestation
- `default_brand_voice_seed` — initial 5 brand_dimensions seed values
- `default_ppim_signature` — initial `{interaction, economics, predictability, brand_dimension}` quadruple

---

## 4. Domain + Email Provisioning Options

### 4.1 Domain options

#### Option A — Bring-your-own (BYO)
1. Affiliate enters domain (e.g. `carmenbeach.com`).
2. UAE issues a verification token: `gigaton-domain-verify=<random-32>`.
3. Affiliate adds DNS TXT record at `_gigaton-verify.<domain>` containing the token. (DNS TXT preferred over file-upload because tour-operator + agency entity types may not have a writable web root yet.)
4. Background poller checks every 30s for 10 min; on hit, domain marked `verified`.
5. Once verified, affiliate optionally points apex/www CNAME at `gigaton-landing.app` (or A-record at the provided Cloud Run / Firebase Hosting IP) to activate the landing template.

#### Option B — Auto-provision Gigaton subdomain
1. Affiliate picks slug (e.g. `acme-mgmt`).
2. Slug validated against profanity + reserved list (`api`, `www`, `app`, `gigaton`, `admin`, `ti`, etc.).
3. `acme-mgmt.gigaton.ai` provisioned automatically (Cloud DNS record + Firebase Hosting / Cloud Run domain mapping).
4. Auto-verified — no DNS challenge needed (gigaton.ai is platform-owned).
5. Upgrade path: affiliate can later add a BYO domain that points at the same hosting target; both work in parallel until BYO is promoted to primary.

**Sub-domain free; BYO requires the affiliate already owns the apex.**

### 4.2 Business-email verification

Two flows depending on whether the affiliate has a working mailbox at the domain yet:

#### Flow 1 — Email magic-link (default)
1. Affiliate enters `legal@<domain>` (or another local-part of their choosing — `support@`, `hello@`, etc.).
2. UAE sends a one-time magic link to that mailbox via SendGrid (template: `entity_business_email_verify`).
3. Affiliate clicks the link; UAE marks email verified.

#### Flow 2 — Mail-forward bootstrap (for affiliates who don't have mail set up yet)
1. If the affiliate chose option B (auto-provision Gigaton subdomain), AND has no MX records on the subdomain, Gigaton offers to auto-provision `<local>@<slug>.gigaton.ai` forwarding to the affiliate's verified Google identity (from step 1).
2. Magic link delivered via forwarded mailbox — affiliate confirms.
3. Upgrade path: affiliate can later configure their own MX (e.g. Google Workspace) and Gigaton's forwarder is disabled per-domain.

**Anti-pattern:** allowing free-text `gmail.com`/`yahoo.com` business emails — the platform explicitly requires `<local>@<entity_domain>` to make the entity a real legal counterparty, not a hobby project. Caught at step 4 form validation.

---

## 5. Where This Lives in Existing Engines

No new modules. All endpoints are **additive** to existing services per the locked doctrine.

| Capability | Engine | Storage |
|---|---|---|
| Entity record + lifecycle state | **UAE** | New table `entities` (entity_id PK, status, entity_type, operator_context JSONB, created_by_human_id, created_at) — extends UAE's existing `client_namespaces` model |
| Namespace registration + capability catalog | **UAE** | Existing `client_namespaces` + `capabilities_catalog` tables |
| Domain ownership + email verification | **UAE** | New tables `entity_domains` + `entity_business_emails` + `domain_verification_tokens` |
| Legal acceptance audit | **UAE** | New table `legal_acceptance_records` (entity_id, doc_type, doc_hash, accepted_by_human_id, accepted_at, ip, user_agent) |
| Stripe Customer + product catalog binding | **gigaton-engine** (per locked decision B3) | Extends `gigaton-engine/billing/` module shipping in 30-day-roadmap Week 1 |
| brand_dimensions catalog + PPIM signature | **intel-silo** | Existing `brand_dimensions` table extended with `entity_id` FK |
| Connector defaults + OAuth start | **connector-api** | Existing `user_connections` table (per [[universal_connector_hub_architecture]]) extended with `entity_id` FK |
| Event log (every wizard step emits) | **HME** | Existing `events` table — 10 new event types prefixed `Entity*` |
| Human ↔ affiliate ↔ entity graph | **persona-engine** | New table `human_entity_relations` (human_id, entity_id, role ∈ {creator, admin, affiliate_revenue_share, viewer}, created_at, terminated_at) |
| Landing-page templates | **gigaton-ui-system** | New `/templates/landing/<entity_type>.tsx` files; rendered server-side via Firebase Hosting with entity-specific data substitution |
| First-interaction recipes | varies per entity_type | mimi-whatsapp (chat-first types), connector-api (signup-first types), gigaton-ui-system (landing-first types) |
| Default Penrose / KPI panels | **decision-engine** | Existing Penrose scoreboard; per-entity_type panel preset stored in `decision-engine/config/penrose_presets_per_entity_type.yaml` |
| Gignet trigger-map per entity_type | **gigaton-gateway** | Existing `orchestrator_triggers` Postgres table — seed rows tagged with entity_type |

---

## 6. Net-New Endpoints Required (Additive Only)

**12 net-new endpoints, all additive.** Engine assignments:

| # | Method + Path | Engine | Purpose |
|---|---|---|---|
| 1 | `POST /v1/entities` | UAE | Atomic entity creation; emits `EntityDraftCreated`; returns `entity_id` |
| 2 | `GET /v1/entities/{id}` | UAE | Read entity state + provisioning step statuses |
| 3 | `POST /v1/entities/{id}/domain` | UAE | Claim a domain (BYO or auto-provision-subdomain); issues verification token |
| 4 | `POST /v1/entities/{id}/domain/verify` | UAE | Poll-trigger or webhook-receive for domain verification |
| 5 | `POST /v1/entities/{id}/email/verify` | UAE | Send magic-link to business email |
| 6 | `POST /v1/entities/{id}/email/confirm` | UAE | Confirm magic-link click |
| 7 | `POST /v1/entities/{id}/legal/accept` | UAE | Capture ToS / Privacy / AUP / DPA acceptance (4 records in one call) |
| 8 | `POST /v1/entities/{id}/stripe-customer` | gigaton-engine | Create Stripe Customer record; bind to entity |
| 9 | `POST /v1/entities/{id}/namespace` | UAE | Register `client_namespaces` row + seed capabilities |
| 10 | `POST /v1/entities/{id}/ppim-anchor` | intel-silo | Seed brand_dimensions rows + write PPIM signature |
| 11 | `POST /v1/entities/{id}/connectors/default-wire` | connector-api | Queue per-entity_type default connectors (OAuth-start links or paste-credential prompts) |
| 12 | `POST /v1/entities/{id}/first-interaction` | gigaton-gateway (orchestrator) | Trigger entity-type-specific first-interaction recipe; flips entity `live` |

**Plus 1 read-only aggregator on the gateway** so the chat UI can poll a single endpoint:
- `GET /v1/entities/{id}/provisioning-state` (gigaton-gateway) — aggregates step status from all engines + returns `next_action_for_chat`.

**Manifest extension:** the existing `master-knowledge-base/manifests/onboarding_v1.yaml` (currently 10 stages for operator onboarding) gets a sibling `entity_creation_v1.yaml` (10 stages) — same shape, different stage definitions. Gateway resolver routes `entity_creation_v1` intents the same way it routes onboarding intents.

---

## 7. Affiliate ↔ Entity Relationship Model

### Cardinality
- **One affiliate → N entities.** Hard cap: 5 entities in v1. Soft warning at 3 ("You've created 3 entities — most affiliates focus on 1-2; want to talk to support before adding a 4th?"). The cap exists to prevent farmed sock-puppet entities from gaming the affiliate revenue share.
- **One entity → ≥1 humans.** The creator is `role: creator + admin` by default. Additional admins can be invited later (out of v1 wizard scope — separate `/v1/entities/{id}/invitations` endpoint, v1.1).
- **One entity → 0 or 1 affiliate.** If the creator entered via affiliate code, that affiliate gets the persistent revenue share. If the creator signed up direct (no code), `affiliate_id = null` and 100% margin stays with the platform.

### Revenue share
- Per [[master_project_plan]] Chapter 11 Gignet affiliate-network platform (18 pages × 25 certs × 5 tiers × 8 products × 4 phases): affiliate revenue share is computed per entity per billing cycle based on tier + cert + product matrix.
- Stored in `human_entity_relations.metadata.revenue_share_pct` (snapshot at creation; can be renegotiated via separate Owner-approved flow).

### Persistence + termination cascades
- **Affiliate persists across entities** — if the human creates entity A then entity B, both reference the same `affiliate_id`.
- **Affiliate termination** (e.g. ToS violation, voluntary exit) → all entities they created enter `status: orphan_review`. Owner manually decides: (a) transfer to another affiliate, (b) absorb to platform direct, (c) retire entity + cascade-delete operator data per DPA right-to-delete clause.
- **Entity termination** (affiliate retires one specific entity) → entity moves to `status: archived`; data retained per DPA retention clause (default 90 days, configurable per jurisdiction); Stripe Customer set to `delinquent: false + email_to_invoice = null` so no further billing fires.

---

## 8. Build Sequence — 30-Day Arc

### Week 1 (2026-05-26 → 2026-06-01) — Design freeze, no production deploys

| Item | Owner | DoD |
|---|---|---|
| `entity_types.yaml` v0 with all 7 types | Legal-agent workstream + Founder | YAML committed at `master-knowledge-base/legal/v0_drafts/templates/entity_types.yaml`; reviewed by Founder |
| Wizard wireframes (chat-first + form-first) | UI designer + Claude | Figma or markdown wireframe for each of the 10 steps; chat copy drafted |
| Stripe product matrix per entity_type | Founder + Gigaton agent | All 30+ Stripe products (across 7 entity types) listed with price IDs in `gigaton-engine/config/stripe_test_catalog.yaml` |
| Manifest `entity_creation_v1.yaml` | Gigaton agent | Stage definitions + state-transition map committed to `master-knowledge-base/manifests/` |
| Legal templates ToS / Privacy / AUP / DPA v0 (variable-substitution-ready) | Legal-agent workstream + paralegal | Templates with `{{entity_name}}`, `{{domain}}`, `{{jurisdiction}}` placeholders; reviewed |
| Landing-page template wireframes per entity_type | UI designer | 7 Figma frames; demo copy drafted |
| `entities` + `entity_domains` + `legal_acceptance_records` schema | DB-design agent | Migrations drafted (not yet applied); reviewed against existing UAE schema for FK consistency |

### Week 2 (2026-06-02 → 2026-06-08) — Backend endpoints + first BYO domain dry-run

| Item | Owner | DoD |
|---|---|---|
| UAE endpoints 1–7 implemented + tested in staging | UAE agent | All 7 endpoints respond per spec; unit + integration tests pass |
| gigaton-engine endpoint 8 (Stripe Customer create) | gigaton-engine agent | Endpoint creates a real Stripe test-mode Customer; webhook round-trip verified |
| Domain DNS-TXT verification poller wired | UAE agent | Background poller checks every 30s; verifies real-world domain in <2min |
| Email magic-link via SendGrid wired | UAE agent | Real magic-link arrives in mailbox; clicking confirms |
| End-to-end dry-run for `carmen_beach_properties` (recreate as entity #1 via wizard) | Founder + Gigaton agent | Carmen Beach completes wizard via real flow — domain verified, email verified, 4 legal docs accepted, Stripe Customer created — no manual intervention |

### Week 3 (2026-06-09 → 2026-06-15) — Connector defaults + landing pages + first 5 affiliate-created entities

| Item | Owner | DoD |
|---|---|---|
| connector-api endpoint 11 (default-wire) per entity_type | connector-api agent | For each of the 7 entity types, calling the endpoint queues the correct connectors |
| Landing-page templates rendered server-side per entity_type | UI agent | All 7 templates render with entity-specific substitution; live on `<slug>.gigaton.ai` for subdomain entities |
| gateway endpoint 12 + provisioning-state aggregator | Gateway agent | Chat UI polls one endpoint and gets the full step-status view |
| persona-engine `human_entity_relations` table + relationship endpoints | persona-engine agent | Human ↔ affiliate ↔ entity graph readable + writable |
| First 5 affiliate-created entities go live | Founder + early affiliates | 5 real entities created end-to-end by 5 different humans (or simulated affiliates); KPI dashboard reflects 5 `EntityFirstInteractionReady` events |

### Week 4 (2026-06-16 → 2026-06-22) — Gignet auto-trigger + scale to 25+

| Item | Owner | DoD |
|---|---|---|
| Gignet trigger map wired per entity_type | Gateway agent | All 7 entity types have per-type `orchestrator_triggers` seeded; auto-trigger fires verified end-to-end |
| Affiliate revenue-share calc bound to Stripe webhook | gigaton-engine agent | Subscription/invoice events fire revenue-share computation; share-row written |
| Landing-page A/B framework hooked into gigaton-ui-system | UI agent | Per-entity_type landing template supports variant A/B via the existing Penrose `decision_velocity` substrate |
| 25+ entities live | Affiliate + Founder | 25 entities reach `status: live` across at least 3 entity types; cohort report published |
| Retro + v1.1 backlog | Founder + Owner | Retro doc at `master-knowledge-base/retros/2026_06_22_entity_creation_v1_retro.md`; v1.1 features (multi-admin, Stripe Connect, EU/GDPR, custom legal clauses) prioritized |

---

## 9. Open Decisions for User (max 6)

1. **Subdomain auto-provision: free for all entity_types, or only for `solo_affiliate_operator` and `saas_platform`?** Recommendation: free for all (lowers friction; subdomain costs Gigaton ~$0). Alternative: gate behind tier or behind paid Starter to disincentivize sock-puppets.
2. **Max entities per affiliate in v1: hard cap at 5, or soft-cap at 3 with manual review above?** Recommendation: hard cap 5 + soft warning at 3. Founder/Owner can manually raise on appeal.
3. **Domain ownership verification mechanism: DNS TXT (default), email-link-to-WHOIS-listed-contact, or file-upload to web root?** Recommendation: DNS TXT only in v1. Email-to-WHOIS and file-upload add brittleness (WHOIS privacy, no web root yet) for marginal UX gain.
4. **`marketing_media_agency` and `unified_real_estate_operator` — keep both as distinct entity types, or collapse `unified_real_estate_operator` into a tagged `property_management` variant?** Recommendation: keep distinct (very different KPI panel + connector default sets — MLS + agent-commission economics are non-trivial to express as tags on `property_management`).
5. **Direct sign-up (no affiliate code) allowed in v1, or affiliate-gated only?** Recommendation: affiliate-gated only in v1 to enforce attribution; allow direct sign-up in v1.1 after the attribution + revenue-share substrate is stable. Founder/Owner can bypass for the 3 internal entities (Gigaton AI, Ti Solutions, Carmen Beach Properties).
6. **Stripe Customer per entity or per affiliate-human?** B1 locks single platform Stripe account; this is about Customer-record granularity *within* that account. Recommendation: per-entity (one Stripe Customer per entity) so revenue-recognition + Tax + invoicing all flow cleanly per-entity. The affiliate-human is tracked separately in persona-engine + revenue-share table; never represented as a Stripe Customer.

---

## 10. Anti-Patterns

- **No domain or no business email = no entity.** Hard block at step 3/4. The user's stated minimum is non-negotiable.
- **Free-email-provider business email** (`gmail.com`, `yahoo.com`, etc.) — rejected at step 4. Entity must own its identity at its own domain.
- **Hardcoding entity_type behavior inside engine code** — every entity_type must come from `entity_types.yaml`. New type = new YAML row, never new code branch.
- **Cross-entity data leak.** Every query in every engine MUST filter by `operator_context.entity_id`. No global queries that span entities without explicit Founder/admin-token authorization.
- **EU-domiciled entities in v1.** GDPR DPA not yet counsel-reviewed; flag at step 2 (jurisdiction selection) and route to a waitlist instead of completing the wizard.
- **Malformed templated legal docs.** Every template render must pass a structural validator (`{{placeholders}}` resolved, no `null` substitutions, no truncated paragraphs). Step 5 blocks on validator pass.
- **Allowing wizard completion with `EntityProvisioningStalled` unacknowledged.** Background failure must surface to chat with a remediation banner; do not mark `status: live` until at least step 10 completes cleanly.
- **Multiple humans claiming "creator" role on the same entity.** Creator = creator (one human). Additional humans can be `admin` but not `creator`. Re-assignment of creator role (e.g. founder departure) requires Owner approval + audit.
- **Affiliate revenue share applied to entities the affiliate didn't create.** Hard-bound to the `affiliate_id` at creation time and never mutable.
- **Free-text entity_name without uniqueness check.** Entity_name + jurisdiction must be unique within the platform to prevent impersonation. Domain uniqueness is the primary constraint; entity_name is the human-readable secondary.

---

## 11. Cross-Reference Summary

- This flow extends the existing 10-stage operator onboarding ([[onboarding_workflow_v1_completion_verified_2026_05_22]]) but is a SIBLING workflow, not a fork — operator onboarding assumes an entity already exists. Entity creation creates the entity; then operator onboarding (which is itself entity-scoped) runs inside it.
- All entity-creation events flow into the existing Gignet auto-trigger fabric ([[gignet_auto_trigger_orchestration]]); the 10 trigger-map rows for entity creation get added to `orchestrator_triggers`.
- The Interactive Experience Builder bundle ([[2026_05_25_interactive_experience_builder_architecture.md]]) becomes the default first-interaction recipe for `saas_platform`, `managed_service_agency`, `marketing_media_agency`, and `solo_affiliate_operator` entity types — operator describes their brand in chat, bundle is generated, becomes the live landing demo.
- The 30-day launch roadmap ([[2026_05_25_30_day_gigaton_company_launch_roadmap.md]]) currently bootstraps 3 entities manually (Gigaton AI, Ti Solutions, Carmen Beach Properties) — those 3 are the dogfood test of this flow in Week 2; affiliate-driven N-wide creation lights up Weeks 3–4.
