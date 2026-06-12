---
name: pr14-post-merge-followup-fixes-2026-05-26
description: "PR #14 in todd-gig/master-knowledge-base (runbooks PR — OAuth client recreation + Q&A pipeline + legacy scope sunset) was already MERGED 2026-05-26. Post-merge review surfaced 3 P1 issues that need a follow-up commit BEFORE any sibling agent executes the OAuth-client-recreation runbook or the consent-screen-edit step in the sunset plan."
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  urgency: "P1 (not Thursday-blocking, but blocks safe execution of the merged runbooks)"
  status: open — follow-up commit needed
  originSessionId: 6e6b0670-1f83-4845-993e-48d0475c7a3e
promoted_from: pr14_post_merge_followup_fixes_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# PR #14 Post-Merge Follow-Up Fixes

## Context

PR #14 in `todd-gig/master-knowledge-base` merged 2026-05-26 (+802/-0, three new runbooks + decisions-log append). Substantive content is sound but 3 issues surfaced in post-merge review that must be fixed before the runbooks are safe to execute.

## Issues

### Fix 1 — MIG-CANCEL supersession banner (P1, BLOCKS sibling-agent execution)

**File:** `runbooks/2026_05_25_oauth_client_recreation_gigaton_platform_migration.md`

**Problem:** The entire runbook's premise (intelligence-silo migrates `carmen-beach-properties` → `gigaton-platform`) is contradicted by **MIG-CANCEL** locked in `decisions/2026-05-25_architecture_decisions_log.md` and `[[RESUME_HERE_2026_05_26_full_session_handoff]]` §4. carmen-beach-properties engines STAY put; gigaton-platform is warm-DR mirror only.

**Fix:** Prepend a status banner:
```
STATUS: SUPERSEDED 2026-05-26 by MIG-CANCEL — DR-only mirror, no production migration.
This runbook is preserved for the DR-mirror OAuth-client provisioning subset only.
DO NOT execute the production-migration steps.
```

**Why this is P1:** A sibling agent or future Claude session could execute this runbook verbatim and undo MIG-CANCEL intent.

### Fix 2 — `/chat` → `/intelligence` rename (P1)

**File:** `runbooks/2026_05_25_intelligence_qa_on_ingested_files.md` §1 and §7

**Problem:** Still references `/chat` for path and intent classification. Per **INTEL-1** in `decisions/2026-05-25_architecture_decisions_log.md` (lines 9-19 of this very PR), `/chat` was renamed to `/intelligence`. The route alias landed in `gigaton-ui-system` PR #41.

**Fix:** `s/\/chat/\/intelligence/g` in runbook prose and architecture diagram.

**Why this is P1:** Self-inconsistency inside the same PR — operator following the runbook hits a 301/404 trying to navigate to a removed route.

### Fix 3 — Duplicate `## 7.` heading (P1)

**File:** `2026_05_25_intelligence_qa_on_ingested_files.md` lines 357 and 370

**Problem:** Both "Implementation order" and "Critical Files for Implementation" are numbered `## 7.`.

**Fix:** Renumber second to `## 8.`.

### Fix 4 — Sunset plan §5.4 (P1)

**File:** `runbooks/2026_05_25_legacy_scope_sunset_plan.md` §5.4

**Problem:** Says "Edit consent screen at `console.cloud.google.com/auth/scopes?project=carmen-beach-properties` (or `gigaton-platform` post-migration)." MIG-CANCEL conflict — consent screen lives permanently on `carmen-beach-properties`.

**Fix:** Strip the "or gigaton-platform" clause.

## P2 nits (do alongside, low urgency)

- PAYOUT-1 entry in decisions log (lines 47-48) still has stale TBD currency-rounding clarifications. Per `[[payout_1_and_intel_1_clarifications_locked_2026_05_26]]`, all 4 PAYOUT-1 clarifications are locked. Decisions log should be amended.
- OAuth-client-recreation runbook §2.2 — `oauth2.googleapis.com/v1/iam-policies/.../brands` is not a real endpoint shape. Use `gcloud iap oauth-brands list --project=carmen-beach-properties` instead.
- Q&A runbook §5 Phase 3 path string `MD Files/intelligence-engine/` contains a literal space — fragile in shell/CI; flag for rename or quoting convention.

## Recommended action

Follow-up commit on branch `docs/post-pr14-merge-followup-2026-05-26` with the 4 P1 fixes + P2 nits. PR can be small (likely <50 lines diff). Either ratified by Todd, or a sibling Claude session can execute as a chore commit + PR.

**Constraint per [[mcp_multi_tenant_namespace_blocker_2026_05_26]] / sibling-coordination doctrine:** DON'T edit these files without checking for an active `.cxguy-active-migration` marker in the repo. If a sibling is currently authoring follow-on runbooks, they may overlap.

## Cross-references

- Source PR: `gh pr view 14 --repo todd-gig/master-knowledge-base`
- MIG-CANCEL: `decisions/2026-05-25_architecture_decisions_log.md` MIG-CANCEL entry
- INTEL-1: same decisions log INTEL-1 entry (lines 9-19 of PR #14)
- Sibling fleet state: `[[sibling_fleet_state_and_mig_cancel_conflict_2026_05_26]]`
