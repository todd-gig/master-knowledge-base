# Omnichannel Customer-Support Flow — Design Doc

**Date.** 2026-05-25
**Author.** Claude (design only — no code, no branches).
**Status.** DRAFT — design freeze target end of Week 1 (2026-06-01).
**Doctrine anchors.** [[foundational_goal_gigaton_engineered_brand_experience]] (PPIM) · [[foundational_modular_replication_via_input_substitution]] · [[universal_connector_hub_architecture]] · [[gignet_auto_trigger_orchestration]] · [[onboarding_workflow_v1_completion_verified_2026_05_22]] · [[product_service_package_gigaton_ti_solutions]].
**Related.**
- `master-knowledge-base/docs/architecture/2026_05_25_entity_creation_flow_n_wide.md` — entity creation provisions the support inbox per entity_type
- `master-knowledge-base/docs/architecture/2026_05_25_30_day_gigaton_company_launch_roadmap.md` — 30-day launch
- [[api_reference_2026_05_19]] — mimi-whatsapp + HME + intelligence-silo + connector-api endpoint surfaces
- `mimi-whatsapp` repo — current SMS + WhatsApp engine (Twilio-backed); LIVE at rev `00005-t5k`

---

## 1. Goal & Non-Goals

### Goal
Provide a single **omnichannel support flow** that:

1. Accepts inbound customer messages on **4 ingress channels**: email, platform chat, SMS, WhatsApp.
2. Triages inbound to the right human responder via **Slack** (team-side) or the **Gigaton operator dashboard** (in-platform).
3. Routes the response back through the **same channel** the customer used (channel-preserving reply).
4. Is **multi-tenant by default** — `gigaton-ai` (platform support for new operators during beta) and any operator (Carmen Beach, Multipli, virtual-tour shop-owners, etc.) all use the same engine with `operator_context` substitution.
5. Records every interaction as a **first-class PPIM artifact** with multi-axis tags, threaded across channel changes, attributable to revenue/cost.

The mechanism is the same engine across all operator types — only `operator_context` differs. Adding a new operator's inbox = a new `X-Client-Namespace` value + Slack channel auto-provision, never an engine change.

### Non-Goals (v1, 30-day window)
- **Full ticketing system** — no SLA timers, no auto-escalation tree, no L1/L2/L3 routing, no CSAT survey loop. v1 is a unified inbox with channel-aware reply routing. Zendesk/Intercom feature parity = v1.2+.
- **AI auto-reply** — every outbound v1 is human-authored. Decision-engine may pre-draft a suggested reply (proposal state) but the human in Slack hits send.
- **Voice / phone** — voice calls are out of v1. Twilio voice adapter is a v1.2 candidate.
- **Custom routing rules per operator** (round-robin, skills-based) — v1 routes to one Slack channel per operator. v1.1 introduces per-operator routing rules table.
- **Customer-portal self-service** — no "view your tickets" customer-facing UI. The customer's "portal" IS their original channel (their email/SMS/WhatsApp inbox).
- **Knowledge-base auto-suggestion** — intel-silo's memory_search will be hinted to the responder in Slack as context, but no public KB UI v1.
- **Inbound voice transcription / IVR** — out.

---

## 2. Channels

Per channel: ingress mechanism, routing target, reply mechanism, identity capture.

| # | Channel | Ingress | Identity Capture | Routing | Reply | Backing Engine |
|---|---|---|---|---|---|---|
| 1 | **Email** | Postmark/SendGrid inbound parse webhook → POST `/v1/support/inbound` (gateway → HME). Operator's `support@<their-domain>` MX'd (or forwarded) to inbound-parse vendor. | `from_email`, `from_name`, `Message-ID`, `In-Reply-To`, `References` headers | Slack thread post + HME `support.inbound.received` event | SMTP send via SendGrid (operator-domain DKIM-signed); preserves Message-ID chain so customer's mail client threads | **connector-api** (SendGrid adapter, new in v1) + HME |
| 2 | **SMS** | Twilio inbound webhook → mimi-whatsapp `/webhooks/sms` (new alias of existing whatsapp handler) → POST `/v1/support/inbound` | `to_e164`, `from_e164` | Slack thread post + HME `support.inbound.received` event | Twilio outbound via mimi-whatsapp `/v1/messages`; TCPA opt-out (STOP/HELP) auto-handled at engine | **mimi-whatsapp** (LIVE) + HME |
| 3 | **WhatsApp** | Twilio (or Meta) inbound webhook → mimi-whatsapp `/webhooks/whatsapp` (LIVE) → POST `/v1/support/inbound` | `from_wa_id`, `profile_name` | Slack thread post + HME `support.inbound.received` event | Twilio outbound via mimi-whatsapp `/v1/messages`; **24h session window** enforced — outside window engine auto-uses pre-approved template | **mimi-whatsapp** (LIVE) + HME |
| 4 | **Platform chat** | Embedded widget on `<operator-domain>` (rendered by gigaton-ui-system) → WebSocket to gigaton-gateway → POST `/v1/support/inbound` | session_id, optional logged-in `human_id` (persona-engine), browser fingerprint | Slack thread post + HME `support.inbound.received` event + chat-widget remains open with typing indicator | gigaton-ui-system pushes reply to WebSocket → renders in chat bubble | **gigaton-ui-system** + HME |
| 5 | **Slack (team-side triage)** | NOT a customer channel. Inbound from #1-4 are mirrored to `#support-{operator_id}` in operator's Slack workspace; team replies in the thread. | Slack `user_id` + `email` (Slack lookup) → mapped to platform `human_id` via UAE | Bridge bot consumes `message.channels` events filtered by thread_ts in `support_threads.slack_thread_ts` | Bridge bot identifies original channel from thread metadata; calls the right backing engine to send | **connector-api** Slack adapter (new in v1) + HME |

**The customer never sees Slack.** Slack is purely the team-side triage UI. The customer sees their original channel — their email arrives via SMTP, their WhatsApp reply arrives via Twilio, their chat-widget message renders in the widget.

---

## 3. Identity + Threading

### Identity unification
Same customer across channels (e.g. `+1-555-1234` SMS == `carol@example.com` email) is unified via **persona-engine** `human_id`:

- Each inbound message resolves to a `human_id`:
  - Existing persona match (phone, email, wa_id, browser-fingerprint+logged-in-session) → reuse `human_id`
  - No match → create a new `humans` row in persona-engine with the captured identifier and `trust_tier: T0`, status `unverified_contact`
- A merge proposal is fired into decision-engine `/v1/proposals` when two contact identifiers share signals (same phone last-4 + same name + same operator_context within 30d). Human approves the merge in dashboard; on approval persona-engine merges human rows and re-attributes prior threads.
- Per operator scoping — Carmen Beach's `carol@example.com` is a different `human_id` from Multipli's `carol@example.com`. Cross-operator joining is explicitly disabled (per modular replication doctrine).

### Thread persistence
HME owns the canonical thread. New table:

```
support_threads
  thread_id            uuid PK
  operator_id          text (X-Client-Namespace)
  human_id             uuid FK persona-engine
  origin_channel       enum(email|sms|whatsapp|chat)
  current_channel      enum(...)               -- can switch (rare but supported)
  slack_channel_id     text                    -- e.g. C0123ABC
  slack_thread_ts      text                    -- the Slack timestamp anchor
  status               enum(open|pending_team|pending_customer|resolved|archived)
  multi_axis_tags      jsonb                   -- {industry, geo, lifecycle, segment, intent_class, ...}
  ppim_signature       jsonb
  created_at           timestamptz
  last_message_at      timestamptz
  resolved_at          timestamptz
```

```
support_messages
  message_id           uuid PK
  thread_id            uuid FK
  direction            enum(inbound|outbound)
  channel              enum(email|sms|whatsapp|chat|slack_internal)
  channel_message_id   text                    -- provider-side id (email Message-ID, twilio SID, slack ts)
  channel_in_reply_to  text                    -- email In-Reply-To, twilio in_reply_to_sid, slack thread_ts
  body_text            text
  body_html            text NULL
  attachments          jsonb
  authored_by_human_id uuid NULL               -- responder for outbound
  llm_draft_id         uuid NULL               -- decision-engine proposal if pre-drafted
  emitted_at           timestamptz
  ppim_signature       jsonb
```

Thread continuity rule: a reply on ANY channel that matches `(human_id, operator_id, no other open thread in last 7d)` lands in the same `thread_id`. Switching channels mid-conversation is supported (rare but real — customer starts via chat, asks for SMS callback).

---

## 4. Routing Rules

### On inbound
```
inbound from channel X for operator_id Y:
  1. resolve human_id (persona-engine — match-or-create)
  2. find-or-create support_thread for (operator_id, human_id) per the 7d rule
  3. emit HME event support.inbound.received with thread_id
  4. lookup operator triage preference:
       a. operator has Slack workspace connected (connector-api credential exists for slack provider)?
            → bridge bot posts to #support-{operator_id} in operator's Slack
              - new thread: posts message with metadata block (channel, human display name, multi-axis tags)
              - existing thread (matched by support_threads.slack_thread_ts): posts as reply in existing thread
       b. else (operator has no Slack)?
            → bridge bot posts to operator's in-platform dashboard at /support/inbox
              - same metadata block rendered in dashboard UI
       c. operator_id == 'gigaton-ai' (platform-level beta support)?
            → ALWAYS posts to internal Slack workspace #beta-support (overrides the above)
  5. fire gignet trigger event support_inbound_routed → may fan-out to:
       - intel-silo memory_search for context retrieval (hint top-3 prior interactions)
       - decision-engine /v1/proposals (suggested-reply draft)
       - persona-engine BFT snapshot for the human (so responder sees trust_tier + state)
```

### On reply (outbound)
```
human responds in Slack thread (or in dashboard textbox):
  1. capture authored-by → map Slack user_id → human_id via UAE (cached)
  2. lookup support_thread by slack_thread_ts (or dashboard thread_id)
  3. determine target_channel:
       - default = thread.current_channel
       - if responder uses Slack `/reply-via email|sms|whatsapp|chat` slash command → switch channel for this message only
  4. dispatch via the right engine:
       - email → connector-api SendGrid send (with proper In-Reply-To header chain)
       - sms → mimi-whatsapp /v1/messages (SMS sender)
       - whatsapp → mimi-whatsapp /v1/messages (24h window check; auto-template if outside)
       - chat → gigaton-ui-system websocket push
  5. emit HME event support.outbound.sent with message_id + provider_message_id
  6. update support_thread.status (open → pending_customer)
```

---

## 5. Reply Path Detail

Slack reply flow end-to-end:

1. **Team member types in Slack thread** under the bridge-bot's inbound post.
2. **Bridge bot** (connector-api Slack adapter) subscribes to Slack Events API `message.channels` event with `thread_ts` filter on the bot's channels.
3. Bridge bot performs `(slack_channel_id, slack_thread_ts) → thread_id` lookup against `support_threads`. If no match, the message is ignored (it's a team-internal sidebar).
4. Bridge bot extracts response body (strips Slack mentions, expands user references), reads slash-command channel-override if present.
5. Bridge bot calls the appropriate engine to send:
   - mimi-whatsapp `POST /v1/messages` for SMS / WhatsApp
   - connector-api SendGrid send endpoint for email (new `POST /v1/operators/{id}/connectors/email/send`)
   - gigaton-ui-system chat-push endpoint for platform chat (new `POST /v1/chat/threads/{id}/push`)
6. Engine returns `provider_message_id`, bridge bot persists outbound row in `support_messages`.
7. HME emits `support.outbound.sent` event with thread_id, channel, latency_ms.
8. Decision-engine sees the event → updates Penrose `revenue_per_human_touch` denominator. If the responder used a pre-drafted LLM suggestion, decision-engine logs the human-override event (REVERSAL or MODIFICATION) with HMAC signature per [[api_reference_2026_05_19]] §2.
9. PPEME re-estimates the customer's BFT state from the new event (state estimator).
10. Intel-silo ingests the inbound + outbound pair as semantic memory chunk tagged `support.{channel}.{operator_id}`.

---

## 6. Net-New Endpoints (additive only — no new modules)

All endpoints are added to **existing engines**. No new service.

| Endpoint | Engine | Purpose |
|---|---|---|
| `POST /v1/support/inbound` | **gateway → HME** | Universal inbound webhook. Body: `{operator_id, channel, channel_message_id, from_identifier, body, in_reply_to?, attachments?}`. Idempotent on `(channel, channel_message_id)`. Returns `{thread_id, message_id, routed_to: "slack"|"dashboard"}`. |
| `POST /v1/support/threads/{thread_id}/reply` | **gateway → HME** | Universal reply (alternate to Slack — used by operator dashboard textbox). Body: `{body, channel_override?, authored_by_human_id}`. Returns `{message_id, dispatched_to_engine, provider_message_id}`. |
| `GET /v1/operators/{id}/support/threads` | **HME** | Operator dashboard listing. Query params: `status, channel, since, limit`. Returns `{threads: [...], count}`. |
| `GET /v1/support/threads/{id}` | **HME** | Single thread + full message history. |
| `POST /v1/support/threads/{id}/resolve` | **HME** | Mark thread resolved. Body: `{resolution_note, by_human_id, satisfaction_inferred?}`. Emits `support.thread.resolved`. |
| `POST /v1/webhooks/email-inbound` | **gateway** (proxied to HME) | Postmark/SendGrid inbound parse webhook receiver. Verifies vendor signature; converts to canonical inbound shape; calls `/v1/support/inbound`. |
| `POST /v1/webhooks/slack-events` | **gateway** (proxied to connector-api Slack bridge adapter) | Slack Events API receiver. Handles `message.channels`, `app_mention`, `member_joined_channel`. Filters non-thread messages out. |
| `POST /v1/operators/{id}/connectors/email/send` | **connector-api** | SMTP send via SendGrid (operator-domain DKIM). Body: `{to, from, subject, body_text, body_html, in_reply_to?, references?}`. Returns `{message_id, provider_message_id}`. |
| `POST /v1/operators/{id}/connectors/slack/connect` | **connector-api** | Begin Slack OAuth install flow for an operator. Returns `{install_url, state}`. |
| `POST /v1/operators/{id}/connectors/slack/provision-channel` | **connector-api** | Auto-create `#support-{operator_id}` channel + invite operator admin + invite bridge bot. Idempotent. |
| `POST /v1/chat/threads/{id}/push` | **gigaton-ui-system** | Push outbound chat message to widget over WebSocket. Body: `{body, authored_by_human_id}`. Returns 202. |
| `POST /v1/webhooks/sms` | **mimi-whatsapp** | New explicit SMS webhook handler (already implicitly handled by Twilio webhook; this aliases for clarity). |

**Endpoint count summary: 12 net-new endpoints** (across HME, gateway, connector-api, gigaton-ui-system, mimi-whatsapp). Zero new modules; zero new services.

---

## 7. Multi-Tenant Model

- Every endpoint requires `X-Client-Namespace: <operator_id>` header (per gateway middleware shipped 2026-05-21 §A.1).
- Per-operator data isolation enforced at engine layer — every query in HME's `support_threads` + `support_messages` filters on `operator_id`. UAE enforces capability check (`support.read`, `support.respond`, `support.resolve`).
- **Gigaton platform itself is just an operator** — `operator_id = 'gigaton-ai'`. The beta-launch support inbox (where new operators contacting Gigaton with platform questions land) uses identical infrastructure; only the `X-Client-Namespace` differs.
- **Per-operator Slack channel** — `#support-{operator_id}` auto-provisioned during entity creation step 9 (per `2026_05_25_entity_creation_flow_n_wide.md`). If operator has not connected Slack, the in-platform dashboard `/support/inbox` is the fallback triage surface.
- **No cross-tenant leakage** — bridge bot validates `(slack_channel_id → operator_id)` on every Slack event; a Slack message in `#support-multipli` cannot dispatch on Carmen Beach's `human_id`.

---

## 8. Channel-Specific Gotchas

| Channel | Gotcha | Mitigation |
|---|---|---|
| WhatsApp | **24h session window** — outside window, free-form messages rejected by Twilio; only pre-approved templates allowed. | mimi-whatsapp checks `last_inbound_at` on send; if > 24h, auto-substitutes a pre-approved template with the operator's text injected into a permitted variable slot. v1 ships with 3 templates per operator: appointment_reminder, follow_up_question, transactional_update. Template approval workflow with Meta is operator-side homework — documented in onboarding. |
| SMS | **Character limits** — single SMS = 160 GSM-7 chars OR 70 UCS-2 chars (emoji forces UCS-2). Long messages = multi-segment, billed per segment. | mimi-whatsapp splits at 153/67 boundaries, sends as concatenated segments. Outbound preview in Slack shows segment count + estimated cost. |
| SMS | **TCPA opt-out compliance** — STOP/UNSUBSCRIBE/CANCEL/END/QUIT must immediately stop messages to that number; HELP/INFO returns operator info. | mimi-whatsapp keyword-detects on inbound; on STOP, persists `support.human.opted_out=true` + responds with mandated confirmation + halts all future outbound to that E.164. HELP returns a short bio + opt-out instructions. |
| Email | **Deliverability** — SPF/DKIM/DMARC must be configured per operator domain or replies bounce / spam. | During entity creation step 9, connector-api email-connector OAuth flow includes DNS verification — operator must add SendGrid CNAMEs to their DNS or accept the `mail.gigaton.ai` shared domain (less branded, more deliverable on day 1). DNS unverified = outbound emails go via shared domain with operator name in From display + `reply-to: support@<operator-domain>`. |
| Email | **Reply threading** — Gmail/Outlook thread by `In-Reply-To` + `References` headers + Subject matching. Lose the chain = customer sees a new conversation. | `support_messages.channel_message_id` stores the full `Message-ID`. Outbound always sets `In-Reply-To` to the most recent inbound's Message-ID and accumulates `References` chain. Subject preserves `Re: ` prefix exactly once. |
| Platform chat | **WebSocket disconnects** — customer closes browser tab → reply arrives → never seen. | Persist all chat messages server-side; on widget reconnect (same session_id cookie within 30d), replay unread messages. For logged-in operators-of-operators (B2B chat), email-on-disconnect fallback after 5min unread. |
| Slack | **Rate limits** — Slack Web API caps at 1 message/sec/channel; Events API ack required within 3 sec. | Bridge bot uses queue + token-bucket per channel; acks Events API immediately and processes asynchronously. |
| Slack | **Thread message-count cap** — Slack threads degrade UX past ~200 replies. | When thread crosses 100 replies, bridge bot posts a "thread continued →" link to a new Slack message and updates `slack_thread_ts` to the new anchor. HME thread continuity is unaffected. |
| All | **Inbound from blocked / opt-out humans** | persona-engine carries `do_not_contact_channels: [email, sms, ...]`; outbound dispatch checks against this and refuses with explicit reason logged in `support_messages.dispatch_refused_reason`. |

---

## 9. Build Sequence — 30-Day Arc

Aligns with the design-freeze + deploys-resume pattern locked for the beta launch arc.

### Week 1 (2026-05-25 → 2026-06-01) — Design Freeze
- Lock this design doc + decisions (5 open items in §10)
- SendGrid (or Postmark — TBD §10) account provisioned for `gigaton.ai`; DKIM/SPF set up
- Slack workspace provisioned for `gigaton-ai` internal use (`#beta-support` channel created)
- Slack bridge bot Slack-app manifest written + reviewed (no code yet)
- HME schema migrations drafted: `support_threads`, `support_messages` tables
- Multi-axis tag taxonomy locked for `support_threads.multi_axis_tags` (industry / geo / lifecycle / intent_class / urgency)
- 29 ONBOARDING_EVENT_TYPES extended with 6 new `support.*` event types
- Wave 2 self-healing spec dependencies confirmed not-blocking

### Week 2 (2026-06-02 → 2026-06-08) — MVP Path
- HME schema migrations applied (alembic stack); 2 new tables LIVE
- gateway: `POST /v1/support/inbound` + `POST /v1/support/threads/{id}/reply` routes added to routing_table
- mimi-whatsapp: `/webhooks/sms` alias + `support.inbound.received` event emission on inbound; existing WhatsApp inbound wired to call `/v1/support/inbound`
- connector-api: Slack OAuth + Slack bridge adapter MVP (post inbound to channel; consume `message.channels` events; dispatch to mimi-whatsapp); SendGrid send adapter MVP
- gigaton-ui-system: platform-chat widget MVP (embeddable script tag); `/support/inbox` page in operator dashboard
- End-to-end smoke per channel: send Gigaton.ai an inbound on each of 4 channels; team responds in `#beta-support`; verify reply lands on the right channel
- Beta-launch support inbox cuts over to this flow (replaces ad-hoc `todd@gigaton.ai` + Slack DMs)

### Week 3 (2026-06-09 → 2026-06-15) — Multi-Tenant + Identity
- Per-operator Slack channel auto-provisioning wired into entity-creation step 9 (operator's entity creation → `#support-{operator_id}` auto-created + bridge bot invited)
- persona-engine identity unification (phone+email merge proposals) wired; manual approval UI in dashboard
- Carmen Beach onboarded as first non-platform operator (their `support@carmenbeach.com` MX'd; SMS via their Twilio number; WhatsApp via their Meta business profile; `#support-carmenbeach` provisioned)
- Decision-engine `/v1/proposals` pre-drafts wired — responder sees suggested reply in Slack thread as a separate bot message
- intel-silo memory_search hint wired — top-3 prior interactions surfaced in Slack thread metadata block

### Week 4 (2026-06-16 → 2026-06-22) — Pipeline Integration
- Multipli + virtual-tour-marketplace operators onboarded
- 50/day vendor-inquiry pipeline routes "support-ish" inbound into the omnichannel flow (instead of bespoke intake)
- Penrose `revenue_per_human_touch` metric instrumented from `support_messages` data
- `support.thread.resolved` events drive PPEME state-estimate refresh for the human (their post-support trust delta)
- Per-operator routing rules table introduced (round-robin / time-of-day) — staged for v1.1 enablement
- Soft v1 GA: docs page published at `gigaton.ai/docs/support`

---

## 10. Open Decisions for User (max 5)

1. **Email inbound vendor** — Postmark (cleaner inbound parse API, $10/mo + $1.50/1k) vs SendGrid (already in stack for outbound, single-vendor simpler) vs Mailgun. Recommendation: **SendGrid Inbound Parse** for single-vendor.
2. **Slack workspace for beta-support** — use existing `todd-gig.slack.com` (or whichever) vs spin up dedicated `gigaton-ai.slack.com`. Recommendation: **dedicated workspace** so per-operator workspace pattern is consistent (gigaton-ai is just another operator).
3. **Default reply channel when ambiguous** — if customer wrote from email but their persona has a known WhatsApp + the team member doesn't specify, reply via WhatsApp (richer) or email (where they wrote from)? Recommendation: **reply on the channel they wrote from** (channel-preserving by default; explicit slash-command to switch).
4. **AI pre-drafted reply UX in Slack** — render as a separate bot message under the inbound that the responder copies/pastes? Render as a `/draft` slash command result on demand? Auto-fill responder's compose box (not supported by Slack API)? Recommendation: **separate bot message with "Use this draft" button** that ports the text to the responder's input.
5. **Resolution detection** — explicit `/resolve` slash command only, or also auto-detect "thanks!" / 7-day silence / customer NPS positive response? Recommendation: **explicit only in v1** to avoid false positives; v1.1 introduces inference w/ confidence threshold and human-confirm.

---

## 11. Anti-Patterns

- **A new module for support** — violates the [[product_service_package_gigaton_ti_solutions]] no-new-module locked doctrine. Support distributes across existing engines.
- **Customer sees Slack** — Slack is purely team-side triage. Any UX where customer is asked to "join our Slack" violates the doctrine of channel-preserving response.
- **Per-operator hardcoded routing** — operator-specific behavior must live in `operator_context` / Slack channel / capability table, never in engine code.
- **Cross-operator data joining** — Carmen Beach's customer record and Multipli's customer record with the same email are explicitly separate `human_id`s. Joining requires explicit operator-merge action with audit.
- **Storing customer credentials in support_messages** — if a customer pastes a password into support chat, intel-silo's secret-grep scanner (per AX-024) flags + redacts before persistence.
- **WhatsApp free-form outside 24h window** — Twilio will reject; engine must auto-template-substitute, not silently fail.
- **Outbound without TCPA opt-out check** — every outbound dispatch hits the persona-engine `do_not_contact_channels` check; refuse to dispatch if blocked.
- **Slack thread without HME thread_id** — every bridge-bot inbound Slack post carries thread_id in metadata block; if Slack thread orphans (e.g. team manually creates a thread without bot involvement), bridge bot ignores.
- **AI-authored outbound v1** — every outbound v1 is human-authored (LLM may pre-draft). Auto-send without human approval = scope creep into Decision Execution Engine territory; defer.
- **Hardcoded channel list** — channels are catalog rows in `connectors_catalog`, not enums in code. Adding a 5th channel (Telegram, Instagram DM, Discord) = new catalog row + adapter, not engine change.

---

## ppim_signature

```yaml
ppim_interaction: support (every class — inquiry, dispute, refund, general)
ppim_economics:
  cost_estimate_per_touch: 4-8 staff-minutes (depends on channel + complexity) + per-channel $$ (SMS $0.0075/seg, WhatsApp $0.005/msg, email $0.0001/send, chat $0)
  revenue_attribution_path: indirect — preserved-customer LTV via thread.resolved → PPEME state update → next-booking probability uplift; Penrose `revenue_per_human_touch` denominator
ppim_predictability: medium (response time + first-touch resolution rate predictable within 25% by Week 4 once 30-day cohort instrumented)
ppim_brand_dimension: responsiveness + resolution + personalization (channel-preserving = personalization signal)
```

---

## Cross-references

- [[api_reference_2026_05_19]] — endpoints in §2 (decision-engine), §4 (HME), §6 (persona-engine), §7 (intel-silo), §8 (mimi-whatsapp), §9 (connector-api)
- [[universal_connector_hub_architecture]] — Slack + SendGrid are connectors; entries in `connectors_catalog`
- [[gignet_auto_trigger_orchestration]] — `support.inbound.received`, `support.outbound.sent`, `support.thread.resolved` are first-class trigger events in `orchestrator_triggers`
- [[onboarding_workflow_v1_completion_verified_2026_05_22]] — Stage 9 entity creation auto-provisions `#support-{operator_id}` Slack channel
- [[foundational_modular_replication_via_input_substitution]] — same engine, `operator_context` substituted; Gigaton-ai is just operator_id `gigaton-ai`
- `2026_05_25_entity_creation_flow_n_wide.md` — each entity_type's `default_connectors` includes the channel set appropriate for support (e.g. property_management = WhatsApp + email; saas_platform = email + chat)
