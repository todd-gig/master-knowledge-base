---
name: ""
metadata: 
  node_type: memory
  originSessionId: 148a52ab-8712-44bb-bd02-5031917a4e18
promoted_from: red_phone_v0_channels_gated_email_inplatform_only.md
promoted_at: 2026-06-02T20:13:25Z
---

# Red Phone v0 Channels — Gated to Email + In-Platform Only (until others verified)

## The directive (verbatim)

> "Understand only email + system notifications from within platform will be available as options until completed and functional + ensure there are no broken paths and users are able to operate system end to end after next deployment"

## What this means concretely

**Until SMS / Telegram / WhatsApp / Webhook channels are each independently merged, deployed, AND verified end-to-end:**

- The `red_phone_config.channels` operator-facing config UI exposes **ONLY** two channel options:
  - `email` (transactional email)
  - `in_platform` (Gigaton-UI in-app notification, bell icon / notification center)
- Selecting other channels (`sms`, `telegram`, `whatsapp`, `webhook`) is **disabled / hidden** in the UI
- Backend validation **rejects** any operator config submission that includes a non-allowed channel — clean error, not a silent failure

**Why:** the partial channel adapters (SMS/Telegram/Webhook PRs #1/#2/#3 BLOCKED, BotFather not created, TFV not submitted to Twilio yet) cannot be exposed as options because they will silently no-op (`error_code: missing_env` / `no_credentials`) which is worse than not being an option. Operators who think they're configured for SMS but aren't will miss emergencies.

## "No broken paths" audit checklist (must pass before next deployment)

For every user-facing surface, confirm:

1. **Cowork-app `/cowork` route** — chat submit returns a real response with `tier` + `routing_reasons` populated (not empty/null), TierBadge renders, no 500 errors. Default operator (no special config) gets at minimum `tier=third-party-cloud` + 1+ routing reason.
2. **Admin Review Queue `/admin/review-queue`** — loads for any user with brand_experience_manager role; empty state renders cleanly when no items; submitting any pool filter returns either matching rows or empty-state, never 500.
3. **Founder Sign-off `/founder/signoff`** — loads for founder; empty state when no signoff items pending; submit accepts pool field gracefully.
4. **NavRail circles** (5 new approval surfaces) — all 5 are tier_3_recommend gated; circles render as locked OR functional based on operator's actual tier; clicking a locked circle shows the tooltip + does NOT 404.
5. **Red Phone config admin UI** — operator can:
   - View their current channel config
   - Add a recipient (with `email` or `in_platform` only; other types DISABLED in dropdown)
   - Set `payment_threshold_usd`
   - See their per-operator-per-year legal Sheet (link or empty state)
   - Cannot save a config containing disabled channels (backend rejects with clear message)
6. **Any /v1/intelligence/query call** — returns successfully with the new fields populated for every intent class; `system_routed: true` when flag is on; fail-soft to legacy path when flag is off.
7. **Connector Hub** — the ~32 endpoints that were silently failing now return either 200 with data OR 4xx with a clear `axiom_ref` + message; never a silent 400/empty.
8. **Onboarding stages** — a brand-new operator can complete stage 0 through tier_3_recommend WITHOUT hitting a gate that depends on red-phone, SMS, Telegram, or any of the blocked features. Tier-3 capability unlock happens via the existing flow.

## What ships in next deployment to satisfy this directive

| Item | Status | Action |
|---|---|---|
| Wire `expert_escalation` into operator-api `integration_hooks.py` request path | NOT DONE | NEW small PR Wed AM |
| Wire `fire_red_phone` caller in operator-api (after escalation) | NOT DONE | Same PR as above |
| Flip `INTELLIGENCE_SYSTEM_ROUTING=1` after smoke | NOT DONE | After wire-up + observation |
| Email channel adapter (transactional, NOT Gmail-DWD) | NOT BUILT | NEW small PR — use SendGrid free tier OR Cloud Run + SMTP relay through a no-DWD provider |
| In-platform notification channel adapter | NOT BUILT | NEW small PR — writes to a `notifications` collection consumed by the existing UI notification bell |
| `red_phone_config.channels` validation: only `email` + `in_platform` allowed in v0 | NOT BUILT | Same as adapter PR — add allowlist |
| FE channel-selector dropdown in red-phone config UI: SMS/Telegram/WhatsApp/Webhook DISABLED with tooltip "Coming soon — pending verification" | NOT BUILT | NEW small PR in gigaton-ui-system |
| Broken-path audit (8-item checklist above) | NOT RUN | Manual or scripted pass before merge to main + deploy |
| Resolve 5 conflict-blocked PRs (kept in branch for future channel rollout, NOT merged in this deployment) | BLOCKED | Defer to post-channel-verification phase |

**Important sequencing:** the 5 conflict-blocked channel PRs (red-phone #1 Sheet, #2 Telegram, #3 SMS + UAE #42/#43 + SIE #228) DO need resolution, but they ship in a SEPARATE deployment after each channel is independently verified. The next deployment intentionally ONLY includes email + in-platform + the no-broken-paths fixes.

## Sample messages by channel (for the 2 enabled channels)

### Email

- Subject: `[Red Phone] {urgency} — {short summary}`
- Body: emergency context (PII-redacted) + ACK link (`https://acks.{operator-brand-domain}/<token>`) + reply-to address
- From: a transactional sender address that doesn't need Workspace DWD (e.g. `notifications@gigaton.ai` via SendGrid)

### In-platform notification

- Appears in the Gigaton-UI notification bell
- Bell badge increments with red dot for urgency
- Clicking opens an in-app modal with the same content as email + an in-UI ACK button (no separate URL)
- Persists across sessions until ACKed

## How to apply

- ANY agent / PR author adding a new channel to red-phone: check this memory FIRST; ensure it is added as an option ONLY after the no-op state is impossible (credentials configured + adapter test-deployed against real endpoint + at least one synthetic event delivered end-to-end).
- ANY UI surface that exposes channel selection: read from a canonical `ENABLED_CHANNELS` server-side constant; never hardcode.
- ANY operator support ticket about "I configured SMS but didn't get the alert": first check that the channel was actually enabled in `ENABLED_CHANNELS`. If they configured it via a UI bug or stale FE, that's a regression in the gate.

## When this gate gets relaxed

Per channel, when ALL three are true:
1. Code adapter merged + deployed
2. Credentials provisioned + healthy (Secret Manager values valid, external service responsive)
3. End-to-end synthetic event delivered + ACKed successfully

Then add the channel to `ENABLED_CHANNELS` in a follow-up PR. Don't remove from this gate until that PR ships.
