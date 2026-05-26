---
type: human-onboarding-message
recipient: matt@gigaton.ai
sender: todd@gigaton.ai
delivery: Slack DM in gigaton-ai.slack.com once Matt accepts the workspace invite
created: 2026-05-25 EOD
priority: HIGH (gates beta-launch support readiness)
task_estimated_time: 20-30 minutes
---

# DM to send to @matt in gigaton-ai.slack.com

> Copy from the divider below and paste into a Slack DM to Matt. Edit any context if needed (e.g. add a "welcome" intro line in your voice).

---

Hey Matt — welcome to gigaton-ai.slack.com 👋

I've got one ~20-30min setup task for you to unblock beta-launch support. This is the email side of our omnichannel support pipeline (customers can reach us via email, SMS, WhatsApp, chat, and platform UI; you'll be triaging in Slack and replies route back to the customer's original channel).

## What you're setting up
**Gmail API access on `support@gigaton.ai`** via a Google Workspace collaborative inbox + a service account for backend sending. This replaces an earlier SendGrid plan; we chose Gmail to keep everything in the Google stack and use Pub/Sub for native inbound (aligns with our orchestration fabric).

## Steps (~20-30 min)

### 1. Create the support@gigaton.ai collaborative inbox (~5 min)
1. Open https://admin.google.com/ → **Directory → Groups → Create group**
2. Group email: `support@gigaton.ai`
3. Type: **Collaborative Inbox** (lets multiple people claim/respond from the same shared inbox)
4. Members: `todd@gigaton.ai`, `bella@gigaton.ai`, `matt@gigaton.ai`
5. Permissions: **"Anyone in the world can post"** (so external customers can email us)
6. Save the group

### 2. Create the backend service account (~5 min)
1. Open https://console.cloud.google.com/iam-admin/serviceaccounts?project=gigaton-platform
2. Click **"+ CREATE SERVICE ACCOUNT"**
3. Name: `gmail-support-relay`
4. Description: `Backend SA for Gigaton omnichannel support email sending via Gmail API with domain-wide delegation`
5. Skip the role grants step (no IAM roles needed; permissions come via DWD)
6. Click **DONE**
7. Click into the new SA → **Keys** tab → **Add Key → Create new key → JSON → Create**
8. The JSON file downloads. **DM that file to me (Todd)** — I'll move it to GCP Secret Manager and delete the local copy. Don't email it.
9. On the SA Details page, copy the **OAuth 2 Client ID** (a long numeric value, e.g. `1234567890`). Send me that ID too.

### 3. Authorize the service account for Gmail in Workspace (~5 min)
1. Open https://admin.google.com/ → **Security → Access and data control → API controls → Domain-wide Delegation**
2. Click **"Add new"**
3. Client ID: paste the Client ID from Step 2 #9
4. OAuth scopes (paste this comma-separated string exactly):
   ```
   https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.modify
   ```
5. Click **Authorize**

### 4. Confirm + ping Todd (~2 min)
Reply in this DM with:
- [ ] Group created
- [ ] Service account JSON sent to Todd
- [ ] Service account Client ID: `<paste here>`
- [ ] Domain-wide delegation authorized

Once you ping me with all four, I'll wire the backend Gmail adapter (Pub/Sub watch for inbound + send-via-gmail outbound) and the support pipeline goes live within a few hours.

## What you don't need to do tonight
- WhatsApp / SMS / Twilio setup (separate stream)
- Slack bridge bot setup (I'm wiring that Week 2)
- Any DNS work (Todd has that)
- Any code changes

## Questions?
Ping me in the DM if anything is unclear. The Workspace admin UI is occasionally weird; happy to screenshare if you're stuck for >5 min on any step.

Thanks for jumping on this 🙏 — it's the last unblocker for beta-launch support.

---

> END OF DM BODY. The rest of this file is Todd-only context.

## Notes for Todd (post-Matt-completion)

Once Matt completes the 4 steps:

1. Move the SA JSON to GCP Secret Manager:
   ```bash
   gcloud secrets create gmail-support-relay-sa-key \
     --project=gigaton-platform \
     --replication-policy=automatic
   gcloud secrets versions add gmail-support-relay-sa-key \
     --project=gigaton-platform \
     --data-file=/path/to/downloaded-sa-key.json
   rm /path/to/downloaded-sa-key.json
   ```
2. Note the SA Client ID — needed for the Gmail adapter config in connector-api (Week 2)
3. Validate domain-wide delegation actually grants Gmail access:
   ```bash
   # impersonate support@gigaton.ai via the SA + try a gmail.users.profile.get
   # (will require a small Python script Week 2; not tonight)
   ```
4. Ping Matt with thanks + estimate when support@ will be live (~24h post-Pub/Sub wiring in Week 2)
