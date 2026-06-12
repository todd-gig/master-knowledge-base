---
title: MCP Download + Connection + Claude Version — 1-Week Implementation Spec
established: 2026-05-26
deadline: 2026-06-02
status: SPEC — awaiting Todd ratification
priority: HIGH (per [[mcp_download_connection_claude_version_1week_priority_2026_05_26]])
authors: Claude Opus 4.7 (research subagent)
supersedes: none
unblocks: Wave 2 operator self-serve onboarding + cross-operator Ti Agent Matrix
ppim_signature: surface.spec.mcp_distribution.v1
---

# MCP Download + Connection + Claude Version — 1-Week Implementation Spec

> **Scope-only document.** No code authored. This spec maps the gap between today's `gigaton-memory` single-server reality and a productized "operators install Claude + connect to Gigaton MCP" flow. Per the priority memory ([[mcp_download_connection_claude_version_1week_priority_2026_05_26]]), the runway is 1 week (deadline ~2026-06-02). The output of this PR is the basis for Todd's go/no-go + decision ratification before any code spawns.

---

## 0. Glossary (quick decoder)

- **MCP** — Model Context Protocol (Anthropic's open spec for tool-server integration)
- **stdio transport** — local process pipe (today's `gigaton-memory` default)
- **HTTP transport** — remote/network MCP server (needed for cloud-hosted gigaton servers)
- **Connector** — what claude.ai's web/desktop UI calls a registered MCP server (Slack, Notion, etc.)
- **Connector UUID** — the identifier Anthropic assigns when an MCP server is registered in the claude.ai connector dashboard
- **Operator** — a Gigaton tenant (carmen-beach, liquefex, incontekst, multipli, etc.)
- **Namespace** — the multi-tenant boundary key (`X-Client-Namespace` header in gateway calls)

---

## 1. Scope decomposition

Todd's 3-part directive (paraphrased from [[mcp_download_connection_claude_version_1week_priority_2026_05_26]]):

> "understand the MCP download > connection + claude version is super important in enabling system capabilities and its a short term requirement to complete within a week to enable significant additional functionalities"

Decomposes into three concrete tracks:

### 1.1 Download — "how does an operator get an MCP-capable Claude on their machine?"

Deliverable: a single linkable operator-facing install page covering:

- **Claude Desktop** (recommended default for non-developer operators) — direct download link to https://claude.ai/download for macOS / Windows / Linux
- **Claude Code** (recommended for technical operators) — `npm install -g @anthropic-ai/claude-code` or `brew install claude` install path
- **Per-OS prerequisites** (Node ≥18 for Claude Code; nothing for Desktop)
- **One-paragraph "which should I install?"** decision tree, mirroring the persona split in §5 below

This page is the entry point that the chat-onboarding orchestrator (per [[onboarding_v1_manifest_verified_2026_05_25]]) will link to from a new Stage 7-or-8 step.

### 1.2 Connection — "how does an operator connect their installed Claude to Gigaton?"

Deliverable: documented + tested handshake covering:

- **For Claude Desktop**: copy-paste `claude_desktop_config.json` snippet (pattern already proven by `/Users/admin/Gigaton-UI-Platform/gigaton-memory-server/claude_desktop_config_snippet.json:1-12`)
- **For Claude Code**: equivalent `~/.claude.json` `mcpServers` block (pattern already live for Todd, per `jq '.mcpServers' /Users/admin/.claude.json`)
- **For claude.ai (web)**: Todd-registered "Gigaton" connector entry in the Anthropic connector dashboard — operators click "Add Gigaton" + complete OAuth, mirroring how Slack/Notion/Drive land in their session

The connection flow must inject the operator's `X-Client-Namespace` so multi-tenant isolation holds from the first call. See §3 Gap and §7 Decision #2 — this is the single biggest open question and **must be resolved before code lands**.

### 1.3 Claude version recommendation — "which model + version per operator role?"

Deliverable: a recommendation matrix (see §5) surfaced in two places:

- **Onboarding chat** — when an operator reaches the "install Claude" stage, the orchestrator suggests a model based on their declared role (per `onboarding_v1.yaml` Stage 2 People + Stage 6 Org Processes outputs)
- **Settings → AI Models** in `gigaton-ui-system` — a static recommendation card per role with rationale + cost note

Current models (as of 2026-05-26 per this session's powering model):

- `claude-opus-4-7` (Opus 4.7) — strategic / CEO / CFO use cases
- `claude-sonnet-4-6` (Sonnet 4.6) — default for day-to-day operator chat
- `claude-haiku-4-5-20251001` (Haiku 4.5) — high-volume batched ops

---

## 2. Current state survey (what exists today)

### 2.1 Live MCP servers in the ecosystem

**Built + wired** (verified 2026-05-26):

- **`gigaton-memory`** — single MCP server in production. Source at `/Users/admin/Gigaton-UI-Platform/gigaton-memory-server/`. Tools at `src/gigaton_memory_server/server.py:123-298` (8 tools registered via `@mcp.tool()` decorator). Wired into Todd's Claude Code via `~/.claude.json` `mcpServers.gigaton-memory` entry. Backs the Obsidian vault at `/Users/admin/Documents/Obsidian Vault/Gigaton/`. **Single-operator (Todd's vault).** Not multi-tenant.
- Tools observed in this Claude session as deferred-tool names: `mcp__gigaton-memory__add_decision`, `add_memory`, `diff_since`, `get_dashboard`, `get_master_plan`, `list_open_loops`, `list_sources`, `search_memory` — confirmed 8/8 match the server.py registry.

**Scaffolded but not yet live**:

- **`gignet-local-node`** — `/Users/admin/Documents/GitHub/gignet-local-node/node/mcp_server.py:91-152`. Skeleton with handler registry for Tier 0-2 tools (`node.*`, `fs.*`, `slm.*`); the actual MCP SDK serve loop is TODO (line 147 explicit). This is the user-installed peer concept; would run on the operator's machine on `127.0.0.1:7180`. mTLS-bound to platform. **Different scope** from "Gigaton-hosted MCP" — this is for local file/SLM access; the operator-Gigaton connection is the cloud-hosted side.
- **`mcp-sie`** at `/Users/admin/Documents/GitHub/Gigaton-UI-Platform/mcp-sie/` — directory exists but only `README.md`, `requirements.txt`, `server.py` present. Per directory listing — not investigated further this pass; flag as known-existing artifact.

**Spec'd but not built** (per `/Users/admin/Documents/Obsidian Vault/Gigaton/memory/architecture/mcp-master-tool-list-2026-05-26.md`):

8 additional servers: `gigaton-decision`, `gigaton-connectors`, `gigaton-ingest`, `gigaton-orchestrator`, `gigaton-onboarding`, `gigaton-arts`, `gigaton-clickup-phase`, `gigaton-billing-cost`. ~62 additional tools. **All Wave 2/3 — outside this 1-week window.**

### 2.2 MCP infrastructure elsewhere in repos

Searched: `gigaton-gateway`, `user-access-engine`, `intelligence-silo`, `decision-engine`, `persona-engine`, `gigaton-ui-system`.

- **No FastMCP / `@mcp.tool` / `mcp.server` imports** found in any of the 6 core engines. Confirmed via `grep -rl "FastMCP\|@mcp.tool" /Users/admin/Documents/GitHub/gigaton-gateway /Users/admin/Documents/GitHub/intelligence-silo` (returned empty).
- Only references to "mcp" in those repos are coincidental matches in alembic migration names (`0011_seed_multipli_overlay.py`, `0013_seed_cbp_overlay.py`) and the `decision-engine/drift_sentinel/gigmcp_analysis/` directory (the "gigmcp" string is the Gigaton MCP industry analysis tool, unrelated to Model Context Protocol).
- **`master-knowledge-base/gigmcp/`** directory exists — also the analysis-tool gigmcp, not an MCP server.

**Conclusion**: today, MCP-server code lives in exactly TWO places: `gigaton-memory-server/` (production) and `gignet-local-node/` (skeleton). The 6 core engines have no MCP surface; everything operators consume from them goes through HTTP at the gateway.

### 2.3 What operators do today (pre-MCP-distribution era)

Per [[user_facing_capabilities_2026_05_19]] + [[operator_runbook_2026_05_19]]:

- Operators log into `gigaton-platform.web.app` with Google OAuth (per `operator_runbook_2026_05_19.md:204-211`)
- They use the web UI (`/chat`, `/dashboard`, `/connectors`, `/sources`) for everything
- No operator besides Todd has Claude Desktop or Claude Code wired to any Gigaton server
- All "AI" the operator interacts with is mediated through the web app (which itself calls Anthropic API server-side from `gigaton-ui-system` or relevant engine)

**There is no operator-installable Gigaton MCP today.** This spec is the bridge.

### 2.4 Claude.ai connector pattern (existing, observed in this session)

This Claude session has 11 connectors visible in the deferred-tool registry (per system reminder above). Each follows the pattern:

```
connector_uuid: <UUID>
name: <Display Name>          # e.g. "ClickUp", "Slack", "Notion"
url: <Cloud-hosted MCP server URL>
auth: OAuth2 (Todd authorized at connector-add time)
tools: mcp__claude_ai_<Name>__<tool_name>
```

Observed connector slugs in this session's deferred-tool list: `Apollo_io`, `Clay`, `ClickUp`, `Cloudflare_Developer_Platform`, `Gmail`, `Google_Calendar`, `Google_Drive`, `Indeed`, `Intercom`, `Mermaid_Chart`, `Notion`, `Outreach`, `Slack`, `Vibe_Prospecting`.

**A "Gigaton" connector would slot into this exact same dashboard**, with its own UUID, OAuth flow, and tool prefix `mcp__claude_ai_Gigaton__<tool_name>`. Todd's existing connector registrations are the proof-of-pattern.

---

## 3. Gap analysis (operator end-to-end flow)

Five gates, walking through what a hypothetical Multipli operator needs to do tomorrow:

| # | Gate | Current state | Gap to close |
|---|---|---|---|
| 1 | **Discover** Gigaton has an MCP server | Nothing on `/connectors` or in onboarding chat mentions MCP | Add Stage 7-or-8 step + `/connectors/mcp-claude` page in gigaton-ui-system |
| 2 | **Install** Claude Code or Desktop | No operator-facing install link | Write 1-page install guide (per §1.1) |
| 3 | **Authenticate** as an authorized operator | `gigaton-memory` has no auth (stdio, local). The web/cloud connector pattern uses OAuth — we have UAE OAuth but it's not wired to MCP yet | Stand up MCP-server-side OAuth handshake delegating to UAE `/v1/oauth/google/*` |
| 4 | **Authorize** scopes per operator | UAE has the capabilities catalog (per `_DEFAULT_CATALOG` in `user-access-engine/api/services/access.py`) but no MCP tool maps to it | Add per-MCP-tool scope tags + UAE permission check at server invocation |
| 5 | **Use** Gigaton tools from Claude | Only Todd's vault-scoped 8 tools work; no multi-tenant tool exposes any actual Gigaton platform data | Build minimum-viable 5-8 Gigaton platform tools (see §4.2) |

**Single hardest gap: #4 + #5 together** (namespace isolation). See [[mcp_multi_tenant_namespace_blocker_2026_05_26]] — flagged as Tier-A blocker. **Must resolve before any tool that returns operator-scoped data ships.**

---

## 4. Architecture proposal

### 4.1 Server location — extend gigaton-gateway vs new repo?

**Recommendation: NEW REPO `gigaton-mcp-server`**, deployed as a Cloud Run service in `gigaton-platform` project.

Rationale:

1. **Lifecycle independence** — MCP server iterates fast in Wave 1; gateway is stable. Coupling slows both.
2. **Distinct auth model** — MCP uses bearer tokens + OAuth-with-resource-server flow; gateway uses session JWTs. Mixing creates middleware ambiguity.
3. **Pattern proven** — `gigaton-memory-server` is already a standalone Python package; the cloud variant copies the FastMCP shape but with HTTP transport + auth middleware. Lift-and-shift.
4. **Pre-existing precedent** — per `[[mcp-master-tool-list-2026-05-26]]` §3, the doctrine is 9 separate servers (one per concern), not one monolithic gateway-mounted server.

**Trade-off accepted**: one more Cloud Run service to manage. Mitigated by reusing the gigaton-platform SA + secret patterns.

**Future**: Wave 2/3 servers (`gigaton-decision`, `gigaton-connectors`, etc.) follow the same Cloud Run pattern; each can be its own service. Or — if op cost is a concern — they can co-exist as separate `FastMCP` mounts on a single multi-protocol process. **Defer this decision** until Wave 2.

### 4.2 Minimum-viable Wave 1 tool surface

5-8 tools, all read-only, all operator-scoped via `X-Client-Namespace`:

| Tool | Backing | Read/Write | Rationale |
|---|---|---|---|
| `get_dashboard` | `decision-engine /v1/penrose/scoreboard` (per `[[user_facing_capabilities_2026_05_19]]` §6) | R | Operator's first "is my biz healthy?" check |
| `list_namespaces` | `user-access-engine /v1/namespaces` (live per `[[operator_runbook_2026_05_19]]` §D) | R | Which operator am I scoped to? |
| `get_current_namespace` | UAE `/v1/namespaces/{namespace_id}` | R | Resolve operator metadata for the active session |
| `list_personas` | `persona-engine /v1/personas` (presumed live) | R | Show available personas / brand voices |
| `list_skills` | gateway `/v1/access/check` capabilities endpoint | R | Operator's available capabilities |
| `get_onboarding_state` | gateway `/v1/onboarding/state` (LIVE per `[[onboarding_v1_manifest_verified_2026_05_25]]`) | R | "Where am I in onboarding?" inside Claude |
| `list_open_loops` (operator-scoped) | mirror of vault tool, but reads from operator's L2 memory store | R | "What's pending for me?" |
| `search_memory` (operator-scoped) | intel-silo `/memory/search` (live per `[[user_facing_capabilities_2026_05_19]]` §2 Source Registry) | R | First semantic search over operator's own ingested docs |

**NO writes in Wave 1.** Per `gigaton-memory-server/README.md:148` ("read-mostly, append-rarely") doctrine and Tier-B Open Question #5 in `[[mcp-master-tool-list-2026-05-26]]` (write-tool concurrency). Writes are Wave 2.

### 4.3 Auth flow

```
Operator (Claude Code or Desktop)
      │
      │ 1. Operator adds Gigaton connector (via claude.ai dashboard, one-time)
      │    → Claude initiates OAuth: redirect to https://mcp.gigaton.ai/oauth/authorize
      │
      ▼
gigaton-mcp-server (Cloud Run, in gigaton-platform project)
      │
      │ 2. /oauth/authorize → 302 to UAE /v1/oauth/google/login
      │    (with state=<mcp-callback-token>)
      │
      ▼
user-access-engine
      │
      │ 3. Google OAuth roundtrip (operator consents)
      │    → UAE issues JWT (existing flow per operator_runbook §3)
      │    → UAE 302s back to mcp-server /oauth/callback with state + jwt
      │
      ▼
gigaton-mcp-server
      │
      │ 4. Exchanges JWT → MCP bearer token (scoped: operator_id, capabilities)
      │    Returns bearer to Claude → Claude stores per-connector
      │
      ▼
[Every subsequent MCP tool call from Claude]
      │
      │ 5. Claude sends: Authorization: Bearer <mcp-token>
      │    Server validates → resolves operator_id → injects X-Client-Namespace
      │    on every downstream gateway call
      │
      ▼
gigaton-gateway → engine (decision, intel, UAE, etc.)
```

**Per-operator scoping**: server-side resolution from the bearer token. Tools do NOT take `operator_id` as an argument. This closes the [[mcp_multi_tenant_namespace_blocker_2026_05_26]] Tier-A gap by construction — the operator cannot ask for someone else's data because they cannot specify a target.

### 4.4 Connector registration in claude.ai dashboard

One-time Todd action (~5 min):

1. Visit https://claude.ai/settings/connectors (or equivalent admin UI)
2. Click "Add custom connector"
3. Fill in: Name = "Gigaton", URL = `https://mcp.gigaton.ai`, OAuth endpoints (authorize + token + callback)
4. Anthropic assigns a connector_uuid; Todd records in `[[mcp-master-tool-list-2026-05-26]]` §3 server-A row
5. Connector becomes available in every Claude session under "Add Gigaton connector" in the UI
6. Per-operator OAuth happens at first-use per session (Step 1-4 of §4.3)

### 4.5 Transport choice

- **stdio**: NOT for Wave 1 multi-tenant. stdio = local-only, no auth model. (`gigaton-memory` uses stdio for Todd because vault is local.)
- **HTTP (SSE-based streaming, Anthropic's MCP HTTP transport)**: YES. This is what cloud-hosted MCP servers use; matches the claude.ai-connector pattern; supports OAuth.
- **Mount under api.gigaton.ai/mcp/* vs dedicated mcp.gigaton.ai subdomain**: dedicated `mcp.gigaton.ai` recommended for cert + CORS clarity, and matches the operator-runbook §0 pattern of distinct hostnames per surface.

---

## 5. Claude version recommendation matrix

| Operator role | Recommended model | Model ID | Rationale | Cost note |
|---|---|---|---|---|
| **CEO / Strategic decision-maker** | Opus 4.7 | `claude-opus-4-7` | Deep reasoning on complex multi-variable decisions; founder/CFO/board-level analysis; tradeoff exploration | Highest per-token; offset by sparing usage |
| **Operator (day-to-day)** | Sonnet 4.6 | `claude-sonnet-4-6` | Strong general capability + balanced cost. Default for everything that isn't strategic or batched | Mid-tier; recommended baseline |
| **Customer-facing / chat-volume / batched** | Haiku 4.5 | `claude-haiku-4-5-20251001` | Fast, cheap, sufficient for templated/structured tasks. Powers high-volume support, message drafting, classification | Lowest; ~5-10x cheaper than Sonnet |
| **Code authoring** | Opus 4.7 (1M context) | `claude-opus-4-7` | Long-context refactoring + spec writing. Falls back to Sonnet for narrow tasks | Highest; constrain to PR-scale work |

### 5.1 Where to surface

- **Onboarding chat (Stage 7 or 8 — TBD with Todd)**: when operator reaches the "install Claude" step, the orchestrator asks "what's your primary role?" + recommends matching model
- **`gigaton-ui-system /settings/ai-models`**: static recommendation card per role with link to model docs + "set as default" button (this stores operator preference; future MCP tools can read it via UAE)
- **`/connectors/mcp-claude` page** (new): the install + connect + model-pick flow in one place

### 5.2 Anti-recommendations

- **Do not recommend Opus to brand-new operators** — cost shock + capability overhead. Sonnet 4.6 is the friendlier "first install" suggestion; let them upgrade after observing usage patterns.
- **Do not recommend Haiku for first-time setup** — onboarding has multi-step reasoning; Haiku can struggle. Reserve for post-onboarding batched ops.
- **Do not advertise "any model works"** — operators with no LLM background interpret that as "ChatGPT-4 is fine"; opinionated default reduces support burden.

---

## 6. Implementation roadmap (7 days)

Constraints:
- Per [[mcp_multi_tenant_namespace_blocker_2026_05_26]], namespace decision MUST be ratified before code writes start (Day 0).
- Per [[migration_is_value_blocking_2026_05_25]] (if still in force), GCP migration may be in flight — confirm before deploys.
- 1 person-week assumed; ~2h/day operator-attended for Todd actions (OAuth client creation, connector registration).

### Day 0 — Decision ratification (Todd, ~1 hr)

- Todd reviews this spec + answers §7 decisions
- Todd confirms `gigaton-platform` GCP project + `mcp.gigaton.ai` DNS available
- **Output**: 5 decisions in [[mcp_download_connection_claude_version_1week_priority_2026_05_26]]

### Day 1-2 — Stand up `gigaton-mcp-server` repo + Cloud Run

- **Scope**: new GitHub repo `todd-gig/gigaton-mcp-server`. Copy `gigaton-memory-server/` scaffold; replace stdio with HTTP transport; add FastAPI middleware for bearer-token validation
- **Repo**: NEW `gigaton-mcp-server`
- **Est. LOC**: ~600 (300 server core + 200 auth middleware + 100 Cloud Run + Dockerfile + cloudbuild.yaml)
- **Blocking on**: Day 0 decisions; `mcp.gigaton.ai` DNS in Cloudflare
- **Deploy**: `gcloud run deploy gigaton-mcp-server --source . --region us-central1 --project gigaton-platform --allow-unauthenticated --service-account=mcp-server-runtime@gigaton-platform.iam.gserviceaccount.com`
- **Smoke**: `curl https://mcp.gigaton.ai/health` returns 200

### Day 2-3 — Implement Wave 1 tools (5-8)

- **Scope**: 8 tools from §4.2; each is a thin proxy to existing engine HTTP endpoint with `X-Client-Namespace` injection from bearer token
- **Repo**: `gigaton-mcp-server`
- **Est. LOC**: ~400 (50 per tool × 8 tools)
- **Blocking on**: Day 1-2 deploy; engines reachable from gigaton-platform project
- **Deploy**: same as Day 1-2 (rebuild + redeploy)
- **Smoke**: each tool callable via `curl -H "Authorization: Bearer <test-token>"` returning expected JSON for `carmen-beach` operator

### Day 3-4 — OAuth handshake (UAE ↔ MCP server)

- **Scope**: implement §4.3 flow end-to-end. New endpoints in `gigaton-mcp-server`: `/oauth/authorize`, `/oauth/callback`, `/oauth/token`. New endpoint in `user-access-engine`: `/v1/oauth/mcp/issue` to mint MCP-scoped bearer tokens from a UAE JWT
- **Repos**: `gigaton-mcp-server` (~300 LOC) + `user-access-engine` (~150 LOC)
- **Est. LOC**: ~450 + tests
- **Blocking on**: Day 1-3; UAE `/v1/oauth/google/*` must be live (confirmed per `[[operator_runbook_2026_05_19]]` §3)
- **Deploy**: rebuild MCP server + redeploy UAE (`gcloud run deploy user-access-engine`)
- **Smoke**: end-to-end browser flow: hit `https://mcp.gigaton.ai/oauth/authorize` → land at Google consent → return to MCP with bearer

### Day 4-5 — Claude.ai connector registration + first end-to-end test

- **Scope**: Todd registers "Gigaton" custom connector in claude.ai dashboard (§4.4); records connector_uuid in vault. Todd opens a fresh Claude.ai session, adds the connector, completes OAuth, calls `get_dashboard` — verifies returned data is scoped to his operator
- **Repo**: doc-only; update `connected-sources.md` in vault
- **Est. LOC**: 0 code; ~50 lines doc
- **Blocking on**: Day 4 deploys live + `mcp.gigaton.ai` cert valid
- **Smoke**: visible in Claude session as `mcp__claude_ai_Gigaton__get_dashboard` etc.

### Day 5-6 — Operator-facing install guide + onboarding chat step

- **Scope**: write the install page (per §1.1) at `master-knowledge-base/docs/operator/install-claude-mcp.md`; add a new chat affordance to `onboarding_v1.yaml` Stage 7 or 8 (TBD with Todd) that links operators to the install page + connector registration link + recommends model per §5
- **Repos**: `master-knowledge-base` (~200 lines doc) + `master-knowledge-base/manifests/onboarding_v1.yaml` (~30 lines YAML) + `gigaton-ui-system` (~150 LOC new page at `/connectors/mcp-claude`)
- **Est. LOC**: ~380
- **Blocking on**: Day 4-5 first end-to-end working
- **Deploy**: `firebase deploy --only hosting` for UI; commit + push for docs
- **Smoke**: open `/connectors` as a fresh operator, see the new "Claude MCP" card, click through

### Day 6-7 — Todd-as-first-operator validation + handoff

- **Scope**: Todd runs the entire onboarding flow as if he were a brand-new operator. Walks the install path, registers the connector in a NEW claude.ai account (or "incognito" mode), verifies tools, sets model preference, files any bugs as separate PRs
- **Repo**: bug-fix PRs in whichever repo surfaces issues
- **Est. LOC**: TBD (target: <200 across all fixes)
- **Blocking on**: Day 5-6 complete
- **Smoke**: a non-Todd Claude session, with the connector added, can list dashboards + namespaces for the operator who logged in

**Total estimated LOC across 7 days**: ~2,030 (server: 600 + tools: 400 + OAuth: 450 + docs+UI: 380 + bug-fix buffer: 200).

---

## 7. Decisions Todd needs to make (Day 0)

Before any code spawns, ratify these:

### Decision 1 — Repo strategy: new `gigaton-mcp-server` vs extend `gigaton-gateway`?

- **Spec recommends**: NEW repo `gigaton-mcp-server` (per §4.1 rationale)
- **Alternative**: mount under `gigaton-gateway` at `/mcp/*` path
- **If you defer**: I'll proceed with NEW repo on Day 1; reversible via `git mv` if you flip later

### Decision 2 — Multi-tenant namespace enforcement model (Tier-A blocker)

Per [[mcp_multi_tenant_namespace_blocker_2026_05_26]], three options:

- **(a)** Every tool takes explicit `operator_id` arg, validated against caller identity server-side
- **(b)** Server resolves `operator_id` from bearer token; ignores client-supplied  ← **spec recommends**
- **(c)** Hybrid: reads use (b); writes use (a) with double-check

**Spec recommends (b)** — closes the leak by construction; aligns with [[namespace_middleware_silent_400_audit_2026_05_25]]'s "server-side enforcement is the only safe default" finding.

### Decision 3 — OAuth scopes: which Gigaton ops are operator-controllable vs admin-only?

- **Spec recommends Wave 1**: ALL 8 read tools scoped to `mcp.gigaton.read` (single scope); no admin tools in Wave 1
- **Alternative**: per-tool scopes (`mcp.gigaton.dashboard.read`, `mcp.gigaton.namespaces.read`, etc.) — more granular, more setup
- **Wave 2+**: separate `mcp.gigaton.write` + admin scopes for `create_operator`, `acknowledge_axiom`, etc.

### Decision 4 — Claude version default

- **Spec recommends**: Sonnet 4.6 (`claude-sonnet-4-6`) as the default onboarding suggestion (per §5)
- **Alternative**: Sonnet for non-CEO; Opus for CEO from the start
- **If you defer**: Sonnet 4.6 baseline gets shipped; per-role variants land in Wave 2

### Decision 5 — Pricing / billing implications

- **Question**: Does the operator pay Anthropic directly (BYO Claude API key), or does Gigaton bundle Claude usage into the platform price?
- **Spec recommends Wave 1**: BYO Claude. Operator installs Claude Desktop/Code with their own Anthropic subscription. Gigaton's MCP server is free-tier (Gigaton pays for Cloud Run compute, ~$5-15/month at Wave 1 volumes). No billing complexity in Week 1.
- **Wave 2+ option**: Gigaton-managed Anthropic keys + add markup to operator monthly fee; requires Stripe integration + per-operator usage attribution. Defer.

### Decision 6 — Connector_uuid assignment

- **Action item**: Todd registers the connector in https://claude.ai/settings/connectors (~5 min, Day 4)
- **Pre-requisite**: `mcp.gigaton.ai` DNS + cert valid (Day 1-2 deliverable)
- **No engineering blocker**: Todd does this single action when prompted on Day 4

---

## 8. Risks + open questions

### Risks

1. **Multi-tenant data leak during Wave 1** — if Decision 2 doesn't ratify (b), any tool that returns operator-scoped data risks cross-tenant exposure once a 2nd operator onboards. **Mitigation**: hold launch until Decision 2 ratified.
2. **Anthropic MCP HTTP transport spec instability** — the spec is evolving; what works today may break in 90 days. **Mitigation**: pin Anthropic SDK versions; subscribe to MCP changelog; budget Wave-2 capacity for protocol updates.
3. **`mcp.gigaton.ai` cert provisioning delay** — Cloudflare DNS verification can take hours. **Mitigation**: start DNS setup on Day 0 in parallel with code (not blocking).
4. **OAuth scope creep in Claude Desktop** — Anthropic may require additional scopes or consent UX changes between when this spec ships and when the connector goes live. **Mitigation**: design for the minimum scope first; iterate.
5. **Operator confusion: "which Claude do I install?"** — Desktop vs Code vs claude.ai web are 3 separate products. **Mitigation**: opinionated default in §1.1 (Desktop for non-devs, Code for devs); link to single install page.
6. **Onboarding chat manifest version conflict** — adding a Stage 7-or-8 step requires a manifest version bump + UAE migration. Per [[uae_migration_0007_parked_for_5_27_sprint]] there's already an open migration in the queue. **Mitigation**: stage the chat-step add into the existing 0007 migration window OR introduce as a new 0008 migration during the 5/27 sprint Day-0.

### Open questions (not blocking Day 0)

- **Where does the operator's Claude bearer token live?** Claude Desktop stores per-connector tokens encrypted at rest; Claude Code stores in `~/.claude.json`. Verify Anthropic's storage model matches our compliance posture (likely yes, but document).
- **How do we handle the case where an operator has multiple namespaces?** Wave 1: bearer is scoped to ONE namespace at connection time; multi-namespace operators add the connector multiple times with different OAuth identities. Wave 2: implement a `set_active_namespace(namespace_id)` tool + bearer re-issue.
- **MCP-server observability**: do we emit Penrose-relevant telemetry for tool calls? Recommend logging per-call latency + bearer-resolved operator_id to a new `mcp_tool_call` table in intel-silo (Wave 2).
- **Rate limits per operator**: gateway has `operator_quotas.yaml` (per `[[operator_runbook_2026_05_19]]` §2 Step 3). The MCP server should respect these by passing through to the gateway. Verify the gateway returns rate-limit headers; if not, add (Wave 2).
- **Audit trail**: per [[mcp_session_to_l2_promotion]], session-discovered content needs explicit operator promotion to L2 memory. Wave 1 doesn't write to memory, so no immediate concern, but worth flagging for Wave 2 write tools.
- **gignet-local-node interaction**: the local-node skeleton at `/Users/admin/Documents/GitHub/gignet-local-node/` is a SEPARATE concern (operator's local files + SLM). NOT in this 1-week scope. Flag for explicit future spec covering how local-node + gigaton-mcp-server compose.
- **Wave-2 server collision risk**: per [[mcp-master-tool-list-2026-05-26]] §5 build order, Wave 2 adds 4 more servers. If each is a separate Cloud Run service, naming clashes are unlikely; if mounted under one process, namespace collisions need a per-server FastMCP prefix. **Decide at Wave-2 kickoff**, not now.

---

## 9. Test plan (for the PR that ships the implementation)

When Wave 1 implementation PRs come in over Days 1-7, each should include:

- [ ] **Unit**: each tool's happy path + 404 + 403 + 500 fallbacks
- [ ] **Integration**: end-to-end OAuth flow against staging UAE
- [ ] **Multi-tenant smoke**: 2 operators (carmen-beach + a synthetic second op) — verify tool calls return ONLY the caller's data
- [ ] **Browser smoke**: register Gigaton connector in a clean claude.ai session; call `get_dashboard`; verify response shape matches OpenAPI
- [ ] **Claude Desktop smoke**: paste config snippet into `claude_desktop_config.json`; restart Desktop; verify tools appear in picker
- [ ] **Claude Code smoke**: add to `~/.claude.json`; restart Code; verify `mcp__gigaton__*` tools deferred-loadable
- [ ] **Rollback test**: stop MCP server → confirm Claude reports "MCP server unavailable" gracefully (no Claude crash)

---

## 10. Cross-references

- **Priority memory**: `/Users/admin/.claude/projects/-Users-admin/memory/mcp_download_connection_claude_version_1week_priority_2026_05_26.md` — the 1-week directive
- **Tier-A blocker memory**: `/Users/admin/.claude/projects/-Users-admin/memory/mcp_multi_tenant_namespace_blocker_2026_05_26.md` — namespace enforcement
- **Canonical tool list**: `/Users/admin/Documents/Obsidian Vault/Gigaton/memory/architecture/mcp-master-tool-list-2026-05-26.md` — ~70 future tools across 9 servers; Wave 1/2/3 ordering
- **Architecture doctrine**: `[[universal_connector_hub_architecture]]` — Gigaton IS the universal connector hub; this MCP server is the operator-facing surface of that doctrine
- **Existing MCP server**: `/Users/admin/Gigaton-UI-Platform/gigaton-memory-server/` — pattern + scaffold to copy
- **Existing MCP skeleton**: `/Users/admin/Documents/GitHub/gignet-local-node/node/mcp_server.py:91` — different scope (local-node) but useful for tier-gating patterns
- **Onboarding manifest**: `master-knowledge-base/manifests/onboarding_v1.yaml` — where the Stage 7-or-8 step lands
- **Operator runbook**: `[[operator_runbook_2026_05_19]]` §3 — current onboarding pattern this builds on
- **User-facing capabilities**: `[[user_facing_capabilities_2026_05_19]]` — pre-MCP-distribution state of operator capabilities

---

## 11. PPIM signature footer

```yaml
ppim_signature:
  surface: spec.runbook.mcp_distribution
  doctrine_alignment:
    - foundational_goal_gigaton_engineered_brand_experience  # MCP is operator-facing surface; PPIM compliance via per-tool scope tagging
    - foundational_modular_replication_via_input_substitution  # every tool serves N operators by swapping bearer-resolved namespace
    - universal_connector_hub_architecture                    # MCP server IS the universal connector hub for AI agents
    - feedback_always_build_user_self_serve                   # operator-driven install + connect, no Todd-side ticket
    - feedback_connection_states_must_be_explicit             # explicit "Gigaton MCP connected" state, no implicit "I think it's wired"
  brand_dimensions_touched:
    - responsiveness   # operator-installable, ~1-week to value
    - quality          # opinionated install/model defaults
    - personalization  # per-operator namespace + per-role model recommendation
  economics:
    cost_estimate_usd_month: 5-15  # Cloud Run idle + sparse-traffic Wave 1
    revenue_unlock_path: "operator self-serve onboarding accelerates beta cohort #1-#3 activation; unblocks Ti Agent Matrix"
  drift_risks:
    - namespace_leak_if_decision_2_chooses_option_a_without_validation
    - protocol_version_drift_when_anthropic_updates_mcp_http_spec
```

---

*Spec authored 2026-05-26 by Claude Opus 4.7 as research+spec subagent under the SDK harness. No code authored; no engine repos touched. Ratification + implementation gating with Todd.*
