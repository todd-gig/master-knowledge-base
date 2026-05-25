---
title: Entity Comparison Matrix — clause-by-clause differences across the three v0 legal scaffolds
version: v0-draft-2026-05-25
status: PENDING-PARALEGAL-REVIEW
last_reviewed: 2026-05-25
authored_by: AI draft-assistant
---

# Entity Comparison Matrix

This matrix shows where the three entity scaffolds (Gigaton AI / Carmen Beach Properties / Ti Solutions) **converge** and **diverge** clause-by-clause, and **why** the divergences exist. Use this to spot inconsistencies, confirm intentional differences, and route attention.

## Top-line summary

| Dimension | Gigaton AI | Carmen Beach Properties | Ti Solutions |
|---|---|---|---|
| **Business model** | Self-serve SaaS | Vacation rental property management | Managed-service consulting |
| **Sales motion** | Product-led, Stripe Checkout | Direct booking + sales-assisted Owner acquisition | Sales-assisted, MSA + SOW |
| **Counterparty type** | B2B + small businesses (some prosumer) | B2C Guests + B2B Owners | B2B mid-market |
| **Primary payment model** | Subscription + metered overage | Per-booking (Guest), monthly commission (Owner) | One-time setup + monthly retainer + performance |
| **Geographic-scope risk surface** | US + MX nominal; EU-exclusion via geo-fence | US/CA/LatAm Guests + MX-located Properties | US + MX |
| **Spanish-language obligation** | Optional courtesy translation | **Required** for B2C Guests (LFPC) | Optional |
| **Primary regulator beyond US/MX privacy law** | FTC (general), state AGs, Stripe-imposed compliance | PROFECO + SAT + Quintana Roo STR registry + condo HOAs | TCPA enforcers (US courts/FCC), CAN-SPAM (FTC), REPEP (PROFECO) |
| **Controller/Processor role** | Controller for own data; Processor for Customer Data | Controller for Guest/Owner data; uses Gigaton as Processor | Processor for Customer's outbound data; Controller for own sales-funnel data |
| **Liability cap (default)** | Greater of 12-mo fees or US$100 | Greater of booking total or US$500 | Greater of 12-mo SOW fees or US$50,000 |
| **Termination data-deletion window** | 30-day grace + 60-day deletion | 30-day grace + 60-day deletion | 30-day grace + 60-day deletion |
| **Excluded jurisdictions** | EU/EEA/UK/CH | EU/EEA/UK/CH | EU/EEA/UK/CH |

## Convergence — clauses identical or substantively similar across all three

Where the same legal rationale applies, we kept language tight and consistent:

| Clause family | Treatment |
|---|---|
| **Excluded Jurisdictions** | Identical across all three — EU/EEA/UK/CH out for v1 beta. |
| **Sub-processor list** | Gigaton AI is the canonical list; Carmen Beach + Ti Solutions DPAs incorporate by reference. |
| **AI processing disclosure** | Same baseline language — explicit AI use, opt-out where feasible, no foundation-model training of customer data, AI Subprocessors named. |
| **Termination data-deletion window** | 30-day grace + 60-day deletion uniformly. |
| **Class-action waiver** | Same baseline language with `[PARALEGAL: enforceability]` marker. |
| **Effective date / Last updated** | 2026-05-26 / 2026-05-25 across all. |
| **Cookie banner reference** | All three reference Section 12 of the respective Privacy Policy. |
| **Breach notification baseline** | "Without undue delay; within 72 hours of confirmation" — Gigaton + Ti Solutions; Carmen Beach references this through its DPA. |
| **Force majeure, severability, no-waiver, assignment** | Same baseline language. |

## Divergence — and why

### 1. Counterparty type and consumer-protection regime

**Gigaton AI.** B2B-dominant; Stripe Checkout clickwrap is standard SaaS pattern. Some prosumer signups possible at $99/mo Starter; California + a few state-law disclosures handle that.

**Carmen Beach Properties.** B2C-dominant (Guests are consumers of vacation rentals); B2B for Owners. **Mexican LFPC + PROFECO impose stricter consumer-protection rules** than US — abusive clauses can be voided, Spanish-controlling text is required for B2C, PROFECO complaint mechanism is preserved regardless of arbitration. Liability cap floor uplifted ($500 vs Gigaton's $100) to reflect higher-value transactions and likely-stricter MX-court tolerance for low caps.

**Ti Solutions.** B2B-only (mid-market customer organizations). No consumer-protection regime applies in the customer relationship; standard B2B contract terms with custom MSA + SOW overlay. Liability cap meaningfully higher ($50K) because of higher contract value ($40K setup + $8K–$25K/mo retainer × 6–12 months = $88K–$340K range).

### 2. Data-flow architecture — who is controller, who is processor

**Gigaton AI** is dual-role:
- **Controller** for its own visitor / sales-funnel / billing data.
- **Processor** for Customer Data when Customers run their own operations on the platform.

**Carmen Beach Properties** is dual-role:
- **Controller** for Guest, Owner, and visitor data (Carmen Beach determines purposes — running an STVR business).
- **Uses Gigaton AI as Processor** + the cascade of sub-processors.
- OTAs (Airbnb, Vrbo) are **independent controllers** for the leg they capture data; Carmen Beach becomes controller upon receipt of the OTA-shared booking data.

**Ti Solutions** is dual-role:
- **Controller** for its own sales-funnel / visitor / staff data.
- **Processor** for Customer's outbound campaign data — Customer is the controller of its leads.

This last distinction matters for **TCPA + CAN-SPAM exposure**: the controller (Customer) carries primary liability; the processor (Ti Solutions) executes per controller's instructions but retains AUP-driven veto for unlawful instructions.

### 3. Sub-processor depth

**Gigaton AI** publishes the canonical list (7 sub-processors: GCP, Cloudflare, Stripe, Twilio, Anthropic, OpenAI, Google Gemini).

**Carmen Beach Properties** adds **independent recipients** (not sub-processors of Carmen Beach):
- OTA platforms (separate controllers);
- Cleaning + maintenance contractors (limited-purpose recipients);
- Mexican tax authority (SAT — legal obligation);
- Property insurers.

**Ti Solutions** adds **engagement-specific sub-processors** beyond the always-on Gigaton stack:
- Dialer / contact-center (Twilio Voice, VCC Live, Vici Dial);
- CRM (HubSpot, Salesforce, depending on engagement);
- Data enrichment (Clay, Apollo, ZoomInfo);
- Document signing (DocuSign);
- LinkedIn Sales Navigator.

The variability is documented in DPA Annex A with the note that the specific stack is engagement-dependent.

### 4. Geographic-scope risk

**Gigaton AI.** US + MX scope; EU/UK excluded; data hosted in US (`us-central1`). Standard cross-border transfer disclosure to MX Data Subjects.

**Carmen Beach Properties.** **Properties physically in Quintana Roo, Mexico.** Even though business operations are US-platform-mediated, the property is in MX → Mexican federal + Quintana Roo state law applies to Property-conduct and Stay-related claims. Two layers of geographic exposure (operator's place of business + property's physical location). Triggers SAT/RFC obligations, Quintana Roo lodging-tax (Impuesto al Hospedaje), municipal STR registry (Solidaridad), and Mexican-condo-HOA jurisdiction.

**Ti Solutions.** US + MX customers; no physical-property dimension. Lower geographic risk than Carmen Beach.

### 5. Sensitive data treatment

**Gigaton AI.** Default: no sensitive-data collection; if a Customer needs to process sensitive data (e.g., healthcare BAA), a supplemental addendum is required.

**Carmen Beach Properties.** **May collect government-ID images** for STR-regulation compliance (Quintana Roo / municipal requirement, where applicable). Enhanced controls: encrypted upload, restricted access, ≤1-year retention, auto-purge, exclusion from AI Subprocessor pipelines.

**Ti Solutions.** Default: no sensitive-data collection; engagement-specific addendum required if a customer's vertical involves sensitive data (e.g., healthcare lead-gen outreach with HIPAA implications).

### 6. AI use cases and disclosures

**Gigaton AI.** General-purpose AI features (content generation, decisioning, classification) — customer-driven use.

**Carmen Beach Properties.** **Consumer-facing AI** — WhatsApp concierge bot interacts directly with Guests. Triggers **Colorado AI Act (effective Feb 2026)** + **California ADMT** disclosure obligations. Carmen Beach AUP includes explicit AI-channel disclosure + human-escalation path. AI Subprocessor cascade flows through Gigaton.

**Ti Solutions.** **B2B AI use** — internal to operations + Customer-approved AI-deployed customer-facing artifacts (chatbots, landing pages). Lower consumer-disclosure burden because endpoints are B2B; meeting-recording AI is the consent-sensitive subset (California CIPA two-party + Mexico federal one-party).

### 7. Termination + transition

**Gigaton AI.** Self-serve cancel; cancellation effective at next billing cycle.

**Carmen Beach Properties.** Two layers: Guest cancellation per stated cancellation policy (PROFECO-compatible); Owner PMA termination per separately executed PMA.

**Ti Solutions.** **60-day termination-for-convenience notice** (vs Gigaton's 30 days). Reflects custom-engagement nature — Ti Solutions has staffed up against the engagement; sudden termination disrupts operations and ongoing campaigns.

### 8. Indemnification

**Gigaton AI.** Mutual indemnification; platform-IP infringement on Gigaton's side; Customer Data and Customer's combinations excluded.

**Carmen Beach Properties.** **Three-way indemnification**:
- Guest indemnifies Carmen Beach + Owner for Guest-caused damage / law violations;
- Owner indemnifies Carmen Beach for title / permit / insurance defects (Owner-side warranties are substantial);
- Carmen Beach indemnifies for direct IP infringement only.

**Ti Solutions.** **Customer-heavy indemnification** because Customer drives the outbound content + lists. Specifically, Customer indemnifies for (a) Customer Materials (lists, brand assets, claims about Customer's products), (b) Customer's direction of outreach (TCPA/CAN-SPAM/PROFECO compliance burden on Customer), (c) Customer's products being marketed.

### 9. Class-action waiver enforceability

**All three** include the waiver. **Carmen Beach** has the most exposure to enforceability challenges:
- Mexican Art. 578 Federal Code of Civil Procedure permits collective actions and disfavors class waivers;
- PROFECO retains administrative jurisdiction over consumer complaints regardless of arbitration clauses;
- Carmen Beach's ToS explicitly **preserves PROFECO recourse** for B2C Guests (Section 17.4).

**Gigaton AI** + **Ti Solutions** are B2B-leaning; class waivers are more reliably enforceable but California's PAGA-style carve-outs have created uncertainty in recent years.

### 10. Arbitration forum

All three flag `[PARALEGAL: confirm forum]`. Reasonable defaults:

- **Gigaton AI**: AAA Commercial Rules, Wilmington Delaware (if Gigaton AI is DE-formed) or alternative; MX customers may route to CAM Mexico.
- **Carmen Beach Properties**: **Mexican domestic forum** (CAM Mexico or Quintana Roo state courts) for Property-Stay disputes; US forum for billing-only disputes.
- **Ti Solutions**: Same as Gigaton (since DBA structure).

### 11. Entity structure (and the Ti Solutions question)

**Gigaton AI** — established legal entity (state of formation to confirm); single Stripe account per locked decision B1.

**Carmen Beach Properties** — Mexican operator entity (legal form to confirm) coordinating with US Gigaton AI via the platform Stripe account. **Cross-border tax/legal coordination required** between Carmen Beach's MX RFC obligations + Gigaton's US tax obligations.

**Ti Solutions** — **assumed to be a DBA of Gigaton AI** per the 30-day roadmap recommendation (Section 3, User decision #1). If user instead elects a separate LLC for Ti Solutions, contracting entity, governing law, sub-processor cascade, and tax treatment all shift. Ti Solutions ToS Section 2.1 explicitly flags this contingency.

---

## Cross-document consistency check

| Element | Gigaton | Carmen Beach | Ti Solutions | Aligned? |
|---|---|---|---|---|
| Effective date | 2026-05-26 | 2026-05-26 | 2026-05-26 | ✅ |
| Excluded jurisdictions | EU/UK | EU/UK | EU/UK | ✅ |
| Sub-processors named | GCP, Cloudflare, Stripe, Twilio, Anthropic, OpenAI, Google | (Refs Gigaton's list) | (Refs Gigaton's list + adds engagement-specific) | ✅ |
| 30-day grace + 60-day deletion | ✅ | ✅ | ✅ | ✅ |
| Class waiver clause | Section 15.3 | Section 17.3 | Section 17.3 | ✅ |
| AI processing opt-out | Section 7.4 | Section 11 | Section 10 | ✅ |
| AI Subprocessor no-training default | Section 7.3 | (Via Gigaton DPA) | Section 6 of DPA | ✅ |
| `legal@gigaton.ai` default contact | ✅ | ✅ (with TODO for `legal@carmenbeach.com`) | ✅ (with TODO for `legal@tisolutions.co`) | ✅ |
| Governing-law placeholder | Delaware default + `[PARALEGAL: confirm]` | MX federal + Quintana Roo + `[PARALEGAL: confirm]` | DBA → Gigaton's governing law + `[PARALEGAL: confirm]` | ✅ |
| Cross-references between docs | ToS↔Privacy↔AUP↔DPA via Markdown links | Same | Same | ✅ |
| Banner "v0 DRAFT — PENDING PARALEGAL REVIEW" | ✅ | ✅ | ✅ | ✅ |

---

## Open structural questions for paralegal sign-off

1. **Single ToS vs entity-specific ToS** — currently we have three entity-specific ToS. An alternative is one umbrella Gigaton AI ToS with Carmen Beach + Ti Solutions as "brand-specific addenda." The current structure is **easier to publish per-domain** and **clearer for customers**; the alternative is **more efficient to maintain.** Choose one for v1.

2. **Spanish-language strategy for Carmen Beach** — is a full Spanish translation required (likely yes for PROFECO/LFPC B2C), and who produces it (Mexican counsel)?

3. **Stripe Tax + Merchant of Record** — Stripe is the payment processor + Stripe Tax handles tax collection. Are we positioning Gigaton AI as MoR, Stripe as MoR, or jurisdiction-by-jurisdiction depending on Stripe Tax coverage?

4. **MSA + SOW templates for Ti Solutions** — these need to exist separately; the Ti Solutions ToS references them. Confirm templates are drafted and on file before any Ti Solutions live engagement.

5. **PMA template for Carmen Beach Owners** — same question; PMA template is referenced in Carmen Beach ToS Section 7.

6. **Cookie consent management platform** — choose one (OneTrust / Cookiebot / Termly / homegrown) per domain before launch.

7. **CCPA "Do Not Sell or Share" link** — required on website footer for CCPA/CPRA; confirm engineering will deploy on all 3 entity domains.

8. **DSAR (Data Subject Access Request) tooling** — given the 20-business-day LFPDPPP + 45-day CCPA SLAs, an internal tooling pipeline is required; current state is "manual via privacy@gigaton.ai" which is sustainable for v1 beta but not at scale.

---

*Last reviewed: 2026-05-25 by AI draft-assistant. Status: PENDING-PARALEGAL-REVIEW.*
