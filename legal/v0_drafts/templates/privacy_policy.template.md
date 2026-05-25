---
entity: {{ENTITY_NAME}}
entity_legal_name: {{ENTITY_LEGAL_NAME}}
doc_type: privacy_policy
template_version: v0.1.0
template_source: legal/v0_drafts/templates/privacy_policy.template.md
instance_status: PENDING-PARALEGAL-REVIEW
effective_date: {{EFFECTIVE_DATE}}
applicable_jurisdictions: [{{ENTITY_JURISDICTION}}]
excluded_jurisdictions: [EU, EEA, UK, CH]
last_reviewed: {{LAST_REVIEWED}}
contact: {{ENTITY_CONTACT_EMAIL}}
entity_type: {{ENTITY_TYPE}}
related_docs:
  - terms_of_service.md
  - acceptable_use_policy.md
  - data_processing_addendum.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> Instantiated from `legal/v0_drafts/templates/privacy_policy.template.md`.
> Compliance scope: **U.S. (CCPA/CPRA-aligned baseline) + Mexico (LFPDPPP).**
> **EU / EEA / UK / Swiss residents are explicitly excluded in v1.**

# {{ENTITY_NAME}} — Privacy Policy

**Effective Date:** {{EFFECTIVE_DATE}}
**Last Updated:** {{LAST_REVIEWED}}
**Controller:** {{ENTITY_LEGAL_NAME}} ("**{{ENTITY_NAME}}**," "**we**," "**us**," or "**our**")
**Domain:** {{ENTITY_DOMAIN}}
**Contact:** {{ENTITY_CONTACT_EMAIL}}

---

## 1. Scope

This Privacy Policy describes how {{ENTITY_NAME}} collects, uses, discloses, retains, and protects personal information in connection with {{ENTITY_BUSINESS_DESCRIPTION}}. It applies to (a) visitors of `{{ENTITY_DOMAIN}}`, (b) Customers and Authorized Users of the Service, and (c){% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %} Guests and Owners interacting with properties managed by {{ENTITY_NAME}}{% endif %}{% if ENTITY_TYPE == 'tour_operator' %} Guests booking or participating in Experiences{% endif %}{% if ENTITY_TYPE == 'marketing_agency' %} individuals whose data is processed via Customer-granted access to ad platforms and audience lists{% endif %}{% if ENTITY_TYPE == 'affiliate_solo_operator' %} Downstream Customers of the Affiliate (for whom the Affiliate is the controller and {{ENTITY_NAME}} is processor){% endif %}{% if ENTITY_TYPE == 'saas_platform' %} end users of Customer's deployments of the Service{% endif %}{% if ENTITY_TYPE == 'managed_service' %} individuals whose data is included in Customer's engagement scope{% endif %}.

## 2. Geographic Scope

This Policy is designed for compliance with U.S. federal law and the California Consumer Privacy Act / California Privacy Rights Act ("**CCPA/CPRA**") and, for personal data subject to Mexican law, the Ley Federal de Protección de Datos Personales en Posesión de los Particulares ("**LFPDPPP**") and its Reglamento.

The Service is **not offered to residents of the European Union, the European Economic Area, the United Kingdom, or Switzerland** at this time. If you are located in those jurisdictions, please do not provide personal information to {{ENTITY_NAME}}.

## 3. Information We Collect

We collect the following categories of personal information, as applicable to your relationship with {{ENTITY_NAME}}:

{% for category in ENTITY_DATA_CATEGORIES %}
- **{{ category }}** — see Annex A of the [Data Processing Addendum](data_processing_addendum.md) for the full description and purpose.
{% endfor %}

{% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %}
### 3.1 Guest Data Specifically

For each booking, we collect identifying and contact information (name, email, phone), payment data (via Stripe — we do not store card numbers), stay details (check-in / check-out, guest count, special requests), and any government identification required by Mexican federal law (FMM tourist card, passport reference) or applicable hospitality regulation.
{% endif %}

{% if ENTITY_TYPE == 'tour_operator' %}
### 3.1 Voice and In-Shop Chat Recordings

When you interact with {{ENTITY_NAME}} or a Merchant Partner via WhatsApp voice or Instagram voice messaging during an Experience, the audio and any transcripts produced by AI Subprocessors are collected. We provide notice at the point of recording and obtain consent consistent with applicable two-party-consent jurisdictions.

[PARALEGAL: confirm two-party-consent compliance for MX (federal + Quintana Roo state law) and any US state where Guest originates.]
{% endif %}

{% if ENTITY_TYPE == 'marketing_agency' %}
### 3.1 Ad Platform Access and Audience Lists

We process data via OAuth-authorized access to Customer's accounts on third-party advertising platforms (Meta, Google Ads, TikTok, LinkedIn, etc.). Where Customer uploads audience or customer lists for ad targeting, we treat that data as Customer-controlled and act as Customer's processor; we do not retain copies beyond the duration of the engagement and do not use the lists for any other Customer.

[PARALEGAL: confirm CCPA "selling" / "sharing" treatment of ad-platform handoffs — material classification call.]
{% endif %}

{% if ENTITY_TYPE == 'affiliate_solo_operator' %}
### 3.1 Downstream Customer Data

For data of the Affiliate's downstream customers, the Affiliate is the controller and {{ENTITY_NAME}}'s processing is governed by the Affiliate's own privacy notice. {{ENTITY_NAME}} processes such data solely to operate the Service on the Affiliate's behalf.
{% endif %}

## 4. How We Use Information

We use personal information to: (a) provide and operate the Service; (b) authenticate users and secure accounts; (c) communicate with Customers and Authorized Users; (d) process payments via Stripe; (e) produce Generated Output via AI Subprocessors; (f) compute analytics and decisioning; (g) detect, prevent, and respond to fraud and abuse; (h) comply with legal obligations.

## 5. AI Processing

We use AI Subprocessors (currently Anthropic, OpenAI, and Google) to generate content, route decisions, classify data, and personalize outputs. Personal information may be transmitted to these AI Subprocessors solely to perform a Customer-requested task. We rely on contractual commitments that such information is not used to train foundation models absent explicit opt-in.

Disclosure level for this entity: **{{ai_processing_disclosure}}**.

Customer or end-user may request alternative human-only processing for specified categories by writing to `{{ENTITY_CONTACT_EMAIL}}`; see Section 7.4 of the [Terms of Service](terms_of_service.md).

[PARALEGAL: confirm AI disclosure satisfies Colorado AI Act + California ADMT proposed regs + emerging state laws.]

## 6. Disclosures to Third Parties

We disclose personal information to:

- **Sub-processors** — see Annex A of the [Data Processing Addendum](data_processing_addendum.md). Specific to this entity: {{ENTITY_SUB_PROCESSORS}}.
- **Service providers** acting under written agreements consistent with this Policy.
- **Legal requirements** — to comply with subpoena, court order, or valid legal process, and to enforce our Terms or protect rights, safety, or property.
- **Business transfers** — in connection with a merger, acquisition, financing, or sale of assets, subject to standard confidentiality protections.

We do **not** sell personal information for monetary consideration. {% if ENTITY_TYPE == 'marketing_agency' %}Certain ad-platform integrations may constitute "sharing" for cross-context behavioral advertising under CCPA/CPRA; Customer (or end-user, as applicable) may opt out via Section 8.{% endif %}

{% if ENTITY_TYPE == 'tour_operator' %}
### 6.1 Merchant Partners

During an Experience, limited Guest information (booking confirmation, time of arrival, party size) may be shared with Merchant Partners to coordinate service. We do not share Guest payment data or government ID with Merchant Partners.
{% endif %}

{% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %}
### 6.1 OTA and Channel Partners

Where a Guest books via an OTA (Airbnb, Booking.com, Vrbo, etc.), the OTA shares booking information with us pursuant to the OTA's own terms. We process such information solely to fulfill the stay and as required by tax, hospitality, and immigration law.
{% endif %}

## 7. Retention

We retain personal information for the period necessary to fulfill the purposes described in Section 4 and to comply with legal obligations:

- Account identifiers: duration of the Account + 30-day grace + 60-day deletion window.
- Billing records: 7 years (US tax + IRS retention; MX SAT 5-year minimum applied conservatively as 7).
- Interaction and AI logs: 24 months default, then anonymized for aggregate analytics.
{% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %}
- Guest stay records: 5 years (MX SAT) or as required by hospitality regulation, whichever is longer.
{% endif %}
{% if ENTITY_TYPE == 'marketing_agency' %}
- Campaign performance data: 24 months for benchmarking; aggregated thereafter.
{% endif %}

## 8. Your Rights

### 8.1 U.S. (CCPA/CPRA-aligned baseline)

If you are a California resident (and, where {{ENTITY_NAME}} extends these rights more broadly, any U.S. resident), you have the right to:

- **Know** what personal information we collect and disclose.
- **Access / Portability** — request a copy.
- **Delete** — request deletion, subject to retention exceptions.
- **Correct** inaccurate personal information.
- **Opt out of sale or sharing** for cross-context behavioral advertising (we do not sell; we may share in limited ad contexts described in Section 6).
- **Limit use of sensitive personal information**.
- **Non-discrimination** — we will not deny service or charge different prices for exercising these rights.

To exercise rights, contact `{{ENTITY_CONTACT_EMAIL}}`. We will respond within 45 days (extendable to 90 with notice). We will verify your identity before fulfilling substantive requests.

### 8.2 Mexico (LFPDPPP)

If your personal data is subject to LFPDPPP, you have the rights of Access, Rectification, Cancellation, and Opposition (the "**ARCO Rights**"), and the right to revoke consent. To exercise ARCO Rights, submit a request in writing to `{{ENTITY_CONTACT_EMAIL}}` including: (i) name and proof of identity; (ii) the right being exercised; (iii) the relevant data; (iv) any documents supporting the request. We will respond within 20 business days. You may also file a complaint with the INAI.

[PARALEGAL: confirm Aviso de Privacidad (full) is published and meets LFPDPPP Article 16 requirements; this Policy is the short-form notice.]

### 8.3 Authorized Agents

You may designate an authorized agent to make requests on your behalf, subject to verification.

## 9. Security

We use commercially reasonable administrative, technical, and physical safeguards including encryption in transit (TLS 1.2+) and at rest, role-based access controls, audit logging, isolated tenant data spaces, and key management via Google Cloud KMS. No system is perfectly secure; we will notify affected persons of security incidents as required by applicable law (CCPA, MX LFPDPPP, US state breach notification statutes).

[PARALEGAL: confirm breach-notice language meets MX LFPDPPP Article 20 + applicable US state-by-state requirements.]

## 10. Children

The Service is not directed to children under 13 (or under 16 in jurisdictions where that is the minimum), and we do not knowingly collect their personal information. If we learn we have done so, we will delete it.

## 11. International Transfers

We are based in the United States. Personal information may be processed in the United States and in other countries where our Sub-processors operate. By using the Service, you acknowledge these transfers. Because the Service is not offered in EU/EEA/UK/Switzerland, GDPR transfer mechanisms do not apply in v1.

{% if 'spanish_language_courtesy' in required_clauses %}
## 12. Language

A Spanish translation of this Policy is provided as a courtesy at `{{ENTITY_DOMAIN}}/legal/privacy/es`. In the event of conflict, the English version controls except where Mexican law requires the Spanish version to control for individual consumers.
{% endif %}

## 13. Changes to this Policy

We may update this Policy. Material changes will be communicated by email and posted with a new effective date at `{{ENTITY_DOMAIN}}/legal/privacy`.

## 14. Contact

{{ENTITY_LEGAL_NAME}}
Privacy inquiries: `{{ENTITY_CONTACT_EMAIL}}`
Domain: `{{ENTITY_DOMAIN}}`

---

*Generated from `legal/v0_drafts/templates/privacy_policy.template.md` v0.1.0. Last reviewed: {{LAST_REVIEWED}}. Status: PENDING-PARALEGAL-REVIEW.*
