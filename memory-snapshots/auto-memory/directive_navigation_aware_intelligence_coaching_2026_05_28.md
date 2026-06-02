---
name: directive-navigation-aware-intelligence-coaching-2026-05-28
description: "Platform-wide directive (Todd 2026-05-28). The Human Intelligence Engine MUST surface contextual intelligence + capability-unlock reminders to the operator AS they navigate pages — not only via daily-batch nudges. Every page must answer: (1) what value flows here NOW given current connections/sources, (2) what additional source/channel/input would unlock the next capability up the value pyramid (functionality → capability → superhuman), (3) what's the smallest next action. Surfacing layer = NotificationBell + inline empty-state + persistent CoachingStrip. Data layer = Phase Gate status + Coverage Completeness scoreboard + HIE live ranking. Extends existing daily Insights/Coaching engines with page-context awareness; supersedes their dashboard-only surfacing assumption."
metadata:
  node_type: memory
  type: feedback
  established: 2026-05-28
  status: ACTIVE — 5 build PRs OPEN (4 DRAFT + 1 docs) across UAE/gateway/UI/silo/mkb (same-day execution 2026-05-28)
  lifecycle_state: canonical
  originSessionId: c3d6a014-f8e0-4829-9d0d-6197cc8ac3f6
promoted_from: directive_navigation_aware_intelligence_coaching_2026_05_28.md
promoted_at: 2026-06-02T20:13:25Z
---

# Navigation-Aware Intelligence Coaching

## The directive (verbatim 2026-05-28)

> "ensure that the human intelligence engine intelligence > notifications are provided to user + reminders to enable user to extract value, ex: additional sources, additional channels, etc to unlock extra capabilities > super humans AS the human navigates to pages within the system"

## What this requires (and what's NEW vs existing specs)

The system already has six engines that touch parts of this — they are **dashboard-batch surfaces**, not navigation-aware. This directive adds the missing piece: **per-page contextual intelligence + capability-ladder coaching that fires on navigation, not on a daily sweep.**

| Layer | Existing | NEW per this directive |
|-------|----------|------------------------|
| Daily insight generation | [[super_ability_proactive_insights_nudges]] — runs 06:00 CT, surfaces on Today's Insights panel | Augmented with `page_context` field per insight; insights re-rank when user lands on a page where they're more actionable |
| Bias/coaching nudges | [[super_ability_operator_coaching_engine]] — weekly digest | Surface relevant bias nudges inline on the very page where the bias manifests (e.g., D3 override pattern → show on decisions page) |
| Multi-channel delivery | [[super_ability_push_notifications_system]] — in-platform / email / SMS / FCM | Add `in_app_contextual` channel: a non-modal coaching strip that renders on specific pages without firing a push |
| Empty-state + Day 7/10/14/30 | [[empty_state_guidance_onboarding_nudges]] — fires by elapsed days | Add capability-ladder-aware empty states: shows which superpower unlocks at the next capability tier, what input enables it, smallest next action |
| Progressive enrichment cap | [[feedback_progressive_source_enrichment]] — 4→9 sources post-Day-10 | Page-context aware: on `/connections`, show "connect Gmail to unlock customer-DM-coaching" rather than just "you have N sources" |
| Capability computation | [[user_access_engine_capability_computation]] — `/access/{user_id}/capabilities` | Pair with `/v1/capabilities/next-unlocks` — what is the operator one connection / one input / one action away from |
| Phase Gate status | Per [[phase_gate_ratification_2026_05_28]] §1+§5 ratified; backend builds Fri-Sat 5/29-5/30 | The single source of truth for tier-up coaching ("you are in Phase 3 Connector Integration; 2 more connectors unlock Phase 4 Decision Loop") |
| Universal acquisition UI auto-gen | [[universal_acquisition_framework_2026_05_26]] — composes UI from observed-needs + promotion-priority | This directive applies the same composer pattern to *operators already inside the platform* (progression), not just to acquisition (entry) |

## The runtime model

```
ON NAVIGATION (operator lands on any page)
   │
   ▼
PageContextSignal { page_id, operator_id, route_params, referrer, time_on_prev_page }
   │
   ▼
HIE Live Ranking (intelligence-silo + decision-engine)
   │  inputs:
   │  - PhaseGate status (current phase, gate criteria progress, deliverables_complete/required)
   │  - Coverage Completeness scoreboard ([[context_completeness_doctrine_2026_05_26]])
   │  - Connected-sources inventory + per-source utilization
   │  - Last 30d operator decision/override patterns
   │  - Gigaton promotion priority (per-quarter superpower bias from acquisition framework yaml)
   │  - 10 Intelligence Dimensions per-operator scores (which dimensions are gap)
   │  - Penrose 8-metric scoreboard (drift signals)
   │  ranks:
   │  - applicable_insights[]    (from daily-generation pool, filtered by page_context)
   │  - capability_ladder_step   (the single next-best unlock for THIS page's value)
   │  - bias_or_coaching_nudge   (if a personal pattern is relevant here)
   │  - reminder_strip           (any unfilled commitment / overdue input)
   ▼
SurfaceComposer
   │  decides per item:
   │  - NotificationBell badge  (urgent / cross-page; e.g., FTC cert expiring)
   │  - Inline EmptyState        (page has no data yet → contextual onboarding)
   │  - CoachingStrip            (non-modal banner above page content; explains the unlock)
   │  - SidebarHint              (small persistent hint near the relevant control)
   │  - Modal                    (only for critical / sign-off-required)
   ▼
Operator sees:
   - what value flows on THIS page right now given current state
   - what specific next source/channel/input unlocks the next capability
   - one-click action to do it (or "remind me later" / "don't show me this")
```

## Required endpoint additions (slot into Phase Gate companion)

The Phase Gate companion endpoints §2.2 (per ratified design doc, builds Fri-Sat) already plan to expose phase status. Extend with TWO additional routes to power navigation-aware coaching:

1. **`POST /v1/coaching/page-context`** — body `{ page_id, route_params }`; returns `{ applicable_insights[], capability_ladder_step, bias_nudge, reminders[] }`. Called by every page on mount.
2. **`GET /v1/capabilities/next-unlocks?limit=N`** — returns the ranked list of "next things you could do to climb the value pyramid," each with `{ unlock_name, current_blocker, smallest_action, target_capability, est_value_delta }`.

Both endpoints honor operator-scoped tokens + `permitted_operator_ids` (parent operators see read-only progression for managed children, per [[phase_gate_ratification_2026_05_28]] §5).

## Required gigaton-ui-system additions

Slot into post-Phase-Gate UI follow-up (week of 2026-06-01):

- `components/coaching/CoachingStrip.tsx` — non-modal banner; props `{ headline, body, primary_action, secondary_actions, dismissable }`; renders above page content when present.
- `components/coaching/CapabilityLadder.tsx` — visual progression up the value pyramid (functionality → capability → superhuman) with the operator's current rung highlighted + next rung's required inputs.
- `components/coaching/SidebarHint.tsx` — small persistent hint near the relevant control on the page (e.g., near the "Add connection" button: "Gmail unlocks customer-DM-coaching").
- `hooks/usePageCoaching.ts` — calls `/v1/coaching/page-context` on mount; returns ranked surface items.
- Wire `<CoachingStrip />` into every page layout via the root `IntelligenceLayout` (similar pattern to where `<NotificationBell />` mounts per [[red_phone_v0_build_state_2026_05_27]]).

## Anti-patterns (this directive's job to prevent)

- **Page-blank with no guidance.** Every operator-facing page MUST surface either real data OR a contextual coaching item. Blank ≠ acceptable. (Reinforces [[empty_state_guidance_onboarding_nudges]] but extends it to ALL pages, not just first-time.)
- **Generic "do something" CTAs.** Coaching must name the specific next source/channel/input AND the specific capability it unlocks. "Connect more sources" is forbidden; "Connect Gmail to unlock customer-DM coaching" is required.
- **Dashboard-only intelligence.** If an insight is relevant to a specific page, it surfaces THERE — not only on the dashboard. Operator should not have to navigate away to see what's relevant where they are.
- **Daily-batch staleness.** Page-context coaching is live (ranked on navigation), not yesterday's pre-computed list filtered.
- **No reminder loop.** A capability-unlock recommendation that's been dismissed-deferred must re-surface on a sensible cadence (operator can mute permanently; "remind me later" defaults to 7 days).
- **Pushing toward unlocks the operator can't yet act on.** The ranker must respect phase-gate prerequisites (don't surface "enable auto-execute" coaching while operator is still in Phase 3 connector integration; surface the Phase 3 → 4 unlock instead).

## How to apply going forward

1. **Phase Gate companion build (Fri 5/29 – Sat 5/30):** add the two new endpoints (`POST /v1/coaching/page-context` + `GET /v1/capabilities/next-unlocks`) to the build slate. ~0.5 day additional effort against the ratified ~3.5d total. Update `phase_gate_ratification_2026_05_28` build slice table when this lands.
2. **gigaton-ui-system follow-up (week of 2026-06-01):** the four components + the hook + the layout wiring. Ship behind a feature flag for the cohort.
3. **HIE live-ranker (intelligence-silo extension, week of 2026-06-08):** factor the daily Insights engine logic out so it can run per-request with page_context filtering. Cache hot per-operator results for 5min to bound load.
4. **Per-page coaching content library:** as each new page ships, author its `applicable_insights` predicates + the page's "what unlocks next" mapping. Owned by whoever ships the page. Lives in `gigaton-ui-system/coaching-registry/`.

## Build PRs (opened 2026-05-28 same-day; parallel worktree-isolated agents)

| Repo | PR | Branch | State | What |
|------|----|--------|-------|------|
| user-access-engine | [#53](https://github.com/todd-gig/user-access-engine/pull/53) | `feat/coaching-endpoints-2026-05-28` | DRAFT, mergeable | 2 endpoints + 17 tests; reuses `phase_gate.resolve_permitted_operator_ids`; no migration |
| gigaton-gateway | [#76](https://github.com/todd-gig/gigaton-gateway/pull/76) | `feat/phase-and-coaching-routes-2026-05-28` | DRAFT, MERGEABLE | Wires 2 coaching/capabilities routes + 7 regression tests for phase routes (PR #72 already wired phase routes — sibling discovery prevented duplicate work) |
| gigaton-ui-system | [#58](https://github.com/todd-gig/gigaton-ui-system/pull/58) | `feat/coaching-ui-components-2026-05-28` | DRAFT, MERGEABLE | 4 components + 2 hooks + lib/coaching + coaching-registry (5 page mappings); 55 tests pass; build succeeds |
| intelligence-silo | [#64](https://github.com/todd-gig/intelligence-silo/pull/64) | `feat/hie-live-ranker-scaffold-2026-05-28` | DRAFT | `core/coaching/` scaffold seam (live_ranker / page_context / registry); 22 tests; no integration yet |
| master-knowledge-base | [#33](https://github.com/todd-gig/master-knowledge-base/pull/33) | `docs/coaching-content-library-2026-05-28` | OPEN (docs) | Full runbook + content-library README + 10 seed page-mapping YAMLs |
| gigaton-ui-system | [#60](https://github.com/todd-gig/gigaton-ui-system/pull/60) | `feat/coaching-layout-mount-2026-05-28` (STACKED on #58) | DRAFT | `GlobalCoachingStrip` mount + `usePageCoachingForCurrentRoute` route-aware hook; silent-until-actionable render; mounted in `App.tsx` after `<DirectedWorkflowBanner />` inside HashRouter; 20 tests pass |

**Cross-ref — promotion-priority YAML is already shipped:** decision-engine PR #91 (merged 2026-05-28) landed `config/gigaton_promotion_priorities.yaml` with 3 Q2 superpowers (operate-a-property-business-solo / be-your-own-CFO-CMO-CISO-with-AI-dispatch / scale-talent-network-via-affiliate-recruiting) seeded under INTEL-3 doctrine. Plus `config/activation_metrics.yaml` and read endpoints. When the HIE live-ranker (silo PR #64) graduates from deterministic stub to live ranking, it should read from this file via the decision-engine endpoints. No separate authoring needed.

**Worktrees at:** `/Users/admin/work-coaching-2026-05-28/{uae,gateway,ui,silo,mkb}/` — remove with `git worktree remove <path>` per repo after PRs merge.

**Findings during build (worth knowing for next session):**
- Gateway PR #72 merged ~25 min before I started — already wired all 11 phase routes. Agent correctly detected via grep and pivoted to add only the 2 coaching routes. Reinforces [[operational_feedback_2026_05_27]] lesson: ALWAYS check current state, don't assume.
- UAE has 3 pre-existing test failures (`test_signoff_pool_field`, `test_signoff_routes`) on `main` unrelated to coaching work. Tracked separately.
- gigaton-ui-system has no `src/` directory + no test runner — uses root-level layout + `npx tsx <test>` convention; agent followed existing pattern.
- intelligence-silo local sandbox lacks `torch` (2 pre-existing failures); CI will have it.
- `signoff_items` table has no `operator_id` column — operator-scoped overdue reminder deferred until either the join via `client_namespaces` is added or `signoff_items` gets an operator scope.

## Related

- [[foundational_goal_maximize_human_superpowers]] — the WHY this directive exists. Operationalizes "real-time coaching loop" at the page-navigation grain.
- [[context_completeness_doctrine_2026_05_26]] — coverage scoreboard powers the "what's missing for next tier" ranker input.
- [[phase_gate_ratification_2026_05_28]] — phase status is the keystone data source for tier-up coaching.
- [[universal_acquisition_framework_2026_05_26]] — same composer pattern, applied to progression-inside-platform instead of acquisition-into-platform.
- [[red_phone_v0_build_state_2026_05_27]] — NotificationBell is the urgent-surface delivery channel; CoachingStrip is the non-urgent companion.
