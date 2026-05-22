# Provisioning `api.gigaton.ai` — DNS + Cloud Run domain mapping

**Owner:** todd@gigaton.ai
**Created:** 2026-05-20 (Gignet Phases C-G sprint)
**Estimated user time:** 10-15 min active + 1-24h DNS propagation wait
**Why:** Webhook endpoints (GitHub / Cloud Build / Twilio / Stripe / etc.) need a stable URL for vendor registration. Also resolves master plan §3.6 drift #4.

---

## Audit findings (2026-05-20)

Probed live state with `gcloud`:
- ❌ `gigaton.ai` is **NOT verified** in Google Search Console under todd@gigaton.ai (gcloud domains list-user-verified returned empty)
- ❌ **NO existing** Cloud Run domain mappings in `gigaton-platform/us-central1` (gcloud beta run domain-mappings list returned 0)

So the work has TWO steps: (1) verify domain ownership, (2) add the per-subdomain CNAME.

---

## Step 1 — Verify domain ownership in Google Search Console (one-time, ~5 min)

This grants Google Cloud (Cloud Run, Domain Mappings) the ability to issue managed SSL certs for any `*.gigaton.ai` subdomain.

### 1a. Trigger the verification flow

Open Google Search Console:
```
https://search.google.com/search-console/welcome
```

Sign in as **todd@gigaton.ai**.

Click **"Add property"** → choose **"Domain"** (the LEFT option, not "URL prefix").
Enter: `gigaton.ai`
Click **Continue**.

Search Console will display a **TXT record** that looks like:
```
google-site-verification=ABCDEF1234567890_xyz...
```

**Copy this value** (the `google-site-verification=...` string). Keep this Search Console tab open — you'll click "Verify" after step 1b.

### 1b. Add the TXT record at GoDaddy

Open GoDaddy DNS manager for `gigaton.ai`:
```
https://dcc.godaddy.com/manage/gigaton.ai/dns
```

Click **"Add New Record"** → set:
- **Type:** `TXT`
- **Name:** `@` (this means root domain)
- **Value:** the exact `google-site-verification=...` string from step 1a
- **TTL:** 1 hour (default)

Click **Save**. GoDaddy typically takes 1-30 min to propagate; can be up to 1 hour.

### 1c. Verify in Google Search Console

Wait ~5 min. Back in the Search Console tab, click **Verify**.

If it succeeds: you'll see "Ownership verified." Move to step 2.

If it fails: wait another 5-10 min and retry. (DNS propagation timing varies.) Confirm the TXT record is visible publicly with:
```bash
dig +short TXT gigaton.ai | grep google-site
```

---

## Step 2 — Add the CNAME record for `api.gigaton.ai` (one-time, ~2 min)

Back in GoDaddy DNS manager (same page as 1b):

Click **"Add New Record"** → set:
- **Type:** `CNAME`
- **Name:** `api`
- **Value:** `ghs.googlehosted.com.` (note the trailing dot)
- **TTL:** 1 hour

Click **Save**.

Verify it propagated:
```bash
dig +short CNAME api.gigaton.ai
# Should output: ghs.googlehosted.com.
```

---

## Step 3 — Tell Claude "DNS done, create the mapping"

Once `dig` confirms the CNAME resolves, ping me (Claude). I'll run:

```bash
gcloud beta run domain-mappings create \
  --service=gigaton-gateway \
  --domain=api.gigaton.ai \
  --region=us-central1 \
  --project=gigaton-platform
```

This requires authorization (production-infra modification). Cloud Run will:
- Verify the CNAME resolves to ghs.googlehosted.com
- Auto-issue a managed SSL cert (usually 5-15 min)
- Begin serving https://api.gigaton.ai → gigaton-gateway

Verify with:
```bash
curl -sI https://api.gigaton.ai/v1/healthz | head -5
# Expect HTTP/2 200
```

---

## Step 4 — Update downstream references

After api.gigaton.ai goes live, the following docs need a sweep (I'll do this in a docs PR):
- `repo_registry.md` — update gigaton-gateway URL
- `master_project_plan.md` §3.1 — flip `api.gigaton.ai` from NXDOMAIN to live
- `master_project_plan.md` §3.6 drift #4 — strike from list
- `api_reference_2026_05_19.md` — update base URL
- `operator_runbook_2026_05_19.md` — update daily health check URL

---

## Why not skip verification + use the *.run.app URL?

Two reasons:
1. **Vendor lock-in pain.** Every webhook registered with the *.run.app URL has to be re-registered when api.gigaton.ai eventually goes live. Easier to do it once.
2. **Cert trust.** Some vendor webhook senders (older Stripe SDKs, certain Twilio configs) trip on non-custom domains.

The whole flow above takes ~15 min of your active time + propagation. Worth it.

---

## Troubleshooting

- **"GoDaddy says invalid TXT value":** GoDaddy sometimes wraps in quotes — paste WITHOUT outer quotes. If GoDaddy strips the `=` sign, type it back in.
- **Search Console still says "not verified" after 1h:** check the TXT actually saved (refresh DNS page); some accounts have CAA records that block this — uncommon but possible.
- **`gcloud domain-mappings create` says "domain ownership not verified":** the verification from Search Console must be under the SAME Google account used for gcloud (todd@gigaton.ai). Both confirmed under todd@gigaton.ai per the audit.
- **`gcloud domain-mappings create` says "service does not exist":** confirm region — gigaton-gateway is in `us-central1` (verified 2026-05-20).
