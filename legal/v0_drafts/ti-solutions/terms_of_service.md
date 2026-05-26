---
entity: Ti Solutions
doc_type: terms_of_service
version: v0-draft-2026-05-25
status: PENDING-PARALEGAL-REVIEW
effective_date: 2026-05-26
applicable_jurisdictions: [US, MX]
excluded_jurisdictions: [EU, UK]
last_reviewed: 2026-05-25
contact: legal@gigaton.ai
related_docs:
  - privacy_policy.md
  - acceptable_use_policy.md
  - data_processing_addendum.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> **Entity-status note:** As of 2026-05-25, the locked recommendation in the 30-day launch roadmap is that Ti Solutions operate as a **DBA ("doing business as") under Gigaton AI's legal entity** rather than as a separate LLC. The user's final decision on legal-entity structure is pending. This draft assumes the DBA structure (Ti Solutions branding; Gigaton AI legal entity behind it; one Stripe account per locked decision B1).
>
> If the user instead elects a separate LLC, several sections (1, 2, 17, 18) will need rework. **[PARALEGAL: confirm entity structure and adjust all references accordingly before finalization.]**

# Ti Solutions — Master Services Agreement Template / Terms of Service

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25
**Service Provider:** Ti Solutions, a DBA of Gigaton AI ("**Ti Solutions**," "**we**," "**us**," "**our**")
**Domain:** tisolutions.co
**Contact:** legal@gigaton.ai (TODO: confirm a dedicated `legal@tisolutions.co` alias)

---

## 1. Acceptance and Structure

These Terms of Service ("**Terms**") apply to Ti Solutions' managed-service offering. Because Ti Solutions delivers professional services on a custom-scoped basis to mid-market customers, the operative agreement is typically a **Master Services Agreement ("MSA")** plus one or more **Statements of Work ("SOW")** rather than self-serve clickwrap. These Terms serve as a baseline that may be (a) accepted via clickwrap for sales-funnel intake (e.g., booking a scoping call, downloading a white paper), and (b) overlaid by a custom MSA + SOW once a Customer is signed.

Where a fully executed MSA + SOW exists between Ti Solutions and a Customer, **the MSA + SOW prevails over these Terms** to the extent of inconsistency.

By using `tisolutions.co`, requesting a scoping call, providing information for a proposal, or otherwise engaging with Ti Solutions' services (the "**Services**"), you ("**Customer**") agree to these Terms, the [Privacy Policy](privacy_policy.md), the [Acceptable Use Policy](acceptable_use_policy.md), and (for engaged Customers) the [Data Processing Addendum](data_processing_addendum.md).

[PARALEGAL: confirm we want a clickwrap baseline + custom MSA structure vs single combined contract; recommend MSA template review by counsel before public launch.]

## 2. Legal Entity and Geographic Scope

### 2.1 Legal entity

Ti Solutions is operated as a **DBA / d/b/a** of **Gigaton AI** (a [PARALEGAL: insert state/country of formation] legal entity). All contracting, invoicing, and tax obligations are performed under the Gigaton AI legal entity, with "Ti Solutions" appearing as a customer-facing brand. The single platform Stripe account (per Gigaton's billing-architecture decision B1) handles invoicing for all Ti Solutions engagements.

### 2.2 Geographic scope

The Services are offered to Customers domiciled in the **United States and Mexico** during the v1 beta period. We do not market to or accept engagements from Customers domiciled in the European Union, European Economic Area, United Kingdom, or Switzerland (the "**Excluded Jurisdictions**"). If a prospective Customer is domiciled in an Excluded Jurisdiction, we will decline engagement during the beta period.

[PARALEGAL: confirm EU exclusion is appropriate; for B2B managed services the customer-protection regimes are less consumer-oriented but data-protection (GDPR) still applies — exclusion is the recommended risk-bounded posture for v1.]

## 3. Definitions

- **"Customer"** — the business entity engaging Ti Solutions for Services under an MSA + SOW (or, for pre-engagement interactions, the entity inquiring about Services).
- **"Authorized User"** — an employee, contractor, or designated representative of Customer with access to deliverables or to Ti Solutions' staff.
- **"Services"** — the consulting, managed-service operation, integration build, deliverable production, and related professional services described in an SOW. Includes "Vendor Growth Engine," "Outbound Operating System," "Interaction Management as a Service," and custom packages.
- **"Deliverables"** — the documents, artifacts, datasets, code, configurations, training materials, and other tangible outputs produced under an SOW.
- **"Customer Materials"** — data, content, brand assets, customer lists, prior collateral, and other materials provided by Customer for use in the Services.
- **"Gigaton Platform"** — the Gigaton AI software platform, used by Ti Solutions to deliver the Services (see Section 11).
- **"AI Subprocessors"** — Anthropic, OpenAI, Google (Gemini), as used by the Gigaton Platform.

## 4. The Services

Ti Solutions provides managed-service delivery of the Gigaton+Ti Solutions product+service package, including:

(a) **Discovery & scoping** — assessment of Customer's current sales / interaction / outbound operations and identification of opportunity areas;
(b) **Configuration & integration** — setup of the Gigaton Platform tenant, connection of Customer's third-party systems (CRM, dialer, OTAs, communication channels, etc.);
(c) **Content & playbook production** — outbound scripts, interactive experiences, brand-aligned communications, fit-scoring models, ROI calculators, proposal generators;
(d) **Operational execution** — Ti Solutions personnel operate the Gigaton Platform on Customer's behalf (sending outbound, qualifying responses, handing off qualified leads to Customer's sales team);
(e) **Measurement & strategy** — monthly reviews, performance reporting, calibration, recommendations.

The specific scope, deliverable schedule, fees, performance targets, and term are set forth in the applicable SOW.

## 5. Engagement Terms (Baseline; SOW Controls)

### 5.1 Setup package

Ti Solutions typically charges a one-time **setup package fee** (baseline US$40,000) covering discovery, configuration, initial content production, and kickoff. Setup is invoiced upon SOW execution; payment terms typically Net-15.

### 5.2 Retainer

Ti Solutions typically charges a **monthly retainer** (baseline US$8,000–US$25,000 depending on scope) for ongoing operational execution. Retainer is invoiced monthly in advance.

### 5.3 Performance components

SOWs may include a **performance component** (e.g., per-funded-contract bonus, percent-of-incremental-net-revenue for a defined window). Performance components are paid in arrears upon measurement and validation.

### 5.4 Invoicing and payment

All fees are invoiced via Stripe (under Gigaton AI's platform Stripe account per B1). Stripe Tax is enabled and calculates applicable taxes. Payment terms default to Net-15 for invoices; failures to pay after 30 days may result in suspension of operational delivery.

### 5.5 Expenses

Out-of-pocket expenses (third-party tooling, ad spend, vendor licenses, travel where applicable) are billed at cost plus [PARALEGAL: confirm markup %, common is 0% (pass-through) or 10%] markup, as detailed in the SOW.

### 5.6 Refunds and chargebacks

The setup package and prior-month retainer are non-refundable. Future-period retainer may be refunded pro rata if Ti Solutions fails to deliver per the SOW and fails to cure within 14 days of written notice. Chargebacks initiated without prior dispute resolution may result in immediate suspension and collection costs.

## 6. Customer's Responsibilities

Customer agrees to:

(a) Provide timely, accurate, and complete information needed for the Services (CRM access, target lists, brand assets, sales-process documentation);
(b) Designate a primary point of contact authorized to make decisions on behalf of Customer;
(c) Respond to information requests within a reasonable time (typically 3 business days);
(d) Operate Customer's portion of the workflow per the SOW (e.g., timely follow-up on qualified leads handed off);
(e) Maintain valid permissions and consents from Customer's contacts for the marketing/outreach activities executed by Ti Solutions on Customer's behalf — including TCPA consent for SMS/calls, CAN-SPAM compliance for email, GDPR-style consent if Customer maintains EU contacts (Customer must not direct Ti Solutions to contact EU-resident leads during v1 beta given Section 2.2 exclusion);
(f) Pay invoices when due.

## 7. Authorized Use of the Gigaton Platform

In delivering the Services, Ti Solutions provides Customer access to a Gigaton Platform tenant. Customer's use of the Gigaton Platform is subject to the [Gigaton AI Terms of Service](../gigaton-ai/terms_of_service.md), [Acceptable Use Policy](../gigaton-ai/acceptable_use_policy.md), and [Data Processing Addendum](../gigaton-ai/data_processing_addendum.md), which are **incorporated by reference**. Where the Gigaton Terms and these Ti Solutions Terms address the same subject matter, the Ti Solutions Terms control for the Customer's relationship with Ti Solutions, but the Gigaton Terms apply to Customer's direct use of the Platform.

## 8. Customer Materials and Customer Data

### 8.1 Ownership

Customer retains all right, title, and interest in Customer Materials and Customer Data. Customer grants Ti Solutions a non-exclusive, worldwide license, for the duration of the engagement, to use, copy, modify, store, transmit, and create derivative works of Customer Materials and Customer Data solely to provide the Services.

### 8.2 Confidentiality of Customer Materials

Customer Materials are Customer's Confidential Information per Section 12.

### 8.3 Customer Data processing

Personal data within Customer Materials is processed under the [Data Processing Addendum](data_processing_addendum.md).

### 8.4 Use of Customer logos / case studies

With Customer's prior written consent, Ti Solutions may use Customer's name and logo on the Ti Solutions website and in marketing materials to identify Customer as a client. With separate written consent, Ti Solutions may publish a sanitized case study. Consent may be withdrawn on 30 days' notice for future use; published materials may remain in publication archives.

## 9. Deliverables and Intellectual Property

### 9.1 Custom Deliverables — Customer ownership

Deliverables specifically produced for Customer's engagement (e.g., Customer-specific scripts, configurations, playbooks, ROI models) are owned by Customer upon full payment. Ti Solutions retains a perpetual license to use techniques, methods, and know-how learned through the engagement (residual knowledge).

### 9.2 Ti Solutions / Gigaton retained IP

The underlying Gigaton Platform, Ti Solutions' methodologies, prompt templates, scoring models, frameworks, and any preexisting or independently developed work product are owned by Ti Solutions or Gigaton AI. Customer receives a non-exclusive license to use these as embedded in Deliverables but no ownership.

### 9.3 AI-generated outputs

To the extent Deliverables contain AI-generated content, Section 9.2 of the Gigaton AI Terms applies. Customer acknowledges that AI-generated content may overlap with content produced for other customers and may not be uniquely protectable by copyright.

### 9.4 Third-party materials

Where Deliverables incorporate third-party materials (stock photography, fonts, third-party libraries), the relevant license terms apply. Ti Solutions will identify such third-party materials and the applicable license in the SOW or Deliverable documentation.

## 10. AI Processing Disclosure

The Services use AI extensively. AI-driven activities include:

(a) Drafting outbound messages, scripts, content, and proposals;
(b) Scoring leads and ranking opportunities;
(c) Summarizing customer interactions and producing performance reports;
(d) Generating interactive brand experiences (chatbots, landing pages, WhatsApp flows) deployed for Customer's prospects;
(e) Recommending next-best actions for Ti Solutions operators and Customer's sales team.

Customer expressly consents to AI processing of Customer Materials and Customer Data for these purposes. Customer may, by written notice, request exclusion of specific data categories from AI processing where the underlying business need can be met without AI (some methods will be impaired or unavailable).

[PARALEGAL: confirm AI-disclosure language is acceptable for a B2B context; consider whether SOW should include a per-engagement AI-use declaration listing categories of AI use specific to that engagement.]

## 11. Sub-Processor Stack

Ti Solutions uses the **Gigaton AI** platform as its sole technology infrastructure. Through Gigaton, Ti Solutions accesses Stripe, Twilio, Anthropic, OpenAI, Google (Gemini), GCP, and Cloudflare — full list in the [Gigaton AI Data Processing Addendum](../gigaton-ai/data_processing_addendum.md) Annex A and at `gigaton.ai/legal/subprocessors` (TODO: build).

Ti Solutions may engage additional third parties specific to a Customer engagement (e.g., a dialer vendor like VCC Live or Vici Dial, a data-enrichment vendor like Clay or Apollo). Such engagements are disclosed in the SOW and governed by the [Data Processing Addendum](data_processing_addendum.md).

## 12. Confidentiality

Each party will (a) use the other's Confidential Information only to perform under these Terms, (b) protect it with at least the standard of care it uses for its own (and at minimum reasonable care), (c) not disclose to third parties except sub-processors under confidentiality obligations.

"Confidential Information" includes Customer Materials, Ti Solutions methodologies, financial terms, strategic plans, prospect lists, and customer-of-customer data. Excluded: publicly known information, information independently developed without reference, information legally received from a third party, or information whose disclosure is legally required (with notice where lawful).

Confidentiality survives for **5 years** after termination, **indefinitely** for trade secrets.

[PARALEGAL: confirm survival periods are standard for the industry; consider longer (e.g., 7 years) for highly sensitive industries.]

## 13. Performance, SLAs, and Warranties

### 13.1 Performance commitments

Ti Solutions will perform the Services with reasonable care and skill consistent with industry standards for managed-service consulting. Specific deliverable-level SLAs (e.g., proposal turnaround time, meeting cadence, performance targets) are set forth in each SOW.

### 13.2 Performance targets vs. guarantees

Where an SOW includes performance targets (e.g., "X funded contracts per quarter"), these are objectives and the basis for performance-component compensation, but unless explicitly framed as a guarantee with a specified remedy, are not contractual guarantees. Underperformance triggers the performance-component math (lower bonus) but not refund of base fees.

### 13.3 Disclaimer

EXCEPT AS EXPRESSLY STATED, **THE SERVICES AND DELIVERABLES ARE PROVIDED "AS IS"**, without warranty of merchantability, fitness for a particular purpose, non-infringement, or any specific performance outcome. AI-generated content may contain inaccuracies and must be reviewed by Customer before use.

## 14. Limitation of Liability

EXCLUDED DAMAGES (consequential, lost profits, etc.) — same as Gigaton AI Terms Section 12.1.

LIABILITY CAP: TI SOLUTIONS' AGGREGATE LIABILITY UNDER THESE TERMS AND ANY SOW WILL NOT EXCEED **THE GREATER OF (A) THE TOTAL FEES PAID BY CUSTOMER UNDER THE SOW GIVING RISE TO THE CLAIM IN THE 12 MONTHS PRECEDING THE CLAIM, OR (B) US$50,000.**

[PARALEGAL: confirm $50K floor is appropriate for typical engagement value ($40K setup + $8K-$25K/mo retainer); consider whether the floor should scale with engagement size — e.g., 1x annual retainer.]

EXCLUSIONS (do not cap): payment obligations, indemnification obligations, breach of confidentiality, Customer's violation of AUP, gross negligence or willful misconduct, and amounts excluded by law.

## 15. Indemnification

### 15.1 By Ti Solutions

Ti Solutions will defend Customer against third-party claims that Deliverables (as delivered by Ti Solutions and used per these Terms) directly infringe such third party's U.S. or Mexican IP rights. Exclusions: claims arising from Customer Materials, Customer-driven modifications, Customer's use beyond the SOW scope, or AI-generated outputs that Customer approved for use.

### 15.2 By Customer

Customer will defend Ti Solutions and its personnel against claims arising from (a) Customer Materials (including IP rights in Customer's lists, brand assets, and content), (b) Customer's direction of Ti Solutions to perform outreach to specific contacts (TCPA/CAN-SPAM/PROFECO compliance is Customer's responsibility unless explicitly delegated in writing), (c) Customer's products/services that are the subject of the marketing/outreach, (d) violation of the AUP.

## 16. Term, Termination, Suspension

### 16.1 Term

The MSA + SOW governs term. Default SOW term is 6–12 months with automatic 30-day rolling renewal absent 30 days' written notice of non-renewal.

### 16.2 Termination for convenience

Either party may terminate an SOW on **60 days' written notice** (or as specified in the SOW). Customer remains liable for fees through the notice period and for any non-refundable setup fee.

### 16.3 Termination for cause

Either party may terminate immediately upon written notice for material breach uncured after 14 days, insolvency, or fraud.

### 16.4 Effect of termination

Upon termination: (a) Customer's outstanding payment obligations survive, (b) Deliverables produced through the termination date are delivered upon final payment, (c) Customer Data is returned/exported within a **30-day grace period** and deleted from Ti Solutions / Gigaton systems within **60 days** thereafter, (d) confidentiality and IP provisions survive.

## 17. Governing Law and Dispute Resolution

### 17.1 Governing law

These Terms are governed by the laws of [PARALEGAL: confirm — Delaware if Gigaton AI is DE-formed; otherwise Gigaton AI's state of formation]. Mexican law applies to Mexican-domiciled Customer aspects to the extent of mandatory provisions.

### 17.2 Informal resolution

60-day informal-resolution period before formal proceedings.

### 17.3 Arbitration

Disputes that cannot be resolved informally will be resolved by **binding arbitration** administered by [PARALEGAL: select forum — AAA Commercial Arbitration Rules venue Wilmington DE OR JAMS OR CAM Mexico for MX-only disputes]. **THE PARTIES WAIVE ANY RIGHT TO PARTICIPATE IN A CLASS, COLLECTIVE, OR REPRESENTATIVE ACTION.** [PARALEGAL: confirm class-waiver enforceability — note that for B2B managed-service agreements, class-action concerns are minimal but the waiver is still standard.]

### 17.4 Exceptions

Either party may seek injunctive relief for IP infringement, breach of confidentiality, or unpaid invoices in a court of competent jurisdiction.

## 18. Miscellaneous

Severability, no-waiver, assignment (Customer may not assign without consent; Ti Solutions may assign in a corporate transaction), force majeure, independent contractor (Ti Solutions is not Customer's employee, partner, or joint-venturer; Ti Solutions personnel are independent of Customer's HR / payroll), notices (legal@gigaton.ai), language (English controls), export compliance — all parallel Gigaton AI Terms Sections 18.1–18.9.

### 18.1 Non-solicitation of personnel

For the term of the engagement and 12 months thereafter, neither party will solicit for employment any employee or contractor of the other who was substantially involved in the engagement, without prior written consent. General-public job postings are not solicitation.

[PARALEGAL: confirm non-solicit enforceability in target jurisdictions — California broadly disfavors employee non-solicits; Mexico has labor-law considerations; consider time-period adjustment.]

### 18.2 Independent contractor and Gigaton platform reuse

Customer acknowledges that Ti Solutions operates the same Gigaton Platform for multiple Customers. Methods, prompts, models, and infrastructure that are not Customer-specific Deliverables may be reused across engagements. Ti Solutions will not disclose Customer's Confidential Information across engagements.

---

## Contact

Ti Solutions (a DBA of Gigaton AI)
Email: `legal@gigaton.ai` (TODO: confirm dedicated `legal@tisolutions.co`)
CxGuy / Sales: `cxguy@tisolutions.co` (TODO: confirm)
Mailing address: [PARALEGAL: insert Gigaton AI's registered address; consider whether tisolutions.co needs its own mailing or shares Gigaton AI's]

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
