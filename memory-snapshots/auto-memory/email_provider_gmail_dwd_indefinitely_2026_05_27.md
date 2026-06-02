---
name: email_provider_gmail_dwd_indefinitely_2026_05_27
description: "Email provider doctrine reversal — Gigaton uses Google Mail (Workspace DWD via gmail-support-relay SA) indefinitely. Overrides prior \"NOT Gmail-DWD, use SendGrid\" guidance."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 943a8dc1-3984-4d2b-8bc3-e20e7dcc92d8
promoted_from: email_provider_gmail_dwd_indefinitely_2026_05_27.md
promoted_at: 2026-06-02T20:13:25Z
---

Todd directive 2026-05-27: **"sendgrid isnt being use, we are doing google mail indefinitely"**.

This **overrides** the prior guidance in:
- [[red_phone_v0_channels_gated_email_inplatform_only]] ("transactional, NOT Gmail-DWD — use SendGrid free tier OR Cloud Run + SMTP relay through a no-DWD provider")
- [[RESUME_HERE_2026_05_27_morning_red_phone_completion]] ("transactional, NOT Gmail-DWD, use SendGrid free tier or similar")

**Why (inferred):** avoids introducing another vendor/account/key; the Workspace + `gmail-support-relay@gigaton-platform.iam.gserviceaccount.com` SA are already provisioned, and Matt is already on the DWD configuration task (P3 in the resume doc) — so finishing what's started rather than forking to SendGrid.

**How to apply:**
- Email adapters (red-phone, future operator outreach, etc.) use **Gmail API + Workspace Domain-Wide Delegation** via `gmail-support-relay@gigaton-platform.iam.gserviceaccount.com`, impersonating a sender mailbox (default `notifications@gigaton.ai`).
- Scope: `https://www.googleapis.com/auth/gmail.send`.
- "Indefinitely" — do not propose SendGrid/Mailgun/SES/etc. swap-outs without an explicit Todd directive that supersedes this one.
- Workspace admin DWD config (Matt action) is the gating dependency for any email-channel exposure. Until that lands, adapters must degrade cleanly to `error_code="dwd_not_configured"`, never crash.
- Bulk-send caps: Gmail caps are lower than transactional providers (~2k/day per Workspace user). If volume becomes the binding constraint later, surface that to Todd before swapping providers; don't silently swap.
