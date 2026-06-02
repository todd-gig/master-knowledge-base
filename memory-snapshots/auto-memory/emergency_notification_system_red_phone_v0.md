---
name: ""
metadata: 
  node_type: memory
  originSessionId: 148a52ab-8712-44bb-bd02-5031917a4e18
promoted_from: emergency_notification_system_red_phone_v0.md
promoted_at: 2026-06-02T20:13:25Z
---

# Emergency Notification System ("Red Phone") — v0 Spec

## Why this exists (separate from Slack-channel paging)

Standard HARD escalations route to a per-pool Slack channel + audit row (the v0 default). That's adequate for *informational* paging — the expert sees it, picks it up, ACKs in-channel.

**Some HARD escalations need more.** Specifically: when an event requires a recipient to **affirmatively acknowledge AND initial** (non-repudiation), and when the acknowledgement record itself must be **legally trackable** (audit by counsel, regulator, or counterparty). Examples:

- Payment authorization above a configured threshold (per-operator)
- Access grant / revoke on a privileged account
- Deploy/rollback affecting customer data
- Promote-symbol / judge-action / drift-rollback in production
- Any action where "the operator said yes" must survive subpoena

Slack messages don't satisfy any of those. SMS + email + WhatsApp + Telegram fan-out, ACK loop, initialed signature, and Google-Drive-backed legal record do.

## Canonical name + class placement

Canonical name: **Red Phone**. New escalation class **`EMERGENCY`** sits one rung above `HARD` in the precedence ladder defined in [[ti_expert_escalation_decision_logic]]:

```
EMERGENCY > HARD > SOFT > MANAGED > NONE
```

Selection (in addition to the current HARD rules):

- `intent.requires_red_phone == True` (explicit flag set upstream)
- `intent.payment_amount_usd > org.red_phone_payment_threshold_usd` (per-operator, default $10,000)
- `intent` ∈ {`promote_symbol`, `rollback_calibration`, `judge_action`} AND `bundle.routing_score == 10`
- `intent.affects_production_customer_data == True`
- `routing_hint == "force_red_phone"`

When `EMERGENCY` fires, the standard HARD path STILL runs (review queue / signoff matrix row written; Slack channel notified). The red-phone fan-out is **additive**, not a replacement.

## Channels (v0)

Each channel is independently enable-able per operator. The operator's `red_phone_config` row declares which channels are "the red phone" for them — channels marked there fan out in parallel; channels not marked are silent.

| Channel | Backend | Dep status |
|---|---|---|
| **SMS** | Twilio (already wired via mimi-whatsapp) | reuse existing Twilio account; new sub-account or messaging-service ID |
| **Email** | gmail-support-relay SA (already provisioned per [[gmail_support_relay_setup_2026_05_25]]) | Workspace admin clicks were PARKED 2026-05-25 eve — need to confirm completion before email channel works |
| **WhatsApp** | Twilio WhatsApp + Meta WABA | BLOCKED until Matt's Meta verification completes (3-7d) |
| **Telegram** | Telegram Bot API (new) | Bot creation + token storage in Secret Manager required |
| **User-classified "red phone"** | configurable webhook URL | operator names the service in their config; system POSTs a defined payload |

`to_be_determined` channels (per user 2026-05-26): keep the channel registry open-schema so new channels (Signal, Discord, voice call via Twilio, etc.) can be added without migration.

## ACK + initialed signature workflow

Each outgoing message carries:

- A unique `ack_token` (UUIDv4, server-side issued)
- A short URL (`acks.gigaton.ai/{token}` — TBD subdomain) leading to an ACK page
- Inline ACK affordances per channel:
  - SMS / WhatsApp: reply `ACK <last-4-of-token> <initials>` (case-insensitive)
  - Email: click the link AND type initials on the linked page
  - Telegram: inline buttons + a follow-up "type your initials" prompt
  - Custom webhook: receives the ack_token; recipient service is responsible for posting back `{ack_token, initials, timestamp, ip}`

Initials are stored as typed text (minimum). Future v1 can layer a drawn-signature widget (the gigaton-ui-system already has `lucide-react` icons; signature pads ship as a small dep).

## Google-services legal-doc tracking

Every red-phone event (send + each ACK + each initial) is **appended** to a per-operator Google Doc maintained by the platform via the Drive/Docs API. The doc is the legal artifact: timestamped, ordered, immutable from the operator's side (platform owns write; operator gets View+Comment).

Structure:

- One Doc per operator per calendar year: `Red Phone Legal Log — {operator_name} — {YYYY}`
- Owned by `gmail-support-relay@gigaton-platform.iam.gserviceaccount.com` (the existing SA)
- Stored in a Drive folder the operator's legal counsel can be shared into (Comment-level access; no edit)
- Each event appended as a row in a table-shaped section (or as a Sheet, see open question below)
- A monthly summary row + a quarterly export-to-PDF webhook (legal counsel reads the PDF)

Why Google over a Postgres table: legal counsel reads Docs, not databases. The platform also writes the same rows to a Postgres `red_phone_audit` table for engineering queries — Drive is the legal-facing surface; Postgres is the engineering-facing surface; they must agree by construction (event-sourced from the same write).

## Data model (Postgres)

```sql
-- Per-operator config: which channels are the red phone, thresholds, recipient roster
CREATE TABLE red_phone_config (
  org_id           uuid PRIMARY KEY REFERENCES orgs(id),
  channels         jsonb NOT NULL DEFAULT '[]',          -- ["sms","email","whatsapp","telegram","webhook:slack-xyz"]
  recipients       jsonb NOT NULL DEFAULT '[]',          -- [{user_id, role, channel_overrides}]
  payment_threshold_usd numeric(12,2) DEFAULT 10000.00,
  legal_doc_id     text,                                 -- Drive Doc id; null until first event provisions it
  legal_folder_id  text,                                 -- Drive folder id (operator + counsel access)
  retry_policy     jsonb NOT NULL DEFAULT '{"per_channel_retries":2,"escalate_after_minutes":15}',
  created_at       timestamptz NOT NULL DEFAULT now(),
  updated_at       timestamptz NOT NULL DEFAULT now()
);

-- One row per emergency event (the trigger)
CREATE TABLE red_phone_events (
  event_id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id           uuid NOT NULL REFERENCES orgs(id),
  triggered_by     text NOT NULL,                        -- "expert_escalation:HARD" | "intent:payment_authorize" | etc.
  escalation_ref   text,                                 -- pointer to the review_queue / signoff_matrix row
  payload          jsonb NOT NULL,                       -- summary + context for the recipient
  channels_dispatched jsonb NOT NULL DEFAULT '[]',
  legal_doc_appended_at timestamptz,
  created_at       timestamptz NOT NULL DEFAULT now()
);

-- One row per channel send + one row per ACK
CREATE TABLE red_phone_messages (
  message_id       uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id         uuid NOT NULL REFERENCES red_phone_events(event_id),
  channel          text NOT NULL,                        -- "sms" | "email" | "whatsapp" | "telegram" | "webhook"
  recipient        text NOT NULL,                        -- phone | email | tg-chat-id | webhook-url
  ack_token        text NOT NULL UNIQUE,
  sent_at          timestamptz NOT NULL DEFAULT now(),
  acknowledged_at  timestamptz,
  initials         text,                                 -- recipient-typed initials at ACK time
  ack_ip           inet,
  ack_user_agent   text,
  legal_doc_appended_at timestamptz                      -- separate from event-level append (ACK rows append too)
);
```

## Service shape (recommended)

A new small service: `red-phone-engine` (Cloud Run, low-traffic, high-importance). Endpoints:

- `POST /v1/emergency/trigger` — called from `should_escalate_to_ti_expert` when class promotes to EMERGENCY. Dispatches fan-out, returns `event_id`.
- `GET /v1/emergency/ack/{ack_token}` — ACK page (the short-URL target). Captures initials + IP + UA.
- `POST /v1/emergency/ack-inline` — for SMS/WhatsApp/Telegram reply-based ACKs (callback from Twilio / Telegram webhook).
- `POST /v1/emergency/webhook-ack` — for custom-webhook channels.
- `GET /v1/emergency/event/{event_id}` — status (which channels ACKed, outstanding initials, etc.).

Cron job: every 60s, scan unacknowledged events past `escalate_after_minutes`; re-fan-out to next recipient in roster.

## Open decisions (default in brackets — proceed with default if no answer)

1. **Per-channel ACK syntax for SMS/WA/Telegram**: `ACK <last-4-token> <initials>` is unambiguous but verbose. Default: keep verbose; iterate after first 10 events.
2. **Legal-doc format — Google Doc vs Google Sheet**: Sheet is more queryable + counsel-friendly for filtering. Doc is more "legal-record-shaped." Default: **Sheet** (operator gets pretty PDF export quarterly; counsel-friendly).
3. **Who is the default recipient when `recipients[]` is empty**: the operator's owner (per UAE org row). Default: yes — owner is fallback; warn on first emergency that roster is empty.
4. **"Red phone" subdomain for the ACK short-link**: `acks.gigaton.ai`. Default: yes; requires DNS entry + Cloud Run mapping.
5. **Telegram bot — one platform bot or per-operator bot**: per-operator bot lets the operator brand it; one platform bot is simpler. Default: **one platform bot** for v0; revisit if any operator requests white-label.
6. **Retry escalation order**: per-channel retries first, then next recipient? Or fan-out to all channels at every retry? Default: per-channel retries first, then expand recipient list at `escalate_after_minutes`.
7. **PII handling**: the payload contains intent context, which may include customer PII. Default: redact PII from the channel payload (use a short reference like "view at acks.gigaton.ai/{token}"); full context only behind login on the ACK page.
8. **What counts as "initialed"** — typed text matching 1-4 letters, or drawn-signature widget. Default: **typed letters (min 2, max 4)**; v1 adds drawn signature.

## Dependencies + build sequencing

**Blocked-on** (must complete before any channel works):

- Email channel → Workspace admin clicks (PARKED per [[gmail_support_relay_setup_2026_05_25]]) — Bella or todd needs to complete the DWD entry
- WhatsApp channel → Matt's Meta WABA verification (3-7 day review, in progress per session handoff)
- Telegram channel → bot creation (5 min) + token in Secret Manager
- SMS channel → Twilio sub-account decision OR reuse mimi-whatsapp's Twilio (architectural call)
- Legal-doc tracking → Drive/Docs API enabled on gigaton-platform (verify) + operator-counsel-access folder convention defined

**Build sequence:**

1. Postgres migrations (`red_phone_config`, `red_phone_events`, `red_phone_messages`)
2. red-phone-engine skeleton service (no channels yet; in-memory dispatch + Postgres write)
3. ACK page (server-rendered HTML on the same service; initials capture)
4. Channel adapters one at a time: SMS first (reuse Twilio) → email (depends on Workspace) → WhatsApp (depends on Matt) → Telegram (new) → webhook (last)
5. Legal-doc adapter (Sheet writer + folder convention)
6. Integration into `expert_escalation` as a new `EMERGENCY` class

## Why: doctrinal motivation

- **Non-repudiation** is the fundamental legal requirement. Slack-only paging fails this; multi-channel + ACK + initials + Google-Doc append satisfies it.
- **Operator-classified red phone** matches [[smen_doctrine]] sovereignty: the operator owns which channel reaches them at 3am, not Gigaton.
- **Legal counsel reads Docs/Sheets, not databases**: the Google surface is the legally-citable artifact; the Postgres surface is the engineering working copy. Event-sourced from one write so they cannot diverge.
- **Two-tier paging** (Slack for HARD, red-phone for EMERGENCY) avoids alert fatigue: not every HARD event needs to wake the operator. EMERGENCY is the explicit "this needs you NOW + on the record" tier.

## How to apply

- When wiring a new intent that could plausibly need non-repudiable ACK: ask "would counsel want a signed record of every yes?" — if yes, mark it `requires_red_phone` or define a threshold.
- When adding a new operator: stand up their `red_phone_config` row, provision their Drive folder, share with counsel, before they cross any payment / access / deploy threshold.
- When a channel goes dark (Twilio outage, Telegram API change): the fan-out is parallel-redundant by design; v0 just logs the failure. v1 should page on missing-ACK regardless of channel status.
- When testing in staging: use a `dry_run=true` flag on the event; messages dispatched but `recipient` rewritten to a test phone/email/chat; legal-doc append goes to a `Red Phone Legal Log — STAGING` doc.
