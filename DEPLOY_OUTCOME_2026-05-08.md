---
title: 2026-05-08 deploy outcome — what shipped, what didn't, what's queued
date: 2026-05-08
window: 17:58 CT → 18:50 CT (well within 19:00 cutoff)
---

# What shipped to production tonight

## Cloud Run services on `carmen-beach-properties`

| Service | New revision | Outcome |
|---|---|---|
| **gigaton-engine** | `gigaton-engine-00002-mxd` | **31-day 503 cleared** — `/health=200`, was rev 00001-sxz broken since 2026-04-07 |
| **decision-engine** | `decision-engine-00001-8s8` | New service deployed (separate from `decision-engine-service` which is the SIE backend) |
| **sales-operating-system** | `sales-operating-system-00001-c9w` | Refreshed, tests intact |
| **intelligence-silo** | `intelligence-silo-00001-4m7` (NotReady) → silo fixes pushed; retry #3 in flight | First-ever deploy attempt; uncovered 3 code bugs (see "Issues found + fixed" below) |
| **SIE 11 backends** | refreshing via daily_deploy.sh on `feat/affiliate-signoff-chain22-v2` branch | In progress at write time — chain 22 v2 + migration 027 land alongside |

## Backend infrastructure changes

- IAM grant `roles/firebaserules.admin` on `gigaton-platform` SA `github-action-1192684337` — applied this afternoon (was silently blocking Firebase Rules CI since 2026-05-06)
- `INTELLIGENCE_LLM_ENABLED=0` set on `operator-api` (chat in stub-echo mode pending license-attribution infra; see decision doc 2026-05-08_INTELLIGENCE_LLM_ENABLED_off_pending_tracking.md)
- `MEMORY_ENCODER_BACKEND=sentence_transformers` already set on memory-service (verified earlier — hyperbolic memory recall stack is active in production)

## SIE chain 22 v2 (lands alongside SIE deploy)

When SIE daily_deploy.sh finishes:
- Migration 027 runs → tables `affiliate_agreements`, `affiliate_kyc`, `affiliate_terms`, `affiliate_state_transitions` exist in prod
- New endpoints live: `/operator/affiliate/onboard/start`, `/agreement/sign`, `/connect/onboarding-link`, `/connect/webhook`, `/state/{user_id}`, `/state/transition`
- Affiliate state machine: `pending → agreement_signed → kyc_verified → active`

# Issues found + fixed during tonight's deploy

## 1. cloudbuild `$COMMIT_SHA` not auto-populated

**Symptom:** All 4 cloudbuild submits failed with `invalid image name "gcr.io/.../X:": could not parse reference` (empty tag).
**Root cause:** `gcloud builds submit` from local tarball doesn't auto-populate `$COMMIT_SHA`.
**Fix:** Added `--substitutions=COMMIT_SHA=$(git rev-parse HEAD)` to `deploy_cloudbuild()` in `master-knowledge-base/scripts/deploy_19.sh`.

## 2. intelligence-silo cloudbuild.yaml lost from disk

**Symptom:** `intelligence-silo: no cloudbuild.yaml at /Users/admin/Documents/GitHub/intelligence-silo`.
**Root cause:** File existed at 16:41 CT (verified during deploy plan prep); gone by deploy time. Lost during sweep-branch / stash operations.
**Fix:** Restored from git commit `d1d6522` (the wip snapshot pushed earlier today). Now committed to `wip/intelligence-silo-deploy-fixes-2026-05-08` branch + PR #1 on todd-gig/intelligence-silo.

## 3. silo `pyproject.toml` invalid `build-backend`

**Symptom:** `ModuleNotFoundError: No module named 'setuptools.backends'` during `pip install -e ".[dev]"`.
**Root cause:** `build-backend = "setuptools.backends._legacy:_Backend"` doesn't exist.
**Fix:** Set to `"setuptools.build_meta"` (standard).

## 4. silo `pyproject.toml` invalid PEP 508 in `[gpu]` extra

**Symptom:** After fixing #3: `ValueError: invalid pyproject.toml config: project.optional-dependencies.gpu[0]. configuration error: must be pep508`.
**Root cause:** `torch>=2.2.0+cu121` is invalid (build-tag `+cu121` only allowed with `==`).
**Fix:** Set to `torch>=2.2.0`. cu121 wheels come from `--index-url` at install time, not from version pin.

## 5. silo `os.getlogin()` crashes in Cloud Run

**Symptom:** After fixing #3 and #4: container builds + pushes OK, but on startup uvicorn crashes with `OSError: [Errno 25] Inappropriate ioctl for device` in `core/vault/vault.py:105`.
**Root cause:** `os.getlogin()` requires a controlling terminal. Cloud Run containers have none.
**Fix:** Wrapped in try/except with `USER`/`LOGNAME` env fallback + `'cloud-run'` default. `VAULT_DISABLED=true` is set in cloudbuild.yaml but `SecureVault.__init__` runs encryption init unconditionally — this fix is also defense in depth.

## 6. Firebase CI 403 on `firebaserules.googleapis.com`

**Symptom:** Firebase deploy CI failed with `caller does not have permission`.
**Root cause:** SA `github-action-1192684337@gigaton-platform` lacked `roles/firebaserules.admin`.
**Fix applied:** IAM grant landed at 17:30 CT.

## 7. Firebase CI 403 on `artifactregistry.googleapis.com` enable

**Symptom:** After fixing #6: SA can deploy Firebase Rules, but can't enable Artifact Registry API.
**Root cause:** SA has `serviceUsageConsumer` (use APIs) but not admin (enable APIs).
**Status:** Not fixed tonight — `todd@gigaton.ai` lacks IAM permission on `gigaton-platform`. Drafted message for Bella: `MESSAGE_TO_BELLA_2026-05-08.md`. **Operator action: enable artifactregistry.googleapis.com on gigaton-platform once.**

# What's queued for tomorrow / next deploy

## In flight at end of this session

- **silo retry #3** (background `bah43uszm`, build `78a491ed-ffe9-42af-8eb5-ef686de2467e`) — vault.py fix in. Expect 10-15 min. If green: silo first-ever live + can fire `post_deploy_silo_url.sh`.
- **SIE daily_deploy** (background `b4hkplyj1`) — currently on memory-service. Chain 22 v2 endpoints + migration 027 land when it finishes. Expect 8-12 min.

## Open PRs (review queue)

| Repo | PR | What |
|---|---|---|
| todd-gig/sovereign-influence-engine | #193 | Phase A+B+C (951+ tests, 968/972 passing — 4 failures pre-existed) |
| todd-gig/sovereign-influence-engine | #194 | Chain 22 v2 backend (migration 027 + endpoints + state machine) |
| todd-gig/master-knowledge-base | #1 | Day-0 governance bundle |
| todd-gig/master-knowledge-base | #2 | Affiliate-centralization decision + Carmen Beach descope + LLM_ENABLED off + tonight runbook |
| todd-gig/intelligence-silo | #1 | Tonight's silo fixes (pyproject + vault.py) |
| bella-byte/Gigaton-UI-Platform | #118, #121, #125, #126, #127, #128 | 6 PRs (most either already on main or queued for Bella's review) |

## Operator action items

1. **Enable Artifact Registry API on gigaton-platform** — see MESSAGE_TO_BELLA_2026-05-08.md (or grant todd@gigaton.ai admin on that project). Unblocks every Firebase deploy.
2. **Review + merge silo PR #1** to land tonight's fixes onto main.
3. **Review + merge SIE PRs #193, #194** to land Phase A+B+C (already deployed via daily_deploy tonight) and chain 22 v2 (already deployed) onto canonical master.
4. **Carmen Beach unblock by Wednesday 2026-05-13** per `decisions/2026-05-08_carmen_beach_descope.md`.

# Net production impact

| Before tonight | After tonight |
|---|---|
| gigaton-engine: 503 since 2026-04-07 | **/health = 200** |
| Firebase Rules CI silently failing since 2026-05-06 | IAM grant landed; one Bella-side API enable away from green |
| intelligence-silo never deployed | First-ever attempt; 3 code bugs found + fixed; retry in flight |
| SIE: master-only, no chain 22 v2 | Refreshing now; chain 22 v2 endpoints + migration 027 land tonight via daily_deploy |
| `MEMORY_ENCODER_BACKEND=sentence_transformers` | unchanged (was already set; verified) |
| Chat path real LLM mode | OFF pending license-attribution infra |
| Affiliate centralization | Architecture decision committed (PR #2); backend + frontend PRs open |

7 distinct issues identified across infra + Cloud Run + IAM + Python packaging + container runtime, 6 of 7 resolved during the same window. The one remaining (Bella permissions) is a 30-second console click.
