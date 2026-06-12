# Dogfood install + E2E validation — gigaton-local-mind

**Operator:** todd (gated through 2026-06-10)
**Status:** ready-when-phase-1-merges
**Established:** 2026-06-02
**Parent commitment:** `[[directive_local_mind_buildout_2026_06_01]]`

This is the canonical operator-facing runbook. The matching memory entry
at `~/.claude/projects/-Users-admin/memory/dogfood_install_local_mind_2026_06_02.md`
is the AI's quick-reference companion.

Run this the moment **all three** Phase 1 PRs land on `main` AND their
Cloud Run auto-deploys settle (~90s each):

1. `gigaton-mcp` PR #2 — local-mind MCP server (MERGED 2026-06-02 16:44 UTC)
2. `intelligence-silo` PR #69 — `POST /v1/qa/ingest_preembedded`
3. `gigaton-gateway` PR #82 — `/v1/qa/ask` augment + `/v1/local-mind/handshake`

## Prereqs

- Cloud Run services green: `gigaton-gateway` + `intelligence-silo` revisions match HEAD of main
- `gh auth status` shows `todd-gig` active
- Python 3.11+ in the env you'll run Claude Desktop's MCP servers from
- ~3GB free disk for MiniLM (90MB) + spaCy en_core_web_sm (50MB) + headroom

## 1. Install (one-time, ~10 min including model downloads)

```bash
# 1.1 Sync monorepo
cd /Users/admin/Gigaton-UI-Platform/gigaton-mcp
git fetch origin && git checkout main && git pull --ff-only

# 1.2 Install gigaton-local-mind editable
cd servers/gigaton-local-mind
uv pip install -e .

# 1.3 Install spaCy model wheel (~50MB) — pyproject lists it as optional dep
uv pip install -e ".[spacy-model]"

# 1.4 Warm the MiniLM model (~90MB download from HuggingFace).
#     Note: the public lib API is `embed_texts`, NOT `get_embedder` — the
#     latter is internal. If the install docs anywhere reference
#     `get_embedder`, they are stale; the validated public surface is:
python -c "from gigaton_local_mind.embedder import embed_texts; \
v = embed_texts(['warm-up']); \
print('warmed:', len(v[0]))"
# Expect: warmed: 384

# 1.5 Verify capability probe (smoke — server boots cleanly)
python -m gigaton_local_mind --probe 2>&1 || echo "(probe flag may not exist yet — fine)"
```

## 2. Register in Claude Desktop

Edit `~/.claude.json` (or create if missing) — add an entry under `mcpServers`:

```json
{
  "mcpServers": {
    "gigaton-local-mind": {
      "command": "/Users/admin/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/admin/Gigaton-UI-Platform/gigaton-mcp/servers/gigaton-local-mind",
        "run",
        "python",
        "-m",
        "gigaton_local_mind"
      ],
      "env": {
        "GIGATON_GATEWAY_URL": "https://gigaton-gateway-sqatlxhlza-uc.a.run.app",
        "GIGATON_OPERATOR_ID": "todd",
        "MCP_TRANSPORT": "stdio"
      }
    }
  }
}
```

Restart Claude Desktop. Look for `gigaton-local-mind` in the MCP servers
indicator.

## 3. Handshake to gateway (validates Phase 1 PR C end-to-end)

From Claude Code or a Python shell:

```python
import httpx, os
r = httpx.post(
    f"{os.environ['GIGATON_GATEWAY_URL']}/v1/local-mind/handshake",
    headers={
        "X-Operator-Id": "todd",
        "Authorization": f"Bearer {os.environ['GIGATON_JWT_TODD']}",
    },
    json={
        "operator_id": "todd",
        "capability_tier": 2,
        "local_mind_version": "0.1.0",
        "capabilities_enabled": ["embed", "search", "dedup", "redact_pii"],
        "machine_fingerprint": "todd-mac-primary-2026"
    }
)
print(r.status_code, r.json())
# Expect: 200, routing_hints.embed == "local",
#         dogfood_gate.operator_id_is_in_dogfood == true
```

## 4. Smoke-test all 5 tools (in Claude Desktop chat)

1. **embed_chunks** — `embed_chunks(texts=["hello world", "gigaton ships fast"], namespace="dogfood")` → expect list of 2 × 384-dim float lists
2. **dedup_chunks** — `dedup_chunks(chunks=[{text:"a", metadata:{}}, {text:"a", metadata:{}}, {text:"b", metadata:{}}])` → expect `kept=[True, False, True]`, reason on dup
3. **redact_pii** — `redact_pii(text="Email todd.cx@turtleisland.solutions, phone (555) 123-4567")` → expect both redacted + Todd's name redacted if spaCy NER hits
4. **index_preembedded** — `embed_chunks` then `index_preembedded` the result → expect `{ingested: N, namespace: "dogfood"}` + file exists at `~/.gigaton/local-mind/todd/dogfood.faiss`
5. **search_local** — `search_local(query="hello", namespace="dogfood", k=2)` → expect top hit is `"hello world"` with score > 0.7

## 5. End-to-end validation against the cloud silo

Run the dogfood E2E script — this is the canonical "did Phase 1 actually
ship?" check:

```bash
cd /Users/admin/Documents/GitHub/master-knowledge-base
python scripts/dogfood_e2e_local_mind.py
```

The script:

1. Synthesises 3 deterministic test documents with run-tagged markers
   (e.g. `GIGADOG-A-AbCd12-2026`)
2. Embeds them locally via `gigaton_local_mind.embedder.embed_texts`
   (asserts 384-dim)
3. POSTs to `/v1/qa/ingest_preembedded` with `X-Operator-Id: todd` —
   asserts `ingested: 3` + `embedding_source: "local-mind"`
4. Replays the same idempotency_key — asserts `ingested: 0` +
   `deduped_idempotent: 3`
5. Waits 5s for FAISS to settle
6. Queries `/v1/qa/ask` via the gateway with question about marker A —
   asserts the answer or citations contain the marker, AND
   `local_mind_available: true` (proves PR #82 augment landed)
7. Verifies `event=ingest_preembedded` + `event=qa_ask` log lines via
   `gcloud logging read` (skip with `--no-logs`)
8. Emits cleanup guidance (intel-silo has no per-chunk delete endpoint
   as of 2026-06-02 — chunks are tiny + clearly labelled; leave or page
   silo ops for a FAISS surgical delete by `GIGADOG-` substring)

Exit code 0 = all green. Exit 1 = at least one step failed (the
summary table shows which).

Useful flags:

```bash
# Dry-run — exercises the script wiring without network or model load
python scripts/dogfood_e2e_local_mind.py --dry-run

# Skip the Cloud Logging step (e.g. gcloud auth stale)
python scripts/dogfood_e2e_local_mind.py --no-logs

# Override target services
python scripts/dogfood_e2e_local_mind.py \
    --gateway-url https://gigaton-gateway-staging.example \
    --silo-url   https://intelligence-silo-staging.example

# Wiring self-test (used by CI)
python scripts/dogfood_e2e_local_mind.py --self-test
```

## 6. Validate cost-saved telemetry (manual spot-check)

The E2E script's step 6 covers this automatically. To check by hand:

```bash
# silo: should show cost_avoided_usd=0.00 source=local-mind
gcloud logging read 'resource.type=cloud_run_revision
  AND resource.labels.service_name=intelligence-silo
  AND jsonPayload.event="ingest_preembedded"
  AND jsonPayload.operator_id="todd"' \
  --limit=5 --project=gigaton-platform

# gateway: should show local_mind_available=true post-handshake
gcloud logging read 'resource.type=cloud_run_revision
  AND resource.labels.service_name=gigaton-gateway
  AND jsonPayload.event="qa_ask"
  AND jsonPayload.operator_id="todd"
  AND jsonPayload.local_mind_available=true' \
  --limit=5 --project=gigaton-platform
```

## 7. Rollback (if anything goes sideways)

Remove the entry from `~/.claude.json`, restart Claude Desktop. Local
FAISS index at `~/.gigaton/local-mind/todd/` is harmless — leave or
`rm -rf` at will. Nothing else on the machine is modified.

## 8. Dogfood-week observations to capture

Write findings to `[[dogfood_week_findings_2026_06_<dd>]]` daily:

- Install friction (numpy<2 pin, spaCy wheel, etc.)
- Cold-start latency on the MiniLM lazy-load (first `embed_chunks` call)
- Memory footprint of the MCP server process at steady-state
- Did any tool error in real chat usage? Capture the exact error.
- Cost-avoided counter — what's the daily $ saved by routing embeds local?
- One thing to fix BEFORE Multipli onboards on 2026-06-10

## 9. After dogfood-week passes

Open onboarding to Multipli (operator #1) per the cohort sequence — see
`[[uaf_phase_c_shipped_2026_05_28]]` for the activation pattern. Each
operator gets their own `~/.gigaton/local-mind/<op>/` dir + their own
`~/.claude.json` entry.

## Cross-refs

- `[[directive_local_mind_buildout_2026_06_01]]` — the parent commitment
- `[[follow_up_local_mind_auth_jwt_vs_proxy_2026_06_02]]` — Phase 2
  auth-upgrade decision
- `[[feedback_pre_retarget_stacked_prs_before_merging_parent]]` — branch
  hygiene
- `[[dogfood_install_local_mind_2026_06_02]]` — sibling memory entry
  (AI quick-reference)
