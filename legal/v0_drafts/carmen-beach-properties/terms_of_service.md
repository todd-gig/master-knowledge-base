---
entity: Carmen Beach Properties
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
> Carmen Beach Properties is an operator entity (short-term vacation rental property management in Playa del Carmen, Mexico) that uses **Gigaton AI** as its underlying technology platform (sub-processor relationship). These Terms are intended for two audiences: **(1) Guests** who book a stay at a managed property, and **(2) Owners** who entrust property inventory to Carmen Beach Properties for management. The two audiences receive overlapping but distinct sets of rights and obligations; clauses marked **[GUEST]** or **[OWNER]** apply specifically.
>
> Look for `[PARALEGAL: …]` markers throughout — Mexican consumer protection (LFPC + PROFECO), short-term-rental regulations specific to Quintana Roo state, and US state consumer protection (CCPA + state-specific) all apply.

# Carmen Beach Properties — Terms of Service

**Effective Date:** 2026-05-26
**Last Updated:** 2026-05-25
**Operator:** Carmen Beach Properties ("**Carmen Beach**," "**we**," "**us**," "**our**")
**Domain:** carmenbeach.com
**Contact:** legal@gigaton.ai (TODO: confirm a dedicated `legal@carmenbeach.com` alias)

---

## 1. Acceptance

These Terms of Service ("**Terms**") form a binding agreement between you ("**you**," "**your**," and (where applicable) "**Guest**" or "**Owner**") and Carmen Beach Properties. By booking a stay, listing or entrusting property inventory, creating an account, or otherwise using our services (the "**Services**"), you agree to these Terms, the [Privacy Policy](privacy_policy.md), the [Acceptable Use Policy](acceptable_use_policy.md), and (for Owners) the [Data Processing Addendum](data_processing_addendum.md), each incorporated by reference.

If you do not agree, do not use the Services. If you are accepting on behalf of an entity, you represent that you have authority to bind that entity.

[PARALEGAL: confirm clickwrap acceptance enforceability under Mexican consumer protection (LFPC) for B2C Guest bookings; confirm whether a Spanish-language "Términos y Condiciones" pop-up is required at booking-confirmation step.]

## 2. Geographic Scope and Excluded Jurisdictions

The Services are offered to and intended for use by Guests located in the United States, Mexico, Canada, and Latin American countries other than those listed in this Section. We **do not knowingly accept bookings from, market to, or process payments from** Guests residing in the European Union, the European Economic Area, the United Kingdom, or Switzerland during our v1 beta period (the "**Excluded Jurisdictions**"). By making a booking, you represent that you are not domiciled in an Excluded Jurisdiction.

For Owners, the Services are offered only to Owners of property located in Mexico (Quintana Roo and adjacent states), regardless of the Owner's domicile, **provided the Owner is not domiciled in an Excluded Jurisdiction**.

[PARALEGAL: confirm legality of EU-Guest exclusion in light of (1) EU consumer-rights regulations on cross-border bookings, (2) practical impossibility of perfectly geo-fencing inquiries to a Mexico-located physical property, and (3) industry-norm practice (most boutique STVR operators do accept EU bookings — confirm whether risk-bounded exclusion is the right beta posture vs. accepting with EU-compliant terms).]

## 3. Definitions

- **"Guest"** means an individual who books or seeks to book a stay at a Carmen Beach managed property.
- **"Owner"** means an individual or entity that entrusts a property to Carmen Beach for management under a separate Property Management Agreement ("**PMA**").
- **"Property"** means a vacation rental unit managed by Carmen Beach, located in Playa del Carmen or nearby in Quintana Roo, Mexico.
- **"Stay"** means a Guest's authorized occupancy of a Property under a confirmed booking.
- **"Platform"** means the website at `carmenbeach.com`, the owner portal, the WhatsApp concierge channel, and related software used to deliver the Services.
- **"Gigaton Sub-processor"** means Gigaton AI, the underlying technology platform that powers the Platform (see Section 10).

## 4. The Services

### 4.1 For Guests

We offer:
- Listing and booking of Properties for short-term stays;
- Concierge support during the Stay (WhatsApp-first, Spanish + English);
- Pre-arrival communications, check-in instructions, and in-stay support;
- Payment processing via Stripe (under the Gigaton AI platform Stripe account);
- Optional add-ons (cleaning, transportation, experiences) where offered.

### 4.2 For Owners

We offer:
- Property marketing, distribution to OTAs (Airbnb, Vrbo, Booking.com) and direct channels;
- Dynamic pricing, calendar management, channel sync;
- Guest acquisition, booking management, concierge service to Guests;
- Cleaning, maintenance coordination, and on-the-ground operations;
- Owner reporting, monthly statements, and net-to-owner payouts;
- Use of the Gigaton AI platform for data-driven property analytics.

The detailed scope, commission rate, and term for each Owner are set forth in the separately executed PMA. These Terms are general; the PMA controls in case of conflict for Owner-specific matters.

[PARALEGAL: confirm that a separate PMA template is on file; recommend the PMA includes (1) commission % (default 20%), (2) reserve fund for repairs, (3) inventory list, (4) termination terms, (5) exclusivity, (6) Owner indemnification re: title/permits, (7) Mexican law compliance attestation including STR permits and SAT (RFC) registration.]

## 5. Booking, Payment, and Cancellation [GUEST]

### 5.1 Booking

A Stay is confirmed only when (a) you complete the booking flow on carmenbeach.com (or an authorized OTA channel), (b) you receive a written confirmation email from Carmen Beach, and (c) the booking deposit or full payment is successfully captured by Stripe.

We reserve the right to decline any booking at our discretion (subject to applicable non-discrimination laws) and to cancel a booking before the Stay begins for verified force-majeure events, government-ordered restrictions, or material misrepresentation by the Guest.

### 5.2 Payment

All payments are processed by **Stripe, Inc.** under Gigaton AI's platform Stripe account. By providing payment information, you authorize Carmen Beach (via Gigaton's platform via Stripe) to charge the designated payment method. Prices are stated in U.S. Dollars (USD) by default; conversion to Mexican Pesos (MXN) at the time of charge is per Stripe's exchange rate.

**Taxes.** Stripe Tax automatically calculates and collects applicable Mexican VAT (IVA), Mexican lodging taxes (ISH where applicable to short-term rentals in Quintana Roo), and U.S. state or local taxes where required. The Guest is responsible for any taxes that cannot be automatically collected.

[PARALEGAL: confirm Quintana Roo lodging tax (Impuesto al Hospedaje) treatment for short-term rentals; confirm Stripe Tax has the right registrations in MX (RFC, SAT obligations) or whether Carmen Beach itself needs RFC + monthly DIOT filings; this is a material compliance question for Mexican operations.]

### 5.3 Security deposit

For most Properties, a refundable security deposit (typically $300 USD) is authorized as a hold on the Guest's payment method or charged and refunded post-Stay. The deposit may be used to cover documented damages, excessive cleaning, lost keys, missing inventory, or violations of house rules. Any non-refunded portion will be itemized in writing within 14 days of departure.

### 5.4 Cancellation policy

[PARALEGAL: insert per-Property or operator-default cancellation policy. Recommended default:
- **Free cancellation**: 30+ days before check-in → 100% refund minus payment-processor fees.
- **Partial refund**: 14-29 days before check-in → 50% refund.
- **No refund**: < 14 days before check-in → 0% refund (Guest may seek travel-insurance recovery).
- **Force majeure**: government-ordered travel restrictions, natural disasters affecting the Property → full refund or rebooking credit.

Confirm that this default is compatible with Mexican consumer protection (LFPC) — PROFECO has issued opinions disfavoring strict no-refund clauses; recommend including a clear "right to cancel within X hours of booking" clause + force-majeure floor.]

### 5.5 Modifications

You may request a modification (date change, guest count, etc.) up to 14 days before check-in, subject to Property availability and a possible rate adjustment. Approval is at our discretion.

### 5.6 Chargebacks

Initiating a chargeback for a confirmed and delivered Stay without first attempting to resolve the dispute in good faith with us may result in account suspension and additional collection costs.

## 6. Stay Conduct [GUEST]

During the Stay, the Guest agrees:

(a) to use the Property solely for lawful personal residential purposes; **no events, parties, or commercial activity** without prior written consent;
(b) to comply with the house rules provided in the welcome packet (including quiet hours, maximum-occupancy limits, no-smoking rules, pet policies);
(c) to be responsible for the conduct of all persons present at the Property during the Stay;
(d) to promptly report damage, loss, or maintenance issues;
(e) not to sublet, transfer, or share the Property with persons not on the booking;
(f) to comply with all applicable Mexican laws and local regulations, including those governing short-term rentals, condominium / HOA rules, and public conduct;
(g) to obtain own travel insurance — Carmen Beach does not provide travel insurance, evacuation coverage, or medical assistance.

Violations may result in immediate termination of the Stay without refund and recovery of damages from the security deposit and, where damages exceed the deposit, from the Guest directly.

[PARALEGAL: confirm Mexican law on landlord remedies for early termination — Quintana Roo civil code provisions on lease termination; confirm "no-events" clause + occupancy-limit enforcement is consistent with local STR regulations + condo HOA rules typically attached to the Property.]

## 7. Owner Obligations [OWNER]

The Owner represents and warrants:

(a) the Owner has good and marketable title (or equivalent legal authority to lease) for the Property;
(b) the Property complies with all applicable Mexican federal, state (Quintana Roo), and municipal laws, including land-use, condominium, short-term-rental, and tax regulations;
(c) the Owner holds and maintains required permits, licenses, and registrations (SAT/RFC, municipal STR permits where required, condominium-association approvals);
(d) the Property is insured at the Owner's expense for fire, theft, liability, and other reasonably foreseeable risks;
(e) the Owner will provide accurate inventory, condition reports, and disclosures;
(f) the Owner will not separately list the Property on third-party platforms during the term of the PMA without our prior written consent (exclusivity per the PMA);
(g) the Owner will indemnify Carmen Beach for any third-party claim arising out of the Owner's breach of the foregoing.

[PARALEGAL: insurance minima — recommend US$1M general liability + property insurance at replacement value; confirm Mexican condo-level master policies usually exist but typically exclude commercial short-term-rental use, so Owner-level supplemental coverage is required.]

## 8. Owner Payouts [OWNER]

Carmen Beach retains a commission (default **20%**) on net booking revenue (gross booking less Stripe fees, OTA channel fees, taxes collected and remitted, and refunds). The remaining net is paid to the Owner monthly, on or before the 5th of the following month, via wire transfer or Stripe-issued Invoice.

The first three (3) months of Owner payouts are processed **manually** (via wire/SPEI); after that, we may migrate to a Stripe Connect-style automated payout pending Owner consent and KYC.

Monthly Owner statements include: gross bookings, channel breakdown, refunds, commission, expenses (cleaning, maintenance), and net payout.

[PARALEGAL: confirm tax treatment of Owner payouts — Carmen Beach is paying a Mexican Owner from a Stripe account ultimately under Gigaton's US legal entity. Cross-border SAT withholding implications? RFC of Owner required? Recommend tax-counsel review.]

## 9. Cleaning, Damage, and House Rules

Cleaning fees are charged per Stay at the rate posted on the Property listing. Excessive cleaning required beyond standard turnover (defined as 2x normal cleaning labor or evidence of major mess) may be charged against the security deposit.

Damage means physical damage to the Property, its furnishings, or inventory beyond ordinary wear and tear. Disputes regarding damage are documented with photos, repair quotes, and Owner sign-off where applicable, and may be referred to Stripe dispute resolution if not resolved bilaterally.

## 10. Use of Gigaton AI as Technology Sub-Processor

Carmen Beach uses the **Gigaton AI** platform (operated by Gigaton AI, a U.S. legal entity; see `gigaton.ai`) as its underlying technology infrastructure. This means:

- Bookings, communications, payments, and operational data flow through Gigaton's systems.
- Gigaton processes data **on Carmen Beach's behalf as a processor / sub-processor**, under the [Data Processing Addendum](data_processing_addendum.md) between Gigaton and Carmen Beach.
- Sub-sub-processors used by Gigaton (Stripe, Twilio for WhatsApp, Anthropic/OpenAI/Google for AI, Google Cloud Platform, Cloudflare) are listed in Gigaton's published Sub-processor list at `gigaton.ai/legal/subprocessors` (TODO: build).

Guests and Owners are informed of this arrangement here and in the [Privacy Policy](privacy_policy.md).

[PARALEGAL: confirm the sub-processor chain is correctly characterized — Carmen Beach (controller) → Gigaton AI (processor) → Stripe/Twilio/Anthropic/etc. (sub-processors); confirm Guest/Owner-level notices are sufficient; confirm whether Mexican LFPDPPP requires explicit consent for cross-border processing to the U.S.]

## 11. AI Processing Disclosure

The Services use AI (via the Gigaton AI platform) for:

(a) WhatsApp concierge responses and message drafting;
(b) pricing recommendations and revenue management;
(c) booking-fit assessment and Guest communications;
(d) summarizing reviews and operational data;
(e) generating property landing-page content.

Where AI is used to communicate directly with a Guest or Owner, we will (i) clearly disclose that the Guest/Owner is interacting with an AI-assisted system, (ii) provide a path to escalate to a human, and (iii) not represent AI-generated content as authored by a specific named human.

You may opt out of AI-driven communications by contacting `concierge@carmenbeach.com` (TODO: confirm); some convenience features may be degraded.

[PARALEGAL: confirm AI disclosure language meets emerging norms (California ADMT, Colorado AI Act) for "consumer-facing AI" — Carmen Beach's WhatsApp concierge bot likely qualifies.]

## 12. Intellectual Property

Carmen Beach (and its licensors, including Gigaton AI) retains all rights in the Platform, including software, design, content, trademarks, photography, and 3D Matterport tours. Owner photography contributed under the PMA is licensed to Carmen Beach for the term of the PMA + a survival period for legacy listings.

Guests may not republish photography or Property listings without prior written consent.

## 13. Warranties and Disclaimers

EXCEPT AS EXPRESSLY STATED, **THE SERVICES AND THE PROPERTIES ARE PROVIDED "AS IS"**. We make no warranty regarding (a) the suitability of a Property for a Guest's particular purpose, (b) availability of utilities or amenities at all times, or (c) freedom from incidental disruptions (construction in the neighborhood, weather events, etc.).

We do not warrant uninterrupted operation of OTA channels, payment processors, or the WhatsApp concierge channel — these depend on third-party platforms.

[PARALEGAL: confirm Mexican consumer-protection (LFPC) allows the AS-IS disclaimer for B2C; LFPC tends to be stricter than US — recommend a "minimum-fitness" carve-out for Mexican B2C Guests.]

## 14. Limitation of Liability

TO THE MAXIMUM EXTENT PERMITTED BY LAW, IN NO EVENT WILL CARMEN BEACH (OR ITS PERSONNEL, LICENSORS, OR SUB-PROCESSORS INCLUDING GIGATON AI) BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, INCLUDING LOST PROFITS, PERSONAL INJURY (except where caused by Carmen Beach's gross negligence or willful misconduct), OR EMOTIONAL DISTRESS.

OUR TOTAL CUMULATIVE LIABILITY IS LIMITED TO THE GREATER OF (A) THE TOTAL AMOUNT PAID BY YOU FOR THE BOOKING GIVING RISE TO THE CLAIM, OR (B) US$500.

Personal-injury and property-damage claims at the Property are governed by the Owner's insurance and applicable Mexican law; Carmen Beach is not the insurer.

[PARALEGAL: confirm liability cap enforceability under Mexican B2C law; Mexican PROFECO/LFPC has invalidated abusive limitation clauses; recommend higher floor + carve-out for gross negligence/willful misconduct.]

## 15. Indemnification

### 15.1 By Guest

Guest will indemnify Carmen Beach (and the Owner) from claims arising from (a) damage caused by Guest or Guest's invitees, (b) Guest's violation of these Terms or house rules, (c) Guest's violation of applicable law, and (d) personal-injury claims attributable to Guest conduct.

### 15.2 By Owner

Owner will indemnify Carmen Beach from claims arising from (a) defects in title, permits, or insurance, (b) violations of Mexican STR regulations or condo/HOA rules, (c) personal-injury claims attributable to Property condition, and (d) breach of Owner representations.

### 15.3 By Carmen Beach

We will defend you against third-party claims that our Services (as we provide them) directly infringe such third party's intellectual property right, subject to standard exclusions (Customer Data, combinations, modifications).

## 16. Term, Suspension, Termination

### 16.1 Guest

A Guest relationship begins at booking and ends at departure plus any post-Stay reconciliation period. Either party may cancel before check-in per Section 5.4. We may terminate a Stay in progress for material violation of these Terms or house rules.

### 16.2 Owner

The Owner relationship is governed by the PMA. These Terms continue as long as Owner uses the Services. On PMA termination, Owner Data is treated per Section 17.

### 16.3 Data deletion grace

Following termination of an account or PMA, we retain account data for a **30-day grace period** for export and reconciliation, then delete from production within **60 days** thereafter. See [Privacy Policy](privacy_policy.md) Section 11 for retention exceptions (tax, audit, litigation hold).

## 17. Governing Law and Dispute Resolution

### 17.1 Governing law

(a) For Guest bookings of Properties located in Mexico: **Mexican federal law and the law of Quintana Roo state**.
(b) For Owner relationships: as set forth in the PMA; in the absence of a PMA choice, **Mexican federal law and Quintana Roo state**.
(c) For payment-processing disputes: as governed by Stripe Terms of Service.

[PARALEGAL: confirm governing-law selection enforceability; Mexican-located property + Mexican law for STR transactions is the cleanest path; but limits forum-selection options.]

### 17.2 Informal resolution

The parties agree to attempt informal resolution for 60 days before commencing formal proceedings.

### 17.3 Arbitration

[PARALEGAL: arbitration in Mexico is governed by the Mexican Commercial Code arbitration provisions; CAM Mexico is a common forum. Consider whether arbitration is appropriate for B2C Guest bookings — Mexican PROFECO retains jurisdiction over consumer complaints regardless of arbitration clauses, so arbitration is best framed as supplemental for B2B Owner relationships and excluded for B2C Guests with PROFECO recourse preserved.]

**Class-action waiver:** **THE PARTIES WAIVE ANY RIGHT TO PARTICIPATE IN A CLASS, COLLECTIVE, OR REPRESENTATIVE ACTION**, subject to the enforceability of such waivers under applicable law. [PARALEGAL: confirm — Mexican class-action statute (Art. 578 Federal Code of Civil Procedure) limits enforceability of class waivers.]

### 17.4 PROFECO recourse [GUEST]

For Guests who are consumers (`consumidores`), nothing in these Terms limits your right to seek redress with the **Procuraduría Federal del Consumidor (PROFECO)** or any other Mexican consumer-protection authority.

## 18. Privacy

See the [Privacy Policy](privacy_policy.md). Gigaton AI is our technology sub-processor for data handling; the underlying processor chain and AI processing are described there.

## 19. Changes to these Terms

We may update these Terms; material changes will be posted on `carmenbeach.com/legal/tos` with at least 30 days' notice for active Owner relationships, and at booking time for new Guest relationships. Continued use constitutes acceptance.

## 20. Notices

Notices to Carmen Beach: `legal@gigaton.ai` (TODO: confirm dedicated `legal@carmenbeach.com` alias).
Notices to you: email address on file.
Mexican legal-process address: [PARALEGAL: insert — likely needs Mexican domicilio for service of process].

## 21. Miscellaneous

Severability, no-waiver, assignment, force majeure, independent-contractors, export-compliance, and language provisions apply as in the Gigaton AI Terms of Service Sections 18.1–18.9.

**Language.** These Terms are executed in English. A Spanish translation is provided for convenience at `carmenbeach.com/legal/tos-es`; **for Guests who are Mexican consumers, the Spanish version is binding**; for all others, the English version controls. [PARALEGAL: confirm — Mexican LFPC + PROFECO require Spanish for B2C contracts of adhesion; this is significant.]

---

## Contact

Carmen Beach Properties
Concierge: `concierge@carmenbeach.com` (TODO: confirm)
Legal: `legal@gigaton.ai` (TODO: confirm dedicated alias)
Mexican domicile for service of process: [PARALEGAL: insert]

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
