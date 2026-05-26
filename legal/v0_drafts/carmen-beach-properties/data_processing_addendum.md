---
entity: Carmen Beach Properties
doc_type: data_processing_addendum
version: v0-draft-2026-05-25
status: PENDING-PARALEGAL-REVIEW
effective_date: 2026-05-26
applicable_jurisdictions: [US, MX]
excluded_jurisdictions: [EU, UK]
last_reviewed: 2026-05-25
contact: privacy@gigaton.ai
related_docs:
  - terms_of_service.md
  - privacy_policy.md
  - acceptable_use_policy.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> Carmen Beach Properties' DPA covers two parallel relationships:
> 1. **Carmen Beach (controller) → Gigaton AI (processor)** — Gigaton processes Guest/Owner personal data on Carmen Beach's behalf. This is incorporated by reference to Gigaton AI's [Data Processing Addendum](../gigaton-ai/data_processing_addendum.md).
> 2. **Carmen Beach (controller) → Owner / OTA partners (joint or independent)** — describes how Carmen Beach treats Owner data and OTA-sourced Guest data.
>
> This document does NOT create a separate controller-processor relationship between Carmen Beach and Guests (Guests are Data Subjects, not controllers/processors).

# Carmen Beach Properties — Data Processing Addendum

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25

This Data Processing Addendum ("**DPA**") supplements the [Terms of Service](terms_of_service.md) and the [Privacy Policy](privacy_policy.md). It documents how Carmen Beach Properties handles personal data in its capacity as controller, and how the Gigaton AI processor relationship and OTA partnerships flow through.

## 1. Controller-Processor Architecture

```
Guest / Owner / Visitor (Data Subject)
        │
        ▼
Carmen Beach Properties  ←—— CONTROLLER (legal entity, determines purposes + means)
        │
        ▼
Gigaton AI (operates the platform)  ←—— PROCESSOR
        │
        ▼
Gigaton's sub-processors:
        ├── Stripe (payment data — PCI-DSS scope held by Stripe)
        ├── Twilio (SMS + WhatsApp messaging)
        ├── Anthropic / OpenAI / Google (AI inference — content + decisioning)
        ├── Google Cloud Platform (hosting, storage, encryption)
        └── Cloudflare (CDN, DNS, DDoS, edge security)
        ▼
Independent third parties Carmen Beach engages directly:
        ├── OTAs (Airbnb, Vrbo, Booking.com) — separate controllers when they capture booking via their own platform
        ├── Cleaning / maintenance contractors — independent businesses, limited-purpose recipients
        ├── Local government (SAT for tax, municipal STR registration) — legal-obligation recipients
        └── Insurance carriers — separate controllers for claims
```

## 2. Carmen Beach as Controller — Statutory Basis

Carmen Beach is the **controller** of personal data of Guests, Owners, prospects, and website visitors under:

- **California CCPA/CPRA** — Carmen Beach is the "business" collecting personal information from California-resident consumers.
- **Mexican LFPDPPP** — Carmen Beach is the "responsable" (controller) under Art. 3(XIV).

Carmen Beach determines the purposes and means of processing as set forth in the [Privacy Policy](privacy_policy.md).

## 3. Gigaton AI as Carmen Beach's Processor

### 3.1 Relationship

Carmen Beach engages Gigaton AI as its data processor for substantially all data-processing activity supporting the Services. The terms governing this relationship are set forth in:

(a) The [Gigaton AI Data Processing Addendum](../gigaton-ai/data_processing_addendum.md), accepted by Carmen Beach as part of Carmen Beach's tenancy on the Gigaton platform; and
(b) The customer-specific addendum between Carmen Beach (as Gigaton customer / controller) and Gigaton AI (as processor), executed separately as Carmen Beach's signed copy of the standard Gigaton DPA.

Sections 4 (Sub-processors), 5 (AI Subprocessor commitments), 6 (Security measures), 7 (Incident notification), and 8 (Data return and deletion) of the Gigaton DPA are **incorporated by reference** here and apply to all Personal Data Carmen Beach submits to or generates on the Gigaton platform.

### 3.2 Categories of Data Subjects (Gigaton processing on behalf of Carmen Beach)

- **Guests** — past, current, prospective; including booking-inquiry Guests who never complete a booking;
- **Owners** — past, current, prospective;
- **Visitors** — anonymous and identified;
- **Contractors and staff** — cleaning, maintenance, concierge personnel where their data flows through the platform.

### 3.3 Categories of Personal Data processed by Gigaton on Carmen Beach's behalf

Per Section 3.2 of the Gigaton DPA, augmented by Carmen Beach-specific data:

- Identification: name, email, phone, billing address;
- Booking + transaction: dates, properties, prices, payment status, refund history;
- Payment: cardholder info (limited fields; full PCI scope at Stripe);
- Government-ID images (where collected for STR compliance — sensitive category, enhanced protection);
- Communications: WhatsApp, email, in-app chat;
- OAuth tokens for connected Google/Microsoft/etc. accounts (Owners) — references stored in Gigaton Secret Manager;
- Behavioral telemetry: site usage, concierge interaction patterns;
- AI processing inputs and outputs.

### 3.4 Special note on sensitive data (government IDs)

Where Mexican STR regulations require collection of government-issued ID, Carmen Beach instructs Gigaton to:

(a) capture the ID via a secure upload flow;
(b) store the image in encrypted object storage with restricted access;
(c) retain only as long as required by applicable law (typically ≤ 1 year);
(d) auto-purge per a scheduled deletion job;
(e) not transmit the image to AI Subprocessors (Anthropic, OpenAI, Google) absent a specific business need that Carmen Beach has approved in writing.

[PARALEGAL: confirm the legal basis for sensitive-data collection (STR regulation citation; if no statutory requirement, recommend NOT collecting); document the auto-purge job in operational runbook.]

## 4. OTA Partnerships — Independent Controllers

For Guests who book via Airbnb, Vrbo, Booking.com, or other OTAs:

- Each OTA is an **independent controller** for the data it collects directly from the Guest under the OTA's own terms.
- The OTA shares with Carmen Beach the data necessary to fulfill the booking (typically name, dates, contact info, booking reference) — that shared data, once received by Carmen Beach, becomes Carmen Beach Personal Data, processed under this DPA.
- Carmen Beach does not control the OTA's pre-share processing of the Guest data.

[PARALEGAL: confirm characterization is correct under CCPA / LFPDPPP — there are arguments that OTAs and accommodation providers are **joint controllers** for some processing (e.g., booking-fulfillment); document the Air Force / Booking-Holdings / Vrbo data-sharing model and consider whether a joint-controllership note is needed.]

## 5. Contractor and Service-Provider Engagements

Carmen Beach engages cleaning, maintenance, security, concierge, transportation, and similar contractors who may receive limited personal data necessary for the engagement (e.g., Guest name + check-in/out times + access code, no payment data).

Where a contractor processes personal data substantially on Carmen Beach's behalf (not for the contractor's own purposes), Carmen Beach will execute a written data-protection agreement requiring (a) confidentiality, (b) purpose limitation, (c) appropriate security, and (d) return or deletion upon completion of the engagement.

[PARALEGAL: confirm whether a Mexican `cláusula de confidencialidad` is sufficient or whether a fuller LFPDPPP-compliant `convenio de transferencia` is required for each contractor; recommend a one-page contractor DPA template.]

## 6. Owner-Specific Data Processing

For Owners, Carmen Beach processes:

(a) Owner identification and tax data (name, RFC, bank/SPEI details);
(b) Property information (location, photos, inventory, permits);
(c) Booking outcomes attributed to the Owner's Property;
(d) Communications between Carmen Beach and the Owner;
(e) Payout history.

Owner data is shared with Stripe (payment infrastructure), SAT/IRS (tax reporting where required), and within Carmen Beach + Gigaton operations.

Owner has the right to receive a complete data export upon PMA termination, within 30 days of request.

## 7. Data Subject Rights Coordination

Data Subjects (Guests, Owners, visitors) may exercise rights described in the [Privacy Policy](privacy_policy.md) directly with Carmen Beach. Carmen Beach will:

- respond directly to all rights requests (no rerouting to Gigaton);
- engage Gigaton via the Gigaton DPA Section 8.1 for the technical assistance needed to fulfill the request (e.g., data export, record deletion, opt-out propagation across the connector stack);
- maintain a register of rights requests and outcomes.

## 8. Incident Coordination

Personal-data incidents are coordinated as follows:

- If Carmen Beach discovers an incident first (e.g., a contractor breach), Carmen Beach assesses, contains, and notifies regulators/Data Subjects per applicable law, and informs Gigaton if any cross-platform implications exist.
- If Gigaton discovers an incident affecting Carmen Beach's data, Gigaton notifies Carmen Beach per Section 7 of the Gigaton DPA (within 72 hours), and Carmen Beach is responsible for downstream Data Subject and regulator notifications.

Both parties cooperate in incident investigation, root-cause analysis, and corrective action.

## 9. Cross-Border Transfers

Carmen Beach is a Mexican operation; the underlying platform infrastructure is in the United States. By using the Services, Guests and Owners consent to the cross-border transfer of their personal data to the United States, as disclosed in the [Privacy Policy](privacy_policy.md) Section 9. For Owners, additional cross-border-transfer disclosures may apply where the Owner's primary residence is outside Mexico.

## 10. Audit Rights

Owners may request, no more than once per 12-month period, a summary of (a) data Carmen Beach holds about the Owner and the Owner's Property, (b) sub-processors engaged in the Owner's data processing, and (c) security measures applicable to the Owner's data. Carmen Beach will respond within 30 days. On-premises audits are not generally available; Carmen Beach may provide responses to a written security questionnaire as a substitute.

## 11. Term, Survival

This DPA is effective on the Effective Date and remains in force as long as Carmen Beach processes personal data of the Data Subject. Sections 3, 7, 8, and 9 survive termination.

## 12. Order of Precedence

In case of conflict regarding data processing: (1) this DPA, (2) the [Terms of Service](terms_of_service.md), (3) the Owner's PMA (Owner relationships), (4) the [Privacy Policy](privacy_policy.md), (5) the [Acceptable Use Policy](acceptable_use_policy.md).

---

## Annex A — Sub-processor Chain Reference

| Tier | Party | Role |
|---|---|---|
| 1 | Carmen Beach Properties | Controller |
| 2 | Gigaton AI | Processor |
| 3 | Google Cloud Platform | Sub-processor — hosting / storage / encryption |
| 3 | Cloudflare | Sub-processor — CDN / DNS / DDoS |
| 3 | Stripe | Sub-processor — payment processing + Stripe Tax |
| 3 | Twilio | Sub-processor — SMS / WhatsApp |
| 3 | Anthropic | Sub-processor — AI inference |
| 3 | OpenAI | Sub-processor — AI inference |
| 3 | Google (Gemini) | Sub-processor — AI inference |
| Independent | Airbnb / Vrbo / Booking.com | Independent controller (OTA booking funnel) |
| Independent | Cleaning / maintenance contractors | Limited-purpose recipients under contractor DPA |
| Independent | SAT / IRS / municipal STR registry | Legal-obligation recipients |
| Independent | Property insurance carriers | Independent controllers (claims) |

Annex B (security measures) is incorporated by reference from the Gigaton AI [Data Processing Addendum](../gigaton-ai/data_processing_addendum.md) Annex B.

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
