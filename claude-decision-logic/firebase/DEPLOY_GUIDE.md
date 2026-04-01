# Decision Engine — Firebase Deployment Guide

## Prerequisites

1. **Node.js** 18+ (for Firebase CLI)
2. **Python** 3.12+ (for Cloud Functions runtime)
3. **Firebase CLI**: `npm install -g firebase-tools`
4. **An existing Firebase project** in the [Firebase Console](https://console.firebase.google.com)

## Quick Start (5 steps)

### Step 1: Configure your project ID

Edit `.firebaserc` and replace the placeholder with your actual Firebase project ID:

```json
{
  "projects": {
    "default": "your-actual-project-id"
  }
}
```

You can find your project ID in the Firebase Console → Project Settings → General.

### Step 2: Authenticate

```bash
firebase login
```

### Step 3: Enable required services

In the Firebase Console, enable:

- **Cloud Functions** (Blaze plan required — pay-as-you-go)
- **Firestore** (Native mode, not Datastore mode)
- **Hosting** (free tier is sufficient)

Or via CLI:

```bash
firebase experiments:enable webframeworks  # if prompted
```

### Step 4: Deploy

From the `firebase/` directory:

```bash
# Make the deploy script executable (first time only)
chmod +x deploy.sh

# Deploy everything
./deploy.sh

# Or deploy specific components
./deploy.sh functions    # Cloud Functions only
./deploy.sh firestore    # Rules + indexes only
./deploy.sh hosting      # Static site only
```

The deploy script automatically copies the engine package into `functions/engine/` before deploying.

### Step 5: Verify

```bash
# Health check
curl https://YOUR_PROJECT_ID.web.app/api/health

# Submit a test decision
curl -X POST https://YOUR_PROJECT_ID.web.app/api/v1/decisions/evaluate \
  -H "Content-Type: application/json" \
  -d '{
    "decision_id": "TEST-001",
    "title": "Test tactical decision",
    "decision_class": "D1",
    "owner": "test-user",
    "requested_action": "Validate deployment",
    "problem_statement": "Need to confirm Firebase deployment works",
    "value_scores": {
      "revenue_impact": 3,
      "cost_efficiency": 4,
      "time_leverage": 5,
      "strategic_alignment": 3,
      "customer_human_benefit": 3,
      "knowledge_asset_creation": 2,
      "compounding_potential": 3,
      "reversibility": 5,
      "downside_risk": 1,
      "execution_drag": 1,
      "uncertainty": 1,
      "ethical_misalignment": 0
    },
    "trust_scores": {
      "evidence_quality": 4,
      "logic_integrity": 4,
      "outcome_history": 3,
      "context_fit": 4,
      "stakeholder_clarity": 4,
      "risk_containment": 4,
      "auditability": 4
    }
  }'
```

## Local Development with Emulators

Firebase emulators let you test everything locally without touching production:

```bash
./deploy.sh emulators
```

This starts:

- Functions emulator on `http://localhost:5001`
- Firestore emulator on `http://localhost:8080`
- Hosting emulator on `http://localhost:5000`
- Emulator UI on `http://localhost:4000`

All API calls route through hosting → functions just like production.

## Architecture

```
Client Request
    ↓
Firebase Hosting (static landing page + /api/* rewrites)
    ↓
Cloud Function: api (Python 3.12, 512MB)
    ↓
Decision Engine Pipeline (12-stage processing)
    ↓
Firestore Persistence
    ├── decisions          (decision objects + results)
    ├── audit_records      (append-only audit trail)
    ├── certificates       (QC/VC/TC/EC chain)
    ├── learning_records   (post-execution variance)
    └── learning_summaries (daily aggregates)
```

### Firestore Triggers

- `on_decision_update`: Fires when any decision document is modified. Automatically logs state transitions to `audit_records`.

### Scheduled Functions

- `scheduled_learning_summary`: Runs daily at 6 AM UTC. Computes aggregate learning metrics and stores a digest in `learning_summaries`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/v1/config` | Engine configuration |
| POST | `/api/v1/decisions/evaluate` | Full pipeline evaluation |
| GET | `/api/v1/decisions` | List decisions (?class=D1&state=draft&limit=50) |
| GET | `/api/v1/decisions/history/{id}` | Decision + full audit trail |
| POST | `/api/v1/decisions/transition` | State machine validation |
| POST | `/api/v1/decisions/gap-analysis` | Gap analysis |
| POST | `/api/v1/learning/record` | Record learning outcome |
| GET | `/api/v1/learning/summary` | Aggregate learning metrics |

## Security

Firestore Security Rules enforce:

- **Authentication required** for all reads
- **Operator role** required for writes (decisions, learning records)
- **Admin role** required for deletes
- **Audit records are append-only** — no client updates or deletes
- **Learning summaries are write-protected** — only Cloud Functions (Admin SDK) can write

To set user roles, use Firebase Auth custom claims:

```python
from firebase_admin import auth
auth.set_custom_user_claims(uid, {"role": "operator"})
```

## Firestore Indexes

Pre-configured indexes (deployed via `firestore.indexes.json`):

- Decisions by class + created_at
- Decisions by lifecycle_state + priority_score
- Audit records by decision_id + timestamp
- Learning records by decision_class + applied
- Certificates by decision_id + cert_type + issued_at

## Cost Estimation (Blaze Plan)

For typical usage (< 1000 decisions/month):

- **Cloud Functions**: ~$0 (free tier: 2M invocations/month)
- **Firestore**: ~$0-2/month (free tier: 50K reads, 20K writes/day)
- **Hosting**: ~$0 (free tier: 10GB/month)

The engine is designed to be cost-efficient — each decision evaluation is a single function invocation with a small Firestore write batch.

## Troubleshooting

**"Functions deploy failed: Python version mismatch"**
→ Ensure `python312` is specified in `firebase.json` and your local Python is 3.12+.

**"Permission denied" on Firestore writes**
→ Check that the calling user has the correct custom claim (`role: "operator"`). Cloud Functions use the Admin SDK and bypass rules.

**"Module not found: engine"**
→ Run `./deploy.sh` instead of `firebase deploy` directly. The deploy script copies the engine package into `functions/`.

**Emulator data not persisting**
→ The `--export-on-exit` flag saves emulator data to `./emulator-data/`. Make sure the directory is writable.
