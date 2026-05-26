"""PPIM (Predictably Profitable Interaction Management) shared validator library.

Canonical home of every cross-engine PPIM-signature invariant. Importable by
gigaton-gateway (stamp time), HME (envelope validation), and decision-engine
(rollup-read validation) so the four invariants of `ppim_attribution_chain`
are enforced by exactly one piece of code in three places.

Public surface — re-exported from `libs.ppim.attribution_chain`:
    GIGATON_ROOT, MAX_CHAIN_DEPTH
    validate_chain, is_terminated, is_within_depth_cap,
    has_no_self_attribution, leaf_matches_operator, repair_chain
"""

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

__all__ = [
    "GIGATON_ROOT",
    "MAX_CHAIN_DEPTH",
    "has_no_self_attribution",
    "is_terminated",
    "is_within_depth_cap",
    "leaf_matches_operator",
    "repair_chain",
    "validate_chain",
]
