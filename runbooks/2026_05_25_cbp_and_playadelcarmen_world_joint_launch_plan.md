---
title: CBP + PDC Sub-client Joint Launch Plan
created: 2026-05-25
revised: 2026-05-25-eve
owner: todd@gigaton.ai
status: SCAFFOLD COMMITTED — pending user FIRST_DEPLOY actions
governs: Entity #3 (CBP) + Entity #3.1 (walking tour + DMS) activation, sequenced against v0.7 beta-activation week and the migration freeze
supersedes: nothing — fills the gap between [[beta_activation_one_week_plan_2026_05_25]] (cohort-level) and per-operator activation
---

# CBP + PDC Sub-client — Joint Launch Plan

## ⚡ REVISION 2026-05-25 eve — read this first

User directive: **skip playadelcarmen.world DNS provisioning**, assume everything should be prepared, migration in 1 week, **goal = get all possible live utilizing playadelcarmen.homes ASAP**.

**Locked decisions:**

| # | Lock |
| --- | --- |
| D1 | **playadelcarmen.world DEFERRED** until post-migration. Not provisioning DNS/MX/Firebase in gigaton-platform now. |
| D2 | **Sub-client surfaces deploy to subdomains of playadelcarmen.homes**: `tour.playadelcarmen.homes` (walking tour) + `services.playadelcarmen.homes` (DMS marketing, new A record added 2026-05-25 → 199.36.158.100). |
| D3 | **Use existing `playa-del-carmen` stub repo** for sub-client surfaces. Multi-site Firebase Hosting deploys both subdomains from one repo. **SCAFFOLD COMMITTED 2026-05-25 eve** (commit `e30d4c6` on branch `chore/rebrand-carmen-beach-to-pdc`). |
| D4 | (was .world mail) — moot under new direction |
| D5 | **Static HTML + Tailwind via CDN** (no build step) — Phase 1 ships value fast. Phase 2 (post-beta) may introduce Next.js if dynamic features needed. |
| D6 | (was cross-domain redirect) — moot since same domain now |

**Implication of this revision:** sub-client (#3.1) *customer-facing surfaces* are decoupled from *operational activation*. Surfaces can go live anytime (just needs user FIRST_DEPLOY actions). Operational activation (UAE namespace + affiliate row + license row) still gated on migration + Phase3_Spec_A/C/D, which is post-Wed 5/27 work.

**Pending user actions** (~15 min total, see `playa-del-carmen/docs/FIRST_DEPLOY.md`):

1. `firebase login --reauth`
2. `firebase hosting:sites:create tour-pdc --project=carmen-beach-properties`
3. `firebase hosting:sites:create services-pdc --project=carmen-beach-properties`
4. Firebase Console — map `tour.playadelcarmen.homes` → site `tour-pdc`
5. Firebase Console — map `services.playadelcarmen.homes` → site `services-pdc`
6. `cd ~/Documents/GitHub/playa-del-carmen && firebase deploy --only hosting`

After deploy: visible at `https://tour.playadelcarmen.homes/` and `https://services.playadelcarmen.homes/` with Phase 1 placeholder content. Content TODOs marked inline in `sites/{tour,services}/index.html`.

The rest of this document is the pre-revision plan, retained for reference. **Sections about playadelcarmen.world DNS/MX provisioning are SUPERSEDED by D1 above.**

---

## Why this runbook exists

`beta_activation_one_week_plan_2026_05_25` v0.7 says: "Sun 2026-05-31 — CBP (#3) + walking-tour DBA sub-client (#3.1) onboard." It does not say *how*. This runbook fills that gap, also covering provisioning of the new `playadelcarmen.world` domain that the sub-client will live on.

Decisions locked by [[beta_cohort_entity_structure_2026_05_25]]:
- CBP = Entity #3, independent operator, brand = **PDC**, platform domain = **playadelcarmen.homes** (already deployed at root, platform under `/platform/*`)
- Walking-tour + interactive-experiences + local-business-DMS = Entity **#3.1**, a **DBA sub-client OF CBP** — affiliate-tracked + license-gated, NOT an independent operator. Attribution rolls up to CBP via `parent_operator_id` + `ppim_attribution_chain`.

User decisions today (2026-05-25 evening):
- `support@gigaton.ai` Workspace setup is **parked-as-complete** (not blocking this plan; another operator finishes it). All references in this plan assume support@ is functional by the time CBP launch needs it (Sun 5/31).
- User owns `playadelcarmen.homes` (already provisioned in carmen-beach-properties) and `playadelcarmen.world` (not provisioned anywhere).
- `playadelcarmen.world` hosts BOTH the walking-tour customer surface AND a client-facing DMS marketing site engineered to integrate online with real-world marketing activities.

## Current state (verified 2026-05-25 evening)

### playadelcarmen.homes (CBP — Entity #3)

| Layer | State | Location |
|---|---|---|
| DNS zone | ✅ Live | `playadelcarmen-homes` zone in `carmen-beach-properties` |
| DNS records | ✅ A root + 5 subdomains (api/book/chat/shop/tour) → `199.36.158.100` (Firebase Hosting); MX + SPF + DMARC live | same zone |
| Email | ✅ admin@playadelcarmen.homes alive (Workspace MX configured) | Workspace |
| Hosting | ✅ Basic real estate site at `/` (static, must not be overwritten) | Firebase Hosting site `carmen-beach-properties` |
| Platform path | 🟡 Configured in firebase.json (`/platform/**` → Cloud Run `carmen-web`) but not yet validated end-to-end with the consolidated app | `Carmen-Beach-Properties` repo |
| Repo | ✅ Turborepo monorepo, 0-day stale, `Carmen-Beach-Properties` on disk | github.com/todd-gig/Carmen-Beach-Properties |
| UAE operator namespace | ❌ Not seeded (CBP not yet in `client_namespaces`) | UAE — gated on migration |
| Decision-engine preset | ❌ Not seeded (no Penrose preset for CBP) | decision-engine — gated on migration |
| Connector activations | ❌ None (Drive / WhatsApp / booking / Stripe TBD) | gated on UAE namespace |
| Billing setup | ❌ Stripe customer + first product package + invoice cadence not configured | gigaton-engine — gated on B3 build |
| support@ routing | 🟡 support@gigaton.ai parked; CBP-specific support routing TBD | Workspace + Gmail relay |

### playadelcarmen.world (walking tour + DMS — Entity #3.1)

| Layer | State |
|---|---|
| Domain ownership | ✅ User owns at registrar |
| DNS zone | ❌ Not in `carmen-beach-properties` or `gigaton-platform` |
| Workspace MX / mail | ❌ Not configured |
| Firebase Hosting site | ❌ Not provisioned |
| Repo | 🟡 `/Users/admin/Documents/GitHub/playa-del-carmen` stub exists (README + CLAUDE.md only, 2 commits, last 5/16). Could host this OR start fresh. |
| Sub-client UAE namespace | ❌ Not seeded (requires Phase3_Spec_A `parent_operator_id` migration first) |
| Affiliate-tracking row | ❌ Not seeded (requires Phase3_Spec_C `affiliate_events` table) |
| License row | ❌ Not seeded (requires Phase3_Spec_D `licenses` table) |
| Content (walking tour customer site) | ❌ None |
| Content (DMS client-facing marketing site) | ❌ None |

## Constraints from cohort & migration plans

From [[migration_is_value_blocking_2026_05_25]]:
> No operator activation begins until the carmen-beach-properties → gigaton-platform migration completes.

From [[beta_activation_one_week_plan_2026_05_25]] v0.7:
> Sun 2026-05-31 EOD — CBP (#3) + walking-tour DBA sub-client (#3.1) onboard.

From [[gcp_engine_migration_accelerated_2026_05_25]]:
> Wed 2026-05-27 eve = Migration session 1. Thu 2026-05-28 eve = Migration session 2. 24-48h soak. Sat 2026-05-30 = Gigaton-self full activation.

Therefore work splits into two buckets:

- **Bucket A — Can ship NOW (pre-migration, no operator-activation):** DNS provisioning, Workspace mail setup, repo scaffold, copy/content drafts, Firebase Hosting site creation in `gigaton-platform`. Anything that doesn't touch UAE / decision-engine / gigaton-engine.
- **Bucket B — Must wait for post-migration (Sat 5/30 onward):** UAE namespace seeding for CBP, sub-client `parent_operator_id` link, decision-engine preset, connector activations, billing setup, affiliate row, license row, end-to-end onboarding-v1 chat-first flow.

## Open decisions to lock (before any provisioning)

| # | Question | Suggested default | Status |
|---|---|---|---|
| D1 | Which GCP project hosts `playadelcarmen.world` DNS + Firebase site? | **`gigaton-platform`** (avoids migration debt) | pending |
| D2 | Layout: subdomains or path-based? | **Path-based: `/` = DMS marketing landing, `/tours/*` = walking tour booking**. Single Firebase Hosting site, simpler SEO, sub-client attribution preserved via path | pending |
| D3 | Repo strategy for `playadelcarmen.world` | **Use the existing `playa-del-carmen` stub** — rename if needed; add Next.js app inside it. Don't fork yet. | pending |
| D4 | Mail at `@playadelcarmen.world` — Workspace user or just MX-to-CBP? | **Workspace alias forwarding to admin@playadelcarmen.homes** (no new mailbox cost; mail is unified with CBP) | pending |
| D5 | Does the DMS site itself get a Cloud Run backend, or static-only Phase 1? | **Static-only Phase 1**, dynamic in Phase 2 (post-beta). Beta deliverable is the marketing positioning, not a functional booking flow yet. | pending |
| D6 | Walking-tour booking — reuse CBP's `book.playadelcarmen.homes` infra or new? | **Reuse via cross-domain redirect** in beta: `playadelcarmen.world/tours/book` → `book.playadelcarmen.homes/tours/*`. Post-beta, lift into its own service. | pending |

## Sequenced plan against v0.7 timing

### Tue 2026-05-26 (Multipli sprint day — DO NOT TOUCH this plan during the day)

Multipli sprint EOD has priority. No CBP/.world work during day. **Eve only, if time permits**:
- Lock D1-D6 with user (~10 min)

### Wed 2026-05-27 (morning — pre-migration window, Bucket A only)

User is preparing for migration session 1 (eve). Daytime is available for non-engine work.

**1. Provision `playadelcarmen.world` DNS in `gigaton-platform`** (~15 min):

```bash
# Enable Cloud DNS API
gcloud services enable dns.googleapis.com --project=gigaton-platform

# Create the managed zone
gcloud dns managed-zones create playadelcarmen-world \
  --project=gigaton-platform \
  --dns-name=playadelcarmen.world. \
  --description="playadelcarmen.world — walking tour + DMS marketing (Entity #3.1)"

# Capture the 4 NS records the user must paste at their domain registrar
gcloud dns record-sets list --zone=playadelcarmen-world --project=gigaton-platform \
  --type=NS --name=playadelcarmen.world.
```

User pastes those 4 NS records at the registrar (wherever they bought `.world`). Propagation: 5 min - 48 hrs (usually <1 hr).

**2. Add Workspace MX + SPF + DMARC** (~5 min, mirrors playadelcarmen.homes pattern):

```bash
# MX → Google Workspace
gcloud dns record-sets create playadelcarmen.world. \
  --zone=playadelcarmen-world --project=gigaton-platform --type=MX --ttl=3600 \
  --rrdatas="1 aspmx.l.google.com.,5 alt1.aspmx.l.google.com.,5 alt2.aspmx.l.google.com.,10 alt3.aspmx.l.google.com.,10 alt4.aspmx.l.google.com."

# SPF
gcloud dns record-sets create playadelcarmen.world. \
  --zone=playadelcarmen-world --project=gigaton-platform --type=TXT --ttl=3600 \
  --rrdatas='"v=spf1 include:_spf.google.com ~all"'

# DMARC (start with p=none, reporting to admin@playadelcarmen.homes — unified)
gcloud dns record-sets create _dmarc.playadelcarmen.world. \
  --zone=playadelcarmen-world --project=gigaton-platform --type=TXT --ttl=3600 \
  --rrdatas='"v=DMARC1; p=none; rua=mailto:admin@playadelcarmen.homes; ruf=mailto:admin@playadelcarmen.homes; fo=1; adkim=r; aspf=r"'
```

**3. Add `playadelcarmen.world` as a secondary domain in Workspace** (~5 min, user clicks):

- <https://admin.google.com/ac/domains/secondary>
- Add domain → `playadelcarmen.world` → Verify via TXT record (gcloud creates it automatically when you add a verify-token TXT)
- Once verified, set up the alias `admin@playadelcarmen.world` → forwards to `admin@playadelcarmen.homes`

**4. Provision Firebase Hosting site** (~5 min):

```bash
# In a Firebase project that lives in gigaton-platform (need to verify if one exists)
firebase projects:list
# If gigaton-platform Firebase project doesn't exist yet, create it via Firebase Console
# Then add hosting site:
firebase hosting:sites:create playadelcarmen-world --project=gigaton-platform
# Connect to domain (custom domain mapping in Firebase Console)
```

**5. Scaffold the repo** (~30 min):

```bash
cd /Users/admin/Documents/GitHub/playa-del-carmen
# It's currently a stub (README + CLAUDE.md only). Add Next.js + Firebase Hosting config.
pnpm dlx create-next-app@latest . --typescript --tailwind --app --src-dir --import-alias '@/*'
# Add firebase.json + apphosting.yaml pointing to playadelcarmen.world
# Initial content: placeholder DMS marketing landing + /tours route
git add -A && git commit -m "feat: scaffold playadelcarmen.world Next.js app"
git push
```

Defer: actual content drafting goes to Fri 5/29.

### Wed 2026-05-27 eve through Fri 2026-05-29 — MIGRATION

`playadelcarmen.world` and CBP launch work is BLOCKED. Only emergencies touch carmen-beach-properties during the migration windows.

### Fri 2026-05-29 (afternoon, post-Wave-2-deploy) — Content drafting

Bucket A still — no operator activation yet. Drafts in the `playa-del-carmen` repo:

1. **DMS marketing landing copy** — value prop for local Playa del Carmen businesses. The "engineered to integrate online with real-world marketing activities" angle is the differentiator. Sections:
   - Hero: what the integrated DMS does
   - Real-world integration examples (QR-coded brochure pickup → digital remarketing → in-store conversion, etc.)
   - Offering tiers (mapped to license tiers from Phase3_Spec_D)
   - Affiliate CTA (for partners who refer local businesses)
2. **Walking tour landing copy** — tourist-facing value prop. Sections:
   - Tour catalog (placeholder content, real catalog comes from CBP `book.playadelcarmen.homes`)
   - "Book now" → cross-domain redirect to `book.playadelcarmen.homes/tours/*`
3. **About / contact** — points back to CBP corporate, email `admin@playadelcarmen.world` (forwards to admin@playadelcarmen.homes)

Deploy to Firebase Hosting on the site `playadelcarmen-world`. Verify the SSL cert.

### Sat 2026-05-30 — Gigaton-self full activation + CBP prep

Per v0.7: "Phase 1 = Gigaton-self full activation." `gigaton@gigaton.ai` runs end-to-end onboarding-v1 on the migrated platform. This proves the substrate before CBP onboards.

**While Gigaton-self runs through onboarding (mostly automated), draft CBP activation inputs:**

- CBP's operator profile (industry, geo, regime, brand-voice)
- Penrose preset weights for vacation-rentals + tours (deviation from default)
- Initial connector targets: WhatsApp Business (for tour bookings), Stripe (for payments), Drive (for property photos / tour scripts), Calendar (for tour scheduling)
- support@ routing decision: does CBP use a dedicated support address (e.g., `support@playadelcarmen.homes` — which IS already MX'd) or share `support@gigaton.ai`? **Recommendation: dedicated `support@playadelcarmen.homes` per [[canonical_correction_carmen_beach_vs_playadelcarmen]] email policy (all CBP email at @playadelcarmen.homes).** This is what UN-blocks the support@gigaton.ai dependency — we sidestep it entirely for CBP.

### Sun 2026-05-31 — CBP + sub-client onboarding

**Morning (CBP, Entity #3):**

1. Seed UAE `client_namespaces` row for CBP (post-migration UAE)
2. Run onboarding-v1 chat-first flow as the CBP owner (Stage 0 → Stage 10)
   - Stage 0 (UAE namespace claim) — operator confirms identity
   - Stage 1 (industry) — vacation rentals
   - Stage 2 (geo / regime) — Playa del Carmen / Quintana Roo / Mexico
   - Stage 3 (brand voice) — PDC voice profile
   - Stage 4 (capability tier 1) — chat enabled
   - Stage 5 (variance check via Wave 2 spec) — submission validated against Gigmcp baseline
   - Stage 6-9 (connector activations) — WhatsApp + Stripe + Drive + Calendar
   - Stage 10 (live_auto_execute unlock)
3. Smoke: `/v1/onboarding/state?operator=cbp` returns tier_5_live; decision-engine Penrose scoreboard shows CBP rows
4. Domain wiring: `playadelcarmen.homes/platform/*` proves the Next.js consolidated app routes via gateway to CBP's namespace
5. **support routing**: `support@playadelcarmen.homes` is the customer support endpoint. Gmail rules forward to CBP's group (a `support@playadelcarmen.homes` Google Group with collaborative inbox — same pattern as [[gmail_support_relay_setup_2026_05_25]] but for the CBP domain, not gigaton.ai)

**Afternoon (sub-client #3.1):**

1. Seed UAE `client_namespaces` row for walking-tour DBA with `parent_operator_id=cbp` (Phase3_Spec_A migration must be live)
2. Seed `affiliate_events` initial referral row (Phase3_Spec_C) — establishes attribution rail
3. Seed `licenses` row granting the sub-client the DMS-services capability tier (Phase3_Spec_D)
4. Walking tour `book.playadelcarmen.homes/tours/*` cross-domain redirect from `playadelcarmen.world/tours/*` verified
5. DMS marketing landing at `playadelcarmen.world/` confirmed live
6. PPIM signature on a synthetic transaction proves `ppim_attribution_chain: ["walking-tour-dba", "cbp", "gigaton-root"]` is emitted correctly (Phase3_Spec_B)

**EOD:**

- Update `[[beta_cohort_entity_structure_2026_05_25]]` with CBP + #3.1 status = ACTIVATED
- Multipli proposal-package P-1..P-6 delivered to Ben Cahir (per v0.7)
- Write `[[cbp_and_subclient_activated_2026_05_31]]` memory documenting the final wiring

## How the support@gigaton.ai dependency actually resolves

User said support@gigaton.ai is parked. The framing of "it blocks CBP launch" turns out to be wrong on closer inspection: **CBP customer support belongs on `@playadelcarmen.homes`, not `@gigaton.ai`**, per the locked 2026-05-16 email policy. So:

- `support@gigaton.ai` = Gigaton-as-platform support (for OPERATORS like Multipli, LiqueFex, CBP themselves talking to Gigaton) — the gigaton-support-relay setup we started today is for THIS.
- `support@playadelcarmen.homes` = CBP customer support (for END USERS / tourists / guests talking to CBP) — different mailbox, different DWD setup if/when needed.
- `support@playadelcarmen.world` = (optional) sub-client support — could just alias to `support@playadelcarmen.homes` for beta (unified) or split later.

**Recommendation: defer `support@gigaton.ai` completion until post-beta (after Sun 5/31). CBP launches with `support@playadelcarmen.homes` (which already exists per MX records). This decouples the two.**

If the user disagrees and `support@gigaton.ai` IS needed before Sun 5/31 (e.g., for operator-facing support during onboarding), the runbook at [`runbooks/2026_05_25_gmail_support_relay_workspace_setup.md`](./2026_05_25_gmail_support_relay_workspace_setup.md) has the steps; total time to complete = ~15 admin clicks.

## What this plan does NOT cover

- Multipli's proposal package contents (handled by Multipli sprint runbook)
- LiqueFex activation (Entity #2, Sat 5/30; needs its own sub-plan once vertical is confirmed)
- Migration mechanics (handled by [[gcp_engine_migration_accelerated_2026_05_25]])
- Gignet affiliate-network platform full build (Chapter 11 of master plan; only the MVP slice in Phase3_Spec_C is in scope for beta)

## Cross-references

- [[beta_activation_one_week_plan_2026_05_25]] — parent week plan; this runbook is the CBP-and-3.1-specific drilldown
- [[beta_cohort_entity_structure_2026_05_25]] — entity definitions
- [[canonical_correction_carmen_beach_vs_playadelcarmen]] — email + domain doctrine (locked 2026-05-16)
- [[migration_is_value_blocking_2026_05_25]] — sequencing constraint
- [[gcp_engine_migration_accelerated_2026_05_25]] — migration mechanics
- [[gmail_support_relay_setup_2026_05_25]] — support@gigaton.ai (operator-facing) setup state
- [[product_service_package_gigaton_ti_solutions]] — GTM wrapper that contextualizes CBP as a billable operator
