---
title: Gmail Support Relay — Workspace + GCP Setup
created: 2026-05-25
owner: todd@gigaton.ai
status: GCP side provisioned; Workspace admin clicks pending
---

# Gmail Support Relay — Workspace + GCP Setup

End-to-end runbook for the `support@gigaton.ai` collaborative inbox + `gmail-support-relay` service-account + Workspace domain-wide delegation. Half is provisioned (GCP); half is admin-console clicks that only a Workspace super-admin can perform.

## Decisions locked

| Decision | Value | Rationale |
|---|---|---|
| GCP project | `gigaton-platform` | Aligned with the accelerated migration target — avoids re-provisioning when carmen-beach-properties engines move per [[gcp_engine_migration_accelerated_2026_05_25]] |
| DWD impersonation subject | `bella@gigaton.ai` | Real Workspace user; bella's mailbox forwards to `todd@` by default. DWD cannot impersonate a Group, so we need a real user as the delegation target. |
| Gmail scopes | `gmail.modify` + `gmail.send` + `gmail.settings.basic` | Full read/send/modify + filter/forwarding mgmt. Maximum flexibility for inbound automation + outbound + settings ops. |
| `support@gigaton.ai` type | Google Group (Collaborative Inbox) | Group provides true assign/take/mark-done UX for human handling of inbound. |

## State as of 2026-05-25

### Already done (GCP)

- ✅ Gmail API enabled on `gigaton-platform` (project number `825651647756`)
- ✅ SA created: `gmail-support-relay@gigaton-platform.iam.gserviceaccount.com`
- ✅ Unique OAuth Client ID captured: **`103580174583594351085`** (the numeric value you paste into the DWD entry)

### Pending (Workspace admin — super-admin only)

- ⬜ W1 — Create Google Group `support@gigaton.ai` with Collaborative Inbox enabled
- ⬜ W2 — Add members + assign owners to the group
- ⬜ W3 — Add verified "Send mail as `support@gigaton.ai`" alias on `bella@gigaton.ai`
- ⬜ W4 — Authorize DWD entry in admin.google.com for the SA's client ID with the three scopes
- ⬜ V1 — Run verification snippet to prove the impersonation chain works end-to-end

---

## W1 — Create `support@gigaton.ai` as Collaborative Inbox

1. Go to <https://groups.google.com/u/0/all-groups> (must be signed in as `todd@gigaton.ai` super-admin)
2. **Create group**
   - Name: `Gigaton Support`
   - Email: `support@gigaton.ai`
   - Description: `Collaborative inbox for inbound customer support. Routed via gmail-support-relay SA for automation.`
3. **Access settings** (after creation, Settings → General):
   - Who can view conversations: **All members of the group**
   - Who can post: **Anyone on the web** (so external senders work)
   - Who can view members: **Group owners**
4. **Enable Collaborative Inbox**: Settings → Member privacy / Posting policies — toggle **Collaborative Inbox: ON**. This enables:
   - Take topics
   - Assign topics to members
   - Mark topics as no action / duplicate / resolved
   - Reply / reassign

## W2 — Members + owners

- **Members**: `bella@gigaton.ai`, `todd@gigaton.ai` (anyone else who handles support)
- **Owners**: `bella@gigaton.ai`, `todd@gigaton.ai`
- **Default forwarding**: bella's mailbox already forwards to todd@ by default per ops convention; no group-level forwarding needed.

## W3 — "Send mail as" alias on bella@

Required because DWD impersonating bella@ will call `gmail.send`. To send with `From: support@gigaton.ai`, the alias must be verified on bella@'s account.

1. Sign in to Gmail as `bella@gigaton.ai` (or use admin-console "log in as" if needed)
2. Settings (gear) → See all settings → **Accounts** tab
3. **Send mail as** → **Add another email address**
   - Name: `Gigaton Support`
   - Email: `support@gigaton.ai`
   - ☑ Treat as an alias
4. Next → **Send Verification**
5. Open the verification email **in the support@ group** (any group member can click it) → click the link → confirm
6. Back in bella@'s Gmail settings, set the alias as default if desired (or leave bella@ as primary and select support@ per-send in code)

## W4 — Authorize Domain-Wide Delegation

This is the step that actually grants the SA the right to act as bella@.

1. Go to <https://admin.google.com/ac/owl/domainwidedelegation> (must be signed in as `todd@gigaton.ai` super-admin)
2. Click **Add new**
3. **Client ID**: `103580174583594351085`
4. **OAuth scopes** (paste as a single comma-separated line, no spaces between):
   ```
   https://www.googleapis.com/auth/gmail.modify,https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.settings.basic
   ```
5. **Authorize**

Verification: the entry should appear in the DWD list with client ID `103580174583594351085` and 3 scopes shown.

---

## V1 — Verify the chain works

Run this Python snippet from a machine where you can write to `gigaton-platform`'s Secret Manager (or with a freshly-downloaded key file):

```python
# pip install google-auth google-api-python-client
from google.oauth2 import service_account
from googleapiclient.discovery import build
import base64
from email.mime.text import MIMEText

# Option A: key file (download via `gcloud iam service-accounts keys create key.json ...`)
KEY_FILE = "/tmp/gmail-support-relay-key.json"
SUBJECT = "bella@gigaton.ai"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.settings.basic",
]

creds = service_account.Credentials.from_service_account_file(
    KEY_FILE, scopes=SCOPES
).with_subject(SUBJECT)

gmail = build("gmail", "v1", credentials=creds, cache_discovery=False)

# Test 1: read access (DWD works at all)
profile = gmail.users().getProfile(userId="me").execute()
print("Impersonating:", profile["emailAddress"])  # should print bella@gigaton.ai
print("Total messages:", profile["messagesTotal"])

# Test 2: send-as alias works
msg = MIMEText("DWD verification — gmail-support-relay impersonation chain is live.")
msg["to"] = "todd@gigaton.ai"
msg["from"] = "support@gigaton.ai"  # uses the verified send-as alias
msg["subject"] = "DWD verify — gmail-support-relay 2026-05-25"
raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
sent = gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
print("Sent message id:", sent["id"])
```

**Expected output:**

```
Impersonating: bella@gigaton.ai
Total messages: <some integer>
Sent message id: <some hex>
```

And `todd@gigaton.ai` should receive an email From: `Gigaton Support <support@gigaton.ai>`.

**If you get `unauthorized_client`:**
- The DWD entry is missing or has wrong client ID. Re-check W4.
- Wait 1-2 minutes after adding DWD (eventual consistency).

**If you get `Delegation denied for ...`:**
- The Workspace user (bella@) doesn't exist, or DWD scopes don't include what the API call needs.

**If sending fails with `Invalid From header` or similar:**
- The "Send mail as" alias on bella@ isn't verified yet (W3 incomplete).

---

## Key handling

Two options for the SA credential:

**Option 1 — Workload Identity (preferred, no key files):** if the relay runs on Cloud Run in `gigaton-platform`, bind the SA to the Cloud Run service via `--service-account=gmail-support-relay@gigaton-platform.iam.gserviceaccount.com`. The runtime gets credentials automatically; no key file leaves GCP.

**Option 2 — Key file (only for local testing or external runtime):**

```bash
gcloud iam service-accounts keys create /tmp/gmail-support-relay-key.json \
  --iam-account=gmail-support-relay@gigaton-platform.iam.gserviceaccount.com \
  --project=gigaton-platform
```

Store the resulting JSON in Secret Manager:

```bash
gcloud secrets create gmail-support-relay-sa-key --project=gigaton-platform --replication-policy=automatic
gcloud secrets versions add gmail-support-relay-sa-key --project=gigaton-platform --data-file=/tmp/gmail-support-relay-key.json
shred -u /tmp/gmail-support-relay-key.json  # or: rm -P on macOS
```

Calendar a 90-day key rotation reminder (matches the platform's KMS rotation cadence per [[session_handoff_2026_05_22_beta_launch_sprint_complete]]).

---

## Blast radius if SA key leaks

With full scopes, a compromised key allows an attacker to (impersonating bella@):
- Read all of bella@'s mail (including support@ forwarded items if bella is a group member)
- Send mail as `support@gigaton.ai` (and any other verified alias on bella@)
- Modify filters/forwarding to exfiltrate future mail

Mitigations baked in:
- Key in Secret Manager only (never committed)
- 90-day rotation
- DWD scope is narrow to Gmail (no Drive/Calendar/etc.)
- Cloud Audit Logs on `gigaton-platform` capture every Gmail API call by this SA

If broader trust escalation matters, downgrade to send-only scope after initial setup is proven.

---

## Cross-references

- [[product_service_package_gigaton_ti_solutions]] — `support@` is the default support channel for the beta cohort
- [[gigaton_user_agreement_tcs.md]] — privacy@gigaton.ai (Bella, DPO) + general support@gigaton.ai already cited in user-facing T&Cs
- [[gcp_engine_migration_accelerated_2026_05_25]] — `gigaton-platform` project choice rationale
