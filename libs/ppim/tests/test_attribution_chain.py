"""Tests for libs/ppim/attribution_chain.py — every predicate + repair_chain.

Covers the four invariants in isolation, the composite validator, and the
six repair rules (R-1..R-6) plus idempotency of repair_chain.
"""

from __future__ import annotations

import pytest

from libs.ppim.attribution_chain import (
    GIGATON_ROOT,
    MAX_CHAIN_DEPTH,
    has_no_self_attribution,
    is_terminated,
    is_within_depth_cap,
    leaf_matches_operator,
    repair_chain,
    validate_chain,
)


# ── 1. is_terminated ─────────────────────────────────────────────────────────


def test_is_terminated_positive_and_negative():
    assert is_terminated(["op", GIGATON_ROOT])
    assert is_terminated([GIGATON_ROOT])
    assert not is_terminated(["op"])
    assert not is_terminated([])
    assert not is_terminated(["op", "parent"])  # missing sentinel


# ── 2. is_within_depth_cap ───────────────────────────────────────────────────


def test_is_within_depth_cap_boundaries():
    assert is_within_depth_cap([GIGATON_ROOT])  # min length 1
    assert is_within_depth_cap(["a"] * (MAX_CHAIN_DEPTH - 1) + [GIGATON_ROOT])
    assert not is_within_depth_cap([])
    assert not is_within_depth_cap(["a"] * (MAX_CHAIN_DEPTH + 1))
    # explicit cap override
    assert is_within_depth_cap(["a", "b", GIGATON_ROOT], cap=3)
    assert not is_within_depth_cap(["a", "b", "c", GIGATON_ROOT], cap=3)


# ── 3. has_no_self_attribution ───────────────────────────────────────────────


def test_has_no_self_attribution_blocks_root_multi_hop():
    # Legit: non-root leaf
    assert has_no_self_attribution(["cbp", GIGATON_ROOT])
    # Legit: root operator with singleton chain
    assert has_no_self_attribution([GIGATON_ROOT])
    # ILLEGAL: root claims to be its own leaf in a multi-hop chain
    assert not has_no_self_attribution([GIGATON_ROOT, "ghost-parent", GIGATON_ROOT])
    assert not has_no_self_attribution([GIGATON_ROOT, GIGATON_ROOT])
    # Empty
    assert not has_no_self_attribution([])


# ── 4. leaf_matches_operator ─────────────────────────────────────────────────


def test_leaf_matches_operator():
    assert leaf_matches_operator(["cbp-walking-tour", "cbp", GIGATON_ROOT], "cbp-walking-tour")
    assert not leaf_matches_operator(["cbp", GIGATON_ROOT], "cbp-walking-tour")
    assert not leaf_matches_operator([], "cbp")


# ── 5. validate_chain (composite) — happy path ───────────────────────────────


def test_validate_chain_happy_path():
    ok, reason = validate_chain(
        ["cbp-walking-tour", "cbp", GIGATON_ROOT], "cbp-walking-tour"
    )
    assert ok and reason == ""


# ── 6. validate_chain — every negative branch ────────────────────────────────


def test_validate_chain_negative_cases():
    # None / wrong type
    ok, r = validate_chain(None, "cbp")  # type: ignore[arg-type]
    assert not ok and "none" in r
    ok, r = validate_chain("not-a-list", "cbp")  # type: ignore[arg-type]
    assert not ok and "not_sequence" in r
    # Empty
    ok, r = validate_chain([], "cbp")
    assert not ok and "empty" in r
    # Non-string element
    ok, r = validate_chain(["cbp", 123, GIGATON_ROOT], "cbp")  # type: ignore[list-item]
    assert not ok and "non_string" in r
    # Missing terminator
    ok, r = validate_chain(["cbp", "parent"], "cbp")
    assert not ok and "not_terminated" in r
    # Depth-cap
    big = [f"hop-{i}" for i in range(MAX_CHAIN_DEPTH)] + [GIGATON_ROOT]
    ok, r = validate_chain(big, "hop-0")
    assert not ok and "exceeds_cap" in r
    # Self-attribution
    ok, r = validate_chain([GIGATON_ROOT, "parent", GIGATON_ROOT], GIGATON_ROOT)
    assert not ok and ("self_attributes" in r or "cycle" in r)
    # Cycle
    ok, r = validate_chain(["a", "b", "a", GIGATON_ROOT], "a")
    assert not ok and "cycle" in r
    # Leaf mismatch (only checked when operator_id supplied)
    ok, r = validate_chain(["cbp", GIGATON_ROOT], "cbp-walking-tour")
    assert not ok and "does_not_match_operator" in r


# ── 7. repair_chain — R-1 empty/None input ──────────────────────────────────


def test_repair_chain_empty_input():
    assert repair_chain(None, "cbp-walking-tour") == ["cbp-walking-tour", GIGATON_ROOT]
    assert repair_chain([], "cbp-walking-tour") == ["cbp-walking-tour", GIGATON_ROOT]
    # Root operator → singleton
    assert repair_chain(None, GIGATON_ROOT) == [GIGATON_ROOT]
    assert repair_chain([], GIGATON_ROOT) == [GIGATON_ROOT]


# ── 8. repair_chain — R-2/R-3/R-4 leaf-mismatch, self-attrib, missing sentinel ─


def test_repair_chain_fixes_common_breakage():
    # R-4 missing sentinel
    out = repair_chain(["cbp-walking-tour", "cbp"], "cbp-walking-tour")
    assert out == ["cbp-walking-tour", "cbp", GIGATON_ROOT]

    # R-2 leaf mismatch — operator_id prepended, deduped
    out = repair_chain(["cbp", GIGATON_ROOT], "cbp-walking-tour")
    assert out == ["cbp-walking-tour", "cbp", GIGATON_ROOT]

    # R-3 self-attribution collapsed for non-root operator
    out = repair_chain([GIGATON_ROOT, "ghost", GIGATON_ROOT], "cbp-walking-tour")
    assert out[0] == "cbp-walking-tour"
    assert out[-1] == GIGATON_ROOT
    assert GIGATON_ROOT not in out[:-1]

    # R-3 self-attribution collapsed for root operator → singleton
    assert repair_chain([GIGATON_ROOT, "anything", GIGATON_ROOT], GIGATON_ROOT) == [GIGATON_ROOT]


# ── 9. repair_chain — R-5/R-6 dedupe + depth-cap truncation ─────────────────


def test_repair_chain_dedupes_and_caps_depth():
    # R-5 dedupe preserves first occurrence
    out = repair_chain(["a", "b", "a", "c", GIGATON_ROOT], "a")
    assert out == ["a", "b", "c", GIGATON_ROOT]

    # R-6 depth-cap truncation: leaf preserved, sentinel preserved, middle dropped
    chain = [f"op-{i}" for i in range(MAX_CHAIN_DEPTH + 5)] + [GIGATON_ROOT]
    out = repair_chain(chain, "op-0")
    assert len(out) == MAX_CHAIN_DEPTH
    assert out[0] == "op-0"
    assert out[-1] == GIGATON_ROOT
    # Ensure the dropped slice came from the MIDDLE, not the boundary.
    assert out[1] != "op-1"  # earliest ancestors were dropped


# ── 10. repair_chain idempotency + always-valid post-condition ──────────────


def test_repair_chain_is_idempotent_and_always_valid():
    pathological_inputs = [
        None,
        [],
        ["cbp-walking-tour"],
        ["cbp-walking-tour", "cbp"],
        ["wrong-leaf", GIGATON_ROOT],
        [GIGATON_ROOT, "x", GIGATON_ROOT],
        ["a", "b", "a", "c", "b", GIGATON_ROOT],
        [f"hop-{i}" for i in range(50)] + [GIGATON_ROOT],
    ]
    for raw in pathological_inputs:
        once = repair_chain(raw, "cbp-walking-tour")
        ok, reason = validate_chain(once, "cbp-walking-tour")
        assert ok, f"repair_chain produced invalid chain for {raw!r}: {reason}"
        # Idempotency — repairing a repaired chain must be a no-op.
        twice = repair_chain(once, "cbp-walking-tour")
        assert twice == once, f"repair_chain not idempotent for {raw!r}: {once} → {twice}"


# Pytest sanity guard so this file is collectable even if the package layout
# changes (we depend on the libs/ root being on sys.path).
def test_package_importable():
    from libs.ppim import validate_chain as _v  # noqa: F401
    assert _v is validate_chain
