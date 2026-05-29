# Influence vs Cost — Deep Dive (10-minute read)

This deep dive explains the **Influence vs Cost** model that Stage 8 turns on: what unit economics mean at this stage, how the credential paste pipeline keeps secrets safe, how Vertex AI IAM differs from other LLM credentials, and the edge cases that determine whether Stage 8 actually delivers profit visibility. It assumes you have read the `why_1min` and `what_3min` documents for Stage 8.

---

## 1. Unit economics — what unit, exactly

"Unit economics" at Stage 8 refers specifically to **cost-per-atomic-action**. That's the unit the manifest names in the `review-unit-economics` action description and that the Influence vs Cost dashboard renders against.

An **atomic action** is the smallest accountable platform operation that consumes resources. Examples:

- One LLM completion call to draft a message.
- One Stripe API call to query a balance.
- One Twilio SMS send.
- One persona-engine BFT-snapshot refresh.
- One decision-engine recommendation evaluation.

Each atomic action carries a cost in dollars, computed from:

- API cost (the provider's posted rate × the size of the call)
- Compute cost (the platform's own runtime cost to execute the call)
- Storage cost (any persistent artifact the action produces)
- Human-time cost (when a human is in the loop)

Stage 8's `review-unit-economics` action surfaces these per-atomic-action numbers and asks the operator to confirm or adjust. The decision-engine then uses cost-per-atomic-action as the cost side of every later projection.

The single-phrase answer to "what unit do unit economics refer to": **cost-per-atomic-action**.

## 2. The Influence vs Cost dashboard

The dashboard renders the operator's full action surface across two axes:

- **Influence** — Penrose-graded lift on the north star + supporting metrics per action class.
- **Cost** — actual cost-per-atomic-action × volume.

Each action class plots as a point. The diagonal (influence == cost) is the break-even line. Points above the line are net-profitable; points below are net-cost. The operator can:

- See which action classes are paying off and which aren't.
- Drill into per-class cost composition (API vs compute vs storage vs human time).
- See how cost-per-action has changed over time as the operator's usage evolved.
- Run what-if projections (drop this class, double that class) against Penrose.

The dashboard is the visible artifact of `tier_4_costs` closing. Before Stage 8, the dashboard is locked; after Stage 8, it's the operator's primary view of platform ROI.

## 3. Backfill — re-grading prior stages against actual cost

Stage 8 backfills unit economics **across all prior stages**. Mechanically:

- The decision-engine re-runs Penrose grading for every active recommendation, now with cost-per-atomic-action included.
- Recommendations that were previously surfaced (graded on lift alone) may be re-graded as net-negative and demoted.
- Action classes whose costs were under-estimated in fallback projections are adjusted upward.
- The operator's predicted-influence-to-date number is recomputed against actual cost.

Backfill is structurally important because the platform has been recommending against fallback costs since Stage 4. Without backfill, those Stage 4-7 recommendations remain mis-graded. Stage 8 corrects the record.

## 4. The credential paste pipeline — end-to-end masking

The credential paste affordance is the platform's primary credential-collection surface. Its security posture:

1. **Client-side capture.** The chat surface renders a masked input field. The value is captured into a sandboxed component that cannot be read by other chat components, by the LLM router, or by the conversation transcript renderer.
2. **TLS-only transit.** The value is sent over TLS to `gigaton-gateway /v1/connectors/credentials` with the operator's session JWT.
3. **Pre-storage probe.** The gateway runs the credential class's `probe` against the provider's API. The probe is a minimal-side-effect read call: list balances (Stripe), list reservations (OTAs), describe account (Twilio), smoke completion (LLM provider), etc. **The probe gates storage** — nothing lands in Secret Manager until it succeeds.
4. **Storage.** On probe success, the value is written to Google Secret Manager under the per-operator name pattern `<operator_id>--<provider>--<purpose>:latest`. The previous version (if any) is retained for rollback.
5. **Confirmation.** Gateway emits `ProviderCredentialRegistered` with `status=validated`. The chat surface confirms "credential stored" without ever re-rendering the value.

The masked value is **never echoed back, never logged in the transcript, never sent to the LLM router**. That triad is the verbatim safety guarantee from the manifest. The chat transcript that's archived to the operator's intelligence-silo bundle does NOT contain the credential; it contains a placeholder token `[CREDENTIAL_REGISTERED:<provider>]`.

## 5. Probe-before-storage — why the pattern matters

A credential that lands in Secret Manager without validation creates a class of silent failure: the credential might be malformed, expired, scoped wrong, or simply pasted from the wrong account. Weeks later, when the platform tries to use it, the failure surfaces as a runtime error far from the place the credential was entered.

The probe pattern eliminates that class. By validating against the provider's API before storage, malformed credentials are rejected at the moment of entry, with the operator in chat. The probe is class-specific:

- `llm_provider` → smoke completion call against the provider's standard completions endpoint.
- `payments` → list balances or test charge with $0 amount.
- `communications` → account describe / who-am-I call.
- `productivity` → workspace describe call.
- `source_code` → list-repos first page.
- `ota_booking` → list reservations last-30-days.
- `analytics` → account summary.
- `calendar_email` → list first page of relevant resource.
- `storage` → list root directory.
- `ai_image_video` → minimal render test.
- `custom` → generic store + retrieve roundtrip.

The probe is the gating step between paste and storage; nothing reaches Secret Manager without passing it.

## 6. Vertex AI IAM — the no-key exception

The `llm_provider` credential class has a documented exception: **Vertex AI Claude + Gemini use IAM (no key); only OpenAI + direct-API Anthropic/Gemini need keys.**

The reason: Vertex AI is Google Cloud's managed offering for Claude and Gemini. Authentication is via service-account IAM, not API key. The platform's gateway runs on Cloud Run with a service account that has Vertex AI invoke permissions; calls to Vertex-hosted models flow through the gateway's existing IAM identity. There is no per-operator API key to paste.

The orchestrator handles this transparently: when the operator inventories "Anthropic" or "Gemini," the orchestrator asks "Vertex AI (no key) or direct API (key required)?" — and routes the paste flow accordingly.

**False**: Vertex AI Claude + Gemini do NOT require an API key paste.

## 7. The per-operator Secret Manager naming pattern

Credentials are stored under: `<operator_id>--<provider>--<purpose>:latest`.

The three-segment name encodes:

- **`<operator_id>`** — the per-operator namespace. Cross-operator access is blocked at the IAM level (Secret Manager IAM bindings are per-operator).
- **`<provider>`** — the canonical provider name (e.g., `stripe`, `twilio`, `openai`, `vertex-ai`).
- **`<purpose>`** — the use-case for this credential. A single provider may have multiple credentials per operator (e.g., `stripe--read-only-ingest` and `stripe--live-payments`); the purpose disambiguates.
- **`:latest`** — the version tag. Secret Manager supports per-version rollback if a rotation goes wrong.

Storage target is verbatim: **"per-operator Secret Manager — name pattern: `<operator_id>--<provider>--<purpose>:latest`"**.

## 8. Billing connection — read-only by design

The `connect-billing` action explicitly requests **read-only** access. The platform never asks for write authority on payment rails because the platform doesn't move money on the operator's behalf at this stage — it ingests invoices and transactions, computes unit economics, and surfaces analysis.

The operational reason: read-only access has a dramatically smaller risk surface than write authority. Even a compromised platform credential cannot move funds; the worst case is read-side data exposure, mitigated by the per-operator namespacing already in place.

When tier_5_live unlocks (Stage 9), specific write authorities may be requested per use-case (e.g., Stripe payout creation for affiliate payouts). Each write authority is a separate consent, with explicit scope, validated by an axiom check.

## 9. Edge cases

- **Operator's billing connector breaks** (OAuth expired, bank requires re-auth). `BillingConnectorLost` fires; the operator is prompted to re-connect. Historical invoices stay; only new-period ingest pauses.
- **Credential rotation.** Operator pastes a new value in chat; the platform runs the probe; on success, Secret Manager versions the new value as `:latest` with the old as `:N-1`. Active engines pick up `:latest` within 60 seconds.
- **Operator wants to revoke a credential.** Supported via `/influence-vs-cost` UI: "Disable credential." The Secret Manager entry is preserved (for audit) but marked `enabled: false`; active engines stop using it within 60 seconds.
- **Provider's API changes.** The probe stops succeeding for new credentials of that class. A `CredentialClassProbeBroken` event fires platform-wide; the connector_catalog row is flagged for update; existing validated credentials continue working under the prior probe contract.
- **Operator below the 80% cost-coverage threshold.** Orchestrator surfaces "you've inventoried N tools but only M have unit-cost coverage — connect billing or register cost for these tools to advance Stage 8."

## 10. The relationship to Stage 9

Stage 9's `interactions_logged_count` and `drift_critical_count` both depend on cost-per-atomic-action being correct. A drift_critical regression often surfaces because actual cost diverges from the model's expected cost — Stage 8's data is what makes the model accurate enough to detect drift.

Stage 8 must close before Stage 9 opens (the manifest's `entry_signal: prior_stage_completed`). An operator who hits Stage 8 with thin cost coverage typically stalls in Stage 9 because Penrose's predictions are too noisy for the drift detector to surface real signal.

## 11. The PPIM signature, restated

- **interaction**: Influence vs Cost dashboard turns on
- **economics**: every later optimization graded by actual $ delta
- **predictability**: HIGH
- **brand_dimension**: financial integrity + transparency

"Financial integrity + transparency" is the operator-experience side of Stage 8. The operator sees, in dollars, what every action class is costing and producing. There's nowhere for cost to hide; there's nowhere for unprofitable action to hide. That visibility is what makes PPIM's "profitable" real.
