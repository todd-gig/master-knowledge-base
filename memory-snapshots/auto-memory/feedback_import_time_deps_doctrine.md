---
name: feedback-import-time-deps-doctrine
description: "HARD RULE established 2026-06-02. Every Python package imported at module-load time (top-level imports, model definitions using EmailStr/HttpUrl, etc.) MUST be explicitly listed in requirements.txt — never assumed transitive. Failure mode: container won't bind 8080 → Cloud Run startup probe times out at 5 min → deploy fails silently → live revision stays on last-healthy → silent stale prod for hours/days. Reinforced after the affiliate-system EmailStr incident locked the gateway at rev 00062-w4l for 23 hours (5 consecutive failed revisions 00063-00067)."
metadata: 
  node_type: memory
  type: feedback
  established: 2026-06-02
  authority: hard rule
  scope: "all gigaton FastAPI services (gateway, UAE, intel-silo, HME, decision-engine, persona-engine, red-phone-engine, etc.)"
  originSessionId: 95ce7a3e-1854-44fc-b54b-1d5cadd60e5a
promoted_from: feedback_import_time_deps_doctrine.md
promoted_at: 2026-06-02T20:13:25Z
---

# Import-time dependencies — HARD RULE

**Rule:** Any Python package referenced at module-load time MUST appear in `requirements.txt` (or the equivalent pinned-deps file). This includes:
- Direct `import x` / `from x import y` at the top of any file that gets imported by `api.main` (transitively).
- Pydantic field types that have **runtime extras** (`EmailStr` → `email-validator`, `HttpUrl` → `idna` etc., constrained-string regex types, etc.).
- Datetime / decimal / network libs used in module-level type annotations or dataclass field defaults.

**Why this matters:** Cloud Run startup probe is **TCP socket on port 8080, 30 attempts × 10s = 5 minutes max**. If the container can't import `api.main` (because a transitive dep is missing), uvicorn never binds 8080 → probe never passes → revision marked unhealthy → traffic stays on the previous revision. The deploy step reports failure, but the live service keeps serving stale code from the last-healthy rev. **Silent prod stagnation.**

**How to apply:**

1. **When adding any new feature module** (e.g. `app/affiliate/`, `app/coaching/`), audit every `import` and `from` line. For each external package, verify the exact dist name is in `requirements.txt`. Pinned version.

2. **Special audit for Pydantic field types.** Pydantic 2.x lists "optional" extras separately:
   - `EmailStr` → requires `email-validator` (NOT installed by base pydantic)
   - `HttpUrl`, `AnyUrl`, `PostgresDsn` → fine on base (no extra)
   - `PaymentCardNumber` → requires nothing extra in v2 (was a v1 extra)
   - `IPvAnyAddress` → fine on base
   - Constrained strings, decimals, dates → fine on base
   - Custom field types with `__get_validators__` may pull in arbitrary deps
   
   Rule of thumb: if your Pydantic field uses a non-stdlib type, grep the package's docs for "optional dependency" and pin accordingly.

3. **Pre-merge check (manual until CI'd):** Locally run:
   ```bash
   docker build -t test-img .
   docker run --rm -e GATEWAY_REQUIRE_JWT=0 -p 8080:8080 test-img &
   sleep 15
   curl -f http://localhost:8080/health
   kill %1
   ```
   If `/health` doesn't return 200 within 15s, something is broken at import. This catches everything before Cloud Run does.

4. **CI improvement (future doctrine work):** add a "container starts + binds 8080" smoke step to the Deploy workflow BEFORE `gcloud builds submit` — uses the same Docker build locally on GHA, runs the container, hits /health, only then submits to Cloud Build. Catches import errors in ~30s instead of waiting 17 min for Cloud Build to time out.

## Precedent incidents (this rule is real)

1. **2026-05-28 Red Phone deps** ([[red_phone_e2e_loop_wired_2026_05_28]] §"Doctrine learned"). httpx + twilio were shipped as `[dev]` not `[dependencies]`. Container crashed on `import twilio` in `api.py`. Took ~5 hr of debugging spread over the day.

2. **2026-06-02 gateway email-validator** (this incident, fixed by PR #83). Affiliate v0.1's `models.py:38` used `EmailStr` without adding `email-validator` to `requirements.txt`. **5 consecutive Cloud Run revisions failed** (00063 through 00067) over 23 hours. Multiple deploy attempts (mine + sibling instances') all bounced off the missing dep. Discovered by reading Cloud Run revision logs directly via `gcloud logging read`.

Both incidents share the exact same shape:
- New feature merged + tests green locally (because the dev environment had the package installed in some other context — pip / brew / system Python)
- Container build succeeds (because the missing dep is not needed during Docker build)
- Container fails to import at run time (because the production base image is minimal)
- Cloud Run startup probe times out at 5 min
- Live revision stays on last-healthy → silent stale prod

## How to find this when it happens

Diagnostic commands (in order):

```bash
# 1. Is the live revision the recent one?
gcloud run services describe <service> --project <p> --region us-central1 \
  --format='value(status.latestReadyRevisionName,status.latestCreatedRevisionName)'
# If created != ready, deploys are failing silently.

# 2. What's the latest revision's status?
gcloud run revisions list --service=<service> --project=<p> --region=us-central1 --limit=5

# 3. Container stdout/stderr from the failed revision
gcloud logging read 'resource.type="cloud_run_revision" \
  AND resource.labels.service_name="<service>" \
  AND resource.labels.revision_name="<failed-rev-name>"' \
  --project=<p> --limit=40 --format='value(textPayload,jsonPayload.message)' --order=asc

# 4. The Cloud Build log for context
gcloud builds log <build-id> --project=<p>
```

The container log will show `ModuleNotFoundError` or whatever the import error is. **This is the single most actionable diagnostic for any "deploy times out" incident**.

## Cross-refs

- [[red_phone_e2e_loop_wired_2026_05_28]] — first precedent; same shape.
- `gigaton-gateway` PR #83 — the email-validator fix that proved out this doctrine.
- `gigaton-gateway` PR #81 — cloudbuild timeout bump 600s→1800s (related but not the actual root cause; symptomatic fix that gave us enough time to discover the real cause via logs).
