---
title: Action item for Bella — enable Artifact Registry API on gigaton-platform
date: 2026-05-08
priority: P1 — blocks Firebase auto-deploy of every PR merged to main
estimated effort: 30 seconds
---

# What's needed (one of these two)

**Option A (faster, recommended):** Enable the Artifact Registry API on `gigaton-platform` project.
1. Open https://console.cloud.google.com/apis/library/artifactregistry.googleapis.com?project=gigaton-platform
2. Click "Enable"

**Option B:** Grant `todd@gigaton.ai` admin role on `gigaton-platform` so he can enable it himself.

# Why it matters

The CI workflow `firebase-hosting-merge.yml` deploys to Firebase Hosting + Firestore + Cloud Functions on every push to main. As of today (2026-05-08), the workflow has been failing on:

```
Error: Permissions denied enabling artifactregistry.googleapis.com.
```

This is the second leg of the same issue we resolved this afternoon (the `firebaserules.admin` IAM grant). The CI runs from `github-action-1192684337@gigaton-platform.iam.gserviceaccount.com`, which now has Firestore Rules permissions but lacks permission to *enable* a Google Cloud API on `gigaton-platform`.

The cleanest fix is to enable the API once (the SA already has `serviceUsageConsumer` to use enabled APIs, just not to enable new ones).

# What this unblocks once done

7 PRs from today auto-deploy on next merge to bella-byte/main:

- #117 (closed — superseded; ignore)
- **#118** preflight + smoke + G0.15 GIM model-release (mostly already on main; redundant)
- **#121** `<ErrorMessage>` deep-links wired into 8 pages (real new work)
- **#125** Monday runbook + 5-min demo + corpus snapshot (mostly already on main)
- **#126** simplicity audit doc (mostly already on main)
- **#127** Chat maintenance-mode banner (real new — set `VITE_INTELLIGENCE_MODE=stub` build env to surface)
- **#128** `/affiliate/onboarding` page (real new — pairs with sovereign-influence-engine PR #194)

Without the API enabled, every merge succeeds in code but fails in CI's Firestore-Functions deploy step. Hosting still updates (that's a different step that already passes).

# After you enable

- A re-trigger of run 25549479539 should turn green: `gh run rerun 25549479539 --repo bella-byte/Gigaton-UI-Platform`
- Tomorrow's deploys land cleanly with no further intervention.

# Background

Same artifact-registry permission gap exists across multiple Firebase projects in our setup. Long-term fix: bake "enable required APIs" into the project-bootstrap script (`platform-master`'s emit-client.sh) so new clients don't hit this. Tracked as a follow-up — not blocking.
