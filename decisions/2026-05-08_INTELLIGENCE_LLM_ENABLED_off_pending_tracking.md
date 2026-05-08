---
title: Decision — INTELLIGENCE_LLM_ENABLED OFF pending license tracking
date: 2026-05-08
decided-by: Todd (operator)
applied-by: Claude in Cowork session
status: ACTIVE — flag is OFF until re-enable criteria met
revisits: when license-tracking infra ships (see "Re-enable criteria" below)
---

# Decision

`INTELLIGENCE_LLM_ENABLED` is set to `0` on `operator-api` Cloud Run service in `carmen-beach-properties` project (us-central1).

**Effect:** the chat path runs in **stub-echo mode** — no real LLM provider calls. Stage 1 (capture) + Stage 3 (cxguy-methodology shape stamp) still fire on every chat message; Stage 2 (classifier) and Stage 4 (real LLM analyze) are skipped.

# Why now

The 60/40 dual-ownership license-attribution model requires per-call tracking so platform-paid LLM costs can be split between co-owners. Today there is no tracking infrastructure. Per session 8 of the Cowork log, `INTELLIGENCE_LLM_ENABLED=1` was already on **without** the tracking layer — that is a policy mismatch in shipped code: legal/financial-attribution gap on every chat call that uses a platform key.

The conservative, reversible move is to turn the flag off until tracking ships. Reverting takes one `gcloud run services update` call.

# What does NOT change

- **Per-user BYOK still works.** `POST /operator/intelligence/user-keys` saves user-provided LLM keys to Cloud Run Secret Manager. When a user key is configured, calls go to *their* provider on *their* bill — out of scope for 60/40 attribution. **If platform fallback is disabled when no user key is set, the flag could be safely re-enabled today.** See "Open question for next session" below.
- **Memory pipeline still runs.** Stage 1 captures every operator_event. Stage 3 stamps cxguy-methodology shape. Episodic memory writes continue. The 4-class memory hierarchy keeps accumulating substrate.
- **Hyperbolic memory rerank is still active** (`MEMORY_ENCODER_BACKEND=sentence_transformers` is set). Recall→rerank pipeline runs on every memory query.
- **Stub-echo mode still produces structured responses.** Frontend gets a deterministic response with action cards. UX is degraded (no creative LLM output) but functional.

# What changes — user-visible

Chat responses become deterministic stub text instead of LLM-generated. **The frontend should communicate this** — currently the chat UI doesn't know the flag is off and may present stub responses as if they're real model output. **TODO before users notice:**

- [ ] `ChatPage.tsx` reads `/operator/system/status` (or new endpoint) → renders a banner "Chat AI is in maintenance mode" when `intelligence_llm_enabled=false`
- [ ] Or: backend `intelligence/query` returns `{mode: "stub"}` flag the UI surfaces

# Re-enable criteria

Flip back to `1` when **at minimum one** of these is true:

1. **Per-call attribution is logged.** Schema (suggested):
   - `llm_call_audit` table: `id, ts, operator_id, org_id, provider, model, input_tokens, output_tokens, est_cost_usd, context (chat|capture|judge|other), trace_id`
   - Every LLM call writes a row before returning
   - Daily aggregation rollup (per operator + per org + per provider)
   - Verifiable against provider invoices (Anthropic, OpenAI, Gemini)

2. **All platform-paid calls are eliminated** — every code path requires a user-supplied key, no platform fallback. Verify by:
   - Code search: zero references to a default/platform LLM key in operator-api or memory-service
   - Runtime test: with no user key configured, chat returns a "configure a key" UX, not an LLM response

3. **Co-owner agreement** explicitly accepts the gap (e.g. monthly manual reconciliation against logs, signed off by both parties).

# What needs to be built (minimal tracking infra)

If choosing path #1 above:

- Migration: `migration_0XX_llm_call_audit.sql` — table per schema above
- operator-api hook: every `intelligence/query` call writes a row pre-return
- memory-service hook: every embedding call (sentence_transformers is local, but real LLM calls if they exist) writes a row
- Daily rollup job: Cloud Run Job + Cloud Scheduler (already a pattern with drift-sentinel-weekly)
- Operator dashboard: per-tenant + per-provider + per-co-owner-share view
- Reconciliation: monthly compare against provider invoices

Realistic scope: 2-4 days of focused work. Could be split: schema + write-hook (Day 1) → daily rollup (Day 2) → dashboard (Day 3) → reconciliation (Day 4).

# Open question for next session

**Does any code path currently fall back to a platform-paid LLM key when no user key is set?**

- Read `services/operator-api/src/intelligence/*.py` (or wherever the chat path lives)
- Look for `os.environ.get('ANTHROPIC_API_KEY' / 'OPENAI_API_KEY' / 'GEMINI_API_KEY')` or similar fallback
- Verify whether SecretStore has platform-level secrets that resolve when user has none

If the answer is **no fallback** → re-enable the flag is safe right now (path #2 above), no tracking needed. Cost is by definition the user's.

If the answer is **yes fallback** → either remove the fallback (smaller change than building tracking) or build the tracking infra.

# What I executed

```
gcloud run services update operator-api --region=us-central1 \
  --project=carmen-beach-properties \
  --update-env-vars=INTELLIGENCE_LLM_ENABLED=0
```

Result: revision `operator-api-00207-fiw` deployed at 100% traffic. Verified `INTELLIGENCE_LLM_ENABLED=0` post-deploy.

# Rollback (if needed during deploy window)

```
gcloud run services update operator-api --region=us-central1 \
  --project=carmen-beach-properties \
  --update-env-vars=INTELLIGENCE_LLM_ENABLED=1
```

This creates a new revision with the flag back on. ~1 minute including health-check.
