---
title: Master Project Plan — 10-Day Execution
created: 2026-05-07
owner: todd@gigaton.ai
horizon: 2026-05-07 → 2026-05-16
status: active
supersedes: PLAN_10_DAY_2026-05-07.md
sources-audited:
  - 18 GitHub repos (full git status + commit history)
  - 5 background audit agents (repos / deployments / desktop / sessions / configs)
  - master-knowledge-base Day 0 plan + HANDOFF.md + PRINCIPLES.md
  - drift_sentinel BETA_2_GAP_LIST.md (as of 2026-05-06 EOD, GREEN)
  - ~/Desktop/* — 25+ spec bundles catalogued
  - ~/Downloads/ — last 30 days catalogued
---

# EXECUTIVE SUMMARY

**What's built:** 6 production backends (decision-engine, gigaton-engine, sales-operating-system, intelligence-silo, SIE operator-api, Carmen-Beach-Properties), 2 frontends (gigaton-ui-system, gigaton-platform.web.app). Code is written, tested, and committed.

**What's missing:** The process layer. There is no single deploy command, no central policy file enforced across repos, no shared memory accessible to Matt or Bella, no automation that runs every day in < 15 minutes, and ~25 Desktop spec bundles that haven't been ingested into the system that should govern them.

**This plan delivers in 10 days:**
1. Foundation — all uncommitted work committed, all branches merged, governance files live
2. Daily deploy automation — one command, < 15 min, all production services
3. Intelligence wiring — silo bridge, shared memory, cross-service weights
4. Knowledge distribution — docs ingested, Matt + Bella can query shared memory
5. Human policy layer — rules file, approval gates, daily ritual enforced in code

---

# LOCKED DECISIONS (do not re-litigate)

| # | Decision |
|---|----------|
| L1 | GCP owner of record: `todd@gigaton.ai`. `todd.cx@turtleisland.solutions` is IAM Viewer only. |
| L2 | Domain strategy: `api/app/decide/sales/sie/docs.gigaton.ai` + `carmenbeach.com` + `admin.carmenbeach.com` |
| L3 | Daily deploy: manual trigger at or by **19:00 CT**. Must be green before next day's work. No cron. Past 20:00 CT = skip, deploy in morning. |
| L4 | CODEOWNERS: `@todd-gig` + `@bella-byte` on every production repo. |
| L5 | Platform frontend emerges as `f(user, org, platform.intelligence)` — NOT spec'd up front (Engine Artifact Doctrine). B-15 deferred to Beta 2.1. |
| L6 | Intelligence silo: `VAULT_DISABLED=true` in Cloud Run, `_NullVault` reads creds from env vars. |
| L7 | Sales OS persistence: Cloud Run volume mount at `/data/sales_os.db` (GCS FUSE or NFS — to provision). |
| L8 | Scoring formula locked: `ROUND((Interaction_Value × 0.6) + (Marketing_Influence × 0.4), 2)` |
| L9 | Drift Sentinel is GREEN as of 2026-05-07 (0 critical / 0 major / 11 minor — all TypeScript `as any`). |

---

# WHAT IS ALREADY DONE (do not redo)

- B-01 through B-20 cascade resolved (BETA_2_GAP_LIST.md — see that file for detail)
- Gate 8 (drift check pre-cert) implemented in decision-engine
- 11 drift rule handlers implemented (41% coverage)
- CLAUDE.md added to all repos
- Drift sentinel GREEN (0 critical, 0 major)
- intelligence-silo: `_NullVault`, `SILO_DATA_DIR`, api.py startup bug fixed, text ingest/search endpoints, `scripts/ingest_docs.py`
- sales-operating-system: GigatonPricingClient, 3 pricing endpoints, Cloud Run Dockerfile + cloudbuild.yaml
- decision-engine: MASTER_ARCHITECTURE.md written
- master-knowledge-base Day 0: PRINCIPLES.md, PROCESS.md, SERVICES.md, CODEOWNERS.template, init-repo.sh, install-codeowners.sh, deploy_19.sh (skeleton) — **staged but not committed**

---

# CURRENT STATE SNAPSHOT

## Repos — deployment readiness

| Repo | Branch | Uncommitted | Docker | CloudBuild | Deployed |
|------|--------|------------|--------|------------|---------|
| decision-engine | main | YES (gates.py, learning_agent.py, drift_sentinel/, tests/) | ✓ | ✓ | Pending verify |
| gigaton-engine | main | YES (CLAUDE.md, agents.py, claude_enrichment.py, multi_agent/api.py, pricing_engine/api.py) | ✓ | ✓ | Pending verify |
| sales-operating-system | main | YES (CLAUDE.md, claude_reasoning.py, gigaton_pricing.py, .dockerignore) | ✓ | ✓ | Pending verify |
| intelligence-silo (worktree) | intelligence-silo-clean | Clean | ✓ | ✓ | NOT DEPLOYED — branch not merged to main |
| gigaton-ui-system | main | YES (CLAUDE.md) | ✗ | ✗ | npm package only |
| Carmen-Beach-Properties | main | ✗ | ✗ | ✓ | SHIPPED (Cloud Run + Cloud SQL) |
| master-knowledge-base | main | YES (PLAN, PRINCIPLES, scripts, HANDOFF, CODEOWNERS.template) | ✗ | ✗ | N/A |
| transcript-knowledge-base | main | YES (CLAUDE.md) | ✗ | ✗ | GitHub Actions (cron) |
| gigaton (frontend) | main | YES (CLAUDE.md) | ✗ | ✗ | Pending verify |

## Hard blockers for intelligence-silo deployment
1. Branch `intelligence-silo-clean` never merged to main
2. `$$DECISION_ENGINE_URL` substitution unresolved in cloudbuild.yaml
3. Secrets not in Secret Manager: `anthropic-api-key`, `silo-vault-passphrase`, `gcp-project-id`, `silo-gcs-bucket`
4. `/data` volume not mounted (FAISS index ephemeral without it)

## Hard blockers for sales-operating-system persistence
1. GCS FUSE volume mount commented out in cloudbuild.yaml
2. SQLite at `/data/sales_os.db` is ephemeral without mount
3. `seed_from_xlsx.py` defaults to `~/Desktop/Sales_Operating_System.xlsx` — broken in Cloud Run

## Security
- Leaked GitHub PAT documented in `Desktop/gigaton_v3_execution/PHASE_0_PAT_ROTATION_RUNBOOK.md` — **confirm it has been rotated before any new repo operations**
- `gcloud auth` token expired — needs `gcloud auth login` before any deploy commands

## Desktop bundles (not yet in repos)
25+ bundles. Priority 6 that must reach a repo this cycle:
1. `claude_brand_interaction_system` → decision-engine or new repo
2. `claude_decision_logic_pack` → already in repo, needs sync
3. `claude_gigaton_standalone_project/specs` → master-knowledge-base
4. `gigaton_enterprise_onboarding_v2` → master-knowledge-base or gigaton-ui-system
5. `gigaton_sie_first_production_bundle_v1` → SIE repo or decision-engine
6. `gigaton_claude_custom_language_repo_v3` → new repo or intelligence-silo

---

# 10-DAY PLAN

## DAY 1 — Commit Everything + Verify Live State
**Goal: clean repos, verified deployed services, no mystery state**

### Step 1.1 — Rotate PAT (10 min) 🔴 SECURITY
```
GitHub → Settings → Developer settings → Personal access tokens → Revoke gho_sQlm...
Create new PAT with repo + workflow + read:org scopes
Update any local git remote URLs that embed the old token
Scan: git log --all -S "gho_" --oneline in all repos
```

### Step 1.2 — Re-authenticate gcloud (5 min)
```bash
gcloud auth login   # browser popup, select todd@gigaton.ai
gcloud config set project carmen-beach-properties  # confirm correct project
gcloud run services list --region=us-central1       # get ground truth on what's live
```
Expected output: list of deployed services with their URLs. Update `master-knowledge-base/SERVICES.md` with real URLs.

### Step 1.3 — Commit master-knowledge-base Day 0 files (15 min)
Files are staged but uncommitted. Commit them now as the governance baseline:
```bash
cd /Users/admin/Documents/GitHub/master-knowledge-base
git add PLAN_10_DAY_2026-05-07.md PRINCIPLES.md HANDOFF.md CODEOWNERS.template
git add scripts/deploy_19.sh scripts/init-repo.sh scripts/install-codeowners.sh
git commit -m "feat: Day 0 governance foundation — plan, principles, deploy ritual, CODEOWNERS"
git push
```

### Step 1.4 — Commit all uncommitted work across repos (30 min)
For each repo with dirty working tree:

**decision-engine** — commit gates.py, learning_agent.py, drift_sentinel/, test files:
```bash
cd /Users/admin/Documents/GitHub/decision-engine
git add engine/gates.py engine/learning_agent.py drift_sentinel/ tests/test_gate_8_drift.py CLAUDE.md
git commit -m "feat: Gate 8 drift check, 11 drift rule handlers, updated learning agent"
git push
```

**gigaton-engine** — commit enrichment, multi-agent override, pricing assumptions:
```bash
cd /Users/admin/Documents/GitHub/gigaton-engine
git add CLAUDE.md integration/ multi_agent/api.py pricing_engine/api.py
git commit -m "feat: B-16-B-20 — pricing assumptions, override hook, cancel endpoint, enrichment updates"
git push
```

**sales-operating-system** — commit reasoning, pricing, dockerignore updates:
```bash
cd /Users/admin/Documents/GitHub/sales-operating-system
git add CLAUDE.md app/services/claude_reasoning.py app/services/gigaton_pricing.py .dockerignore
git commit -m "feat: pricing assumptions propagated, reasoning service updates"
git push
```

**transcript-knowledge-base**, **gigaton** — commit CLAUDE.md files.

### Step 1.5 — Merge intelligence-silo to main (20 min)
```bash
cd /Users/admin/Documents/GitHub/.claude/worktrees/intelligence-silo/intelligence-silo
# Open PR: intelligence-silo-clean → main
gh pr create --title "feat: Cloud Run deployment + text ingest/search + vault + retrain trigger" \
  --body "Consolidates all silo work: api startup fix, _NullVault, SILO_DATA_DIR, ingest/search endpoints, ingest_docs.py script, automated retrain trigger, Cloud Run Dockerfile + cloudbuild.yaml"
# Merge it
gh pr merge --squash
```

**End of Day 1:** All code is committed, repos are clean, deployed state is confirmed, silo is on main.

---

## DAY 2 — Process Foundation Live
**Goal: governance files in every production repo, CODEOWNERS enforced, daily ritual tested**

### Step 2.1 — Install CODEOWNERS across all production repos (20 min)
```bash
cd /Users/admin/Documents/GitHub/master-knowledge-base
./scripts/install-codeowners.sh --apply
# Reviews changes per-repo, commits each one
```
Production repos: decision-engine, gigaton-engine, sales-operating-system, intelligence-silo, Carmen-Beach-Properties, gigaton-ui-system, transcript-knowledge-base

### Step 2.2 — Add PROCESS.md ref to every repo CLAUDE.md (15 min)
Each CLAUDE.md should have a line:
```
## Process
Deploy ritual: master-knowledge-base/PROCESS.md
Daily cutoff: 19:00 CT. See deploy_19.sh.
```

### Step 2.3 — Write POLICY.md — the human rules instruction file (45 min)
This is the document that governs what the system can and cannot do autonomously.
Location: `master-knowledge-base/POLICY.md`

Contents:
```markdown
# GIGATON PLATFORM POLICY

## Autonomous execution allowed (no human approval required)
- Read operations on any connected system
- Draft creation (emails, docs, Slack messages) — draft only, no send
- Code generation + test execution in worktrees
- Memory ingestion (POST /memory/ingest) — any doc
- Lead scoring updates
- Drift sentinel scans and reports

## Requires human approval (SIE queue or explicit chat confirmation)
- Any outbound send (email, Slack, WhatsApp, SMS)
- Any financial transaction or pricing quote presented to a customer
- Merging PRs to main on any production repo
- Cloud Run deployments (daily deploy_19.sh is the only approved path)
- Adding collaborators to any repo
- Creating or deleting GCP resources
- Any decision class D1-D3 (per authority matrix)

## Prohibited (never execute)
- Committing to main without tests passing
- Deploying after 20:00 CT (use morning)
- Accessing customer PII outside the data boundary
- Entering API keys or credentials into any form
- Creating new user accounts on any platform
- Sending mass email or Slack broadcasts

## Override procedure
Any prohibited action can be executed if:
1. A SIE decision record exists with EXECUTE verdict
2. The decision record has a human-signed trust certificate (T3+)
3. The action is logged in deploy-log.jsonl with the decision_id reference

## Escalation path
Blocker → todd@gigaton.ai → 1-hour SLA during business hours
Security issue → rotate credentials first, file decision record second
```

### Step 2.4 — Wire POLICY.md into decision-engine as a loaded config (30 min)
The policy file should be machine-readable, not just human-readable.
Convert POLICY.md into `config/policy.yaml` with the same structure but typed for the engine:
```yaml
autonomous_execution:
  - memory_ingest
  - lead_scoring_update
  - drift_scan
  - draft_creation
  
approval_required:
  - outbound_send
  - customer_pricing_quote
  - pr_merge_production
  - cloud_run_deploy
  - financial_transaction

prohibited:
  - commit_without_tests
  - deploy_after_2000_ct
  - customer_pii_access
  - mass_broadcast
```
This gates the SIE approval queue against the policy at intake.

**End of Day 2:** Every repo has CODEOWNERS + PROCESS reference. POLICY.md exists as human doc + machine config. Governance is live.

---

## DAY 3 — Daily Deploy Automation < 15 Minutes
**Goal: `./scripts/deploy_19.sh` runs all production services clean in < 15 min**

### Step 3.1 — Confirm GCP secrets exist (30 min)
```bash
# Check what secrets exist
gcloud secrets list --project=carmen-beach-properties

# Create missing secrets (values come from your password manager / env):
gcloud secrets create anthropic-api-key --replication-policy=automatic
echo -n "sk-ant-..." | gcloud secrets versions add anthropic-api-key --data-file=-

gcloud secrets create silo-vault-passphrase --replication-policy=automatic
echo -n "..." | gcloud secrets versions add silo-vault-passphrase --data-file=-

gcloud secrets create silo-gcs-bucket --replication-policy=automatic
echo -n "gigaton-silo-data" | gcloud secrets versions add silo-gcs-bucket --data-file=-
```

### Step 3.2 — Create GCS bucket for silo + sales-os persistence (15 min)
```bash
# Silo data (FAISS index, decision journal, checkpoints)
gcloud storage buckets create gs://gigaton-silo-data --location=us-central1

# Sales OS SQLite (simple persistent volume alternative)
gcloud storage buckets create gs://gigaton-salesos-data --location=us-central1
```

### Step 3.3 — Uncomment volume mounts in cloudbuild.yaml files (20 min)
**intelligence-silo/cloudbuild.yaml** — uncomment:
```yaml
--add-volume=name=silo-data,type=cloud-storage,bucket=gigaton-silo-data
--mount-path=/data
--set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest
--set-secrets=VAULT_PASSPHRASE=silo-vault-passphrase:latest
--set-secrets=GCS_BUCKET=silo-gcs-bucket:latest
```
Also resolve the `$$DECISION_ENGINE_URL` substitution — replace with:
```yaml
--set-env-vars=DECISION_ENGINE_URL=https://decision-engine-HASH-uc.a.run.app
```
(Get the actual URL from `gcloud run services describe decision-engine --format='value(status.url)'`)

**sales-operating-system/cloudbuild.yaml** — uncomment:
```yaml
--add-volume=name=salesos-data,type=cloud-storage,bucket=gigaton-salesos-data
--mount-path=/data
--set-secrets=ANTHROPIC_API_KEY=anthropic-api-key:latest
--set-secrets=GIGATON_ENGINE_URL=gigaton-engine-url:latest
```

### Step 3.4 — Fix sales-os seeder path (15 min)
`sales-operating-system/scripts/seed_from_xlsx.py` line ~468 defaults to `~/Desktop/Sales_Operating_System.xlsx`.
Fix: commit a `data/catalog.json` export from the xlsx OR change the default to fail-fast with a clear error message:
```python
xlsx_path = os.environ.get("CATALOG_XLSX_PATH") or os.path.join(
    os.path.dirname(__file__), "..", "data", "catalog_seed.xlsx"
)
if not os.path.exists(xlsx_path):
    logger.warning("No catalog seed file found at %s — skipping seeder", xlsx_path)
    return  # graceful skip, not crash
```

### Step 3.5 — Fill in deploy_19.sh service targets (45 min)
The skeleton exists. Fill in each service's `make deploy` equivalent:

```bash
# In deploy_19.sh, replace TODO stubs with:

deploy_service() {
  local svc="$1"
  local repo_path="$GH_ROOT/$svc"
  echo "→ Deploying $svc..."
  
  # Pull latest
  git -C "$repo_path" pull origin main
  
  # Cloud Build submit (each service has its own cloudbuild.yaml)
  gcloud builds submit "$repo_path" \
    --config="$repo_path/cloudbuild.yaml" \
    --project="$PROJECT_ID" \
    --async  # non-blocking — we wait at the end
    
  echo "  $svc build submitted"
}

# Submit all in parallel
for svc in decision-engine gigaton-engine sales-operating-system intelligence-silo; do
  deploy_service "$svc" &
done
wait  # wait for all 4 Cloud Build triggers

# Health check all services
for svc in decision-engine gigaton-engine sales-operating-system intelligence-silo; do
  URL=$(gcloud run services describe $svc --region=us-central1 \
    --format='value(status.url)' 2>/dev/null)
  if [ -n "$URL" ]; then
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$URL/health" \
      -H "Authorization: Bearer $(gcloud auth print-identity-token)")
    echo "$svc → HTTP $STATUS"
  fi
done
```

### Step 3.6 — Wire Cloud Build triggers in GCP console (30 min — manual UI steps)
For each of the 4 backend services:
1. GCP Console → Cloud Build → Triggers → Create Trigger
2. Source: GitHub repo (`todd-gig/<service-name>`)
3. Branch: `^main$`
4. Config: cloudbuild.yaml in repo root
5. Service account: Cloud Build SA with `roles/run.admin` + `roles/secretmanager.secretAccessor`

Once triggers exist, `git push origin main` on any service repo automatically triggers a deploy.
The `deploy_19.sh` manual script remains the daily ritual — triggers are the safety net.

### Step 3.7 — Test full deploy end-to-end (30 min)
```bash
cd /Users/admin/Documents/GitHub/master-knowledge-base
./scripts/deploy_19.sh --check   # pre-flight only, no deploy
./scripts/deploy_19.sh           # full run — should complete in < 15 min
```
Target: all 4 services green, health checks 200, log entry in `deploy-log.jsonl`.

**End of Day 3:** Daily deploy automation works. Under 15 minutes. One command.

---

## DAY 4 — Cross-Service Intelligence Wiring
**Goal: decision-engine ↔ gigaton-engine ↔ intelligence-silo fully connected**

### Step 4.1 — B-04: Intelligence Silo weights import bridge (45 min)
`intelligence-silo/core/bridge/connector.py` claims to import weights from `decision-engine/config/engine.yaml` but doesn't.

Implement `load_decision_weights()` in the bridge:
```python
# connector.py
def load_decision_weights(self) -> dict:
    """Fetch value_weights and penalty_weights from decision-engine."""
    url = f"{self.engine_url}/config/weights"
    try:
        resp = urllib.request.urlopen(url, timeout=5)
        return json.loads(resp.read())
    except Exception:
        # Fallback: read from bundled engine.yaml
        return self._load_local_weights()
```
Add `GET /config/weights` endpoint to decision-engine that returns the current `value_weights` and `penalty_weights` from engine.yaml.
Wire the weights into the SLM matrix router's scoring at startup.

### Step 4.2 — B-05: Decision-engine ↔ gigaton-engine HTTP bridge (45 min)
Pricing decisions in gigaton-engine bypass governance.

Add `decision-engine/integration/gigaton_client.py` mirroring the GigatonPricingClient pattern:
```python
# Calls gigaton-engine /pricing/calculate
# Returns margin_ok, floor_price, recommended_price
# If margin_ok=False → auto-creates a BLOCK decision record
# If margin_ok=True → creates EXECUTE decision record for audit trail
```
Wire into gigaton-engine's pricing handler:
```python
# After price calculation, POST the result to decision-engine:
decision_client.record_pricing_decision(
    pricing_result=result,
    domain="pricing",
    title=f"Price quote: {product_name}",
)
```

### Step 4.3 — B-03: DAG coefficients from xlsx (30 min)
`gigaton_playa_roisummary.xlsx` lives at `~/Desktop` or `~/Downloads`, not in the repo.
Two-step fix:
1. Copy xlsx to `gigaton-engine/data/gigaton_playa_roisummary.xlsx` and add to `.gitignore` if sensitive, or commit if it contains no PII.
2. Create `gigaton-engine/scripts/calibrate_dag.py` that reads the xlsx and outputs updated `ConversionCoeffs`/`OccupancyCoeffs` Python literals to copy into `dag_model.py`.

Or simpler: add a `data/dag_coefficients.json` that the DAG loads at startup via env var `DAG_COEFFICIENTS_PATH`.

### Step 4.4 — B-10: Implement 4 remaining MAJ drift rule handlers (45 min)
Currently at 41% handler coverage. These 4 bring it to ~56%:
- **MAJ-001** (capability shipment without telemetry)
- **MAJ-006** (schema changes without migration)
- **MAJ-009** (phase gate violation)
- **MAJ-010** (gigent value chain breaks)

Each handler follows the same pattern established in `drift_sentinel/drift_scan.py`.

### Step 4.5 — B-12: GH_TOKEN secret for drift sentinel (10 min)
```bash
# Create GitHub PAT with repo + read:org scopes at github.com/settings/tokens
# Then:
gcloud secrets create drift-gh-token --replication-policy=automatic
echo -n "ghp_..." | gcloud secrets versions add drift-gh-token --data-file=-
# Update drift-sentinel Cloud Run job to use it
gcloud run jobs update drift-sentinel \
  --set-secrets=GH_TOKEN=drift-gh-token:latest \
  --region=us-central1
```

**End of Day 4:** All three core services talk to each other. Drift sentinel has GitHub access. Intelligence weights flow from engine → silo.

---

## DAY 5 — Shared Memory + Matt's Access
**Goal: Matt at matt@gigaton.ai can query platform intelligence in natural language**

### Step 5.1 — Ingest all platform docs into silo semantic index (30 min)
With the silo deployed and `ingest_docs.py` live:
```bash
# Ingest architecture docs
python scripts/ingest_docs.py \
  ../decision-engine/docs/ \
  ../decision-engine/MASTER_FIRST_PRINCIPLES_REFERENCE.md \
  --silo-url https://intelligence-silo-HASH-uc.a.run.app \
  --category doctrine \
  --author todd@gigaton.ai

# Ingest architecture
python scripts/ingest_docs.py \
  ../decision-engine/docs/architecture/MASTER_ARCHITECTURE.md \
  --category architecture \
  --author todd@gigaton.ai

# Ingest all CLAUDE.md files (operating guides)
python scripts/ingest_docs.py \
  ../decision-engine/CLAUDE.md \
  ../gigaton-engine/CLAUDE.md \
  ../sales-operating-system/CLAUDE.md \
  ../intelligence-silo/CLAUDE.md \
  --category operations \
  --author todd@gigaton.ai
```

### Step 5.2 — Enable GCS sync so index is shared (15 min)
In `intelligence-silo/config/silo.yaml`:
```yaml
google:
  enabled: true
  gcs:
    bucket: gigaton-silo-data
    sync_path: intelligence-silo/shared-memory
```
Or set via Cloud Run env var: `GCS_BUCKET=gigaton-silo-data`.
After this, any node that connects to the same GCS bucket syncs the full semantic index automatically.

### Step 5.3 — Create Matt's access token (15 min)
Intelligence silo uses `--no-allow-unauthenticated`. Matt needs a service account or identity token:
```bash
# Option A: Give Matt a service account with invoker role
gcloud iam service-accounts create matt-silo-invoker \
  --display-name="Matt Silo Invoker"
gcloud run services add-iam-policy-binding intelligence-silo \
  --region=us-central1 \
  --member="serviceAccount:matt-silo-invoker@PROJECT.iam.gserviceaccount.com" \
  --role="roles/run.invoker"
# Generate key, share with Matt
gcloud iam service-accounts keys create matt-key.json \
  --iam-account=matt-silo-invoker@PROJECT.iam.gserviceaccount.com

# Option B (simpler): Add --allow-unauthenticated on /memory/search only
# via a lightweight proxy or Cloud Endpoints policy
```

### Step 5.4 — Write Matt's quick-start guide (20 min)
Location: `master-knowledge-base/docs/MATT_QUICKSTART.md`

```markdown
# Querying Platform Intelligence

Base URL: https://intelligence-silo-HASH-uc.a.run.app

## Search shared memory (plain text question)
POST /memory/search
Authorization: Bearer <your-token>
{
  "query": "how does the decision engine work?",
  "top_k": 5
}

## Categories to filter by
- doctrine       — first principles, non-negotiables
- architecture   — system design, connections
- operations     — how to operate each service
- playbook       — sales and delivery processes

## Add knowledge (ingest a doc)
POST /memory/ingest
{
  "text": "...",
  "source": "my-doc.md",
  "category": "playbook",
  "author": "matt@gigaton.ai"
}
```

### Step 5.5 — Wire daily ingest into deploy_19.sh (15 min)
After each deploy, re-ingest any changed docs:
```bash
# In deploy_19.sh, add after health checks:
echo "→ Syncing docs to shared memory..."
python3 "$GH_ROOT/intelligence-silo/scripts/ingest_docs.py" \
  "$GH_ROOT/decision-engine/docs/" \
  --silo-url "$SILO_URL" \
  --category doctrine \
  --author todd@gigaton.ai
```
This means every deployment automatically keeps the shared knowledge base current.

**End of Day 5:** Matt can hit the silo with a plain English question and get cited answers from the architecture docs, doctrine, and operating guides.

---

## DAY 6 — Bella-Byte Integration + SIE Policy Wire
**Goal: Bella has access to shared memory + SIE policy enforces POLICY.md**

### Step 6.1 — Define bella-byte scope (30 min)
The `bella-byte` repo is a placeholder. Define it now:
- Role: Bella is the platform's AI agent persona — she handles customer-facing interactions, lead qualification, content generation, and knowledge sharing
- `bella-byte` repo: her system prompt, operating config, and knowledge base
- She queries the silo for context on every interaction
- Her actions go through the SIE approval queue (per POLICY.md)

Write `bella-byte/CLAUDE.md` with this scope, then add a `bella-byte/config/persona.yaml`.

### Step 6.2 — Wire POLICY.md into SIE intake (45 min)
The SIE approval queue currently has no policy filter at intake.

Add a policy check at the SIE operator-api before any action enters the queue:
```python
def check_policy(action_type: str) -> tuple[str, bool]:
    """Returns (disposition, requires_approval)"""
    policy = load_policy()  # reads config/policy.yaml
    if action_type in policy["prohibited"]:
        return ("blocked", False)
    if action_type in policy["approval_required"]:
        return ("queued", True)
    if action_type in policy["autonomous_execution"]:
        return ("auto_execute", False)
    return ("queued", True)  # default: queue everything unknown
```

### Step 6.3 — Transcript KB: wire all 9 credentials (45 min)
From `project_transcript_kb.md` — 9 credentials still needed:
```bash
# GitHub PAT with workflow scope
gh secret set GITHUB_PAT --body="ghp_..."

# Zoom Server-to-Server OAuth
gh secret set ZOOM_ACCOUNT_ID --body="..."
gh secret set ZOOM_CLIENT_ID --body="..."
gh secret set ZOOM_CLIENT_SECRET --body="..."

# Fireflies
gh secret set FIREFLIES_API_KEY --body="..."

# Notion
gh secret set NOTION_TOKEN --body="..."

# ClickUp
gh secret set CLICKUP_API_TOKEN --body="..."

# Google Drive folder
python3 scripts/create_drive_folder.py
```
Then run historical backfill:
```bash
python3 scripts/backfill.py --since 2025-01-01
```

**End of Day 6:** Bella has a defined scope + silo access. SIE enforces POLICY.md at intake. Transcript KB is fully wired.

---

## DAY 7 — Desktop Bundles → Repos
**Goal: 6 priority Desktop bundles committed to the repos that govern them**

### Step 7.1 — claude_gigaton_standalone_project/specs → master-knowledge-base (20 min)
Copy specs to `master-knowledge-base/specs/`:
- `SYSTEM_ARCHITECTURE.md` → `specs/SYSTEM_ARCHITECTURE.md`
- `DECISION_ENGINE_SPEC.md` → `specs/DECISION_ENGINE_SPEC.md`
- `PRODUCTIZATION_PLAN.md` → `specs/PRODUCTIZATION_PLAN.md`
- `INTEGRATION_MAP.md` → `specs/INTEGRATION_MAP.md`
- `CONNECTIVITY_REQUIREMENTS.md`, `PLATFORM_UI_MVP.md`, `SYSTEM_INVENTORY.md`, `TECH_STACK_DECISION.md`

Commit + ingest into silo memory: `--category architecture`.

### Step 7.2 — gigaton_enterprise_onboarding_v2 → master-knowledge-base (20 min)
Copy to `master-knowledge-base/onboarding/`:
- `enterprise_onboarding_strategy.md`
- `last_mile_build_process.md` (SLA doc — 24-72h build commitment)
- `deployment_guide.md`
- `api_contracts.md`

Commit + ingest: `--category playbook`.

### Step 7.3 — gigaton_claude_custom_language_repo_v3 → new repo (45 min)
This has implementation-ready Python source code. Create a proper repo:
```bash
gh repo create todd-gig/gigaton-language --private
# Copy src/, schemas/, docs/, pyproject.toml
# Write CLAUDE.md, add CODEOWNERS
git push
```
Then ingest the architecture docs: `--category architecture`.

### Step 7.4 — gigaton_sie_first_production_bundle_v1 → decision-engine/sie (30 min)
The SIE bundle has JSON schemas, Python scaffolds, and execution plans.
Copy to `decision-engine/sie/`:
- `04_schemas/` → `sie/schemas/`
- `07_repo_scaffold/` → `sie/scaffold/`
- `06_execution_plan/72_hour_plan.md` → `sie/SPRINT_PLAN.md`

Commit + ingest.

### Step 7.5 — claude_brand_interaction_system → decision-engine/docs (20 min)
Brand interaction system specs (dashboards, forecasting, deployment sequence) belong in decision-engine as they define what the engine produces.
Copy to `decision-engine/docs/brand-interaction/`.
Commit + ingest: `--category architecture`.

**End of Day 7:** All 6 priority Desktop bundles are in repos, committed, and queryable via the silo.

---

## DAY 8 — Knowledge Surface + Docs Site
**Goal: shared memory is queryable by all users, docs site live**

### Step 8.1 — Launch docs.gigaton.ai (45 min)
Using mkdocs-material in a Docker container (fits the same deploy pipeline as everything else):
```dockerfile
FROM squidfunk/mkdocs-material
COPY docs/ /docs/
```
```yaml
# cloudbuild.yaml for docs service
steps:
  - name: gcr.io/cloud-builders/docker
    args: ["build", "-t", "gcr.io/$PROJECT_ID/gigaton-docs:$COMMIT_SHA", "."]
  - name: gcr.io/cloud-builders/gcloud
    args: ["run", "deploy", "gigaton-docs", "--image", "gcr.io/$PROJECT_ID/gigaton-docs:$COMMIT_SHA",
           "--region", "us-central1", "--allow-unauthenticated"]  # docs are public
```
Source the docs from the auto-generated mkdocs.yml pointing at:
- `master-knowledge-base/` (principles, policy, process)
- `decision-engine/docs/` (architecture, doctrine)
- `master-knowledge-base/docs/` (Matt quickstart, Bella guide)

### Step 8.2 — Add /memory/search to daily standup output (20 min)
Create `scripts/morning_brief.sh` — runs at the start of each work day, queries the silo for:
```bash
# Pending decisions in SIE queue
/sie-pending

# Yesterday's deploy log entry
tail -1 master-knowledge-base/deploy-log.jsonl

# Any open critical drift
python3 decision-engine/drift_sentinel/drift_scan.py --quick-check

# Memory search: "what changed yesterday"
curl -s POST https://silo.../memory/search \
  -d '{"query": "what was deployed yesterday", "top_k": 3}'
```

### Step 8.3 — Bulk ingest all remaining high-value Desktop docs (30 min)
Run ingest_docs.py against all remaining priority Desktop bundles:
```bash
python scripts/ingest_docs.py \
  ~/Desktop/gigaton_enterprise_onboarding_v2/ \
  ~/Desktop/claude_brand_interaction_system/ \
  ~/Desktop/gigaton_v3_execution/UNIFIED_DECISION_ENGINE_INTEGRATION.md \
  --silo-url $SILO_URL \
  --category playbook
```

**End of Day 8:** docs.gigaton.ai is live. Morning brief script runs. All priority docs ingested.

---

## DAY 9 — Open Blockers + Carmen Beach
**Goal: close B-06, B-07, B-11 + transcript KB backfill**

### Step 9.1 — B-06: Carmen Beach branch merge (operator decision required)
**Need explicit go-ahead to merge `add-chatgpt-snippets-carmen` → main.**
main has 2 commits not in the branch. Options:
- **Recommended:** `git merge main` into the feature branch first to pick up the 2 commits, then PR + squash merge.
- Alternative: cherry-pick the 2 main commits onto the feature branch.

### Step 9.2 — B-07: SendGrid adapter for Carmen Beach notifications (45 min)
```bash
# In Carmen-Beach-Properties/packages/automation/:
# Create packages/automation/src/adapters/sendgrid.ts
# POST /api/inquiries triggers SendGrid transactional email
# Env vars needed: SENDGRID_API_KEY, FROM_EMAIL, ADMIN_EMAIL
```

### Step 9.3 — B-11: Drive + ClickUp adapters for Drift Sentinel (45 min)
`drift_sentinel/drift_scan.py` has stub adapters for Drive and ClickUp.
Implement:
- `DriveAdapter`: uses `google-auth` + `google-api-python-client` to search recent Drive files for drift signals
- `ClickUpAdapter`: uses ClickUp API to check for tasks tagged as technical debt or doctrine violations

### Step 9.4 — Transcript KB backfill (30 min)
After credentials are wired (Day 6):
```bash
python3 scripts/backfill.py --since 2025-01-01
```
Fix the `daily_report.py` Slack posting: change to draft-only (per doctrine — Slack sends require human approval):
```python
# Instead of posting directly, create a draft message
slack_client.create_canvas(channel=CHANNEL, content=report_text)
# Or simply write to Cloud Logging + send via Gmail draft
```

**End of Day 9:** Carmen Beach blockers cleared. Drift Sentinel has full 5-source coverage. Transcript KB is backfilled.

---

## DAY 10 — Automation + Archive + Handoff
**Goal: the system runs itself. Archive stale repos. Complete handoff to Bella.**

### Step 10.1 — Complete deploy_19.sh automation (30 min)
Final additions to the deploy ritual:
- Post a Slack draft (not send) with deploy summary
- Write to deploy-log.jsonl with all service health statuses
- Send email confirmation via Gmail draft
- Update `SERVICES.md` with current URLs automatically

### Step 10.2 — Archive stale repos (20 min)
Mark as archived on GitHub:
```bash
for repo in Gigaton-UI-Platform liquifex gigaton-data-lake; do
  gh repo archive todd-gig/$repo
done
```
Add `README.md` note: "Archived 2026-05-16. Superseded by [new repo]."

### Step 10.3 — B-04 completion: weight sync in daily deploy (15 min)
Add to deploy_19.sh:
```bash
# After intelligence-silo deploys, trigger weight sync
curl -s -X POST "$SILO_URL/memory/consolidate" \
  -H "Authorization: Bearer $(gcloud auth print-identity-token)"
```

### Step 10.4 — Final drift sentinel scan (15 min)
Run the full scan across all repos:
```bash
python3 decision-engine/drift_sentinel/drift_scan.py
```
Target: GREEN (0 critical, 0 major). Any remaining minors are triaged and either fixed or accepted with rationale.

### Step 10.5 — Update SERVICES.md with final deployed URLs (15 min)
Every service URL, port, health endpoint, and last deploy SHA documented.

### Step 10.6 — Write knowledge transfer bundle for Bella (30 min)
`master-knowledge-base/docs/BELLA_GUIDE.md`:
- How to query shared memory
- How to submit items to the SIE approval queue
- What she can execute autonomously vs. what needs Todd's approval
- Daily deploy ritual participation
- How to ingest new docs

**End of Day 10:** The system governs itself. One command deploys everything in < 15 minutes. Matt and Bella can query shared intelligence. All knowledge is ingested. All stale repos are archived.

---

# PROCESS FOUNDATION — DAILY RITUAL

Once established (after Day 3), every working day follows this ritual:

```
Morning (start of day):
  ./scripts/morning_brief.sh
    → SIE queue check
    → Yesterday's deploy status
    → Drift sentinel quick scan
    → "What changed yesterday" memory query

During day:
  Work on day's tasks per this plan
  All code changes via worktrees, PRs, not direct-to-main
  Any outbound action (email, Slack, price quote) → SIE queue first

19:00 CT (end of day):
  ./scripts/deploy_19.sh
    → Pre-flight: clean trees, time check, previous log green
    → Submit all 4 Cloud Builds in parallel
    → Wait for completion (~10-12 min)
    → Health check all services
    → Re-ingest changed docs to silo
    → Log entry in deploy-log.jsonl
    → Gmail draft with deploy summary

If deploy fails:
  Investigate → fix → re-run deploy_19.sh
  Do NOT go to bed with a red deploy
  If unfixable same day: rollback via gcloud run services update-traffic
```

---

# AUTOMATION TARGET: < 15 MINUTES

| Phase | Time | What |
|-------|------|------|
| Pre-flight checks | 30s | Clean trees, time check, auth token |
| Parallel Cloud Builds | 10-12 min | All 4 backends build + push + deploy simultaneously |
| Health checks | 30s | Curl /health on all services |
| Doc re-ingest | 60s | ingest_docs.py on changed files |
| Log + notify | 15s | deploy-log.jsonl + Gmail draft |
| **Total** | **~13 min** | Well under 15 min target |

---

# OPEN QUESTIONS (need answers to proceed)

| # | Question | Blocks |
|---|----------|--------|
| Q1 | Has the leaked GitHub PAT (`gho_sQlm...`) been rotated? | Day 1.1 |
| Q2 | What GCP project hosts the Gigaton API services? Is it `carmen-beach-properties` or a separate `gigaton-platform` project? | Day 3.1 |
| Q3 | Carmen Beach: go-ahead to merge `add-chatgpt-snippets-carmen` → main? | Day 9.1 |
| Q4 | Stripe architecture: direct charges vs. Connect marketplace? | B-09 |
| Q5 | bella-byte: confirm GitHub username is `@bella-byte` (for CODEOWNERS) | Day 2.1 |
| Q6 | Sales OS: GCS FUSE mount vs. Cloud SQL migration for SQLite persistence? | Day 3.3 |

---

# REFERENCE — ALL OPEN ITEMS BY PRIORITY

## 🔴 Must close by Day 5 (platform foundation)
- B-03: DAG coefficients from xlsx
- B-04: Silo weights import bridge
- B-05: Decision-engine ↔ gigaton-engine HTTP bridge
- Intelligence silo branch → main merge
- Sales OS seeder path fix
- Secret Manager secrets provisioned
- GCS buckets created

## 🟠 Must close by Day 8 (Beta 2.0 complete)
- B-07: SendGrid for Carmen Beach
- B-10: 4 remaining MAJ drift handlers (MAJ-001, -006, -009, -010)
- B-11: Drive + ClickUp adapters for Drift Sentinel
- B-12: GH_TOKEN in GCP
- M-03: Decision Engine test coverage (per-gate failure paths)
- M-04: Intelligence Silo integration tests
- Transcript KB: all 9 credentials + backfill

## 🟡 Close before Beta 2.1 (post this plan)
- B-06: Carmen Beach branch merge (waiting on operator decision)
- B-08: Google Drive sync for Carmen Beach
- B-09: Stripe Connect
- M-01: Carmen Beach 0 tests
- M-05/M-06/M-07: Carmen Beach Lead/Pricing/AI subsystem UIs
- M-08: Observability (Sentry/Datadog)
- M-09: Audit log surface
- M-11: SIE ↔ decision-engine shared schema
- M-12: cxguy-methodology wire-up

## Defer to Beta 2.1
- B-15: Platform frontend (Engine Artifact Doctrine)
- SIE cxguy-methodology full integration
- gignet_usage_billing_dashboard

---

*This document is the single source of truth for the 10-day plan. Update it daily.*
*Canonical location: `master-knowledge-base/MASTER_PROJECT_PLAN.md`*
*Last updated: 2026-05-07*
