---
name: cbp-and-playadelcarmen-world-joint-plan-2026-05-25
description: "REVISED 2026-05-25 eve. playadelcarmen.world DEFERRED; sub-client (#3.1) surfaces shipped to subdomains of playadelcarmen.homes — tour.playadelcarmen.homes (walking tour) + services.playadelcarmen.homes (DMS marketing). PHASE 1 LIVE 2026-05-25 eve. Operational activation (UAE+affiliate+license) still gated on migration + Phase3_Spec_A/B/C/D, target Sun 5/31."
metadata:
  node_type: memory
  type: project
  established: 2026-05-25
  status: PHASE 1 LIVE — sub-client customer surfaces deployed; operational activation still gated on migration
  originSessionId: adda44ad-e8aa-4a3e-bad0-7582f6c8add2
promoted_from: cbp_and_playadelcarmen_world_joint_plan_2026_05_25.md
promoted_at: 2026-06-02T20:13:25Z
---

# CBP + playadelcarmen.world joint launch plan — 2026-05-25

Full runbook: `master-knowledge-base/runbooks/2026_05_25_cbp_and_playadelcarmen_world_joint_launch_plan.md`

## Key findings (mostly state-of-world, not new decisions)

1. **playadelcarmen.homes is well-provisioned** (DNS + MX + DMARC + Firebase Hosting + 5 subdomains all live in `carmen-beach-properties`). PDC basic real estate site at `/`. Platform path `/platform/**` wired in firebase.json. UAE/decision-engine/billing/connectors all not-yet-seeded for CBP (gated on migration).
2. **playadelcarmen.world is greenfield.** No DNS zone, no Firebase site, no mail. User owns at registrar but nothing else exists. Repo stub at `/Users/admin/Documents/GitHub/playa-del-carmen` (2 commits, last 5/16).
3. **support@gigaton.ai is NOT actually a CBP-launch blocker.** Per [[canonical_correction_carmen_beach_vs_playadelcarmen]] 2026-05-16 email policy, CBP customer support belongs on `@playadelcarmen.homes` (which already exists). support@gigaton.ai is for OPERATORS talking to GIGATON — different mailbox, different audience, can complete post-beta without affecting CBP.

## Decisions — LOCKED 2026-05-25 eve

User directive: skip .world DNS in gigaton; prepare everything; migration in 1 week; get all possible live utilizing playadelcarmen.homes ASAP.

| # | Lock |
| --- | --- |
| D1 | **playadelcarmen.world DEFERRED** — not provisioning until post-migration (or further notice). All Entity #3.1 surfaces land on subdomains of playadelcarmen.homes for now |
| D2 | **Subdomain-based on playadelcarmen.homes**: tour.playadelcarmen.homes (walking tour), services.playadelcarmen.homes (DMS marketing, new A record added 2026-05-25) |
| D3 | **Use existing `playa-del-carmen` stub repo**. Multi-site Firebase Hosting deploys both subdomains from one repo. Scaffold COMMITTED 2026-05-25 eve. |
| D4 | (was .world mail) — moot |
| D5 | **Static HTML + Tailwind CDN, no build step** (faster ship than Next.js for Phase 1). Phase 2 may add Next.js post-beta if dynamic features needed |
| D6 | (was cross-domain redirect) — moot since same domain |

## Sequencing vs v0.7 (REVISED 2026-05-25 eve)

- **Mon 5/25 eve (just completed)**: A record for services.playadelcarmen.homes added; `playa-del-carmen` repo scaffold committed on branch `chore/rebrand-carmen-beach-to-pdc` with sites/tour + sites/services + firebase.json + .firebaserc + docs/FIRST_DEPLOY.md
- **Tue 5/26**: Multipli has priority. Whenever todd has 15 min: run the FIRST_DEPLOY.md steps (firebase reauth + hosting:sites:create + domain mapping in console). Both subdomains go live, Phase 1 content visible to the world.
- **Wed 5/27 morning**: content polish on tour/ + services/ (replace TODO(content) markers with real catalog + pricing + WhatsApp number)
- **Wed 5/27 eve - Fri afternoon**: MIGRATION. Static sites unaffected (no engine dependencies).
- **Fri eve - Sat**: CBP activation inputs drafted; Gigaton-self runs onboarding.
- **Sun 5/31**: CBP onboarding-v1 chat-first flow (morning). Sub-client #3.1 *onboarding* (afternoon — needs Phase3_Spec_A+B+C+D live). The sub-client's customer-facing surfaces are ALREADY live by this point; the Sun onboarding is just the operational/attribution wiring (UAE namespace, affiliate row, license row).

**Note:** decoupling the sub-client's customer surfaces (deploy any time) from the sub-client's operational activation (gated on migration + Phase3 specs) means Phase 1 marketing/booking value goes live well before Sun 5/31. This was the "get all possible live ASAP" intent.

## Critical assumption

If Phase3_Spec_A (UAE `parent_operator_id` migration) or _C (affiliate_events) or _D (licenses) hasn't shipped by Sat 5/30, sub-client (#3.1) operational onboarding cannot happen Sun. CBP itself (Entity #3) is unaffected by those specs and can still onboard. Sub-client customer-facing surfaces (`tour.playadelcarmen.homes` + `services.playadelcarmen.homes`) are decoupled — they live regardless. Fallback: ship CBP Sun, defer #3.1 *operational* activation to following week.

## Phase 1 deploy — COMPLETE 2026-05-25 eve

- `tour-pdc` and `services-pdc` Hosting sites created in `carmen-beach-properties` Firebase project
- DNS swapped from A records to CNAMEs (Firebase modern subdomain flow): `tour.playadelcarmen.homes` → `tour-pdc.web.app`, `services.playadelcarmen.homes` → `services-pdc.web.app`
- Both custom domains verified + certs provisioned (faster than the typical 15min – several hours window)
- Content deployed via `firebase deploy --only hosting` from `playa-del-carmen` repo (branch `chore/rebrand-carmen-beach-to-pdc`, commit `e30d4c6`)
- All 4 URLs return HTTP 200 with correct titles:
  - `https://tour-pdc.web.app/` ✅
  - `https://services-pdc.web.app/` ✅
  - `https://tour.playadelcarmen.homes/` ✅
  - `https://services.playadelcarmen.homes/` ✅

Firebase CLI auth lesson: `firebase login:add` adds an account; `firebase login:use` switches active. `bella@` doesn't have permissions on `carmen-beach-properties` so deploys must run as `todd@`.

## Content TODOs (post-deploy, can iterate any time)

Search `sites/{tour,services}/index.html` for `TODO(content)` and `TODO(pricing)`:

- Real tour catalog (3 placeholder cards → real names, descriptions, durations, prices, schedule)
- Real pricing tier numbers (3 `$[TBD]` placeholders)
- Real WhatsApp Business number (2 placeholder `wa.me/?text=...` links)

Edit → `firebase deploy --only hosting` to push updates.
