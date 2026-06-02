# What you'll do in Stage 8 — Tech Stack + Costs (3-minute walkthrough)

Stage 8 is owned by the **intelligence-silo**. Secondary engine is **gigaton-gateway** (it routes credential validation calls). Stage 8 consists of **four actions**:

1. `inventory-tools`
2. `connect-billing`
3. `register-provider-credentials`
4. `review-unit-economics`

## Action 1 — `inventory-tools`

You inventory every 3rd-party tool the operator pays for: Stripe, Twilio, Anthropic, Google, OTAs, Slack, the long tail. The catalog seed pre-fills common tools so the operator confirms instead of starting from a blank page.

The chat affordance is `inline_form`. Each addition emits `ToolInventoried`. The action auto-completes after `min_count: 5` — typically operators have far more than 5.

## Action 2 — `connect-billing`

You connect billing sources — Stripe, your bank, your accounting (QuickBooks / Xero). The OAuth or API-key flow runs inline in chat.

**The connection requests read-only access** — that's the verbatim manifest description. No write authority is requested; the platform ingests invoices and transactions but cannot move money. The action emits `BillingConnectorEstablished` and auto-completes after `min_count: 1`.

## Action 3 — `register-provider-credentials`

For each inventoried tool, the orchestrator walks you through providing the credential inline in chat. The platform knows how to handle a wide universe of **credential classes**:

- **`llm_provider`** — OpenAI, Anthropic direct, Gemini direct, Vertex AI IAM. Note: Vertex AI Claude + Gemini use IAM attestation, not an API key. **False**: Vertex AI Claude + Gemini do NOT still require an API key paste.
- **payments** — Stripe, PayPal, Square, QuickBooks. OAuth flow or API key paste.
- **communications** — Twilio, SendGrid, Mailchimp, Slack, Mailgun, Postmark.
- **productivity** — Notion, ClickUp, Asana, Linear, Monday, Airtable.
- **source_code** — GitHub PAT, GitLab token, Bitbucket app password.
- **ota_booking** — Airbnb iCal, VRBO iCal, Booking.com iCal, Hospitable, Hostaway.
- **analytics** — GA4 service account, HubSpot, Mixpanel, Segment.
- **calendar_email** — Gmail OAuth, Google Calendar OAuth, Outlook OAuth, iCloud app password.
- **storage** — Google Drive OAuth (already collected in Stage 1), Dropbox, OneDrive, S3 IAM key.
- **ai_image_video** — OpenAI DALL-E, Gemini Omni, Runway, ElevenLabs, Vapi.
- **custom** — any provider not in the canonical list.

`llm_provider` is one of the credential classes — that is verbatim per manifest.

Each credential class declares a `probe` field — a validation call the gateway runs against the provider's API before storing the credential. **The probe gates storage**: nothing lands in Secret Manager until the probe succeeds. Bad credentials are rejected at validation time, not surfaced as runtime errors weeks later.

The credential paste affordance is masked end-to-end: values are captured client-side, sent via TLS to gateway `/v1/connectors/credentials` with the operator's session JWT, validated against the provider's API, then stored. The masked input is **never echoed back, never logged in the transcript, never sent to the LLM router**.

Storage target is verbatim: **"per-operator Secret Manager — name pattern: `<operator_id>--<provider>--<purpose>:latest`"**. Per-operator namespaces ensure no cross-operator visibility.

Each successful registration emits `ProviderCredentialRegistered` with `status=validated`. The action auto-completes when every inventoried tool that requires a credential has a validated event — the manifest expresses this as `min_count_predicate: all_credentialed_inventoried_tools`.

## Action 4 — `review-unit-economics`

After billing + credentials are in, intelligence-silo computes **cost-per-atomic-action** across all prior stages. The operator reviews and adjusts where the auto-categorization missed. The chat affordance is `confirmation_only` (a panel with reviewable line items + an Acknowledge button).

`UnitEconomicsReviewed` fires on acknowledge. The action auto-completes on first emit.

## The activation gate

`GET {intel_silo_base}/v1/operators/{operator_id}/cost-coverage` with predicate:

```
all_of:
  - $.tools_with_unit_cost_pct >= 80
  - $.invoice_days_ingested >= 90
```

**X = 80, Y = 90.** Both must hold.

## Events emitted

- `StageStarted`
- `ToolInventoried`
- `BillingConnectorEstablished`
- `ProviderCredentialRegistered`
- `UnitEconomicsReviewed`
- `StageCompleted`

## What unlocks at completion

Stage 8 **closes `tier_4_costs`**. The full **Influence vs Cost dashboard turns on** — that's the visible artifact. The `influence-cost` nav circle illuminates.

## Streak eligibility

Stage 8 is **not streak-eligible**. Cost connectors are configured once and re-validated when credentials rotate. The badge slug is `economics-illuminated`.

## Predicted outcomes

Fallback predicted influence is **$38,000**. The PPIM signature notes that every later optimization is now graded by actual $ delta — the influence vs cost ratio.
