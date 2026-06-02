---
name: learning-loop-live-2026-05-28
description: "The auto-memory → MKB → silo → Q&A learning loop is now LIVE end-to-end. 3,656 MKB chunks ingested. Doctrine queries return cited answers from CONSTITUTION / decisions / runbooks / for-the-group."
metadata: 
  node_type: memory
  lifecycle_state: canonical
  status: LIVE
  type: project
  established: 2026-05-28
  originSessionId: 531af6d3-63fd-43c2-a00f-95d7349257b6
promoted_from: learning_loop_live_2026_05_28.md
promoted_at: 2026-06-02T20:13:25Z
---

# Recursive learning loop — LIVE 2026-05-28 EOD

The architecture described in [[learning_loop_architecture]] (MKB `LEARNING_LOOP.md`) is operational end-to-end as of 2026-05-28.

## What's working

- **127 MKB files / 3,656 chunks** in `carmen-beach-properties` silo FAISS at `operator_id=gigaton`. Covers CONSTITUTION, PRINCIPLES, LEARNING_LOOP, MASTER_PROJECT_PLAN, decisions/, decision-execution-engine/, for-the-group/, manifests/, runbooks/, knowledge-extracts/, claude-systems/v3.2/, brand-knowledge-library/.
- **`/memory/search`** against the silo returns scored results for doctrine queries (e.g. "INTEL-3 algorithmic real-time weight determination" → DECISION_ENGINE_FRAMEWORK + ADAPTIVE_LEARNING_LOOP_ARCHITECTURE).
- **`/v1/qa/ask`** (direct silo) returns prose + 5 real MKB citations grounded in the corpus. Society pipeline activates 7 minds. **Synthesis is extractive-stitch right now** because `ANTHROPIC_API_KEY` isn't set in the silo's Cloud Run env — set it for LLM-router-clean prose.
- **GCS backups:** `gs://gigaton-mkb-backup` exists, first bundle landed 2026-05-28 19:02 UTC. `com.gigaton.mkb-gcs-backup` LaunchAgent runs nightly 02:30 UTC.
- **Auto-memory promote bridge:** identifies 30 promotion candidates today. First scheduled run Sunday 06:00 UTC opens a PR for human review. After merge + next ingest, INTEL-3/PAYOUT-1/feedback rules become directly citeable.

## What's not working yet (logged for future)

- **Gateway `/v1/qa/ask` returns 400/403** — gateway requires `X-Client-Namespace: gigaton` AND the namespace resolver doesn't have `gigaton` registered. This is the [[namespace_middleware_silent_400_audit_2026_05_25]] issue. Workaround: hit silo directly. Real fix: register `gigaton` in the live namespace resolver.
- **`com.gigaton.mkb-ingest` LaunchAgent** — script still uses `gcloud auth print-identity-token --audiences=$SILO_URL` which fails for user creds. Use `SILO_TOKEN=$(gcloud auth print-identity-token)` (no audiences) inline for now. Small follow-up PR to add user-creds fallback in the script.
- **`gigaton-platform` silo** (migration target) is empty + stale — wait for MIG-DEFER silo session before seeding. See [[two_silos_carmen_vs_gigaton_platform_2026_05_28]].

## Key fix shipped — silo FAISS IVF train-defer (intel-silo PR #60)

`SemanticMemory._train_index()` previously crashed when corpus crossed the 256-vec trigger but was below `nlist=1000` (the default for `max_vectors=1M`). Every ingest after the 256th chunk returned HTTP 500 in perpetuity. Fix: defer training until corpus ≥ nlist; numpy fallback search path handles the pre-train state correctly. **If you see "RuntimeError: Number of training points (N) should be at least as large as number of clusters (1000)" in silo logs, this fix has reverted or a new code path bypasses it.**

## Why this matters (the user-stated goal it serves)

> "Every user receives all information / education required to maximize new feature & functionality + process creation + automatic human-adherence management."

Implementation: every doctrine ratified via PR to MKB → ingested into silo on the next push → grounded in `/v1/qa/ask` answers with citations. Users asking "how does comp work?" now get the actual PR #17 + INTEL-3 doctrine cited, not hallucination. After auto-memory promotion ships (Sunday), session-derived doctrine flows back automatically.

## Related

- [[learning_loop_architecture]] — the LEARNING_LOOP.md doc
- [[two_silos_carmen_vs_gigaton_platform_2026_05_28]] — which silo to ingest against
- [[qa_pipeline_phase2_shipped_2026_05_27]] — Q&A pipeline merges
- [[namespace_middleware_silent_400_audit_2026_05_25]] — why gateway 400/403s
