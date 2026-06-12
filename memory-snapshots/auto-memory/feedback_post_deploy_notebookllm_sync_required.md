---
name: feedback-post-deploy-notebookllm-sync-required
description: "After ANY deployment (Cloud Run / SIE / FE / Workers / Functions / etc.), always call ~/.gigaton-notebookllm/scripts/post-deploy-sync.sh <service> <rev>. Refreshes the NotebookLM Drive bundle and appends a row to the pending-clicks log so the user is reminded to manually re-sync NotebookLM sources."
metadata: 
  node_type: memory
  established: 2026-05-22
  serves: foundational_goal_gigaton_engineered_brand_experience (PPIM)
  type: feedback
  originSessionId: b1b33f2c-fb8c-4ff5-b646-546854e5ec46
promoted_from: feedback_post_deploy_notebookllm_sync_required.md
promoted_at: 2026-06-02T20:13:25Z
---

# Rule

Every deploy operation MUST end with:

```bash
bash "${HOME}/.gigaton-notebookllm/scripts/post-deploy-sync.sh" <service-name> <revision-or-tag>
```

Applies to:

- Local launchd deploy plists (e.g. `ai.gigaton.sie-deploy`)
- Manual `gcloud run deploy` invocations done in chat
- GitHub Actions deploy workflows (add as a `post-deploy` step or webhook to a local runner)
- Cloud Build steps that finish a deploy
- Any `kubectl rollout` / `wrangler deploy` / `firebase deploy` Claude runs

**Why:** NotebookLM has no auto re-ingestion. Without this hook, the canonical Gigaton notebook drifts from production within hours of any deploy. The wrapper does two things: (1) re-runs the memory→Drive sync (in case the 30-min launchd job hasn't fired yet), (2) appends a checklist row to `~/.gigaton-notebookllm/pending-notebookllm-clicks.md` that the user clears by manually clicking "sync with source" in https://notebooklm.google.com/. Reason this matters: the master plan reconciliation 2026-05-20 explicitly named NotebookLM as the audit/3rd-party-coherence surface — drifted sources degrade the auditability the folder was built for.

**How to apply:**

1. When Claude RUNS a deploy in chat, fire the wrapper itself afterward.
2. When Claude EDITS a deploy script, append the wrapper call before the success exit (see `daily_deploy.sh` for canonical pattern — the call is wrapped in `|| log "WARN: ..."` so it's non-blocking).
3. When Claude WRITES a new deploy workflow (.yml / .sh / .plist), include the wrapper call in the initial scaffold.
4. After firing, surface the pending-clicks reminder to the user in the response (e.g. "deploy done; pending NotebookLM click-sync logged to `~/.gigaton-notebookllm/pending-notebookllm-clicks.md`").

**Pattern (bash):**

```bash
SVC_REV="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
bash "${HOME}/.gigaton-notebookllm/scripts/post-deploy-sync.sh" "<service>" "${SVC_REV}" || \
    echo "WARN: post-deploy NotebookLM sync failed (non-blocking)"
```

**Pattern (GHA, runs on self-hosted runner that has FDA):**

```yaml
- name: NotebookLM post-deploy sync
  if: always() && steps.deploy.outcome == 'success'
  run: bash ~/.gigaton-notebookllm/scripts/post-deploy-sync.sh ${{ github.event.repository.name }} ${{ github.sha }}
```

# Pre-requisite

User must grant Full Disk Access to `/bin/bash` (one-time, in System Settings → Privacy & Security → Full Disk Access) for the 30-min recurring launchd job AND for any deploy plist that calls the wrapper. Manual terminal runs already have FDA via Terminal.app.

# Cross-references

- [[gigaton_notebookllm_canonical_folder]] — the folder this hook keeps in sync
- [[feedback_post_deploy_self_verification]] — sibling rule for memory/IDE drift checks
- [[feedback_directed_workflow_required_for_every_deploy]] — sibling deploy doctrine
