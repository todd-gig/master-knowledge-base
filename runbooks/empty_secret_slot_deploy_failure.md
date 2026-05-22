# Empty Secret Slot → Cloud Run Deploy Failure (Runbook)

**First observed:** 2026-05-21 00:03-00:27Z (3 consecutive gigaton-gateway deploy failures, cascade triggered by PR #41 merge)
**Severity:** MAJ — blocks deploys; partial revert needed
**Root cause:** Cloud Run validates secret references against existing **versions**, not slots. A secret that exists with no versions = `versions/latest` returns nothing = deploy rejected.

## Symptom

GHA `Deploy gigaton-gateway` workflow fails at Cloud Build step #2 with:

```
ERROR: (gcloud.run.deploy) spec.template.spec.containers[0].env[N].value_from.secret_key_ref.name:
Secret projects/<PROJECT_NUMBER>/secrets/<SECRET_NAME>/versions/latest was not found
```

The deploy completes the image push (step #1) then fails on `gcloud run deploy` revision creation.

## Why it happens

```bash
# This creates an EMPTY slot:
gcloud secrets create openai-api-key --replication-policy=automatic --project=gigaton-platform

# This validates secret + version exists; FAILS if no versions yet:
gcloud run deploy <svc> --set-secrets=OPENAI_API_KEY=openai-api-key:latest ...
```

The trap: it's tempting to create the slot in preparation for a user to paste a credential later. But if the cloudbuild.yaml references the secret BEFORE the user pastes, **every deploy fails** until either (a) the user pastes, or (b) the binding is removed.

## Detection

GHA workflow fails OR rev list shows new revisions in "failed" state:

```bash
gcloud run revisions list --service=<svc> --region=us-central1 --project=<project> --limit=5 \
  --format='table(name,active,creation_timestamp.date())'
```

A new revision appears with `active=` blank (not promoted) — that's a failed deploy.

## Fix patterns (pick one)

### Pattern A — Pre-populate with a placeholder version (RECOMMENDED for known-empty-on-create)

When creating the secret slot, immediately add a `<empty>` placeholder version:

```bash
gcloud secrets create openai-api-key --replication-policy=automatic --project=gigaton-platform
printf '' | gcloud secrets versions add openai-api-key --data-file=- --project=gigaton-platform
```

The application code must handle empty-string gracefully — Phase D's `OpenAIProvider._read_key()` already does this (raises `RoutingError("openai_key_unset")` instead of crashing).

After the user pastes the real key, the latest version automatically becomes whatever they pasted; no cloudbuild change needed.

### Pattern B — Conditional secret mount via cloudbuild substitution

Use `_SUBSTITUTIONS` to make the mount conditional:

```yaml
substitutions:
  _OPENAI_SECRET_MOUNT: "OPENAI_API_KEY=openai-api-key:latest"  # default
# steps:
  - --set-secrets=SESSION_HMAC_KEY=session-hmac-key:latest,${_OPENAI_SECRET_MOUNT}
```

Then trigger deploys with `--substitutions=_OPENAI_SECRET_MOUNT=` (empty) when the secret isn't ready. More flexible but operationally finicky.

### Pattern C — Don't add the binding until the key is pasted

Drop the binding from cloudbuild.yaml until a real version lands. After the user pastes:

```bash
# 1. Verify version exists
gcloud secrets versions list <secret> --project=<project>

# 2. Add binding back via PR or direct edit
sed -i '' 's|--set-secrets=SESSION_HMAC_KEY=session-hmac-key:latest|&,OPENAI_API_KEY=openai-api-key:latest|' cloudbuild.yaml

# 3. Commit + push -> GHA redeploys
```

## The 2026-05-21 cascade — what actually happened

| Time (UTC) | Commit | Outcome | Detail |
|---|---|---|---|
| 00:03:14 | 6e3ff07 — PR #41 merge | ❌ FAILURE | First trip on the empty `openai-api-key` slot |
| 00:05:14 | f69a6cc — /v1/documentation routing hotfix | ❌ FAILURE | Same secret-missing error, unrelated change blocked |
| 00:21:40 | 54554e5 — "unblock auth probe + repair deploy cascade" | ✅ SUCCESS | Removed OPENAI_API_KEY binding from cloudbuild.yaml |
| 00:27:18 | fceca6b — "restore OPENAI_API_KEY secret binding after IAM grant" | ❌ FAILURE | Operator re-added the binding optimistically; secret still empty |
| 03:30:38 | 9c1f4e0 — Revert of fceca6b | ✅ SUCCESS | Back to no-OPENAI-binding state |
| 15:54:20 | ade445f — CORS hotfix | ✅ SUCCESS | Current main; no OPENAI binding |

Net result: gateway is healthy + Anthropic/Gemini work via Vertex AI; the OpenAI provider route returns `RoutingError("openai_key_unset")` for any task routed to GPT-4o.

## Recovery procedure (when user pastes OpenAI key)

```bash
# 1. User pastes (terminal, NOT chat — credential safety):
read -rs OPENAI_KEY
printf '%s' "$OPENAI_KEY" | gcloud secrets versions add openai-api-key --data-file=- --project=gigaton-platform
unset OPENAI_KEY

# 2. Verify version exists:
gcloud secrets versions list openai-api-key --project=gigaton-platform | head -3
# Should show: NAME: 1, STATE: ENABLED

# 3. Re-add binding in cloudbuild.yaml (small PR — agent or user can do):
#    Find this line in cloudbuild.yaml:
#      - --set-secrets=SESSION_HMAC_KEY=session-hmac-key:latest,GITHUB_WEBHOOK_SECRET=github-webhook-secret:latest,CLOUDBUILD_WEBHOOK_SECRET=cloudbuild-webhook-secret:latest,TWILIO_WEBHOOK_SECRET=twilio-webhook-secret:latest
#    Append: ,OPENAI_API_KEY=openai-api-key:latest
#    Commit + push. GHA auto-deploys.

# 4. Verify gateway revision picked it up:
gcloud run services describe gigaton-gateway --region=us-central1 --project=gigaton-platform \
  --format='value(spec.template.spec.containers[0].env[].name)' | grep OPENAI

# 5. Smoke test:
curl -sS -X POST "https://api.gigaton.ai/v1/llm/call" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"smoke","task_class":"classify","model_override":"gpt-4o"}' | head -3
# Expect a 200 with text response, NOT openai_key_unset
```

## Preventive: drift sentinel rule candidate

Future axiom (AX-024 candidate): "Cloud Run secret references must point to secret versions, not just secret slots." Detection: scan cloudbuild.yaml `--set-secrets=` lines; for each `<NAME>=<secret>:latest`, query `gcloud secrets versions list <secret> --project=<project>`; fail if empty.

Severity: MAJ (blocks deploys silently when an operator paste is forgotten).

## Cross-references

- master_project_plan.md §3.3.1 (PR #37 status — was claimed "active on next deploy"; corrected to "binding reverted, pending OpenAI key paste")
- master_project_plan.md §13 (active decisions — add "rebind OPENAI_API_KEY after user pastes")
- decision-engine drift_sentinel AX-024 (proposed)
- gigaton-gateway commit 54554e5 (the unblock hotfix)
- gigaton-gateway commit 9c1f4e0 (revert of premature restore)
