---
type: governance-scaffold
established: 2026-05-26
status: DRAFT — scaffold awaiting Todd ratification of per-entity percentages (deadline 2026-05-28 EOD)
authority: requires Todd sign-off on §3, §5 retry policy, and the §6 checklist before promotion to ACTIVE
serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
ppim_interaction: meta — governs every money-out-of-platform event for every operator entity
ppim_economics: directly determines net rev share routing across CBP / Ti Solutions clients / Multipli / Gignet / Gigaton-self
ppim_predictability: HIGH — every payout is rule-driven (no per-event discretion); $1k floor + bi-weekly Wed cadence are deterministic
ppim_brand_dimension: trust + transparency (recipients see clean amounts; platform absorbs ACH fees; round-up favors recipient)
ppim_outcome_quality: a single ratified source-of-truth for "who gets paid what, when, via which rail" across every entity in the hierarchy
applies_to:
  - gigaton-engine (billing module — payout scheduler + Stripe Connect Express config)
  - gigaton-gateway (attribution_chain stamping → routes commission events to correct entity)
  - user-access-engine (client_namespaces.governance_overlays.compensation JSONB shape — follow-on)
  - persona-engine (HR offer human-in-loop gate per INTEL-1)
  - decision-engine (semantic_classifier cosine thresholds per INTEL-1)
  - intelligence-silo (skill-vector seed values for talent routing)
  - gigaton-ui-system (operator-facing Settings → Payouts; coaching surfaces auto-graduate via competence — no opt-out toggle)
cross_refs:
  - decisions/2026-05-25_architecture_decisions_log.md (PAYOUT-1, INTEL-1, OPS-1, ARCH-1, ARCH-2)
  - /Users/admin/.claude/projects/-Users-admin/memory/payout_1_min_threshold_1k_2026_05_26.md
  - /Users/admin/.claude/projects/-Users-admin/memory/payout_1_and_intel_1_clarifications_locked_2026_05_26.md
  - /Users/admin/.claude/projects/-Users-admin/memory/compensation_payout_structure_thursday_5_28_deadline.md
  - /Users/admin/.claude/projects/-Users-admin/memory/product_service_package_gigaton_ti_solutions.md
  - /Users/admin/.claude/projects/-Users-admin/memory/entity_hierarchy_for_namespace_seed_2026_05_26.md
  - master_project_plan.md (Chapter 11 — Gignet affiliate tier compensation reference)
  - master-knowledge-base/manifests/onboarding_v1.yaml (consuming stage — follow-on PR)
---

# Compensation + Payout Structure — v1 Scaffold

> **Document state.** This is a SCAFFOLD. Every locked decision below is memory-backed and ready to ship; every TBD in §3 requires Todd's per-entity percentage input before this document promotes from DRAFT → ACTIVE. Deadline: **Thursday 2026-05-28 EOD**.

---

## 1. TL;DR

This document is the single ratified source-of-truth for **who gets paid what, when, and via which rail** across every entity in the Gigaton hierarchy (Carmen Beach Properties + sub-clients, Ti Solutions + 5 retainer clients, Multipli prospect, Gignet affiliates, Gigaton-self). It captures the **8 locked decisions** ratified 2026-05-26 EOD (the `$1,000` minimum payout threshold + 4 PAYOUT-1 clarifications + 3 INTEL-1 clarifications governing HR / coaching / classifier-routing) and scaffolds the per-entity compensation tables that Todd will fill in by **Thursday 2026-05-28 EOD**. Until the §3 percentages and §5 retry policy are ratified, the gigaton-engine billing module and the operator-facing Settings → Payouts surface should treat this doc as DRAFT and refuse to execute any payout that does not satisfy the LOCKED §2 constraints. Cross-references the entity hierarchy seed ([[entity_hierarchy_for_namespace_seed_2026_05_26]]) and the joint Gigaton + Ti Solutions go-to-market wrapper ([[product_service_package_gigaton_ti_solutions]]).

**Hybrid strawman fill (2026-05-26)**: 29 TBDs reduced to 8 strategic %s pending Todd's business judgment (Multipli rev share + Ti Solutions 5-client retainer/uplift splits + Gignet 5-tier commission table + recurring-revenue tail). All cost-of-doing-business defaults pre-filled with industry-norm strawmen marked `(_strawman; override if needed_)`.

**The 8 locked decisions** (memory-backed, do not re-litigate without an explicit Todd directive):

1. **Min payout threshold** = `$1,000 USD`, indefinite, every entity, every rail. Source: [[payout_1_min_threshold_1k_2026_05_26]].
2. **Rounding direction** = round UP (favor recipient). Source: [[payout_1_and_intel_1_clarifications_locked_2026_05_26]].
3. **Cadence** = bi-weekly Wednesday (every other Wed). Same source.
4. **ACH fee bearer** = platform absorbs (recipients see clean amounts). Same source.
5. **First-time payout exception** = NO exception (steady-state cadence applies to first payout). Same source.
6. **HR offer human-in-loop gate** = YES — every HR offer requires human pre-review (operator approval queue). Same source.
7. **Coaching graduation** (REVISED 2026-05-26 EOD) = NO opt-out toggle. Coaching nudges auto-suppress per-category as the operator demonstrates competence (correct UI actions + accurate chat prompts). Same source.
8. **Skill-vector cosine thresholds** = `0.55` primary / `0.35` secondary (drives downstream Ti Agent Matrix routing per INTEL-1). Same source.

---

## 2. LOCKED — Payout structure (concrete, do not modify without explicit Todd directive)

These are deterministic rules. The gigaton-engine billing module and Stripe Connect Express config MUST honor each one.

| Rule | Value | Source memory | Implementation pointer |
|---|---|---|---|
| Minimum payout | **`$1,000 USD`** (indefinite, every entity, every rail) | [[payout_1_min_threshold_1k_2026_05_26]] | `payout_schedule.minimum_amount = 100000` (cents) in Stripe Connect Express + ACH alternative same floor |
| Cadence default | **Bi-weekly Wednesday** (every other Wed) | [[payout_1_and_intel_1_clarifications_locked_2026_05_26]] | Stripe `payout_schedule.interval='weekly'` + `weekly_anchor='wednesday'` + internal scheduler skips alternating weeks |
| Rounding direction | **Round UP** (favor recipient) | Same | `math.ceil(amount_cents)` on every payout calculation; document on receipts |
| ACH fee bearer | **Platform absorbs** | Same | Stripe `application_fee = 0` on payout side; fee aggregates to gigaton-engine COGS line, not recipient deduction |
| First-time payout exception | **No exception** | Same | No special-case logic; first payout uses identical threshold + cadence as steady-state |
| Default rail | **Stripe Connect Express** | [[payout_1_min_threshold_1k_2026_05_26]] | Operator onboarding (Stage 7+ in onboarding_v1) collects KYC + bank via Stripe Connect Express hosted flow |
| Alternative rail | **ACH** (same $1k floor, same cadence) | Same | For operators who cannot or will not use Stripe Connect Express; accumulate balances below threshold; release on next scheduled cadence when running total clears |
| Multi-currency | Convert `$1k USD` to operator's home currency at payout time; round per the LOCKED round-up rule | Same | Currency conversion at payout-emit time (not at accrual); store both USD-equivalent and home-currency amounts in payout record |
| Sub-clients | Inherit parent operator's payout config unless explicitly overridden | [[payout_1_min_threshold_1k_2026_05_26]] | E.g. `cbp_walking_tour` uses CBP's Stripe Connect Express account by default; override via `client_namespaces.governance_overlays.payout_override` JSONB key |
| **Failed-payout retry policy** | **3 retries × 24h delay → pause + notify operator** (_strawman: standard Stripe + ACH norm; tracks all 3 attempts in `payout_log` for audit; override if needed_) | — | Lives in gigaton-engine billing module retry worker; config: `max_retries=3, backoff_hours=24, on_exhaust='pause_and_notify'` |

> **Why these are locked.** The 4 PAYOUT-1 clarifications + the $1k floor closed the open clarifications dated 2026-05-25 EOD (which were originally scheduled to auto-fire as defaults on 2026-06-01). Todd ratified all 4 PAYOUT-1 + 3 INTEL-1 on 2026-05-26. They are no longer "defaults" — they are policy.

---

## 3. PLACEHOLDER — Compensation routing per entity

> **Todd: this is where you write the actual percentages.** Every TBD below carries a one-line industry-norm guidance comment so you have a defensible starting range. Do NOT auto-fire defaults — these are human-judgment-required fields.

### 3.1 Carmen Beach Properties (operator: `cbp`)

Entity type: operator (hospitality / short-term rental).
Source: [[entity_hierarchy_for_namespace_seed_2026_05_26]] §1.
Revenue model: per-booking GMV → split across owner / cleaning ops / Gigaton platform / (optionally) Ti Solutions managed-service fee.

**Ordering rule (PRE-FILLED)**: **OTA fees come off the top FIRST** (_strawman: standard industry pattern; gross booking → net after OTA → splits below apply to net; avoids paying %s on phantom revenue; override if needed_).

| Component | % of net (after OTA fee) | Cadence | Rail | Guidance |
|---|---|---|---|---|
| Owner rev share | **REMAINING after OTA + cleaning + Gigaton + Ti Solutions** (_strawman: typically ~80-85% of net for direct-booking; lower for OTA-driven inventory; override if needed_) | per-booking (accrues; pays out bi-weekly Wed if ≥ $1k) | Stripe Connect Express | Industry norm for STR owner-platform splits: 70-85% to owner. CBP-specific factor: owner brought the property + does turnover oversight |
| Cleaning ops (per-stay) | **Pass-through per-stay** (_strawman: cost = service price, not %; Gigaton invoices owner on owner's behalf; override if needed_) | per-stay (accrues; pays out bi-weekly Wed if ≥ $1k) | ACH | Industry norm: cleaning is typically passed through to guest as separate line item; if absorbed in nightly rate, ops share ~5-10% of GMV |
| Gigaton platform fee | **2.5%** of net (_strawman: industry-low to encourage operator margin during v1 beta; tunable per-operator override available; override if needed_) | per-transaction | Internal credit (no external payout) | Industry norm for hospitality SaaS platforms: 3-8% of GMV; competitive with Hostfully / Guesty / Lodgify |
| Ti Solutions service fee (only if owner elects managed-service tier) | **5%** of net (_strawman: typical BPO managed-service overhead range; override if needed_) | monthly | Internal credit | Industry norm for managed-service hospitality: 10-20% of GMV on top of platform fee; offsets Ti Solutions human-touch work (onboarding, optimization, dispute handling) |

**Sum-to-100 check**: OTA fee (off the top) → then on net: cleaning (pass-through $) + Gigaton platform (2.5%) + (optional) Ti service (5%) + owner rev share (remainder) = 100% of net.

### 3.2 CBP sub-clients (walking-tour + DMS marketing)

Entity types: DBA sub-clients of CBP.
- `cbp_walking_tour` — interactive experiences brand at `tour.playadelcarmen.homes`
- `cbp_dms_marketing` — direct marketing services brand at `services.playadelcarmen.homes`

Source: [[entity_hierarchy_for_namespace_seed_2026_05_26]] §3.1.

**Parent-pass-through rule.** Sub-client revenue flows through CBP's Stripe Connect Express account by default (sub-clients inherit parent payout config per the §2 locked rule). The `parent_operator_id` field in `client_namespaces` enables attribution rollup — `ppim_attribution_chain` will read `[cbp_walking_tour, cbp, gigaton-root]` so commission events stamp the full path.

**Sub-client-specific split** (only if Todd wants to carve out a different routing for sub-client revenue):

| Sub-client | % to sub-client owner | % to parent (CBP) | % to Gigaton platform | Cadence | Guidance |
|---|---|---|---|---|---|
| `cbp_walking_tour` | **Pass-through to CBP-parent payout config** (_strawman: single Stripe account for the entire CBP entity tree; override if needed_) | N/A (pass-through) | N/A (pass-through) | per-event | If sub-client is operationally independent (own staff, own GMV pool), might mirror §3.1; if pure CBP up-sell, parent-pass-through is sufficient |
| `cbp_dms_marketing` | **Pass-through to CBP-parent payout config** (_strawman: single Stripe account for the entire CBP entity tree; override if needed_) | N/A (pass-through) | N/A (pass-through) | per-engagement | Marketing-services revenue is typically retainer + outcome-based; structurally closer to §3.3 Ti Solutions clients than to §3.1 STR bookings |

**Per-component %s if split**: N/A (since pass-through chosen). If Todd later wants independent split-out per sub-client, populate the % columns above and remove the pass-through note.

### 3.3 Ti Solutions retainer clients (5)

Entity type: clients of Ti Solutions (BPO / sales managed-service).
Source: [[entity_hierarchy_for_namespace_seed_2026_05_26]] §1 (5 clients under `ti-solutions`).
Revenue model: base monthly retainer + outcome uplift share.

| Client (namespace_id) | Base retainer | Outcome uplift split (Ti / client) | Cadence | Guidance |
|---|---|---|---|---|
| `ti_solutions_kollosche` (AU real estate) | **STRATEGIC — Todd to fill in** | **STRATEGIC — Todd to fill in** | monthly retainer + per-deal uplift | Managed-service retainer typically $5k-$50k/mo per client; outcome-uplift commonly 5-15% of revenue lift; Gigaton platform fee typically 5-10%. Confirm per existing client contract terms. |
| `ti_solutions_medvidi` (healthcare) | **STRATEGIC — Todd to fill in** | **STRATEGIC — Todd to fill in** | monthly retainer + per-acquisition uplift | Managed-service retainer typically $5k-$50k/mo per client; outcome-uplift commonly 5-15% of revenue lift; Gigaton platform fee typically 5-10%. Confirm per existing client contract terms. |
| `ti_solutions_mcgrath` (talent) | **STRATEGIC — Todd to fill in** | **STRATEGIC — Todd to fill in** | monthly retainer + per-placement uplift | Managed-service retainer typically $5k-$50k/mo per client; outcome-uplift commonly 5-15% of revenue lift; Gigaton platform fee typically 5-10%. Confirm per existing client contract terms. |
| `ti_solutions_carerev` (healthcare staffing) | **STRATEGIC — Todd to fill in** | **STRATEGIC — Todd to fill in** | monthly retainer + per-shift-filled uplift | Managed-service retainer typically $5k-$50k/mo per client; outcome-uplift commonly 5-15% of revenue lift; Gigaton platform fee typically 5-10%. Confirm per existing client contract terms. |
| `ti_solutions_integra_ccs` | **STRATEGIC — Todd to fill in** | **STRATEGIC — Todd to fill in** | monthly retainer + per-outcome uplift | Managed-service retainer typically $5k-$50k/mo per client; outcome-uplift commonly 5-15% of revenue lift; Gigaton platform fee typically 5-10%. Confirm per existing client contract terms. |

**Routing rule**: Ti Solutions client retainers flow to Ti Solutions' Stripe Connect Express account (operator-level). Gigaton platform fee on top of retainer is **STRATEGIC — Todd to fill in** (guidance: typically 5-10% of retainer in joint-go-to-market arrangements) — separate carve-out per the joint go-to-market framing in [[product_service_package_gigaton_ti_solutions]].

### 3.4 Multipli (prospect — when active)

Entity type: prospect (vendor financing platform, NA + UK + AU markets).
Source: [[entity_hierarchy_for_namespace_seed_2026_05_26]] §1.
Status: PROSPECT — sprint output bundle was due EOD 2026-05-26.
Revenue model: performance share of Multipli net revenue per design-partner contract.

| Component | % of Multipli net rev | Cadence | Rail | Guidance |
|---|---|---|---|---|
| Performance share to Gigaton | **STRATEGIC — Todd to fill in** | monthly | Stripe Connect Express or ACH (Multipli to pick) | Vendor-financing performance share typically 10-30% of net funded volume × take rate; pending Multipli design partner contract negotiation. |
| Reciprocal credit (if Multipli refers an operator to Gigaton's platform) | **YES** (_strawman: Gigaton credits Multipli's reciprocal fee against the performance share Gigaton owes Multipli (net out at quarter close); override if needed_) | quarterly net-out | Internal credit | Reciprocal-referral mechanism reduces cash transfer overhead; net-out aligns with quarterly contract close. |

**Note**: Multipli is a PROSPECT, not yet a paying operator. Activate this section's percentages only after the design-partner contract is signed and the namespace lifecycle_state flips from `proposed` → `active`.

### 3.5 Gignet affiliates (when active)

Entity type: cross-cutting affiliate network spanning all operators.
Source: [[master_project_plan]] Chapter 11 (Gignet affiliate-network platform — 18 affiliate pages × 25 certs × 5 tiers × 8 products).
Revenue model: tier-based per-conversion commission, paid out of the operator's Gigaton platform fee.

| Tier | Per-conversion rev share % | Cadence | Rail | Guidance |
|---|---|---|---|---|
| Tier 1 (entry) | **STRATEGIC — Todd to fill in** | per-conversion (accrues; pays bi-weekly Wed if ≥ $1k) | Stripe Connect Express | Affiliate commission norms by tier: tier 1 = 5-10%, tier 2 = 10-20%, tier 3 = 20-30%, tier 4 = 30-40%, tier 5 = 40-50% (capped per master_project_plan Chapter 11); recurring-revenue tail commonly 6-24 months declining. Confirm against master_project_plan Chapter 11 tier definitions. |
| Tier 2 | **STRATEGIC — Todd to fill in** | Same | Same | Same guidance as above. |
| Tier 3 | **STRATEGIC — Todd to fill in** | Same | Same | Same guidance as above. |
| Tier 4 | **STRATEGIC — Todd to fill in** | Same | Same | Same guidance as above. |
| Tier 5 (top — Pascal certs / high-volume) | **STRATEGIC — Todd to fill in** | Same | Same | Same guidance as above; consider tail-commission on recurring revenue. |
| Recurring-revenue tail policy (any tier) | **STRATEGIC — Todd to fill in** | (e.g. 6-24 months declining) | — | Affiliate-network norm: 6-24 months declining tail (e.g. 100% → 50% → 25% over 3 quarters). Confirm against master_project_plan Chapter 11. |

**Attribution rule**: Gignet affiliate commission is computed against the conversion's `ppim_attribution_chain`. If the chain is `[cbp_walking_tour, cbp, gigaton-root]` and an affiliate referred the customer, the affiliate's commission comes out of Gigaton's platform fee slice, not out of CBP's owner share. (Source: [[2026-05-08_affiliate_centralization_at_gigaton]] — SIE chain 22 owns the canonical affiliate state; tenants attribute, they do not own.)

### 3.6 Gigaton self (platform)

Entity type: platform-root (`gigaton`).
Revenue model: internal allocation of net rev after every operator entity is paid.

| Internal bucket | % of Gigaton net rev | Cadence | Notes |
|---|---|---|---|
| Operations (cloud infra, 3rd-party API costs, ACH fees absorbed per §2, Stripe processing fees) | **45%** (_strawman: run-rate engineering + infra + customer success + admin; override if needed_) | continuous (COGS line) | Industry norm for SaaS platform ops: 25-40% of net rev |
| R&D (engineering, agent build-out, Wave 2 Intelligence Layer + Ti Agent Matrix expansion) | **25%** (_strawman: Wave 2+ build investment + ML/AI dev; override if needed_) | continuous (engineering payroll) | Industry norm for SaaS R&D: 20-35% of net rev |
| Reserves (runway, regulatory, dispute / chargeback buffer) | **20%** (_strawman: 12-month runway target; release on hit; override if needed_) | continuous (treasury) | Industry norm: 10-20% of net rev |
| Distribution to Todd / equity holders (post-runway) | **10%** (_strawman: founder + future investor distribution post-reserves-floor; override if needed_) | quarterly or per-board-decision | Activates only when reserves cleared minimum threshold (see below) |

**Reserves-floor threshold (PRE-FILLED)**: **12 months of operating expenses** (_strawman: release surplus above this to distribution; override if needed_).

**Sum-to-100 check**: ops (45%) + R&D (25%) + reserves (20%) + distribution (10%) = 100% of Gigaton net rev.

---

## 4. LOCKED — INTEL-1 / HR clarifications

These 3 clarifications were ratified 2026-05-26 EOD alongside the 4 PAYOUT-1 clarifications. They govern how the Intelligence Layer + Self-Engineered HR loops behave around money-adjacent decisions (offers, coaching nudges, talent routing).

### 4.1 HR offer human-in-loop gate

**Rule**: every HR offer requires human pre-review before it leaves the platform.

- Self-Engineered HR auto-drafts the offer (job ad copy, comp package, equity offer, retention adjustment, etc.).
- Drafted offer is routed to the operator's pre-send approval queue via `human-management-engine`.
- Operator clicks "send" or "edit & send" — only then does the offer leave the platform.
- **Why locked this way**: per `CRIT-001` ("automation requires human override") + HR offers carry legal + retention consequences that pure-LLM judgment cannot underwrite.
- **Implementation**: `persona-engine` HR module emits `OfferDrafted` event → `human-management-engine` enqueues for operator approval → gated send.

### 4.2 Coaching graduation (REVISED 2026-05-26 EOD — supersedes opt-out)

**Rule**: NO opt-out toggle. Coaching is automatically REMOVED or CHANGED per-nudge-category as the operator demonstrates competence through (a) correct UI actions and (b) accurate chat prompts.

- **Mechanism**: every operator receives coaching nudges by default. Each nudge category (e.g. "how to connect a Drive folder", "how to interpret variance display", "how to use the prompt suggestor") graduates independently as the operator demonstrates understanding.
- **Graduation criteria per nudge category**:
  - **Correct actions**: operator completed the corresponding UI flow without error `N` times (default `N=3`)
  - **Accurate prompts**: operator's chat prompts in the relevant domain hit the intent classifier with confidence `≥ 0.55` (matches our primary cosine threshold from §4.3) `M` times (default `M=2`)
  - Both criteria must be met to graduate
- **Re-emergence**: if the operator regresses (errors return, or chat prompts drop below `0.35` accuracy), coaching for that category re-activates automatically.
- **Why locked this way**: an opt-out toggle lets operators silence the system's only built-in onboarding correction; the graduation model preserves the autonomy intent (no nag once competent) without the regression risk (operator turns it off + never gets help when they need it).
- **Implementation**:
  - `agent_roles.coaching_categories` JSONB list per role defining nudge categories that role emits.
  - new table `coaching_graduation_state` per `(operator_id, nudge_category)` tracking `correct_action_count`, `accurate_prompt_count`, `graduated_at`, `last_regression_at`.
  - `persona-engine` emits nudge → checks `coaching_graduation_state` → suppresses if graduated → else delivers.
  - `decision-engine` `intelligence/classify` confidence scores feed `accurate_prompt_count` increments.
  - UI flow completions emit `CoachingProgressEvent` to `human-management-engine` → updates `correct_action_count`.
  - Spec follow-on (separate PR) to define every nudge category + its criteria thresholds; ship behind a `coaching.v2_graduation` feature flag.
- **No Settings UI**: there is NO operator-facing toggle. The Settings page will surface graduation STATUS (e.g. "You've graduated 3 of 12 coaching topics") as a transparency mechanism, but the operator cannot disable nudges directly. Regression auto-re-engages — operator's path to "no more nudges" is genuine competence, not a switch.

### 4.3 Skill-vector cosine thresholds (for downstream Ti Agent Matrix routing)

**Rule**: `0.55` primary / `0.35` secondary.

- `0.55` — cosine similarity threshold above which a skill is a PRIMARY match (drives `primary_role_key` in the agent ensemble).
- `0.35` — cosine similarity threshold above which a skill is a SECONDARY match (drives `routed_roles[]` entries, not primary).
- **Why locked this way**: standard sentence-transformers / `all-MiniLM-L6-v2` heuristic for technical-text similarity; tunable post-real-data observation.
- **Implementation**: env-readable constants in `decision-engine/engine/intelligence/semantic_classifier.py` — `COSINE_PRIMARY_THRESHOLD=0.55` + `COSINE_SECONDARY_THRESHOLD=0.35`. Override per-deploy via env. Compensation-relevance: drives which Ti Agent Matrix role earns attribution credit for a query — and downstream, any future per-role internal billing.

---

## 5. Implementation pointers

Where this document is **consumed**:

### 5.1 Stripe Connect Express config (gigaton-engine billing module)

Suggested config keys (illustrative — confirm exact field names against Stripe Connect Express docs at integration time):

```python
# pseudo-config, gigaton-engine/billing/stripe_connect.py
PAYOUT_CONFIG = {
    "minimum_amount_cents": 100_000,        # $1,000 USD floor per §2
    "schedule_interval": "weekly",          # Stripe field
    "weekly_anchor": "wednesday",            # Stripe field
    "biweekly_skip": True,                   # internal scheduler — skip every other Wed
    "rounding_mode": "ROUND_UP",             # math.ceil per §2
    "application_fee_bps": 0,                # platform absorbs per §2
    "first_payout_special_case": False,      # no exception per §2
    "retry_policy": {                        # PLACEHOLDER — needs Todd ratification per §2
        "max_retries": 3,
        "backoff_hours": 24,
        "on_exhaust": "pause_and_notify",
    },
}
```

### 5.2 Onboarding manifest reference (follow-on PR)

`master-knowledge-base/manifests/onboarding_v1.yaml` should add a link to this doc from **Stage 7 (Capability+Payouts)** (_strawman: leaf operator's payout config gathered as part of v1 onboarding's Stage 7; override if needed_). Note: this is a **follow-on PR**, not part of this scaffold.

### 5.3 gigaton-engine billing module (currently in development)

The billing module should:
1. Read §2 LOCKED rules at startup; refuse to start if any are missing.
2. Read §3 per-entity percentages from `client_namespaces.governance_overlays.compensation` JSONB (once Todd ratifies §3 → encode into UAE migration → seed per entity).
3. Emit `PayoutScheduled`, `PayoutAttempted`, `PayoutSucceeded`, `PayoutFailed` events to HME for observability.
4. Cross-reference `ppim_attribution_chain` from gigaton-gateway on every payout to ensure parent / sub-client routing per §3.2.

### 5.4 Operator-facing UI Settings (gigaton-ui-system)

Surfaces:
- **Settings → Payouts** — displays operator's configured Stripe Connect Express account, next scheduled payout date, accrued balance, $1k floor reminder, history.
- **Settings → Coaching graduation status** — transparency-only surface per §4.2 (graduation progress per nudge category); NO opt-out toggle.
- **Settings → Compensation** (admin-only, future) — displays the §3 percentages for the operator's entity; read-only for the operator.

### 5.5 user-access-engine (UAE) schema follow-on

Per [[entity_hierarchy_for_namespace_seed_2026_05_26]] §"NOT in PR #38": `compensation_terms` is NOT yet in the UAE schema. The §3 percentages, once ratified, need a home — either a new `compensation_terms` table or a `governance_overlays.compensation` JSONB key. **AUTHORIZED (PRE-FILLED)**: **YES — flag as follow-on PR; track separately** (_strawman: ship `compensation_terms` JSONB column on `client_namespaces` as a separate UAE schema PR; override if needed_). This doc does not block on it (the percentages can be source-of-truth here while UAE catches up).

---

## 6. Open items for Todd's review (FILL THESE IN)

Checklist Todd ticks off to promote this doc from DRAFT → ACTIVE. Each TBD from §3 + the §2 retry policy + the §5.2 manifest stage:

### Payout structure (§2)
- [x] Failed-payout retry policy — accept suggested default (3 retries × 24h delay → pause + notify) or specify alternative

### CBP (§3.1)
- [x] CBP owner rev share % (strawman: REMAINING after OTA + cleaning + Gigaton + Ti Solutions)
- [x] CBP cleaning ops % (strawman: pass-through per-stay)
- [x] CBP Gigaton platform fee % (strawman: 2.5% of net)
- [x] CBP Ti Solutions service fee % (strawman: 5% of net, managed-service tier only)
- [x] OTA fee ordering (strawman: off the top BEFORE split)

### CBP sub-clients (§3.2)
- [x] `cbp_walking_tour` — split or parent-pass-through? (strawman: pass-through)
- [x] `cbp_dms_marketing` — split or parent-pass-through? (strawman: pass-through)
- [x] If split: per-sub-client % to sub-client owner / parent CBP / Gigaton platform (N/A since pass-through chosen)

### Ti Solutions clients (§3.3) — **STRATEGIC**
- [ ] Kollosche — base retainer + outcome uplift split
- [ ] Medvidi — base retainer + outcome uplift split
- [ ] McGrath — base retainer + outcome uplift split
- [ ] CareRev — base retainer + outcome uplift split
- [ ] Integra-CCS — base retainer + outcome uplift split
- [ ] Gigaton platform fee % on top of Ti Solutions client retainers

### Multipli (§3.4)
- [ ] **STRATEGIC** — Performance share to Gigaton % (when contract activates)
- [x] Reciprocal credit (strawman: YES — net out at quarter close)

### Gignet affiliates (§3.5) — **STRATEGIC**
- [ ] Tier 1 per-conversion rev share %
- [ ] Tier 2 per-conversion rev share %
- [ ] Tier 3 per-conversion rev share %
- [ ] Tier 4 per-conversion rev share %
- [ ] Tier 5 per-conversion rev share %
- [ ] Recurring-revenue tail commission policy (any tier)

### Gigaton self (§3.6)
- [x] Operations % (strawman: 45%)
- [x] R&D % (strawman: 25%)
- [x] Reserves % (strawman: 20%)
- [x] Distribution % and reserves-floor threshold (strawman: 10% + 12 months opex floor)

### Implementation follow-ons (§5)
- [x] Confirm onboarding_v1.yaml stage number to link this doc from (strawman: Stage 7 — Capability+Payouts)
- [x] Authorize UAE schema follow-on for `compensation_terms` (strawman: YES — flag as separate follow-on PR)

**Pre-filled strawmen = 21 of 29; strategic-only remaining = 8 (highlighted with `**STRATEGIC**` flag in §3).**

**Promotion gate**: when every checkbox above is ticked + Todd updates the front-matter `status:` from `DRAFT` → `ACTIVE`, this doc becomes the binding policy. Until then, gigaton-engine billing module remains in dry-run mode for any operator whose §3 percentages are unset. Strawmen are accepted by default; Todd un-ticks any line to revise.

---

## 7. Decisions-log mirror

Cross-reference table linking each section to the underlying memory file and architectural-decision-log entry.

| Section | Underlying decision | Memory file | Decisions-log entry |
|---|---|---|---|
| §2 min payout `$1k` | PAYOUT-1 amendment (Todd 2026-05-26) | `payout_1_min_threshold_1k_2026_05_26.md` | PAYOUT-1 amendment (`decisions/2026-05-25_architecture_decisions_log.md`) |
| §2 rounding round-up | PAYOUT-1 clarification 1 | `payout_1_and_intel_1_clarifications_locked_2026_05_26.md` | PAYOUT-1 clarification |
| §2 cadence bi-weekly Wed | PAYOUT-1 clarification 2 | Same | PAYOUT-1 clarification |
| §2 ACH fee bearer (platform) | PAYOUT-1 clarification 3 | Same | PAYOUT-1 clarification |
| §2 no first-time exception | PAYOUT-1 clarification 4 | Same | PAYOUT-1 clarification |
| §2 default rail Stripe Connect Express | PAYOUT-1 original (2026-05-25) | `payout_1_min_threshold_1k_2026_05_26.md` (cross-ref) | PAYOUT-1 original |
| §3 entity routing | requires Todd ratification | — | (open until §6 checklist ticked) |
| §3.5 Gignet attribution | SIE chain 22 affiliate centralization | — | `decisions/2026-05-08_affiliate_centralization_at_gigaton.md` |
| §4.1 HR human-in-loop | INTEL-1 clarification (HR offer gate) | `payout_1_and_intel_1_clarifications_locked_2026_05_26.md` | INTEL-1 clarification + CRIT-001 reference |
| §4.2 coaching graduation (NO opt-out, auto-suppress via competence) | INTEL-1 clarification (coaching) — REVISED 2026-05-26 EOD | Same | INTEL-1 clarification + competence-graduation model |
| §4.3 cosine thresholds 0.55 / 0.35 | INTEL-1 clarification (classifier) | Same | INTEL-1 clarification |
| §5 Wave 2 Intelligence Layer context | INTEL-1 / INTEL-2 Wave 2 redefinition | — | `docs/architecture/2026_05_25_wave2_intelligence_layer_ti_agent_matrix.md` |

---

## 8. Revision history

| Version | Date | Author | Change |
|---|---|---|---|
| v0.1 (this scaffold) | 2026-05-26 | Claude Opus 4.7 (1M context) — under Todd direction | Initial scaffold; §2 LOCKED + §4 LOCKED + §3 TBDs awaiting Todd ratification; deadline 2026-05-28 EOD |
| v0.2 (hybrid strawman fill) | 2026-05-26 | Claude Opus 4.7 (1M context) — under Todd direction | Pre-filled 21 of 29 TBDs with industry-norm strawmen marked `(_strawman; override if needed_)`; 8 strategic %s flagged `**STRATEGIC — Todd to fill in**` (Multipli performance share + Ti Solutions 5-client retainer/uplift splits + Ti Solutions Gigaton platform fee + Gignet 5-tier commission table + Gignet recurring-revenue tail policy). §2 + §4 LOCKED decisions unchanged. |
| v1.0 (target) | 2026-05-28 EOD | Todd | Ratify the 8 strategic %s + override any strawmen + flip front-matter `status: DRAFT` → `ACTIVE` |

---

## PPIM signature

```
ppim_interaction:        meta — governs every money-out-of-platform event for every operator entity
ppim_economics:          directly determines net rev share routing across all entities
ppim_predictability:     HIGH — every payout is rule-driven; $1k floor + bi-weekly Wed cadence deterministic
ppim_brand_dimension:    trust + transparency (recipients see clean amounts; platform absorbs ACH fees; round-up favors recipient)
ppim_outcome_quality:    single ratified source-of-truth for "who gets paid what, when, via which rail"
ppim_attribution_chain:  [comp_payout_structure_v1, governance, master-knowledge-base, gigaton-root]
```
