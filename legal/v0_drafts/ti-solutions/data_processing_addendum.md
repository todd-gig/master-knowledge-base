---
entity: Ti Solutions
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
> Ti Solutions' DPA has a distinguishing feature: Ti Solutions is **simultaneously processor (vis-à-vis Customer) and controller (vis-à-vis its own staff/sales-funnel data)**, and the Gigaton Platform is a **sub-processor** of Ti Solutions.

# Ti Solutions — Data Processing Addendum

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25

This Data Processing Addendum ("**DPA**") supplements the [Terms of Service](terms_of_service.md) and any MSA + SOW between Ti Solutions ("**Processor**") and Customer ("**Controller**"). It governs Ti Solutions' processing of personal data on Customer's behalf in the course of delivering the Services.

This DPA assumes Customer's processing is within the geographic scope defined in the [Terms of Service](terms_of_service.md) Section 2 (US + MX; EU/UK/EEA/CH excluded).

## 1. Definitions

Defined terms from the [Terms of Service](terms_of_service.md) apply. In addition:

- **"Personal Data"** — information relating to identifiable individuals processed by Ti Solutions on Customer's behalf, including Customer's contact lists, lead/prospect data, response data, employee/representative data, and any personal data within Customer Materials.
- **"Data Subjects"** — individuals to whom Personal Data relates (typically Customer's prospects, leads, contacts, employees).
- **"Sub-processor"** — third party engaged by Ti Solutions to process Personal Data on Customer's behalf, including (centrally) Gigaton AI.
- **"Data Protection Laws"** — same scope as Gigaton AI DPA Section 1.

## 2. Roles

- **Customer is the Controller**. Customer determines the purposes and means of processing.
- **Ti Solutions is the Processor**. Ti Solutions processes Personal Data only on documented instructions from Customer.
- **Gigaton AI is a Sub-processor** of Ti Solutions for substantially all technical processing.

## 3. Customer's Instructions and Responsibilities

### 3.1 Documented instructions

Customer's instructions are set forth in:

(a) These Terms and the [Terms of Service](terms_of_service.md);
(b) The applicable MSA and SOW;
(c) Customer-provided campaign briefs, target lists, copy approvals, and product descriptions;
(d) Customer's responses to in-engagement decision points (e.g., approval of message variants, approval of escalations).

### 3.2 Customer's responsibilities

Customer represents that:

(a) Customer is the Controller of all Personal Data and has a lawful basis for the processing;
(b) Customer has given all required notices to Data Subjects;
(c) Customer has obtained all required consents (TCPA, CAN-SPAM, LFPDPPP, REPEP, etc.) — see [Acceptable Use Policy](acceptable_use_policy.md) Section 1;
(d) Customer has the right to direct outreach to the individuals on the target list;
(e) Customer will not direct Ti Solutions to process Personal Data of Excluded Jurisdictions residents;
(f) Customer will respond to Data Subject rights requests directed at Customer and route only those requiring Ti Solutions' technical assistance to Ti Solutions.

## 4. Categories of Data Processed

### 4.1 Categories of Data Subjects

- **Customer's prospects and leads** — individuals targeted for outreach;
- **Customer's existing customers** — individuals communicated with for upsell, retention, support;
- **Customer's vendors / partners / channel** — individuals engaged for partner-program activity;
- **Customer's employees and representatives** — individuals administering the engagement on Customer's side.

### 4.2 Categories of Personal Data

- Identification: name, email, phone, role, company affiliation, LinkedIn URL;
- Communications data: messages drafted, sent, received, response classifications;
- Engagement metadata: open/click/reply timestamps, scoring outputs;
- Custom-fielded Customer-supplied data: industry, deal size, technology used, region, etc.;
- AI processing inputs and outputs;
- Meeting recordings / transcripts (where consent obtained — see Section 9).

### 4.3 Special categories

Ti Solutions does not knowingly process sensitive categories (health, biometrics, government-ID, race, religion, sexual orientation, criminal history) absent a specific Customer engagement that requires it, in which case a supplemental addendum and elevated controls are required. Customer must not submit sensitive data without prior written notice.

## 5. Sub-processors

### 5.1 Gigaton AI

Customer authorizes Ti Solutions to use **Gigaton AI** as the primary sub-processor for all technical processing. Gigaton's sub-processors (Stripe, Twilio, Anthropic, OpenAI, Google, GCP, Cloudflare) flow through to Customer's processing under the [Gigaton AI Data Processing Addendum](../gigaton-ai/data_processing_addendum.md), which is incorporated by reference.

### 5.2 Engagement-specific sub-processors

Customer authorizes Ti Solutions to engage additional sub-processors specific to the engagement, including but not limited to:

- **Dialer / contact-center platforms** (e.g., VCC Live, Vici Dial, Twilio Flex);
- **Data enrichment** (e.g., Clay, Apollo.io, ZoomInfo);
- **CRM platforms** (e.g., HubSpot, Salesforce — where engagement requires);
- **Document signing** (e.g., DocuSign — for Customer-counterparty contracts);
- **Project management** (e.g., ClickUp, Linear).

The specific sub-processors used in a Customer engagement are listed in **Annex A** and may be updated per Section 5.3.

### 5.3 New sub-processors

Ti Solutions will notify Customer at least **15 days** in advance of engaging a new sub-processor for an active engagement. Customer may object within the notice period; if Ti Solutions cannot reasonably accommodate the objection, Customer may terminate the affected engagement for material breach.

[PARALEGAL: 15 days is shorter than Gigaton's 30 days because managed-service engagements often require quicker tooling adjustments; confirm 15 days is acceptable.]

### 5.4 Sub-processor liability

Ti Solutions remains liable for sub-processors' acts and omissions to the same extent as if performing the processing itself.

## 6. AI Sub-processor Specific Commitments

Ti Solutions uses AI for content generation, lead scoring, classification, response drafting, and meeting summarization. AI Sub-processors include Anthropic, OpenAI, Google (via the Gigaton Platform).

Same commitments as Gigaton AI DPA Section 5:

(a) Commercial API tiers with no training opt-in;
(b) Customer Personal Data not used to train AI Subprocessor foundation models;
(c) Customer may request specific AI Subprocessor selection or exclusion;
(d) Customer acknowledges AI processing involves transmission of inputs to AI Subprocessor.

For meeting-recording AI / transcription specifically:

(e) Recording occurs only with explicit consent at session start (script provided);
(f) Transcripts and recordings stored encrypted; retention default 12 months from session;
(g) AI summarization of meetings runs against transcripts; outputs are Customer Confidential Information.

## 7. Security Measures

Ti Solutions inherits the security posture of the Gigaton Platform (described in [Gigaton AI DPA Annex B](../gigaton-ai/data_processing_addendum.md#annex-b--technical-and-organizational-security-measures-summary)). In addition, Ti Solutions personnel:

- access Customer data via least-privilege provisioning on the Gigaton Platform;
- complete annual privacy and security awareness training;
- operate under written confidentiality obligations;
- have access revoked promptly upon role change or off-boarding;
- never store Customer Data on personal devices or in personal cloud accounts.

For engagement-specific sub-processors (dialer, CRM), Ti Solutions configures appropriate access controls per the SOW.

## 8. Personal Data Incidents

If Ti Solutions becomes aware of an incident affecting Personal Data processed on Customer's behalf, Ti Solutions will:

(a) notify Customer **without undue delay and within 72 hours** of confirmation;
(b) provide information about nature, scope, likely consequences;
(c) cooperate with Customer's regulatory and Data Subject notification obligations;
(d) take reasonable steps to mitigate and prevent recurrence.

Notice goes to Customer's designated security/privacy contact (or, absent designation, the engagement primary contact).

## 9. Special Requirements for Telemarketing / Outbound Data

Where Ti Solutions executes outbound campaigns (SMS, voice, WhatsApp, email):

(a) Customer represents and warrants prior express consent / opt-in / lawful basis as required for the relevant channel;
(b) Ti Solutions maintains opt-out records and honors opt-outs across all channels and future engagements (a global opt-out under one engagement applies across the platform for that individual);
(c) Customer's contact-list provenance documentation may be requested by Ti Solutions and must be provided within 5 business days;
(d) Where Ti Solutions records calls (with consent), recordings are retained per SOW (default 12 months) then deleted.

## 10. Data Subject Rights

If a Data Subject directly contacts Ti Solutions with a rights request (access, deletion, opposition, ARCO), Ti Solutions will:

(a) acknowledge within 5 business days;
(b) forward to Customer (as Controller) within the same period;
(c) suspend further outreach to that Data Subject pending Customer's response;
(d) assist Customer in fulfilling the request to the extent technically required.

Ti Solutions will not respond substantively to such requests except to acknowledge and redirect.

## 11. Data Return and Deletion

Upon termination of the engagement:

(a) Customer may export Customer Data and Personal Data via Ti Solutions' assistance within a **30-day grace period** following the termination effective date;
(b) Ti Solutions deletes Personal Data from active systems within **60 days** of the termination effective date;
(c) Personal Data persisting in encrypted backups deleted on rotation (within 90 days);
(d) Retention required by law (litigation hold, regulatory investigation) is excepted, with continued confidentiality.

## 12. Audit Rights

Customer may request, no more than once per 12-month period, (a) a written summary of Ti Solutions' security and privacy posture, (b) the sub-processor list applicable to Customer's engagement, and (c) responses to Customer's reasonable written security questionnaire. On-premises audits are not generally available; an annual written attestation may be provided.

## 13. Cross-Border Transfers

US-based primary infrastructure; Mexico-resident Data Subjects' data may transfer to the US under the Gigaton Platform stack. Customer is responsible for disclosing this in Customer's own privacy notice and obtaining any consents required.

## 14. Liability

Liability provisions in the [Terms of Service](terms_of_service.md) Section 14 apply.

## 15. Term and Survival

This DPA is effective on the Effective Date and continues for the duration of the engagement. Sections 6, 7, 8, 10, 11, and 13 survive termination.

## 16. Order of Precedence

(1) MSA + SOW (custom), (2) this DPA, (3) [Terms of Service](terms_of_service.md), (4) Customer's signed proposal, (5) [Privacy Policy](privacy_policy.md), (6) [Acceptable Use Policy](acceptable_use_policy.md).

---

## Annex A — Sub-processors (current as of 2026-05-25, customizable per engagement)

### Always-on sub-processors

| Sub-processor | Category | Purpose |
|---|---|---|
| **Gigaton AI** | Platform | All technical processing |
| (Gigaton AI cascade — Stripe, Twilio, Anthropic, OpenAI, Google, GCP, Cloudflare — see Gigaton DPA Annex A) | | |

### Engagement-specific sub-processors (commonly used; selected per SOW)

| Sub-processor | Category | Typical purpose |
|---|---|---|
| Twilio Programmable Voice / Twilio Flex | Telephony | Outbound calling |
| Vici Dial / VCC Live | Telephony | Outbound calling, queue management |
| HubSpot | CRM | Pipeline tracking, contact sync |
| Salesforce | CRM | (if Customer prefers) |
| Apollo.io / Clay / ZoomInfo | Data enrichment | Lead enrichment |
| DocuSign | Document signing | Contract execution |
| ClickUp | Project management | Engagement workflow |
| Google Workspace | Productivity | Email, Drive |
| Slack | Communication | Customer collaboration |
| LinkedIn Sales Navigator | Lead sourcing | Customer-authorized prospecting |

[PARALEGAL: each engagement-specific sub-processor has its own DPA; confirm Ti Solutions executes the relevant sub-processor's DPA before use; recommend maintaining a current Sub-processor Registry per Customer.]

---

Annex B (security measures) incorporated by reference from [Gigaton AI Data Processing Addendum](../gigaton-ai/data_processing_addendum.md) Annex B.

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
