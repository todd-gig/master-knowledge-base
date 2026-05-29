# Coaching Content Library — Per-Page Coaching Mappings

**Status:** ACTIVE — seed authored 2026-05-28 alongside [navigation-aware coaching runbook](../../runbooks/navigation_aware_intelligence_coaching_2026_05_28.md).
**Canonical source:** this directory.
**Build-time mirror:** `gigaton-ui-system/coaching-registry/page-mappings/` (kept in lockstep via CI sync, identical to the `onboarding_v1.yaml` fork pattern documented in `CLAUDE.md`).

---

## 1. Purpose

The UI registry reads one YAML file per page-id to know what coaching to surface when an operator lands on that page. The mappings power:

- `<CoachingStrip />` body copy (the "smallest next action" string)
- `<SidebarHint />` placement near named controls
- `<EmptyStateWithCoaching />` next-unlock messaging
- The `applicable_insight_types` filter the HIE live-ranker (Phase C) applies against the daily insight pool

The mapping is the **content contract** between page authors and the coaching engine. The engine never invents capability-unlock copy; it only ranks among the inputs declared here.

---

## 2. Naming convention

One file per page-id, slashes replaced by dashes:

| Page-id | Filename |
|---------|----------|
| `/intelligence` | `intelligence.yaml` |
| `/connections` | `connections.yaml` |
| `/decisions` | `decisions.yaml` |
| `/onboarding` | `onboarding.yaml` |
| `/dashboard` | `dashboard.yaml` |
| `/founder` | `founder.yaml` |
| `/owner` | `owner.yaml` |
| `/admin` | `admin.yaml` |
| `/memory` | `memory.yaml` |
| `/settings/notifications` | `settings-notifications.yaml` |

For parameterized routes, use the route template with parameters as `:param`. Example: `/decisions/:id` → `decisions-id.yaml`. The hook strips dynamic params before looking up the mapping.

---

## 3. Schema (annotated YAML example)

```yaml
page_id: /connections                            # MUST match the route the UI mounts on
value_now:
  description: |                                 # one sentence the page can render as a
    Manage your data sources. Each connection   # CoachingStrip body when no unlock is more
    feeds the operator-scoped intelligence       # urgent than describing the page's value-now
    index.
  requires: ["operator_token"]                   # preconditions the page already needs
next_unlock_inputs:                              # ordered by author priority; ranker picks
                                                 # the highest unmet at request time
  - input_kind: connector                        # taxonomy — see §3.1
    name: gmail                                  # canonical identifier the platform knows
    target_capability: customer-dm-coaching      # capability slug that unlocks once landed
    smallest_action: "Connect Gmail to enable customer-DM coaching"
    est_value_delta: 3                           # 1-5 ordinal, used as ranker tiebreaker
  - input_kind: connector
    name: clickup
    target_capability: project-progress-intelligence
    smallest_action: "Connect ClickUp to surface project-progress insights"
    est_value_delta: 2
applicable_insight_types:                        # ranker filters the daily insight pool to
  - connector_recommendation                     # these types when ranking insights for this
  - coverage_gap                                  # page
  - revenue_opportunity_match
```

### 3.1 `input_kind` taxonomy

| `input_kind` | Meaning | Example `name` |
|--------------|---------|----------------|
| `connector` | 3rd-party connector | `gmail`, `clickup`, `stripe`, `twilio` |
| `source` | Knowledge/documentation source | `drive_folder`, `notion_workspace`, `url_set` |
| `channel` | Delivery channel | `sms`, `email`, `fcm`, `in_platform` |
| `input` | Operator-declared input | `north_star`, `icp_segment`, `bft_snapshot` |
| `signoff` | Awaiting sign-off on the sign-off matrix | `tier_5_live_signoff`, `auto_execute_class_signoff` |
| `configuration` | Settings toggle | `shadow_mode`, `notification_strict` |

### 3.2 `applicable_insight_types` canonical slugs

The slugs below are the Phase-A launch set. As the daily insight engine adds new types, add them here. A type listed in a page mapping but not present in the engine MUST fail the lint script.

- `connector_recommendation`
- `coverage_gap`
- `revenue_opportunity_match`
- `decision_pattern_alert`
- `phase_gate_progress`
- `signoff_pending`
- `override_pattern_bias`
- `cost_drift`
- `cohort_benchmarking`
- `memory_query_recommendation`
- `notification_preference_tuning`

---

## 4. Ownership

- **Whoever ships a new page authors its mapping.** The mapping lands in the **same PR** as the page, so a page cannot ship without coaching content.
- The master-knowledge-base copy is canonical; the `gigaton-ui-system/coaching-registry/` copy is a build-time mirror. Edits MUST land in master-knowledge-base first; the UI-side mirror PR is mechanical.
- Schema changes (new `input_kind`, new `applicable_insight_types` slug) require a PR to this README + a sibling PR to the HIE live-ranker / lint script. Coordinate via the directive memory `directive-navigation-aware-intelligence-coaching-2026-05-28`.

---

## 5. How to test (proposed, future)

A `coaching-registry/_test/` lint script (sibling repo, owner TBD) validates:

1. Every `page_id` matches an actual UI route (cross-checks against `gigaton-ui-system/src/routes.ts`).
2. Every `target_capability` resolves in the capabilities catalog OR is on the future-capability registry with a tracking issue.
3. Every `applicable_insight_types` slug exists in the daily insights engine.
4. Every `input_kind` / `name` pair resolves in the connector catalog (for `connector`) or the equivalent registry for other kinds.
5. YAML parses cleanly under `yaml.safe_load`.

Until the lint script exists, authors should manually run:

```bash
python3 -c "import sys, yaml; yaml.safe_load(open(sys.argv[1]))" path/to/your-page.yaml
```

before opening the PR.

---

## 6. Cross-refs

- Runbook: `runbooks/navigation_aware_intelligence_coaching_2026_05_28.md`
- Directive memory: `directive-navigation-aware-intelligence-coaching-2026-05-28`
- Existing manifest fork pattern: `CLAUDE.md` §"Manifest fork — onboarding_v1.yaml"
- Existing onboarding manifest: `manifests/onboarding_v1.yaml`
