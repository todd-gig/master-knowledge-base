"""gigmcp → decision-engine industry-catalog sync (Cloud Run Job).

ENTRYPOINT: `python -m gigmcp.industry_sync`

Wave 2 PR2 of Stage 5 variance-aware self-healing. PR1 (decision-engine
commit a7f0d7b) added the variance computation that consumes rows from
`industry_catalogs` (Wave 1 migration 004). This job is what keeps those
rows fresh from the canonical gigmcp surface.

EXECUTION MODEL:

    [Cloud Scheduler 03:00 UTC daily]
              │
              ▼  HTTP POST (OIDC-signed)
    [Cloud Run Job: gigmcp-industry-sync]
              │
              ├─── GET  ${GIGMCP_EXPORT_URL}/industries          (index)
              ├─── GET  ${GIGMCP_EXPORT_URL}/industries/{tag}    (per-industry)
              ├─── psycopg2 → /cloudsql/...:gigaton-engine-pg
              │           (decision-engine-pg, decision_engine DB,
              │            industry_catalogs table)
              └─── Cloud Monitoring custom metrics
                     custom.googleapis.com/gigmcp/sync/{
                         fetched,upserted,skipped_malformed,
                         unchanged,failed_industries }

CONFLICT RESOLUTION (per spec):
    UPSERT favors-newer keyed on (etag, source_updated_at).
    1. If no existing row at (operator_id='gigmcp:canonical',
       industry_slug, sub_vertical), INSERT.
    2. If existing row has source.etag == incoming etag, NO-OP
       (increment 'unchanged'). Idempotency invariant.
    3. If existing row has source.etag != incoming etag AND
       incoming source_updated_at > existing source_updated_at,
       UPDATE.
    4. If existing row is operator-submitted (no source block),
       NEVER overwrite — operators are the source of truth for
       their own rows. Increment 'preserved_operator'.

VERIFY-BEFORE-DEPLOY ITEMS (per spec §"What gigmcp is"):

  ☐ Confirm `gigmcp-export` Cloud Run service exists in
    gigaton-platform: `gcloud run services list --project=gigaton-platform | grep gigmcp`
    AS OF 2026-05-25 IT DOES NOT EXIST. This sync job cannot be
    smoke-tested end-to-end until that service is stood up. The job
    is configurable (GIGMCP_EXPORT_URL env var) and will exit non-zero
    cleanly if the source is unreachable, so it's safe to pre-deploy.

  ☐ Confirm gigmcp-sync-runtime SA exists with the IAM grants listed
    in runbooks/gigmcp_industry_sync.md.

  ☐ Confirm Cloud SQL instance gigaton-engine-pg is in gigaton-platform
    project (post-accelerated-migration). Pre-migration this points
    at carmen-beach-properties; sync env vars must change with the
    migration window.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional, Tuple

import requests

from gigmcp.translators.v1_to_industry_catalog import (
    GIGMCP_OPERATOR_ID,
    TranslationError,
    existing_row_etag,
    existing_row_source_updated_at,
    translate,
    validate_payload,
)

logger = logging.getLogger("gigmcp.industry_sync")
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

# ---- config ---------------------------------------------------------------

GIGMCP_EXPORT_URL = os.environ.get(
    "GIGMCP_EXPORT_URL",
    "",  # empty = will fail fast in main()
)
HTTP_TIMEOUT_SEC = int(os.environ.get("GIGMCP_HTTP_TIMEOUT_SEC", "30"))
HTTP_RETRIES = int(os.environ.get("GIGMCP_HTTP_RETRIES", "3"))
HTTP_RETRY_BACKOFF_SEC = float(os.environ.get("GIGMCP_HTTP_BACKOFF_SEC", "2.0"))

# Decision-engine Postgres. Cloud Run Job uses unix-socket path
# `/cloudsql/<conn-name>` mounted via --set-cloudsql-instances.
PG_HOST = os.environ.get("DECISION_ENGINE_DB_HOST", "")
PG_PORT = os.environ.get("DECISION_ENGINE_DB_PORT", "5432")
PG_DB = os.environ.get("DECISION_ENGINE_DB_NAME", "decision_engine")
PG_USER = os.environ.get("DECISION_ENGINE_DB_USER", "decision_engine")
PG_PASSWORD_SECRET = os.environ.get(
    "DECISION_ENGINE_DB_PASSWORD_SECRET", "decision-engine-pg"
)
GCP_PROJECT = os.environ.get(
    "GCP_PROJECT", os.environ.get("GOOGLE_CLOUD_PROJECT", "gigaton-platform")
)

HME_EVENT_TOPIC = os.environ.get("HME_EVENT_TOPIC", "")  # optional, no-op if unset

# ---- HTTP layer -----------------------------------------------------------


class GigmcpHTTPError(Exception):
    """Wraps any non-200 / timeout / connection error from gigmcp-export."""


def _http_get_with_retry(url: str) -> Dict[str, Any]:
    last_err: Optional[Exception] = None
    for attempt in range(1, HTTP_RETRIES + 1):
        try:
            resp = requests.get(url, timeout=HTTP_TIMEOUT_SEC)
            if resp.status_code == 200:
                return resp.json()
            # 4xx — non-retryable. 5xx — retryable.
            if 400 <= resp.status_code < 500:
                raise GigmcpHTTPError(
                    f"GET {url} returned {resp.status_code} (non-retryable): "
                    f"{resp.text[:200]}"
                )
            last_err = GigmcpHTTPError(
                f"GET {url} returned {resp.status_code} (attempt {attempt}/{HTTP_RETRIES})"
            )
        except requests.RequestException as e:
            last_err = GigmcpHTTPError(f"GET {url} raised {type(e).__name__}: {e}")
        if attempt < HTTP_RETRIES:
            time.sleep(HTTP_RETRY_BACKOFF_SEC * attempt)
    raise last_err  # type: ignore[misc]


def list_industries_to_sync(base_url: str) -> List[str]:
    """Calls gigmcp-export /industries which returns a JSON array of
    canonical industry tags. Empty array is valid (no industries known
    yet) — caller treats as soft failure (exit code 1, no exception)."""
    payload = _http_get_with_retry(f"{base_url.rstrip('/')}/industries")
    if isinstance(payload, dict) and "industries" in payload:
        return list(payload["industries"])  # tolerate {"industries": [...]} shape
    if isinstance(payload, list):
        return list(payload)
    raise GigmcpHTTPError(
        f"GET /industries returned unexpected shape: {type(payload).__name__}"
    )


def fetch_industry(base_url: str, industry_tag: str) -> Dict[str, Any]:
    return _http_get_with_retry(
        f"{base_url.rstrip('/')}/industries/{industry_tag}"
    )


# ---- DB layer -------------------------------------------------------------


def _read_db_password() -> str:
    """Returns the decision-engine PG password.

    Lookup order:
      1. Env var DECISION_ENGINE_DB_PASSWORD (CI / local override)
      2. Google Secret Manager projects/{GCP_PROJECT}/secrets/{PG_PASSWORD_SECRET}/versions/latest

    Raises on lookup failure — sync cannot proceed without DB auth.
    """
    direct = os.environ.get("DECISION_ENGINE_DB_PASSWORD")
    if direct:
        return direct
    # Lazy import — avoid hard dep when running unit tests with mocks
    from google.cloud import secretmanager  # type: ignore

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{GCP_PROJECT}/secrets/{PG_PASSWORD_SECRET}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("utf-8")


def connect_to_decision_engine_db():  # -> psycopg2.connection
    """Open a psycopg2 connection. Caller is responsible for closing."""
    import psycopg2  # lazy — keeps unit tests free of native deps
    import psycopg2.extras

    if not PG_HOST:
        raise RuntimeError(
            "DECISION_ENGINE_DB_HOST is not set; refusing to connect"
        )
    password = _read_db_password()
    # Unix-socket detection: Cloud SQL connector exposes /cloudsql/<name>;
    # psycopg2 treats this as a directory containing socket files.
    if PG_HOST.startswith("/"):
        dsn = (
            f"host={PG_HOST} dbname={PG_DB} user={PG_USER} password={password}"
        )
    else:
        dsn = (
            f"host={PG_HOST} port={PG_PORT} dbname={PG_DB} "
            f"user={PG_USER} password={password}"
        )
    conn = psycopg2.connect(dsn)
    conn.autocommit = False
    return conn


# ---- upsert ---------------------------------------------------------------

UPSERT_RESULT_INSERTED = "upserted"
UPSERT_RESULT_UPDATED = "upserted"  # both flow into the same metric bucket
UPSERT_RESULT_UNCHANGED = "unchanged"
UPSERT_RESULT_PRESERVED_OPERATOR = "preserved_operator"


def upsert_industry_catalog_row(
    conn,
    row: Dict[str, Any],
) -> str:
    """Apply favor-newer conflict resolution. Returns one of the
    UPSERT_RESULT_* sentinels above. Commits its own transaction so
    one bad row doesn't poison the rest of the sync.

    The row dict comes from translators.v1_to_industry_catalog.translate()
    and includes two non-column fields: `_source_etag` and
    `_source_updated_at` used only for the conflict check.
    """
    import psycopg2.extras

    incoming_etag = row["_source_etag"]
    incoming_updated_at = row["_source_updated_at"]

    industry_slug = row["industry_slug"]
    sub_vertical = row.get("sub_vertical")  # NULL allowed

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(
            """
            SELECT catalog_id, catalog_json, submitted_by_user_id::text
              FROM industry_catalogs
             WHERE operator_id = %s
               AND industry_slug = %s
               AND (sub_vertical IS NOT DISTINCT FROM %s)
             FOR UPDATE
            """,
            (GIGMCP_OPERATOR_ID, industry_slug, sub_vertical),
        )
        existing = cur.fetchone()

        if existing is None:
            cur.execute(
                """
                INSERT INTO industry_catalogs (
                    operator_id, industry_slug, sub_vertical,
                    catalog_json, confidence_score, seed_for_industry,
                    submitted_by_user_id, multi_axis_tags
                ) VALUES (
                    %s, %s, %s, %s::jsonb, %s, %s, %s::uuid, %s::jsonb
                )
                """,
                (
                    row["operator_id"],
                    row["industry_slug"],
                    row["sub_vertical"],
                    json.dumps(row["catalog_json"]),
                    row["confidence_score"],
                    row["seed_for_industry"],
                    row["submitted_by_user_id"],
                    json.dumps(row["multi_axis_tags"]),
                ),
            )
            conn.commit()
            return UPSERT_RESULT_INSERTED

        # Existing row. Conflict-resolution gate.
        existing_json = existing["catalog_json"]
        if isinstance(existing_json, str):
            # Some drivers return JSONB as str
            existing_json = json.loads(existing_json)

        existing_etag = existing_row_etag(existing_json)
        existing_updated_at = existing_row_source_updated_at(existing_json)

        # Operator-submitted rows have no source block → never overwrite
        if existing_etag is None and existing_updated_at is None:
            conn.commit()  # release row lock
            return UPSERT_RESULT_PRESERVED_OPERATOR

        # Same etag → idempotent no-op
        if existing_etag == incoming_etag:
            conn.commit()
            return UPSERT_RESULT_UNCHANGED

        # Different etag → favor newer source_updated_at
        if existing_updated_at and incoming_updated_at <= existing_updated_at:
            conn.commit()
            return UPSERT_RESULT_UNCHANGED

        # Newer payload wins
        cur.execute(
            """
            UPDATE industry_catalogs
               SET catalog_json = %s::jsonb,
                   confidence_score = %s,
                   multi_axis_tags = %s::jsonb,
                   submitted_at = NOW()
             WHERE catalog_id = %s
            """,
            (
                json.dumps(row["catalog_json"]),
                row["confidence_score"],
                json.dumps(row["multi_axis_tags"]),
                existing["catalog_id"],
            ),
        )
        conn.commit()
        return UPSERT_RESULT_UPDATED


# ---- metrics + events -----------------------------------------------------


def write_metric(metrics: Dict[str, int]) -> None:
    """Emit each counter as a Cloud Monitoring custom metric.
    Best-effort — metric failure must NOT fail the sync."""
    try:
        from google.cloud import monitoring_v3  # type: ignore
    except ImportError:
        logger.warning("google-cloud-monitoring not installed; skipping metric emit")
        return
    try:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{GCP_PROJECT}"
        now = time.time()
        seconds = int(now)
        nanos = int((now - seconds) * 1e9)
        interval = monitoring_v3.TimeInterval(
            {"end_time": {"seconds": seconds, "nanos": nanos}}
        )
        for key, value in metrics.items():
            series = monitoring_v3.TimeSeries()
            series.metric.type = f"custom.googleapis.com/gigmcp/sync/{key}"
            series.resource.type = "global"
            series.resource.labels["project_id"] = GCP_PROJECT
            point = monitoring_v3.Point(
                {"interval": interval, "value": {"int64_value": int(value)}}
            )
            series.points = [point]
            client.create_time_series(
                request={"name": project_name, "time_series": [series]}
            )
    except Exception as e:  # noqa: BLE001
        logger.warning("metric emit failed: %s", e)


def emit_hme_event(event_type: str, payload: Dict[str, Any]) -> None:
    """Emit an HME event via Pub/Sub. Mirrors the AX-008 sweep pattern.
    Topic configured via HME_EVENT_TOPIC env var; if unset, no-op."""
    if not HME_EVENT_TOPIC:
        logger.info("HME_EVENT_TOPIC unset; would emit %s %s", event_type, payload)
        return
    try:
        from google.cloud import pubsub_v1  # type: ignore
    except ImportError:
        logger.warning("google-cloud-pubsub not installed; skipping HME emit")
        return
    try:
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(GCP_PROJECT, HME_EVENT_TOPIC)
        msg = json.dumps(
            {
                "event_type": event_type,
                "source": "gigmcp-industry-sync",
                "emitted_at": datetime.now(timezone.utc).isoformat(),
                "payload": payload,
            }
        ).encode("utf-8")
        publisher.publish(topic_path, msg).result(timeout=10)
    except Exception as e:  # noqa: BLE001
        logger.warning("HME event emit failed: %s", e)


# ---- main -----------------------------------------------------------------


def run_sync(
    *,
    base_url: str,
    conn,
    industries: Optional[Iterable[str]] = None,
) -> Dict[str, int]:
    """Pure-sync orchestrator — accepts an already-opened conn so tests
    can pass a mock. Returns the metrics dict.

    If `industries` is None, fetches the index from gigmcp-export.
    """
    metrics = {
        "fetched": 0,
        "upserted": 0,
        "unchanged": 0,
        "preserved_operator": 0,
        "skipped_malformed": 0,
        "failed_industries": 0,
    }

    if industries is None:
        industries = list_industries_to_sync(base_url)
    industries = list(industries)

    fetched_at = datetime.now(timezone.utc).isoformat()

    for industry_tag in industries:
        try:
            payload = fetch_industry(base_url, industry_tag)
        except GigmcpHTTPError as e:
            logger.warning("fetch_industry(%s) failed: %s", industry_tag, e)
            metrics["failed_industries"] += 1
            emit_hme_event(
                "GigmcpSyncFetchFailed",
                {"industry_tag": industry_tag, "error": str(e)},
            )
            continue

        try:
            validate_payload(payload)
        except TranslationError as e:
            logger.warning(
                "validate_payload(%s) failed: %s", industry_tag, e
            )
            metrics["skipped_malformed"] += 1
            emit_hme_event(
                "GigmcpSyncMalformed",
                {"industry_tag": industry_tag, "error": str(e)},
            )
            continue

        try:
            row = translate(
                payload,
                source_url=f"{base_url.rstrip('/')}/industries/{industry_tag}",
                fetched_at=fetched_at,
            )
            result = upsert_industry_catalog_row(conn, row)
            metrics[result] = metrics.get(result, 0) + 1
            metrics["fetched"] += 1
        except Exception as e:  # noqa: BLE001
            # Any DB / translation error on a single industry must not
            # poison the rest of the run. Roll back this row's txn so the
            # connection stays usable for the next iteration.
            try:
                conn.rollback()
            except Exception:  # noqa: BLE001
                pass
            logger.exception(
                "upsert failed for industry %s; continuing", industry_tag
            )
            metrics["failed_industries"] += 1
            emit_hme_event(
                "GigmcpSyncUpsertFailed",
                {"industry_tag": industry_tag, "error": str(e)},
            )
            continue

    return metrics


def main() -> int:
    if not GIGMCP_EXPORT_URL:
        logger.error(
            "GIGMCP_EXPORT_URL is not set; cannot proceed. See spec §verify-before-deploy."
        )
        return 2

    started_at = datetime.now(timezone.utc)
    logger.info(
        "gigmcp-industry-sync starting source=%s project=%s",
        GIGMCP_EXPORT_URL,
        GCP_PROJECT,
    )

    try:
        conn = connect_to_decision_engine_db()
    except Exception as e:  # noqa: BLE001
        logger.exception("DB connect failed: %s", e)
        emit_hme_event(
            "GigmcpSyncStartFailed",
            {"phase": "db_connect", "error": str(e)},
        )
        return 3

    try:
        try:
            metrics = run_sync(base_url=GIGMCP_EXPORT_URL, conn=conn)
        except GigmcpHTTPError as e:
            logger.exception("index fetch failed: %s", e)
            emit_hme_event(
                "GigmcpSyncStartFailed",
                {"phase": "index_fetch", "error": str(e)},
            )
            return 4
    finally:
        try:
            conn.close()
        except Exception:  # noqa: BLE001
            pass

    duration_sec = (datetime.now(timezone.utc) - started_at).total_seconds()
    metrics["duration_sec"] = int(duration_sec)

    write_metric(metrics)
    emit_hme_event("GigmcpSyncCompleted", metrics)
    logger.info("gigmcp-industry-sync completed metrics=%s", metrics)

    # Exit non-zero if we didn't actually sync anything — Cloud Scheduler
    # will surface this as a failed execution and page on alert policies.
    return 0 if metrics["fetched"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
