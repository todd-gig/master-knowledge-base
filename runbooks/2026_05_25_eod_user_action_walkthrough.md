---
type: user-action-walkthrough
established: 2026-05-25 EOD
status: in-progress
purpose: Sequential steps to complete all human-only actions tonight + this week to unblock parallel agent work
estimated_time:
  tonight: 30-45 min
  this_week: ~6 hours total spread across operator availability
---

# EOD User Action Walkthrough — 2026-05-25

## TIER 1 — TONIGHT (30-45 min total, unblocks tomorrow)

### Step 1 — OAuth redirect URI (2 min) 🔴 GATES Day 2 cutover

1. Open https://console.cloud.google.com/apis/credentials?project=gigaton-platform
2. Find OAuth 2.0 Client ID starting `825651647756-bpb2sk8r…`
3. Click pencil icon → "Edit"
4. Scroll to "Authorized redirect URIs" → click "+ ADD URI"
5. Paste exactly: `https://intelligence-silo-sqatlxhlza-uc.a.run.app/v1/oauth/drive/callback`
6. Click "SAVE"

Keep the existing carmen-beach URI (`intelligence-silo-rjmcrtvuzq-…`) for rollback safety until Day 7.

---

### Step 2 — Create gigaton-ai.slack.com workspace (5-10 min)

1. Open https://slack.com/get-started#/createnew
2. Email: `todd@gigaton.ai`
3. Workspace name: `Gigaton AI`
4. Workspace URL: `gigaton-ai` (so it becomes `gigaton-ai.slack.com`)
5. **Skip team invites for now** — you'll add the support bridge bot programmatically later
6. Create these initial channels:
   - `#beta-support` — internal Gigaton platform support
   - `#alerts` — for Penrose / GCP / GHA alert routing
   - `#deploys` — for deploy status notifications
   - `#general` (default)
7. **Save the workspace URL + your admin login** — I'll need them when wiring the support bridge bot in Week 2

> The per-operator `#support-{op_id}` channels will be auto-created during entity onboarding (per omnichannel design §4 + entity-creation flow Step 9).

---

### Step 3 — Gmail API + Workspace setup (~10 min) [Google-stack, swapped from SendGrid]

1. **Create support@gigaton.ai Workspace group** (collaborative inbox):
   - https://admin.google.com/ → Directory → Groups → Create group
   - Email: `support@gigaton.ai`
   - Type: **Collaborative Inbox**
   - Members: todd@, bella@, matt@
   - "Anyone in the world can post"
2. **Create service account for backend Gmail relay**:
   - https://console.cloud.google.com/iam-admin/serviceaccounts?project=gigaton-platform
   - Name: `gmail-support-relay`
   - Generate JSON key → save (I'll mirror to GCP Secret Manager in Week 2)
   - Copy the **Client ID** from SA details page
3. **Authorize service account in Workspace**:
   - https://admin.google.com/ → Security → API controls → Domain-wide Delegation → Add new
   - Client ID: paste from step 2
   - Scopes: `https://www.googleapis.com/auth/gmail.send,https://www.googleapis.com/auth/gmail.readonly,https://www.googleapis.com/auth/gmail.modify`
4. **Skip MX record changes** — Workspace already handles `support@gigaton.ai` inbound natively.
5. **Pub/Sub watch on inbox** = Week 2 automated wiring; nothing to do tonight.

**Tell me when done** — I'll save the SA JSON to GCP secret + wire the Pub/Sub watch + extend the omnichannel design doc with the Gmail adapter spec.

---

### Step 4 — WhatsApp Business API verification (15-20 min to initiate; 3-7 day Meta wait)

1. Open https://business.facebook.com/ (use a personal Facebook acct admin'd by you)
2. **Business Settings → Business Info → "Add" Business** → name: `Gigaton AI`
3. Verify business via:
   - Domain: `gigaton.ai` (needs Meta domain verification — they'll give you a TXT record to add to DNS)
   - Legal name + address + tax ID (use your DBA filing if Gigaton AI doesn't have separate EIN yet)
4. **WhatsApp Manager → Add Phone Number**:
   - Use a NEW phone number (not your personal cell). Options:
     - Buy a Twilio number (recommended; ~$1/mo): https://console.twilio.com/us1/develop/phone-numbers
     - Use a Google Voice number
5. **Display Name:** "Gigaton AI Support"
6. **Category:** "Other Business" or "Technology"
7. Submit for review (Meta + Twilio review takes 3-7 business days)
8. Once approved, Twilio gives you the WhatsApp Sender ID — drop into a GCP secret named `whatsapp-sender-gigaton-ai`

**Parallel: same flow per-DBA later** — Ti Life, Ti Solutions, Total Interactions, Carmen Beach Properties (already has one). Defer those until they actually have customers.

---

### Step 5 — DNS records to add (~5 min, gives me the entity-creation flow unlock)

Add these CNAME records at your DNS provider (where `gigaton.ai` lives):

```
ti.gigaton.ai.                  CNAME  ghs.googlehosted.com.
life.ti.gigaton.ai.             CNAME  ghs.googlehosted.com.
solutions.ti.gigaton.ai.        CNAME  ghs.googlehosted.com.
total.ti.gigaton.ai.            CNAME  ghs.googlehosted.com.
```

(SendGrid MX record removed — Gmail handles support@gigaton.ai natively via existing Workspace MX records.)

(The Google Hosted target `ghs.googlehosted.com` is for Firebase Hosting; we'll point each Ti DBA subdomain at the same `gigaton-platform.web.app` site with rewrites in Firebase. Confirm once added — I'll wire the Firebase config in the next session.)

**Tell me which DNS provider** (GoDaddy / Cloudflare / Google Domains / etc.) — I can give exact UI-step screenshots if you want.

---

## TIER 2 — THIS WEEK (~6 hours spread across availability)

### Step 6 — Stripe Connect setup for Carmen Beach property owners (~1h per owner × 3 owners)

Per 30D-4 lock: Stripe Connect Express IMMEDIATELY (not manual invoices).

1. Open https://dashboard.stripe.com/ → **Connect → Settings**
2. Enable Stripe Connect on the existing platform Stripe account
3. **Configure Connect:**
   - Platform name: `Gigaton AI`
   - Account type: **Express** (Stripe handles KYC; lowest friction for owners)
   - Branding: upload Gigaton AI logo + brand colors
4. **For each property owner** (start with the 3 you have):
   - Send them an onboarding link from Connect dashboard
   - They complete KYC (~10-15 min for them; Stripe approves typically same-day)
   - Once verified, their Connect Account ID gets stored in the operator's record
5. **Test:** create a sandbox booking; verify split-payment flows correctly

Day 4 of migration (Fri 5/29) sales-OS cutover needs Stripe Connect live to be useful for Carmen Beach launch (Week 5).

---

### Step 7 — Paralegal engagement (~$8-24K, 2-3 weeks elapsed)

1. Pick a paralegal/lawyer (recommend a US tech-SaaS lawyer + a Mexican corporate counsel; Carmen Beach needs both)
2. Send them the v0 drafts at `/Users/admin/Documents/GitHub/master-knowledge-base/legal/v0_drafts/`
3. Specifically flag the punchlist (top 5 attention items in legal/v0_drafts/README.md)
4. Engage for "v0 → v1 review + sign-off for beta launch"
5. **Critical sub-decision for them:** Ti DBA status — DBA-under-Gigaton-AI vs separate LLC? (Recommend DBA per 30D ratification, but they should confirm tax-legally clean.)

---

### Step 8 — Migration cutover (Tomorrow morning 5/26, ~5h operator-attended)

The migration prep agent is finishing tonight. Tomorrow AM you'll have 4 ready-to-run cutover scripts. Sequence:

1. ~09:00 CT: run `decision-engine_cutover_ready.sh` → smoke 10 min → soak 30 min
2. ~10:00 CT: run `intelligence-silo_cutover_ready.sh` → smoke 10 min → soak 30 min (needs Step 1 OAuth URI already added)
3. ~11:00 CT: run `gigaton-engine_cutover_ready.sh` → smoke 10 min → soak 30 min
4. ~12:00 CT: run `sales-operating-system_cutover_ready.sh` → smoke 10 min → soak 30 min
5. ~13:00 CT: end-of-cutover full smoke chain across all engines
6. Days 5-7 (Wed-Fri): 7-day soak window where you watch for incidents but don't deploy anything new

I'll be online during the cutover to triage anything that fails. Each script has a rollback line at the bottom.

---

## TIER 3 — DEFERRABLE (Week 2+)

### Step 9 — BYO apex domains for individual Ti DBAs (if/when needed)
- Buy `tilife.com` / `tisolutions.co` / `totalinteractions.com` if you want apex-level branding for any DBA
- Until then, subdomains under `ti.gigaton.ai` are the default

### Step 10 — Per-entity business email setup
- For each entity that launches: `support@<domain>`, `legal@<domain>`, `noreply@<domain>` aliases
- Google Workspace: ~$6/user/month per entity
- Until Carmen Beach launch, the only business email needed is `support@gigaton.ai` (Step 3 SendGrid handles inbound)

### Step 11 — Additional WhatsApp Senders per DBA (when each launches paying customers)
- Same flow as Step 4 per DBA

### Step 12 — Beta operator invite list (Week 4-5 prep)
- Decide which ~25 operators get first-week invites
- Per audit: invite-only, cap N≤25, non-EU only

---

## What I'm doing IN TANDEM while you work the above

- Migration prep agent (Days 1-4) — IN FLIGHT, will produce 4 cutover-ready scripts by ~22:00 CT tonight
- Synthesizing tomorrow's resume plan
- Watching for any agent failures or new deploys to triage
- Standing by for your Tier 1 completion confirmations

---

## Tier 1 completion checkbox

Mark `[x]` here in this file as you complete each:

- [ ] Step 1 — OAuth URI added (2 min)
- [ ] Step 2 — gigaton-ai.slack.com created + 4 channels (5-10 min)
- [ ] Step 3 — SendGrid account + domain auth + API key + Inbound Parse host (10-15 min)
- [ ] Step 4 — WhatsApp/Meta business verification submitted (15-20 min)
- [ ] Step 5 — DNS CNAME + MX records added (~5 min)

Total: ~37-52 min of focused work tonight to unblock everything for tomorrow.
