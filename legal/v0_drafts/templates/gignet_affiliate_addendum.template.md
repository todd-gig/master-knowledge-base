---
entity: {{ENTITY_NAME}}
entity_legal_name: {{ENTITY_LEGAL_NAME}}
doc_type: gignet_affiliate_addendum
template_version: v0.1.0
template_source: legal/v0_drafts/templates/gignet_affiliate_addendum.template.md
instance_status: PENDING-PARALEGAL-REVIEW
effective_date: {{EFFECTIVE_DATE}}
last_reviewed: {{LAST_REVIEWED}}
contact: {{ENTITY_CONTACT_EMAIL}}
entity_type: {{ENTITY_TYPE}}
applicability: "Mandatory when ENTITY_TYPE == 'affiliate_solo_operator'; optional include-by-reference when a saas_platform entity runs an affiliate program."
related_docs:
  - terms_of_service.md
  - privacy_policy.md
  - acceptable_use_policy.md
  - data_processing_addendum.md
---

> # v0 DRAFT — PENDING PARALEGAL REVIEW — NOT TO BE PUBLISHED AS-IS
>
> Instantiated from `legal/v0_drafts/templates/gignet_affiliate_addendum.template.md`.
> This addendum is **mandatory** for every entity instantiated with
> `ENTITY_TYPE == affiliate_solo_operator`. It supplements (and where it
> conflicts, controls over) that entity's [Terms of Service](terms_of_service.md)
> for matters specifically governed by the Gignet program.

# Gignet Affiliate Addendum

**Effective Date:** {{EFFECTIVE_DATE}}
**Last Updated:** {{LAST_REVIEWED}}
**Affiliate:** {{ENTITY_LEGAL_NAME}} (the "**Affiliate**")
**Platform Operator:** Gigaton AI ("**Gigaton**")
**Affiliate Domain:** {{ENTITY_DOMAIN}}
**Affiliate Contact:** {{ENTITY_CONTACT_EMAIL}}

---

## 1. Relationship to Gigaton

The Affiliate is an **independent contractor** that has been admitted to the Gignet affiliate program ("**Program**"). The Affiliate uses the Gigaton platform as a **sub-processor** to deliver services to the Affiliate's own customers ("**Downstream Customers**"). Nothing in this addendum creates a partnership, joint venture, employment, agency, or franchise relationship between the Affiliate and Gigaton.

The Affiliate is solely responsible to its Downstream Customers; Gigaton has no privity with, and no direct obligations to, Downstream Customers except as a sub-processor under the Affiliate's own data-processing agreements.

[PARALEGAL: confirm classification of Affiliate as independent contractor (not franchisee) — review against US franchise-disclosure rules (FTC Franchise Rule) + state franchise registration where applicable; review against MX commercial-representation law.]

## 2. Affiliate Eligibility and Onboarding

To maintain Affiliate status, the Affiliate must continuously meet the following:

(a) be a registered legal entity in good standing in the Affiliate's jurisdiction;
(b) operate from a domain the Affiliate owns or lawfully controls (`{{ENTITY_DOMAIN}}`);
(c) maintain a business-class email account on that domain (`{{ENTITY_CONTACT_EMAIL}}` — gmail/hotmail/yahoo/outlook addresses are not permitted for Program correspondence);
(d) complete identity verification (KYC) via Stripe Connect or an equivalent process designated by Gigaton;
(e) maintain a current Privacy Policy, Terms of Service, and AUP applicable to Downstream Customers;
(f) comply with all applicable laws including tax, anti-money-laundering, sanctions, and data-protection law.

Gigaton may suspend or terminate Affiliate status if any of these lapse.

## 3. License to Use the Gigaton Brand

Gigaton grants the Affiliate a non-exclusive, non-transferable, non-sublicensable, revocable license, during the term of the Program, to use the marks "Gigaton," "Gignet," and the Gigaton logo solely to:

(a) factually identify the Affiliate as a "Gignet Affiliate" or "Powered by Gigaton" on the Affiliate's website, marketing materials, and customer-facing pages;
(b) use Gigaton-supplied marketing assets as published in the Affiliate portal, in unaltered form.

The Affiliate must **not**:

(a) use the Gigaton or Gignet marks as part of the Affiliate's own product name, company name, domain name, social-media handle, or trademark filings;
(b) state or imply that Gigaton endorses the Affiliate's specific advice, recommendations, or business outcomes;
(c) use the Gigaton or Gignet marks in any manner that disparages Gigaton or in connection with content prohibited by the Acceptable Use Policy.

Goodwill arising from the Affiliate's use of the marks accrues to Gigaton.

[PARALEGAL: confirm trademark-license scope is sufficient to protect mark + avoid naked-license claim; recommend quality-control checkpoints.]

## 4. Revenue Share and Payouts

Revenue share is calculated as a percentage of net subscription revenue actually collected from the Affiliate's referred or operated accounts on the Gigaton platform, net of refunds, chargebacks, credits, taxes, payment-processing fees, and any AI/compute pass-through costs.

The current revenue-share percentages, tier qualifications, and payout cadence are published in the Affiliate portal at `gigaton.ai/affiliate/economics` and may be updated by Gigaton on **30 days' advance notice**.

Payouts are made via **Stripe Connect** to the Affiliate's connected account, monthly, on or about the 15th of the following month, subject to a minimum payout threshold and to KYC compliance. Stripe Connect fees and reserves apply per Stripe's terms.

[PARALEGAL: confirm revenue-share structure does not trigger broker-dealer / securities concerns; confirm classification of payout for US tax (1099) + MX tax reporting; recommend annual review of FTC influencer/affiliate disclosure rules.]

## 5. Affiliate Responsibility to Downstream Customers

The Affiliate is solely responsible for:

(a) all contractual relationships with Downstream Customers (terms, privacy, data-processing agreement);
(b) collection and remittance of all applicable taxes on the Affiliate's services to Downstream Customers (Gigaton handles only platform-level Stripe-Tax for Gigaton's own subscription fee, not for the Affiliate's invoiced services);
(c) responding to Downstream-Customer support inquiries, complaints, refund requests, and data-subject requests;
(d) maintaining adequate insurance (recommended: general liability + cyber/errors-and-omissions);
(e) providing accurate disclosures to Downstream Customers about AI processing (the Affiliate may incorporate Gigaton's standard AI-disclosure language by reference).

In its agreements with Downstream Customers, the Affiliate must (i) list Gigaton AI as a sub-processor, (ii) impose data-protection obligations no less protective than those in Gigaton's [Data Processing Addendum](data_processing_addendum.md), and (iii) require Downstream-Customer consent to such sub-processing.

[PARALEGAL: confirm flow-down of sub-processor obligations is adequate; review against CCPA Service-Provider chain + LFPDPPP Article 36 cross-border transfer requirements.]

## 6. Compliance Obligations

The Affiliate must:

(a) comply with the Gigaton [Acceptable Use Policy](acceptable_use_policy.md);
(b) not represent or guarantee specific business outcomes from use of Gigaton;
(c) not engage in deceptive marketing, false comparison advertising, or affiliate-spamming practices;
(d) comply with the FTC's Endorsement Guides (16 CFR Part 255) — clearly disclose the Affiliate's material relationship with Gigaton wherever applicable;
(e) not solicit other Gigaton customers (whose direct relationship is with Gigaton) to migrate to the Affiliate.

## 7. Confidentiality

The Affiliate may receive non-public information about Gigaton's roadmap, pricing, customers, or operations. The Affiliate must treat such information as confidential and use it solely to operate as an Affiliate. Confidentiality obligations survive termination for 3 years (perpetual for trade secrets).

## 8. Term and Termination

This addendum commences on the Effective Date and continues until terminated. Either party may terminate:

(a) **For convenience**, on 30 days' written notice;
(b) **For cause**, immediately on written notice for material breach uncured within 14 days, for the Affiliate's loss of eligibility (Section 2), for violation of the AUP, or for any conduct materially damaging to the Gigaton brand;
(c) **Effective immediately** if the Affiliate is the subject of a regulatory action, criminal indictment, sanctions designation, or insolvency proceeding materially affecting the Affiliate's ability to operate.

### 8.1 Effect of Termination

Upon termination:

(a) the Affiliate's brand license under Section 3 immediately terminates; the Affiliate must remove all uses of the Gigaton/Gignet marks within 14 days;
(b) Gigaton will pay any earned but unpaid revenue share through the termination date, less any chargebacks, refunds, and clawbacks for the standard chargeback-risk window (180 days);
(c) the Affiliate's existing Downstream-Customer relationships continue per the Affiliate's own agreements; Gigaton may, at its discretion, offer continuity of the underlying platform to Downstream Customers directly if the Affiliate is unable or unwilling to continue serving them;
(d) Sections 5, 6, 7, 9, and 10 survive.

[PARALEGAL: confirm post-termination Downstream-Customer "rescue" right — material for customer-continuity scenarios; should disclose to Affiliate at signup.]

## 9. Indemnification and Liability

The Affiliate will defend and indemnify Gigaton against any third-party claim arising from (a) the Affiliate's services to Downstream Customers, (b) the Affiliate's breach of this addendum or applicable law, (c) the Affiliate's marketing or representations, or (d) Downstream-Customer data the Affiliate routes through the Gigaton platform.

Each party's liability under this addendum is subject to the limitation-of-liability provisions of the underlying [Terms of Service](terms_of_service.md).

## 10. Miscellaneous

### 10.1 Order of Precedence
In the event of conflict: (1) this addendum, (2) the Terms of Service, (3) the AUP, (4) the Privacy Policy, (5) the DPA, (6) materials published in the Affiliate portal.

### 10.2 Changes
Gigaton may modify this addendum by posting a revised version at `gigaton.ai/legal/gignet_affiliate_addendum` and notifying the Affiliate by email; material changes are effective 30 days after notice.

### 10.3 Assignment
The Affiliate may not assign without Gigaton's prior written consent (not to be unreasonably withheld for a sale of substantially all Affiliate assets in good standing).

### 10.4 Governing Law and Dispute Resolution
Governed by, and subject to the dispute-resolution provisions of, the underlying Terms of Service.

---

## Contact

Gigaton AI — Program Operations
Affiliate program email: `affiliates@gigaton.ai` (TODO: confirm)
General: `legal@gigaton.ai`

---

*Generated from `legal/v0_drafts/templates/gignet_affiliate_addendum.template.md` v0.1.0. Last reviewed: {{LAST_REVIEWED}}. Status: PENDING-PARALEGAL-REVIEW.*
