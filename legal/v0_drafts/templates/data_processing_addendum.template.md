---
entity: {{ENTITY_NAME}}
entity_legal_name: {{ENTITY_LEGAL_NAME}}
doc_type: data_processing_addendum
template_version: v0.1.0
template_source: legal/v0_drafts/templates/data_processing_addendum.template.md
instance_status: PENDING-PARALEGAL-REVIEW
effective_date: {{EFFECTIVE_DATE}}
applicable_jurisdictions: [{{ENTITY_JURISDICTION}}]
excluded_jurisdictions: [EU, EEA, UK, CH]
last_reviewed: {{LAST_REVIEWED}}
contact: {{ENTITY_CONTACT_EMAIL}}
entity_type: {{ENTITY_TYPE}}
related_docs:
  - terms_of_service.md
  - privacy_policy.md
  - acceptable_use_policy.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> Instantiated from `legal/v0_drafts/templates/data_processing_addendum.template.md`.
> v1 scope: **CCPA/CPRA + LFPDPPP**. **GDPR / UK GDPR do not apply in v1
> because EU/UK customers are excluded.** This DPA is intended to be
> attached to and incorporated into the [Terms of Service](terms_of_service.md).

# {{ENTITY_NAME}} — Data Processing Addendum (DPA)

**Effective Date:** {{EFFECTIVE_DATE}}
**Last Updated:** {{LAST_REVIEWED}}

This DPA forms part of the [Terms of Service](terms_of_service.md) between {{ENTITY_LEGAL_NAME}} ("**{{ENTITY_NAME}}**") and the Customer accepting those Terms ("**Customer**"). To the extent of any conflict between this DPA and the Terms with respect to data-protection obligations, this DPA controls.

## 1. Definitions

- **"Applicable Data Protection Law"** means CCPA/CPRA (California Consumer Privacy Act / California Privacy Rights Act), other U.S. state comprehensive privacy laws (Virginia VCDPA, Colorado CPA, Connecticut CTDPA, Utah UCPA, Texas TDPSA, etc.) to the extent applicable, the U.S. federal laws governing the data category (HIPAA where applicable, GLBA where applicable, COPPA where applicable), and, for personal data subject to Mexican law, the LFPDPPP and its Reglamento.
- **"Customer Personal Information"** means personal information processed by {{ENTITY_NAME}} on behalf of Customer in providing the Service.
- **"Processor"**, **"Service Provider"**, **"Sub-processor"**, **"Personal Information"**, **"Sale"**, and **"Share"** have the meanings given by Applicable Data Protection Law.

## 2. Role of the Parties

{% if ENTITY_TYPE == 'saas_platform' %}
For Customer Personal Information processed via the Service, Customer is the "**Business**" / "controller" / "responsable" (under CCPA / general usage / LFPDPPP respectively) and {{ENTITY_NAME}} acts as Customer's "**Service Provider**" / processor / encargado.
{% endif %}
{% if ENTITY_TYPE == 'managed_service' or ENTITY_TYPE == 'marketing_agency' %}
Customer is the "**Business**" / controller / responsable. {{ENTITY_NAME}} acts as Customer's "**Service Provider**" / processor / encargado in delivering the engagement. {{ENTITY_NAME}} engages Gigaton AI as a sub-processor underlying the Service.
{% endif %}
{% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %}
For Owner data and for Guest data collected directly by {{ENTITY_NAME}}, {{ENTITY_NAME}} acts as a "**Business**" / controller / responsable. For Guest data routed via an OTA where the OTA is the originating controller, {{ENTITY_NAME}} is a joint or independent controller depending on the OTA's terms. {{ENTITY_NAME}} engages Gigaton AI as platform sub-processor.

[PARALEGAL: confirm controller-vs-processor split with each OTA's data-sharing agreement.]
{% endif %}
{% if ENTITY_TYPE == 'tour_operator' %}
{{ENTITY_NAME}} acts as a "**Business**" / controller / responsable for booking and Experience-related data, and as joint controller with Merchant Partners for data shared during an Experience. {{ENTITY_NAME}} engages Gigaton AI as platform sub-processor.
{% endif %}
{% if ENTITY_TYPE == 'affiliate_solo_operator' %}
For data of Downstream Customers, the Affiliate ({{ENTITY_NAME}}) is the controller and Gigaton AI is the platform sub-processor. The Affiliate is solely responsible for its own privacy disclosures and consents with Downstream Customers.
{% endif %}

## 3. Subject Matter and Duration

- **Subject Matter**: processing necessary to provide the Service.
- **Duration**: for the term of the Terms plus the post-termination retention/grace period described in Section 7.5 of the Terms.
- **Nature and Purpose**: as described in the [Privacy Policy](privacy_policy.md) Section 4 and as instructed by Customer.
- **Categories of Personal Information**: see Annex B.
- **Categories of Data Subjects**: see Annex B.

## 4. Customer Instructions

{{ENTITY_NAME}} will process Customer Personal Information only (a) on documented instructions from Customer (including via Customer's use of the Service), (b) as required by Applicable Data Protection Law, or (c) as set forth in this DPA. If {{ENTITY_NAME}} cannot comply with an instruction, it will notify Customer.

## 5. CCPA/CPRA Service-Provider Commitments

When acting as Customer's Service Provider, {{ENTITY_NAME}}:

(a) will not Sell or Share Customer Personal Information;
(b) will not retain, use, or disclose Customer Personal Information for any purpose other than the business purposes specified in the Terms or as permitted under CCPA Regulations §7050(b);
(c) will not retain, use, or disclose Customer Personal Information outside the direct business relationship between {{ENTITY_NAME}} and Customer;
(d) will not combine Customer Personal Information with personal information from other sources except as permitted under CCPA Regulations §7050(b);
(e) will notify Customer if {{ENTITY_NAME}} can no longer meet its obligations under CCPA;
(f) will provide reasonable assistance to Customer in responding to verifiable consumer requests.

[PARALEGAL: confirm CCPA Service-Provider clause meets §1798.140(ag) + §7050 requirements; review on annual basis.]

## 6. LFPDPPP Processor Commitments

When acting as encargado of Customer's personal data subject to LFPDPPP, {{ENTITY_NAME}}:

(a) will process personal data only on the responsable's documented instructions;
(b) will treat the data confidentially under LFPDPPP Article 50;
(c) will implement security measures consistent with LFPDPPP Articles 19 and 20;
(d) will not transfer the data to third parties except sub-processors disclosed in Annex A;
(e) will return or delete the data on termination, subject to legal retention requirements;
(f) will allow audits per Section 9.

[PARALEGAL: confirm LFPDPPP encargado clause meets Article 50 + Reglamento Articles 49–52.]

## 7. Security

{{ENTITY_NAME}} maintains administrative, technical, and physical safeguards proportionate to the risk, including:

- Encryption in transit (TLS 1.2+) and at rest (AES-256 or equivalent via cloud-provider KMS);
- Role-based access controls and least-privilege principles;
- Audit logging of administrative actions;
{% if ENTITY_TYPE == 'saas_platform' %}
- Logical multi-tenant isolation between Customer datasets;
{% endif %}
- Vulnerability management and patch cadence consistent with industry norms;
- Security awareness training for personnel with access to Customer Personal Information;
- Background checks for personnel with privileged access, where lawful.

[PARALEGAL: confirm specific control set against MX LFPDPPP Reglamento Article 61 + relevant US state breach-notification statutes.]

## 8. Sub-processors

{{ENTITY_NAME}} engages the Sub-processors listed in **Annex A** to process Customer Personal Information in connection with the Service. Customer hereby authorizes those Sub-processors.

{{ENTITY_NAME}} will:

(a) impose data-protection obligations on each Sub-processor that are no less protective than those in this DPA;
(b) remain responsible to Customer for Sub-processor performance;
(c) provide Customer with at least **30 days' notice** of a new Sub-processor by updating Annex A and notifying the Account's billing contact;
(d) allow Customer to object to a new Sub-processor on reasonable data-protection grounds; if {{ENTITY_NAME}} cannot accommodate, Customer's exclusive remedy is to terminate the affected portion of the Service.

## 9. Audits

Customer may, upon at least 30 days' written notice and no more than once per 12-month period (absent a security incident), request reasonable information necessary to confirm {{ENTITY_NAME}}'s compliance with this DPA. {{ENTITY_NAME}} will respond by providing the most recent third-party audit report (e.g., SOC 2, ISO 27001) covering the Service, or, if unavailable, a written response to Customer's questions. On-site audits are by mutual agreement and at Customer's expense.

[PARALEGAL: confirm audit clause is reasonable; SaaS norm is documentation-only with on-site by mutual agreement.]

## 10. Data Subject Requests

If {{ENTITY_NAME}} receives a request directly from a data subject regarding Customer Personal Information, {{ENTITY_NAME}} will (a) not respond substantively, (b) promptly forward to Customer, and (c) reasonably assist Customer in responding. Where {{ENTITY_NAME}} acts as controller (e.g., for Owner data in property-management contexts), {{ENTITY_NAME}} responds directly.

## 11. Personal Information Breach Notification

{{ENTITY_NAME}} will notify Customer without undue delay, and in no case later than **72 hours**, after becoming aware of a confirmed personal-information breach affecting Customer Personal Information. The notification will include the information required by Applicable Data Protection Law, to the extent then known.

## 12. International Transfers

{{ENTITY_NAME}} is based in the United States. Customer Personal Information may be processed in the United States and in Mexico and in countries where Sub-processors operate. Because the Service is not offered to EU/EEA/UK/Switzerland data subjects, GDPR transfer mechanisms (SCCs / IDTA) do not apply in v1. For transfers of MX-resident data, {{ENTITY_NAME}} relies on LFPDPPP-compliant mechanisms including the recipient's binding written commitments.

[PARALEGAL: confirm MX cross-border transfer mechanism — LFPDPPP Article 36 + Reglamento Article 74.]

## 13. Return and Deletion

On termination, {{ENTITY_NAME}} will (a) make Customer Personal Information available for export for 30 days, then (b) delete Customer Personal Information from production systems within 60 days, subject to legal-retention exceptions described in the [Privacy Policy](privacy_policy.md).

## 14. Liability

Each party's liability under this DPA is subject to the limitation-of-liability provisions of the Terms.

---

## Annex A — List of Sub-processors

The following Sub-processors are engaged as of {{LAST_REVIEWED}}. Updates are published at `{{ENTITY_DOMAIN}}/legal/sub-processors`.

| Sub-processor | Purpose | Location |
|---|---|---|
{% for sp in ENTITY_SUB_PROCESSORS %}
| {{ sp.name }} | {{ sp.purpose }} | {{ sp.location }} |
{% endfor %}

> When `{{ENTITY_TYPE}}` is not `saas_platform`, **Gigaton AI** is engaged as the underlying platform Sub-processor for orchestration, decisioning, and AI routing.

## Annex B — Categories of Data Subjects and Personal Information

**Categories of Data Subjects:**

{% if ENTITY_TYPE == 'saas_platform' or ENTITY_TYPE == 'managed_service' or ENTITY_TYPE == 'marketing_agency' or ENTITY_TYPE == 'affiliate_solo_operator' %}
- Customer's Authorized Users (employees, contractors of Customer);
- Customer's end-users or downstream customers, to the extent Customer routes their data through the Service.
{% endif %}
{% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %}
- Property Owners;
- Guests (booking through direct or OTA channels);
- Customer-side Authorized Users (e.g., on-site staff).
{% endif %}
{% if ENTITY_TYPE == 'tour_operator' %}
- Experience Guests;
- Merchant-Partner contacts;
- Tour-guide and operational staff.
{% endif %}

**Categories of Personal Information processed:**

{% for category in ENTITY_DATA_CATEGORIES %}
- {{ category }}
{% endfor %}

**Special/Sensitive categories:** Subject to LFPDPPP "datos personales sensibles" treatment and to CCPA/CPRA "sensitive personal information" limitations where applicable. {{ENTITY_NAME}} does not knowingly process biometric or health data except where expressly described in the [Privacy Policy](privacy_policy.md).

---

*Generated from `legal/v0_drafts/templates/data_processing_addendum.template.md` v0.1.0. Last reviewed: {{LAST_REVIEWED}}. Status: PENDING-PARALEGAL-REVIEW.*
