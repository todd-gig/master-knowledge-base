"""Tests for gigmcp.industry_sync.

Run from master-knowledge-base/ root:
    python3 -m pytest gigmcp/tests/

These tests use a fake in-memory store and a fake HTTP layer so they
require neither psycopg2 nor live GCP. The integration smoke is the
ad-hoc `gcloud run jobs execute` documented in
runbooks/gigmcp_industry_sync.md — not asserted here.

Each test is small + opinionated about the invariant under test.
"""
from __future__ import annotations

import json
import unittest
from typing import Any, Dict, List, Optional
from unittest.mock import patch

from gigmcp import industry_sync
from gigmcp.translators.v1_to_industry_catalog import (
    GIGMCP_OPERATOR_ID,
    GIGMCP_SENTINEL_UUID,
    existing_row_etag,
    existing_row_source_updated_at,
)


# ---------------------------------------------------------------------------
# Fake DB connection — mimics just enough of psycopg2's surface so the
# upsert SQL paths run in pure Python. We don't care about the SQL strings;
# we care about the favor-newer/idempotency invariants.
# ---------------------------------------------------------------------------

class FakeCursor:
    def __init__(self, store: "FakeStore"):
        self._store = store
        self._last_select_key: Optional[tuple] = None
        self._last_select_result: Optional[dict] = None

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def execute(self, sql: str, params=()):
        sql_lower = sql.strip().lower()
        if sql_lower.startswith("select"):
            # match SELECT ... FROM industry_catalogs WHERE op/slug/sub
            self._last_select_key = (params[0], params[1], params[2])
            self._last_select_result = self._store.find(*self._last_select_key)
        elif sql_lower.startswith("insert"):
            (
                operator_id,
                industry_slug,
                sub_vertical,
                catalog_json,
                confidence_score,
                seed_for_industry,
                submitted_by_user_id,
                multi_axis_tags,
            ) = params
            self._store.insert(
                operator_id=operator_id,
                industry_slug=industry_slug,
                sub_vertical=sub_vertical,
                catalog_json=json.loads(catalog_json),
                confidence_score=confidence_score,
                seed_for_industry=seed_for_industry,
                submitted_by_user_id=submitted_by_user_id,
                multi_axis_tags=json.loads(multi_axis_tags),
            )
        elif sql_lower.startswith("update"):
            catalog_json, confidence_score, multi_axis_tags, catalog_id = params
            self._store.update(
                catalog_id=catalog_id,
                catalog_json=json.loads(catalog_json),
                confidence_score=confidence_score,
                multi_axis_tags=json.loads(multi_axis_tags),
            )
        else:
            raise AssertionError(f"unexpected SQL: {sql_lower[:60]}")

    def fetchone(self):
        return self._last_select_result


class FakeConn:
    def __init__(self, store: "FakeStore"):
        self._store = store
        self.committed = 0
        self.rolled_back = 0
        self.closed = False
        self.autocommit = False

    def cursor(self, cursor_factory=None):
        return FakeCursor(self._store)

    def commit(self):
        self.committed += 1

    def rollback(self):
        self.rolled_back += 1

    def close(self):
        self.closed = True


class FakeStore:
    def __init__(self):
        self.rows: List[Dict[str, Any]] = []
        self._next_id = 1

    def find(self, operator_id, industry_slug, sub_vertical):
        for r in self.rows:
            if (
                r["operator_id"] == operator_id
                and r["industry_slug"] == industry_slug
                and r["sub_vertical"] == sub_vertical
            ):
                return {
                    "catalog_id": r["catalog_id"],
                    "catalog_json": r["catalog_json"],
                    "submitted_by_user_id": r["submitted_by_user_id"],
                }
        return None

    def insert(self, **row):
        row["catalog_id"] = f"row-{self._next_id}"
        self._next_id += 1
        self.rows.append(row)

    def update(self, *, catalog_id, catalog_json, confidence_score, multi_axis_tags):
        for r in self.rows:
            if r["catalog_id"] == catalog_id:
                r["catalog_json"] = catalog_json
                r["confidence_score"] = confidence_score
                r["multi_axis_tags"] = multi_axis_tags
                return
        raise AssertionError(f"no row {catalog_id}")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_payload(
    industry_tag: str = "vacation-rental-hospitality",
    *,
    etag: str = "sha256:v1",
    updated_at: str = "2026-05-25T03:00:00Z",
    processes=None,
    sub_vertical=None,
) -> Dict[str, Any]:
    return {
        "industry_tag": industry_tag,
        "sub_vertical": sub_vertical,
        "processes": processes
        if processes is not None
        else [
            {
                "name": "booking",
                "description": "guest-facing reservation",
                "field_type": "numeric",
                "distribution_stats": {"mean": 4.2, "stddev": 1.1, "n": 250},
            },
            {
                "name": "checkin",
                "description": "key handoff + verification",
                "field_type": "free_text",
            },
        ],
        "signals": [
            {
                "name": "guest_friction",
                "definition": "delta between expectation and reality",
                "observable_proxies": ["NPS", "complaints"],
            }
        ],
        "etag": etag,
        "updated_at": updated_at,
        "multi_axis_tags": ["geo:NA", "regime:established"],
    }


# ---------------------------------------------------------------------------
# Test 1 — sync_idempotent
# Running twice with the same gigmcp snapshot produces same row count + no
# duplicates. Second run's only effect is incrementing 'unchanged'.
# ---------------------------------------------------------------------------

class TestSyncIdempotent(unittest.TestCase):
    def test_running_twice_does_not_create_duplicates(self):
        store = FakeStore()
        conn = FakeConn(store)
        payload = make_payload()

        def fake_fetch(base_url, tag):
            return payload

        with patch.object(industry_sync, "fetch_industry", side_effect=fake_fetch):
            m1 = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["vacation-rental-hospitality"],
            )
            m2 = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["vacation-rental-hospitality"],
            )

        # Same row count after both runs
        self.assertEqual(len(store.rows), 1)
        # First run inserted, second run was no-op
        self.assertEqual(m1["upserted"], 1)
        self.assertEqual(m1["unchanged"], 0)
        self.assertEqual(m2["upserted"], 0)
        self.assertEqual(m2["unchanged"], 1)


# ---------------------------------------------------------------------------
# Test 2 — conflict_resolution_favors_newer
# Pre-seed row with older updated_at; gigmcp returns newer → row overwritten.
# Reverse: pre-seed newer; gigmcp older → row preserved.
# ---------------------------------------------------------------------------

class TestConflictResolutionFavorsNewer(unittest.TestCase):
    def test_newer_etag_with_newer_updated_at_wins(self):
        store = FakeStore()
        # Seed an older gigmcp-sourced row
        store.insert(
            operator_id=GIGMCP_OPERATOR_ID,
            industry_slug="agency-marketing",
            sub_vertical=None,
            catalog_json={
                "processes": [{"name": "old"}],
                "source": {
                    "provider": "gigmcp",
                    "etag": "sha256:old",
                    "source_updated_at": "2026-05-01T00:00:00Z",
                    "fetched_at": "2026-05-01T00:00:00Z",
                },
            },
            confidence_score=0.85,
            seed_for_industry=True,
            submitted_by_user_id=GIGMCP_SENTINEL_UUID,
            multi_axis_tags=[],
        )
        conn = FakeConn(store)
        payload = make_payload(
            "agency-marketing",
            etag="sha256:new",
            updated_at="2026-05-25T03:00:00Z",
        )
        with patch.object(
            industry_sync, "fetch_industry", side_effect=lambda u, t: payload
        ):
            metrics = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["agency-marketing"],
            )
        self.assertEqual(metrics["upserted"], 1)
        self.assertEqual(len(store.rows), 1)
        # Row now has new etag
        self.assertEqual(
            existing_row_etag(store.rows[0]["catalog_json"]), "sha256:new"
        )

    def test_older_etag_with_older_updated_at_loses(self):
        store = FakeStore()
        # Seed a newer gigmcp-sourced row
        store.insert(
            operator_id=GIGMCP_OPERATOR_ID,
            industry_slug="b2b-saas",
            sub_vertical=None,
            catalog_json={
                "processes": [{"name": "demo"}],
                "source": {
                    "provider": "gigmcp",
                    "etag": "sha256:new",
                    "source_updated_at": "2026-05-25T03:00:00Z",
                    "fetched_at": "2026-05-25T03:00:00Z",
                },
            },
            confidence_score=0.85,
            seed_for_industry=True,
            submitted_by_user_id=GIGMCP_SENTINEL_UUID,
            multi_axis_tags=[],
        )
        conn = FakeConn(store)
        payload = make_payload(
            "b2b-saas",
            etag="sha256:old-different",
            updated_at="2026-05-01T00:00:00Z",
        )
        with patch.object(
            industry_sync, "fetch_industry", side_effect=lambda u, t: payload
        ):
            metrics = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["b2b-saas"],
            )
        # Different etag but older updated_at → unchanged
        self.assertEqual(metrics["upserted"], 0)
        self.assertEqual(metrics["unchanged"], 1)
        # Row preserved unchanged
        self.assertEqual(
            existing_row_etag(store.rows[0]["catalog_json"]), "sha256:new"
        )

    def test_operator_submitted_row_never_overwritten(self):
        """Rows with no `source` block (= operator submission) are sacred."""
        store = FakeStore()
        store.insert(
            operator_id=GIGMCP_OPERATOR_ID,  # could be any operator; using sentinel to force collision
            industry_slug="boutique-hotel",
            sub_vertical=None,
            catalog_json={
                # No 'source' key → operator submission
                "processes": [{"name": "operator-curated"}],
            },
            confidence_score=0.95,
            seed_for_industry=False,
            submitted_by_user_id="00000000-0000-0000-0000-000000000abc",
            multi_axis_tags=[],
        )
        conn = FakeConn(store)
        payload = make_payload(
            "boutique-hotel",
            etag="sha256:gigmcp",
            updated_at="2026-05-25T03:00:00Z",
        )
        with patch.object(
            industry_sync, "fetch_industry", side_effect=lambda u, t: payload
        ):
            metrics = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["boutique-hotel"],
            )
        self.assertEqual(metrics["preserved_operator"], 1)
        self.assertEqual(metrics["upserted"], 0)
        # Original row content untouched
        self.assertEqual(
            store.rows[0]["catalog_json"]["processes"][0]["name"],
            "operator-curated",
        )


# ---------------------------------------------------------------------------
# Test 3 — malformed_source_skips
# A bad gigmcp payload doesn't kill the whole sync. The good neighbors
# still get upserted.
# ---------------------------------------------------------------------------

class TestMalformedSourceSkipped(unittest.TestCase):
    def test_malformed_increments_metric_and_continues(self):
        store = FakeStore()
        conn = FakeConn(store)

        good = make_payload("good-industry", etag="sha256:good")
        bad = {"industry_tag": "bad-industry"}  # missing processes/etag/updated_at

        def fake_fetch(base_url, tag):
            if tag == "good-industry":
                return good
            return bad

        emitted = []
        with patch.object(industry_sync, "fetch_industry", side_effect=fake_fetch), \
             patch.object(industry_sync, "emit_hme_event",
                          side_effect=lambda et, p: emitted.append((et, p))):
            metrics = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["bad-industry", "good-industry"],
            )

        self.assertEqual(metrics["skipped_malformed"], 1)
        self.assertEqual(metrics["upserted"], 1)
        self.assertEqual(metrics["fetched"], 1)  # bad doesn't count as fetched
        # HME warning emitted for the bad one
        bad_events = [e for e in emitted if e[0] == "GigmcpSyncMalformed"]
        self.assertEqual(len(bad_events), 1)
        self.assertEqual(bad_events[0][1]["industry_tag"], "bad-industry")
        # Good row was actually written
        self.assertEqual(len(store.rows), 1)
        self.assertEqual(store.rows[0]["industry_slug"], "good-industry")


# ---------------------------------------------------------------------------
# Test 4 — success_metric_written
# A successful run emits the metric counters via write_metric().
# ---------------------------------------------------------------------------

class TestSuccessMetricWritten(unittest.TestCase):
    def test_metrics_emitted_on_completion(self):
        store = FakeStore()
        conn = FakeConn(store)

        with patch.object(
            industry_sync, "fetch_industry",
            side_effect=lambda u, t: make_payload(t)
        ), patch.object(
            industry_sync, "list_industries_to_sync",
            return_value=["a", "b", "c"],
        ), patch.object(
            industry_sync, "connect_to_decision_engine_db", return_value=conn
        ), patch.object(
            industry_sync, "_read_db_password", return_value="x"
        ), patch.object(
            industry_sync, "write_metric"
        ) as mock_write, patch.object(
            industry_sync, "emit_hme_event"
        ) as mock_emit, patch.object(
            industry_sync, "GIGMCP_EXPORT_URL", "http://fake"
        ):
            rc = industry_sync.main()

        self.assertEqual(rc, 0)
        # write_metric called exactly once with a dict containing fetched>=1
        self.assertEqual(mock_write.call_count, 1)
        emitted_metrics = mock_write.call_args[0][0]
        self.assertGreaterEqual(emitted_metrics["fetched"], 1)
        self.assertEqual(emitted_metrics["fetched"], 3)
        # HME completion event emitted
        completion = [
            c for c in mock_emit.call_args_list
            if c[0][0] == "GigmcpSyncCompleted"
        ]
        self.assertEqual(len(completion), 1)


# ---------------------------------------------------------------------------
# Test 5 (bonus) — etag_unchanged_no_write
# Belt-and-suspenders for the same-etag short-circuit.
# ---------------------------------------------------------------------------

class TestEtagUnchangedNoWrite(unittest.TestCase):
    def test_same_etag_skips_update_path_entirely(self):
        store = FakeStore()
        store.insert(
            operator_id=GIGMCP_OPERATOR_ID,
            industry_slug="commercial-real-estate",
            sub_vertical=None,
            catalog_json={
                "processes": [{"name": "x"}],
                "source": {
                    "etag": "sha256:identical",
                    "source_updated_at": "2026-05-25T03:00:00Z",
                    "provider": "gigmcp",
                    "fetched_at": "2026-05-25T03:00:00Z",
                },
            },
            confidence_score=0.85,
            seed_for_industry=True,
            submitted_by_user_id=GIGMCP_SENTINEL_UUID,
            multi_axis_tags=[],
        )
        conn = FakeConn(store)
        # Same etag, but a different (newer) updated_at — should still
        # be no-op because etag short-circuit fires first.
        payload = make_payload(
            "commercial-real-estate",
            etag="sha256:identical",
            updated_at="2026-12-31T00:00:00Z",
        )
        with patch.object(
            industry_sync, "fetch_industry", side_effect=lambda u, t: payload
        ):
            metrics = industry_sync.run_sync(
                base_url="http://fake",
                conn=conn,
                industries=["commercial-real-estate"],
            )
        self.assertEqual(metrics["unchanged"], 1)
        self.assertEqual(metrics["upserted"], 0)


if __name__ == "__main__":
    unittest.main()
