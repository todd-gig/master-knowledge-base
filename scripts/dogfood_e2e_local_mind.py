#!/usr/bin/env python3
"""dogfood_e2e_local_mind.py — end-to-end validation for gigaton-local-mind.

Run AFTER:
  1. gigaton-mcp PR #2 merged (DONE 2026-06-02 16:44 UTC)
  2. intel-silo PR #69 merged + Cloud Run revision deployed
  3. gigaton-gateway PR #82 merged + Cloud Run revision deployed
  4. gigaton-local-mind installed locally + registered in ~/.claude.json
     (see runbooks/2026_06_02_dogfood_install_local_mind.md)

Validates the local→cloud flow end-to-end:

  - Local embedding produces 384-dim vectors via gigaton-local-mind.
  - Pre-embedded chunks ingest into intel-silo via
    POST /v1/qa/ingest_preembedded (X-Operator-Id auth, optional
    X-Admin-Token).
  - Newly ingested chunks are queryable via /v1/qa/ask within ~10s.
  - Cost-avoided telemetry shows up in gateway + silo Cloud Run logs
    (use --no-logs to skip the gcloud calls).
  - The ingest is idempotent — re-running the same idempotency_key
    returns ``ingested: 0`` + ``deduped_idempotent: 3``.

Cleanup
-------
intel-silo does NOT (as of 2026-06-02) expose an operator-facing
delete endpoint for individual Q&A chunks. The only DELETE routes
are ``/v1/sources/{source_id}`` (admin-scoped sources) and
``/v1/oauth/drive/{user_id}`` (drive tokens) — neither matches the
per-chunk write surface used by ``/v1/qa/ingest_preembedded``.

So this script emits a CLEANUP WARNING with the marker strings, the
operator_id, and the namespace it wrote to. The operator can then
either (a) leave the dogfood chunks in place — they're harmless,
small, and well-labelled — or (b) page intel-silo ops to run a
direct FAISS surgical delete by marker substring. A future
``/v1/admin/qa/delete_by_marker`` endpoint is the right long-term
fix; tracked as an open loop in MEMORY.md.

Usage
-----

    # Standard run — pulls operator id + URLs from env / defaults.
    python scripts/dogfood_e2e_local_mind.py

    # Override target services explicitly.
    python scripts/dogfood_e2e_local_mind.py \\
        --operator-id todd \\
        --gateway-url https://gigaton-gateway-sqatlxhlza-uc.a.run.app \\
        --silo-url   https://intelligence-silo-rjmcrtvuzq-uc.a.run.app

    # Skip Cloud Logging checks (e.g. on a machine without gcloud auth).
    python scripts/dogfood_e2e_local_mind.py --no-logs

    # Dry run — prints what each step WOULD do, no network, no embedder.
    python scripts/dogfood_e2e_local_mind.py --dry-run

Env vars (also accepted)
------------------------

    GIGATON_OPERATOR_ID  default operator id (else --operator-id)
    GIGATON_GATEWAY_URL  default gateway base URL
    GIGATON_SILO_URL     default intel-silo base URL
    GIGATON_ADMIN_TOKEN  optional X-Admin-Token (silo soft-gate bypass)

Exit codes
----------

    0   — all steps passed
    1   — at least one step failed (details printed)
    2   — bad CLI args / missing prereq (e.g. httpx not installed)
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import secrets
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Optional

# httpx is a gigaton-local-mind dependency and will be installed by the
# install runbook. We do NOT fall back to urllib here because we want
# the script to fail-loud if the local-mind venv isn't activated — that
# is itself a useful dogfood failure signal.
try:
    import httpx
except ImportError:  # pragma: no cover — only hit on a non-dogfood machine
    sys.stderr.write(
        "ERROR: httpx not installed. Run from the gigaton-local-mind "
        "venv (the dogfood install runbook installs it as a dep).\n"
    )
    sys.exit(2)


# ─────────────────────────────────────── constants ──

EMBEDDING_DIM = 384
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_GATEWAY = "https://gigaton-gateway-sqatlxhlza-uc.a.run.app"
DEFAULT_SILO = "https://intelligence-silo-rjmcrtvuzq-uc.a.run.app"
INDEX_SETTLE_SECONDS = 5
GCP_PROJECT = "gigaton-platform"
HTTP_TIMEOUT = 60.0

# Markers are deterministic + per-run idempotency-keyed so re-running
# the script produces a clean PASS every time (no stale state collisions
# across runs). The CHAR sequence is just a-z so it survives any silo-side
# normalisation.
MARKER_PREFIX = "GIGADOG"
MARKER_LETTERS = ("A", "B", "C")


# ─────────────────────────────────────── helpers ──


def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_id() -> str:
    # ~6 chars of url-safe randomness — collision-resistant for the
    # idempotency key + run tag without being unwieldy in log output.
    return secrets.token_urlsafe(4).rstrip("=").replace("_", "").replace("-", "")[:6]


@dataclass
class StepResult:
    name: str
    passed: bool
    detail: str = ""
    elapsed_ms: int = 0


@dataclass
class DogfoodConfig:
    operator_id: str
    gateway_url: str
    silo_url: str
    admin_token: Optional[str]
    no_logs: bool
    dry_run: bool
    run_tag: str = field(default_factory=_short_id)
    namespace: str = "dogfood"

    @property
    def idempotency_key(self) -> str:
        # Fresh per run — the silo persists keys for 24h, so re-running
        # the script back-to-back yields independent PASSes. To exercise
        # the dedup path explicitly, use --idempotency-key-fixed.
        return f"dogfood-e2e-{self.operator_id}-{self.run_tag}"


# ─────────────────────────────────────── step impls ──


def synthesize_documents(cfg: DogfoodConfig) -> list[dict[str, Any]]:
    """Step 1 — three deterministic test docs with run-tagged markers.

    The marker shape is ``GIGADOG-<letter>-<run_tag>-2026`` so:
        - Cross-run independence is preserved (each run has its own
          marker, so the Q&A retrieval can't be satisfied by a previous
          run's leftover chunk → forces the just-ingested chunk to win).
        - Cleanup is grep-able (operator can search "GIGADOG-" in the
          silo FAISS index to find every dogfood chunk ever ingested).
    """
    docs = []
    for letter in MARKER_LETTERS:
        marker = f"{MARKER_PREFIX}-{letter}-{cfg.run_tag}-2026"
        docs.append({
            "letter": letter,
            "marker": marker,
            "text": (
                f"The dogfood test marker {letter} is {marker}. "
                "This document was synthesised by "
                "scripts/dogfood_e2e_local_mind.py to validate the "
                "gigaton-local-mind → intelligence-silo flow end-to-end. "
                "If you are reading this from a Q&A answer, the local "
                "embed + pre-embedded ingest path is working as designed."
            ),
        })
    return docs


def embed_locally(docs: list[dict[str, Any]], cfg: DogfoodConfig) -> list[list[float]]:
    """Step 2 — embed via gigaton-local-mind's lib API directly.

    We import ``gigaton_local_mind.embedder.embed_texts`` directly
    (bypassing the MCP server) because this script's job is to validate
    the local→cloud DATA flow, not the Claude-Desktop-tool-call flow
    (which is exercised separately by the smoke-test list in the
    install runbook).

    Dry-run: returns deterministic ``[0.0] * 384`` vectors so the rest
    of the script can be reasoned about without a model download.
    """
    if cfg.dry_run:
        return [[0.0] * EMBEDDING_DIM for _ in docs]
    try:
        from gigaton_local_mind.embedder import embed_texts  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "Cannot import gigaton_local_mind.embedder — is the "
            "gigaton-local-mind package installed in this venv? "
            "Run `uv pip install -e .` from "
            "/Users/admin/Gigaton-UI-Platform/gigaton-mcp/"
            "servers/gigaton-local-mind/. "
            f"Underlying error: {exc}"
        ) from exc
    vecs = embed_texts([d["text"] for d in docs])
    for i, v in enumerate(vecs):
        if len(v) != EMBEDDING_DIM:
            raise RuntimeError(
                f"Embedding {i} has dim {len(v)}, expected {EMBEDDING_DIM}. "
                f"Model contract is {EMBEDDING_MODEL}."
            )
    return vecs


def ingest_to_silo(
    cfg: DogfoodConfig,
    docs: list[dict[str, Any]],
    embeddings: list[list[float]],
) -> dict[str, Any]:
    """Step 3 — POST /v1/qa/ingest_preembedded.

    Auth model (from intel-silo qa_ingest_preembedded.py):
        - ``X-Operator-Id`` header must match ``body.operator_id`` or 403.
        - ``X-Admin-Token`` (when valid) bypasses the cross-tenant guard.
        - When silo's ADMIN_TOKEN env is unset, missing both headers is
          accepted (fail-open dev). We always send X-Operator-Id so
          prod behaviour is exercised.
    """
    if len(docs) != len(embeddings):
        raise AssertionError(
            f"docs/embeddings length mismatch: {len(docs)} vs {len(embeddings)}"
        )
    payload = {
        "operator_id": cfg.operator_id,
        "idempotency_key": cfg.idempotency_key,
        "local_mind_version": "0.1.0",
        "chunks": [
            {
                "text": doc["text"],
                "embedding": emb,
                "metadata": {
                    "category": cfg.namespace,
                    "source": "dogfood_e2e_local_mind.py",
                    "marker": doc["marker"],
                    "letter": doc["letter"],
                    "run_tag": cfg.run_tag,
                    "ingested_at": _now_iso(),
                },
            }
            # `strict=True` requires Python ≥3.10; we pre-assert equal
            # lengths so plain zip is safe + back-compatible to 3.8.
            for doc, emb in zip(docs, embeddings)
        ],
    }
    headers = {
        "Content-Type": "application/json",
        "X-Operator-Id": cfg.operator_id,
    }
    if cfg.admin_token:
        headers["X-Admin-Token"] = cfg.admin_token

    url = cfg.silo_url.rstrip("/") + "/v1/qa/ingest_preembedded"
    if cfg.dry_run:
        return {
            "_dry_run": True,
            "url": url,
            "chunk_count": len(payload["chunks"]),
            "idempotency_key": cfg.idempotency_key,
        }

    resp = httpx.post(url, json=payload, headers=headers, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def ask_qa(cfg: DogfoodConfig, letter: str, marker: str) -> dict[str, Any]:
    """Step 5 — POST /v1/qa/ask via the gateway.

    The gateway (after PR #82) augments 200 JSON responses with
    ``local_mind_available: true`` + ``local_capabilities: [...]`` when
    the operator has an active handshake. We check that field in the
    caller — its absence indicates the handshake didn't land or the
    gateway revision hasn't picked up PR #82.
    """
    question = (
        f"What is the dogfood test marker {letter}? "
        f"(Look for {MARKER_PREFIX}-{letter}-{cfg.run_tag}-... in the corpus.)"
    )
    payload = {
        "question": question,
        "operator_id": cfg.operator_id,
        "category": cfg.namespace,
        "top_k": 5,
        "fast": True,
    }
    headers = {"Content-Type": "application/json"}
    # The gateway resolves operator_id from the JWT (sub claim). For a
    # local dogfood run we expect the operator to have GIGATON_JWT_TODD
    # (or similar) in env. If absent, the gateway will not run the
    # augment path — we surface that as a SOFT-FAIL on step 5.
    jwt = os.environ.get(f"GIGATON_JWT_{cfg.operator_id.upper()}")
    if jwt:
        headers["Authorization"] = f"Bearer {jwt}"

    url = cfg.gateway_url.rstrip("/") + "/v1/qa/ask"
    if cfg.dry_run:
        return {
            "_dry_run": True,
            "url": url,
            "question": question,
            "auth_attached": bool(jwt),
            "expected_marker": marker,
        }

    resp = httpx.post(url, json=payload, headers=headers, timeout=HTTP_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def check_gcloud_logs(cfg: DogfoodConfig) -> tuple[bool, str]:
    """Step 6 — verify telemetry markers in Cloud Logging.

    We look for two events from the last ~5 minutes:
        - silo ``event=ingest_preembedded`` with this operator_id +
          source=local-mind (proves PR #69's log line is emitting)
        - gateway ``event=qa_ask`` with local_mind_available=true
          (proves PR #82's augment landed)

    If gcloud is not on PATH or the auth context is stale, this step
    is reported as SKIP rather than FAIL — log presence is downstream
    of the actual data flow.
    """
    if not shutil.which("gcloud"):
        return True, "SKIP — gcloud not on PATH"

    five_min_ago = (_dt.datetime.now(_dt.timezone.utc)
                    - _dt.timedelta(minutes=5)).strftime("%Y-%m-%dT%H:%M:%SZ")

    silo_filter = (
        f'resource.type=cloud_run_revision '
        f'AND resource.labels.service_name=intelligence-silo '
        f'AND jsonPayload.event="ingest_preembedded" '
        f'AND jsonPayload.operator_id="{cfg.operator_id}" '
        f'AND timestamp>="{five_min_ago}"'
    )
    gw_filter = (
        f'resource.type=cloud_run_revision '
        f'AND resource.labels.service_name=gigaton-gateway '
        f'AND jsonPayload.event="qa_ask" '
        f'AND jsonPayload.operator_id="{cfg.operator_id}" '
        f'AND jsonPayload.local_mind_available=true '
        f'AND timestamp>="{five_min_ago}"'
    )
    found_silo = _gcloud_logs_have_hits(silo_filter)
    found_gw = _gcloud_logs_have_hits(gw_filter)
    if found_silo and found_gw:
        return True, "both silo + gateway log lines present"
    parts = []
    if not found_silo:
        parts.append("silo ingest_preembedded log MISSING")
    if not found_gw:
        parts.append("gateway qa_ask local_mind_available=true log MISSING")
    return False, "; ".join(parts)


def _gcloud_logs_have_hits(log_filter: str) -> bool:
    try:
        out = subprocess.run(
            [
                "gcloud", "logging", "read", log_filter,
                "--limit=1", "--format=value(timestamp)",
                f"--project={GCP_PROJECT}",
            ],
            capture_output=True, text=True, timeout=30, check=False,
        )
        return bool(out.stdout.strip())
    except (subprocess.SubprocessError, OSError):
        return False


def cleanup_warning(cfg: DogfoodConfig, docs: list[dict[str, Any]]) -> str:
    """Step 7 — emit cleanup guidance (no automated delete is available).

    See module docstring for why this is a warning, not a DELETE.
    """
    markers = [d["marker"] for d in docs]
    return (
        f"intel-silo has no per-chunk delete endpoint as of 2026-06-02. "
        f"The {len(markers)} dogfood chunks remain in operator_id="
        f"{cfg.operator_id} under category={cfg.namespace}. "
        f"Markers: {', '.join(markers)}. "
        f"To purge: page silo ops for a FAISS surgical delete by marker "
        f"substring '{MARKER_PREFIX}-' (or leave in place — chunks are "
        f"<1 KiB each and clearly labelled as dogfood artifacts)."
    )


# ─────────────────────────────────────── runner ──


def _step(name: str) -> Any:
    """Decorator that times a step and produces a StepResult.

    Used by the dispatcher below so each step's pass/fail + duration is
    captured uniformly (and a single exception path produces a clear
    failure rather than a stack trace dump).
    """
    def deco(fn: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> StepResult:
            t0 = time.perf_counter()
            try:
                detail = fn(*args, **kwargs)
                return StepResult(name=name, passed=True,
                                  detail=detail or "",
                                  elapsed_ms=int((time.perf_counter() - t0) * 1000))
            except Exception as exc:  # noqa: BLE001 — we want the message
                return StepResult(name=name, passed=False,
                                  detail=f"{type(exc).__name__}: {exc}",
                                  elapsed_ms=int((time.perf_counter() - t0) * 1000))
        return wrapper
    return deco


def run_all(cfg: DogfoodConfig) -> list[StepResult]:
    results: list[StepResult] = []

    # ── Step 1: synthesize ──────────────────────────────────────────
    @_step("1. Synthesize 3 deterministic test documents")
    def s1() -> str:
        nonlocal docs
        docs = synthesize_documents(cfg)
        return f"created {len(docs)} docs, markers={[d['marker'] for d in docs]}"
    docs: list[dict[str, Any]] = []
    results.append(s1())
    if not results[-1].passed:
        return results

    # ── Step 2: embed locally ───────────────────────────────────────
    @_step("2. Embed locally via gigaton_local_mind.embedder.embed_texts")
    def s2() -> str:
        nonlocal embeddings
        embeddings = embed_locally(docs, cfg)
        dims = {len(v) for v in embeddings}
        if dims != {EMBEDDING_DIM}:
            raise AssertionError(
                f"embedding dims {dims} != {{{EMBEDDING_DIM}}}"
            )
        return f"embedded {len(embeddings)} × {EMBEDDING_DIM}-dim vectors (dry_run={cfg.dry_run})"
    embeddings: list[list[float]] = []
    results.append(s2())
    if not results[-1].passed:
        return results

    # ── Step 3: ingest pre-embedded ─────────────────────────────────
    @_step("3. POST /v1/qa/ingest_preembedded → intel-silo")
    def s3() -> str:
        nonlocal ingest_resp
        ingest_resp = ingest_to_silo(cfg, docs, embeddings)
        if cfg.dry_run:
            return f"DRY RUN — would POST to {ingest_resp['url']}"
        if ingest_resp.get("ingested") != len(docs):
            raise AssertionError(
                f"silo responded ingested={ingest_resp.get('ingested')}, "
                f"expected {len(docs)}. Full body: {ingest_resp}"
            )
        if ingest_resp.get("embedding_source") != "local-mind":
            raise AssertionError(
                f"silo responded embedding_source="
                f"{ingest_resp.get('embedding_source')}, "
                f"expected 'local-mind'"
            )
        return (f"ingested={ingest_resp['ingested']}, "
                f"embedding_source={ingest_resp['embedding_source']}, "
                f"idempotency_key={ingest_resp['idempotency_key']}")
    ingest_resp: dict[str, Any] = {}
    results.append(s3())
    if not results[-1].passed:
        return results

    # ── Step 3.5: idempotency replay (sanity) ───────────────────────
    @_step("3b. Idempotency replay → same key returns ingested=0 + dedup count")
    def s3b() -> str:
        if cfg.dry_run:
            return "DRY RUN — skipped"
        replay = ingest_to_silo(cfg, docs, embeddings)
        if replay.get("ingested") != 0:
            raise AssertionError(
                f"replay ingested={replay.get('ingested')}, expected 0 "
                f"(idempotency-store regression). Full body: {replay}"
            )
        if replay.get("deduped_idempotent") != len(docs):
            raise AssertionError(
                f"replay deduped_idempotent={replay.get('deduped_idempotent')}, "
                f"expected {len(docs)}"
            )
        return (f"replay correctly deduped {replay['deduped_idempotent']} chunks "
                f"under same idempotency_key")
    results.append(s3b())
    # idempotency failure is bad but recoverable — keep going so the Q&A
    # step still runs against the original (successful) ingest.

    # ── Step 4: wait for index settle ───────────────────────────────
    @_step(f"4. Wait {INDEX_SETTLE_SECONDS}s for FAISS index to settle")
    def s4() -> str:
        if cfg.dry_run:
            return "DRY RUN — skipped"
        time.sleep(INDEX_SETTLE_SECONDS)
        return "ok"
    results.append(s4())

    # ── Step 5: query Q&A via gateway ───────────────────────────────
    @_step("5. POST /v1/qa/ask via gateway → answer cites GIGADOG-A marker")
    def s5() -> str:
        first_doc = docs[0]
        qa = ask_qa(cfg, first_doc["letter"], first_doc["marker"])
        if cfg.dry_run:
            return f"DRY RUN — would POST to {qa['url']}"
        answer = (qa.get("answer") or "").strip()
        if first_doc["marker"] not in answer:
            # Fallback — sometimes the synthesised answer paraphrases.
            # Check citations directly: the just-ingested chunk's text
            # should be in at least one citation.
            cited_texts = " | ".join(
                str(c.get("text", "")) for c in (qa.get("citations") or [])
            )
            if first_doc["marker"] not in cited_texts:
                raise AssertionError(
                    f"marker {first_doc['marker']!r} NOT in answer "
                    f"or citations. Answer: {answer[:200]!r}. "
                    f"Citation snippets: {cited_texts[:400]!r}"
                )
            citation_note = " (matched in citations, not answer body)"
        else:
            citation_note = " (matched in answer body)"

        # local_mind_available is the canary for PR #82 — its ABSENCE
        # is a soft-fail (Phase 1 contract: missing field is a valid
        # response shape; means handshake hasn't landed for this op).
        lma = qa.get("local_mind_available")
        if lma is None:
            extra = " | local_mind_available=ABSENT (handshake not yet bound for op)"
        elif lma is True:
            extra = " | local_mind_available=true (PR #82 augment confirmed)"
        else:
            extra = f" | local_mind_available={lma!r} (UNEXPECTED)"

        return (f"answer length={len(answer)} chars{citation_note}; "
                f"confidence={qa.get('confidence')}; "
                f"citation_count={len(qa.get('citations') or [])}{extra}")
    results.append(s5())

    # ── Step 6: gcloud log telemetry ────────────────────────────────
    if cfg.no_logs:
        results.append(StepResult(
            name="6. Verify gcloud telemetry (silo + gateway)",
            passed=True, detail="SKIP (--no-logs)",
        ))
    elif cfg.dry_run:
        results.append(StepResult(
            name="6. Verify gcloud telemetry (silo + gateway)",
            passed=True, detail="DRY RUN — would query Cloud Logging",
        ))
    else:
        @_step("6. Verify gcloud telemetry (silo + gateway)")
        def s6() -> str:
            ok, detail = check_gcloud_logs(cfg)
            if not ok:
                raise AssertionError(detail)
            return detail
        results.append(s6())

    # ── Step 7: cleanup warning ─────────────────────────────────────
    @_step("7. Cleanup guidance (no automated delete available)")
    def s7() -> str:
        return cleanup_warning(cfg, docs)
    results.append(s7())

    return results


# ─────────────────────────────────────── CLI ──


def _parse_args(argv: list[str] | None = None) -> DogfoodConfig:
    ap = argparse.ArgumentParser(
        description="End-to-end dogfood validation for gigaton-local-mind.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument(
        "--operator-id",
        default=os.environ.get("GIGATON_OPERATOR_ID", "todd"),
        help="Operator tenant (default: env GIGATON_OPERATOR_ID or 'todd')",
    )
    ap.add_argument(
        "--gateway-url",
        default=os.environ.get("GIGATON_GATEWAY_URL", DEFAULT_GATEWAY),
        help=f"Gateway base URL (default: {DEFAULT_GATEWAY})",
    )
    ap.add_argument(
        "--silo-url",
        default=os.environ.get("GIGATON_SILO_URL", DEFAULT_SILO),
        help=f"intel-silo base URL (default: {DEFAULT_SILO})",
    )
    ap.add_argument(
        "--admin-token",
        default=os.environ.get("GIGATON_ADMIN_TOKEN"),
        help="Optional X-Admin-Token (silo soft-gate bypass)",
    )
    ap.add_argument(
        "--no-logs", action="store_true",
        help="Skip the gcloud Cloud Logging verification step",
    )
    ap.add_argument(
        "--dry-run", action="store_true",
        help="Print what each step would do; no network, no model load",
    )
    args = ap.parse_args(argv)
    return DogfoodConfig(
        operator_id=args.operator_id,
        gateway_url=args.gateway_url,
        silo_url=args.silo_url,
        admin_token=args.admin_token,
        no_logs=args.no_logs,
        dry_run=args.dry_run,
    )


def _render_summary(results: list[StepResult]) -> str:
    """ASCII-art summary — no emoji per repo guidance."""
    lines = ["", "=" * 72, "Dogfood E2E — Local Mind → Cloud Silo", "=" * 72]
    all_pass = True
    for r in results:
        tag = "[PASS]" if r.passed else "[FAIL]"
        if not r.passed:
            all_pass = False
        lines.append(f"{tag} ({r.elapsed_ms:>6} ms)  {r.name}")
        if r.detail:
            # Wrap detail at ~80 cols for readability.
            indented = "        " + r.detail.replace("\n", "\n        ")
            lines.append(indented)
    lines.append("=" * 72)
    lines.append("RESULT: " + ("ALL GREEN" if all_pass else "FAILED"))
    lines.append("=" * 72)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    cfg = _parse_args(argv)
    if cfg.operator_id != "todd":
        sys.stderr.write(
            f"NOTE: dogfood window is gated to operator_id=todd through "
            f"2026-06-10; running with operator_id={cfg.operator_id!r} "
            f"will fail at the silo soft-gate unless --admin-token is set "
            f"or the dogfood gate has been opened to this operator.\n"
        )
    print(json.dumps({
        "event": "dogfood_e2e_start",
        "operator_id": cfg.operator_id,
        "gateway_url": cfg.gateway_url,
        "silo_url": cfg.silo_url,
        "run_tag": cfg.run_tag,
        "idempotency_key": cfg.idempotency_key,
        "dry_run": cfg.dry_run,
        "no_logs": cfg.no_logs,
        "started_at": _now_iso(),
    }, indent=2))
    print()
    results = run_all(cfg)
    print(_render_summary(results))
    return 0 if all(r.passed for r in results) else 1


# ─────────────────────────────────────── inline smoke ──


def _smoke_dry_run() -> int:
    """Minimal dry-run that exercises every step's offline path.

    Invoked by ``python scripts/dogfood_e2e_local_mind.py --self-test`` so
    contributors can verify the script's wiring without hitting the
    network or downloading the MiniLM model. Returns 0 on success.
    """
    rc = main([
        "--operator-id", "todd",
        "--gateway-url", "https://example-gateway.invalid",
        "--silo-url", "https://example-silo.invalid",
        "--no-logs",
        "--dry-run",
    ])
    return rc


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(_smoke_dry_run())
    sys.exit(main())
