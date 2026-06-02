---
name: cloudbuild-dollar-escape-in-yaml-comments-too
description: "Cloud Build's substitution parser reads single-dollar refs everywhere in cloudbuild.yaml — including YAML comments. Both bash code AND comment lines must use $$ to escape, or `key in the template 'X' is not a valid built-in substitution` errors block the deploy."
metadata:
  type: feedback
established: 2026-05-20
originSessionId: this-session
promoted_from: feedback_cloudbuild_dollar_escape_in_yaml.md
promoted_at: 2026-06-02T20:13:25Z
---

# Cloud Build YAML — every dollar in the file is parsed, not just code

Cloud Build pre-processes `cloudbuild.yaml` through its substitution engine BEFORE handing the YAML to its build steps. The substitution engine reads any `$VARNAME` token anywhere in the file — including:

- bash heredocs / inline scripts (the obvious case)
- shell variable assignments in `args:`
- **YAML comment lines** (the non-obvious case)
- `description:` blocks
- env-var defaults in `substitutions:`

If the parser hits a `$VARNAME` that isn't a built-in (PROJECT_ID, BUILD_ID, etc.) or a `_USER_DEFINED` substitution, the entire submit fails with:

```
ERROR: (gcloud.builds.submit) INVALID_ARGUMENT: generic::invalid_argument: invalid value for 'build.substitutions': key in the template "VARNAME" is not a valid built-in substitution
```

## The rule

**Every dollar sign in `cloudbuild.yaml` that isn't a built-in must be `$$` (double dollar).** That includes inside YAML comments.

For variables you want bash to expand, write `$$BASH_VAR`. The Cloud Build parser converts `$$` → `$`, leaving bash to see `$BASH_VAR`.

## Built-ins that are safe as single-dollar

`$PROJECT_ID`, `$PROJECT_NUMBER`, `$LOCATION`, `$BUILD_ID`, `$REPO_NAME`, `$BRANCH_NAME`, `$TAG_NAME`, `$REVISION_ID`, `$COMMIT_SHA`, `$SHORT_SHA` and any `$_USER_SUBSTITUTION` defined in the `substitutions:` map.

Anything else (your own bash-expanded variables — `$FOO`, `$EXTRA_FLAGS`, `$SECRETS_LIST`, `$VAR`, `$FILES`, etc.) must be `$$FOO`.

## How to apply

In any cloudbuild.yaml change, grep for `\$[A-Z_][A-Z0-9_]*` that is NOT preceded by another `$` and NOT a built-in:

```bash
grep -nE '\$[A-Z_][A-Z0-9_]*' cloudbuild.yaml | grep -v '\$\$' | grep -v -E '\$(PROJECT_ID|BUILD_ID|REPO_NAME|BRANCH_NAME|TAG_NAME|COMMIT_SHA|SHORT_SHA|REVISION_ID|PROJECT_NUMBER|LOCATION)\b'
```

If anything matches inside a comment block, prefer rewording over `$$`. Comments shouldn't carry executable shell syntax — replace the dollar example with prose, or with the bare variable name (no leading dollar).

## Incidents — append to this list when re-bitten

- **2026-05-19** (PR #16-ish on intelligence-silo) — `$EXTRA_FLAGS` reverted twice by IDE auto-formatters. Mitigation: added a "KEEP $$ — DO NOT change" comment.
- **2026-05-20 silo PR #29** — `$SECRETS_LIST` introduced in the bash block; deploy failed on first GHA fire after `chore/auto-deploy-on-main-silo` (PR #28) merged. Fix shipped in PR #29.
- **2026-05-20 silo PR #30** — PR #29 was a stale half-fix: the explanatory comment inside cloudbuild.yaml contained a `$VAR` example, which the parser then read literally. Fix shipped in PR #30 — replaced the comment example with prose.

## Why this matters

Each occurrence costs ~10 minutes (deploy → CI failure → log scrape → fix → repush → re-CI). Three back-to-back occurrences on 2026-05-20 alone (one of which was a self-defeating fix that referenced the trap in a way that re-triggered it). Future agents touching cloudbuild.yaml should grep BEFORE pushing.

## Cross-references

- `intelligence-silo/cloudbuild.yaml` — has the canonical "$$ KEEP" comment + the updated DO-NOT-include-dollar-examples comment block
- 2026-05-19 master handoff (where $EXTRA_FLAGS was originally documented)
