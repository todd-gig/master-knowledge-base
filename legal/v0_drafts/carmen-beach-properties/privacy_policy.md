---
entity: Carmen Beach Properties
doc_type: privacy_policy
version: v0-draft-2026-05-25
status: PENDING-PARALEGAL-REVIEW
effective_date: 2026-05-26
applicable_jurisdictions: [US, MX]
excluded_jurisdictions: [EU, UK]
last_reviewed: 2026-05-25
contact: privacy@gigaton.ai
related_docs:
  - terms_of_service.md
  - acceptable_use_policy.md
  - data_processing_addendum.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> Bilingual EN/ES requirement for Mexican B2C guest relationships — `[PARALEGAL: …]` markers flag Mexican LFPDPPP-specific items.

# Carmen Beach Properties — Privacy Policy

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25
**Controller:** Carmen Beach Properties ("**Carmen Beach**," "**we**," "**us**," "**our**")
**Domain:** carmenbeach.com
**Contact:** privacy@gigaton.ai (TODO: confirm a `privacy@carmenbeach.com` alias)

This Privacy Policy describes how Carmen Beach Properties collects, uses, discloses, and protects personal information when you visit `carmenbeach.com`, book a stay, communicate with our concierge, or otherwise interact with our Services (defined in the [Terms of Service](terms_of_service.md)). It applies to **Guests** and **Owners**, and (where context requires) to general website visitors.

This Policy is also intended to serve as Carmen Beach's **Aviso de Privacidad Integral** under the Mexican LFPDPPP. A short-form Spanish-language notice (*aviso simplificado*) is available at `carmenbeach.com/legal/aviso-es` (TODO: build).

---

## 1. Geographic Scope

Carmen Beach offers Services to Guests located in **the United States, Canada, Mexico, and Latin America** and to Owners of property in **Mexico (Quintana Roo and adjacent states)**. We do not knowingly accept bookings from, market to, or process payments from residents of the **European Union, European Economic Area, United Kingdom, or Switzerland** during our v1 beta period (the "**Excluded Jurisdictions**"). If you reside in an Excluded Jurisdiction, please do not use the Services.

[PARALEGAL: see ToS Section 2 cross-reference; same EU-exclusion caveat applies.]

This Policy is designed to comply with:
- **California Consumer Privacy Act / California Privacy Rights Act (CCPA/CPRA)** — U.S. baseline (Section 7);
- **Mexico LFPDPPP** and its Regulations — for all Mexico-resident Guests and Owners (Section 8).

## 2. Carmen Beach uses Gigaton AI as a sub-processor

Carmen Beach operates on the **Gigaton AI** platform. This means:

- The website, owner portal, payment processing, WhatsApp concierge, calendar sync, and analytics all run on Gigaton AI infrastructure.
- **Carmen Beach is the controller** of personal information collected about you.
- **Gigaton AI is the processor** acting on Carmen Beach's behalf, under the [Data Processing Addendum](data_processing_addendum.md) between Carmen Beach and Gigaton AI.
- **Gigaton AI's sub-processors** (Stripe for payments, Twilio for SMS/WhatsApp, Anthropic/OpenAI/Google for AI, Google Cloud Platform for hosting, Cloudflare for security) are listed at `gigaton.ai/legal/subprocessors` (TODO: build).

If you have questions about how data flows through this stack, contact `privacy@gigaton.ai` (TODO: confirm).

## 3. What Personal Information We Collect

### 3.1 From Guests

- **Booking data**: name, email, phone, billing address, dates of Stay, guest count, special requests.
- **Payment data**: cardholder name, billing address, card last-4 + expiry + brand (full card data collected and stored by Stripe; we never receive the full PAN).
- **Identification data**: passport / government-ID image where required for check-in (Mexican STR regulations may require this; if collected, treated as sensitive and retained only as long as required by law).
- **Communications**: messages exchanged via WhatsApp, email, or in-app chat; call logs (if any).
- **Stay metadata**: check-in/check-out timestamps, key/lock events (if smart-lock equipped), in-stay support requests.

### 3.2 From Owners

- **Account data**: name, email, phone, RFC (Mexican tax ID), legal entity, bank/SPEI details for payouts.
- **Property data**: inventory list, photos, pricing, calendar, condo/HOA approvals.
- **Insurance and permits**: insurance certificates, STR permits, condo association documents.

### 3.3 From everyone (automatically)

- IP address, browser, device type, referrer, pages viewed (server logs + analytics);
- Cookies and similar technologies (see Section 12);
- Location of device at the time of booking (only if you have enabled location services).

### 3.4 From OTAs (for Guests who booked via an OTA channel)

When you book via Airbnb, Vrbo, Booking.com, or another OTA, we receive the Guest data that the OTA shares with us under the OTA's own terms — typically name, dates, booking reference, sometimes contact information.

### 3.5 Sensitive personal information

We may collect **government-ID images** for check-in compliance with Mexican STR regulations. We do not knowingly collect health information, biometric identifiers, precise geolocation beyond device-level, race/ethnicity, religion, or other sensitive categories. If you submit sensitive information in a free-text field, we will treat it under enhanced confidentiality but cannot affirmatively prevent collection.

[PARALEGAL: confirm whether Quintana Roo / federal SAT regulations actually require ID collection from STR guests; if yes, document the legal basis (legal obligation), retention period, and access controls; if no, recommend removing this collection to reduce scope.]

## 4. How We Use Personal Information

| Purpose | Source data | Lawful basis (US) | Lawful basis (MX LFPDPPP) |
|---|---|---|---|
| Process bookings and payments | Guest data | Contract performance | Contractual necessity (Art. 10) |
| Communicate with you (pre, during, post-Stay) | Contact + communications data | Contract performance / legitimate interest | Contractual necessity |
| Operate properties (cleaning, maintenance, check-in) | Booking + Stay data | Contract performance | Contractual necessity |
| Owner reporting and payout | Owner + booking data | Contract performance | Contractual necessity |
| Tax reporting (IVA, ISH, SAT, US 1099 if applicable) | Booking + Owner data | Legal obligation | Legal obligation |
| Comply with STR / safety / ID-check regulations | Government-ID data | Legal obligation | Legal obligation |
| Resolve disputes and damage claims | Stay + photo + payment data | Legitimate interest | Legitimate interest |
| Marketing communications (opt-out available) | Contact data | Consent / legitimate interest | Consent (opt-out for secondary purposes) |
| Improve the Services (aggregate analytics) | Behavioral data | Legitimate interest | Legitimate purpose; consent for non-essential |
| Detect fraud, abuse, security incidents | All categories | Legitimate interest | Legitimate purpose |

[PARALEGAL: LFPDPPP requires distinguishing primary purposes (no opt-out) from secondary purposes (opt-out required). Confirm classification above — marketing, analytics for product improvement, and aggregate trend analysis are secondary purposes requiring opt-out.]

## 5. AI Processing Disclosure

The Services use AI (via Gigaton AI's platform) for:

(a) WhatsApp concierge bot — drafting replies to Guest inquiries (a human reviews / takes over for non-routine matters);
(b) Pricing recommendations and dynamic-pricing decisions;
(c) Booking-fit scoring (assessing whether a booking inquiry matches the Property type);
(d) Review summarization and operational analytics;
(e) Marketing-page content generation.

When you interact with our WhatsApp concierge, you will see an opening disclosure that the channel is AI-assisted and human-escalation is available on request. Decisions that materially affect Guests (e.g., booking refusal, refund decisions) are reviewed by a human before being communicated.

You may opt out of AI-driven communications by replying "human" in WhatsApp or by emailing `concierge@carmenbeach.com` (TODO: confirm). Some response-time advantages may be reduced.

[PARALEGAL: see AI disclosure paragraph in Gigaton AI Privacy Policy Section 8; same emerging-norm considerations apply (Colorado AI Act, CA ADMT regs).]

## 6. How We Share Personal Information

| Recipient category | Purpose |
|---|---|
| **Gigaton AI (sub-processor)** | All Services operations (Section 2) |
| **Stripe** | Payment processing, billing, tax |
| **Twilio (WhatsApp Business)** | Concierge messaging |
| **OTAs (Airbnb, Vrbo, Booking.com)** | Booking distribution and reconciliation (Guest already has a relationship with the OTA) |
| **Property cleaning, maintenance, security contractors** | Operational coordination — limited to what is necessary (e.g., arrival times, access codes), under confidentiality |
| **Owners** | Aggregate booking data for the Owner's property; specific Guest details only as necessary (e.g., for a damage claim) |
| **Tax authorities (SAT, IRS where applicable)** | Tax reporting obligations |
| **Legal/regulatory** | Compliance with subpoena, court order, government request, or to protect rights and safety |
| **Insurers** | Damage / personal-injury claims under Property insurance |
| **Successors in interest** | In the event of a merger, sale, or reorganization of Carmen Beach or Gigaton AI |

We do **not** sell or share personal information for cross-context behavioral advertising as defined under CPRA, nor do we engage in adtech retargeting on `carmenbeach.com`.

## 7. California Residents (CCPA / CPRA)

Same rights described in Gigaton AI's Privacy Policy Section 6 apply to California-resident Guests and Owners:

- Right to know;
- Right to delete;
- Right to correct;
- Right to opt out of sale/sharing (we do neither);
- Right to limit sensitive personal information use;
- Right to non-discrimination.

To exercise rights, email `privacy@gigaton.ai` (TODO: confirm) from the email associated with your booking or Owner account.

## 8. Mexico Residents (LFPDPPP)

### 8.1 ARCO Rights

You have the right to **Access**, **Rectification**, **Cancellation**, and **Opposition** (ARCO Rights) regarding your personal data, and the right to **revoke consent** and to **limit use and disclosure**.

To exercise ARCO Rights, send a written request to `privacy@gigaton.ai` (TODO: confirm) including:
- Your name and contact information;
- Documentation proving your identity (or a legal representative's authorization);
- A clear description of the right being exercised and the data concerned.

We will respond within **20 business days** and implement granted requests within **15 business days** thereafter.

You may also file a complaint with the **Instituto Nacional de Transparencia, Acceso a la Información y Protección de Datos Personales (INAI)**: [home.inai.org.mx](https://home.inai.org.mx).

### 8.2 Designated representative

[PARALEGAL: confirm whether LFPDPPP requires a designated privacy department / officer for an entity of Carmen Beach's size; if so, insert role + contact.]

### 8.3 Identification of the controller

**Controller:** Carmen Beach Properties
**Domicile:** [PARALEGAL: insert Mexican domicile address — required for LFPDPPP aviso]
**Contact:** privacy@gigaton.ai (TODO: confirm dedicated MX privacy alias)

### 8.4 Primary vs. secondary purposes

Primary purposes (no opt-out): processing bookings, payments, tax reporting, STR-regulation compliance, dispute resolution.

Secondary purposes (opt-out via `privacy@gigaton.ai`): marketing, aggregate analytics for product improvement, customer satisfaction surveys.

[PARALEGAL: confirm primary/secondary classification meets LFPDPPP Art. 16 + 17 requirements; recommend a one-click opt-out mechanism per Reglamento.]

## 9. International Data Transfers

When you use the Services, your personal data is transferred to and processed in the **United States** (Gigaton AI infrastructure on Google Cloud `us-central1`). For Mexico-resident Data Subjects, this is a cross-border transfer disclosed under LFPDPPP Art. 36. By using the Services, you acknowledge and consent to this transfer.

## 10. Data Retention

| Data | Retention |
|---|---|
| Booking records | 5 years post-Stay (Mexican SAT + US tax) |
| Payment records | 7 years (US accounting / Mexican SAT) |
| Government-ID images (if collected) | Per STR-regulation requirement (typically ≤ 1 year), then deleted |
| Communications (WhatsApp, email) | 24 months post-last-contact |
| Marketing-opt-in records | Until opt-out + reasonable suppression list |
| Owner records | Duration of PMA + 7 years (tax/audit) |
| Backups | Up to 90 days encrypted; deleted on rotation |

After applicable retention periods, data is deleted or anonymized.

## 11. Data Security

We rely on Gigaton AI's security infrastructure (TLS, KMS encryption, RBAC, MFA, audit logging — see Gigaton AI [Data Processing Addendum](data_processing_addendum.md) Annex B). For physical operations (key handoff, on-site contractors), we use need-to-know access codes and rotate them between Stays.

If you have reason to believe your account or Stay data has been compromised, contact `security@gigaton.ai` (TODO: confirm).

## 12. Cookies and Similar Technologies

We use cookies to:

- maintain authenticated sessions (essential);
- remember language preference and search filters (functional);
- measure aggregate site usage (analytics — opt-in where required);
- detect and prevent fraud and abuse (security).

A cookie banner is shown on first visit. We do not use third-party advertising cookies.

[PARALEGAL: confirm cookie disclosure meets LFPDPPP secondary-purpose requirements + CCPA "Do Not Sell" link.]

## 13. Breach Notification

If we determine that an incident has resulted in unauthorized access to or disclosure of personal information, we will notify affected Guests and Owners without undue delay, consistent with Cal. Civ. Code §1798.82 (California), LFPDPPP Art. 20 (Mexico), and other applicable state statutes.

## 14. Children's Privacy

The Services are not directed to children under 18, and we do not knowingly collect data from individuals under 18 except as part of a family booking made by an adult guardian, where the only data collected about minors is name and headcount (for occupancy limits and safety).

## 15. Changes to this Policy

Material changes will be communicated at least 30 days in advance by email to active Guests and Owners. Continued use after the effective date is acceptance.

## 16. Contact

Privacy inquiries: `privacy@gigaton.ai` (TODO: confirm dedicated `privacy@carmenbeach.com` alias)
Concierge: `concierge@carmenbeach.com` (TODO: confirm)
Mexican domicile: [PARALEGAL: insert]
INAI complaint procedure: [home.inai.org.mx](https://home.inai.org.mx)

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
