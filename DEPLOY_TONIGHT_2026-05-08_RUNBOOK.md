---
title: 19:00 CT Deploy Runbook — Friday 2026-05-08
created: 2026-05-08 17:00 CT
horizon: tonight, single deploy window
---

# Pre-flight (do once, ~2 min)

```bash
# Confirm gcloud is auth'd as todd@gigaton.ai (not bella@):
gcloud config get-value account
# Should print: todd@gigaton.ai
# If not: gcloud config set account todd@gigaton.ai

# Run the script's own preflight (governance + time + auth check):
cd ~/Documents/GitHub/master-knowledge-base
./scripts/deploy_19.sh --check
```

Expect: `✓ pre-flight clean (CT hour=<hr>, gcloud=ok, prev=ok, governance=ok)`.

# Step 1 — fire the deploy (~15-25 min wall-clock)

```bash
cd ~/Documents/GitHub/master-knowledge-base
./scripts/deploy_19.sh
```

What runs (PDC descoped to 2026-05-13 — 6 services tonight):

| # | Service | Mechanism | What it does |
|---|---|---|---|
| 1 | decision-engine | cloudbuild | rebuilds + redeploys 9-stage decision pipeline |
| 2 | gigaton-engine | cloudbuild | **fixes the 503** that's been there since 2026-04-07 (rev 1 broken; current code is correct) |
| 3 | sales-operating-system | cloudbuild | rebuilds + redeploys catalog + agent runtime |
| 4 | intelligence-silo | cloudbuild | **first-ever deploy** — 15-min build (PyTorch+sentence-transformers), 4Gi/2CPU |
| 5 | sovereign-influence-engine | sie_daily | runs SIE's daily_deploy.sh — builds + pushes 11 images, runs migrations, redeploys all 11 backends |
| 6 | Gigaton-UI-Platform | firebase_auto_verify | NO-OP (auto-deploys via Firebase on PR merge); just verifies last CI run was green |

# Step 2 — wire the silo URL into Firebase Functions (~2 min, after step 1 finishes)

The silo just came up for the first time. The chat `Gigaton (local)` provider is wired in code (`functions/src/providers.ts:121`) but reads `GIGATON_SILO_URL` env which isn't set yet.

```bash
cd ~/Documents/GitHub/master-knowledge-base
./scripts/post_deploy_silo_url.sh
```

That script:
1. Reads the silo's Cloud Run URL
2. /health checks it
3. Sets `GIGATON_SILO_URL` Firebase Functions secret
4. Tells you the redeploy command

# Step 3 — redeploy Firebase Functions to pick up the secret (~3 min)

```bash
cd ~/Documents/GitHub/Gigaton-UI-Platform
firebase deploy --only functions --project=gigaton-platform
```

# Step 4 — verify the chat path actually serves real LLM (or stub)

Open https://gigaton-platform.web.app, sign in, send a chat message.

**Expected today:** stub-echo response (deterministic, not creative). Reason: `INTELLIGENCE_LLM_ENABLED=0` on operator-api per [decisions/2026-05-08_INTELLIGENCE_LLM_ENABLED_off_pending_tracking.md](decisions/2026-05-08_INTELLIGENCE_LLM_ENABLED_off_pending_tracking.md).

If you decide to flip back on (after auditing platform-key fallback per the decision doc):
```bash
gcloud run services update operator-api --region=us-central1 \
  --project=carmen-beach-properties \
  --update-env-vars=INTELLIGENCE_LLM_ENABLED=1
```

# What's expected to be running by ~19:30 CT

After everything green:

| Service | URL |
|---|---|
| Operator API (gateway) | https://api-gateway-service-rjmcrtvuzq-uc.a.run.app |
| Operator API (direct) | https://operator-api-rjmcrtvuzq-uc.a.run.app — Phase A+B+C if PR #193 merged |
| **gigaton-engine** | https://gigaton-engine-rjmcrtvuzq-uc.a.run.app — **back from 503** |
| **intelligence-silo** | https://intelligence-silo-rjmcrtvuzq-uc.a.run.app — **first-ever live** |
| Decision-engine + 10 SIE backends | private (behind gateway) |
| Frontend | https://gigaton-platform.web.app |

# What to do if something fails

## PDC skipped intentionally
Already descoped. If the deploy log marks the run failed because PDC was attempted, the comment-out in deploy_19.sh didn't take. Fix: re-edit `scripts/deploy_19.sh` and confirm the `Carmen-Beach-Properties` line begins with `#`.

## intelligence-silo build fails
Probably out of build minutes or PyPI hiccup. Re-run just that service:
```bash
./scripts/deploy_19.sh intelligence-silo
```

## SIE daily_deploy.sh fails
Step is `bash daily_deploy.sh` inside the SIE clone. Look at `~/Documents/Claude/Projects/CxGuy-2.0/sovereign-influence-engine/deploy_logs/`. SIE has its own retry / rollback. Re-run via:
```bash
./scripts/deploy_19.sh sovereign-influence-engine
```

## Firebase Functions deploy fails
Most common cause: missing secret. The IAM grant for `firebaserules.admin` was applied today (was the silent CI failure since 2026-05-06). If THIS time it fails for a different reason, surface the error.

## Past 20:00 CT
deploy_19.sh's preflight refuses. Tomorrow morning is the next window.

# Post-deploy (recommend doing tomorrow)

- [ ] Inspect `deploy-log.jsonl` end-of-run lines — confirm all 6 services ended `ok`
- [ ] Re-baseline /health on every service vs the morning baseline (was: gigaton-engine 503, others 200/403-as-expected)
- [ ] Tag the cycle in master-knowledge-base if you're tracking releases
- [ ] Run the 60-hour value audit (per `recurring_60h_value_audit.md` memory) before next deploy

# At-a-glance

```
Pre:     ./scripts/deploy_19.sh --check
Deploy:  ./scripts/deploy_19.sh
Post-1:  ./scripts/post_deploy_silo_url.sh
Post-2:  cd ~/Documents/GitHub/Gigaton-UI-Platform && firebase deploy --only functions --project=gigaton-platform
Verify:  open https://gigaton-platform.web.app, send chat message
```

**Total wall-clock: ~25–30 min for the full sequence.**
