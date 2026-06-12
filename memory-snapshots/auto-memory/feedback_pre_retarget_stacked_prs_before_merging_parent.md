---
name: feedback-pre-retarget-stacked-prs-before-merging-parent-2026-06-01
description: "When merging a PR that has stacked children, retarget the children to main BEFORE merging the parent. Otherwise `gh pr merge --delete-branch` triggers auto-close on the children because their base ref is deleted. Reopen of an auto-closed PR fails because the base ref is gone. Recovery requires creating fresh PRs from the same head branches — preserves commits but burns the original PR number. Reinforces the [[three_week_cadence_compressed_to_eod_2026_05_28]] doctrine."
metadata:
  node_type: memory
  type: feedback
  established: 2026-06-01
  lifecycle_state: canonical
  originSessionId: c3d6a014-f8e0-4829-9d0d-6197cc8ac3f6
promoted_from: feedback_pre_retarget_stacked_prs_before_merging_parent.md
promoted_at: 2026-06-02T20:13:25Z
---

# Pre-retarget stacked PRs before merging parent

## The rule

When you have stacked PRs (child.base = parent.head), and you intend to merge the parent with `--delete-branch`:

**ALWAYS retarget every stacked child to `main` BEFORE merging the parent.**

```bash
# correct order
gh pr edit <child> --base main    # FIRST
gh pr merge <parent> --merge --delete-branch
gh pr merge <child> --merge --delete-branch
```

If you forget, GitHub auto-closes the children at the same wall-clock instant the parent merges (because their base ref no longer exists). And once auto-closed against a deleted base, the child is unrecoverable as-is — `gh pr reopen` returns `GraphQL: Could not open the pull request`. The only path forward is `gh pr create --head <same-branch> --base main` to open a fresh PR, which preserves commits but burns the original PR number.

## Why

`--delete-branch` triggers ref deletion on the GitHub side; refs cannot be resurrected. The PR object remains visible (history is preserved) but is permanently in `CLOSED` state. Reopen requires a valid base ref, which doesn't exist anymore.

## How to apply

For any campaign that ships PRs in waves with cross-PR base references:

1. Identify every stacked child via the dependency map (recommended: keep a `base → head` table in the design memory like the v0.1 affiliate build did).
2. **Before** the first parent merge, retarget every direct child to `main`. They go `mergeStateStatus: UNKNOWN` briefly while GH recomputes the diff, then back to `CLEAN` (or `CONFLICTING` if true conflicts exist, which signals real work to do).
3. Confirm children are `CLEAN/MERGEABLE` against `main`.
4. Merge parents with `--delete-branch`.
5. Merge children with `--delete-branch`.

## How NOT to apply

- **Do not** rely on GitHub's "auto-retarget on parent merge" — it only fires when the parent is merged WITHOUT branch deletion (i.e., `--delete-branch=false`). If you delete the parent's branch, retarget does not happen; auto-close does.
- **Do not** attempt `gh pr reopen` on a child that auto-closed against a deleted base. It returns GraphQL error and wastes time.
- **Do not** try to push a new commit to the child branch hoping GH will reopen — it won't.

## Real incident: 2026-06-01 affiliate v0.1 activation

Tier 1 merge of UAE #54 + UI #61 (both with `--delete-branch`) auto-closed their stacked children #55 (UAE root seed) + #62 (UI signup welcome). Both PRs vanished from the open list at the exact second the parent merged. Recovery: created #57 (replaces #55) + #64 (replaces #62) from the same head branches against `main`. Same commits, same diff, same review surface — just new PR numbers. ~3 min recovery cost.

The doctrine was already in memory as [[three_week_cadence_compressed_to_eod_2026_05_28]] ("auto-close-on-base-deletion trap"). I had it loaded and still hit the trap because I executed the merges from the recommended-tier order in the design memory WITHOUT first reading the retarget step. **Memory present ≠ memory applied.** This is now a separate, more prominent memory specifically about the prophylactic step.

## Tactical: when you also want to preserve the parent's branch

If a parent has multiple stacked children AND you can't retarget them all simultaneously (e.g., manual review needed per child), merge the parent with `--delete-branch=false`. The parent's branch sticks around, child PRs remain valid, and you can delete the parent's branch later via `gh api -X DELETE repos/<owner>/<repo>/git/refs/heads/<branch>` once all children have merged or been retargeted.

## Related

- [[three_week_cadence_compressed_to_eod_2026_05_28]] — the original "auto-close-on-base-deletion trap" entry, lumped with other doctrine reinforcements; this memory promotes it to its own first-class rule
- [[operational_feedback_2026_05_27]] — sibling pattern: pre-flight verify state before destructive actions
- [[affiliate_system_design_v0_2026_05_28]] — the campaign where this trap was triggered and recovered from
