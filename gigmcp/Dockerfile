# gigmcp-industry-sync Cloud Run Job image
#
# Pattern mirrors decision-engine/Dockerfile but is intentionally
# minimal: no FastAPI / uvicorn / health server — this is a batch
# script invoked once per Cloud Scheduler tick. Entrypoint exits 0
# on success, non-zero on failure, and Cloud Run Job surfaces the
# exit code to Cloud Logging / Monitoring.

FROM python:3.12-slim

# tini handles SIGTERM cleanly when Cloud Run preempts a long-running
# job (the sync is typically <60s but a stuck HTTP retry could hold the
# process). Without tini the Python process inherits PID 1 and ignores
# default-action signals.
RUN apt-get update \
 && apt-get install -y --no-install-recommends tini \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps in their own layer so source changes don't bust
# the wheel cache.
COPY gigmcp/requirements.txt /app/gigmcp/requirements.txt
RUN pip install --no-cache-dir -r /app/gigmcp/requirements.txt

# Copy package source. Tests are deliberately included so an operator
# can `gcloud run jobs execute --override` with a debug entrypoint to
# run pytest inside the deployed image during a smoke verification.
COPY gigmcp/ /app/gigmcp/

# Non-root for least-privilege. Cloud Run already restricts container
# capabilities but this is belt-and-suspenders.
RUN useradd --uid 1000 --no-create-home --shell /usr/sbin/nologin gigmcp \
 && chown -R gigmcp:gigmcp /app
USER gigmcp

ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    LOG_LEVEL=INFO

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["python", "-m", "gigmcp.industry_sync"]
