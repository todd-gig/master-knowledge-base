# Migrations

Alembic-style, ordered SQL migrations.

## Files
- `migration_manifest.json` - ordered migration metadata
- `001_initial_schema.sql` - baseline audit table
- `002_prompt_release_tables.sql` - prompt release governance tables
- `003_benchmark_runs.sql` - benchmark result storage
- `004_dashboard_views.sql` - dashboard-ready views

## Usage
Apply in manifest order. The Python migration runner can read the manifest and apply unapplied migrations.
