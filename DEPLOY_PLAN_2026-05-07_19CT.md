---
title: 7pm CT Deploy Plan — 2026-05-07
created: 2026-05-07 16:00 CT (3h runway to 19:00 CT)
audience: operator (Todd)
purpose: maximize what lands in tonight's deploy
---

# CI status across the queue

15 open PRs. Verified CI rollups + mergeable status:

| PR | Title | CI | Mergeable | Tier |
|---|---|---|---|---|
| **SIE #193** | Phase A+B+C (951+ tests) | 968/972 ✅ (4 pre-existing failures) | MERGEABLE | **A — merge first** |
| **#117** | readiness memo | 4/6 ✅ | MERGEABLE | A |
| **#125** | Monday runbook + 5-min demo | 7/7 ✅ | MERGEABLE | A |
| **#126** | simplicity-gate audit (docs) | 5/5 ✅ | MERGEABLE | A |
| #113 | P0 consent gate | 3/3 ✅ | CONFLICTING | B — resolve, then merge |
| #114 | Google-only auth | 3/3 ✅ | CONFLICTING | B |
| #120 | rate-response thumbs + A/B | 3/3 ✅ | CONFLICTING | B |
| #123 | substrate-strip + voice | 4/4 ✅ | CONFLICTING | B |
| #124 | staged-loading | 4/4 ✅ | CONFLICTING | B |
| #118 | preflight + smoke + G0.15 | 3/4 (1 fail) | CONFLICTING | C — fix CI |
| #115 | signup referral | 1/3 (2 fail) | CONFLICTING | C |
| #116 | affiliate (DRAFT, superseded) | 1/3 (2 fail) | **CLOSE** (#119 supersedes) |
| #119 | onboarding orchestrator + new affiliate | (no CI yet) | CONFLICTING | C — wait for CI |
| #121 | error-resolution deep-links | (no CI yet) | CONFLICTING | C |
| #122 | local-save onboarding | (no CI yet) | CONFLICTING | C |

# Tier A — merge before 19:00 CT (high confidence, low risk)

## 1. SIE PR #193 — biggest single value unlock

**One click in GitHub UI:** https://github.com/todd-gig/sovereign-influence-engine/pull/193

- **968/972 tests passing** (99.6%). The 4 failures pre-date this PR (`rebuild_with_evidence` import — same on master since 2026-05-05). I left a comment on the PR explaining.
- After merge → SIE redeploys 11 services with Phase A+B+C (Intent Inference, NIX Engine, Bias Detection, Causal Mapper, Evidence Chain, MCP Bridge, Sales OS Bridge, Gigaton Language Loop, Transcript Pipeline).
- Squash-merge recommended.

## 2. PR #117 — platform-readiness memo

https://github.com/bella-byte/Gigaton-UI-Platform/pull/117

- Pure docs (181-line memo) + 24-line CLAUDE.md update + 15-line `rateResponse` stub.
- Squash-merge.
- Post-merge: Firebase auto-deploys to gigaton-platform.web.app.

## 3. PR #125 — Monday runbook + 5-min demo + smoke screenshots

https://github.com/bella-byte/Gigaton-UI-Platform/pull/125

- Pure docs (3 files, 398 lines) + 19-line addition to `scripts/smoke/route-smoke.mjs`.
- Note: the 19-line script add references functions from PR #118. If #118 hasn't merged, the script add is dead weight — harmless but useless. Still safe to merge.

## 4. PR #126 — simplicity-gate audit (2026-05-02)

https://github.com/bella-byte/Gigaton-UI-Platform/pull/126

- Pure docs (1 file, 145 lines).
- Provides citation rationale for #113 + #114 + #119 + #122. Land it first so reviewers can reference.

# Tier B — quick conflict resolution, then merge (CI green, just needs rebase/conflict)

These are all **CI green** but **CONFLICTING** — usually means main moved while the PR sat. Each is mergeable after a 5-minute conflict resolution in GitHub UI ("Resolve conflicts" button).

| PR | Likely conflict source |
|---|---|
| #113 P0 consent | Probably with #114 — auth/signup flow |
| #114 Google-only auth | Probably with #113 |
| #120 rate-response | ChatPage.tsx vs #123, #124 |
| #123 substrate-strip + voice | ChatPage.tsx vs #120, #124 |
| #124 staged-loading | ChatPage.tsx vs #120, #123 |

**Strategy:** merge #113 first → resolve #114 (1-line conflict). Merge #120 first → resolve #123/#124 in sequence.

If you have 30 minutes, all 5 of these can land tonight too.

# Tier C — needs work, defer past tonight

| PR | Why deferred |
|---|---|
| #115 signup referral | 2/3 CI failures — debug before merge |
| #116 DRAFT — superseded by #119 | **Close** with note pointing at #119 |
| #118 preflight + smoke + G0.15 | 1 CI failure — investigate the failure first |
| #119 onboarding orchestrator | Replaces #116, but no CI yet — wait for green |
| #121 error-resolution | No CI yet; depends on #118; rebase after #118 lands |
| #122 local-save onboarding | No CI yet; depends on #119 |

# Tonight's actual deploy mechanics

`master-knowledge-base/scripts/deploy_19.sh` is now production-ready (was a skeleton this morning). Verified `--check` passes. Deploys per-service:

```
SERVICE                        MECHANISM             PATH
decision-engine                cloudbuild            ~/Documents/GitHub/decision-engine
gigaton-engine                 cloudbuild            ~/Documents/GitHub/gigaton-engine
sales-operating-system         cloudbuild            ~/Documents/GitHub/sales-operating-system
intelligence-silo              cloudbuild            ~/Documents/GitHub/intelligence-silo
sovereign-influence-engine     sie_daily             ~/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine
Carmen-Beach-Properties        gh_workflow           ~/Documents/GitHub/Carmen-Beach-Properties
Gigaton-UI-Platform            firebase_auto_verify  ~/Documents/GitHub/Gigaton-UI-Platform
```

Mechanisms:
- **cloudbuild** — `gcloud builds submit --config=cloudbuild.yaml --project=carmen-beach-properties`
- **sie_daily** — runs SIE's existing `daily_deploy.sh` (build + push 11 images, run migrations, redeploy services, health-check)
- **gh_workflow** — `gh workflow run deploy-prod.yml` (triggers Carmen Beach's GH Actions deploy)
- **firebase_auto_verify** — verifies last `firebase-hosting-merge.yml` run on main was green (Gigaton-UI-Platform auto-deploys on PR merge — no separate command needed)

# Tonight's runbook

```bash
# 16:30 CT — review and merge Tier A in GitHub UI:
#   open and merge: SIE #193, then PRs #117, #125, #126 (in any order)
#   each merge to bella-byte/main auto-fires firebase-hosting-merge.yml
#
# 17:00 CT — (optional) resolve conflicts on Tier B:
#   #113 first → #114 → #120 → #123 → #124
#
# 18:50 CT — verify gcloud auth fresh:
gcloud auth print-identity-token >/dev/null && echo OK

# 19:00 CT — fire the deploy:
cd /Users/admin/Documents/GitHub/master-knowledge-base
./scripts/deploy_19.sh --check        # preflight only
./scripts/deploy_19.sh                # actually deploy

# Expected: <15 min wall-clock, all green
# Logs: master-knowledge-base/deploy-log.jsonl
```

# Optional: install the prompt-based launchd plist (one-time setup)

The 19:00 CT prompt fires automatically if you load the plist:

```bash
# unload the broken old SIE plist
launchctl unload ~/Library/LaunchAgents/ai.gigaton.sie-deploy.plist 2>/dev/null

# install the new prompt-based one (asks you before deploying)
cp /Users/admin/Documents/GitHub/master-knowledge-base/scripts/launchagents/ai.gigaton.daily-deploy-prompt.plist \
   ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/ai.gigaton.daily-deploy-prompt.plist

# verify
launchctl list | grep ai.gigaton.daily-deploy-prompt
```

# What value lands by 19:30 CT if everything goes well

| If merged | What ships to production |
|---|---|
| SIE #193 | 11 SIE backends upgraded with Phase A+B+C (Intent Inference, Bias Detection, Causal Mapper, Evidence Chain, MCP Bridge, NIX Engine, Sales OS Bridge — full L3/L4 the operational state doc was missing) |
| #117 | platform-readiness memo + rate-response stub on gigaton-platform.web.app |
| #125 | Monday beta runbook + 5-min demo script live |
| #126 | simplicity-gate audit doc live |
| (Tier B if you do them) #113 | GDPR/CCPA-compliant signup |
| #114 | Email/password signup removed; Google-only |
| #120 | Thumbs feedback on chat + Learning Dashboard A/B panel |
| #123 | IntelQueue substrate fallback + voice dictation in chat |
| #124 | Staged-loading indicator + chat-timeout self-resolve |

**SIE goes from "deployed but missing L3/L4 logic" → "fully wired"** — that's the operational-state-doc gap closing.

# What I am NOT doing in this turn

- Not auto-merging any PRs (your call; needs review).
- Not closing #116 (your call, even though #119 supersedes).
- Not rebasing #114, #122, #121, #125, #124 onto their dependencies (would loop until merge order is decided).
- Not committing master-knowledge-base governance work — these `.md` files are uncommitted on the local main branch. They CAN be committed as a separate PR after tonight's deploy if useful; they're not blocking the deploy.
- Not running deploy_19.sh now (will do at 19:00 CT per the locked decision; preflight passed at 16:00).

# Risks for tonight

1. **SIE has 4 pre-existing CI failures.** They're not new and don't affect runtime, but if your branch protection requires green CI to merge, you'll have to override. The comment on PR #193 documents why.
2. **5 PRs touch ChatPage.tsx** (#120, #123, #124 + the merged #91, #88). Conflict-resolution sequence matters — merging out of order produces avoidable rebases.
3. **#118 has a CI failure** that's NOT investigated yet. Before merging it, look at the failure log.
4. **Carmen Beach hasn't been touched today.** It has its own deploy pipeline; if no PR is merged tonight, deploy_19.sh's `gh workflow run deploy-prod.yml` will redeploy the existing main HEAD (no-op-ish).
