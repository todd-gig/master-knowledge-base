    ---
    title: Export Instructions
    tags:
      - export
  - ops
type: instructions-note
    status: draft
    created: 2026-03-26
    updated: 2026-03-26
    purpose: >
      Explain how to use and extend the export package.
    ---
# Export Instructions

## How to use

1. Open `README.md`.
2. Load `CLAUDE.md` into the project root context.
3. Keep `registry/project_index.json` available for routing.
4. Use `99_full_transcript.md` as the primary evidence source.
5. Extend machine files before productionizing.

## How to update

1. append new transcript material
2. re-run extraction
3. refresh Markdown summaries
4. sync JSON registries
5. run tests
6. build new zip
