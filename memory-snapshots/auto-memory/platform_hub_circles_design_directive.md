---
name: platform-hub-circles-design-directive
description: "PLATFORM-WIDE UI DIRECTIVE established 2026-05-29. /platform is the canonical hub — every app surface is reachable as a circle from this one page. Circles are bright/active (unlocked) or dim/inactive (locked); clicking a locked circle navigates the operator into the human task / education / requirement that unlocks it. Source of truth for gating = master-knowledge-base/manifests/onboarding_v1.yaml `nav_circles` + `capability_tiers` + `stages.actions[]`. Active enablement = gateway /v1/onboarding/state.nav_circles_enabled. FE primitive = useNavCircleGating + NavRail (already exists for the rail; needs PlatformPage adoption + a new locked-click destination)."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-29
  authority: directive
  scope: gigaton-ui-system + master-knowledge-base/manifests + gateway onboarding routes
  originSessionId: 95ce7a3e-1854-44fc-b54b-1d5cadd60e5a
promoted_from: platform_hub_circles_design_directive.md
promoted_at: 2026-06-02T20:13:25Z
---

# Platform Hub Circles — design directive

**Rule:** `/platform` is the single entry hub. Every app surface (page or sub-page worth top-level visibility) is rendered as a circle. Circle visual state IS the gamification surface.

**Why:** Eliminates the "trapped on /founder" failure mode + makes the value-pyramid (activities → capabilities → super-human abilities) literally visible. Operator can see at a glance what they have access to, what's coming next, and exactly what to do to unlock the next capability.

**How to apply:**

1. **Two states only — bright (unlocked) and dim (locked).**
   - Bright = `nav_circles_enabled` (from gateway `/v1/onboarding/state`) contains this circle_id.
   - Dim = it does not. Render with greyscale + reduced opacity + lock badge (mirror the existing NavRail styling).

2. **Clicking a bright circle navigates to its `route`.** Standard SPA navigation. Use the manifest's `route` field.

3. **Clicking a dim circle MUST navigate into the unlock path** — not just a tooltip. The unlock path is the canonical chat-first onboarding flow at `/chat?onboarding=stage-<N>`, where the stage is the LAST entry in `capability_tiers[tier_required].unlocked_by_stages[]`. The chat orchestrator already drives the operator through that stage's `actions[]` (human task / education_ref / auto_complete_on event). This means:
   - No new "unlock detail modal" needed for v1 — reuse the existing chat onboarding orchestrator as the unlock UI.
   - On stage completion the backend flips `nav_circles_enabled` → circle becomes bright on next /v1/onboarding/state poll. No FE state-machine to write.

4. **Source of truth = the manifest, not hardcoded JSX.** PlatformPage renders by mapping `manifest.nav_circles` → `<CircleNode>`. Never hardcode a circle in JSX. To add or rename a circle, edit `master-knowledge-base/manifests/onboarding_v1.yaml` and ship a manifest version bump. The FE reads the resolved manifest from `GET /v1/onboarding/manifest`.

5. **Role-gated circles (Founder / Owner / Admin) layer ON TOP of tier gating.** Founder already has `additional_gate: '@gigaton.ai email domain'` in the manifest. Owner + Admin need the same pattern (`additional_gate: 'role:owner'` / `'role:admin'`). Hide entirely if role missing — don't show a dim circle the operator can never unlock.

6. **The hero `FARM` center node** stays as the visual anchor. It navigates to `/dashboard` (operator's primary daily ops view).

7. **Layout = concentric orbits, not single ring.** Inner orbit = Tier 1-2 capabilities (immediate). Outer orbit = Tier 3-5 + role-gated (aspirational). This makes the "next thing to unlock" visually closer to the operator's current orbit. Reuse the existing `SatelliteNode` styling in PlatformPage.tsx.

8. **Sub-pages do NOT get top-level circles.** `/connectors/*` sub-pages live behind one "Connectors" circle. `/founder/*` sub-pages stay as panels inside FounderPage. `/admin/review-queue`, `/owner/recruitment` etc. live as panels inside their parent role page. Top-level circles = capabilities, not pages.

9. **Anti-patterns:**
   - Static decorative satellite nodes with no onClick (today's PlatformPage has 5 of these — must be replaced).
   - Hardcoding the circle list in JSX (loses manifest as source of truth).
   - Modal overlays for "what unlocks this" — push to the chat orchestrator instead.
   - Hiding a circle entirely just because it's tier-locked — locked-but-visible IS the value of this UX.
   - A circle whose route doesn't exist (e.g. current manifest references `/people`, `/brand`, `/goals`, `/processes`, `/assignments`, `/influence-vs-cost` — none built). Either build the page, re-point to an existing surrogate, or remove from manifest.

10. **Universal mount.** PlatformPage is the only place circles render as a hub. The existing `NavRail` (left rail on /chat + /cowork) stays as the per-page mini-launcher mounted globally (separate cleanup item — see related platform-wide directives).

## Ratified design decisions (2026-05-29)

These four calls were made by Todd directly. Do NOT relitigate without explicit instruction.

1. **Manifest reconciliation = BUILD the missing pages.** Honor the manifest as authored. Build the 6 missing pages (`/people`, `/brand`, `/goals`, `/processes`, `/assignments`, `/influence-vs-cost`) as real surfaces. ALSO add the 5 unmapped live surfaces to the manifest as new circles (`/intelligence` → tier_2_personalized, `/cowork` → tier_3_recommend, `/connectors` → tier_1_data, `/owner` → role-gated, `/admin` → role-gated). Final circle count = ~16 (chat + sources + dashboard + connectors + people + brand + intelligence + goals + org-processes + cowork + assignments + influence-cost + calibration + founder + owner + admin).
   - **Why:** the manifest is the source of truth; reality must match it, not the other way around. Surrogate-pointing would dilute the activities→capabilities→super-human-abilities ladder.
   - **Cost honesty:** ~3-5 days of new UI work to ship the 6 missing pages before the hub is fully wired. Hub can ship in stages — circles for built pages go bright on day 1, others stay dim with valid unlock paths.

2. **Locked-click destination = `/chat?onboarding=stage-N`.** No modal, no inline expansion. Operator clicks dim circle → SPA-navigate into the chat orchestrator at the unlocking stage. Hover still shows the existing NavRail-style tooltip for previewing.
   - **Why:** zero new UI to build, reuses the proven chat-first onboarding flow, backend auto-flips circle on stage completion via existing `auto_complete_on` events. No FE state machine to write.

3. **Layout = concentric orbits by tier.** Center = FARM (→ /dashboard). Inner orbit = tier_1_data + always. Middle orbit = tier_2_personalized + tier_3_recommend. Outer orbit = tier_4_costs + tier_5_live + role-gated. The visual radius IS the capability-pyramid distance.
   - **Why:** operator's current orbit visually shows where they are; outer dim orbits show the super-human-ability tier as aspirational. Matches the value-pyramid mental model 1:1.

4. **Role-gated circles HIDE ENTIRELY when operator lacks role.** Founder/Owner/Admin circles only render for operators with `@gigaton.ai` email (Founder) or `role:owner` / `role:admin` claims. No dim "you can't have this" affordance. Tier-locked circles still show dim — only role-locked hide.
   - **Why:** tier-locked = "you will earn this"; role-locked = "this is for a different person". Showing role-locked circles dim creates confusion + false hope. Tier circles bring the gamification value; role circles don't.

## Source-of-truth references

- **Manifest:** `master-knowledge-base/manifests/onboarding_v1.yaml` (1146 lines; 11 circles, 5 tiers, 10 stages)
- **FE gating hook:** `gigaton-ui-system/hooks/useNavCircleGating.ts`
- **Existing rail implementation:** `gigaton-ui-system/components/NavRail.tsx` (pattern to mirror in PlatformPage)
- **Hub page:** `gigaton-ui-system/pages/PlatformPage.tsx` (currently static decoration — needs manifest-driven rewrite)
- **Gateway state endpoint:** `GET /v1/onboarding/state?operator_id=…` → `{ nav_circles_enabled: string[], current_stage_id: string, tier: ... }`
- **Gateway manifest endpoint:** `GET /v1/onboarding/manifest?operator_id=…` (ETag-aware)
- **Unlock destination pattern:** `/chat?onboarding=stage-<N>` where N is `capability_tiers[tier_required].unlocked_by_stages.at(-1)`

## Cross-refs

- [[directive_navigation_aware_intelligence_coaching_2026_05_28]] — adjacent doctrine; CoachingStrip / CapabilityLadder live INSIDE pages once you arrive at them. The circles hub is the GLOBAL view; that doctrine is the per-page view.
- [[uaf_phase_c_shipped_2026_05_28]] — auto-UI composer (server-driven component registry) lives at /acquisition-demo currently; long-term the hub circles could compose page bodies via the same registry.
- App.tsx routes: 41 routes currently exist; circles hub reduces this to ~12-14 top-level entries.
