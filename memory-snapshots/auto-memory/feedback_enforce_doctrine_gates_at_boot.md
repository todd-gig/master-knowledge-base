---
name: enforce-doctrine-gates-at-boot-not-docstrings
description: When a migration, config, or deploy step is doctrine-gated (founder approval, AX-010, sign-off matrix, etc.), encode the gate as runtime code in the boot path. NEVER rely on a docstring or comment alone — auto-deploys do not read prose.
metadata:
  type: feedback
established: 2026-05-19
priority: 1
promoted_from: feedback_enforce_doctrine_gates_at_boot.md
promoted_at: 2026-06-02T20:13:25Z
---

## The rule

If a migration / config change / capability requires doctrine sign-off before being applied, the GATE must live in code that the boot path executes. A docstring saying "NOT applied per AX-010" is documentation, not enforcement.

**Anti-patterns observed:**
- Alembic migration with docstring "Founder approval required" + boot script runs `alembic upgrade head` unconditionally → migration auto-applies on first deploy that picks it up
- Capability seed file documented as "draft, pending sign-off" + UAE startup loads `_DEFAULT_CATALOG` indiscriminately → draft capabilities go live
- Config flag with `# TODO: gate behind feature flag` comment + no feature flag wired → flag is "on" in prod

## Why

Auto-deploy pipelines fire on `push to main`. Once code is merged, the boot path runs whatever's there. Humans-in-the-loop CANNOT be the enforcement mechanism for an automated pipeline. Doctrine-as-comment is fundamentally incompatible with continuous deployment.

Engineered enforcement options (any of these are acceptable; pick by scope):

1. **Runtime allow-list env var**. Boot script reads `ENFORCED_MIGRATIONS_MAX=0007` from Secret Manager. Alembic upgrades only up to 0007, never beyond, regardless of what's on disk. Founder approval = updating the secret value.

2. **Separate Cloud Run Job for gated work**. Move financial-impact / irreversible migrations to `alembic/financial/` with their own Cloud Run Job (`carmen-financial-migrate`). Default boot path doesn't see them. Founder approval = manually invoking the Job.

3. **Migration-level metadata + pre-upgrade hook**. Each migration file declares `requires_approval: bool` + an approval-token check before `op.create_table()`. Boot path's alembic invocation checks the table.

4. **Branch-protected migration files**. Make `alembic/financial/` a CODEOWNERS-required-review-from-Todd path. Combined with branch protection on `main`, this gates the human side too (but does NOT replace runtime enforcement — both layers needed).

5. **Feature flags via GrowthBook / LaunchDarkly / config-server**. Any gated capability defaults to OFF; flipping on requires a config update outside the deploy pipeline.

## How to apply

**Whenever you write:**
- An alembic migration with a sign-off requirement
- A config seed marked "draft / pending review"
- A capability or model marked "experimental / behind flag"
- An integration that should not auto-activate

**Ship the enforcement gate in the SAME PR.** Either:
- Add the runtime check that reads the gate state from Secret Manager / env var
- Move the artifact into a Cloud Run Job tree that requires explicit execution
- Annotate with metadata that the boot path actively checks

**Reject PRs that contain doctrine-gated artifacts without code-level enforcement.** A docstring is not a gate.

## When the rule was established

2026-05-19 ~02:15 UTC. HME auto-deploy fired commit 2e7569d (Value of Human Contribution Matrix). Migration `0008_contribution_records.py` carried docstring "FINANCIAL-IMPACT — NOT applied per AX-010. Founder approval required." Boot script `start.sh` runs `alembic upgrade head` unconditionally. Migration auto-applied to production. P0 HME outage followed for separate reasons. Post-incident: this rule.

## Concrete example (HME case)

The fix for HME specifically (track for future): rewrite `start.sh` to:

```bash
# Read max applied migration from env (defaults to "head" only in dev)
ALEMBIC_UPGRADE_TARGET="${ALEMBIC_UPGRADE_TARGET:-0007}"  # SET BY DEPLOY CONFIG
alembic upgrade "$ALEMBIC_UPGRADE_TARGET"
```

Founder approval to advance: update Cloud Run env var `ALEMBIC_UPGRADE_TARGET=0008` via a separate change-control commit + explicit deploy with founder sign-off.

