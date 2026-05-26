"""Translates gigmcp-export v1 industry payload → decision-engine
`industry_catalogs` row dict.

Source shape (per spec §"What gigmcp is + what we're reading"):
    {
      "industry_tag": "vacation-rental-hospitality",
      "sub_vertical": "short-term-rental",          # optional
      "processes": [
          {"name": "booking", "description": "...",
           "distribution_stats": {...},
           "allowed_values": [...],                  # optional, for enum fields
           "field_type": "numeric|enum|free_text"},
          ...
      ],
      "signals": [
          {"name": "...", "definition": "...",
           "observable_proxies": ["...", "..."]},
          ...
      ],
      "etag": "sha256:abcd...",
      "updated_at": "2026-05-25T03:00:00Z",
      "multi_axis_tags": ["geo:NA", "regime:established", ...]   # optional
    }

Target row (per decision-engine migration 004):
    industry_catalogs(
      catalog_id UUID PK,
      operator_id TEXT,
      industry_slug TEXT,
      sub_vertical TEXT,
      catalog_json JSONB,             # {processes, escalations, frameworks,
                                      #  lifecycle_stages, pricing_models,
                                      #  signals, source: {etag,...}}
      process_count INT,              # GENERATED
      confidence_score REAL,
      seed_for_industry BOOLEAN,
      submitted_by_user_id UUID,
      submitted_at TIMESTAMPTZ,
      multi_axis_tags JSONB,
      ...
    )

gigmcp-sourced rows use:
    operator_id = 'gigmcp:canonical'             # sentinel
    submitted_by_user_id = GIGMCP_SENTINEL_UUID  # see below
    seed_for_industry = True
    confidence_score = 0.85                      # canonical-source default
    catalog_json.source = {provider, etag, source_url, fetched_at}
"""
from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


# Sentinel UUID for gigmcp-sourced submissions. Stable across runs — keep
# this constant once any environment has been seeded so re-runs UPDATE
# instead of clobbering. Generated from name 'gigmcp:canonical' via
# uuid.uuid5(uuid.NAMESPACE_URL, 'gigaton://gigmcp/canonical').
GIGMCP_SENTINEL_UUID = str(
    uuid.uuid5(uuid.NAMESPACE_URL, "gigaton://gigmcp/canonical")
)

GIGMCP_OPERATOR_ID = "gigmcp:canonical"
GIGMCP_PROVIDER_NAME = "gigmcp"
GIGMCP_DEFAULT_CONFIDENCE = 0.85


REQUIRED_TOP_LEVEL_KEYS = {"industry_tag", "processes", "etag", "updated_at"}
REQUIRED_PROCESS_KEYS = {"name"}


class TranslationError(ValueError):
    """Raised when a gigmcp payload cannot be translated. Caller logs +
    increments `skipped_malformed` and CONTINUES the sync — never aborts."""


def validate_payload(payload: Dict[str, Any]) -> None:
    """Cheap shape check. Raises TranslationError on the first missing
    required field. Does NOT validate semantic correctness (e.g. that
    distribution_stats are numeric); the consumer (decision-engine
    variance/compute.py) is responsible for graceful handling of bad
    distributions."""
    if not isinstance(payload, dict):
        raise TranslationError(f"payload is not a dict (got {type(payload).__name__})")
    missing = REQUIRED_TOP_LEVEL_KEYS - payload.keys()
    if missing:
        raise TranslationError(f"missing required keys: {sorted(missing)}")
    if not isinstance(payload["processes"], list):
        raise TranslationError("processes must be a list")
    for i, p in enumerate(payload["processes"]):
        if not isinstance(p, dict):
            raise TranslationError(f"processes[{i}] not a dict")
        pm = REQUIRED_PROCESS_KEYS - p.keys()
        if pm:
            raise TranslationError(f"processes[{i}] missing: {sorted(pm)}")


def translate(
    payload: Dict[str, Any],
    *,
    source_url: str,
    fetched_at: str,
) -> Dict[str, Any]:
    """Convert validated gigmcp payload → industry_catalogs row dict
    ready for upsert.

    Returns a dict whose keys are column names. process_count is
    GENERATED in the DB so we don't include it.
    """
    validate_payload(payload)

    catalog_json: Dict[str, Any] = {
        "processes": payload["processes"],
        "signals": payload.get("signals", []),
        "escalations": payload.get("escalations", []),
        "frameworks": payload.get("frameworks", []),
        "lifecycle_stages": payload.get("lifecycle_stages", []),
        "pricing_models": payload.get("pricing_models", []),
        "source": {
            "provider": GIGMCP_PROVIDER_NAME,
            "etag": payload["etag"],
            "source_url": source_url,
            "fetched_at": fetched_at,
            "source_updated_at": payload["updated_at"],
        },
    }

    return {
        "operator_id": GIGMCP_OPERATOR_ID,
        "industry_slug": payload["industry_tag"],
        "sub_vertical": payload.get("sub_vertical"),
        "catalog_json": catalog_json,
        "confidence_score": float(
            payload.get("confidence_score", GIGMCP_DEFAULT_CONFIDENCE)
        ),
        "seed_for_industry": True,
        "submitted_by_user_id": GIGMCP_SENTINEL_UUID,
        "multi_axis_tags": payload.get("multi_axis_tags", []),
        # The next two fields aren't columns — the sync uses them for
        # conflict resolution (see industry_sync.upsert_industry_catalog_row).
        "_source_etag": payload["etag"],
        "_source_updated_at": payload["updated_at"],
    }


def existing_row_etag(existing_catalog_json: Optional[Dict[str, Any]]) -> Optional[str]:
    """Pull the source.etag out of an existing catalog_json. Returns None
    if the existing row was submitted by an operator (no source block) or
    if catalog_json itself is None."""
    if not existing_catalog_json:
        return None
    src = existing_catalog_json.get("source")
    if not isinstance(src, dict):
        return None
    return src.get("etag")


def existing_row_source_updated_at(
    existing_catalog_json: Optional[Dict[str, Any]]
) -> Optional[str]:
    """Pull source.source_updated_at out of existing row, for the
    favor-newer comparison. Returns None for operator-submitted rows."""
    if not existing_catalog_json:
        return None
    src = existing_catalog_json.get("source")
    if not isinstance(src, dict):
        return None
    return src.get("source_updated_at")


__all__ = [
    "GIGMCP_SENTINEL_UUID",
    "GIGMCP_OPERATOR_ID",
    "GIGMCP_PROVIDER_NAME",
    "GIGMCP_DEFAULT_CONFIDENCE",
    "TranslationError",
    "validate_payload",
    "translate",
    "existing_row_etag",
    "existing_row_source_updated_at",
]
