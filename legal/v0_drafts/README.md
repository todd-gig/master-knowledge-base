# Legal v0 Drafts — Template-Driven Entity Scaffold

**Status:** v0 draft — PENDING PARALEGAL REVIEW. **Do not publish or rely on without licensed-attorney review for the target jurisdictions.**

**Scope v1:** U.S. (CCPA/CPRA-aligned baseline) + Mexico (LFPDPPP). **EU / EEA / UK / Switzerland customers are explicitly excluded in v1.**

---

## 1. Why this directory exists

Gigaton's product framing (see `~/.claude/projects/-Users-admin/memory/MEMORY.md` → `product_service_package_gigaton_ti_solutions.md` and `master_project_plan.md`) anticipates **many entities** spinning up over time, not three. These include:

- The first three (Carmen Beach Properties, Gigaton AI, Ti Solutions);
- A marketing + media-management agency;
- A consolidated Playa-del-Carmen real-estate operator;
- A 5th-Avenue PDC walking-tour operator (with in-shop owner chat/voice);
- N additional entities spawned by the **Gignet affiliate program** — each human = an affiliate, each affiliate requires its own organization with a domain + business-class email.

Hand-writing every legal pack per entity does not scale. Instead this directory holds:

1. **Parameterized templates** (Jinja-style placeholders) under `templates/`.
2. **An entity-type taxonomy** at `entity_types.yaml` that drives which optional clauses each template renders.
3. **Bespoke instances** under `<entity-slug>/` directories — each is the rendered output for one operating entity (Carmen Beach, Gigaton AI, Ti Solutions today; more later).

The **entity-creation flow** (designed in parallel by another agent) consumes these templates programmatically: when a new entity is provisioned, the flow loads `entity_types.yaml`, picks the right `{{ENTITY_TYPE}}` profile, fills the `{{...}}` parameters from the entity record, renders the four core documents (+ affiliate addendum where applicable), and stores them under a new `<entity-slug>/` directory.

The three existing bespoke directories (Carmen Beach Properties, Gigaton AI, Ti Solutions) are themselves **instances** of template instantiation — they serve as validation examples that the templates produce legally coherent documents.

---

## 2. Directory layout

```
legal/v0_drafts/
├── README.md                          ← this file
├── entity_types.yaml                  ← taxonomy: data categories, sub-processors,
│                                        jurisdictions, required-vs-optional clauses
│                                        per ENTITY_TYPE
├── templates/
│   ├── terms_of_service.template.md
│   ├── privacy_policy.template.md
│   ├── acceptable_use_policy.template.md
│   ├── data_processing_addendum.template.md
│   └── gignet_affiliate_addendum.template.md   ← mandatory for affiliate entities
├── gigaton-ai/                        ← INSTANCE — ENTITY_TYPE: saas_platform
│   └── terms_of_service.md            (hand-drafted; used as template validation example)
├── ti-solutions/                      ← INSTANCE — ENTITY_TYPE: managed_service
└── carmen-beach-properties/           ← INSTANCE — ENTITY_TYPE: property_management
```

---

## 3. How the entity-creation flow consumes these templates

Pseudocode the entity-creation flow follows:

```python
# 1. Operator (or admin) provisions a new entity through the entity-creation UI.
entity = {
    "ENTITY_NAME":                "Acme Walks",
    "ENTITY_LEGAL_NAME":          "Acme Walks S.A. de C.V.",
    "ENTITY_DOMAIN":              "acmewalks.mx",
    "ENTITY_CONTACT_EMAIL":       "legal@acmewalks.mx",
    "ENTITY_BUSINESS_DESCRIPTION":"a walking-tour operator on 5th Avenue, Playa del Carmen",
    "ENTITY_JURISDICTION":        "MX-QuintanaRoo",
    "ENTITY_TYPE":                "tour_operator",
    "EFFECTIVE_DATE":             "2026-06-15",
    "LAST_REVIEWED":              "2026-05-25",
    "PLATFORM_STRIPE_ACCOUNT_HOLDER": "Gigaton AI",   # always per B1
}

# 2. Load entity-type profile.
profile = yaml.safe_load(open("legal/v0_drafts/entity_types.yaml"))["entity_types"][entity["ENTITY_TYPE"]]
entity["ENTITY_DATA_CATEGORIES"] = profile["data_categories"]
entity["ENTITY_SUB_PROCESSORS"]  = expand_sub_processors(profile["sub_processors"])
entity["required_clauses"]       = profile["required_clauses"]
entity["optional_clauses"]       = profile.get("optional_clauses", [])
entity["ai_processing_disclosure"] = profile["ai_processing_disclosure"]

# 3. Render each template and write under a new instance directory.
for tpl in ["terms_of_service", "privacy_policy",
            "acceptable_use_policy", "data_processing_addendum"]:
    render(f"templates/{tpl}.template.md", entity,
           out=f"legal/v0_drafts/{slug(entity['ENTITY_NAME'])}/{tpl}.md")

# 4. If affiliate, also render the addendum (mandatory).
if entity["ENTITY_TYPE"] == "affiliate_solo_operator":
    render("templates/gignet_affiliate_addendum.template.md", entity,
           out=f"legal/v0_drafts/{slug(entity['ENTITY_NAME'])}/gignet_affiliate_addendum.md")

# 5. Flag all rendered files PENDING-PARALEGAL-REVIEW in metadata + create a review task.
```

---

## 4. Template parameter reference

Every template uses Jinja2-style `{{...}}` placeholders. The entity-creation flow MUST supply all of these; the templates assume non-null values.

| Parameter | Type | Example |
|---|---|---|
| `ENTITY_NAME` | string | "Carmen Beach Properties" |
| `ENTITY_LEGAL_NAME` | string | "Carmen Beach Properties S.A. de C.V." |
| `ENTITY_DOMAIN` | hostname | "carmenbeach.com" |
| `ENTITY_CONTACT_EMAIL` | business email | "legal@carmenbeach.com" |
| `ENTITY_BUSINESS_DESCRIPTION` | one sentence | "vacation-rental and property-management services in Playa del Carmen" |
| `ENTITY_DATA_CATEGORIES` | list of strings | from `entity_types.yaml` |
| `ENTITY_SUB_PROCESSORS` | list of objects `{name, purpose, location}` | from `entity_types.yaml` |
| `ENTITY_JURISDICTION` | ISO-like | "MX-QuintanaRoo" / "US-WA" |
| `ENTITY_TYPE` | one of the keys in `entity_types.yaml::entity_types` | "property_management" |
| `PLATFORM_STRIPE_ACCOUNT_HOLDER` | always "Gigaton AI" | "Gigaton AI" |
| `EFFECTIVE_DATE` | ISO date | "2026-06-15" |
| `LAST_REVIEWED` | ISO date | "2026-05-25" |
| `ai_processing_disclosure` | "high" / "medium" / "low" | from `entity_types.yaml` |
| `required_clauses` | list of strings | from `entity_types.yaml` |
| `optional_clauses` | list of strings | from `entity_types.yaml` |

**12 first-class operator-supplied parameters** + **3 profile-derived collections** + **3 profile-derived flags** = templates render fully when given a valid entity-type + 12 string/date fields.

---

## 5. Template conditionals — quick reference

Conditional sections render only when matched:

- `{% if ENTITY_TYPE == 'X' %}` — entity-type-specific clauses (services description, IP assignment for managed/agency variants, OTA handling for property/real-estate, etc.).
- `{% if 'CLAUSE_TOKEN' in required_clauses %}` — required-clause inclusion (e.g., `'mexico_lfpc_consumer_carveout'`, `'spanish_language_courtesy'`, `'host_fund_handling'`).
- `{% if 'CLAUSE_TOKEN' in optional_clauses %}` — opt-in clauses (`'affiliate_program_reference'`, `'tour_operator_addendum'`).
- `{% for category in ENTITY_DATA_CATEGORIES %}` / `{% for sp in ENTITY_SUB_PROCESSORS %}` — list rendering.

See `entity_types.yaml::clause_registry` for the canonical clause-token vocabulary and where each token gates content in the templates.

---

## 6. Entity types supported (Day 1)

Seven entity types are seeded:

| `ENTITY_TYPE` | Seed instance | AI disclosure | Notes |
|---|---|---|---|
| `saas_platform` | Gigaton AI | high | First-party multi-tenant SaaS |
| `managed_service` | Ti Solutions | high | Done-for-you on top of Gigaton |
| `property_management` | Carmen Beach Properties | high | OTA-channel + MX hospitality |
| `marketing_agency` | TBD | high | Ad platforms + audience lists |
| `real_estate_consolidated` | TBD (Playa del Carmen) | high | Brokerage + property mgmt + listings |
| `tour_operator` | TBD (5th Ave PDC) | high | Voice + IG/WhatsApp + in-person |
| `affiliate_solo_operator` | per-affiliate | medium | Mandatory Gignet addendum |

Adding a new type: add a key under `entity_types:` in `entity_types.yaml` with all required fields, then add corresponding `{% if ENTITY_TYPE == 'new_type' %}` blocks where the new type's clauses differ from existing ones. The clause-registry section documents every conditional location.

---

## 7. Validation rule — round-tripping the existing bespoke instances

To validate the templates, instantiate them against the parameter sets corresponding to the three existing bespoke directories and verify the rendered output is materially equivalent to the hand-drafted versions (modulo formatting). Paralegal review should be the determinant of "materially equivalent." This validation is REQUIRED before the entity-creation flow goes live.

Validation parameter sets:

- **Gigaton AI** → `ENTITY_TYPE=saas_platform`, `ENTITY_JURISDICTION=US-DE`, with `affiliate_program_reference` in optional_clauses (because Gignet is its program).
- **Ti Solutions** → `ENTITY_TYPE=managed_service`, `ENTITY_JURISDICTION=US-WA`.
- **Carmen Beach Properties** → `ENTITY_TYPE=property_management`, `ENTITY_JURISDICTION=MX-QuintanaRoo`, with `tour_operator_addendum` in optional_clauses if/when tours are added.

---

## 8. What is NOT templatable

The following must still be hand-written per entity (the templates flag these as `[PARALEGAL: ...]` markers):

1. **Registered-agent / legal-notices physical address** — varies per legal entity, requires confirmed corporate registration.
2. **Governing-law venue selection (specific arbitration forum + venue)** — counsel-dependent strategy call per entity's exposure.
3. **Trust-account / fiduciary specifics for host-fund handling** — varies per property-management Owner agreement and MX-state notarial requirements.
4. **Broker-licensing disclosures (real-estate)** — depends on actual licenses held in each market.
5. **MX SAT / INM / hospitality record-retention windows** — depend on entity registration type (RFC class, immigration status of operator).
6. **Two-party-consent specifics for voice recording** — varies per MX state + US-state-of-guest residence; cannot template all combinations.
7. **OTA-partner-specific compliance language** — each OTA (Airbnb / Booking / Vrbo) has its own host-terms; per-OTA review required.
8. **Statement-of-Work (SOW) substance** — must be written per managed-service or agency engagement.

These can be progressively templated as common patterns emerge across entities, but should not be guessed at draft time.

---

## 9. Coordination with the entity-creation flow

The parameter names in this README, in `entity_types.yaml`, and in the `templates/*.md` files are the **contract** with the entity-creation-flow agent. Changes to parameter names MUST be coordinated; do not rename without updating both sides.

The flow is expected to set `instance_status: PENDING-PARALEGAL-REVIEW` in the rendered frontmatter and create a review task per rendered instance.

---

---

## 10. Paralegal review checklist (covers all 12 rendered entity instances)

The three existing bespoke directories contain 12 finished v0 drafts (3 entities × 4 doc types) authored 2026-05-25. Counsel review should proceed in five phases.

### Phase 1 — Entity-structure verification (BLOCKS everything else)

- [ ] Confirm **Gigaton AI**'s legal entity (LLC vs Inc?), state of formation, registered agent. Fills the address placeholder in ~12 places.
- [ ] Confirm **Ti Solutions** entity decision: DBA of Gigaton AI (recommended in 30-day roadmap §3) vs separate LLC. If LLC, rework ToS Sections 1, 2, 17, 18 + all DPAs.
- [ ] Confirm **Carmen Beach Properties** legal-entity structure in Mexico (S de RL / S.A. de C.V.) given properties physically in Quintana Roo. Document cross-border arrangement with Gigaton AI for Stripe billing.

### Phase 2 — Jurisdictional review

- [ ] Confirm EU/UK Excluded-Jurisdictions posture is correct risk-bounded path for each entity, OR design EU-compliant variant.
- [ ] California CCPA/CPRA — 12-month look-back categories + ADMT regs 2026 cross-check.
- [ ] Mexico LFPDPPP — confirm each Privacy Policy meets all "Aviso de Privacidad Integral" elements.
- [ ] Other US state laws (VA VCDPA, CO CPA, CT CTDPA, UT UCPA, TX TDPSA, FL FDBR) — add residency-aware addendums or affirm CA-baseline-only posture.
- [ ] Spanish-language requirement for Carmen Beach Guest B2C contracts (LFPC + PROFECO) — engage MX counsel for Spanish version + translation authority.

### Phase 3 — Substance review (clause-level)

- [ ] Arbitration + class waiver — confirm enforceability in CA, TX, MX (Art. 578 Federal Code of Civil Procedure). Preserve PROFECO recourse for Carmen Beach Guests.
- [ ] Liability caps — Gigaton: greater of 12-mo fees or US$100. Carmen Beach: greater of booking total or US$500. Ti Solutions: greater of 12-mo SOW fees or US$50,000. Confirm each.
- [ ] Indemnification scope + AI-output carve-outs.
- [ ] AI disclosure alignment with Anthropic / OpenAI / Google AUPs + Colorado AI Act (Feb 2026) + CA ADMT regs + NYC AEDT.
- [ ] Sub-processor flow-down — confirm Gigaton's contractual commitments with each AI Subprocessor support the no-training assertion.
- [ ] Carmen Beach: Mexican STR regs (Quintana Roo + Solidaridad municipality), SAT/RFC, IVA/ISH tax, condo/HOA interplay.
- [ ] Ti Solutions: TCPA + CAN-SPAM + REPEP + state-level mini-TCPAs + recording-consent regimes (CA CIPA two-party; MX one-party).
- [ ] Data Subject rights operationalization — pipeline to honor access/deletion/opt-out within statutory SLAs (LFPDPPP 20 BD + CCPA 45 days).

### Phase 4 — Operational placeholders (require Todd's input)

- [ ] Email aliases per entity: `legal@`, `privacy@`, `security@`, `abuse@`, `appeals@`, `support@`, `concierge@`, `cxguy@`. Provision via Google Workspace.
- [ ] Registered-agent / legal-notices physical addresses per entity.
- [ ] Arbitration forum + venue (AAA vs JAMS for US; CAM Mexico for MX).
- [ ] Governing-law selections (Delaware vs alt for Gigaton/Ti; MX federal + Quintana Roo for Carmen Beach).
- [ ] Cancellation policy specifics for Carmen Beach ToS Section 5.4.
- [ ] Stripe Tax registration status in US, MX (EU declined for v1 beta).
- [ ] PMA template for Carmen Beach Owners (exists separately — confirm cross-reference accuracy).
- [ ] MSA + SOW templates for Ti Solutions (exist separately — confirm).
- [ ] Non-solicit period for Ti Solutions §18.1 (default 12 months — CA concerns).
- [ ] Pass-through markup % for Ti Solutions §5.5 (default 0–10%).

### Phase 5 — Sign-off and publication

- [ ] Counsel review of all 12 documents.
- [ ] Red-lines + revisions producing `v1_drafts/` sibling folder.
- [ ] Founder + Owner co-sign per responsibility-scoped matrix.
- [ ] Translate Carmen Beach docs to Spanish + Mexican counsel review.
- [ ] Publish to: `gigaton.ai/legal/{tos,privacy,aup,dpa}`, `carmenbeach.com/legal/*` (+ `/-es`), `tisolutions.co/legal/*`.
- [ ] Stripe Checkout flow links to live legal pages prior to live-mode flip.
- [ ] Cookie banner deployed on each domain.
- [ ] Consent-record storage backend live (timestamp + IP + accepted version).

---

## 11. Inline `[PARALEGAL: ...]` markers — full punch list (extracted from the 12 rendered instances)

### Gigaton AI — Terms of Service
1. Confirm clickwrap acceptance mechanism enforceability.
2. Confirm geo-fencing language + remediation for Excluded Jurisdictions.
3. Confirm beta-period disclaimers; align with limitation of liability.
4. Confirm Restriction (h) "not for training competing AI models" given evolving disclosure norms.
5. Confirm AI processing + opt-out language under emerging AI disclosure norms.
6. Confirm "AS IS" disclaimer enforceability under MX LFPC.
7. Confirm liability cap amount + enforceability under CCPA + LFPDPPP statutory penalties.
8. Confirm Delaware vs alternative US state for governing law.
9. Confirm arbitration forum + venue.
10. Confirm class-action waiver enforceability in target jurisdictions.
11. Confirm 30-day arbitration opt-out window under FAA case law.
12. Insert registered-agent / legal-notices physical address.
13. Confirm Spanish-controlling-language requirement for B2C Mexican consumers.

### Gigaton AI — Privacy Policy
14. Confirm 50-state US privacy-law residency-aware variant before scaling beyond beta.
15. Confirm Mexican aviso de privacidad has all required elements.
16. Confirm whether other US state laws require addendums.
17. Confirm AI-disclosure alignment with Colorado AI Act 2026 + CA ADMT regs 2025-2026 + NYC AEDT.
18. Confirm tax/audit retention periods (US IRS + MX SAT).
19. Confirm cookie banner implementation matches CCPA + LFPDPPP secondary-purpose opt-out.
20. Confirm 50-state breach-notification mapping.
21. Confirm any third-party analytics SDKs in use; align cookie disclosure.

### Gigaton AI — AUP
22. Confirm AI-misuse list cross-references Anthropic / OpenAI / Google published AUPs.

### Gigaton AI — DPA
23. Confirm definitions align with each statute's actual term-of-art (CCPA "service provider"; LFPDPPP "encargado").
24. Confirm sensitive-data carve-out; recommend explicit BAA template for healthcare + GLBA for financial-services operators.
25. Confirm AI Subprocessor contractual flow-down matches asserted commitments; recommend annual audit.
26. Confirm 72-hour incident-notice baseline against statutory floors.
27. Confirm Controller/Processor liability allocation under each Data Protection Law.
28. Confirm background-check scope/practicality for small team.
29. Confirm whether email-delivery provider (SendGrid/Postmark) needs sub-processor listing.

### Carmen Beach Properties — Terms of Service
30. Confirm clickwrap enforceability under Mexican LFPC for B2C; Spanish pop-up at booking confirmation.
31. Confirm legality of EU-Guest exclusion; risk-bounded posture vs accepting with EU-compliant terms.
32. Confirm PMA template exists + recommended contents.
33. Confirm Quintana Roo Impuesto al Hospedaje; Stripe Tax registrations vs RFC + DIOT obligations.
34. Confirm cancellation policy with PROFECO/LFPC; force-majeure floor.
35. Confirm Mexican law on landlord remedies for early Stay termination.
36. Insurance minima — US$1M GL + replacement-cost property; Mexican condo master-policy STR-use exclusion.
37. Confirm cross-border Owner-payout tax treatment (SAT withholding, Owner RFC).
38. Confirm sub-processor chain characterization; LFPDPPP consent for US-MX cross-border processing.
39. Confirm AI disclosure language meets emerging norms for consumer-facing AI.
40. Confirm AS-IS carve-out + "minimum-fitness" for MX B2C.
41. Confirm liability cap enforceability under Mexican B2C law; higher floor + gross-negligence carve-out.
42. Confirm governing-law selection; Quintana Roo for STR transactions.
43. Confirm arbitration appropriateness for B2C; preserve PROFECO recourse.
44. Confirm class-action waiver under Mexican Art. 578.
45. Insert Mexican domicile for service of process.
46. Confirm Spanish-controlling-language requirement (LFPC).

### Carmen Beach Properties — Privacy Policy
47. Confirm Spanish-language aviso requirement.
48. Confirm legal basis for government-ID collection under Quintana Roo STR regs; document auto-purge.
49. Confirm primary vs secondary purposes classification (LFPDPPP Art. 16 + 17).
50. Confirm OTA controller relationship characterization (joint-controllership alt).
51. Confirm Owner-contractor DPA template — `cláusula de confidencialidad` vs `convenio de transferencia`.

### Carmen Beach Properties — AUP
52. Confirm Mexican non-discrimination obligations for STR hosting.
53. Confirm review-extortion clause consistent with PROFECO + FTC CRFA.

### Carmen Beach Properties — DPA
54. (Refer back to Gigaton DPA items + Carmen-Beach-specific.)

### Ti Solutions — Terms of Service
55. **Confirm entity structure** — DBA vs separate LLC. **CRITICAL** — 12+ references depend on this.
56. Confirm EU exclusion posture vs GDPR-compliant B2B variant.
57. Confirm clickwrap baseline + custom MSA structure.
58. Confirm $50K liability floor for typical engagement value.
59. Confirm B2B AI-disclosure framework; per-engagement AI-use declaration in SOW.
60. Confirm meeting-recording consent script (CA CIPA two-party).
61. Confirm survival periods for confidentiality.
62. Confirm non-solicit enforceability (CA disfavors).
63. Confirm arbitration forum.
64. Confirm Customer reps cover full do-not-contact registries (REPEP, state DNCs).

### Ti Solutions — Privacy Policy
65. Confirm controller-processor allocation for outbound-campaign data; joint-controllership alt.

### Ti Solutions — AUP
66. Confirm prohibited-industries list (ICO, BNPL, etc.).
67. Confirm REPEP reference accuracy.

### Ti Solutions — DPA
68. Confirm 15-day sub-processor change notice (vs Gigaton's 30-day).

---

## 12. Estimated paralegal effort + rough cost

- Phase 1 (entity structure): 2–4 hours.
- Phase 2 (jurisdictional review): 8–16 hours (US privacy/contract counsel + MX counsel).
- Phase 3 (substance review): 16–24 hours.
- Phase 4 (operational placeholders): 2–4 hours (Todd-input dependent).
- Phase 5 (sign-off + publication): 4–8 hours.

**Total: ~32–56 hours paralegal + 8–16 hours supervising attorney + ~8 hours Mexican counsel.**

**Rough cost** (US paralegal $125–$200/hr, attorney $350–$650/hr, MX counsel $150–$300/hr):
- Paralegal: $4,000–$11,200
- Attorney: $2,800–$10,400
- MX counsel: $1,200–$2,400
- **Total: $8,000–$24,000 for v1 production-ready scaffold.**

[PARALEGAL: above is internal-planning estimate only — please provide firm's actual scoping figure.]

See [`entity_comparison_matrix.md`](entity_comparison_matrix.md) for clause-by-clause comparison across the three entity instances and the structural rationale for each divergence.

---

*This README and the template scaffold are themselves PENDING-PARALEGAL-REVIEW. Last reviewed: 2026-05-25.*

