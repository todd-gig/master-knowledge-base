---
name: mcp-3-decisions-locked-2026-05-26
description: "3 critical MCP decisions LOCKED 2026-05-26 EOD (Todd accepted spec defaults from PR #21): (1) multi-tenant = server-side bearer-token resolution, (2) repo = NEW gigaton-mcp-server Cloud Run service, (3) Claude version default = Sonnet 4.6 with Opus 4.7 surfaced for strategic personas + Haiku 4.5 for batched ops. Unblocks 1-week MCP build."
metadata: 
  node_type: memory
  type: project
  established: 2026-05-26
  status: LOCKED — Todd directive
  scope: gigaton-mcp-server architecture + every consuming surface
  deadline_reference: "2026-06-02 (1-week priority per [[mcp_download_connection_claude_version_1week_priority_2026_05_26]])"
  originSessionId: fc56c866-aa65-41d6-a729-1d21c8fe1dcb
promoted_from: mcp_3_decisions_locked_2026_05_26.md
promoted_at: 2026-06-02T20:13:25Z
---

# 3 MCP decisions LOCKED — 2026-05-26 EOD

## Source

PR #21 `master-knowledge-base/runbooks/2026_05_26_mcp_download_connection_claude_version_1week_spec.md` (~455 lines) surfaced 3 critical decisions. Todd accepted all 3 defaults 2026-05-26 EOD via "Accept all 3 defaults — start building".

## Decision 1 — Multi-tenant enforcement

**LOCKED**: Server-side resolution from bearer token. **NO `operator_id` argument on any MCP tool.**

- **Why**: prevents cross-operator data leakage the day Multipli onboards (Tier-A blocker per [[mcp_multi_tenant_namespace_blocker_2026_05_26]] referenced in PR #21).
- **How to apply**:
  - MCP server validates bearer JWT on every tool call → extracts `operator_id` from `user_claims` (UAE-issued)
  - Server queries UAE for the operator's namespace state → applies tool filters at the server layer
  - Tool input schemas DO NOT include any `operator_id` field — anything that would naïvely accept one is rejected at the FastAPI Pydantic validation layer
  - `X-Operator-Id` header from operator's Claude Code IS ignored on this server (vs gateway middleware which accepts it as fallback) — bearer token only

## Decision 2 — Repo strategy

**LOCKED**: NEW `gigaton-mcp-server` Cloud Run service. Not a mount on `gigaton-gateway`.

- **Why**:
  - Lifecycle independence (MCP server scales + deploys separately from the API gateway)
  - Distinct auth model (operator-bearer-token vs gateway's mixed IAM + session JWT)
  - Aligns with the 9-server doctrine referenced in `[[mcp-master-tool-list-2026-05-26]]` (each MCP server has a single bounded purpose; `gigaton` server exposes platform-wide operator surfaces; future per-entity servers can be spun off similarly)
- **How to apply**:
  - Create GitHub repo `todd-gig/gigaton-mcp-server`
  - Cloud Run service `gigaton-mcp-server` deployed on `gigaton-platform` project
  - Runtime SA: `gigaton-mcp-server-runtime@gigaton-platform.iam.gserviceaccount.com` (NEW; needs IAM grant)
  - Public URL (with auth middleware): `https://gigaton-mcp-server.gigaton-platform.run.app` (or claude.ai-registered connector URL)
  - Copies the `gigaton-memory-server` (at `/Users/admin/Gigaton-UI-Platform/gigaton-memory-server/`) pattern but swaps stdio → HTTP transport + adds the auth middleware

## Decision 3 — Claude version recommendation

**LOCKED**: **Sonnet 4.6 baseline** for new operators. **Opus 4.7 surfaced as upgrade for strategic personas** (CEO/CFO/CTO). **Haiku 4.5 only for batched ops** that explicitly opt in.

- **Why**: avoids cost-shock + capability overhead for first-install operators; most day-to-day operator work doesn't need Opus 4.7's depth; Haiku 4.5 saves cost where speed > depth (e.g. log triage, bulk classification)
- **Model IDs** (verified against current Claude knowledge cutoff Jan 2026):
  - `claude-sonnet-4-6` — DEFAULT
  - `claude-opus-4-7` — strategic personas
  - `claude-haiku-4-5-20251001` — batched ops
- **How to apply**:
  - Operator-facing onboarding (Stage 7+) recommends Sonnet 4.6 + provides override options
  - Settings → Models surface lets operator change the default at any time
  - Persona-engine OrgPersona records can carry `recommended_model` field — strategic personas (CEO/CFO/CTO) seed with Opus 4.7 recommendation; specialist personas (devops, marketing growth, support) seed with Sonnet 4.6
  - Batched-ops tooling (e.g. Wave 2 self-healing variance jobs) call Haiku 4.5 explicitly via tool args
  - Track per-operator model usage in `gigaton-engine` billing module for cost transparency

## Implementation roadmap (per PR #21 spec, ~7 days, ~2,030 LOC)

| Day | Track | LOC | Status |
|---|---|---|---|
| 1-2 | Cloud Run service scaffold (gigaton-memory-server pattern + HTTP + auth middleware) | ~600 | **STARTING NOW** (subagent spawned 2026-05-26 EOD) |
| 2-3 | 8 Wave-1 read-only tools (get_dashboard / list_namespaces / get_current_namespace / list_personas / list_skills + 3 more) | ~400 | queued |
| 3-4 | OAuth handshake (MCP server + UAE `/v1/oauth/mcp/issue` endpoint) | ~450 | queued |
| 5-6 | Install guide + chat-onboarding integration + `/connectors/mcp-claude` UI page | ~380 | queued |
| 6-7 | Bug-fix buffer + Todd-as-first-operator validation | ~200 | queued |

## Cross-references

- [[mcp_download_connection_claude_version_1week_priority_2026_05_26]] — original Todd directive
- PR #21 spec (mkb): `master-knowledge-base/runbooks/2026_05_26_mcp_download_connection_claude_version_1week_spec.md`
- [[universal_connector_hub_architecture]] — the architecture this enables
- [[user_facing_capabilities_2026_05_19]] — current pre-MCP operator-facing surface
- [[operator_runbook_2026_05_19]] — current operator ops playbook (will gain MCP install steps in Day 5-6)
- Existing `gigaton-memory-server` at `/Users/admin/Gigaton-UI-Platform/gigaton-memory-server/` — Day 1-2 scaffold copies its pattern
