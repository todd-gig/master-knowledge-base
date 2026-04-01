    ---
    title: Thread Export Package README
    tags:
      - thread-export
  - obsidian
  - knowledge-system
  - training-system
  - execution-system
type: thread-export-readme
    status: draft
    created: 2026-03-26
    updated: 2026-03-26
    purpose: >
      Package the visible conversation into a reusable Markdown and code bundle.
    ---
# Thread Export Package

## Scope

This package is generated from the **visible conversation only** in the current chat session.

## Included

- executive synthesis
- goals, insights, requirements, architecture, governance, deployment
- capability and negotiation system logic
- prompt/training files
- machine-readable configs and starter code
- full visible transcript captured in `99_full_transcript.md`

## Not Included

- hidden system instructions
- non-visible prior chats not shown in this thread
- external artifacts unless explicitly recreated here

## Recommended Use

1. Store this package in Obsidian or Git.
2. Use `CLAUDE.md` + `registry/project_index.json` as the root routing layer.
3. Extend the machine schemas before production deployment.
4. Use the transcript file as traceable source material for future codification.
