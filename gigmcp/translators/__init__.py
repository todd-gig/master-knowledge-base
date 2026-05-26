"""Translators map gigmcp-export response shapes to decision-engine
`industry_catalogs` rows.

Versioned because the gigmcp-export wire format is expected to evolve
faster than the decision-engine schema. Add `v2_to_industry_catalog.py`
when v2 ships; never bend the consumer schema to match a producer change.
"""
