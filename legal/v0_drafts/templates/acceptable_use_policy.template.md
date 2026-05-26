---
entity: {{ENTITY_NAME}}
entity_legal_name: {{ENTITY_LEGAL_NAME}}
doc_type: acceptable_use_policy
template_version: v0.1.0
template_source: legal/v0_drafts/templates/acceptable_use_policy.template.md
instance_status: PENDING-PARALEGAL-REVIEW
effective_date: {{EFFECTIVE_DATE}}
last_reviewed: {{LAST_REVIEWED}}
contact: {{ENTITY_CONTACT_EMAIL}}
entity_type: {{ENTITY_TYPE}}
related_docs:
  - terms_of_service.md
  - privacy_policy.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> Instantiated from `legal/v0_drafts/templates/acceptable_use_policy.template.md`.

# {{ENTITY_NAME}} — Acceptable Use Policy

**Effective Date:** {{EFFECTIVE_DATE}}
**Last Updated:** {{LAST_REVIEWED}}

This Acceptable Use Policy ("**AUP**") governs your use of {{ENTITY_BUSINESS_DESCRIPTION}} (the "**Service**") and is incorporated by reference into the [Terms of Service](terms_of_service.md). Violation of this AUP is a material breach of the Terms and may result in immediate suspension or termination.

## 1. Prohibited Content

You must not use the Service to upload, generate, store, transmit, or distribute content that:

(a) is unlawful, defamatory, fraudulent, deceptive, obscene, or invasive of another's privacy;
(b) infringes any third party's intellectual property or proprietary rights;
(c) depicts or facilitates child sexual abuse material (CSAM), violent extremism, terrorism financing, or human trafficking;
(d) constitutes harassment, threats, doxxing, stalking, or non-consensual intimate imagery;
(e) discriminates against protected classes in housing, lending, employment, credit, education, or public accommodation in violation of applicable law;
(f) impersonates any person or entity in a manner intended to deceive;
(g) contains malware, ransomware, or any code designed to disrupt or gain unauthorized access to systems.

## 2. Prohibited Conduct

You must not:

(a) probe, scan, or test the vulnerability of the Service without prior written authorization;
(b) bypass, disable, or circumvent rate limits, security measures, authentication, or access controls;
(c) conduct denial-of-service attacks or generate traffic designed to overload the Service;
(d) scrape, harvest, or mass-extract data from the Service except via documented APIs in accordance with their rate limits;
(e) use the Service to send unsolicited bulk email (UBE), SMS, WhatsApp messages, or other communications in violation of CAN-SPAM, TCPA, Mexican LFPDPPP marketing-consent rules, or platform-specific policies (Twilio, WhatsApp Business, Meta);
(f) submit knowingly false or misleading information to the Service;
(g) use the Service in any manner that violates U.S. or Mexican export-control laws, sanctions, or anti-corruption laws.

## 3. AI-Specific Restrictions

You must not use the Service or any Generated Output to:

(a) generate content that impersonates a real person without that person's consent;
(b) generate or distribute election disinformation, deepfakes, or synthetic media in violation of applicable election or media law;
(c) train, fine-tune, or distill any competing foundation model or large language model;
(d) automate decisions in domains where applicable law requires human review or specific procedural safeguards (e.g., employment screening, credit decisions, housing rental decisions, healthcare diagnoses) without ensuring such safeguards are in place;
(e) circumvent the safety filters or content moderation of any AI Subprocessor.

[PARALEGAL: confirm AI-specific restriction list is current with NYC AEDT, CA ADMT, Colorado AI Act, and FTC guidance on impersonation.]

## 4. Communications Channels

When the Service sends messages on your behalf via SMS, WhatsApp, email, or social DMs, you represent that:

(a) you have obtained valid express consent from each recipient consistent with TCPA (US), CAN-SPAM (US), MX LFPDPPP, and platform-specific (Twilio, WhatsApp Business Platform, Meta) policies;
(b) all messages include accurate sender identification and a working opt-out mechanism where required;
(c) you will honor opt-out requests promptly (within 10 business days under CAN-SPAM; immediately for transactional confirmations).

{% if ENTITY_TYPE == 'marketing_agency' %}
### 4.1 Audience List Hygiene

For audience or customer lists uploaded for ad targeting, you represent that each list-member's data was collected with the legal basis required for the intended use (including for "matched audience" or "custom audience" uploads to Meta, Google, TikTok, LinkedIn).
{% endif %}

{% if ENTITY_TYPE == 'tour_operator' %}
### 4.2 In-Person Recording

If you record audio or video during an Experience, you must obtain consent consistent with two-party-consent jurisdictions (including Mexico) and post visible notice at recording locations.
{% endif %}

## 5. Resource and Cost Limits

(a) You must not exceed published rate limits or quotas.
(b) You must not use the Service to consume disproportionate AI tokens, compute, or storage in a manner inconsistent with your subscription tier or SOW.
(c) You authorize {{ENTITY_NAME}} to throttle or temporarily restrict your access if your usage causes operational or cost anomalies pending notice and resolution.

## 6. Connector and Integration Rules

When you connect a third-party service (e.g., Google Drive, Twilio, Stripe, Meta, Airbnb), you represent that you are authorized to do so and that your use through the Service complies with that third party's terms. You are responsible for revoking access via the third party if you no longer authorize that integration.

{% if ENTITY_TYPE == 'property_management' or ENTITY_TYPE == 'real_estate_consolidated' %}
## 7. OTA-Channel Compliance

You must not use the Service in any manner that violates the terms of an OTA partner (Airbnb, Booking.com, Vrbo, etc.), including by manipulating reviews, evading platform fees, conducting off-platform bookings in violation of the OTA's policies, or scraping the OTA's interfaces beyond what its API permits.

[PARALEGAL: confirm AUP alignment with Airbnb Host Terms, Booking.com Partner Terms, Vrbo Partner Agreement — material for OTA suspension risk.]
{% endif %}

{% if ENTITY_TYPE == 'affiliate_solo_operator' %}
## 7. Affiliate-Specific Conduct

As a Gignet Affiliate, you must additionally:

(a) accurately represent your relationship to the Gigaton platform; do not claim to be employed by or partnered with Gigaton AI beyond your Affiliate status;
(b) not use the Gigaton brand outside the limited license set forth in the [Gignet Affiliate Addendum](gignet_affiliate_addendum.md);
(c) not solicit other Gigaton customers as your downstream customers in a manner that interferes with their direct relationship with Gigaton AI.
{% endif %}

## 8. Reporting Abuse

To report a suspected violation of this AUP, contact `{{ENTITY_CONTACT_EMAIL}}` with the subject line "AUP REPORT" and reasonable detail. {{ENTITY_NAME}} investigates reports in good faith but does not guarantee a specific outcome.

## 9. Enforcement

{{ENTITY_NAME}} may, in its reasonable discretion:

(a) require Customer to remedy a violation within a stated period;
(b) suspend access immediately for material or repeated violations;
(c) terminate the Account for egregious or uncured violations;
(d) cooperate with law enforcement where required.

## 10. Changes

{{ENTITY_NAME}} may update this AUP from time to time. The current version is always posted at `{{ENTITY_DOMAIN}}/legal/aup`.

---

*Generated from `legal/v0_drafts/templates/acceptable_use_policy.template.md` v0.1.0. Last reviewed: {{LAST_REVIEWED}}. Status: PENDING-PARALEGAL-REVIEW.*
