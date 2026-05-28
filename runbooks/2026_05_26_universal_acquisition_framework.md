# Universal Acquisition Framework — Implementation Runbook

**Status:** SPEC — drafted 2026-05-26 from Todd directive
**Repos in scope:** `intelligence-silo`, `user-access-engine`, `gigaton-ui-system`, `decision-engine`, `master-knowledge-base`, `gigaton-gateway`
**Effort estimate:** ~4 weeks, ~10 PRs, sequences AFTER GCP migration + Wave 2 Week-1 substrate + Q&A pipeline Phase 2
**North star:** [[foundational_goal_maximize_human_superpowers]] — every UI surface this framework generates must measurably leave the user MORE capable than before they engaged.

---

## 1. Origin

User directive (verbatim, 2026-05-26):

> "we have a sales process + multiple processes > create complete acquisition process to be utilized as framework and applied to customer, client, and talent + affiliate + alt user categories with goal of being able to enable automatically UI development of system based on user actions + needs + gigaton interest in promoting services > functionalities > super human powers enabled"

Today the platform has:

- A sales process (sales-operating-system catalog + Sales-OS reframe per [[sales_os_reframe_and_wave2_decisions_2026_05_25]])
- An operator onboarding flow (chat-first 10-stage per [[onboarding_workflow_v1_completion_verified_2026_05_22]])
- An affiliate network spec (Gignet Ch 11 of [[master_project_plan]])
- A talent dispatch matrix (Wave 2 Ti Agent Matrix, in build)

These run as **disconnected funnels**. This runbook unifies them into a single substrate with category overlays.

---

## 2. Architecture

### 2.1 The 7 stages (shared substrate, applied to all 5 categories)

| # | Stage | What happens | Data primitive |
|---|---|---|---|
| 1 | Awareness | First signal observed (visit, ad-touch, doc-fetch, intro-DM, referral click) | `SignalEvent` (pre-IDP) |
| 2 | Identification | Identity resolved across channels; IDP profile created/updated; provisional category vector assigned | `IDPProfile` (post-resolve) |
| 3 | Qualification | 10 Intelligence Dimensions scored; ethnographic frames projected; trust tier T0-T4 assigned; needs inferred | `NeedsProfile` |
| 4 | Engagement | Auto-generated UI surface presents matched superpower/functionality/service; Ti Agent Matrix dispatches conversation | `OfferRendering` + Intelligence Layer session |
| 5 | Onboarding | Category-specific manifest executes (customer/client/talent/affiliate/alt-user) | Manifest run + signoff events |
| 6 | Activation | First value event delivered (category-specific success metric trips) | `ActivationEvent` → Penrose scoreboard |
| 7 | Compounding | Memory accumulates, dispatch sharpens, real-time coaching activates, HR signal fires on utilization | Memory writes + HME utilization scan |

### 2.2 The 5 categories with overlays

| Category | Primary metric | LTV horizon | Specialized stage tweaks |
|---|---|---|---|
| **Customer** | Revenue per customer | 1-3 yr | Awareness via marketing channels; activation = transaction |
| **Client** (operator) | Platform ARR + tier-unlock depth | 3-7 yr | Onboarding = 10-stage manifest; activation = Tier_5_live |
| **Talent** | Utilization × accept-rate × retention | 5-10 yr | Qualification via skill_vectors cosine match; engagement = first dispatch |
| **Affiliate** | Referred-LTV × commission economics | 2-5 yr | Engagement = tracking link issuance; activation = first attributed conversion |
| **Alt-user** | Strategic optionality value (qualitative) | Variable | Qualification via custom NDA/scope; engagement may be ongoing dialog |

### 2.3 Data plane

```
SignalEvent (Firestore: unauthenticated_signals)
   ▼
IDP resolution worker → IDPProfile (Postgres: idp_profiles)
   ▼
NeedsProfile = needs_inference(IDPProfile, intelligence_silo)
   │   uses: 10 Intelligence Dimensions + ethnographic frames + Variable Registry
   ▼
OfferSet = offer_matcher(NeedsProfile, gigaton_promotion_priorities)
   │   ranks Gigaton-owned superpowers; biased by promotion config
   ▼
UI Auto-Gen Renderer composes from registered components
   │   gigaton-ui-system/components/auto/*
   ▼
Engagement via Intelligence Layer (/intelligence page, Ti Agent dispatch)
   ▼
Category-specific Onboarding Manifest (master-knowledge-base/manifests/*)
   ▼
ActivationEvent → Penrose 8-metric scoreboard
   ▼
Compounding (memory hierarchy + HME utilization + Self-Engineered HR)
```

---

## 3. Component-by-component spec

### 3.1 SignalEvent + capture (Stage 1)

- **New endpoint:** `POST /v1/acquisition/signal` on gigaton-gateway (unauthenticated, rate-limited).
- **Body:** `{event_type, channel, page_url?, referrer?, device_fingerprint, geo, language, intent_hint?, timestamp}`.
- **Storage:** Firestore `unauthenticated_signals` collection.
- **Triggers:** writes to `gignet-orchestrator` topic with `task=acquisition.signal_received` for fan-out.

Detailed wire-format contract: see [[uaf_phase_a_shared_schemas]].

### 3.2 IDP profile + resolution (Stage 2)

- **New table (UAE):** `idp_profiles` — `id, primary_identity, alt_identities[], provisional_category_vector jsonb, first_seen_at, last_seen_at, signal_count, resolved boolean`.
- **Resolver worker:** matches `device_fingerprint` + email + phone + auth cookies across SignalEvents → upserts IDPProfile.
- **Category vector:** initially uniform over 5 categories; updated by every subsequent signal via NeedsProfile inference.

Detailed wire-format contract: see [[uaf_phase_a_shared_schemas]].

### 3.3 NeedsProfile inference (Stage 3)

- **New module:** `intelligence-silo/core/intelligence/needs_inference.py`.
- **Function:** `infer_needs(idp_profile, recent_signals[]) -> NeedsProfile`.
- **NeedsProfile shape:**

  ```python
  @dataclass
  class NeedsProfile:
      dimensions_strong: list[IntelligenceDimension]  # which of the 10 they bring
      dimensions_gap: list[IntelligenceDimension]     # which they need from us
      ethnographic_frames: dict[str, list[str]]       # frame -> tags
      latent_needs: list[str]                          # inferred from signals
      inferred_intent: str                             # short phrase
      category_confidence: dict[str, float]            # 5 categories → confidence
      trust_tier: int                                  # T0-T4
      language_primary: str                            # ISO 639-1
      language_alt: list[str]
  ```

### 3.4 Offer matcher (Stage 4 input)

- **New module:** `intelligence-silo/core/intelligence/offer_matcher.py`.
- **Function:** `match_offers(needs_profile, promotion_priorities) -> OfferSet`.
- **OfferSet shape:**

  ```python
  @dataclass
  class Offer:
      superpower_id: str          # e.g. "operate-a-property-business-solo"
      functionality_ids: list[str] # e.g. ["pricing-auto-optimize", "guest-msg-auto-respond"]
      service_package_id: str     # e.g. "carmen-beach-platform-tier-2"
      match_score: float           # 0-1
      promotion_weight: float      # from config
      composite_rank: float        # match_score * promotion_weight
      evidence: list[str]          # why this matched (citations)
  ```

### 3.5 UI Auto-Gen Renderer (Stage 4)

- **New module (FE):** `gigaton-ui-system/lib/autoUiComposer.ts`.
- **Function:** `composePage(idp_profile, needs_profile, offer_set) -> JSX.Element`.
- **Component registry:** `gigaton-ui-system/components/auto/registry.ts`:

  ```typescript
  export const AUTO_COMPONENTS = {
    HeroCard: { props: ["superpower_headline", "supporting_proof"] },
    FunctionalityProof: { props: ["functionality_id", "demo_mode"] },
    CTAStrip: { props: ["service_package_id", "tier_unlock_path"] },
    DispatchedAdvisor: { props: ["ti_agent_ensemble"] },
    QualificationDashboard: { props: ["dimensions_known", "dimensions_to_ask"] },
    LanguageToggle: { props: ["language_primary", "language_alts"] },
  };
  ```

- **Composer rules:**
  - If `needs_profile.category_confidence` has clear leader (>0.8) → render category-specific manifest entry.
  - Else render top-3 offers as competing HeroCards (lets behavior break the tie).
  - Always render `LanguageToggle` if `language_primary != "en"` OR `language_alt` non-empty.
  - Always render `QualificationDashboard` (per [[foundational_goal_maximize_human_superpowers]] — qualification must be visible).

### 3.6 Promotion-priority config (Stage 4 ranking input)

- **New file:** `decision-engine/config/gigaton_promotion_priorities.yaml` — see memory file [[universal_acquisition_framework_2026_05_26]] §"Gigaton promotion-priority signal" for shape.

### 3.7 Category-specific onboarding manifests (Stage 5)

- **Existing:** `master-knowledge-base/manifests/onboarding_v1.yaml` (CLIENT).
- **New:**
  - `manifests/acquisition/customer_v1.yaml` — checkout + access + product walkthrough
  - `manifests/acquisition/talent_v1.yaml` — role contract + skill_vector capture + first-dispatch criteria
  - `manifests/acquisition/affiliate_v1.yaml` — tracking link + terms + initial referral kit
  - `manifests/acquisition/alt_user_v1.yaml` — NDA/scope + scoped-access provisioning

### 3.8 Activation events (Stage 6)

- **Pattern:** existing Penrose 8-metric scoreboard receives `ActivationEvent{category, idp_profile_id, metric, value}`.
- **Per-category metric mapping** lives in `decision-engine/config/activation_metrics.yaml`.

### 3.9 Compounding loop (Stage 7)

- Leverages existing infra:
  - Memory hierarchy ([[wave2_intelligence_layer_ti_agent_matrix]] §2.2)
  - HME utilization sweep (Wave 2 §8)
  - Self-Engineered HR trigger thresholds (Wave 2 §8)
- New: per-IDP-profile compounding metrics view: `views/compounding_per_profile.sql`.

---

## 4. Implementation phases

### Phase A — Substrate (Wk 3 of Wave 2)

- Signal capture endpoint + Firestore collection
- IDP resolution worker + Postgres table
- Provisional category vector
- **Effort:** 1.5 days

### Phase B — Intelligence inference (Wk 4)

- `needs_inference.py` (depends on Q&A pipeline Phase 2 — shares the qualification primitives)
- `offer_matcher.py`
- Promotion-priority config + ratification
- **Effort:** 2.5 days

### Phase C — Auto-UI renderer (Wk 5)

- Auto component registry (6 components)
- `autoUiComposer.ts` composition rules
- Language toggle wiring
- E2E test: synthetic IDP profile → composed page → snapshot
- **Effort:** 3 days

### Phase D — Onboarding manifests (Wk 5)

- 4 net-new YAMLs (customer / talent / affiliate / alt-user)
- Manifest loader reads category overlay + base 7-stage
- **Effort:** 2 days

### Phase E — Activation + Compounding (Wk 6)

- ActivationEvent wired to Penrose scoreboard
- Per-category metric config
- Compounding view
- HR-signal threshold check
- **Effort:** 1.5 days

### Phase F — Onboard first cohort across all 5 categories (Wk 6 close)

- Customer: one real Carmen Beach guest
- Client: Multipli vendor as cohort #1 ([[multipli_vendor_growth_engine_sprint_2026_05_22]])
- Talent: one role recruit via existing affiliate channel
- Affiliate: one Ti Solutions affiliate
- Alt-user: one researcher access grant
- **Effort:** 0.5 day instrumentation; cohort-driven calendar

**Total:** ~10 engineering days for v1; ~4 calendar weeks given Wave 2 sequencing.

---

## 5. Sequencing constraints

| Blocker | Why it sequences before this framework |
|---|---|
| GCP migration | `idp_profiles` table + signal collection should live in `gigaton-platform` from day 1 |
| Wave 2 Week-1 substrate | Ti Agent Matrix dispatch is required for Engagement stage |
| Q&A pipeline Phase 2 | NeedsProfile inference reuses qualification primitives (10 Intelligence Dimensions scoring + ethnographic frames + principles filter) |
| Compensation+payout structure (Thu 5/28) | Talent + affiliate overlays need payout rails locked |
| Namespace enforcement decision | IDP profile + signal capture must be namespace-scoped from day 1 ([[mcp_multi_tenant_namespace_blocker_2026_05_26]]) |

---

## 6. Open decisions

1. **Promotion priority Q2 list** — what 3-5 superpowers lead?
2. **Alt-user sub-categorization** — named sub-types vs catch-all?
3. **UI auto-gen guardrails** — what surfaces stay hand-built vs auto-composed?
4. **Identity resolution privacy boundary** — how aggressively do we cross-channel match before explicit consent? Likely answer: only post-auth (so unauthenticated signals stay anonymous until user authenticates).

---

## 7. Critical files

- `intelligence-silo/core/intelligence/dimensions.py` (existing, source of truth for qualification)
- `intelligence-silo/core/intelligence/ethnographic_frames.py` (Q&A pipeline Phase 2 — prereq)
- `intelligence-silo/core/intelligence/needs_inference.py` (NEW)
- `intelligence-silo/core/intelligence/offer_matcher.py` (NEW)
- `user-access-engine/migrations/00XX_idp_profiles.sql` (NEW)
- `gigaton-gateway/app/routes/acquisition.py` (NEW)
- `gigaton-ui-system/lib/autoUiComposer.ts` (NEW)
- `gigaton-ui-system/components/auto/*` (NEW — 6 components)
- `decision-engine/config/gigaton_promotion_priorities.yaml` (NEW)
- `decision-engine/config/activation_metrics.yaml` (NEW)
- `master-knowledge-base/manifests/acquisition/{customer,talent,affiliate,alt_user}_v1.yaml` (NEW)
