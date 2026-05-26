# OAuth Client Recreation Runbook — `gigaton-platform` Migration

**Status:** PROCEDURE — execute during GCP project migration
**Authored:** 2026-05-25
**Companion:** [gcp_engine_migration_accelerated_2026_05_25.md](../../.claude/projects/-Users-admin/memory/gcp_engine_migration_accelerated_2026_05_25.md)

---

## 1. Why this runbook exists

When intelligence-silo migrates from `carmen-beach-properties` → `gigaton-platform`, the Google OAuth 2.0 client (currently `1097430360365-9k8e611hh5p5gc1ubhdnec7lf7h89r2f.apps.googleusercontent.com`) **does NOT migrate** with it.

OAuth 2.0 clients are tied to the GCP project that owns them. There is no API to transfer one across projects. We have to:

1. Create a new OAuth client in `gigaton-platform`
2. Set up the OAuth consent screen in `gigaton-platform`
3. Update silo env/secrets to use the new client ID + secret
4. (Optionally) keep the old client active during a transition window
5. (Optionally) re-publish the consent screen in the new project

This runbook captures every step so it doesn't get rediscovered mid-migration under time pressure.

---

## 2. Pre-flight (BEFORE silo moves to gigaton-platform)

### 2.1 Confirm we still need OAuth in gigaton-platform

Per [PR #40](https://github.com/todd-gig/intelligence-silo/pull/40), the silo requests:
- `openid`
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/drive.file` (post PR #40 — non-sensitive)
- `https://www.googleapis.com/auth/drive.readonly` (legacy single-account flow — pending sunset per [legacy DRIVE_SCOPES sunset plan](./2026_05_25_legacy_drive_scopes_sunset_plan.md))

The new OAuth client in `gigaton-platform` needs to list these same scopes.

### 2.2 Snapshot current state in `carmen-beach-properties`

Run BEFORE provisioning anything new — saves rediscovery if rollback is needed:

```bash
# Client ID + secret are in env vars; export them for reference
gcloud secrets versions access latest --secret=GOOGLE_DRIVE_OAUTH_CLIENT_JSON --project=carmen-beach-properties > /tmp/cbp_oauth_snapshot.json
chmod 600 /tmp/cbp_oauth_snapshot.json
# DO NOT commit this file anywhere

# Snapshot OAuth consent screen scope list
TOKEN=$(gcloud auth print-access-token)
curl -s -H "Authorization: Bearer $TOKEN" -H "X-Goog-User-Project: carmen-beach-properties" \
  "https://oauth2.googleapis.com/v1/iam-policies/projects/carmen-beach-properties/brands" \
  > /tmp/cbp_oauth_brand_snapshot.json
```

### 2.3 Identify all redirect URIs currently configured

Current silo redirect URI (per `core/drive_oauth.py:68-70`):
```
https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/v1/oauth/drive/callback
```

After migration the silo's Cloud Run URL will change (new project = new hash suffix). The new redirect URI will be of the form:
```
https://intelligence-silo-<NEW_HASH>-uc.a.run.app/v1/oauth/drive/callback
```

OR — preferred — proxy through the stable public host:
```
https://gigaton.ai/v1/oauth/drive/callback
https://gigaton-platform.web.app/v1/oauth/drive/callback
```

**Recommendation:** Use the stable host (gigaton.ai or gigaton-platform.web.app) as the redirect URI for the NEW client. Avoids needing to update the OAuth client every time Cloud Run regenerates the URL.

---

## 3. Provision the new OAuth client in `gigaton-platform`

### 3.1 Enable required APIs

```bash
gcloud services enable \
  iamcredentials.googleapis.com \
  oauth2.googleapis.com \
  drive.googleapis.com \
  --project=gigaton-platform
```

### 3.2 Configure OAuth consent screen (console-only — no API)

Open https://console.cloud.google.com/auth/branding?project=gigaton-platform

Fill in:
- **App name:** Gigaton (or whatever's on the carmen-beach-properties consent screen — keep consistent)
- **User support email:** todd@gigaton.ai
- **App logo:** Upload (if you have one)
- **App home page:** `https://gigaton-platform.web.app` (or `https://gigaton.ai` once that's hosting the FE)
- **App privacy policy:** `https://gigaton-platform.web.app/privacy` (live after [FE PR #37](https://github.com/todd-gig/gigaton-ui-system/pull/37) merge)
- **App terms of service:** `https://gigaton-platform.web.app/terms` (same)
- **Authorized domains:** `gigaton.ai`, `web.app`
- **Developer contact email:** todd@gigaton.ai
- **User type:** External (same as carmen-beach-properties)

### 3.3 Add the required scopes

Open https://console.cloud.google.com/auth/scopes?project=gigaton-platform

Add:
- `openid`
- `https://www.googleapis.com/auth/userinfo.email`
- `https://www.googleapis.com/auth/drive.file`
- (Only if legacy flow still in use — see sunset plan) `https://www.googleapis.com/auth/drive.readonly`

### 3.4 Create the OAuth 2.0 client

Open https://console.cloud.google.com/auth/clients?project=gigaton-platform → **+ CREATE CLIENT**

- **Application type:** Web application
- **Name:** `intelligence-silo-prod` (or similar; this is admin-only label)
- **Authorized JavaScript origins:**
  - `https://gigaton-platform.web.app`
  - `https://gigaton.ai` (once that domain hosts the FE)
- **Authorized redirect URIs:**
  - `https://gigaton-platform.web.app/v1/oauth/drive/callback`
  - `https://gigaton.ai/v1/oauth/drive/callback` (only if/when gigaton.ai is fronting the silo via the gateway)
  - (Transitional) `https://intelligence-silo-<NEW_HASH>-uc.a.run.app/v1/oauth/drive/callback` — get the actual Cloud Run URL after silo deploys to gigaton-platform

Click **Create** → download the credentials JSON.

### 3.5 Store the new credentials as a secret

```bash
# Save the downloaded credentials JSON to a temp file (chmod 600)
GCLOUD_QUOTA_PROJECT=gigaton-platform gcloud secrets create GOOGLE_DRIVE_OAUTH_CLIENT_JSON \
  --project=gigaton-platform \
  --replication-policy=automatic

GCLOUD_QUOTA_PROJECT=gigaton-platform gcloud secrets versions add GOOGLE_DRIVE_OAUTH_CLIENT_JSON \
  --project=gigaton-platform \
  --data-file=/path/to/downloaded_client.json
```

### 3.6 Grant silo runtime SA access to the secret

```bash
# Identify the silo's runtime SA in gigaton-platform (created during migration)
SILO_SA=intelligence-silo-runtime@gigaton-platform.iam.gserviceaccount.com  # adjust to actual

gcloud secrets add-iam-policy-binding GOOGLE_DRIVE_OAUTH_CLIENT_JSON \
  --member="serviceAccount:$SILO_SA" \
  --role=roles/secretmanager.secretAccessor \
  --project=gigaton-platform
```

---

## 4. Update silo to use the new client (single PR)

Files to modify in `intelligence-silo`:

### 4.1 Update default redirect URI

`core/drive_oauth.py:68-70`:
```python
# OLD
DEFAULT_REDIRECT_URI = (
    "https://intelligence-silo-rjmcrtvuzq-uc.a.run.app/v1/oauth/drive/callback"
)

# NEW
DEFAULT_REDIRECT_URI = (
    "https://gigaton-platform.web.app/v1/oauth/drive/callback"
)
```

### 4.2 Confirm cloudbuild.yaml points the secret env at the new project

`cloudbuild.yaml` (or wherever the deploy step lives) — the secret reference `GOOGLE_DRIVE_OAUTH_CLIENT_JSON` should resolve to the new `gigaton-platform` secret. Verify the GHA workflow uses the right `PROJECT_ID` substitution.

### 4.3 Front-end frontend return URL

`core/drive_oauth.py:71`:
```python
DEFAULT_FRONTEND_RETURN_URL = "https://gigaton-platform.web.app/sources?drive_connected=1"
```

This is already correct — points to the FE host, not the silo. No change needed.

---

## 5. Cutover sequence

### 5.1 Coexistence phase (recommended — 1-2 days)

Both OAuth clients (old + new) remain active. Silo deploys to gigaton-platform with the NEW client's credentials.

- Existing tokens in the silo's `oauth_tokens` table were issued by the OLD client. They will keep working for read/refresh as long as the OLD client exists.
- New auth attempts from the migrated silo go through the NEW client.

### 5.2 Hard cutover

After verifying the migrated silo flow end-to-end:

1. Delete the OLD OAuth client at https://console.cloud.google.com/auth/clients?project=carmen-beach-properties
2. Existing tokens issued by the OLD client immediately stop working
3. Users need to re-authorize via the NEW client

**This forces every user to re-auth.** If you want to avoid that:

Option (a): Leave the OLD client alive indefinitely (only `carmen-beach-properties` decommission triggers its deletion). No user impact.
Option (b): Run a migration job that proactively re-auths every user via a server-to-server flow. Not possible — OAuth user consent cannot be transferred.

Recommendation: Option (a). The OLD client costs nothing to keep alive. Decommission only when carmen-beach-properties is fully drained.

### 5.3 Re-publish the consent screen

After the new client is wired and tested:
- Open https://console.cloud.google.com/auth/audience?project=gigaton-platform
- Verify status panel shows the right scopes
- Click **PUBLISH APP**
- Smoke from a non-test-user account — should see the standard consent screen, no warning (since all scopes are non-sensitive post sunset plan)

---

## 6. Verification checklist

After cutover, run:

```bash
# 1. Silo deploy in gigaton-platform shows the right OAuth client ID in env
gcloud run services describe intelligence-silo \
  --project=gigaton-platform --region=us-central1 \
  --format="value(spec.template.spec.containers[0].env)" \
  | grep -A1 GOOGLE_DRIVE_OAUTH_CLIENT_JSON

# 2. /v1/oauth/drive/start returns an auth URL with the NEW client ID
curl -s "https://gigaton-platform.web.app/v1/oauth/drive/start?user_id=test" \
  | jq -r '.auth_url' | grep -oE 'client_id=[^&]+'
# Should print the NEW client_id, not the OLD 1097430360365-9k8e611hh...

# 3. End-to-end smoke from a non-test-user Google account in incognito browser
#    - Visit the auth URL from step 2
#    - Grant consent
#    - Verify callback returns success
#    - Verify the silo's oauth_tokens table has a new row

# 4. Confirm consent screen says "In production" (not Testing) in the new project
open "https://console.cloud.google.com/auth/audience?project=gigaton-platform"
```

---

## 7. Rollback

If the new OAuth client setup fails or causes regressions:

1. Revert silo's `DEFAULT_REDIRECT_URI` to the old Cloud Run URL
2. Update the silo's secret binding to point back at the `carmen-beach-properties` secret (requires temporary cross-project secret access grant)
3. Re-deploy silo to carmen-beach-properties (rollback the whole migration step)

The OLD OAuth client is left intact throughout, so this rollback only needs the silo to be running in carmen-beach-properties again.

---

## 8. Time estimate

- Console clicks (3.2 – 3.4): **15 min**
- Secret + IAM (3.5 – 3.6): **5 min**
- PR to update silo defaults (4.1 – 4.3): **10 min**
- Coexistence phase + smoke: **30-60 min**
- Hard cutover (5.2): **none needed if Option (a)**
- Re-publish consent screen (5.3): **10 min**

Total: **~1.5 hours operator-attended**.

---

## 9. Open questions

1. Do we re-bootstrap the OAuth consent screen brand under the same legal-entity name as carmen-beach-properties, or take this chance to formalize the Gigaton brand on the consent screen?
2. Do we want to set up OAuth verification + CASA in parallel with this migration, OR continue staying in the non-sensitive scope set (drive.file) indefinitely?
3. Do we forcibly invalidate old tokens after the migration (clean state) or keep them alive (zero user friction)?
