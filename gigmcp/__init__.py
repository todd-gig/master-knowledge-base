"""gigmcp — Gigaton MCP industry-catalog integration package.

This package is the BATCH-CONSUMER side of gigmcp (Gigaton's Model Context
Protocol process). gigmcp itself is exposed to interactive Claude sessions
via stdio; here we read its industry-knowledge surface over HTTP (via the
sibling `gigmcp-export` Cloud Run service) and upsert canonical rows into
decision-engine's `industry_catalogs` table (Wave 1, migration 004).

Two facts to keep in mind reading this code:

1. **master-knowledge-base is a knowledge/governance repo by convention.**
   Per its CLAUDE.md, "Never put runnable application code here." The
   gigmcp/ tree is the one exception, justified by Wave-2 spec §"Repo":
   no separate `gigmcp` repo exists in `todd-gig`, and the integration
   surface is small enough (one batch script, no service) that creating
   a new repo would be more friction than insight. If this grows past
   ~1k LOC, lift it out into `todd-gig/gigmcp-platform`.

2. **This package writes to a sibling repo's database (decision-engine's
   Cloud SQL).** That coupling is intentional — gigmcp is the source of
   truth for industry canon; decision-engine is the consumer. The sync
   direction is gigmcp → decision-engine, never the reverse. If
   decision-engine's schema for `industry_catalogs` changes, this
   package's translator (translators/v1_to_industry_catalog.py) must
   change with it — flag in decision-engine PRs that touch
   `migrations/004_industry_catalogs.sql`.
"""

__version__ = "0.1.0"
