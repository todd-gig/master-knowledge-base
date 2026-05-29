---
title: Navigation-Aware Intelligence Coaching — Implementation Runbook
status: SPEC — Phase A in flight 2026-05-28 (UAE + UI components + content seed)
authored: 2026-05-28
directive_memory: directive-navigation-aware-intelligence-coaching-2026-05-28
repos_in_scope:
  - user-access-engine
  - gigaton-gateway
  - intelligence-silo
  - gigaton-ui-system
  - master-knowledge-base
serves:
  - foundational_goal_maximize_human_superpowers
  - context_completeness_doctrine_2026_05_26
  - phase_gate_ratification_2026_05_28
cross_refs:
  - 2026_05_25_intelligence_qa_on_ingested_files.md
  - 2026_05_26_universal_acquisition_framework.md
  - 2026_05_26_to_2026_06_01_deploy_freeze_operating_playbook.md
---

# Navigation-Aware Intelligence Coaching

**One-line.** As operators navigate pages, the Human Intelligence Engine surfaces — on the page itself — (1) what value flows here NOW given current connections/sources, (2) what next source/channel/input unlocks the next capability up the value pyramid (functionality → capability → superhuman), and (3) the smallest next action to get there.

---

## 1. Why — doctrine link

This directive operationalizes [[foundational_goal_maximize_human_superpowers]] at the page-navigation grain. The "maximize human superpowers" goal is satisfied only if every operator-facing surface measurably advances the operator's capability. That requires three preconditions which dashboard-batch coaching does NOT meet:

1. **Live ranking on navigation** — what is relevant HERE NOW, not yesterday's batch.
2. **Capability-ladder awareness** — the next-best unlock that climbs the value pyramid, respecting phase-gate prerequisites ([[phase_gate_ratification_2026_05_28]] §1+§5).
3. **Coverage-completeness gating** — never push toward unlocks the operator can't yet act on ([[context_completeness_doctrine_2026_05_26]] — coverage scoreboard powers the ranker).

### The directive (verbatim, Todd 2026-05-28)

> "ensure that the human intelligence engine intelligence > notifications are provided to user + reminders to enable user to extract value, ex: additional sources, additional channels, etc to unlock extra capabilities > super humans AS the human navigates to pages within the system"

### What's NEW vs existing engines

| Layer | Existing | NEW per this directive |
|-------|----------|------------------------|
| Daily insight generation | Today's Insights panel runs 06:00 CT batch | Insights re-rank when user lands on a page where they're more actionable; `page_context` field added per insight |
| Bias/coaching nudges | Weekly digest | Surface relevant bias nudges inline on the very page where the bias manifests |
| Multi-channel delivery | NotificationBell in-platform / email / SMS / FCM | Add `in_app_contextual` channel: non-modal CoachingStrip that renders on specific pages without firing a push |
| Empty-state + Day 7/10/14/30 | Fires by elapsed days | Capability-ladder-aware empty states: shows which superpower unlocks at the next tier, what input enables it, smallest next action |
| Progressive enrichment cap | 4→9 sources post-Day-10 | Page-context aware: on `/connections`, show "connect Gmail to unlock customer-DM-coaching" rather than just "you have N sources" |
| Capability computation | `/access/{user_id}/capabilities` | Pair with `/v1/capabilities/next-unlocks` — what is the operator one connection / one input / one action away from |
| Phase Gate status | Per `phase_gate_ratification_2026_05_28` §1+§5 ratified | Single source of truth for tier-up coaching ("you are in Phase 3 Connector Integration; 2 more connectors unlock Phase 4 Decision Loop") |

---

## 2. What — the runtime model

The grain is page navigation. Each page mount fires a single coaching request; the response composes onto the page through a small set of UI primitives.

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
   │  - Coverage Completeness scoreboard
   │  - Connected-sources inventory + per-source utilization
   │  - Last 30d operator decision/override patterns
   │  - Gigaton promotion priority (per-quarter superpower bias yaml)
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

---

## 3. Where — file map

| Repo | Path | Purpose | Phase |
|------|------|---------|-------|
| `user-access-engine` | `api/services/coaching.py` | Deterministic ranker (Phase A) → calls into silo HIE (Phase C) | A → C |
| `user-access-engine` | `api/routers/coaching.py` | `POST /v1/coaching/page-context` + `GET /v1/capabilities/next-unlocks` | A |
| `gigaton-gateway` | route table | Proxies UAE coaching routes; passes existing `/v1/phase/*` through | A |
| `intelligence-silo` | `core/coaching/` | HIE live-ranker scaffold (full HIE wiring lands Phase C) | A scaffold → C live |
| `gigaton-ui-system` | `src/components/coaching/CoachingStrip.tsx` | Non-modal banner above page content | A |
| `gigaton-ui-system` | `src/components/coaching/CapabilityLadder.tsx` | Visual progression up the value pyramid | A |
| `gigaton-ui-system` | `src/components/coaching/SidebarHint.tsx` | Small persistent hint near the relevant control | A |
| `gigaton-ui-system` | `src/components/coaching/EmptyStateWithCoaching.tsx` | Capability-ladder-aware empty state | A |
| `gigaton-ui-system` | `src/hooks/usePageCoaching.ts` | Calls `/v1/coaching/page-context` on mount; returns ranked surface items | A |
| `gigaton-ui-system` | `coaching-registry/page-mappings/<page>.yaml` | Per-page coaching content the UI registry consumes | A seed → ongoing |
| `master-knowledge-base` | `runbooks/navigation_aware_intelligence_coaching_2026_05_28.md` | This runbook | A |
| `master-knowledge-base` | `manifests/coaching-content-library/` | Canonical per-page coaching content library (seeds the UI registry) | A |
| `decision-engine` | `config/gigaton_promotion_priorities.yaml` (proposed) | Quarterly per-superpower promotion bias the ranker consults | open question |

---

## 4. How — endpoint contracts

Both endpoints live in `user-access-engine` and are proxied by `gigaton-gateway`. Both honor operator-scoped bearer tokens and the parent-read-only pattern from [[phase_gate_ratification_2026_05_28]] §5 (`?operator_id=` query param permitted for parent operators whose token has `permitted_operator_ids` covering the child).

```
POST /v1/coaching/page-context
Auth: operator bearer; honors ?operator_id= for parent read-only (per Phase Gate ratification §5)
Body: { "page_id": "/connections", "route_params": {"id":"..."} }
Response:
{
  "page_id": "...",
  "operator_id": "...",
  "applicable_insights": [
    {"id":"...","headline":"...","body":"...","severity":"info|low|medium|high","action_url":"..."}
  ],
  "capability_ladder_step": {
    "unlock_name":"...","current_blocker":"...","smallest_action":"...",
    "target_capability":"...","est_value_delta":1
  },
  "bias_nudge": null,
  "reminders": [{"id","headline","action_url","dismissed_until"}]
}

GET /v1/capabilities/next-unlocks?limit=N
Auth: operator bearer
Response:
{
  "operator_id":"...",
  "next_unlocks":[
    {"unlock_name","current_blocker","smallest_action","target_capability",
     "est_value_delta","prerequisites_met"}
  ]
}
```

### Phase A (deterministic) vs Phase C (HIE live) behavior

- **Phase A** — `UAE coaching.py` reads the YAML page-mapping for `page_id`, intersects against the operator's connector inventory + Phase Gate state, and returns the highest-value unmet unlock as `capability_ladder_step`. `applicable_insights` is a static lookup against the page mapping's `applicable_insight_types`. `bias_nudge` is always `null`.
- **Phase C** — same response shape, but `applicable_insights` is re-ranked per-request by the intelligence-silo HIE live-ranker, `bias_nudge` may be populated, and `capability_ladder_step` is selected from a multi-armed bandit instead of static priority. Response shape is identical, so the UI does not change at the C cutover.

### Caching & cost

- HIE results cached per `(operator_id, page_id)` for **5 minutes** (proposed; see open questions §10).
- A dismissal sets `dismissed_until = now + 7d` (proposed cadence; see §10).

---

## 5. How — UI integration

A page author wires coaching with one hook and zero-to-three components depending on the page's needs.

### 5.1 Minimum integration (every page)

```typescript
// In any page component:
import { usePageCoaching } from '@/hooks/usePageCoaching';
import { CoachingStrip } from '@/components/coaching/CoachingStrip';

export function ConnectionsPage() {
  const { strip, ladderStep, insights, reminders, dismiss } = usePageCoaching('/connections');
  return (
    <>
      {strip && <CoachingStrip {...strip} onDismiss={() => dismiss(strip.id)} />}
      {/* ...page body... */}
    </>
  );
}
```

The hook returns `null`/empty arrays until the endpoint resolves; the strip renders only when non-null. The hook is also responsible for honoring `dismissed_until` from localStorage (key pattern: `coaching:dismiss:<insight_id>`).

### 5.2 Page-author-controlled components

| Component | When to mount | Where on page |
|-----------|---------------|---------------|
| `<CoachingStrip />` | Always (renders if hook returns one) | Above page header content |
| `<CapabilityLadder />` | Pages that explain progression (dashboard, /onboarding, /founder) | In a dedicated panel or sidebar |
| `<SidebarHint />` | Pages with discrete affordances (e.g., near "Add connection" button) | Adjacent to the named control |
| `<EmptyStateWithCoaching />` | Replace generic empty state when a page has no data yet | Page body when data is empty |

### 5.3 Dismissable behavior

- Dismiss writes `coaching:dismiss:<insight_id>=<iso_timestamp>` to localStorage.
- The hook excludes any insight whose key exists and whose value is in the future.
- Default `dismissed_until` from the server is 7 days (`reminders[].dismissed_until`). The client overrides with its own localStorage timestamp if the user manually dismisses.
- A "don't show me this again" choice writes `coaching:dismiss:<insight_id>=permanent`.
- Unmuting all is a single localStorage clear of keys matching `coaching:dismiss:*` (offered via Settings → Notifications).

---

## 6. How — content authoring

The `coaching-registry/page-mappings/<page>.yaml` convention is the per-page content library. The UI registry consumes these; the canonical source lives in `master-knowledge-base/manifests/coaching-content-library/page-mappings/` and is forked into `gigaton-ui-system/coaching-registry/` at build time (same pattern as `manifests/onboarding_v1.yaml`).

**Naming.** One file per page-id, slashes replaced by dashes. Example: `/connections` → `connections.yaml`, `/settings/notifications` → `settings-notifications.yaml`.

**Annotated example** (`connections.yaml`):

```yaml
page_id: /connections
value_now:
  description: "Manage your data sources. Each connection feeds the operator-scoped intelligence index."
  requires: ["operator_token"]      # what the page already needs to render its value-now
next_unlock_inputs:                 # ordered by priority; ranker picks highest unmet
  - input_kind: connector           # connector | source | channel | input | signoff | configuration
    name: gmail
    target_capability: customer-dm-coaching
    smallest_action: "Connect Gmail to enable customer-DM coaching"
    est_value_delta: 3              # 1-5 scale; relative within this page
  - input_kind: connector
    name: clickup
    target_capability: project-progress-intelligence
    smallest_action: "Connect ClickUp to surface project-progress insights"
    est_value_delta: 2
applicable_insight_types:           # the ranker filters daily-pool insights to these types
  - connector_recommendation
  - coverage_gap
  - revenue_opportunity_match
```

**Field reference.**

- `page_id` — must match the route the UI mounts on.
- `value_now.description` — one sentence the page can render as a CoachingStrip body when no unlock is more urgent.
- `value_now.requires` — preconditions (capabilities, scopes, tier) the page already needs.
- `next_unlock_inputs[].input_kind` — taxonomy for the ranker:
  - `connector` — a 3rd-party connector (Gmail, ClickUp, Stripe, etc.)
  - `source` — a knowledge / documentation source (Drive folder, URL, file upload)
  - `channel` — a delivery channel (SMS, email, FCM)
  - `input` — an operator-declared input (north star, ICP segment, BFT)
  - `signoff` — an awaiting sign-off on the sign-off matrix
  - `configuration` — a settings toggle (e.g., enable shadow mode)
- `next_unlock_inputs[].name` — canonical identifier the platform already knows about.
- `next_unlock_inputs[].target_capability` — the capability slug that unlocks once the input lands. Must exist in the capabilities catalog OR be a documented future capability with a tracking issue.
- `next_unlock_inputs[].est_value_delta` — 1-5 ordinal; used as a tiebreaker when multiple unlocks are unmet.
- `applicable_insight_types` — the ranker's filter against the daily-generation insight pool. Use canonical insight-type slugs from the daily insights engine.

**Ownership.** Whoever ships a new page authors its mapping. Mapping lands in the SAME PR as the page (so the page can't ship without coaching content). The master-knowledge-base mapping is canonical; the UI-side fork is build-time mirror, identical to the `onboarding_v1.yaml` fork pattern documented in `CLAUDE.md` §"Manifest fork — onboarding_v1.yaml".

**Testing (proposed, future).** A `coaching-registry/_test/` lint script validates: (1) all `page_id` values match an actual route; (2) every `target_capability` resolves in the capabilities catalog or is on the future-capability registry; (3) every `applicable_insight_types` slug exists in the daily insights engine; (4) every `input_kind`/`name` pair resolves in the connector catalog (for `connector`) or the equivalent registry for other kinds.

---

## 7. Rollout phases

### Phase A — Deterministic substrate (NOW, in flight 2026-05-28)

- **UAE:** `api/services/coaching.py` + `api/routers/coaching.py` returning deterministic responses from the YAML mappings + Phase Gate state.
- **Gateway:** route table additions for the two new endpoints; existing `/v1/phase/*` already proxied.
- **Silo:** `core/coaching/` scaffold (stub HIE entry point, returns same deterministic response so the silo→UAE contract is fixed early).
- **UI:** the four components + the `usePageCoaching` hook, behind a feature flag for the cohort.
- **mkb (this PR):** this runbook + the seed content library for the 10 launch pages.

### Phase B — UI mounting (week of 2026-06-01)

- Wire `<CoachingStrip />` into every page layout via the root `IntelligenceLayout` (mirroring where `<NotificationBell />` mounts).
- Mount `<EmptyStateWithCoaching />` in the pages whose current empty state is generic.
- Mount `<SidebarHint />` on the connector hub near "Add connection" and on /decisions near "Approve" / "Override".
- Mount `<CapabilityLadder />` on `/dashboard`, `/onboarding`, `/founder`.

### Phase C — HIE live-ranker wired (week of 2026-06-08)

- Factor the daily Insights engine logic into `intelligence-silo/core/coaching/live_ranker.py` so it runs per-request with `page_context` filtering.
- Wire UAE's `coaching.py` to call the silo's `POST /v1/intelligence/coaching/rank` instead of returning deterministic responses.
- Cache hot per-operator results for 5min to bound load.
- Response shape unchanged — UI does not redeploy.

### Phase D — Bias-coaching integration (after, W11–W12 per separate spec)

- Populate `bias_nudge` in the page-context response from the operator-coaching engine (D3 override patterns, override-then-regret signatures, etc.).
- Surface inline on the very page where the bias manifests (e.g., D3 override pattern → /decisions).
- W11–W12 sequencing matches the separate bias-coaching spec; no UI change required.

---

## 8. Anti-patterns (this directive's job to prevent)

1. **Page-blank with no guidance.** Every operator-facing page MUST surface either real data OR a contextual coaching item. Blank ≠ acceptable. (Reinforces empty-state doctrine but extends it to ALL pages, not just first-time.)
2. **Generic "do something" CTAs.** Coaching must name the specific next source/channel/input AND the specific capability it unlocks. "Connect more sources" is forbidden; "Connect Gmail to unlock customer-DM coaching" is required.
3. **Dashboard-only intelligence.** If an insight is relevant to a specific page, it surfaces THERE — not only on the dashboard. Operator should not have to navigate away to see what's relevant where they are.
4. **Daily-batch staleness.** Page-context coaching is live (ranked on navigation), not yesterday's pre-computed list filtered.
5. **No reminder loop.** A capability-unlock recommendation that's been dismissed-deferred must re-surface on a sensible cadence (operator can mute permanently; "remind me later" defaults to 7 days).
6. **Pushing toward unlocks the operator can't yet act on.** The ranker must respect phase-gate prerequisites (don't surface "enable auto-execute" coaching while operator is still in Phase 3 connector integration; surface the Phase 3 → 4 unlock instead).

---

## 9. Verification

### 9.1 Endpoint checks

```bash
# Phase A deterministic — connections page
curl -X POST "$UAE/v1/coaching/page-context" \
  -H "Authorization: Bearer $OP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"page_id":"/connections","route_params":{}}'
# expect: capability_ladder_step.unlock_name in {gmail, clickup, ...}
# expect: applicable_insights[] non-empty if any open insight matches connector_recommendation/coverage_gap/revenue_opportunity_match

curl "$UAE/v1/capabilities/next-unlocks?limit=5" -H "Authorization: Bearer $OP_TOKEN"
# expect: next_unlocks[] non-empty for any operator past stage-0
# expect: prerequisites_met=true for the top item
```

### 9.2 Parent-read-only check

```bash
# Parent operator hitting child's page-context (per Phase Gate §5)
curl -X POST "$UAE/v1/coaching/page-context?operator_id=child_op_id" \
  -H "Authorization: Bearer $PARENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"page_id":"/dashboard","route_params":{}}'
# expect: 200 with child's coaching state
# expect: same call with a parent token whose permitted_operator_ids does NOT cover child_op_id → 403
```

### 9.3 UI render + dismiss

1. Load `/connections` in a fresh session.
2. Confirm `<CoachingStrip />` renders above page content with text matching the YAML's `smallest_action` for the highest-priority unmet `next_unlock_inputs` entry.
3. Click dismiss.
4. Confirm strip disappears.
5. Open DevTools → Application → Local Storage → check key `coaching:dismiss:<insight_id>` exists with an ISO timestamp ≥ now + 7d.
6. Reload page → confirm strip does NOT re-render until that timestamp passes.

### 9.4 Anti-pattern guards (Phase A)

- Navigate to any operator-facing page without data; confirm `<EmptyStateWithCoaching />` (NOT a generic blank) renders.
- On `/connections`, confirm the strip names a specific connector (e.g., "Gmail") and a specific capability ("customer-DM coaching"), not generic CTA copy.
- Confirm an operator in Phase 3 does NOT see Phase 4+ unlocks in `next_unlocks` (`prerequisites_met=false` items are filtered out by the ranker).

---

## 10. Open questions

1. **Promotion-priority quarterly YAML location** — *Proposed:* `decision-engine/config/gigaton_promotion_priorities.yaml`. Mirrors the file referenced by `2026_05_26_universal_acquisition_framework.md` §3.6; reusing the same file avoids two competing priority lists. Awaiting decision-engine owner sign-off before Phase C wires it.
2. **HIE caching TTL** — *Proposed:* 5min per `(operator_id, page_id)`. Tight enough to feel live; loose enough to bound cost. Revisit after Phase C live metrics.
3. **Reminder re-surface cadence** — *Proposed:* 7 days default. Operator may set permanent mute. Calendar-aware re-surface (skip weekends, respect quiet hours) is a Phase D enhancement.
4. **Page-mapping lint script** — owner + ship date for `coaching-registry/_test/`. Currently documented as future; non-blocking for Phase A.
5. **`<CapabilityLadder />` visual model** — pyramid vs. linear vs. radial. UI-team decision pre-Phase-B.

---

## 11. Critical files for implementation

- `user-access-engine/api/services/coaching.py` (NEW, Phase A)
- `user-access-engine/api/routers/coaching.py` (NEW, Phase A)
- `gigaton-gateway/app/routes/coaching.py` (NEW proxy, Phase A)
- `intelligence-silo/core/coaching/__init__.py` (scaffold A → live C)
- `intelligence-silo/core/coaching/live_ranker.py` (Phase C)
- `gigaton-ui-system/src/hooks/usePageCoaching.ts` (NEW, Phase A)
- `gigaton-ui-system/src/components/coaching/CoachingStrip.tsx` (NEW, Phase A)
- `gigaton-ui-system/src/components/coaching/CapabilityLadder.tsx` (NEW, Phase A)
- `gigaton-ui-system/src/components/coaching/SidebarHint.tsx` (NEW, Phase A)
- `gigaton-ui-system/src/components/coaching/EmptyStateWithCoaching.tsx` (NEW, Phase A)
- `gigaton-ui-system/coaching-registry/page-mappings/*.yaml` (forked build-time mirror, Phase A)
- `master-knowledge-base/manifests/coaching-content-library/page-mappings/*.yaml` (CANONICAL, this PR)
- `decision-engine/config/gigaton_promotion_priorities.yaml` (proposed; Phase C)

---

## 12. Cross-refs

- [[foundational_goal_maximize_human_superpowers]] — north-star WHY.
- [[context_completeness_doctrine_2026_05_26]] — coverage scoreboard powers the "what's missing for next tier" input.
- [[phase_gate_ratification_2026_05_28]] — phase status is the keystone data source; §5 parent-read-only governs `?operator_id=`.
- [[universal_acquisition_framework_2026_05_26]] — same composer pattern, applied to progression-inside-platform instead of acquisition-into-platform.
- [[red_phone_v0_build_state_2026_05_27]] — `<NotificationBell />` is the urgent-surface delivery channel; CoachingStrip is the non-urgent companion.
- `runbooks/2026_05_25_intelligence_qa_on_ingested_files.md` — Q&A pipeline shares ranking primitives (10 Intelligence Dimensions, ethnographic frames).
