---
title: B — Custom domains + CI fix (operator checklist)
created: 2026-05-07
context: PROGRESS_2026-05-07.md "Step B" — needs user-only actions (DNS + secrets)
---

# Findings (live state verified)

| Surface | What's live | What's missing |
|---|---|---|
| `gigaton-platform.web.app` (Firebase Hosting) | **HTTP 200, ~500ms** — frontend is LIVE | nothing — works as backup |
| `api-gateway-service-rjmcrtvuzq-uc.a.run.app` | **HTTP 200 on /health** — gateway is LIVE | pretty domain |
| `gigaton.app` DNS | resolves to `52.223.52.2` (AWS parking page) | not yet pointed at Firebase |
| `gigaton.ai` | Google Workspace mailboxes only — **NOT for platform web content** (out of scope) | n/a |
| `firebase-hosting-merge.yml` CI | failing 3× consecutively since 2026-04-29 | missing GitHub secret `FIREBASE_SERVICE_ACCOUNT` |

**Key correction:** the canonical domain is `gigaton.app`, **NOT** `gigaton.ai`. I had the wrong target in PROGRESS_2026-05-07.md and PLAN_10_DAY_2026-05-07.md. Updated below.

# What's already live (the integration is shipping)

`Gigaton-UI-Platform` `vite.config.ts:42` defaults `VITE_SIE_API_BASE` to `https://api-gateway-service-rjmcrtvuzq-uc.a.run.app` — meaning **even without env config, the frontend talks to the live SIE gateway**. 9 API clients (sieApi, talentInboxApi, manifestApi, suggestionsApi, bulkCorpusApi, onboardingApi, canonicalApi, affiliateApi, manifestTypes) all wired and shipping today.

**SIE is generating value right now via gigaton-platform.web.app**, just on an ugly URL.

# Operator actions (only you can do these — DNS + Firebase Console + GitHub Secrets)

## B.1 — Custom domain `gigaton.app` (~10–60 min)

Follow [`docs/gigaton-app-domain-setup.md`](https://github.com/todd-gig/Gigaton-UI-Platform/blob/main/docs/gigaton-app-domain-setup.md) in Gigaton-UI-Platform repo. Already authored, 100 lines, complete. Summary:

1. Firebase Console → Hosting → Add custom domain → `gigaton.app` (and `www.gigaton.app`)
2. Copy the TXT verification record Firebase shows
3. At GoDaddy DNS for gigaton.app: add TXT for verification, A `151.101.1.195`, A `151.101.65.195`, CNAME `www` → `gigaton-platform.web.app.`
4. Wait 5–60 min. Firebase auto-issues Let's Encrypt cert.
5. Smoke test: `curl -sI https://gigaton.app/`
6. Update Firebase Auth → Authorized domains → add `gigaton.app`, `www.gigaton.app`

**Note:** `.app` is HSTS-preloaded — HTTPS only by browser policy. Wait for SSL Connected before cutting over.

## B.2 — Custom domain `api.gigaton.app` for the gateway (~10–60 min)

Same registrar (GoDaddy) + Cloud Run domain mapping:

1. **First verify ownership of `gigaton.app` for your Google account** at https://search.google.com/search-console (TXT record at registrar). One-time per account.
2. Then run:
   ```
   gcloud beta run domain-mappings create \
     --service=api-gateway-service \
     --domain=api.gigaton.app \
     --region=us-central1 \
     --project=carmen-beach-properties
   ```
3. gcloud will print the A/AAAA records to add at GoDaddy. Add them.
4. Wait 5–30 min for cert provisioning.
5. Smoke: `curl -sI https://api.gigaton.app/health` → should return 200.

After live, update `Gigaton-UI-Platform/vite.config.ts:42` default to `https://api.gigaton.app`. (Optional — current default already works.)

## B.3 — Fix broken CI (~5 min)

Last 3 `firebase-hosting-merge.yml` runs failed with:
```
Error: Input required and not supplied: firebaseServiceAccount
```

Root cause: GitHub repo secret `FIREBASE_SERVICE_ACCOUNT` is missing.

Fix:
1. Firebase Console → Project Settings → Service accounts → Generate new private key (JSON)
2. GitHub: `gh secret set FIREBASE_SERVICE_ACCOUNT --repo todd-gig/Gigaton-UI-Platform < downloaded-key.json`
3. Re-run the failing workflow: `gh run rerun 25121334211 --repo todd-gig/Gigaton-UI-Platform`

After this, every merge to `main` deploys to Firebase Hosting automatically.

## B.4 — (Optional) `app.gigaton.app` redirect

If you want `app.gigaton.app` to serve the same surface as `gigaton.app`, add it as an additional Firebase Hosting custom domain in B.1. Otherwise skip.

# What I changed in code/docs

- This file: capture B findings + corrected target domain (`gigaton.app` not `gigaton.ai`).
- I am **NOT** updating the existing `gigaton-app-domain-setup.md` — it's complete and correct.
- I am **NOT** committing changes to Gigaton-UI-Platform from outside its working dir; if VITE_SIE_API_BASE default needs updating after `api.gigaton.app` is live, that's a 1-line PR in that repo.

# Status: B complete to the boundary I can reach

Two operator-only actions remain (DNS records + GitHub secret). Until those land, the integration **stays live on the existing URLs** — gigaton-platform.web.app + api-gateway-service-rjmcrtvuzq-uc.a.run.app. SIE is already generating value.
