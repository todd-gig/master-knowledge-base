# Orchestrator Fabric — Ops Procedures (Phases C-G)

**Created:** 2026-05-20 (Gignet Phases C-G sprint)
**Status:** living document — update as each Phase deploys
**Audience:** operators (Todd, future on-call) running the orchestrator fabric in production

This runbook covers day-to-day ops for the Gignet orchestrator fabric as it comes online across Phases C-G. Pairs with [api_gigaton_ai_dns_provisioning.md](api_gigaton_ai_dns_provisioning.md) for the edge URL + [gignet-orchestrator-dashboard.json](gignet-orchestrator-dashboard.json) for the Cloud Monitoring view.

---

## 1. Daily health check (60 sec)

```bash
# Aggregate orchestrator health
gcloud pubsub subscriptions list --project=gigaton-platform \
  --format='table(name.basename(),topic.basename(),pushConfig.pushEndpoint)' \
  --filter='topic~gignet-orchestrator'
# Expect: 2 active subs (orchestrator-trigger-fan-out + dashboard-stream)

# Cloud Function status
gcloud functions list --project=gigaton-platform \
  --format='table(name,state,updateTime.date())' \
  --filter='name~orchestrator OR name~gignet'
# Expect: all ACTIVE

# Sample task_registry — last 5 claims
gcloud firestore documents list task_registry --project=gigaton-platform --limit=5 \
  --format='value(name.basename(),createTime.date())' 2>/dev/null || echo "use Firebase console for Firestore browsing"

# Gateway aggregate
curl -sI https://api.gigaton.ai/v1/healthz | head -3
# Expect: HTTP/2 200 with aggregate_status: ok
```

If anything is degraded, see §6 troubleshooting.

---

## 2. Adding a new external source (Phase C extensibility)

When you want a new webhook source (e.g. Stripe, Calendar, Airbnb iCal callbacks) to feed events into the orchestrator topic:

1. **Generate signing secret** (if vendor uses HMAC signing):
   ```bash
   SEC=$(openssl rand -hex 32)
   gcloud secrets create <vendor>-webhook-secret --replication-policy=automatic --project=gigaton-platform
   printf '%s' "$SEC" | gcloud secrets versions add <vendor>-webhook-secret --data-file=- --project=gigaton-platform
   gcloud secrets add-iam-policy-binding <vendor>-webhook-secret \
     --member="serviceAccount:gigaton-gateway-runtime@gigaton-platform.iam.gserviceaccount.com" \
     --role="roles/secretmanager.secretAccessor" --project=gigaton-platform
   ```

2. **Build the handler** in `gigaton-gateway/api/webhooks/<vendor>.py` following the GitHub/Twilio template. Map vendor events to `<domain>.<event_type>` events.

3. **Register the webhook in the vendor's console** with payload URL `https://api.gigaton.ai/webhooks/<vendor>` and the signing secret from step 1.

4. **Add an `orchestrator_triggers` Firestore row** mapping the new completion_event_id to its downstream task templates. Document in [[standalone_bundle_net_new_concepts]] trigger map.

5. **Smoke test:** trigger a real event from the vendor (or use vendor's "send test webhook" button); verify a `task_registry` row appears in Firestore within 2 seconds.

---

## 3. Pausing an orchestrator trigger

If a downstream task is buggy and you need to stop the trigger from firing more work:

```bash
# Flip enabled: false in the trigger row (Firestore)
# Via Firebase console: gigaton-platform → Firestore → orchestrator_triggers → <event_id> → enabled = false
# OR via gcloud (Firestore admin API — pending Firestore CLI support)
```

Existing in-flight tasks continue; no new ones spawn from this trigger. Re-enable by flipping back to true.

---

## 4. Reclaiming a stuck task lease

If an agent claimed a task but stopped heartbeating (crashed Claude session, network drop):

```python
# In Cloud Shell or local Python with gignet-coordination installed:
from gignet_coordination import db, list_in_flight

scope = {"repo": "<repo>", "operator_context": ""}
stale = [t for t in list_in_flight(scope, db()) if t.lease_expires_at < datetime.utcnow()]
for t in stale:
    print(f"Stale: {t.task_id} claimed_by={t.claimed_by} expired={t.lease_expires_at}")
    # Mark abandoned so another agent can pick it up
    db().collection("task_registry").document(t.task_id).update({"status": "abandoned"})
```

The natural lease reclamation happens automatically on the next claim attempt (per `claim.py` line 96 — orphan reclaim). Manual cleanup is only for cases where no new agent is trying to claim.

---

## 5. LLM router cost monitoring (Phase D)

```bash
# Today's LLM spend by model
gcloud firestore documents list llm_call_cost --project=gigaton-platform \
  --filter='called_at >= "2026-05-20"' --format=json | jq '[.[] | {model: .fields.model.stringValue, cost: (.fields.cost_usd.doubleValue // 0)}] | group_by(.model) | map({model: .[0].model, total: (map(.cost) | add)})'
```

If `LLM_ROUTER_DAILY_ORG_CAP_USD` (default $50) is hit:
- Gateway returns `429 Budget Exceeded` to new LLM-routed calls
- Email alert fires (Cloud Monitoring policy)
- Override: bump env var on gateway service:
  ```bash
  gcloud run services update gigaton-gateway --region=us-central1 --project=gigaton-platform \
    --set-env-vars=LLM_ROUTER_DAILY_ORG_CAP_USD=100
  ```
  This is a production deploy — counts against the 19:00 CT ritual.

---

## 6. Troubleshooting

### Backlog alert fired ("orchestrator backlog > 100 messages")

```bash
# Tail the Cloud Function logs
gcloud functions logs read orchestrator-trigger-fan-out --project=gigaton-platform --limit=50

# Common causes:
# 1. Function timing out on slow Firestore query → check orchestrator_triggers index
# 2. Function instance hitting cold-start storm → bump min-instances temporarily
# 3. A surge of legitimate task_completed events → may auto-resolve, watch for 10 min
```

### "Gateway 5xx rate > 1%" alert

```bash
gcloud run services logs read gigaton-gateway --region=us-central1 --project=gigaton-platform --limit=100 | grep -E '"severity":"ERROR"'

# If 5xx is from a single route (e.g. /webhooks/github), check that vendor's signing secret rotation
# If 5xx is broad, check downstream engine availability via /v1/healthz
# Rollback the last deploy if needed:
gcloud run services update-traffic gigaton-gateway --region=us-central1 --project=gigaton-platform \
  --to-revisions=<PREVIOUS_REVISION>=100
```

### "Fan-out Cloud Function error rate > 5%" alert

```bash
gcloud functions logs read orchestrator-trigger-fan-out --project=gigaton-platform --limit=100 --severity=ERROR

# Common causes:
# 1. Firestore IAM permission revoked → re-grant roles/datastore.user
# 2. Malformed task_completed event from upstream → trace via emitted_by attribute, fix the emitter
# 3. Missing orchestrator_triggers row for a new event_type → add the row
```

### Local Claude CLI is conflicting with cloud orchestrator

Phase E gignet-local-node integration handles this. Confirm:
```bash
# Is the localhost dashboard running?
curl -sI http://127.0.0.1:7878/healthz | head -3

# Is the SessionStart hook claiming tasks?
cat ~/.gignet/active-claim-*.json 2>/dev/null | head -5

# If yes but heartbeat is stale, the MCP server's heartbeat timer may have crashed.
# Restart the local node:
launchctl unload ~/Library/LaunchAgents/com.gignet.local-node.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.gignet.local-node.plist 2>/dev/null
```

---

## 7. Emergency: stop the entire orchestrator

If something is fundamentally wrong and you need to halt all task spawning:

```bash
# Step 1: stop the Cloud Function (prevents new task_completed → next-task fan-out)
gcloud functions delete orchestrator-trigger-fan-out --project=gigaton-platform --region=us-central1 --quiet
# Re-create later via deploy script in gignet-orchestrator-fn repo

# Step 2: disable Pub/Sub subscription (prevents backlog from building)
gcloud pubsub subscriptions delete eventarc-us-central1-orchestrator-trigger-fan-out-* --project=gigaton-platform --quiet

# Step 3: existing in-flight task_registry rows continue heartbeat or auto-expire
# Do NOT delete the task_registry collection — that destroys lease history
```

**To restart:** re-deploy the Cloud Function via `gignet-orchestrator-fn/deploy.sh`. The Pub/Sub trigger auto-recreates the eventarc subscription.

---

## 8. Cross-references

- [api.gigaton.ai DNS provisioning](api_gigaton_ai_dns_provisioning.md)
- [Cloud Monitoring dashboard JSON](gignet-orchestrator-dashboard.json)
- [Alert policies YAML](gignet-alert-policies.yaml)
- Unified master plan: `/Users/admin/.claude/projects/-Users-admin/memory/master_project_plan.md` §7 + §10
- Orchestration spec: `/Users/admin/.claude/projects/-Users-admin/memory/gignet_auto_trigger_orchestration.md`
- Operator runbook (general): `/Users/admin/.claude/projects/-Users-admin/memory/operator_runbook_2026_05_19.md`
