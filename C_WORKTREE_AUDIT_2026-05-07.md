---
title: C — Gigaton-UI-Platform worktree audit (26 worktrees)
created: 2026-05-07
context: PROGRESS_2026-05-07.md "Step C" — bulk-classify and triage
remote: origin = bella-byte/Gigaton-UI-Platform (NOT todd-gig)
---

# Headline

26 worktrees. **All clean (no uncommitted work).** **25 of 26 branches are local-only (unpushed).** Only `feat/g0.7-platform-master-extraction` has been pushed.

This is the bottleneck for shipping new platform features. The user works in feature worktrees, the code is solid (clean working trees), but **nothing is getting pushed → no PRs → no CI → no deploy.**

# Per-worktree triage

Sorted by "commits ahead of `origin/main`" — heaviest queue at top.

| Branch | Commits ahead | Recommendation |
|---|---|---|
| `chore/frontend-route-smoke-runner` | 11 | **Push + PR** — looks like a multi-step preflight runner |
| `fix/google-only-auth` | 7 | **Push + PR** — auth lockdown, likely revenue-relevant |
| `docs/simplicity-gate-audit-2026-05-02` | 6 | **Push + PR** — docs, low-risk |
| `feat/intel-suggester-sidebar` | 5 | **Push + PR** — intelligence sidebar UI; user-facing value |
| `fix/error-resolution-deep-links` | 5 | **Push + PR** — error UX |
| `fix/p0-signup-consent-gate` | 5 | **Push + PR** — P0 = signup compliance, ship ASAP |
| `feat/intel-decision-engine-wire-fe` | 4 | **Push + PR** — frontend wire to decision-engine; central to integration |
| `chore/platform-readiness-monday-beta` | 3 | **Push + PR** — readiness for "Monday beta" deadline |
| `feat/onboarding-submit-orchestrator` | 3 | **Push + PR** — onboarding orchestrator |
| `fix/onboarding-forms-save-locally` | 3 | **Push + PR** — local-save onboarding |
| `chore/smoke-screenshots-runbook` | 2 | **Push + PR** — runbook, low-priority |
| `feat/learning-dashboard-rerank-ab` | 2 | **Push + PR** — learning dashboard A/B |
| `feat/signup-referral-attribution` | 2 | **Push + PR** — affiliate attribution; ties to revenue |
| `feat-substrate-strip-fallback` | 2 | **Push + PR** — substrate-health UI fallback |
| `fix/admin-dashboard-subnav` | 2 | **Push + PR** — admin nav fix |
| `chore/versioned-pre-push-hook` | 1 | **Push + PR** — pre-push hook |
| `ci/deploy-firestore-functions` | 1 | **Push + PR** — Firestore deploy CI |
| `ci/prune-ephemeral-branches` | 1 | **Push + PR** — branch janitor |
| `feat-chat-staged-loading` | 1 | **Push + PR** — chat staged-loading |
| `feat/affiliate-page` | 1 | **Push + PR** — affiliate page |
| `feat/me-intelligence-user-surface` | 1 | **Push + PR** — `/me/intelligence` page |
| `feat/onboarding-goal-persists` | 1 | **Push + PR** — goal persistence |
| `fix/admin-isadmin-context` | 1 | **Push + PR** — auth context isAdmin fix |
| `fix/contacts-tenant-subscription` | 1 | **Push + PR** — contacts dedup |
| `fix/non-approver-pending-poll` | 1 | **Push + PR** — chat polling fix |
| `feat/g0.7-platform-master-extraction` | (already pushed) | **Open PR** — already on origin |

# Why so much is unpushed

Likely explanation: the firebase-hosting-merge CI is broken (missing `FIREBASE_SERVICE_ACCOUNT` secret). Pushing branches that fail CI creates noise. Operator has been queuing local commits while waiting for the CI fix. **Once `FIREBASE_SERVICE_ACCOUNT` is set up (B.3 in the domain checklist), unblocking this queue is mechanical.**

# Bulk-push recommendation

Do not push all 25 branches at once — that would create 25 simultaneous PRs and overwhelm review. Instead:

## Phase 1 — push the revenue-relevant + P0 branches (7 PRs)

Run in this order, opening each PR before pushing the next:

```
fix/p0-signup-consent-gate                # P0 compliance
fix/google-only-auth                      # auth lockdown
feat/signup-referral-attribution          # affiliate revenue tracking
feat/affiliate-page                       # affiliate UI
feat/intel-decision-engine-wire-fe        # SIE integration in frontend
feat/intel-suggester-sidebar              # intelligence UX
feat/me-intelligence-user-surface         # user-facing /me page
```

## Phase 2 — push the ops + readiness branches (5 PRs)

```
chore/platform-readiness-monday-beta
chore/frontend-route-smoke-runner
chore/smoke-screenshots-runbook
ci/deploy-firestore-functions
ci/prune-ephemeral-branches
```

## Phase 3 — push the polish + small fixes (12 PRs)

The remaining 12 small fixes can go in a single push session.

# Process improvement (separate concern)

Local branches accumulating without pushing is a smell. Two fixes:
1. Add a daily auto-push for clean feature branches (a chore similar to `wip/sweep-*`).
2. Fix the CI so pushing produces useful signal (B.3 above).

# What I am NOT doing in this turn

- Not auto-pushing 25 branches. That's a lot of CI noise + review burden; needs human sequencing.
- Not opening 25 PRs. Same reason.
- Not deleting any worktrees. They contain real work.

# Action requested from operator

1. Pick 3-7 branches from Phase 1 to push first.
2. (Or) Authorize me to push the Phase 1 list autonomously and open PRs with auto-generated bodies.

If authorized, the push + PR loop is a single shell command per branch (~30 seconds each).
