---
type: commercial-terms-template
established: 2026-05-27
version: v0
terms_template_version: multipli_v0
source: docs/governance/comp_payout_structure_v1.md §3.4
status: ACTIVE — renders the LOCKED v0 §3.4 Multipli terms via the self-serve tokenized onboarding link
brand: GIGATON (NOT Ti) per Todd directive 2026-05-26 eve
cohort: beta cohort #1 (first paying operator)
ppim_interaction: commercial-terms surface inside the Multipli self-serve onboarding bundle
ppim_economics: encodes the 18% performance-share routing for Gigaton-attributed funded contracts
ppim_predictability: HIGH — every field is rule-driven; dynamic values render from the signed JWT payload
ppim_brand_dimension: trust + transparency (co-branded lockup; recipient sees exact terms accepted)
ppim_attribution_chain: [multipli_v0_terms, commercial_terms, master-knowledge-base, gigaton-root]
---

# Gigaton × Multipli — Commercial Terms

> **RENDER NOTE (READ FIRST — for the UI/engineering team).** Every `{{field}}`
> placeholder below is bound to a key in the **signed JWT payload** that the
> self-serve tokenized link (`https://gigaton.ai/onboard/multipli/<jwt>`) carries.
> The commercial-terms surface on the landing page renders these values **from
> the JWT payload at request time** — they MUST NEVER be hardcoded in the UI.
> The locked defaults shown in this template are the v0 LOCKED values from
> `comp_payout_structure_v1.md` §3.4; they exist so the template is legible and
> so the token issuer (`POST /v1/onboard/issue-link`) has a canonical source to
> stamp into the payload. If a rendered value disagrees with the JWT payload,
> the JWT payload wins.
>
> `terms_template_version: multipli_v0` — the JWT payload carries
> `terms_template_version` so the accepted version is provably pinned at e-sign time.

---

## Co-branded lockup

`{{co_branded_lockup}}` <!-- placeholder: Gigaton + Multipli co-branded hero/lockup asset; approval-gated per §3.4 landing-page bundle item 1 -->

**Prepared for:** `{{contact}}` <!-- JWT.contact — e.g. Ben Cahir (CEO) -->
**Prospect / namespace:** `{{prospect_id}}` <!-- JWT.prospect_id -->
**Cohort:** `{{cohort}}` <!-- JWT.cohort — default: beta_1 -->
**Terms template version:** `{{terms_template_version}}` <!-- JWT.terms_template_version — default: multipli_v0 -->

---

## 1. Commercial terms

The following terms govern the Gigaton ↔ Multipli engagement. Dynamic fields
render from the JWT payload; locked-policy fields render the defaults shown.

| Term | Value | Source / binding |
|---|---|---|
| **Performance share** | **`{{perf_share_pct}}`% of Multipli net revenue** on Gigaton-attributed funded contracts <br>_(JWT.perf_share_pct — default **18**)_ | §3.4 LOCKED v0 — dynamic; bound to `perf_share_pct` |
| **Cadence** | **Monthly, T+15** after Multipli funding-month close | §3.4 LOCKED v0 — locked policy |
| **Rail** | **`{{rail}}`** _(JWT.rail — default **Stripe Connect Express**)_ | §3.4 + §2 PAYOUT-1 default — dynamic; bound to `rail` |
| **Minimum payout** | **`$ {{min_payout_usd}}` USD** (accrue if below) _(JWT.min_payout_usd — default **1000**)_ | §3.4 + §2 PAYOUT-1 floor — dynamic; bound to `min_payout_usd` |
| **Base retainer** | **None** (beta cohort #1, variable-only) | §3.4 LOCKED v0 — locked policy |
| **Attribution** | **First-touch + 180-day verified-handoff** | §3.4 LOCKED v0 — locked policy |
| **Term** | **6 months initial; auto-renew if either side exceeds 50 funded-contracts-from-Gigaton** | §3.4 LOCKED v0 — locked policy |
| **Year-1 cap** | **$250,000 max performance share** | §3.4 LOCKED v0 — locked policy |

### Field-binding reference (JWT payload → template field)

| JWT payload key | Template field | Dynamic? | Locked default |
|---|---|---|---|
| `prospect_id` | Prospect / namespace | yes | — |
| `contact` | Prepared for | yes | — |
| `cohort` | Cohort | yes | `beta_1` |
| `terms_template_version` | Terms template version | yes | `multipli_v0` |
| `perf_share_pct` | Performance share % | **yes** | `18` |
| `min_payout_usd` | Minimum payout USD | **yes** | `1000` |
| `rail` | Payout rail | **yes** | `Stripe Connect Express` |
| `exp` | (token expiry — not rendered) | n/a | 14-day expiry |
| `jti` | (single-use token id — not rendered) | n/a | — |
| `iat` | (issued-at — not rendered) | n/a | — |

> The remaining §3.4 locked terms (cadence T+15, no base retainer, first-touch +
> 180-day attribution, 6-month auto-renew term, $250K Y1 cap) are **locked policy**,
> not per-prospect parameters, so they are NOT carried as JWT fields — they render
> from this template's locked defaults and change only via a new
> `terms_template_version`.

---

## 2. Attribution definition (binding)

A Multipli vendor counts as **Gigaton-attributed** when both hold:

1. The vendor **originated** in a Gigaton `vendor.financing.captured.v1` event (first-touch), AND
2. The Multipli funding system **confirms a funded contract within 180 days** of that event (verified-handoff).

Performance share is computed against **Multipli net revenue** on each
Gigaton-attributed funded contract, per the canonical per-funded-contract
economics in `comp_payout_structure_v1.md` §3.4.

---

## 3. Acceptance

Acceptance is captured **in-app** (recommended for beta cohort #1; DocuSign is
the upgrade path for cohort #2+). On acceptance, the platform records the signed
`terms_template_version`, flips the namespace `state=active`, bumps the capability
tier to `tier_1_active`, and fires HME `operator.activated.v1`.

E-signature: `{{esign_block}}` <!-- placeholder: in-app e-sign capture; binds accepted terms_template_version + jti -->

---

## Revision history

| Version | Date | Source | Change |
|---|---|---|---|
| v0 | 2026-05-27 | `comp_payout_structure_v1.md` §3.4 (v1.0 ACTIVE) | Initial template — renders LOCKED v0 §3.4 Multipli terms; dynamic fields bound to JWT payload (`perf_share_pct`, `min_payout_usd`, `rail`); locked-policy fields shown as defaults. |
