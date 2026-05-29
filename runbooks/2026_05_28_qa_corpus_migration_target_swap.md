---
title: Q&A corpus migration-target swap (carmen-beach → gigaton-platform)
status: ready
last_updated: 2026-05-28
ppim_axis: continuity-of-value
ppim_priority: HIGH
ppim_predictability: HIGH (state file makes the cutover near-free)
---

# Q&A corpus migration-target swap

When the carmen-beach-properties intel-silo is cut over to its
gigaton-platform replacement (per
[[2026_05_25_gcp_migration_accelerated_complete_plan]]), every operator's
Q&A corpus has to follow. This runbook captures the cutover steps so the
swap is push-button.

## Pre-cutover inventory

Each running operator has:
- A config file at `scripts/qa_corpus_configs/<operator>.json`
- A state file at `~/.local/state/gigaton/qa-corpus/<operator>.json` that
  records (mtime, size, sha256_8) for every file ingested into the
  CURRENT silo URL.
- A launchd job at
  `~/Library/LaunchAgents/com.gigaton.qa-corpus-incremental-<operator>.plist`
  with `SILO_URL` set to the current silo.

As of 2026-05-28, operators with an active corpus: **todd** (446 files /
~8,900 chunks on `intelligence-silo-rjmcrtvuzq-uc.a.run.app`).

## Cutover steps

Run for each operator. Order: do `todd` last so anything driven by his
corpus (cowork UI / `/intelligence` route) stays available until the
swap completes.

1. **Confirm the new silo's URL and health:**

   ```bash
   NEW_SILO=https://intelligence-silo-825651647756.us-central1.run.app
   curl -sS "$NEW_SILO/health"   # expect HTTP 200
   curl -sS -X POST -H 'Content-Type: application/json' \
        -d '{"query":"smoke","operator_id":"<operator>","top_k":1}' \
        "$NEW_SILO/memory/search" | jq .
   ```

   If `/memory/search` 500s, debug the new silo before proceeding — do
   NOT continue (you'll just create a dual-empty-corpus state).

2. **Stop the launchd job to avoid concurrent writes to two silos:**

   ```bash
   launchctl unload ~/Library/LaunchAgents/com.gigaton.qa-corpus-incremental-<operator>.plist
   ```

3. **Re-seed the new silo as a one-shot full ingest:**

   ```bash
   cd ~/Documents/GitHub/master-knowledge-base
   SILO_URL="$NEW_SILO" \
   python3 scripts/qa_corpus_ingest.py \
     --operator <operator> \
     --config scripts/qa_corpus_configs/<operator>.json \
     --state-file ~/.local/state/gigaton/qa-corpus/<operator>-NEW.json \
     --full
   ```

   This walks every source root and POSTs every file (the state file is
   fresh so nothing is skipped). For todd this is ~8 min / 446 files.

4. **Smoke verify the new corpus:**

   ```bash
   curl -sS -X POST -H 'Content-Type: application/json' \
     -d '{"question":"What is the GCP migration plan?","operator_id":"<operator>","top_k":3}' \
     "$NEW_SILO/v1/qa/ask" | jq '.confidence, .citations | length'
   ```

   Expect `confidence > 0.5` and at least one citation. If empty,
   investigate before flipping.

5. **Swap the plist's `SILO_URL` env var to the new silo:**

   ```bash
   PLIST=~/Documents/GitHub/master-knowledge-base/scripts/launchagents/com.gigaton.qa-corpus-incremental-<operator>.plist
   sed -i.bak "s|<string>https://intelligence-silo-rjmcrtvuzq-uc.a.run.app</string>|<string>$NEW_SILO</string>|" "$PLIST"
   rm "$PLIST.bak"
   ```

6. **Replace the live state file with the new one and reload the job:**

   ```bash
   mv ~/.local/state/gigaton/qa-corpus/<operator>.json{,.carmen-beach.bak}
   mv ~/.local/state/gigaton/qa-corpus/<operator>-NEW.json \
      ~/.local/state/gigaton/qa-corpus/<operator>.json
   cp "$PLIST" ~/Library/LaunchAgents/$(basename "$PLIST")
   launchctl load ~/Library/LaunchAgents/$(basename "$PLIST")
   launchctl list | grep qa-corpus-incremental-<operator>   # confirm loaded
   ```

7. **One-shot run to confirm the post-cutover state file is in sync:**

   ```bash
   SILO_URL="$NEW_SILO" \
   python3 scripts/qa_corpus_ingest.py \
     --operator <operator> \
     --config scripts/qa_corpus_configs/<operator>.json \
     --dry-run
   ```

   Expect `skipped_unchanged = <total>` and `to-ingest = 0` on every
   source — that proves state matches reality.

8. **Update operator-api / cowork-UI / gateway routing** to point at the
   new silo URL. Out of scope for this script (handled by the
   gateway-routing PRs in the migration plan).

## Rollback

If the new silo is broken and the FE is already pointed at it:

1. Re-deploy gateway with `INTELLIGENCE_SILO_URL=<carmen-beach URL>`.
2. Swap the plist's `SILO_URL` back.
3. `mv <operator>.json.carmen-beach.bak <operator>.json`.
4. `launchctl unload + load` the plist.

The carmen-beach silo and its corpus stay intact through the cutover
(nothing was deleted there), so rollback is a config swap.

## Why a separate state file per silo URL?

Each silo has its OWN FAISS index. The state file records "I ingested
file X with sha256_8=ab12cd34 into THIS silo." If you point the same
state file at a different silo and run incremental, every file looks
"unchanged" and zero get posted — but the new silo is empty. The
`SILO_URL` field in the state file is a debugging marker; the actual
correctness comes from generating a fresh state file alongside the
re-seed and swapping atomically (steps 3 + 6).
