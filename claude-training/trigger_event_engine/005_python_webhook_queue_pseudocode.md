---
title: Python Webhook and Queue Pseudocode
tags: [python, webhooks, queues]
status: guide
---

# Python Webhook and Queue Pseudocode

```python
from fastapi import FastAPI, Request, HTTPException
from uuid import uuid4

app = FastAPI()

def enqueue_job(job: dict) -> None:
    # replace with Celery, Dramatiq, RQ, Arq, etc.
    pass

@app.post("/webhooks/external")
async def external_webhook(request: Request):
    payload = await request.json()

    event = {
        "event_id": payload.get("id", str(uuid4())),
        "event_type": payload.get("type", "unknown"),
        "payload": payload,
    }

    job = {
        "job_id": str(uuid4()),
        "job_type": "normalized_event_handler",
        "payload": event,
        "retry_count": 0,
        "correlation_id": event["event_id"],
    }

    enqueue_job(job)
    return {"status": "accepted", "event_id": event["event_id"]}
```
