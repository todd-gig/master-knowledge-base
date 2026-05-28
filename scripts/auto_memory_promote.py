#!/usr/bin/env python3
"""auto_memory_promote.py — Promote canonical auto-memory entries into MKB.

Scans ~/.claude/projects/-Users-admin/memory/ for entries that meet the
promotion criteria documented in LEARNING_LOOP.md, copies them into
memory-snapshots/auto-memory/ on a fresh branch, and opens a PR for human
approval.

Idempotent: a memory file already promoted (same content sha256) is skipped.

Usage:
    python scripts/auto_memory_promote.py                # dry-run + report
    python scripts/auto_memory_promote.py --apply        # write files, no PR
    python scripts/auto_memory_promote.py --apply --pr   # write + branch + PR

Exit code 0 = success, 1 = nothing to promote, 2 = error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

AUTO_MEMORY_DIR = Path(
    os.environ.get(
        "AUTO_MEMORY_DIR",
        Path.home() / ".claude" / "projects" / "-Users-admin" / "memory",
    )
)
MKB_ROOT = Path(
    os.environ.get("MKB_ROOT", Path(__file__).resolve().parent.parent)
)
SNAPSHOT_DIR = MKB_ROOT / "memory-snapshots" / "auto-memory"

EXCLUDED_PREFIXES = ("RESUME_HERE_", "_lifecycle_log", "active_work_registry")
DOCTRINAL_SENTINELS = (
    "LOCKED",
    "RATIFIED",
    "INTEL-3",
    "PAYOUT-1",
    "EMAIL-1",
    "DNS-1",
    "MIG-DEFER",
    "MIG-CANCEL",
    "AXIOM-",
    "CONSTITUTION",
    "DOCTRINE",
)
INDEX_FILE = SNAPSHOT_DIR / "INDEX.md"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

# ── Helpers ───────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Best-effort YAML-ish frontmatter parse. Returns {} on miss."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fm: dict = {}
    current_key = None
    for line in m.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        # Two-space-indented subkeys under metadata: get folded as dotted keys.
        if line.startswith("  ") and current_key == "metadata":
            sub = line.strip()
            if ":" in sub:
                k, _, v = sub.partition(":")
                fm[f"metadata.{k.strip()}"] = v.strip().strip("\"'")
            continue
        if ":" in line:
            k, _, v = line.partition(":")
            current_key = k.strip()
            fm[current_key] = v.strip().strip("\"'")
    return fm


def is_excluded(name: str) -> bool:
    return any(name.startswith(p) for p in EXCLUDED_PREFIXES)


def should_promote(path: Path, text: str, fm: dict) -> tuple[bool, str]:
    """Return (promote?, reason)."""
    if fm.get("promote_to_mkb", "").lower() == "false":
        return False, "explicit promote_to_mkb=false"
    if fm.get("promote_to_mkb", "").lower() == "true":
        return True, "explicit promote_to_mkb=true"
    if fm.get("lifecycle_state") == "canonical" and fm.get(
        "metadata.type"
    ) in {"feedback", "project", "reference"}:
        return True, "lifecycle_state=canonical + canonical type"
    if fm.get("metadata.type") == "feedback":
        return True, "behavioral feedback rule"
    body = text[len(FRONTMATTER_RE.match(text).group(0)) :] if FRONTMATTER_RE.match(text) else text
    head = body[:4000]
    for sentinel in DOCTRINAL_SENTINELS:
        if sentinel in head:
            return True, f"doctrinal sentinel: {sentinel}"
    return False, "no promotion criteria met"


def sha256_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def already_snapshotted(name: str, digest: str) -> bool:
    target = SNAPSHOT_DIR / name
    if not target.exists():
        return False
    existing = target.read_text(encoding="utf-8")
    return sha256_of(existing) == digest


def stamp_promoted_frontmatter(text: str, source: Path) -> str:
    """Insert `promoted_from:` + `promoted_at:` into the frontmatter."""
    m = FRONTMATTER_RE.match(text)
    promoted_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    promoted_line = (
        f"promoted_from: {source.name}\n"
        f"promoted_at: {promoted_at}\n"
    )
    if m:
        return (
            "---\n"
            + m.group(1).rstrip()
            + "\n"
            + promoted_line
            + "---\n"
            + text[m.end() :]
        )
    return (
        "---\n"
        + f"name: {source.stem}\n"
        + promoted_line
        + "---\n"
        + text
    )


def run(cmd: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write snapshot files")
    ap.add_argument("--pr", action="store_true", help="open a PR after writing")
    ap.add_argument("--branch", default=None, help="branch name (default auto)")
    args = ap.parse_args()

    if not AUTO_MEMORY_DIR.exists():
        print(f"ERROR: auto-memory dir not found: {AUTO_MEMORY_DIR}", file=sys.stderr)
        return 2

    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

    candidates = []
    for path in sorted(AUTO_MEMORY_DIR.glob("*.md")):
        if is_excluded(path.name):
            continue
        if path.name in {"MEMORY.md"}:
            continue
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        promote, reason = should_promote(path, text, fm)
        if not promote:
            continue
        digest = sha256_of(text)
        if already_snapshotted(path.name, digest):
            continue
        candidates.append((path, text, reason, digest))

    if not candidates:
        print("No new promotions.")
        return 1

    print(f"Found {len(candidates)} promotion candidates:")
    for path, _, reason, _ in candidates:
        print(f"  - {path.name} — {reason}")

    if not args.apply:
        print("\nRun with --apply to write snapshots.")
        return 0

    # Write snapshots
    for path, text, _reason, _digest in candidates:
        stamped = stamp_promoted_frontmatter(text, path)
        (SNAPSHOT_DIR / path.name).write_text(stamped, encoding="utf-8")

    # Update INDEX.md
    write_index()

    if not args.pr:
        print(f"\nWrote {len(candidates)} snapshot files. Use --pr to open a PR.")
        return 0

    # Open PR
    branch = args.branch or f"auto-memory/promote-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M')}"
    run(["git", "checkout", "-b", branch], cwd=MKB_ROOT)
    run(["git", "add", str(SNAPSHOT_DIR.relative_to(MKB_ROOT))], cwd=MKB_ROOT)
    commit_body = "\n".join(f"- {p.name} ({reason})" for p, _, reason, _ in candidates)
    run(
        ["git", "commit", "-m", f"auto-memory: promote {len(candidates)} entries\n\n{commit_body}"],
        cwd=MKB_ROOT,
    )
    run(["git", "push", "-u", "origin", branch], cwd=MKB_ROOT)
    pr_body = (
        "Auto-promoted from `~/.claude/projects/-Users-admin/memory/` per "
        "LEARNING_LOOP.md promotion criteria.\n\n"
        + "## Promoted entries\n\n"
        + commit_body
        + "\n\n_Generated by scripts/auto_memory_promote.py_"
    )
    run(
        [
            "gh",
            "pr",
            "create",
            "--title",
            f"auto-memory: promote {len(candidates)} canonical entries",
            "--body",
            pr_body,
            "--label",
            "auto-memory,learning-loop",
        ],
        cwd=MKB_ROOT,
    )
    print(f"\nOpened PR for branch {branch}.")
    return 0


def write_index() -> None:
    entries = sorted(SNAPSHOT_DIR.glob("*.md"))
    lines = [
        "# Auto-Memory Snapshots — Index",
        "",
        "Promoted from `~/.claude/projects/-Users-admin/memory/` by `scripts/auto_memory_promote.py`.",
        "See [LEARNING_LOOP.md](../../LEARNING_LOOP.md) for promotion criteria.",
        "",
        f"Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"Entries: {len([e for e in entries if e.name != 'INDEX.md'])}",
        "",
        "## Entries",
        "",
    ]
    for entry in entries:
        if entry.name == "INDEX.md":
            continue
        text = entry.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        desc = fm.get("description", "").strip()
        lines.append(f"- [{entry.stem}]({entry.name}) — {desc[:200]}")
    INDEX_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
