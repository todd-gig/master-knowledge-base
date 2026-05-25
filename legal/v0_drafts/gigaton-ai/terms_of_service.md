---
entity: Gigaton AI
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
> This document is a **starting template** drafted by an AI assistant on 2026-05-25, intended as a working draft for an attorney or paralegal to review, refine, and finalize before public publication. It has not been reviewed by counsel. Do not link to it from any production marketing surface, accept payment under its terms, or otherwise hold it out as a binding agreement until the review markers below are resolved and a licensed attorney has approved a final version.
>
> Look for inline `[PARALEGAL: …]` markers throughout — each one flags a judgment call that requires legal review for the target jurisdictions (United States baseline + Mexico for Carmen Beach Properties; **EU/UK customers are explicitly excluded from v1 beta**).

# Gigaton AI — Terms of Service

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25
**Operator:** Gigaton AI ("**Gigaton**," "**we**," "**us**," or "**our**")
**Domain:** gigaton.ai
**Contact:** legal@gigaton.ai (TODO: confirm)

---

## 1. Acceptance of these Terms

These Terms of Service ("**Terms**") form a binding legal agreement between you ("**Customer**," "**you**," or "**your**") and Gigaton AI, governing your access to and use of the Gigaton platform, including the website at `gigaton.ai`, the application at `app.gigaton.ai`, the API at `api.gigaton.ai`, and any related products, services, integrations, dashboards, documentation, and software (collectively, the "**Service**").

By creating an account, clicking "I Agree," accessing the Service, or otherwise using the Service, you acknowledge that you have read, understood, and agree to be bound by these Terms, the [Privacy Policy](privacy_policy.md), the [Acceptable Use Policy](acceptable_use_policy.md), and, where applicable, the [Data Processing Addendum](data_processing_addendum.md), each of which is incorporated by reference. If you do not agree to these Terms, you must not access or use the Service.

If you are accepting these Terms on behalf of a company, organization, or other legal entity, you represent and warrant that you have the authority to bind that entity to these Terms, and "**Customer**" refers to that entity.

[PARALEGAL: confirm clickwrap acceptance mechanism is enforceable — recommend signup flow includes (1) checkbox above "Create Account" button, (2) stored timestamp + IP + user-agent of acceptance in audit log, (3) re-acceptance prompt on material changes.]

## 2. Geographic Scope and Excluded Jurisdictions

The Service is **offered to and intended for customers in the United States and Mexico only** at this time. By using the Service, you represent that you are not located in, and you are not accepting these Terms on behalf of any entity located in, the European Union, the European Economic Area, the United Kingdom, Switzerland, or any other jurisdiction where the offering of the Service has not been explicitly enabled.

We do not knowingly serve customers, process personal data of residents, or accept payment from customers based in the EU, EEA, UK, or Switzerland during the v1 beta period (the "**Excluded Jurisdictions**"). If we discover that a Customer or end user is located in an Excluded Jurisdiction, we reserve the right to suspend or terminate the relevant account under Section 13.

[PARALEGAL: confirm geo-fencing language and remediation; recommend (1) IP-geolocation block at signup, (2) self-attestation, (3) suspension protocol on discovery — confirm minimum-viable disclosure language for current legal exposure.]

## 3. Definitions

- **"Account"** means the account you create to access the Service.
- **"Authorized User"** means an individual (e.g., employee, contractor) who is authorized by Customer to use the Service under Customer's Account.
- **"Customer Data"** means any data, content, information, or materials submitted, uploaded, or transmitted to the Service by or on behalf of Customer, including data ingested from connected third-party services.
- **"Documentation"** means the user guides, API documentation, and help materials made available by Gigaton.
- **"Subscription"** means the paid plan tier (Starter / Operator / Scale) under which Customer accesses the Service.
- **"Sub-processor"** means a third-party service provider engaged by Gigaton to process data on behalf of Customer, as listed in the [Data Processing Addendum](data_processing_addendum.md).
- **"Connector"** means an integration with a third-party service (such as Google Drive, WhatsApp via Twilio, Stripe, etc.) configured by Customer.
- **"Generated Output"** means content, recommendations, decisions, drafts, analyses, summaries, or other outputs produced by the Service, including outputs produced with the assistance of artificial intelligence or large language models.
- **"AI Subprocessors"** means the third-party AI model providers Gigaton uses to produce Generated Output, including but not limited to Anthropic, OpenAI, and Google.

## 4. The Service

### 4.1 Description

Gigaton provides a multi-tenant software-as-a-service platform that connects Customer's third-party tools, ingests data into a unified intelligence layer, generates interactive brand-experience artifacts, supports customer interactions across channels (chat, WhatsApp, email), and surfaces decisioning and analytics dashboards. The Service is intended to help Customer manage business interactions in a manner aligned with Gigaton's "Predictably Profitable Interaction Management" framework.

### 4.2 Subscription Tiers

Subscription plans, included quotas, and add-ons are described on the pricing page at `gigaton.ai/pricing` and may be updated from time to time. Quotas may include limits on the number of brands, connectors, generated bundles, API calls, or AI tokens consumed per billing period.

### 4.3 Beta Status

The Service is currently offered in **beta**. Features may be added, modified, or removed without notice. Beta features may be marked as "alpha," "beta," "experimental," or "preview" and are provided **AS IS** without any service-level commitments beyond those explicitly stated in writing.

[PARALEGAL: confirm beta-period disclaimers — recommend explicit beta clause limiting warranties + SLAs during this period; should align with limitation-of-liability section.]

## 5. Account Registration and Eligibility

To use the Service, you must register for an Account and provide accurate, current, and complete information. You must:

- Be at least 18 years of age (or the age of legal majority in your jurisdiction);
- Have the legal authority to enter into these Terms;
- Not be located in an Excluded Jurisdiction (Section 2);
- Not be on any government list of restricted persons or entities;
- Not have been previously suspended or terminated from the Service.

You are responsible for safeguarding your Account credentials and for all activity that occurs under your Account, whether or not authorized by you. You must promptly notify Gigaton at `security@gigaton.ai` (TODO: confirm) of any unauthorized access or suspected security breach.

## 6. License Grant and Restrictions

### 6.1 License to Customer

Subject to Customer's compliance with these Terms and payment of applicable fees, Gigaton grants Customer a non-exclusive, non-transferable, non-sublicensable, revocable license during the term of these Terms to access and use the Service solely for Customer's internal business purposes.

### 6.2 Restrictions

Customer shall not, and shall not permit any Authorized User or third party to:

(a) copy, modify, reverse engineer, decompile, disassemble, or attempt to derive the source code of the Service except to the limited extent permitted by applicable law notwithstanding this prohibition;
(b) rent, lease, sell, sublicense, distribute, resell, or assign access to the Service to any third party except as expressly permitted;
(c) use the Service to build a competitive product or service or to benchmark with a competitive product;
(d) circumvent or attempt to circumvent any usage limits, rate limits, security mechanisms, or access controls;
(e) use the Service in violation of the [Acceptable Use Policy](acceptable_use_policy.md);
(f) remove, alter, or obscure any proprietary notices included in or with the Service;
(g) use any automated means (other than the Service's own publicly documented API) to access the Service in a manner inconsistent with these Terms or the [Acceptable Use Policy](acceptable_use_policy.md);
(h) use the Service to train, fine-tune, or otherwise improve any competing artificial intelligence model.

[PARALEGAL: confirm restriction (h) — recommend reviewing in light of evolving AI training disclosure norms + emerging regulation; may need carve-outs.]

## 7. Customer Data

### 7.1 Ownership

As between the parties, Customer retains all right, title, and interest in and to Customer Data. Customer grants Gigaton a worldwide, non-exclusive, royalty-free license to host, store, transmit, copy, display, modify, analyze, and create derivative works of Customer Data solely as necessary to (a) provide and improve the Service to Customer, (b) generate Generated Output requested by Customer, (c) maintain operational metrics, security, and abuse detection, and (d) comply with legal obligations.

### 7.2 Sub-Processor Processing

Customer acknowledges that to provide the Service, Gigaton uses Sub-processors (including AI Subprocessors, cloud infrastructure, communication providers, and payment processors). A current list of Sub-processors is maintained in Annex A of the [Data Processing Addendum](data_processing_addendum.md). Customer authorizes Gigaton to engage these Sub-processors on Customer's behalf.

### 7.3 AI Processing Disclosure

**Customer expressly acknowledges and consents that the Service uses artificial intelligence and large language models for:**

(a) automated decisioning (e.g., routing interactions, scoring leads, recommending next-best actions);
(b) content generation (e.g., drafting messages, summaries, landing-page copy, WhatsApp scripts);
(c) data extraction and classification (e.g., parsing connected documents, categorizing interactions);
(d) personalization (e.g., adapting outputs to Customer's brand voice and context).

AI Subprocessors include Anthropic, OpenAI, and Google. Customer Data may be transmitted to these AI Subprocessors in the course of generating Generated Output. Gigaton has obtained contractual commitments from each AI Subprocessor that Customer Data submitted via the Service's commercial API endpoints **will not be used to train the AI Subprocessor's foundation models** absent Customer's explicit opt-in. See Section 7.4 for opt-out and configuration options.

### 7.4 AI Opt-Out

Where technically feasible, Customer may, by written request to `privacy@gigaton.ai` (TODO: confirm), opt out of:

(a) the use of Customer Data for Gigaton's own model improvement (default: opted in for service improvement only — never sold or licensed to third parties for their model training);
(b) the use of specific AI Subprocessors (Customer may request alternative AI Subprocessors, subject to feature parity availability);
(c) the use of AI for specific decisioning categories (Customer may request human-only review for designated categories).

Some Service features depend materially on AI processing; opting out of AI processing in those features may degrade or disable functionality, which Gigaton will disclose at the time of the opt-out request.

[PARALEGAL: confirm AI processing + opt-out language is sufficient under emerging AI disclosure norms — Colorado AI Act, NYC AEDT, California ADMT regs — recommend annual review.]

### 7.5 Customer Data Retention and Deletion

Customer may export Customer Data via the Service at any time during the term. Upon termination of the Account, Gigaton will retain Customer Data for a grace period of **thirty (30) days** to permit Customer to export, after which Customer Data will be deleted from Gigaton's production systems within **sixty (60) days** of the termination effective date, subject to limited retention required for legal compliance, audit, or backup purposes (which retention is described in the [Privacy Policy](privacy_policy.md)).

## 8. Payment Terms

### 8.1 Fees

Customer agrees to pay all fees for the applicable Subscription tier as posted at `gigaton.ai/pricing` at the time of subscription. Fees are exclusive of taxes (see Section 8.4).

### 8.2 Billing and Payment

Subscriptions are billed in advance on a monthly (or annual, if elected) basis. Gigaton uses **Stripe, Inc.** as its sole payment processor. By providing payment information, Customer authorizes Gigaton (via Stripe) to charge the designated payment method for all applicable fees on each renewal date.

### 8.3 Failed Payments and Grace

If a payment fails, Gigaton may retry the charge on day +1, +3, and +7 from the failure date. After 14 days of unresolved non-payment, Gigaton may suspend Customer's access to the Service. If non-payment continues for 30 days, Gigaton may terminate the Account.

### 8.4 Taxes

Customer is responsible for all applicable sales, use, value-added, goods-and-services, or similar taxes ("**Taxes**"). Gigaton uses Stripe Tax for automatic tax calculation and collection where supported. Customer represents that the billing address provided is accurate for Tax-jurisdiction determination.

[PARALEGAL: confirm Stripe Tax handling language is accurate; verify whether Gigaton or Stripe is "Merchant of Record" for each operating jurisdiction.]

### 8.5 Refunds and Disputes

Except as required by applicable law or as expressly stated in these Terms, all fees are non-refundable. Disputed charges must be raised within 30 days of the invoice date. Chargebacks initiated without first contacting Gigaton may result in immediate suspension.

### 8.6 Overage and Metered Charges

Where Customer's Subscription tier includes quotas (e.g., generated bundles, API calls), usage above the quota will be billed as metered overage at the rates posted on the pricing page. Customer may set a budget cap in account settings; the Service will throttle or pause AI-bearing features when the cap is reached.

## 9. Intellectual Property

### 9.1 Gigaton IP

Gigaton retains all right, title, and interest in and to the Service, including all software, algorithms, models, documentation, design elements, trademarks, the Gigaton name and logo, and all improvements, derivative works, and aggregated or anonymized data derived from use of the Service.

### 9.2 Generated Output

Subject to Customer's compliance with these Terms and payment of fees, Customer owns the Generated Output produced for Customer's Account. Customer acknowledges that:

(a) Generated Output is produced with the assistance of AI Subprocessors and may not be unique to Customer (similar prompts may produce similar outputs for different customers);
(b) Generated Output may contain inaccuracies, hallucinations, or errors, and Customer is solely responsible for reviewing Generated Output before relying on or publishing it;
(c) Generated Output is not legal, medical, financial, or other professional advice;
(d) Some Generated Output may not be protectable by copyright or other intellectual-property law in some jurisdictions due to its AI-generated nature.

### 9.3 Feedback

If Customer provides feedback, suggestions, or ideas about the Service ("**Feedback**"), Customer grants Gigaton a perpetual, irrevocable, worldwide, royalty-free license to use Feedback for any purpose without obligation to Customer.

### 9.4 Trademarks

Customer may not use Gigaton's trademarks, logos, or trade names without prior written permission, except to factually describe Customer's use of the Service.

## 10. Confidentiality

Each party will use the other party's Confidential Information only for purposes of these Terms and will protect such information using at least the same standard of care it uses to protect its own confidential information (and in no event less than reasonable care). "Confidential Information" includes non-public business and technical information disclosed in connection with these Terms.

## 11. Warranties and Disclaimers

### 11.1 Mutual Warranties

Each party represents that it has the legal authority to enter into these Terms and that its performance will not violate any other agreement.

### 11.2 Service Warranty

Gigaton warrants that during the term, the Service will materially conform to the Documentation under normal use, subject to Section 4.3 (Beta Status).

### 11.3 Disclaimer

EXCEPT AS EXPRESSLY STATED IN THESE TERMS, **THE SERVICE AND GENERATED OUTPUT ARE PROVIDED "AS IS" AND "AS AVAILABLE" WITHOUT WARRANTY OF ANY KIND**, EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, ACCURACY, AND UNINTERRUPTED OPERATION. GIGATON DOES NOT WARRANT THAT THE SERVICE WILL BE ERROR-FREE OR THAT GENERATED OUTPUT WILL BE ACCURATE OR SUITABLE FOR CUSTOMER'S PURPOSES.

[PARALEGAL: confirm "AS IS" disclaimer is enforceable under MX consumer-protection law (LFPC) for any MX-resident customer; may require carve-outs.]

## 12. Limitation of Liability

### 12.1 Excluded Damages

TO THE MAXIMUM EXTENT PERMITTED BY APPLICABLE LAW, IN NO EVENT WILL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, OR FOR LOST PROFITS, LOST REVENUE, LOST DATA, BUSINESS INTERRUPTION, OR LOSS OF GOODWILL, WHETHER ARISING IN CONTRACT, TORT, NEGLIGENCE, STRICT LIABILITY, OR OTHERWISE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

### 12.2 Cap

EACH PARTY'S TOTAL CUMULATIVE LIABILITY UNDER THESE TERMS WILL NOT EXCEED THE GREATER OF (A) THE AMOUNTS PAID BY CUSTOMER TO GIGATON IN THE TWELVE (12) MONTHS PRECEDING THE CLAIM, OR (B) ONE HUNDRED U.S. DOLLARS (US$100).

### 12.3 Exclusions

The limitations in Sections 12.1 and 12.2 do not apply to (a) Customer's payment obligations, (b) either party's indemnification obligations, (c) breaches of confidentiality, (d) Customer's violation of the Acceptable Use Policy, or (e) liability that cannot be limited under applicable law.

[PARALEGAL: confirm liability cap amount — $100 floor + 12-mo fees is industry standard for SaaS; confirm enforceability for Customer Data breaches under CCPA + MX LFPDPPP statutory penalties.]

## 13. Term, Suspension, and Termination

### 13.1 Term

These Terms commence on the date Customer first accepts them and continue until terminated as set forth herein.

### 13.2 Termination for Convenience

Customer may terminate by canceling the Subscription in account settings, effective at the end of the current billing period. Gigaton may terminate any Subscription on 30 days' written notice.

### 13.3 Termination for Cause

Either party may terminate immediately upon written notice if the other party materially breaches these Terms and fails to cure within 14 days, or if the other party becomes insolvent or files for bankruptcy.

### 13.4 Suspension

Gigaton may suspend Customer's access immediately, without prior notice, if (a) Customer's use poses a security or operational risk to the Service or other customers, (b) Customer violates the Acceptable Use Policy, (c) Customer is delinquent on payment beyond the grace period in Section 8.3, or (d) suspension is required by applicable law or legal process.

### 13.5 Effect of Termination

Upon termination, (a) Customer's access to the Service ends, (b) Customer's outstanding payment obligations survive, (c) Customer may export Customer Data within the 30-day grace period under Section 7.5, and (d) Sections 6.2, 7, 9, 10, 11.3, 12, 13.5, 14, 15, 16, 17, and 18 survive.

## 14. Indemnification

### 14.1 By Gigaton

Gigaton will defend Customer against any third-party claim that the Service, as provided by Gigaton and used in accordance with these Terms, directly infringes such third party's U.S. or Mexican intellectual property right, and will pay damages finally awarded against Customer (or amounts in settlement approved by Gigaton). Gigaton's obligations do not apply to claims arising from (a) Customer Data, (b) Customer's combination of the Service with non-Gigaton products, (c) Generated Output, or (d) Customer's breach of these Terms.

### 14.2 By Customer

Customer will defend Gigaton against any third-party claim arising from (a) Customer Data, (b) Customer's use of the Service in violation of these Terms or applicable law, (c) Customer's use of Generated Output, or (d) Customer's breach of representations or warranties.

### 14.3 Indemnification Process

The indemnified party must (i) promptly notify the indemnifying party in writing, (ii) give the indemnifying party sole control of the defense and settlement, and (iii) provide reasonable assistance at the indemnifying party's expense.

## 15. Governing Law and Dispute Resolution

### 15.1 Governing Law

These Terms are governed by the laws of the State of Delaware, United States, without regard to its conflict-of-laws rules, except as superseded by mandatory provisions of Mexican law for Customers domiciled in Mexico.

[PARALEGAL: confirm Delaware vs alternative US state (Texas, California) — confirm whether Mexico LFPC consumer-protection carve-out should be more specific for MX-resident customers.]

### 15.2 Informal Dispute Resolution

Before initiating arbitration, the parties agree to attempt to resolve any dispute informally for 60 days following written notice.

### 15.3 Binding Arbitration; Class-Action Waiver

ANY DISPUTE NOT RESOLVED INFORMALLY WILL BE RESOLVED BY FINAL AND BINDING INDIVIDUAL ARBITRATION ADMINISTERED BY [PARALEGAL: confirm arbitration forum — AAA Commercial Rules vs JAMS vs other; venue: Wilmington DE? Mexico City for MX customers?]. **THE PARTIES WAIVE ANY RIGHT TO PARTICIPATE IN A CLASS, COLLECTIVE, OR REPRESENTATIVE ACTION.** [PARALEGAL: confirm enforceability of class-action waiver in target jurisdictions — California recent cases on PAGA carve-outs; Mexico class-action statute Art. 578 Federal Code of Civil Procedure.]

### 15.4 Exceptions to Arbitration

Either party may bring an action in court (a) to seek injunctive relief for infringement of intellectual property rights, (b) to recover undisputed amounts owed, or (c) in small-claims court for individual claims within that court's jurisdiction.

### 15.5 Opt-Out

Customer may opt out of the arbitration agreement in Section 15.3 by sending written notice to `legal@gigaton.ai` within 30 days of first accepting these Terms, including Customer's name, account email, and an unequivocal statement of intent to opt out.

[PARALEGAL: confirm 30-day opt-out window is sufficient under FAA case law; some courts have required longer.]

## 16. Changes to these Terms

Gigaton may modify these Terms by posting a revised version at `gigaton.ai/legal/tos` and updating the "Last Updated" date. Material changes will be communicated at least 30 days in advance by email to the Account's billing contact. Continued use after the effective date constitutes acceptance. If Customer does not accept the changes, Customer's exclusive remedy is to terminate the Account before the effective date.

## 17. Notices

Notices to Gigaton must be sent to `legal@gigaton.ai` (TODO: confirm) with a copy to: [PARALEGAL: insert registered-agent / legal-notices physical address].

Notices to Customer will be sent to the email address on Customer's Account.

## 18. Miscellaneous

### 18.1 Entire Agreement

These Terms, together with the documents incorporated by reference, constitute the entire agreement between the parties regarding the subject matter and supersede all prior agreements.

### 18.2 Severability

If any provision is held unenforceable, the remaining provisions remain in full effect, and the unenforceable provision will be modified to the minimum extent necessary to make it enforceable.

### 18.3 No Waiver

A party's failure to enforce a provision is not a waiver of its right to do so later.

### 18.4 Assignment

Customer may not assign these Terms without Gigaton's prior written consent. Gigaton may assign these Terms in connection with a merger, acquisition, reorganization, or sale of substantially all of its assets.

### 18.5 Force Majeure

Neither party is liable for failures or delays caused by events beyond its reasonable control (acts of God, natural disasters, war, terrorism, civil unrest, government action, internet or cloud-infrastructure failures, etc.).

### 18.6 Relationship

The parties are independent contractors. These Terms do not create any partnership, joint venture, agency, or employment relationship.

### 18.7 Export Compliance

Customer represents that it is not located in, under the control of, or a national of any country subject to U.S. export-restriction sanctions, and that Customer will not use the Service in violation of U.S. export-control laws.

### 18.8 U.S. Government End Users

The Service is "commercial computer software" under FAR 12.212 and DFARS 227.7202; U.S. government end users acquire only the rights set forth herein.

### 18.9 Language

These Terms are executed in English. A Spanish-language translation may be provided as a courtesy for Mexican Customers, but in the event of conflict, the English version controls. [PARALEGAL: confirm enforceability in Mexico — LFPC and PROFECO consumer-protection statutes may require Spanish-controlling language for B2C; B2B may differ.]

---

## Contact

Gigaton AI
Email: legal@gigaton.ai (TODO: confirm)
Privacy inquiries: privacy@gigaton.ai (TODO: confirm)
Security inquiries: security@gigaton.ai (TODO: confirm)
Address: [PARALEGAL: insert registered-agent address]

---

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
