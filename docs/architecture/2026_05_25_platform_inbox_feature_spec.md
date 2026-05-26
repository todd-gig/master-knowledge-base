# Platform Inbox Feature — Design Spec

**Date.** 2026-05-25
**Author.** Claude (design only — no code, no branches).
**Status.** DRAFT — design freeze target end of Week 1 (2026-06-01).
**Doctrine anchors.** [[foundational_goal_gigaton_engineered_brand_experience]] (PPIM) · [[foundational_modular_replication_via_input_substitution]] · [[universal_connector_hub_architecture]] · [[gignet_auto_trigger_orchestration]] · [[product_service_package_gigaton_ti_solutions]].
**Locked decisions:** **EMAIL-1** (Gmail+Workspace LOCKED INDEFINITELY for all email) · **FEAT-1** (Platform Inbox feature per-entity Gmail surfaced in Gigaton UI).
**Related design docs.**
- `master-knowledge-base/docs/architecture/2026_05_25_entity_creation_flow_n_wide.md` — Step 9 wires default connectors (this spec adds Gmail/Workspace as default in that step)
- `master-knowledge-base/docs/architecture/2026_05_25_omnichannel_support_design.md` — locked Gmail-only inbound + 4-channel routing (this spec generalizes from `support@` triage to full per-entity inbox UI)
- `master-knowledge-base/decisions/2026-05-25_architecture_decisions_log.md` — §EMAIL-1, §FEAT-1
- `[[api_reference_2026_05_19]]` — existing UAE / HME / persona-engine / intel-silo / connector-api endpoint surfaces

---

## 1. Goal & Non-Goals

### Goal
Once an entity owner / Gignet affiliate completes entity-creation Step 3 (domain) + Step 4 (business email) + Step 9 (connector wiring → Google Workspace OAuth), the **Gigaton platform UI displays + lets them READ and RESPOND to all email for that entity's mailbox(es) without leaving the platform**. Multi-mailbox per entity supported (e.g. `support@`, `bookings@`, `hello@` all on the same Workspace tenant).

The same engine surface serves Gigaton-direct (`support@gigaton.ai`), Carmen Beach booking inquiries (`bookings@carmenbeach.com`), Ti Solutions client comms (`client-relations@tisolutions.com`), and virtual-tour shop-owner chats — all via `operator_context` substitution. Adding a new entity's inbox = a new `gmail-oauth-{entity_id}` secret + a `connectors_catalog` row reference, never an engine change.

### Non-Goals (v1)
- **Full mail-client replacement.** No filters/rules editor, no signatures editor (use Workspace), no contact-management surface, no advanced compose (mail-merge, CC/BCC suggestions, send-later UI). Platform Inbox is a focused triage + reply surface — power users still keep Gmail.
- **Calendar integration v1.** No event creation from email, no meeting suggestion. Calendar API is a separate locked workstream.
- **IMAP / Exchange / Outlook fallback.** Per EMAIL-1, Gmail+Workspace only. Operators on non-Workspace mail are not eligible for the Platform Inbox until they migrate (covered in entity-creation Step 9 OAuth flow — if no Workspace, surface a friendly "Workspace required" callout).
- **Auto-reply / AI auto-send.** Every outbound v1 is human-authored (LLM may pre-draft via decision-engine `/v1/proposals`, identical pattern to omnichannel support — defer auto-send to Decision Execution Engine v1.1).
- **Per-user inbox-within-inbox.** v1 surfaces the entity's mailboxes; each operator-of-operator sees the entity inboxes their UAE capability set permits. No per-individual Gmail OAuth.
- **Send-as / aliases beyond Workspace native.** Whatever Workspace's Send-As config supports works; we don't add a platform-side alias layer.
- **Retention / archival policy enforcement.** Workspace owns retention (Vault / TTLs). Platform Inbox is a read+reply surface, not a system of record for compliance retention.

---

## 2. User Journeys

### Journey A — Affiliate connects Workspace during entity creation → first inbox load
1. Affiliate completes entity-creation Steps 1-8 (per `entity_creation_flow_n_wide`). On Step 9 the wizard offers the entity-type's default connectors; **Google Workspace is in the `default_connectors` list for every entity_type that has email as a channel** (which is every entity_type in v1 — saas_platform, managed_service_agency, property_management, marketing_media_agency, unified_real_estate_operator, virtual_walking_tour_marketplace, solo_affiliate_operator).
2. UI presents a "Connect Google Workspace" card with the entity's verified domain pre-filled. Affiliate clicks → OAuth consent screen for `gmail.readonly` + `gmail.send` + `gmail.modify` scopes against the workspace tenant.
3. On consent return, UAE persists refresh token to `gmail-oauth-{entity_id}` in Secret Manager (same shape as existing carmen-beach `oauth-gmail-*` pattern). connector-api begins **initial inbox sync** (last 30 days of INBOX threads — bounded to keep first-load fast) and starts the Gmail `users.watch` Pub/Sub subscription.
4. HME emits `EntityConnectorDefaultsQueued` → `EntityFirstInteractionReady` (per entity-creation event chain) once the first sync batch lands. Operator gets in-app notification: "Your inbox is ready — 47 threads loaded." Total wall-clock for typical mailbox: 30-60 sec.
5. Operator clicks the notification → lands at `/inbox`. First thread visible. Reply works on first try.

### Journey B — Customer email arrives → operator sees in dashboard → replies → reply lands in customer's Gmail
1. Customer sends mail to `bookings@carmenbeach.com`. Gmail receives. Workspace's `gmail.users.watch` Pub/Sub watch fires → push subscription POSTs to connector-api `/v1/webhooks/gmail-inbound`.
2. connector-api fetches the new message via Gmail API (`users.messages.get` with full payload), idempotency-checked on `email_message_id`, and emits `email.received` event to HME with entity_id + thread_id + message metadata + multi-axis tags.
3. HME upserts `support_threads` + `support_messages` rows (extending the existing tables from omnichannel-support design with the new email-specific fields). decision-engine pre-drafts a suggested reply via `/v1/proposals` (off-channel, won't auto-send).
4. Operator opens `/inbox`. New unread thread shows at the top with channel badge "email", subject preview, multi-axis tag chips (urgency / intent_class). Operator clicks the thread.
5. Thread view renders messages chronologically. The decision-engine pre-draft appears as a collapsible "Suggested reply" card above the compose box. Operator edits or replaces the draft text, clicks **Reply**.
6. gigaton-ui-system POSTs to gateway `/v1/operators/{entity_id}/inbox/threads/{thread_id}/reply`. Gateway routes to connector-api → `gmail.users.messages.send` with proper `In-Reply-To` + `References` headers preserving the thread.
7. Reply event logged to HME with `direction=outbound` + PPIM signature + the message lands in the customer's Gmail inbox correctly threaded under the original conversation. Operator's Gmail "Sent" folder also gets it (Gmail handles that natively because we sent via Gmail API).

### Journey C — Operator searches "did Sarah ever ask about X" → unified result across inbox + chat + SMS via persona-engine
1. Operator types into the global search bar (top of every `/inbox*` page): `sarah refund`.
2. UI POSTs to HME `/v1/operators/{entity_id}/search` with query. HME runs full-text search across `support_threads.body_text` + `support_messages.body_text` scoped by `operator_id` (X-Client-Namespace enforced).
3. Before returning, HME calls persona-engine `/v1/humans/match` with the surface terms — persona-engine identifies the canonical `human_id` for "Sarah" (matching across `email_address[]` + `phone_e164[]` + `wa_id[]` + name fuzzy-match).
4. HME re-queries thread filtered by `human_id` → returns ALL threads where Sarah is the counterpart, regardless of which channel they arrived on (email, SMS, WhatsApp, platform chat). All channels show in one ranked list with channel badges and the matching snippet highlighted.
5. Operator clicks the top hit (an email from 3 months ago about a refund) → lands in `/inbox/{thread_id}`. The right-side identity-resolution sidebar shows: "Sarah Chen — also reached out via WhatsApp (Apr 12), SMS (Mar 8), platform chat (Feb 2)." Operator can click any of those to context-switch.

---

## 3. OAuth + Connector Flow

### Scopes
| Scope | Why |
|---|---|
| `gmail.readonly` | List threads + messages + labels for inbox display |
| `gmail.send` | Send replies + new messages |
| `gmail.modify` | Label management (apply/remove labels), archive (remove `INBOX` label), star/unstar |
| `gmail.metadata` (NOT requested) | Insufficient — can't read message bodies; ruled out |
| `gmail.full` (NOT requested) | Excessive — includes Drafts CRUD + Settings; ruled out per scope-minimization doctrine |

### Token storage
- Per-entity refresh token persisted in Secret Manager at `gmail-oauth-{entity_id}` (e.g. `gmail-oauth-carmen-beach-properties`, `gmail-oauth-gigaton-ai`, `gmail-oauth-multipli`).
- Same shape as existing carmen-beach `oauth-gmail-*` secrets — JSON blob with `{refresh_token, client_id, client_secret_ref, scope, granted_at, last_refreshed_at}`.
- Migration note: when the GCP project-consolidation arc lands ([[gcp_engine_migration_accelerated_2026_05_25]]), the secret namespace flips from `carmen-beach-properties` project to `gigaton-platform` project; naming standardizes to `gmail-oauth-{entity_id}` everywhere.
- Access tokens are short-lived (1h) and cached in-memory in connector-api with refresh-on-expiry. Refresh tokens are exchanged via the `client_id` + `client_secret` stored in the platform-wide `google-oauth-client-secret` secret.
- Per-connection metadata (account email, scopes granted, last sync, watch expiration) lives in `user_connections` (per [[universal_connector_hub_architecture]]) keyed on (`entity_id`, `connector_id='google_workspace_gmail'`).

### Re-auth flow
- Google refresh tokens for OAuth web-app clients expire after **6 months of inactivity** OR if the user revokes at `myaccount.google.com`.
- connector-api logs every refresh attempt; on `invalid_grant`, the connection state flips to `status: expired`, an HME event `email.connection.expired` is emitted, and the entity owner sees a banner in `/inbox`: "Your Workspace connection expired — reconnect to resume." Click → re-runs the OAuth flow described in Journey A.
- The Pub/Sub `users.watch` subscription also expires every **7 days** per Gmail API rules. A Cloud Scheduler cron in connector-api re-issues `users.watch` calls every 6 days for every entity with an active connection. Watch re-issue failure → `email.watch.refresh_failed` HME event + banner.

### Authorize → first-sync handshake
1. Operator clicks "Connect Google Workspace" → UAE `POST /v1/entities/{id}/google-workspace/connect` → returns OAuth `authorization_url` with `state=<entity_id>:<nonce>`.
2. Operator consents → Google redirects to `gateway.gigaton.ai/v1/oauth/callback/google-workspace?code=...&state=...`.
3. Gateway proxies to UAE callback handler → UAE exchanges code for refresh+access token, writes secret, writes `user_connections` row, returns `{connection_id, mailbox_email}`.
4. UAE emits HME event `email.connection.established` → triggers connector-api `/v1/inbox/{entity_id}/sync` for initial 30-day pull + `gmail.users.watch` setup.

---

## 4. Pub/Sub Inbound Watch

### Per-entity topology
- One Pub/Sub topic per entity: `gmail-inbound-{entity_id}` in `gigaton-platform` project (post-migration; carmen-beach project pre-migration).
- One push subscription per topic targeting connector-api: `https://connector-api.gigaton.ai/v1/webhooks/gmail-inbound` with `audience=connector-api`, OIDC-authenticated.
- `gmail.users.watch` request includes `topicName` + `labelIds: ['INBOX']` (only fire on INBOX changes) + `labelFilterBehavior: 'INCLUDE'`.

### Inbound webhook flow
1. Gmail fires Pub/Sub message: `{emailAddress, historyId}` (Gmail's payload is minimal — just the watermark).
2. connector-api `/v1/webhooks/gmail-inbound` receives, verifies OIDC, looks up entity from emailAddress → entity mapping (cached in `user_connections`).
3. connector-api fetches changes since the last `historyId` via `gmail.users.history.list` (the historyId watermark is per-entity, stored in `user_connections.metadata.last_history_id`).
4. For each new message: `gmail.users.messages.get` → parse → check idempotency on `(entity_id, email_message_id)` → upsert `support_messages` row → emit HME `email.received` event with `{entity_id, thread_id, email_message_id, email_thread_id, from, to, subject, snippet, gmail_label_ids}`.
5. HME's existing trigger map fires downstream actions: persona-engine identity match, intel-silo memory ingestion, decision-engine proposal pre-draft.

### Watermark + replay
- `last_history_id` is updated atomically only after successful HME emit. Webhook failure mid-fetch = no watermark advance = next webhook re-fetches the missed history range. Idempotency on `email_message_id` prevents duplicates.
- Cold-start backfill: when an entity first connects, connector-api uses `gmail.users.messages.list` (with `q='in:inbox newer_than:30d'`) to seed, not history-list — history-list only retains ~30 days of history anyway.

---

## 5. Outbound Send Flow

```
Operator clicks "Reply" in /inbox/{thread_id} UI
  ↓
gigaton-ui-system POST to gateway:
  /v1/operators/{entity_id}/inbox/threads/{thread_id}/reply
  body: {body_text, body_html?, in_reply_to_message_id, attachments?, label_ids_to_apply?}
  ↓
gateway routes to connector-api with X-Client-Namespace + UAE capability check (support.respond)
  ↓
connector-api:
  1. Resolves refresh token from gmail-oauth-{entity_id} secret
  2. Loads thread context from HME (original message's email_message_id + email_thread_id + References chain)
  3. Constructs RFC-5322 MIME message:
       - From: <operator's mailbox, e.g. bookings@carmenbeach.com>
       - To: <recipient from original thread>
       - Subject: Re: <original subject, deduplicating "Re: "> 
       - In-Reply-To: <original email_message_id>
       - References: <accumulated References chain + original Message-ID>
       - Body-Text + Body-HTML alternatives
  4. Calls gmail.users.messages.send with threadId=<email_thread_id>
       (Gmail respects this to keep the message inside the existing thread server-side)
  5. Persists outbound support_messages row with provider Message-ID
  6. Emits HME event email.sent
  ↓
Reply lands in customer's Gmail correctly threaded
Operator's Gmail "Sent" folder also has it (Gmail handles automatically when sent via API)
Gigaton inbox UI optimistically renders the outbound message immediately;
   confirms on HME ack.
```

### PPIM signature on every outbound
```yaml
ppim_interaction: support|booking_inquiry|sales|... (inferred from thread.multi_axis_tags.intent_class)
ppim_economics:
  cost_estimate_per_call: 0.0001 USD (Gmail API send) + 3-6 staff-minutes
  revenue_attribution_path: indirect — preserves customer LTV via thread resolution; Penrose `revenue_per_human_touch` denominator
ppim_predictability: medium (within 25% by Week 4 once cohort instrumented)
ppim_brand_dimension: responsiveness + resolution + personalization
```

---

## 6. HME Schema Extension

Reuses `support_threads` + `support_messages` from omnichannel-support design (no new tables for v1). New fields added via additive migrations:

```sql
ALTER TABLE support_threads ADD COLUMN email_thread_id text;       -- Gmail's threadId
ALTER TABLE support_threads ADD COLUMN gmail_label_ids text[];     -- e.g. {'INBOX','IMPORTANT','Label_4'}
ALTER TABLE support_threads ADD COLUMN inbox_owner_entity_id text; -- which entity's mailbox received this
CREATE INDEX idx_support_threads_email_thread ON support_threads(operator_id, email_thread_id);

ALTER TABLE support_messages ADD COLUMN email_message_id text;     -- RFC-5322 Message-ID header
ALTER TABLE support_messages ADD COLUMN email_in_reply_to text;    -- RFC-5322 In-Reply-To
ALTER TABLE support_messages ADD COLUMN email_references text[];   -- RFC-5322 References chain
ALTER TABLE support_messages ADD COLUMN is_inbox_owner_action bool DEFAULT false;
  -- TRUE = inbox owner (or their operator-of-operator team) sent it
  -- FALSE = ext counterpart sent it OR support-bot generated it
CREATE UNIQUE INDEX idx_support_messages_email_msgid ON support_messages(operator_id, email_message_id) WHERE email_message_id IS NOT NULL;
```

### 2 new HME event types
- `inbox.thread_label_changed` — payload `{thread_id, label_ids_before, label_ids_after, by_human_id}`
- `inbox.thread_archived` — payload `{thread_id, by_human_id, archived_at}`

(Plus the existing `email.received` / `email.sent` events from omnichannel-support cover the read+reply path.)

### Multi-axis tag schema on `support_threads.multi_axis_tags` (per omnichannel design + modular-replication doctrine)
```json
{
  "industry": "hospitality",
  "sub_vertical": "short_term_rental",
  "geo": ["country:mexico","state:quintana_roo","city:playa_del_carmen"],
  "regime": ["mx_sat"],
  "segment": "tourist",
  "lifecycle": "inquiry",
  "intent_class": "booking_inquiry",
  "urgency": "medium",
  "channel_origin": "email",
  "provenance": "operator_supplied",
  "modality": "qualitative"
}
```

---

## 7. UI Surface (gigaton-ui-system)

3 net-new pages. All scoped by `X-Client-Namespace = entity_id`.

### `/inbox` — thread list
- Top bar: global search (UnifiedSearch — see Journey C), channel filter chips (email / sms / whatsapp / chat), label filter (Gmail labels), status filter (open / pending_customer / resolved).
- Thread rows: avatar (persona-engine resolved or fallback initials), counterpart name, subject preview, last-message snippet, channel badge, multi-axis tag chips (top 2 most-discriminative), last-message timestamp, unread indicator.
- Bulk actions: archive selected, label selected, mark resolved selected.
- Infinite scroll; default pagination 50/page; sort by last_message_at DESC.

### `/inbox/{thread_id}` — single thread view
- Header: counterpart name + Gmail labels + status + reply-to mailbox dropdown (if entity has multiple mailboxes).
- Message stream: chronological, with direction indicator (inbound left / outbound right), per-message timestamp, channel icon, attachment previews. Quoted-text auto-collapsed (Gmail-style).
- Suggested reply (decision-engine pre-draft): collapsible card above compose, with "Use draft" button.
- Compose box: rich-text + plain-text toggle, attachments, send-button. Inline channel-aware suggestions (intel-silo memory_search results: "3 similar past threads — most-effective reply was X").
- Right sidebar: identity-resolution panel showing `human_id` cross-channel surface — "also reached out via: WhatsApp (2 threads), SMS (5 threads), platform chat (1 thread)". Click any → context-switch.
- Top-right actions: Archive (apply Gmail INBOX label removal), Label (multi-select label picker), Mark resolved.

### `/inbox/connectors` — OAuth admin
- Per-entity card showing connected Workspace tenant (`workspace.email`, scopes granted, last sync, connection status).
- Multi-mailbox list under each entity: which mailboxes are being watched (e.g. `bookings@`, `support@`, `hello@`).
- Revoke button → calls `DELETE /v1/entities/{id}/google-workspace` → deletes secret + revokes refresh token via Google revocation endpoint + tears down Pub/Sub watch + flips connection status to `disconnected`.
- Reconnect button (for expired connections) → re-runs OAuth from Journey A.

---

## 8. Multi-Channel Unified Thread

When Sarah emails `support@gigaton.ai` AND later WhatsApps the same support number, persona-engine matches her via `(email_address ∋ sarah@example.com)` + `(phone_e164 ∋ +1-555-...)` + name fuzzy-match → returns a single `human_id`. Both messages land in **ONE thread** (per the omnichannel `support_threads` 7-day continuity rule), ordered chronologically. Operator sees both in `/inbox/{thread_id}`.

### Reply routing when channels are mixed
- Per omnichannel doctrine: **reply on the channel of the most recent inbound message**, unless operator explicitly switches.
- In `/inbox/{thread_id}`, the compose box header indicates "Replying via WhatsApp (last message from Sarah was WhatsApp at 3:14pm)". A channel-switch dropdown lets operator pick a different channel; only channels Sarah has used + has not opted out of are selectable.
- Cross-channel dispatch is the existing omnichannel infrastructure — the inbox UI delegates to the same gateway endpoint `/v1/support/threads/{id}/reply` with `channel_override` parameter.

### Anti-cross-tenant leakage
- `human_id` is scoped per `operator_id` (per modular-replication doctrine). Sarah-at-Carmen-Beach and Sarah-at-Multipli are different `human_id`s even if the email + phone match exactly. Cross-entity joining is explicitly disabled.
- Search results in `/inbox` for an operator NEVER include data from a different entity's namespace. Enforced at HME query layer + UAE capability check.

---

## 9. Operator Self-Serve Onboarding

In entity-creation flow Step 9 (`default_connectors` wiring), Google Workspace is the FIRST connector card shown (because email is foundational). UI affordance:

```
┌──────────────────────────────────────────────────────────┐
│ Connect Google Workspace                                 │
│                                                          │
│ Pull your entity's email into Gigaton so you can         │
│ read + reply without switching apps.                     │
│                                                          │
│ Domain: carmenbeach.com (verified in Step 3)            │
│ Mailboxes to connect: bookings@, support@, hello@        │
│   (auto-detected from Workspace tenant after consent)    │
│                                                          │
│ [ Connect Workspace → ]                                  │
│                                                          │
│ ☐ Don't have Google Workspace? Set up at workspace.google│
│   .com/business/, then come back here.                   │
└──────────────────────────────────────────────────────────┘
```

- Click → OAuth flow per §3.
- On consent return, background sync starts. Operator sees a non-blocking toast: "Connected — your inbox will be ready in about 30 seconds."
- When `email.connection.established` + first sync complete → in-app notification: "Your inbox is ready — {n} threads loaded. View now →"
- Notification click → `/inbox`. Banner at top: "First-time tip: replies you send here go straight to the customer's Gmail — they won't see Gigaton anywhere in the email."

---

## 10. Net-New Endpoints (additive only — no new modules)

| # | Method + Path | Engine | Purpose |
|---|---|---|---|
| 1 | `POST /v1/entities/{id}/google-workspace/connect` | UAE | Begin OAuth install; returns `{authorization_url, state}` |
| 2 | `DELETE /v1/entities/{id}/google-workspace` | UAE | Revoke connection: delete secret + revoke at Google + tear down watch |
| 3 | `POST /v1/oauth/callback/google-workspace` | UAE (gateway-proxied) | OAuth callback handler; exchanges code → writes secret → emits `email.connection.established` |
| 4 | `POST /v1/webhooks/gmail-inbound` | connector-api | Pub/Sub push-subscription receiver; verifies OIDC; fetches changes; emits `email.received` |
| 5 | `POST /v1/inbox/{entity_id}/sync` | connector-api | Full re-sync (last 30d) — used on first connect + on operator-initiated "refresh" |
| 6 | `POST /v1/inbox/{entity_id}/threads/{tid}/reply` | connector-api | Send reply via Gmail API; persists outbound row + emits `email.sent` |
| 7 | `GET /v1/inbox/{entity_id}/threads` | HME | Thread list for `/inbox` (filters: status / channel / label / since / limit) |
| 8 | `GET /v1/inbox/{entity_id}/threads/{tid}` | HME | Single thread + messages for `/inbox/{thread_id}` |
| 9 | `POST /v1/inbox/{entity_id}/threads/{tid}/label` | connector-api | Apply/remove Gmail labels via `users.messages.modify`; emits `inbox.thread_label_changed` |
| 10 | `POST /v1/inbox/{entity_id}/threads/{tid}/archive` | connector-api | Remove `INBOX` label via `users.messages.modify`; emits `inbox.thread_archived` |

**Engine-by-engine totals:**
- **UAE:** 3 endpoints (#1, #2, #3) + 0 new tables (reuses `user_connections` + new secret naming pattern)
- **connector-api:** 5 endpoints (#4, #5, #6, #9, #10) + 1 Gmail adapter module + Pub/Sub watch lifecycle manager + Cloud Scheduler cron for 6-day watch refresh
- **HME:** 2 endpoints (#7, #8) + schema extension on existing `support_threads` / `support_messages` tables + 2 new event types (`inbox.thread_label_changed`, `inbox.thread_archived`)
- **gigaton-ui-system:** 3 new pages (`/inbox`, `/inbox/{thread_id}`, `/inbox/connectors`) + UnifiedSearch global widget
- **persona-engine:** 0 new endpoints; extends `humans.email_address[]` field if not already present (likely already there per omnichannel design); existing `/v1/humans/match` endpoint serves the cross-channel unified-search use case
- **intel-silo:** 0 new endpoints; semantic memory ingestion of email body+subject as it does for SMS/WhatsApp/chat; existing `/v1/memory/search` serves the inbox reply-context-suggestion use case

**Total: 10 net-new endpoints across UAE, connector-api, HME — zero new services, zero new modules.**

---

## 11. Identity Unification + Privacy

### Identity unification
- persona-engine `humans` table already carries `email_address text[]` (one human can have N emails) per the omnichannel-support design. This spec leverages that field; no schema change.
- On inbound email arrival:
  1. `from_email` extracted from RFC-5322 `From:` header.
  2. persona-engine `/v1/humans/match` called with `{email: from_email, operator_id: <entity_id>}`.
  3. If matched → reuse existing `human_id` (and append `from_email` to `email_address[]` if it's not already there).
  4. If no match → create new `humans` row with `trust_tier: T0`, `status: unverified_contact`, `email_address: [from_email]`.
  5. Fuzzy-merge candidates surface as proposals into decision-engine (per omnichannel design) when 2 humans share signals; operator approves merge in dashboard.

### Operator-facing identity sidebar
In `/inbox/{thread_id}`, the right sidebar fetches `GET /v1/personas/{human_id}` and renders:
- Display name + avatar
- All known channels: `["sarah@example.com", "+1-555-XXXX", "wa:1555XXXX"]` (channels they've actually used; not all `email_address[]` entries)
- Past thread count by channel
- BFT state snapshot (trust_tier + recent state estimate from PPEME)
- Past interaction summary (top-3 by recency from intel-silo memory_search)

### Privacy
- **Email content encrypted at rest in HME.** `support_messages.body_text` + `body_html` stored encrypted under the per-entity KMS key (per the existing KMS keyring shipped 2026-05-22). Decryption only on operator read with valid `X-Client-Namespace`.
- **Cross-entity inbox queries impossible.** Every HME query layer + UAE capability layer filters by `operator_id` from `X-Client-Namespace` header. No global queries that span entities.
- **No auto-archive without operator action.** Threads remain in INBOX until operator explicitly archives. (Anti-pattern below.)
- **Retention: Workspace owns it.** Platform never auto-deletes emails for compliance reasons — Workspace Vault + Workspace retention rules govern. The platform deletes only when the operator explicitly archives + the operator-account-level retention rule cascades.
- **Right to erasure (GDPR / DPA).** If a customer requests erasure, operator triggers `POST /v1/personas/{human_id}/erase` in persona-engine (existing endpoint), which cascades to HME (anonymize support_messages where `human_id` matches) and to intel-silo (purge semantic chunks). Email content in the customer's own Gmail is theirs to manage — not ours.

---

## 12. Quotas + Cost Model

### Gmail API quotas (per Workspace tenant)
- **1 billion quota units / day per Workspace** — extremely generous (a typical inbox at ~500 msgs/day uses < 100k units).
- **Rate limit: 250 quota units / second / user** — burst-safe. connector-api uses exponential backoff + per-user token bucket; v1 won't hit the ceiling for any realistic operator.

### Pub/Sub costs
- Inbound `gmail-inbound-{entity_id}` topics — Pub/Sub charges $40/TB ingress. Each Gmail Pub/Sub notification is ~200 bytes (`{emailAddress, historyId}` JSON). At 1000 emails/day/entity, that's 200KB/day — **negligible** (<$0.01/operator/month).
- Push subscriptions are free (only pay for delivery to non-GCP targets — connector-api is on Cloud Run, same-network).

### Internal cost target
**<$0.01/operator/day for inbox sync at average mailbox size** (~500 msgs/day with 5% reply rate).
- Gmail API calls: free (within quota)
- Pub/Sub: <$0.01/month
- Cloud Run egress for `messages.get` payloads: <$0.005/operator/day (1000 msgs × ~5KB each = 5MB/day)
- HME storage: ~5KB/message * 365 days * 500 msgs = ~900MB/entity/year ≈ $0.02/year for storage; cost dominated by query compute (Postgres on Cloud SQL — already a fixed cost per the shared instance)

Per the [[user_influence_vs_cost_dashboard_spec]] doctrine, every inbox interaction writes to `third_party_call_cost` with per-event cost attribution.

---

## 13. Anti-Patterns

- **Storing email content in plaintext at rest.** Bodies are encrypted at the HME layer under per-entity KMS key. Decryption only on authenticated read.
- **Cross-entity inbox queries.** Every query in every engine filters by `operator_id` derived from `X-Client-Namespace` header. No "admin god view" that joins inboxes across entities — even Founder admin uses per-entity namespace switching to inspect.
- **Auto-archive without operator action.** Threads remain in INBOX until operator explicitly archives. No "auto-archive after 30 days" rule. Workspace's native archiving is operator-controlled and unchanged by Gigaton.
- **Auto-delete emails for retention compliance.** Platform never deletes emails for compliance — Workspace Vault + Workspace retention rules govern. We have no business deleting customer emails.
- **Per-individual Gmail OAuth.** Each entity's Workspace tenant is what we OAuth — not each operator-of-operator's personal Gmail. Saves token mgmt + scope sprawl; Workspace admin gives Gigaton mailbox access at tenant level.
- **Polling Gmail every N minutes instead of Pub/Sub watch.** Always use `users.watch` push subscription. Polling burns quota + adds latency + drifts.
- **Forgetting `In-Reply-To` / `References` on outbound.** Customer's mail client would treat our reply as a new conversation. Every outbound send REQUIRES correct header chain — covered by connector-api send adapter contract test.
- **Hardcoding entity-specific behavior.** Same Gmail adapter serves every entity. Entity-specific behavior is `operator_context` substitution; never code branch.
- **AI auto-send.** Every outbound v1 is human-authored. LLM may pre-draft via decision-engine `/v1/proposals`; auto-send is Decision Execution Engine v1.1+ territory.
- **IMAP fallback.** Per EMAIL-1, Gmail+Workspace only. Operators on non-Workspace mail are not eligible — surface a "Workspace required" callout at Step 9 instead of building an IMAP code path that's locked-out anyway.
- **Per-mailbox separate UI tab.** v1 unifies all mailboxes per entity in one `/inbox` view, with channel/recipient filter chips. Per-mailbox tab is power-user feature deferred to v1.1.
- **Forgetting to refresh the Pub/Sub watch every 7 days.** Watch expires silently. Cron in connector-api refreshes every 6 days for every active entity. Missed refresh = `email.watch.refresh_failed` HME event + operator banner.

---

## 14. Build Sequence — Compressed 4-Week Arc

(Assumes no migration blocking; the [[gcp_engine_migration_accelerated_2026_05_25]] parallel deploys remain DR standby and don't block this spec.)

### Week 1 (2026-05-25 → 2026-06-01) — Design freeze + foundations
| Item | Owner | DoD |
|---|---|---|
| This spec finalized + reviewed | Founder + Claude | Spec at design-freeze; 5 open decisions in §15 resolved |
| HME schema migration drafted (additive: `email_message_id`, `email_thread_id`, `gmail_label_ids`, etc.) | HME agent | Alembic migration in PR-ready state; reviewed against existing `support_threads`/`support_messages` |
| connector-api Gmail adapter module scaffolded | connector-api agent | Module skeleton + token storage path + Gmail API client wrapper; no Pub/Sub yet |
| UAE OAuth start/callback endpoints scaffolded | UAE agent | Endpoints #1 + #3 from §10 return placeholder; OAuth handshake tested in staging w/ a test Workspace tenant |
| Per-entity secret naming convention locked (`gmail-oauth-{entity_id}`) + Secret Manager IAM grants drafted | Platform agent | Naming + IAM doc committed; carmen-beach `oauth-gmail-*` secrets identified for migration |

### Week 2 (2026-06-02 → 2026-06-08) — Pub/Sub watch + inbound + send + MVP UI list/thread
| Item | Owner | DoD |
|---|---|---|
| Pub/Sub topic-per-entity + push-subscription provisioner | connector-api agent | Calling `/v1/inbox/{entity_id}/sync` creates topic + sub + initial 30d backfill |
| `POST /v1/webhooks/gmail-inbound` end-to-end | connector-api agent | Real inbound email → `email.received` event in HME within 5 sec |
| `POST /v1/inbox/{entity_id}/threads/{tid}/reply` end-to-end | connector-api agent | Operator-side test reply sent via API arrives correctly threaded at recipient |
| HME endpoints #7 + #8 (thread list + single thread) | HME agent | API returns expected payload shapes; multi-axis tags surface |
| gigaton-ui-system `/inbox` MVP (list view) | UI agent | Renders threads, filter chips work, no reply UI yet |
| gigaton-ui-system `/inbox/{thread_id}` MVP (read-only thread view) | UI agent | Renders message stream chronologically, no compose yet |
| Carmen Beach + Gigaton-direct + 1 other entity used as dogfood test | Founder | Real mail flowing through 3 entities, no cross-tenant leakage |

### Week 3 (2026-06-09 → 2026-06-15) — Reply composer + identity + multi-channel
| Item | Owner | DoD |
|---|---|---|
| `/inbox/{thread_id}` compose box + reply button | UI agent | Operator can reply from UI; arrives at customer correctly threaded |
| decision-engine pre-draft `/v1/proposals` integration | UI + decision-engine agent | Suggested reply card appears above compose; "Use draft" button ports text |
| persona-engine identity-resolution sidebar | UI + persona-engine agent | Sidebar shows cross-channel surface for the thread's human_id |
| Multi-channel thread unification visible in `/inbox/{thread_id}` | UI agent | Email + WhatsApp + SMS in the same thread render chronologically with channel badges |
| Cloud Scheduler 6-day watch-refresh cron | connector-api agent | Cron LIVE in staging; verified watch refreshes successfully |
| `inbox.thread_label_changed` + `inbox.thread_archived` events end-to-end | HME + connector-api agent | Labeling/archiving from UI emits the event; Gmail reflects the change |

### Week 4 (2026-06-16 → 2026-06-22) — Search + label mgmt + revoke + first 25 operators
| Item | Owner | DoD |
|---|---|---|
| UnifiedSearch global widget | UI + HME agent | Search across inbox + chat + SMS + WhatsApp threads scoped to entity; identity-unified via persona-engine |
| Label management UI (multi-select, apply/remove) | UI + connector-api agent | Operator can apply Gmail labels from the UI; reflects in Gmail |
| `/inbox/connectors` revoke + reconnect flow | UI + UAE agent | Revoke deletes secret + revokes at Google + tears down watch; reconnect re-runs OAuth |
| Penrose `revenue_per_human_touch` instrumentation includes inbox messages | decision-engine agent | Inbox messages count toward the denominator like SMS/WhatsApp do |
| First 25 operators using the inbox in production | Founder + affiliates | 25 entities have a connected Workspace + at least 1 reply sent through the UI; KPI dashboard reflects |
| Retro + v1.1 backlog | Founder | Retro doc; v1.1 features (per-mailbox tabs, AI auto-send, advanced compose, calendar integration) prioritized |

---

## 15. Open Decisions for User (max 5)

1. **Gmail OAuth client: shared platform-wide vs per-GCP-project?** A single Google Cloud OAuth client (`google-oauth-client-id` + `google-oauth-client-secret` in `gigaton-platform` Secret Manager) used for all entities, OR one OAuth client per GCP project that hosts entities. Recommendation: **single platform-wide client** — simpler operations, single consent screen review by Google, and `state` parameter carries entity_id for routing. Per-project would multiply review surface + complicate the migration story.
2. **Multi-mailbox handling — auto-detect vs operator-pick?** When a Workspace tenant has multiple mailboxes (`bookings@`, `support@`, `hello@`), should we auto-watch all of them, or let operator pick which to surface in the platform inbox? Recommendation: **auto-watch all, surface all in `/inbox`, let operator filter via UI chip if they want only one**. Picking is overhead; filtering is delightful.
3. **Initial sync depth — 30 days, 90 days, or entire mailbox?** First-connect backfill window. 30 days = fast (target 30-60 sec), keeps storage modest, may miss long-running threads. 90 days = thorough, slow (5-15 min on a busy mailbox). Entire mailbox = could be hours + tens of GB. Recommendation: **30 days at first-connect** with a `POST /v1/inbox/{entity_id}/sync?days=N` operator-triggered deeper-sync option (capped at 365 days even via that escape hatch).
4. **Send-on-behalf vs delegated-send — which Gmail send pattern?** Workspace supports both. Send-on-behalf = sent from the operator's mailbox, requires `gmail.send` scope (what this spec proposes). Delegated-send = operator-of-operator's personal Gmail sends "as" the entity mailbox, requires Workspace admin to grant delegation. Recommendation: **send-on-behalf via Gmail API with tenant-level OAuth** — simpler, doesn't require admin to provision delegation per operator-of-operator.
5. **Encryption-at-rest key per-entity vs platform-wide?** §13 says per-entity KMS key. Per-entity = strongest isolation + clean revocation (delete key = unreadable); platform-wide = simpler ops, one key for all entities. Recommendation: **per-entity KMS key** (we already have a KMS keyring shipped 2026-05-22; one key per entity is ~$1/month overhead and is the right default for the multi-tenant doctrine).

---

## 16. Anti-Patterns (Engineering-level summary)

(Cross-referencing §13 — repeated here in checklist form for code reviewers.)

- [ ] Never store email body plaintext at rest. Always KMS-encrypted.
- [ ] Never query `support_threads` without `operator_id` filter from `X-Client-Namespace`.
- [ ] Never auto-archive or auto-delete on behalf of operator.
- [ ] Never request scopes beyond `gmail.readonly` + `gmail.send` + `gmail.modify`.
- [ ] Never poll Gmail; always `users.watch` + Pub/Sub push.
- [ ] Never construct outbound MIME without `In-Reply-To` + `References` chain for replies.
- [ ] Never hardcode entity-specific behavior in adapter code.
- [ ] Never auto-send LLM-drafted replies (v1).
- [ ] Never store OAuth tokens outside Secret Manager.
- [ ] Never forget the 6-day Pub/Sub watch refresh cron.

---

## ppim_signature

```yaml
ppim_interaction: support|booking_inquiry|sales|operations|... (inferred per thread.multi_axis_tags.intent_class)
ppim_economics:
  cost_estimate_per_inbound_event_usd: 0.0001 (Gmail API + Pub/Sub) + 0 staff-minutes (event-driven)
  cost_estimate_per_reply_usd: 0.0001 (Gmail API send) + 3-6 staff-minutes (operator authoring)
  cost_estimate_per_operator_per_day_usd: <0.01 at average mailbox size
  revenue_attribution_path: indirect — preserved customer LTV via thread resolution; Penrose `revenue_per_human_touch` denominator; cross-channel identity unification compounds attribution
ppim_predictability: medium (response time + first-touch resolution rate predictable within 25% by Week 4 once 30-day cohort instrumented; same metrics as omnichannel support)
ppim_brand_dimension: responsiveness + resolution + personalization (in-platform reply = no context-switch = personalization signal; cross-channel identity = brand coherence)
```

---

## Cross-references

- [[foundational_goal_gigaton_engineered_brand_experience]] — Platform Inbox completes the PPIM loop for email (read → respond → measure → attribute)
- [[foundational_modular_replication_via_input_substitution]] — same engine, `operator_context` = entity_id; adding an entity's inbox = secret + connection row, never code
- [[universal_connector_hub_architecture]] — Google Workspace Gmail is a connector in `connectors_catalog`; one of the highest-priority defaults per entity_type
- [[gignet_auto_trigger_orchestration]] — `email.received` / `email.sent` / `email.connection.established` / `inbox.thread_archived` are first-class trigger events
- `2026_05_25_entity_creation_flow_n_wide.md` — Step 9 wires Google Workspace as a default connector for every entity_type
- `2026_05_25_omnichannel_support_design.md` — extends the `support_threads`/`support_messages` schema; multi-channel reply routing is reused
- [[api_reference_2026_05_19]] — endpoint surfaces this spec extends (UAE, HME, connector-api, persona-engine, intel-silo, gigaton-ui-system)
- `decisions/2026-05-25_architecture_decisions_log.md` — §EMAIL-1 (Gmail+Workspace locked), §FEAT-1 (this feature)
