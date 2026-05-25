---
type: human-onboarding-message
recipient: matt@gigaton.ai
sender: todd@gigaton.ai
delivery: Slack DM in gigaton-ai.slack.com
created: 2026-05-26 ~00:40 UTC
priority: HIGH (gates beta-launch WhatsApp + omnichannel support)
task_estimated_time: 30-45 min hands-on + 3-7 day Meta review wait
---

# DM to send Matt — WhatsApp Business API + Meta Business Verification

Hey Matt — welcome again 👋 One more setup task to unblock our omnichannel customer support for beta launch. This is the WhatsApp + Meta side (email is handled separately, all Google-stack).

## What you're setting up
**Meta Business Manager + WhatsApp Business API for `Gigaton AI` entity.** This lets us route customer support requests (and later, marketing/onboarding messages) through WhatsApp at scale. Twilio is our WhatsApp Sender provider; Meta has to approve the business identity first.

Estimated hands-on time: **30-45 min**. Then there's a 3-7 day Meta review wait, so getting this initiated tonight or tomorrow is the unblocker.

## Steps

### 1. Create Meta Business Manager account for "Gigaton AI" (~10 min)
1. Open https://business.facebook.com/ — log in with a personal Facebook account you control (your own; doesn't matter which one as long as you're admin)
2. Click **"Create Account"** in Business Settings
3. **Business name:** `Gigaton AI`
4. **Your name:** `Matt <last name>`
5. **Business email:** `matt@gigaton.ai`
6. Click **Submit** — you're now Business Manager admin
7. **Business Settings → People → Add** → add `todd@gigaton.ai` as Admin
8. **Business Settings → Business Info → Edit** → fill in:
   - Legal name: `Gigaton AI` (or whatever the formal legal entity is — if you're unsure, ask Todd; this can be updated later)
   - Address: [Todd's business address]
   - Phone: [Todd's business phone]
   - Tax ID: [if available — can leave blank initially]
   - Website: `gigaton.ai`
9. Click **Save**

### 2. Domain verification (Meta needs to confirm we own gigaton.ai) (~5 min)
1. **Business Settings → Brand Safety → Domains → Add** → `gigaton.ai`
2. Meta gives you 3 verification options. Pick **"Meta-tag verification"** or **"DNS TXT record"** — TXT is cleanest:
3. Meta shows a TXT record value like `facebook-domain-verification=abc123xyz...`
4. **Send the TXT value to Todd** (DM in Slack) — he'll add the DNS record (you don't have DNS admin); usually propagates in 5-15 min
5. After Todd confirms the record is added, click **"Verify"** in Meta

### 3. WhatsApp Sender phone number (~10 min)
You need a phone number that's NEVER been used with WhatsApp consumer or WhatsApp Business app. Two clean options:

**Option A — Buy a Twilio number (recommended, ~$1.15/mo):**
1. Open https://console.twilio.com/us1/develop/phone-numbers/manage/search (log in with Todd's Twilio account — DM him for creds if you don't have them)
2. Search for a US number — pick one in a major area code (avoid 1-800 / vanity for v1)
3. **CRITICAL**: When buying, check the box **"Voice + SMS + WhatsApp"** capabilities (default is voice+SMS only)
4. Purchase
5. The number will appear in Twilio's Phone Numbers dashboard
6. DM Todd the new number — he'll add it as a GCP secret for the engine to use

**Option B — Use an existing dedicated business line** (only if Todd has a number that's never touched WhatsApp).

### 4. WhatsApp Business API verification submission (~10 min)
1. **Business Settings → WhatsApp Accounts → Add → "Create a WhatsApp Business Account"**
2. Account name: `Gigaton AI`
3. Time zone: `America/Mexico_City` (or your local — doesn't matter much)
4. Currency: `USD`
5. **Add Phone Number** → enter the number from Step 3
6. Verification method: **Twilio** (Meta-Twilio integration handles the deep-link; you'll get an automated SMS/voice code from Meta during the process)
7. **Display Name:** `Gigaton AI Support` (this is what customers see in WhatsApp)
8. **Category:** `Technology` or `Other → Software Service` (either works)
9. **About message** (optional, ~140 chars): `AI-powered platform for engineered brand experiences and predictably profitable interaction management.`
10. Submit for review.

> **Wait time:** Meta typically reviews in 1-3 business days, sometimes up to 7. Status visible in Business Settings → WhatsApp Accounts.

### 5. Once approved (likely Wed/Thu/Fri this week) — ping Todd
When Meta approves the WhatsApp Sender:
1. Twilio will get the green light from Meta
2. You'll see "Approved" status in Meta Business Manager → WhatsApp Accounts
3. **DM Todd in Slack: "WhatsApp approved 🎉"** — he'll wire the Twilio credentials into the omnichannel pipeline

## What you don't need to do
- Email setup (Todd doing himself via Gmail/Workspace)
- DNS records (Todd has access)
- Code changes (Week 2 backend wiring is on Todd / Claude)
- Per-DBA WhatsApp Senders (Ti Life / Solutions / Total — that's later when those DBAs launch)

## Confirmation checklist — reply in this DM
- [ ] Meta Business Manager account `Gigaton AI` created
- [ ] Todd added as admin
- [ ] gigaton.ai domain TXT record value DM'd to Todd
- [ ] Domain verified in Meta
- [ ] Twilio number purchased: `+1-XXX-XXX-XXXX`
- [ ] WhatsApp Business Account created
- [ ] WhatsApp Sender submitted for Meta review
- [ ] Meta approval received (3-7 days)

## Questions?
Ping me in this DM. Meta's UI changes regularly so the menu names might drift slightly from what's above; flag anything that doesn't match and I'll re-orient.

Thanks Matt 🙏 — this + the email setup are the last 2 unblockers for omnichannel support readiness.
