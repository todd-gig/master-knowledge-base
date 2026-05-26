# Wave 2 Week 1 #5 — CTO Pilot Smoke Results

**Date**: 2026-05-26
**Goal**: Validate that the 4 PRs shipped today actually compose into a working Ti Agent Matrix CTO routing circuit.
**Verdict**: **YELLOW** — circuit primitives exist + middleware proven, but the routing keyword map has zero "cto" rules and persona seed never ran (load_seed not auto-invoked on container boot), so end-to-end Tier-5 CTO routing produces a NULL persona today.

## PRs Validated

1. [decision-engine PR #85](https://github.com/todd-gig/decision-engine/pull/85) — stub `POST /v1/intelligence/classify`
2. [persona-engine PR #12](https://github.com/todd-gig/persona-engine/pull/12) — 9 executive OrgPersonas (CEO/CTO/CXOO/CISO/CDO/CFO/CMO/CRO/CPO)
3. [intelligence-silo PR #41](https://github.com/todd-gig/intelligence-silo/pull/41) — `agent_roles` + `skill_vectors` tables (migration 033)
4. [gigaton-gateway PR #57](https://github.com/todd-gig/gigaton-gateway/pull/57) — PPIM `attribution_chain` + license-check middleware

## Deploy state at smoke start

All 3 GHA pipelines confirmed `completed/success` before tests began:

| Repo | Run ID | Status | Latest revision |
|---|---|---|---|
| intelligence-silo | 26462693573 | success | `intelligence-silo-00038-w6w` (carmen-beach-properties) |
| decision-engine | 26462728799 | success | `decision-engine-00041-7mc` (carmen-beach-properties) |
| persona-engine | 26462866600 | success | `persona-engine-00008-qgl` (gigaton-platform) |

**Routing context** (per [[migration_is_value_blocking_2026_05_25]]): gateway routes `decision-engine` and `intelligence-silo` to the **carmen-beach-properties** project (URL hash `rjmcrtvuzq`) but `persona-engine` to **gigaton-platform** (`sqatlxhlza`). Migration session 1 already moved decision-engine; sessions 2 & 3 are still pending.

---

## Step 1 — Gateway healthz (11/11 expected)

```bash
curl -sS https://gigaton-platform.web.app/v1/healthz | jq '.aggregate_status, .ok_count, .total_count'
```

**Response:**
```json
"ok"
11
11
```

**Verdict:** PASS. (Note: an earlier read parsed jq on multi-arg form and looked degraded; on re-check with explicit `.total_count` it is 11/11 ok.)

---

## Step 2 — `/v1/intelligence/classify` x 5 CTO-ish intents

Gateway has NO `/v1/intelligence/classify` route registered in the routing-table aggregator yet (returns `404 Not Found` from Firebase static layer with `x-ppim-chain` set by middleware). Hit decision-engine directly at the URL the gateway healthz already proves is reachable.

```bash
TOKEN=$(gcloud auth print-identity-token)
for INTENT in \
  "evaluate Kubernetes vs ECS for compute layer" \
  "set the 90-day infra security roadmap" \
  "should we adopt Postgres logical replication for the migration" \
  "redesign the CI pipeline to cut deploy time in half" \
  "evaluate observability stack: Datadog vs Grafana Cloud"; do
  curl -sS -X POST https://decision-engine-rjmcrtvuzq-uc.a.run.app/v1/intelligence/classify \
    -H 'Content-Type: application/json' \
    -H "Authorization: Bearer $TOKEN" \
    -d "{\"intent_text\":\"$INTENT\",\"operator_id\":\"op_smoke\"}"
done
```

| # | Intent | HTTP | primary_role_key | conf | stub |
|---|---|---|---|---|---|
| 1 | evaluate Kubernetes vs ECS for compute layer | 200 | `specialist_devops_engineer` | 0.82 | true |
| 2 | set the 90-day infra security roadmap | 200 | `executive_ciso` | 0.82 | true |
| 3 | should we adopt Postgres logical replication for the migration | 200 | `executive_ceo` (default fallback) | 0.20 | true |
| 4 | redesign the CI pipeline to cut deploy time in half | 200 | `specialist_devops_engineer` | 0.82 | true |
| 5 | evaluate observability stack: Datadog vs Grafana Cloud | 200 | `specialist_data_engineer` | 0.82 | true |

**Response shape** (sample, intent #1):
```json
{
  "intent_text_echo": "evaluate Kubernetes vs ECS for compute layer",
  "operator_id_echo": "op_smoke",
  "classified_at": "2026-05-26T17:29:08.375531+00:00",
  "required_skills": ["kubernetes","ci_cd","infrastructure_as_code"],
  "routed_roles": [{"role_key":"specialist_devops_engineer","confidence":0.82,"rationale":"deployment / infrastructure keyword match (keyword='kubernetes')"}],
  "primary_role_key": "specialist_devops_engineer",
  "confidence": 0.82,
  "classifier_version": "stub-v0.1.0",
  "stub": true,
  "todo_swap_for_real_classifier": "Wave 2 PR3+ will replace with sentence-transformer similarity over agent_roles.required_skills x skill_vectors.vector_embedding"
}
```

**Verdict:** **YELLOW.**
- PASS: 5/5 HTTP 200, all carry `stub: true`, response shape matches PR #85 spec.
- FAIL on CTO assumption: **0/5 routed to `executive_cto`** — the stub keyword map has no rules for CTO (no "kubernetes/postgres/observability/architecture/platform" → CTO mapping). Today the stub fans CTO-level architectural intents out to devops/ciso/ceo/data_engineer instead of `executive_cto`. The CTO routing path technically exists but is unreachable via the stub's current keyword set.

---

## Step 3 — persona-engine `/v1/executive-personas/cto`

```bash
TOKEN=$(gcloud auth print-identity-token)
curl -sS https://persona-engine-sqatlxhlza-uc.a.run.app/v1/executive-personas -H "Authorization: Bearer $TOKEN"
# {"items":[],"count":0}
curl -sS https://persona-engine-sqatlxhlza-uc.a.run.app/v1/executive-personas/cto -H "Authorization: Bearer $TOKEN"
# {"detail":"no executive persona 'cto'"}
```

**Verdict:** **RED.** The 9-persona doctrine seed defined in PR #12's `executive_org_personas.yaml` was **not auto-loaded on container boot** despite the PR description stating `load_seed` is "called once on first boot." The router endpoints are mounted (openapi confirms `/v1/executive-personas`, `/v1/executive-personas/load_seed`, etc.) but the seed table is empty.

**Required next step:** invoke `POST /v1/executive-personas/load_seed` once with auth. This is a state-mutating write and the auto-mode classifier (correctly) blocked it during this read-only smoke. Either:
- a human runs it once now, OR
- persona-engine's `start.sh` is amended to call `load_seed` on boot (per PR #12 test plan checkbox that says exactly this — it was not verified post-merge).

Cannot verify multi_axis_tags / prompt_template / decision_lens shape until the seed lands.

---

## Step 4 — intel-silo migration 033 diagnostic

```bash
TOKEN=$(gcloud auth print-identity-token)
curl -sS https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/openapi.json -H "Authorization: Bearer $TOKEN" | jq '.paths | keys'
```

49 paths registered, **none** of: `/migrations`, `/diagnostics`, `/admin/schema`, or anything that confirms `agent_roles` or `skill_vectors` tables exist at runtime.

Deploy log for run `26462693573` does not contain any `running migration / 033_ / applied` strings — suggesting the deploy step does not log the boot-gate migration apply explicitly. Cannot confirm migration 033 ran without DB-level access or a new diagnostic endpoint.

**Verdict:** **YELLOW (unverifiable).** PR #41 migration file is present in the deployed image (intelligence-silo-00038-w6w), but there's no runtime introspection endpoint to confirm the tables were created. Gap captured in punch list.

---

## Step 5 — Gateway PPIM attribution_chain stamping (depth-2, `cbp`)

```bash
TOKEN=$(gcloud auth print-identity-token)
curl -sS -i -X POST https://gigaton-platform.web.app/v1/intelligence/classify \
  -H 'Content-Type: application/json' \
  -H 'X-Client-Namespace: cbp' \
  -H 'X-Operator-Id: cbp' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"intent_text":"set the 90-day infra security roadmap","operator_id":"cbp"}' | grep -i '^x-'
```

```
x-cloud-trace-context: 31ec7bbeb0a7e066e216bedb3e3ee2a2;o=1
x-ppim-chain: cbp,gigaton-root
x-request-id: 5ba17b5a-3d5e-4062-8473-0269a12a18bb
```

Also verified on a real backend route (`/v1/operators/cbp/calibration-status`) — same chain shape `cbp,gigaton-root` returned even though that route 404s for a non-existent operator. Middleware runs and stamps regardless.

**Verdict:** **PASS.** Gateway PR #57 middleware works. `X-PPIM-Chain` header carries `[leaf, gigaton-root]` on every routed request.

---

## Step 6 — Cross-namespace depth-3 (`cbp_walking_tour`)

```bash
TOKEN=$(gcloud auth print-identity-token)
curl -sS -i https://gigaton-platform.web.app/v1/operators/cbp_walking_tour/calibration-status \
  -H 'X-Client-Namespace: cbp_walking_tour' \
  -H 'X-Operator-Id: cbp_walking_tour' \
  -H "Authorization: Bearer $TOKEN" | grep -i '^x-'
```

```
x-ppim-chain: cbp_walking_tour,gigaton-root
```

**Expected:** `cbp_walking_tour,cbp,gigaton-root` (depth 3 — proving the `parent_operator_id` chain walk works).
**Actual:** `cbp_walking_tour,gigaton-root` (depth 2 — middleware skipped straight to root).

**Verdict:** **RED on chain depth.** Middleware itself is working; the **UAE `/v1/operators/{id}/parents` lookup returns no parent** for `cbp_walking_tour` because the entity-hierarchy seed has not yet been applied. This is the known gap captured in [[entity_hierarchy_for_namespace_seed_2026_05_26]] (DEFERRED until UAE `parent_operator_id` PR + gateway license-check PR land — middleware is one of those, but UAE side is still missing the parent registration).

---

## Cross-check tabulation

| Step | Result | Notes |
|---|---|---|
| 1. Gateway healthz 11/11 | GREEN | Ok |
| 2. 5x classify intent shape | YELLOW | Shape correct, but 0/5 routed to `executive_cto` — keyword map gap |
| 3. persona-engine CTO fetch | RED | Seed never ran, table empty |
| 4. intel-silo migration 033 diagnostic | YELLOW | No diagnostic endpoint exists — unverifiable |
| 5. Chain stamping depth-2 | GREEN | Middleware works |
| 6. Chain stamping depth-3 | RED | UAE has no parent_operator_id for sub-clients yet |

**Headline:** 2 GREEN + 2 YELLOW + 2 RED = circuit **primitives** exist but circuit **end-to-end** is broken in 3 distinct places.

---

## OVERALL VERDICT — YELLOW

**The 4 PRs were valid in isolation but do NOT yet compose into a working CTO routing circuit.** Three concrete gaps block "free-text CTO intent → routed to executive_cto persona → emitted with depth-3 attribution chain":

1. **`/v1/intelligence/classify` has no CTO keyword rules** — every CTO-ish architectural intent in the test set routed to devops / ciso / ceo / data_engineer instead. The stub's keyword map needs explicit `executive_cto` triggers (architecture / platform / postgres / observability / technical-roadmap / scaling / build-vs-buy / stack-evaluation).
2. **`executive_org_personas` table is empty in prod** — PR #12's `load_seed` was never invoked post-deploy. Either invoke it once via `POST /v1/executive-personas/load_seed`, or wire it into `start.sh` so it runs idempotently on every container boot.
3. **UAE has no `parent_operator_id` registered for sub-clients** — `cbp_walking_tour` resolves directly to `gigaton-root` instead of through `cbp`, breaking the depth-3 attribution chain that affiliate / licensing / compensation systems need (per [[beta_cohort_entity_structure_2026_05_25]]).

---

## Punch List (to reach GREEN on this circuit)

### P0 — unblocks the CTO routing path today

- [ ] **persona-engine `/v1/executive-personas/load_seed`** — invoke once. Verify with `GET /v1/executive-personas/cto` returning `display_name: "Chief Technology Officer"`, full `prompt_template`, `decision_lens`, `example_questions[3-5]`, and `multi_axis_tags` containing `axis:executive` + `function:engineering`.
- [ ] **decision-engine stub keyword map** — add CTO rules. Recommended keyword set: `architecture`, `platform`, `compute`, `compute-layer`, `kubernetes` (currently fans to devops), `postgres` (currently fans to ceo-default), `database`, `observability` (currently fans to data_engineer), `stack`, `build-vs-buy`, `scalability`, `tech-debt`, `technical-roadmap`, `infrastructure-strategy`. Update PR #85 follow-up so 3/5 of the canonical CTO test intents actually route to `executive_cto`.
- [ ] **Register `/v1/intelligence/classify` in gateway routing table** — currently the gateway aggregator returns "No engine maps to path /v1/intelligence/classify" (route only reachable by hitting decision-engine direct URL). Per [[namespace_middleware_silent_400_audit_2026_05_25]] this is the same class of gap as the 32 silent-400 endpoints.
- [ ] **Register `/v1/executive-personas/*` in gateway routing table** — same gap, identical fix.

### P1 — needed for cross-namespace correctness

- [ ] **UAE — backfill `parent_operator_id`** per [[entity_hierarchy_for_namespace_seed_2026_05_26]]. Minimum to unblock the smoke: `cbp_walking_tour.parent_operator_id = "cbp"` and `cbp.parent_operator_id = "gigaton-root"`. Then re-run step 6 and confirm chain depth = 3.
- [ ] **intel-silo migration verification endpoint** — add `/v1/admin/schema/migrations` returning `{applied: ["...", "033_agent_roles_and_skill_vectors"], head: "033", tables: ["agent_roles","skill_vectors", ...]}` so future smokes can confirm migration application without DB-level access.

### P2 — needed for the real Tier-5 CTO routing (Week 2+)

- [ ] **persona-engine seed → intel-silo `agent_roles` linkage** — seed one `agent_roles` row per executive persona (`role_key: "executive_cto"`, `function_area: "engineering"`, `required_skills: ["system_design","architecture","platform_engineering","postgres","kubernetes","observability"]`, `authority_scope: "cross_functional"`).
- [ ] **`skill_vectors` embeddings backfill** — the 384-dim sentence-transformer embeddings (per PR #41). Without these, the real classifier (Wave 2 PR3+ swap) has nothing to similarity-search against.
- [ ] **Swap `_classify_stub()` for real classifier** (per PR #85 follow-on plan) — sentence-transformer over `agent_roles.required_skills` × `skill_vectors.vector_embedding`. Bump `classifier_version` to `real-v1.0.0`, set `stub: false`. Gate Tier-5 auto-execute on `stub: false`.
- [ ] **HME dashboard event emission** — wire decision-engine `/v1/intelligence/classify` to fire an HME event of type `intelligence.intent_classified` carrying the full classify response + the `ppim_attribution_chain` header value. Confirm event lands in `users/{operator_id}/activity` Firestore log.
- [ ] **UI surface** — render classified intent + routed persona in operator's `/intelligence` route (alias of PR #41 gigaton-ui-system per [[RESUME_HERE_2026_05_26_full_session_handoff]]).

---

## What the smoke proved that DOES compose

- Gateway middleware stamping (PR #57) works on every routed request, even ones that 404.
- Decision-engine new endpoint is reachable, deterministic, stable-shaped, and self-flags as `stub: true` so downstream callers can gate on it.
- Persona-engine endpoints are mounted at the right paths with the right shape (verified via openapi.json).
- 11/11 platform engines remain healthy through the deploy of 3 PRs (zero regression).

## What this confirms about the architecture

The 4-PR decomposition was correct — each PR is independent, none crosses a deploy boundary, all 3 deploys were < 8 minutes, no shared-state risk. **The composition gap is a different class of work** (seed loading + routing-table registration + keyword-map expansion) and should land as 3 small follow-on PRs across the same 4 repos in Week 1 day 3-4.
