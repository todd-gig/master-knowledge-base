---
name: feedback-directed-workflow-required-for-every-deploy
description: "STANDING DOCTRINE established 2026-05-20. Every UI/UX change + feature + functionality deployment must ship a directed user-facing workflow that surfaces on the operator's next login. Reason: maximum value cannot be generated if the human doesn't implement / understand / utilize the new capability. Enforces human-tech alignment without drift."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-20
  state_set_by: doctrine-codification-after-documentation-ingest-deploy
  lifecycle_state: active
  status: ACTIVE — required for every PR that ships operator-visible behavior
  serves: foundational_goal_gigaton_engineered_brand_experience
  ppim_brand_dimension: adoption + comprehension + value-realization
  originSessionId: 3b512896-7bb2-4c6a-9322-7e52464bb2cd
promoted_from: feedback_directed_workflow_required_for_every_deploy.md
promoted_at: 2026-06-02T20:13:25Z
---

# Directed post-deploy workflow is required for every UI/UX / feature / functionality deploy

## The rule

Every PR that ships **operator-visible behavior** (UI, UX, new feature, new functionality, new endpoint that operators consume) MUST include a corresponding entry in the FE directed-workflow registry. That entry surfaces as a guided banner + step-by-step modal on the operator's next login, walking them through:

1. WHERE the new capability lives (deep-link / route)
2. WHAT to do to activate / configure / use it
3. HOW they'll know it's working (verification check per step)
4. WHY it matters (PPIM rationale in plain language)

The PR is not "done" until the workflow entry exists and the workflow's `actionHref` deep-links resolve to live routes the destination pages handle.

## Why

Maximum value is never generated when:

- A feature exists in code but the operator doesn't know it shipped
- The operator knows it shipped but can't find it
- The operator finds it but doesn't know how to set it up
- The operator sets it up but can't verify it's working
- The operator uses it but doesn't understand WHY it benefits them

Each of these failure modes silently destroys ROI on engineering work. A 10-PR feature with 0% adoption produces 0% value. Adoption is not optional — it is the gating constraint on every other Gigaton outcome.

The directed workflow forces alignment between what we build (tech) and what gets implemented (human). It enforces the foundational goal — **"Facilitate predictably profitable interaction management of a gigaton engineered brand experience"** — by making sure the human side of every interaction loop is closed.

## How to apply

For every PR that introduces operator-visible behavior:

1. **Author the workflow definition** in `gigaton-ui-system/services/directedWorkflows.ts`. Use `DOCUMENTATION_INGEST_WORKFLOW` as the template. Required fields:
   - `id` — stable kebab slug + introduction date (e.g. `documentation-ingest-2026-05-20`)
   - `name`, `description` — operator-friendly
   - `introducedAt` — ISO timestamp of the deploy that ships it
   - `ppimRationale` — one-sentence PPIM mapping per [[foundational_goal_gigaton_engineered_brand_experience]]
   - `featureFlag` — capability key gating surfacing (so operators without the capability don't see it)
   - `steps[]` — each step has `id`, `title`, `description`, `actionLabel`, `actionHref`, `verifyDescription`
   - `successCelebration` — copy shown on 100% completion (confetti is automatic)

2. **Wire `?action=` query params** on each destination page so the workflow's `actionHref` deep-link can trigger the right control (e.g. `/connectors/documentation?action=connect` auto-opens the OAuth flow).

3. **Add auto-completion detection** in the destination page using `markStepComplete(workflowId, stepId)` from `hooks/useDirectedWorkflows.ts`. Watch the observable state (account count, subscription count, bundle status, etc.) and auto-complete when the user actually does the thing.

4. **Include the doctrine reference** in the PR body. Sample bullet: *"Adds directed workflow entry per [[feedback_directed_workflow_required_for_every_deploy]] — surfaces on next login as `<workflow-name>`."*

5. **The banner + modal pick up new workflows automatically** from the registry. No further wiring needed in `App.tsx`.

## What counts as "operator-visible behavior"

Includes:
- Any new page or route
- Any new connector / integration / OAuth flow
- Any new capability the operator can toggle / configure
- Any change to an existing flow that changes the steps the operator takes
- Any new dashboard panel, metric, or report
- Any new initiative / coaching surface

Excludes (no workflow needed):
- Pure backend refactors with no UI surface change
- Database migrations that operators never touch
- Internal observability / telemetry plumbing
- Bug fixes that restore previously-documented behavior

When in doubt: ship the workflow. The cost of an unused workflow entry is zero; the cost of an unadopted feature is the entire value of the engineering work.

## Where the infrastructure lives

- Registry: `gigaton-ui-system/services/directedWorkflows.ts`
- Hook: `gigaton-ui-system/hooks/useDirectedWorkflows.ts`
- Banner: `gigaton-ui-system/components/DirectedWorkflowBanner.tsx`
- Modal: `gigaton-ui-system/components/DirectedWorkflowModal.tsx`
- Route: `/setup/:workflowId` (configured in `App.tsx`)
- Persistence: localStorage (v0; backend persistence via HME Initiative events is next)

First instance: Documentation Ingest 7-step workflow (PR todd-gig/gigaton-ui-system#29, commit `306cf2c`, 2026-05-20).

## How to handle violations

When you review a PR that ships operator-visible behavior but lacks a workflow entry:
1. Block merge with a comment citing this memory
2. Author writes the workflow entry in a follow-up commit before merge
3. If the omission ships anyway, open an immediate follow-up PR to backfill (do not let it sit)

## Cross-references

- [[directed_workflow_registry_pattern]] — implementation pattern + future-feature instructions
- [[feedback_always_build_user_self_serve]] — sister doctrine: every feature must have a self-serve loop. The directed workflow IS that self-serve loop's onboarding surface.
- [[feedback_always_include_gamification]] — sister doctrine: gamification (confetti, badges, streaks). The directed workflow is gamified completion-driven.
- [[empty_state_guidance_onboarding_nudges]] — earlier work on empty-state nudges; directed workflow is the productized successor.
- [[documentation_ingest_feature_spec]] — first feature to land with a directed workflow.
- [[feedback_always_record_why]] — the workflow's `ppimRationale` field operationalizes this rule for end-users.
