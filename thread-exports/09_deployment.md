    ---
    title: Deployment
    tags:
      - deployment
  - ops
type: deployment-note
    status: draft
    created: 2026-03-26
    updated: 2026-03-26
    purpose: >
      Describe deployment and packaging implications.
    ---
# Deployment

## Immediate deployment target

- local zip bundle
- Obsidian vault
- Claude project knowledge base
- Git-backed repo

## Recommended deployment path

1. store package in Git
2. validate machine JSON files
3. run tests
4. build export zip
5. ingest into Claude/other prompt system
6. use transcript-backed updates for future versions

## CI implications

- lint Markdown frontmatter
- validate JSON schemas
- verify required files
- build export bundle
