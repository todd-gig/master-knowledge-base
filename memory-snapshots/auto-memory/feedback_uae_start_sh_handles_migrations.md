---
name: feedback-uae-start-sh-handles-migrations
description: "UAE's start.sh runs `alembic upgrade head` on every container boot (with retry + fail-soft policy added 2026-05-20 after a wedge incident). The cloudbuild.yaml migrate step is intentionally disabled — start.sh is the canonical apply path. DO NOT open a PR to 're-enable' the commented-out cloudbuild migrate step. Future UAE migrations just need a PR merge → auto-deploy → start.sh applies."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-05-28
  status: ACTIVE doctrine
  originSessionId: c3d6a014-f8e0-4829-9d0d-6197cc8ac3f6
promoted_from: feedback_uae_start_sh_handles_migrations.md
promoted_at: 2026-06-02T20:13:25Z
---

# Feedback — UAE migrations run via start.sh, NOT cloudbuild

**Rule:** UAE applies alembic migrations on every container start via `start.sh`. The cloudbuild.yaml has the migrate step commented out **on purpose**. Do not "fix" this.

**Why:** Per `start.sh` docstring (commit history 2026-05-20): the boot-time apply path was added after the cloudbuild migrate step proved fragile (one specific migration wedged 4 consecutive deploys via a transient OperationalError on the post-upgrade `alembic_version` UPDATE). The boot-time apply has retry + fail-soft (warn + start uvicorn anyway) — much more resilient than build-time apply against transient Cloud SQL Auth Proxy connection drops.

**Mirrors the HME pattern** (per the start.sh docstring reference). Likely true for other Gigaton services with alembic.

**How to apply:**

- **Do NOT** open a PR to uncomment the cloudbuild migrate step in UAE.
- **Do NOT** propose a "follow-up migrate enablement" PR when reviewing UAE deploys.
- **Do** ship new alembic migrations as just-another-file in the PR. Auto-deploy + start.sh handle the apply.
- **Do** verify alembic upgrade ran by checking the deploy's container logs for the start.sh trace (`[start.sh] alembic upgrade head (attempt 1)` + no WARN lines).
- **Edge case:** If start.sh's fail-soft warning fires (alembic failed both attempts), service starts anyway against a stale schema. The WARN line in container logs is the canonical signal — alert on it.

**Pre-condition for Cloud Run Jobs as bootstrap pattern:** because start.sh applies on boot, by the time the deploy is green, alembic IS at head. Cloud Run Jobs that run `alembic upgrade head` after deploy are redundant no-ops (verified 2026-05-28 by the migrate Cloud Run Job's exit-0-with-no-upgrade-operations behavior).

**Impact on the cloudbuild.yaml comment:** the comment ("Re-enable when api/models/ + alembic/versions/ land in a subsequent deploy") is now outdated — those files have landed (PR #50, 2026-05-28) and start.sh already handles them. The comment could be updated to "Intentionally disabled — start.sh applies migrations on boot per fail-soft policy." Low priority but useful for the next person who reads the file.

**Discovered:** 2026-05-28 during the Phase Gate sprint. I attempted to run a Cloud Run Job to apply 0024_phase_gate; the migration had already been applied by start.sh moments before during the new revision's container boot. The Job ran (auto-mode classifier approved by user) and was a no-op.

**Cross-refs:**

- [[build_sprint_postmortem_2026_05_28]] §"What worked #4" — same pattern
- [[phase_gate_live_2026_05_28_eod]] §"start.sh runs alembic upgrade head" — same finding
- UAE `start.sh` file itself (lines 1-50) — the canonical doctrine source
