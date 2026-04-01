# Decision Execution Engine

FastAPI service layer that converts decision governance logic into executable controls.

## What it does
- Accepts normalized decision objects
- Computes value and trust scores
- Evaluates authority, policy, and state transition rules
- Issues certificate states
- Returns `execute`, `escalate`, `block`, or `needs_data`
- Produces an auditable transition log

## Core flow
1. Ingest decision payload
2. Validate schema
3. Score value and trust
4. Evaluate policy gates
5. Route authority
6. Advance state machine
7. Emit execution packet

## Run
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Endpoints
- `GET /health`
- `GET /v1/config`
- `POST /v1/decisions/evaluate`
- `POST /v1/decisions/transition`

## Strategic note
This is the enforcement layer between markdown doctrine and real-world system actions.
