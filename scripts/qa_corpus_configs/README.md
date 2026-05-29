# Q&A corpus configs (per operator)

Each operator has one JSON config that names every source root the
incremental ingest should walk. The default `todd.json` mirrors what was
seeded on 2026-05-28 (Obsidian vault + auto-memory + MKB runbooks +
architecture + manifests).

## Onboarding a new operator

1. Copy `todd.json` to `<operator-slug>.json`.
2. Replace `operator_id` and rewrite `sources` to point at that operator's
   actual document trees (Drive sync, repo checkouts, mounted vaults …).
3. Optional: store the file in this repo so other operators / siblings can
   review it; or in `~/.config/gigaton/qa-corpus/<op>.json` if it shouldn't
   be shared.
4. Add a launchd plist alongside `com.gigaton.qa-corpus-incremental-todd.plist`
   pointing at the new config (or just override `--operator` + `--config`).
5. First-run is full ingest (cold state file); subsequent runs are
   incremental against `~/.local/state/gigaton/qa-corpus/<operator>.json`.

## Source-root conventions

| `category` | Used for |
|---|---|
| `vault`        | Operator's Obsidian / personal knowledge vault |
| `memory`       | Claude Code auto-memory (`~/.claude/.../memory`) |
| `runbook`      | Operational runbooks (one-off ops + recurring playbooks) |
| `architecture` | Long-lived architectural decisions / spec docs |
| `manifest`     | YAML / JSON manifests the operator uses for config-driven flows |
| `drive:<folder>` | When Drive content is added later, use `drive:<folder-name>` |

The category becomes the prefix of the `source` field on every ingested
chunk, so `/v1/qa/ask` citations show `vault:memory/glossary.md` etc.

## Multi-silo (migration target)

When the carmen-beach → gigaton-platform migration completes, point the
plist's `SILO_URL` env var at the new silo URL and re-run — the script's
state file makes the first post-migration run almost free if the corpus
hasn't changed.
