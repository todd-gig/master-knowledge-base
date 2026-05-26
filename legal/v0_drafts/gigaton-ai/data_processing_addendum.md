---
entity: Gigaton AI
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

# Gigaton AI — Data Processing Addendum

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25

This Data Processing Addendum ("**DPA**") supplements the [Terms of Service](terms_of_service.md) entered into between **Gigaton AI** ("**Processor**," "**Gigaton**") and **Customer** ("**Controller**"). This DPA governs Gigaton's processing of personal data on Customer's behalf in connection with Customer's use of the Service.

This DPA is offered as Gigaton's standard processor-side terms. By accepting the Terms of Service and using the Service, Customer accepts this DPA where applicable to Customer's processing. Customer may execute a counter-signed copy on request to `privacy@gigaton.ai` (TODO: confirm).

## 1. Definitions

Terms defined in the [Terms of Service](terms_of_service.md) have the same meanings here. In addition:

- **"Personal Data"** means any information relating to an identified or identifiable natural person that Customer (as Controller) submits to or generates within the Service.
- **"Data Subject"** means the identified or identifiable individual to whom Personal Data relates (typically the Customer's End Users — guests, prospects, employees, contacts, etc.).
- **"Processing"** means any operation performed on Personal Data, including collection, recording, organization, storage, retrieval, use, disclosure, or deletion.
- **"Sub-processor"** means any third party engaged by Gigaton to process Personal Data on behalf of Customer.
- **"Data Protection Laws"** means the privacy and data-protection laws applicable to the parties' processing, including without limitation:
  - **United States:** California Consumer Privacy Act / California Privacy Rights Act ("CCPA/CPRA"); Virginia Consumer Data Protection Act; Colorado Privacy Act; Connecticut CTDPA; Utah UCPA; Texas TDPSA; HIPAA (only where Customer is a covered entity and a separate BAA is executed); other applicable U.S. state laws.
  - **Mexico:** Ley Federal de Protección de Datos Personales en Posesión de los Particulares ("LFPDPPP") and its Regulations.
- **"Excluded Jurisdictions"** has the meaning given in the Terms of Service Section 2 (EU, EEA, UK, Switzerland) — out of scope for this v1 beta DPA.

[PARALEGAL: confirm definitions align with each statute's actual term-of-art (e.g., CCPA uses "service provider" rather than "processor"; LFPDPPP uses "encargado").]

## 2. Roles and scope

### 2.1 Roles

- **Customer is the Controller** of Personal Data processed via the Service. Customer determines the purposes and means of processing.
- **Gigaton is the Processor** (CCPA: "service provider"; LFPDPPP: "encargado"). Gigaton processes Personal Data only on documented instructions from Customer.

### 2.2 Customer's instructions

Customer's instructions for processing are set forth in (a) the Terms of Service, (b) this DPA, (c) Customer's use of the Service (including Connector configurations, prompts, and feature settings), and (d) any additional written instructions Customer provides. Gigaton will notify Customer if, in its opinion, an instruction violates Data Protection Laws (Gigaton is not obligated to provide legal advice).

### 2.3 Customer's responsibilities

Customer represents and warrants that it:

(a) is the Controller of all Personal Data submitted to the Service and has a lawful basis for the processing;
(b) has provided all required notices to Data Subjects (e.g., its own privacy notice covering Gigaton as a Sub-processor);
(c) has obtained all required consents where consent is the lawful basis;
(d) will not submit Personal Data of residents of Excluded Jurisdictions to the Service;
(e) will respond to Data Subject requests directed at Customer and will only forward Data Subject requests to Gigaton where Gigaton's assistance is genuinely required.

## 3. Categories of data processed

### 3.1 Categories of Data Subjects

- **Customer's employees, contractors, and Authorized Users** (administering the Service);
- **Customer's prospects, leads, and contacts** (who Customer markets to or communicates with via the Service);
- **Customer's customers and End Users** (who book, transact, communicate, or otherwise interact via the Service — e.g., guests of an STVR operator, leads of a sales operator, vendors-customers of a financing operator);
- **Customer's vendors and counterparties** (where their data flows through Connectors).

### 3.2 Categories of Personal Data

| Category | Examples | Source |
|---|---|---|
| **Identification data** | Name, email address, phone number, role, company name | Customer entry; Connector ingest (Gmail, Drive, HubSpot, etc.) |
| **Booking and transaction data** | Reservation details, dates, property/service identifiers, prices, payment status | Customer entry; Connector ingest (Stripe, Airbnb, Vrbo, Booking.com if connected) |
| **Payment data** | Cardholder name, billing address, card last-4 + brand + expiry; NEVER full PAN or CVV | Stripe (Sub-processor) — full PCI-DSS scope held by Stripe |
| **Communication data** | Message content, timestamps, channel, thread context (SMS, WhatsApp, email, in-app chat) | Twilio (SMS/WhatsApp); Gmail Connector; in-app chat capture |
| **OAuth tokens and credentials references** | Refresh tokens for Drive, Gmail, Calendar; references to Secret-Manager-stored secrets | OAuth flow at signup; never raw secrets in application code |
| **Audio data (when enabled)** | Voice recordings, transcripts | Customer-uploaded; voice-ingest Connector |
| **Behavioral and usage data** | Pages viewed, features used, interaction sequences | Service telemetry |
| **AI processing inputs/outputs** | Prompts, ingested-content snippets, model outputs | Service-generated when AI features are invoked |
| **Sensitive Personal Data** | We do NOT request sensitive categories (health, biometric, government-ID, precise geolocation, race/ethnicity, religion, sexual orientation, financial-account-number except via Stripe, criminal history). Customer must NOT submit such data without first contacting privacy@gigaton.ai and executing a supplemental addendum (e.g., a HIPAA BAA where applicable). | N/A — Customer obligation |

[PARALEGAL: confirm sensitive-data carve-out language is sufficient; recommend explicit BAA template for any healthcare operator + explicit GLBA template for any financial-services operator.]

### 3.3 Nature and purposes of processing

Gigaton processes Personal Data to:

(a) provide and operate the Service as configured by Customer;
(b) generate AI outputs (drafts, summaries, decisions, classifications) at Customer's request;
(c) deliver communications via Twilio (SMS/WhatsApp) and email infrastructure on Customer's behalf;
(d) collect payments via Stripe on Customer's behalf (where Customer has enabled commerce features);
(e) provide analytics, dashboards, and Penrose-scoreboard outputs to Customer;
(f) maintain Service security, integrity, and abuse prevention;
(g) comply with legal obligations.

### 3.4 Duration

Gigaton will process Personal Data for the duration of the Terms of Service, plus the post-termination grace and deletion periods set forth in Section 8.

## 4. Sub-processors

### 4.1 Authorization

Customer authorizes Gigaton to engage the Sub-processors listed in **Annex A** to process Personal Data on Customer's behalf. Customer may obtain the current Sub-processor list at `gigaton.ai/legal/subprocessors` (TODO: build).

### 4.2 Sub-processor terms

Gigaton ensures by written contract that each Sub-processor (a) processes Personal Data only as instructed, (b) implements appropriate security measures, (c) is subject to confidentiality obligations, and (d) is liable to Gigaton for compliance with terms substantially equivalent to those in this DPA.

### 4.3 New Sub-processors

Gigaton will notify Customer at least 30 days before engaging a new Sub-processor or replacing an existing one (via in-app notification, the Sub-processor page, and/or email to Customer's billing contact). Customer may object in writing within the notice period; if Gigaton cannot reasonably accommodate the objection, Customer may terminate the affected portion of the Service for material breach.

### 4.4 Liability

Gigaton remains liable to Customer for the acts and omissions of its Sub-processors to the same extent as if performing the processing itself.

## 5. AI Subprocessors — specific commitments

Because AI processing is a core feature of the Service and a frequent privacy concern, this Section sets out specific commitments for the AI Subprocessors listed in Annex A (Anthropic, OpenAI, Google):

(a) Gigaton uses the **commercial API tiers** of each AI Subprocessor, under contracts that exclude API submissions from foundation-model training corpora absent explicit opt-in;
(b) Gigaton does **not** opt Customer's Personal Data into any AI Subprocessor's training pipeline;
(c) Customer may request, by email to `privacy@gigaton.ai` (TODO: confirm), the use of specific AI Subprocessors or the exclusion of others, subject to feature-parity availability;
(d) Gigaton publishes the current AI Subprocessor list (Annex A) and updates it under Section 4.3;
(e) Customer acknowledges that AI processing involves transmission of input data (which may include Personal Data) to the AI Subprocessor for the duration of the API request, plus any retention period stated in the AI Subprocessor's published terms (typically 0–30 days for abuse monitoring; see Annex A links).

[PARALEGAL: confirm that AI Subprocessor contractual flow-down is in place + matches what is asserted here; recommend annual audit of each AI Subprocessor's published terms vs the commitments in this Section.]

## 6. Security measures

Gigaton implements the technical and organizational security measures described in **Annex B**, including:

- TLS 1.2+ encryption in transit; encryption at rest (Google Cloud KMS-managed keys with rotation);
- Role-based access control with least-privilege defaults;
- Multi-factor authentication for staff with access to production systems;
- Secret-Manager-based storage of all credentials and tokens (no plaintext secrets in code or config);
- Audit logging of administrative and data-access events;
- Regular vulnerability scanning, dependency updates, and security reviews;
- Incident response plan with notification procedures (Section 7);
- Multi-tenant isolation via per-Customer namespaces, scopes, and database-row-level filtering;
- Backups encrypted, geographically replicated within the United States, and retained no longer than 90 days.

Gigaton may update Annex B from time to time provided that the overall level of security is not materially reduced.

## 7. Personal data incidents

If Gigaton becomes aware of a Personal Data Incident (defined as a breach of security leading to the accidental or unlawful destruction, loss, alteration, or unauthorized disclosure of or access to Personal Data processed under this DPA), Gigaton will:

(a) notify Customer **without undue delay** and in any event within **72 hours** of confirming the incident;
(b) provide Customer with information reasonably available about the nature, scope, and likely consequences of the incident;
(c) take reasonable steps to mitigate the incident and prevent recurrence;
(d) cooperate with Customer to fulfill Customer's regulatory and Data Subject notification obligations under Data Protection Laws.

Notice will be sent to the Customer's designated security contact (or, absent designation, the billing contact). Initial notice may be preliminary and supplemented as facts develop.

This notification does not constitute an acknowledgment of fault or liability.

[PARALEGAL: confirm 72-hour notice is appropriate; LFPDPPP Art. 20 + Reglamento require "immediate" notification "as soon as" the incident is confirmed; many US state laws require notice "without unreasonable delay" + within specific outer bounds (e.g., 30 days in MD/HI/FL); recommend documenting the 72-hour baseline as a floor and confirming specific statutory floors.]

## 8. Data Subject rights, data return, and deletion

### 8.1 Assistance with Data Subject requests

If a Data Subject contacts Gigaton directly with a rights request (access, deletion, correction, opposition, opt-out, ARCO), Gigaton will forward the request to Customer within 5 business days and not respond directly except to acknowledge receipt and direct the Data Subject to the Customer.

Gigaton will provide Customer with reasonable assistance in responding to Data Subject requests, including by providing tools within the Service to export, correct, or delete specific records. Customer is responsible for the substantive response.

### 8.2 Data return and deletion

Upon termination of the Terms of Service:

(a) Customer may export Customer Data, including Personal Data, via the Service or via reasonable assistance from Gigaton for a **30-day grace period** following the termination effective date;
(b) Gigaton will delete Personal Data from production systems within **60 days** of the termination effective date (i.e., within 30 days after the grace-period end);
(c) Personal Data persisting in encrypted, immutable backups will be deleted on Gigaton's regular backup-rotation schedule (within 90 days);
(d) Gigaton may retain Personal Data beyond these periods only where required by law (e.g., tax, audit, litigation hold), and only the minimum necessary, subject to continued confidentiality and security commitments.

### 8.3 Audit and documentation

Upon Customer's written request and no more frequently than once per 12-month period (except where required by law or in connection with an Incident), Gigaton will provide:

(a) responses to Customer's reasonable written information-security questionnaire;
(b) summaries of Gigaton's most recent third-party security assessments or certifications, where available;
(c) reasonable cooperation with Customer's regulatory audit requests, at Customer's expense, subject to confidentiality protections.

Gigaton is not obligated to permit on-premises inspections of its facilities except as required by law.

## 9. International data transfers

The Service is hosted primarily in the United States. By using the Service, Customer authorizes the transfer of Personal Data to the United States.

For Mexico-resident Data Subjects, Customer is responsible for providing the disclosures required by LFPDPPP Art. 36 to those Data Subjects (Gigaton's processing of such Personal Data in the United States is a cross-border transfer that must be disclosed in Customer's own privacy notice).

This DPA does not contemplate transfers from the European Economic Area, United Kingdom, or Switzerland (Excluded Jurisdictions). If Customer's processing involves Data Subjects in those jurisdictions, Customer must not use the Service for such processing during the v1 beta.

## 10. Liability and indemnification

The liability and indemnification provisions of the Terms of Service apply to this DPA. Notwithstanding any contrary provision, Gigaton's total liability arising out of this DPA is subject to the aggregate cap in Terms of Service Section 12.2, regardless of the number of Data Subjects, Personal Data Incidents, or claims.

[PARALEGAL: confirm liability allocation between Controller (Customer) and Processor (Gigaton) under each applicable Data Protection Law; statutory damages under CCPA $100–$750 per consumer per incident + LFPDPPP fines can be very large for Customers; confirm flow-through to indemnification.]

## 11. Term and termination

This DPA is effective on the Effective Date and remains in effect for the duration of the Terms of Service. Sections 6, 7, 8, 9, 10, and 12 survive termination.

## 12. Miscellaneous

### 12.1 Conflict

In the event of conflict between this DPA and the Terms of Service regarding the processing of Personal Data, this DPA controls.

### 12.2 Order of precedence

(1) This DPA, (2) the Terms of Service, (3) Customer's online order or signup configuration, (4) the [Privacy Policy](privacy_policy.md), (5) the [Acceptable Use Policy](acceptable_use_policy.md).

### 12.3 Counterparts

This DPA may be executed in counterparts, including by electronic signature.

---

## Annex A — Sub-processors (current as of 2026-05-25)

| Sub-processor | Category | Purpose | Location | Personal-data categories | Reference / DPA URL |
|---|---|---|---|---|---|
| **Google Cloud Platform (Alphabet Inc.)** | Cloud infrastructure | Hosting (Cloud Run, Cloud SQL, Firestore, GCS, KMS, Secret Manager); compute; storage; encryption | United States (`us-central1` primary) | All categories listed in Section 3.2 | https://cloud.google.com/terms/data-processing-addendum |
| **Cloudflare, Inc.** | CDN / DNS / DDoS | DNS resolution, content delivery, DDoS protection, edge security | Global edge; US-customer-data | Identification + behavioral (IP, user-agent, request metadata) | https://www.cloudflare.com/cloudflare-customer-dpa/ |
| **Stripe, Inc.** | Payment processing | Card processing, billing, Stripe Tax, dispute handling | United States | Identification + payment data | https://stripe.com/legal/dpa |
| **Twilio Inc.** | Communication infrastructure | SMS, WhatsApp Business API delivery | United States | Identification + communication data (phone, message contents) | https://www.twilio.com/legal/data-protection-addendum |
| **Anthropic, PBC** | AI processing | Large-language-model inference (Claude family) for content generation, decisioning, classification | United States | Whatever Customer or End User submits as input + Service-generated context | https://www.anthropic.com/legal/dpa |
| **OpenAI, L.L.C.** | AI processing | Large-language-model inference (GPT-family) — alternative provider, Customer-selectable | United States | Same as Anthropic | https://openai.com/policies/data-processing-addendum |
| **Google LLC (Gemini / Vertex AI)** | AI processing | Large-language-model inference (Gemini family) — alternative provider | United States | Same as above | https://cloud.google.com/terms/data-processing-addendum |
| **[PARALEGAL: confirm whether email-delivery provider is on the list — e.g., SendGrid, Postmark, Google Workspace SMTP. If yes, add a row.]** | | | | | |

### Removed Sub-processors
*(None as of 2026-05-25 — this DPA is v0)*

---

## Annex B — Technical and organizational security measures (summary)

### B.1 Access control

- Role-based access control (RBAC) on all production systems.
- Multi-factor authentication required for all production-system access.
- Just-in-time elevation for sensitive operations; logged + audited.
- Sign-off matrix (responsibility-scoped) gates approval-required actions (schema changes, billing changes, doctrine changes).
- Per-Customer namespace isolation enforced at the database row, gateway routing, and engine layers.

### B.2 Encryption

- TLS 1.2+ for all data in transit between client and Service, between Service and Sub-processors.
- AES-256 encryption at rest for databases (Cloud SQL), object storage (GCS), and Firestore.
- Customer-Managed Encryption Keys (CMEK) via Google Cloud KMS, with annual rotation policy.
- Secret-Manager-only storage for tokens, keys, and credentials (no plaintext in code/config).

### B.3 Operational security

- Hardened OS images via managed Cloud Run runtime.
- Vulnerability scanning of container images at build.
- Dependency-management policy (alerts on critical CVEs; remediation SLA aligned to severity).
- Secure-software-development lifecycle: code review, automated tests, security-review gate.

### B.4 Logging and monitoring

- Centralized logging in Google Cloud Logging.
- Audit trail of administrative actions (data access, configuration changes, sign-offs).
- Drift sentinel monitoring of doctrinal axioms (security-relevant invariants).
- Alerting on anomalous activity, error spikes, budget-cap breaches, and security signals.

### B.5 Resilience and backup

- Daily encrypted backups of production databases.
- Backups retained up to 90 days, then deleted.
- Disaster-recovery procedure documented; recovery-point objective (RPO) ≤ 24 hours; recovery-time objective (RTO) ≤ 24 hours.

### B.6 Personnel

- Background checks for personnel with production-system access [PARALEGAL: confirm scope/practicality for a 2-3 person team].
- Confidentiality obligations in employment / contractor agreements.
- Annual security awareness training.
- Off-boarding procedure to revoke access promptly upon role change or separation.

### B.7 Physical security

- Data centers operated by Google Cloud — Google's physical-security controls (SOC 2 Type II, ISO 27001, etc.) apply. Gigaton itself does not operate physical data-center facilities.

### B.8 Incident response

- Documented incident-response plan with severity classification, escalation, and notification procedures.
- Incident commander role with on-call rotation.
- Post-incident retrospective for every Severity-1 incident with documented corrective actions.

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
