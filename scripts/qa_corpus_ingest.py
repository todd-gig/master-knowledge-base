#!/usr/bin/env python3
"""qa_corpus_ingest.py — per-operator incremental ingest into intel-silo Q&A.

A parameterized, config-driven, incrementally-aware sibling of the existing
single-shot ``ingest_mkb_to_silo.sh`` (which targets ``operator_id=gigaton``
and only walks the MKB tree). This script targets ARBITRARY operators with
ARBITRARY source trees, and skips files whose (mtime, size) haven't changed
since the last run — so cron / launchd can fire it frequently and cheap.

Why this exists (lessons from the 2026-05-28 seed):

    1. Cron incremental re-ingest — auto-memory grows every session.
    2. Re-ingest target after the carmen-beach → gigaton-platform migration —
       just swap SILO_URL (env or --silo-url) when the new silo cuts over.
    3. Per-operator ingest — when Multipli / Carmen Beach / Ti-Solutions
       onboard, each operator gets a config file at
       ``scripts/qa_corpus_configs/<operator>.json``.

This script is the single substrate behind all three.

Usage
-----

    # One-shot incremental (default — state file keeps cron cheap)
    python3 qa_corpus_ingest.py \\
        --operator todd \\
        --silo-url https://intelligence-silo-rjmcrtvuzq-uc.a.run.app \\
        --config scripts/qa_corpus_configs/todd.json

    # Full re-ingest (force every file, ignore state)
    python3 qa_corpus_ingest.py --operator todd --full

    # Only files modified after a UTC timestamp (state file untouched)
    python3 qa_corpus_ingest.py --operator todd --since 2026-05-28T00:00:00Z

    # Dry-run: list what would be sent without POSTing
    python3 qa_corpus_ingest.py --operator todd --dry-run

Env vars (also accepted)
------------------------

    SILO_URL    base URL of intel-silo (e.g. https://intelligence-silo-…run.app)
    SILO_TOKEN  bearer token for authenticated Cloud Run endpoints (optional —
                falls back to ``gcloud auth print-identity-token``)

Config file format
------------------

    {
      "operator_id": "todd",
      "sources": [
        {"label": "Obsidian vault", "root": "~/Documents/Obsidian Vault/Gigaton",
         "category": "vault", "extensions": [".md"]},
        {"label": "Auto-memory",    "root": "~/.claude/projects/-Users-admin/memory",
         "category": "memory", "extensions": [".md"]},
        ...
      ]
    }

State file format (default ~/.local/state/gigaton/qa-corpus/<operator>.json)
----------------------------------------------------------------------------

    {
      "last_run_at": "2026-05-28T19:30:00Z",
      "silo_url": "https://…",
      "sources": {
        "Auto-memory": {
          "memory/foo.md": {"mtime": 1748464200.0, "size": 4321,
                            "sha256_8": "ab12cd34", "chunks_stored": 12,
                            "last_ingested_at": "2026-05-28T19:30:00Z"}
        }
      }
    }
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Iterable

# ─────────────────────────────────────── constants ──

# Bound per-file size — anything bigger is unlikely to be a useful doc and
# more likely a generated artifact. The pipeline chunks internally.
MAX_BYTES = 200_000
MAX_CHARS = 180_000

# Conservative secret patterns — refuse the whole file if any match.
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[A-Z0-9]{16}"),
    re.compile(r"AIzaSy[A-Za-z0-9_-]{33}"),
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"gho_[A-Za-z0-9]{36}"),
    re.compile(r"xoxb-\d+-\d+-\d+-[a-z0-9]+"),
    re.compile(r"-----BEGIN (RSA |EC |OPENSSH |)PRIVATE KEY-----"),
]


# ─────────────────────────────────────── helpers ──

def _now_iso() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(s: str) -> float:
    """Accept Z or +00:00; return POSIX seconds."""
    s = s.replace("Z", "+00:00")
    return _dt.datetime.fromisoformat(s).timestamp()


def _default_state_path(operator: str) -> Path:
    return Path.home() / ".local" / "state" / "gigaton" / "qa-corpus" / f"{operator}.json"


def _expand(p: str | Path) -> Path:
    return Path(os.path.expanduser(str(p))).resolve()


def _is_safe(text: str) -> bool:
    return not any(p.search(text) for p in SECRET_PATTERNS)


def _sha256_8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def _gather(root: Path, exts: tuple[str, ...]) -> Iterable[Path]:
    if not root.exists():
        return
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in exts:
            continue
        try:
            if any(part.startswith(".") for part in p.relative_to(root).parts):
                continue
            if p.stat().st_size > MAX_BYTES:
                continue
        except OSError:
            continue
        yield p


def _bearer_token() -> str:
    """Resolve a bearer token for SILO_URL. Order: env, gcloud user creds."""
    tok = os.environ.get("SILO_TOKEN", "").strip()
    if tok:
        return tok
    try:
        out = subprocess.run(
            ["gcloud", "auth", "print-identity-token"],
            check=True, capture_output=True, text=True, timeout=15,
        )
        return out.stdout.strip()
    except Exception:  # noqa: BLE001
        return ""


# ─────────────────────────────────────── state ──

def _load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"last_run_at": None, "silo_url": None, "sources": {}}
    try:
        with path.open() as f:
            return json.load(f)
    except Exception:  # noqa: BLE001
        return {"last_run_at": None, "silo_url": None, "sources": {}}


def _save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    tmp.replace(path)


# ─────────────────────────────────────── ingest ──

def _post(silo_url: str, body: bytes, token: str, timeout: float = 60.0) -> dict[str, Any]:
    req = urllib.request.Request(
        silo_url.rstrip("/") + "/memory/ingest",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def _ingest_one(path: Path, root: Path, source_label: str, category: str,
                operator: str, silo_url: str, token: str,
                dry_run: bool, record_only: bool = False
                ) -> tuple[str, str, str, dict[str, Any]]:
    """Return (rel_path, status, msg, file_meta)."""
    rel = str(path.relative_to(root))
    meta: dict[str, Any] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return rel, "FAIL", f"read:{e}", meta
    if not text.strip():
        return rel, "EMPTY", "", meta
    if not _is_safe(text):
        return rel, "SKIP_SECRET", "", meta
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]

    meta = {
        "mtime": path.stat().st_mtime,
        "size": path.stat().st_size,
        "sha256_8": _sha256_8(text),
        "last_ingested_at": _now_iso(),
    }
    if dry_run:
        return rel, "DRY", "would-ingest", meta
    if record_only:
        # Behaves like OK to the caller (state gets recorded) but no POST.
        return rel, "OK", "record-only", meta

    body = json.dumps({
        "text": text,
        "source": f"{category}:{rel}",
        "category": category,
        "operator_id": operator,
        "is_markdown": path.suffix.lower() == ".md",
    }).encode("utf-8")
    try:
        j = _post(silo_url, body, token)
        meta["chunks_stored"] = int(j.get("chunks_stored", 0))
        return rel, "OK", "", meta
    except urllib.error.HTTPError as e:
        return rel, "FAIL", f"HTTP_{e.code}", meta
    except Exception as e:  # noqa: BLE001
        return rel, "FAIL", f"ERR:{type(e).__name__}", meta


def _changed(state_entry: dict[str, Any] | None, path: Path) -> bool:
    """True if file mtime or size disagrees with state."""
    if not state_entry:
        return True
    try:
        st = path.stat()
    except OSError:
        return False
    return (
        state_entry.get("mtime") != st.st_mtime
        or state_entry.get("size") != st.st_size
    )


# ─────────────────────────────────────── main ──

def _load_config(config_path: Path | None, operator_cli: str | None) -> dict[str, Any]:
    if config_path and config_path.exists():
        with config_path.open() as f:
            cfg = json.load(f)
        if operator_cli:
            cfg["operator_id"] = operator_cli
        return cfg

    # Default config = the 5 sources I seeded on 2026-05-28 for todd.
    return {
        "operator_id": operator_cli or "todd",
        "sources": [
            {"label": "Obsidian vault",
             "root": "~/Documents/Obsidian Vault/Gigaton",
             "category": "vault", "extensions": [".md"]},
            {"label": "Auto-memory",
             "root": "~/.claude/projects/-Users-admin/memory",
             "category": "memory", "extensions": [".md"]},
            {"label": "MKB runbooks",
             "root": "~/Documents/GitHub/master-knowledge-base/runbooks",
             "category": "runbook", "extensions": [".md"]},
            {"label": "MKB architecture",
             "root": "~/Documents/GitHub/master-knowledge-base/docs/architecture",
             "category": "architecture", "extensions": [".md"]},
            {"label": "MKB manifests",
             "root": "~/Documents/GitHub/master-knowledge-base/manifests",
             "category": "manifest", "extensions": [".yaml", ".yml"]},
        ],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Per-operator incremental Q&A corpus ingest into intel-silo.",
    )
    ap.add_argument("--operator", default=None,
                    help="Operator ID (overrides config). Default from config.")
    ap.add_argument("--silo-url", default=os.environ.get("SILO_URL"),
                    help="intel-silo base URL. Env SILO_URL also accepted.")
    ap.add_argument("--config", type=Path, default=None,
                    help="Path to JSON config. Default = embedded todd sources.")
    ap.add_argument("--state-file", type=Path, default=None,
                    help="State JSON path. Default ~/.local/state/gigaton/qa-corpus/<op>.json.")
    ap.add_argument("--since", default=None,
                    help="UTC ISO timestamp; only ingest files with mtime > since "
                         "(does NOT update state).")
    ap.add_argument("--full", action="store_true",
                    help="Ignore state — re-ingest every matching file.")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true",
                    help="List what would be ingested without POSTing.")
    ap.add_argument("--record-only", action="store_true",
                    help="Walk files and record state (mtime/size/sha256_8) "
                         "WITHOUT POSTing. Use this once to bootstrap a state "
                         "file against an already-ingested corpus, so the "
                         "next incremental run only posts genuinely-new files.")
    args = ap.parse_args(argv)

    cfg = _load_config(args.config, args.operator)
    operator: str = cfg["operator_id"]
    silo_url = args.silo_url or os.environ.get("SILO_URL")
    if not silo_url:
        print("ERROR: --silo-url or env SILO_URL is required.", file=sys.stderr)
        return 2

    state_path = args.state_file or _default_state_path(operator)
    state = _load_state(state_path)
    since_ts = _parse_iso(args.since) if args.since else None
    token = "" if args.dry_run else _bearer_token()

    print(f"silo_url   = {silo_url}")
    print(f"operator   = {operator}")
    print(f"state_file = {state_path}")
    print(f"mode       = {'FULL' if args.full else ('since=' + args.since if since_ts else 'incremental')}")
    if args.dry_run:
        print("DRY RUN — no requests will be sent.")
    print()

    grand = {"ok": 0, "chunks": 0, "skipped_unchanged": 0,
             "skip_secret": 0, "fail": 0, "empty": 0, "dry": 0}
    t0 = time.time()

    for src in cfg["sources"]:
        label = src["label"]
        root = _expand(src["root"])
        category = src["category"]
        exts = tuple(s.lower() for s in src["extensions"])
        if not root.exists():
            print(f"## {label}: ROOT MISSING ({root}) — skipping")
            continue
        files = list(_gather(root, exts))
        source_state: dict[str, Any] = state["sources"].setdefault(label, {})

        # Filter to actually-eligible files BEFORE submitting workers.
        eligible: list[Path] = []
        skipped_unchanged = 0
        for p in files:
            rel = str(p.relative_to(root))
            try:
                st_mtime = p.stat().st_mtime
            except OSError:
                continue
            if since_ts is not None and st_mtime <= since_ts:
                continue
            if not args.full and not _changed(source_state.get(rel), p):
                skipped_unchanged += 1
                continue
            eligible.append(p)

        print(f"## {label} → category={category}  total={len(files)}  "
              f"to-ingest={len(eligible)}  skipped-unchanged={skipped_unchanged}")
        grand["skipped_unchanged"] += skipped_unchanged

        local = {"ok": 0, "chunks": 0, "skip_secret": 0, "fail": 0, "empty": 0, "dry": 0}
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = [
                ex.submit(_ingest_one, p, root, label, category, operator,
                          silo_url, token, args.dry_run, args.record_only)
                for p in eligible
            ]
            for i, f in enumerate(as_completed(futs), 1):
                rel, status, msg, meta = f.result()
                if status == "OK":
                    local["ok"] += 1
                    local["chunks"] += int(meta.get("chunks_stored", 0))
                    # ONLY persist state on success.
                    if since_ts is None:  # --since runs do not touch state
                        source_state[rel] = meta
                elif status == "DRY":
                    local["dry"] += 1
                elif status == "SKIP_SECRET":
                    local["skip_secret"] += 1
                elif status == "EMPTY":
                    local["empty"] += 1
                else:
                    local["fail"] += 1
                if i % 25 == 0 or i == len(eligible):
                    print(f"  [{i}/{len(eligible)}] ok={local['ok']} "
                          f"chunks={local['chunks']} skip={local['skip_secret']} "
                          f"fail={local['fail']} last={status} {rel[:60]}",
                          flush=True)
        print(f"  → {label}: ok={local['ok']} chunks_stored={local['chunks']} "
              f"skip_secret={local['skip_secret']} fail={local['fail']} "
              f"empty={local['empty']} dry={local['dry']}")
        for k in local:
            grand[k] = grand.get(k, 0) + local[k]

    # Save state at the end (atomic write) unless --since (which is read-only).
    if since_ts is None and not args.dry_run:
        state["last_run_at"] = _now_iso()
        state["silo_url"] = silo_url
        if args.record_only:
            state["record_only_bootstrap_at"] = _now_iso()
        _save_state(state_path, state)

    print(f"\n## GRAND TOTAL  ({time.time() - t0:.0f}s)")
    print(f"  ok={grand['ok']}  chunks_stored={grand['chunks']}  "
          f"skipped_unchanged={grand['skipped_unchanged']}  "
          f"skip_secret={grand['skip_secret']}  fail={grand['fail']}  "
          f"empty={grand['empty']}  dry={grand['dry']}")
    return 0 if grand["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
