"""ppim_attribution_chain — canonical validator + repair helpers.

ppim_interaction: every artifact/event stamped by the gateway carries this chain
ppim_economics: enables CBP → CBP-walking-tour parent-share rollup in decision-engine
ppim_predictability: HIGH — four invariants asserted at stamp time AND read time
ppim_brand_dimension: coherence (cost/revenue rolls up to the licensing operator)

Format
------
    chain: list[str]  # leaf-first → root-last
    chain[0]  == operator_of_record (leaf)
    chain[-1] == "gigaton-root"     (platform sentinel)
    len(chain) ∈ [1, MAX_CHAIN_DEPTH]
    all elements distinct (no cycle)

Hard invariants (Phase-3 Spec B §"Self-attribution prevention rule")
--------------------------------------------------------------------
    I-1  TERMINATED          chain[-1] == "gigaton-root"
    I-2  LEAF-OF-RECORD      chain[0]  == operator_id-on-the-request
    I-3  DEPTH-CAP           len(chain) <= MAX_CHAIN_DEPTH (default 10)
    I-4  NO-SELF-ATTRIB      chain[0]  != "gigaton-root"  unless len(chain) == 1

I-4 prevents the platform-root operator from attributing revenue/cost back to
itself with a synthetic multi-element chain. The only valid chain for
operator_id == "gigaton-root" is the singleton ["gigaton-root"].

All four invariants are enforced by `validate_chain` and (defensively)
auto-fixed by `repair_chain` for non-malicious common breakage (missing
sentinel / depth overflow / accidental self-attribution from a misconfigured
seed). repair_chain is the fail-soft path used by the gateway middleware
when UAE returns a chain that's almost-but-not-quite-right; outright invalid
chains (cycles, empty leaf) raise.

Consumers
---------
    gigaton-gateway   stamp time   (api/middleware/attribution_chain.py)
    hme               ingest       (app/events/envelope.py — validates 422 on fail)
    decision-engine   rollup read  (app/rollups/attribution_rollup.py)
"""

from __future__ import annotations

from typing import Sequence

# ── Public constants ─────────────────────────────────────────────────────────

GIGATON_ROOT: str = "gigaton-root"
"""Platform-root sentinel — must appear as the LAST element of every chain."""

MAX_CHAIN_DEPTH: int = 10
"""Hard cap on chain length. Beyond this we truncate-from-the-middle in
repair_chain to preserve both leaf identity AND root termination. 10 hops
covers every plausible operator hierarchy (Gigaton → MSO → operator →
sub-brand → location → DBA → campaign → audience-segment + 2 slack)."""


# ── Per-invariant predicates (cheap, side-effect-free) ───────────────────────


def is_terminated(chain: Sequence[str]) -> bool:
    """I-1: chain ends in the GIGATON_ROOT sentinel."""
    return len(chain) >= 1 and chain[-1] == GIGATON_ROOT


def is_within_depth_cap(chain: Sequence[str], cap: int = MAX_CHAIN_DEPTH) -> bool:
    """I-3: chain length is within the depth cap (inclusive)."""
    return 1 <= len(chain) <= cap


def has_no_self_attribution(chain: Sequence[str]) -> bool:
    """I-4: leaf is not GIGATON_ROOT, unless the chain is the singleton root.

    A request from the platform-root operator MAY only carry ["gigaton-root"]
    — any longer chain claiming the leaf is the root is a self-attribution
    attempt (typically a misconfigured seed in UAE; never legitimate)."""
    if not chain:
        return False
    if chain[0] == GIGATON_ROOT:
        return len(chain) == 1
    return True


def leaf_matches_operator(chain: Sequence[str], operator_id: str) -> bool:
    """I-2: chain[0] is exactly the operator-of-record on the request."""
    return len(chain) >= 1 and chain[0] == operator_id


def _has_no_cycle(chain: Sequence[str]) -> bool:
    """All chain elements distinct (no operator appears twice)."""
    return len(set(chain)) == len(chain)


# ── Composite validator ──────────────────────────────────────────────────────


def validate_chain(
    chain: Sequence[str],
    operator_id: str | None = None,
    *,
    cap: int = MAX_CHAIN_DEPTH,
) -> tuple[bool, str]:
    """Return (valid, reason). Reason is empty on success, human-readable on fail.

    `operator_id=None` skips invariant I-2 — used by the rollup read path,
    which validates the chain shape independent of who's asking.
    """
    if chain is None:
        return False, "chain_is_none"
    if not isinstance(chain, (list, tuple)):
        return False, "chain_not_sequence"
    if len(chain) == 0:
        return False, "chain_empty"
    if not all(isinstance(e, str) and e for e in chain):
        return False, "chain_has_non_string_or_empty_element"

    if not is_terminated(chain):
        return False, f"chain_not_terminated_in_{GIGATON_ROOT!r}"
    if not is_within_depth_cap(chain, cap=cap):
        return False, f"chain_depth_{len(chain)}_exceeds_cap_{cap}"
    if not has_no_self_attribution(chain):
        return False, "chain_self_attributes_to_root"
    if not _has_no_cycle(chain):
        return False, "chain_contains_cycle"
    if operator_id is not None and not leaf_matches_operator(chain, operator_id):
        return False, f"chain_leaf_{chain[0]!r}_does_not_match_operator_{operator_id!r}"

    return True, ""


# ── Auto-repair (fail-soft path used by gateway when UAE returns almost-valid) ─


def repair_chain(
    chain: Sequence[str] | None,
    operator_id: str,
    *,
    cap: int = MAX_CHAIN_DEPTH,
) -> list[str]:
    """Return a chain that satisfies all four invariants for `operator_id`.

    Repair rules (idempotent + order-stable):
        R-1  None / empty           → [operator_id, GIGATON_ROOT]
                                    (or [GIGATON_ROOT] when operator_id IS root)
        R-2  Leaf mismatch          → prepend operator_id, dedupe, retry
        R-3  Self-attribution-root  → collapse to [operator_id, GIGATON_ROOT]
                                    when operator_id != GIGATON_ROOT;
                                    collapse to [GIGATON_ROOT] otherwise
        R-4  Missing sentinel       → append GIGATON_ROOT
        R-5  Cycle / dupes          → keep first occurrence, drop the rest
        R-6  Over depth-cap         → keep leaf + last `cap-1` ancestors
                                    (drops middle-of-chain; leaf + root always
                                    preserved per Spec B §"Ordering")

    The function NEVER raises — it always produces a valid chain. Caller logs
    a warning when the returned chain differs from the input (drift signal)."""
    # R-1 — empty / None
    if not chain:
        if operator_id == GIGATON_ROOT:
            return [GIGATON_ROOT]
        return [operator_id, GIGATON_ROOT]

    # Defensive copy + coerce to list[str], drop non-string / empty noise.
    cleaned: list[str] = [e for e in chain if isinstance(e, str) and e]

    if not cleaned:
        return [GIGATON_ROOT] if operator_id == GIGATON_ROOT else [operator_id, GIGATON_ROOT]

    # R-3 — self-attribution: leaf claims to be root but chain is longer.
    if cleaned[0] == GIGATON_ROOT and len(cleaned) > 1:
        if operator_id == GIGATON_ROOT:
            return [GIGATON_ROOT]
        # Operator is NOT root — fix by replacing the bogus leaf.
        cleaned = [operator_id] + [e for e in cleaned if e != GIGATON_ROOT] + [GIGATON_ROOT]

    # R-2 — leaf mismatch: ensure operator_id sits at position 0.
    if cleaned[0] != operator_id:
        if operator_id == GIGATON_ROOT:
            # Root operator MUST have the singleton chain — anything else is bogus.
            return [GIGATON_ROOT]
        cleaned = [operator_id] + [e for e in cleaned if e != operator_id]

    # R-5 — dedupe while preserving first-seen order.
    seen: set[str] = set()
    deduped: list[str] = []
    for e in cleaned:
        if e not in seen:
            seen.add(e)
            deduped.append(e)
    cleaned = deduped

    # R-4 — missing sentinel.
    if cleaned[-1] != GIGATON_ROOT:
        # Drop any stray non-last GIGATON_ROOT first (cycle prevention).
        cleaned = [e for e in cleaned if e != GIGATON_ROOT]
        cleaned.append(GIGATON_ROOT)

    # R-6 — depth cap: keep leaf + last (cap-1) elements. Last element is
    # always GIGATON_ROOT; second-to-last (cap-2) preserves closest ancestors.
    if len(cleaned) > cap:
        leaf = cleaned[0]
        tail = cleaned[-(cap - 1):]  # always ends in GIGATON_ROOT
        cleaned = [leaf] + tail

    # Final safety net — if repair somehow failed an invariant, fall back to
    # the minimal valid chain. This is unreachable in practice; defensive.
    ok, _reason = validate_chain(cleaned, operator_id, cap=cap)
    if not ok:
        if operator_id == GIGATON_ROOT:
            return [GIGATON_ROOT]
        return [operator_id, GIGATON_ROOT]

    return cleaned
