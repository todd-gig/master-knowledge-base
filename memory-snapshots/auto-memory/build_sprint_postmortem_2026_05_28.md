---
name: build-sprint-postmortem-2026-05-28
description: "Post-mortem on the 2026-05-28 parallel-build sprint that shipped Phase Gate backend end-to-end in ~6 hours wall-clock (vs 3.5-day estimate). 5 patterns held: (1) worktree isolation; (2) two parallel agents in different repos; (3) auto-mode classifier appropriately gated prod DB writes; (4) start.sh boot-time alembic obviated the cloudbuild migrate PR; (5) Cloud Run Jobs as one-off prod DB op pattern. 3 misses surfaced that produced follow-up PR #51: bootstrap script naming wrong, scripts/ not in Dockerfile, gateway /v1/phases bypass deferred. Templated for future ships."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-28
  status: ACTIVE doctrine — templating pattern for future sprints
  originSessionId: c3d6a014-f8e0-4829-9d0d-6197cc8ac3f6
promoted_from: build_sprint_postmortem_2026_05_28.md
promoted_at: 2026-06-02T20:13:25Z
---

# Build Sprint Post-Mortem — 2026-05-28

> One-session ship of the Phase Gate backend (UAE PR #50 + gateway PR #72 + migration applied + endpoints verified live). Estimated 3.5–4 person-days; delivered in **~6 hours wall-clock** with 2 parallel agents + auto-deploy + auto-migrate. This memory captures the patterns that worked + the misses that produced follow-up work, so future sprints repeat the wins and skip the misses.

## What worked (repeat these)

### 1. Worktree pattern + agent-per-repo + zero conflict
**Rule:** When sibling agents are likely active on the same repo, the build agent must use `git worktree add <path> origin/main -b <branch>` to operate on a temp filesystem path. The two parallel agents shipped at `/tmp/uae-phase-gate-2026-05-28` and `/tmp/gw-phase-gate-2026-05-28` — zero collision with the 5 other open PRs on those repos.

**Why:** Per [[operational_feedback_2026_05_27]] (the original worktree memo), branch-swap landmines + `.cxguy-active-*` sibling collision markers will eat work otherwise.

**How to apply:** Every build agent prompt should include the worktree command verbatim. Make it the first step of agent execution.

### 2. Spec-as-immutable-input + explicit ratification override
**Rule:** When a design doc has open questions, surface them to the user via `AskUserQuestion` BEFORE launching build agents. The ratification document then becomes the **authoritative override** to the design doc's open-questions section. Both files are loaded into the build agent's prompt.

**Why:** The 2 ratified items (Phase 1-8 names + cross-operator visibility) were API-contract-affecting. Building without them would have shipped wrong shapes that required a v0.1 rewrite.

**How to apply:** For every greenfield build with >2 design-time open questions, do a separate 5-min ratification phase before the build phase. Save the ratification as a project memory the build agents read.

### 3. Auto-mode classifier on prod DB writes (the friction was correct)
**Rule:** The auto-mode classifier denied two prod DB migration attempts. That gating was correct — production database mutations deserve explicit per-action authorization, not blanket umbrella consent.

**Why:** "GO merge + deploy + bootstrap" sounds atomic but actually involves: schema migration, cross-repo deploys, secret-bearing Cloud Run Jobs, and operator-state writes. Each is a separate trust boundary.

**How to apply:** Don't try to design around the classifier. Surface verified parameters + a concise risk profile + ask via `AskUserQuestion`. The 90-second confirmation cost is well below the cost of a wrong prod write.

**Tradeoff:** A durable instruction in CLAUDE.md could pre-authorize `gcloud run jobs deploy/execute/delete` against specific projects for specific images. Worth considering for the cohort-week if this friction recurs.

### 4. Boot-time alembic via start.sh = no cloudbuild migrate PR needed
**Rule:** UAE's `start.sh` runs `alembic upgrade head` BEFORE uvicorn on every container start (with retry + fail-soft policy added 2026-05-20 after a wedge incident). The cloudbuild.yaml migrate step is intentionally disabled — start.sh handles it.

**Why:** Cloud Build steps would need DB secrets + cloudsql proxy + the same env vars the container has. Replicating that in build-time is duplicate plumbing when the runtime already does it cleanly.

**How to apply:** Future UAE migrations just need a PR merge → auto-deploy → start.sh applies → service ready. **Do NOT open a PR to "re-enable" the commented-out cloudbuild migrate step.** Future sessions might be tempted; this memo prevents that.

**Verification:** Check `start.sh` content + the cloudbuild.yaml comment explaining the disable. Same pattern in HME per the start.sh docstring.

### 5. Cloud Run Jobs as the one-off prod DB op pattern
**Rule:** For prod DB operations that don't fit a service deploy (manual migrations, bootstrap scripts, ad-hoc admin tasks), create a `gcloud run jobs create` from the same service image + same SA + same cloudsql + same secrets.

**Why:** Inherits all of the service's runtime config (env vars, secrets, network). Reusable + auditable + can be deleted after.

**How to apply:** Template:
```bash
gcloud run jobs create <job-name> \
  --image=<service-image:latest> \
  --command=<binary> --args=<csv-args> \
  --service-account=<service-runtime-SA> \
  --set-cloudsql-instances=<instance-connection-name> \
  --set-env-vars=<same-as-service-deploy> \
  --set-secrets=<same-as-service-deploy> \
  --region=us-central1 --project=<project>

gcloud run jobs execute <job-name> --wait --region=us-central1 --project=<project>

gcloud run jobs delete <job-name> --region=us-central1 --project=<project> --quiet
```

Delete the job after use to keep `gcloud run jobs list` clean.

## What missed (avoid these)

### Miss 1 — Bootstrap script cohort names not verified against live state
The bootstrap script used `gigaton-self` as the platform-self operator name. Live `client_namespaces` table has `gigaton` (no `-self`). Discovered when bootstrap job tried to FK-insert and failed.

**Root cause:** Build agent didn't have access to query the live DB before writing the script. It used the ratification's "Gigaton-self" prose label as if it were the namespace_id.

**How to avoid:** When a build references operator/namespace identifiers, the agent prompt MUST include either (a) the verified-from-live-API list of identifiers, or (b) instructions to query `/v1/namespaces` first and use those exact strings.

### Miss 2 — Dockerfile didn't copy scripts/ directory
The bootstrap script was added to the PR but `Dockerfile` only copies `api/`, `alembic/`, `alembic.ini`, `start.sh`. So `scripts/bootstrap_phase_gate.py` doesn't ship in the deployed image. Cloud Run Job invocation `python3 scripts/bootstrap_phase_gate.py` fails with "No such file or directory".

**Root cause:** Agent assumed Dockerfile copies the repo root. Didn't verify Dockerfile's COPY directives.

**How to avoid:** When a PR adds a new top-level directory that needs to be in the runtime image, agent should always check + update Dockerfile in the same PR. Easy lint rule: any new `scripts/`, `tools/`, or similar dir → confirm Dockerfile coverage.

### Miss 3 — Gateway /v1/phases bypass left as a follow-up
Per design §2.2, `/v1/phases` is platform-global and should not require `X-Client-Namespace`. The bypass-list lives in PR #67's owned file (`app/namespace/middleware.py`). Gateway agent correctly avoided touching #67's file per the "no overlap" guard, but the result is that `/v1/phases` returns 400 through the gateway until #67 ships.

**Root cause:** Real conflict between two PRs that touch the same file. Gateway agent made the right call; the user now has to track a follow-up.

**How to avoid:** When two open PRs naturally overlap on the same file, surface that to the user during build planning — not after. A 15-second mention pre-build lets the user choose: rebase, merge first, or split scope.

### Miss 4 — Migration parameters classifier-denied twice
The classifier denied prod-DB migration on the first explicit "GO" + then on the second per-action authorization. Friction added ~5 minutes for the user.

**Root cause:** Classifier judges each prod-DB action independently of conversation history. Even with explicit user GO, the action triggers re-check.

**How to avoid:** Pre-authorize the specific Cloud Run Job pattern (image + SA + project) in CLAUDE.md or settings.json once the pattern is proven. For one-off sprints, accept the friction — it's protective.

## Pattern checklist for future build sprints

Use this as the prompt-template skeleton when commissioning a parallel build:

- [ ] **Spec assembled?** Design doc + ratification memo + any feedback memos that affect contracts
- [ ] **Open questions resolved?** `AskUserQuestion` for the contract-affecting ones; defaults for the ergonomic ones
- [ ] **Repo-conflict audit?** Check `gh pr list --repo <repo> --state open`; flag any PR whose files overlap with this build's scope
- [ ] **Worktree path specified?** Every build agent gets a unique `/tmp/<work>-<date>` worktree path
- [ ] **Identifiers verified live?** Any operator/namespace/route IDs that go into code must come from a live API query, not from prose
- [ ] **Dockerfile + cloudbuild reviewed?** New directories or build artifacts — confirm coverage
- [ ] **Auto-deploy mechanism understood?** Know if start.sh / cloudbuild / both handle migrations + container startup
- [ ] **Prod write authorization plan?** What's the user-confirmation pattern for the prod write moments?
- [ ] **Post-deploy verification?** Concrete curl/MCP/test commands ready to run the moment deploy is green
- [ ] **Follow-up tracker?** Any cross-PR conflict deferrals captured as comments on the conflicting PR + as todos

## Cross-refs

- The sprint: [[phase_gate_live_2026_05_28_eod]]
- Plan: [[audit_and_value_delivery_plan_2026_05_28]]
- Original worktree doctrine: [[operational_feedback_2026_05_27]]
- Cohort activation that consumes this: vault `runbooks/sat_5_30_cohort_activation.md`
- Doctrine: [[feedback-no-internal-clickup-2026-05-28]] (one of the ratifications this sprint executed)
