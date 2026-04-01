    ---
    title: Runtime Governance
    tags:
      - governance
  - runtime
type: governance-note
    status: draft
    created: 2026-03-26
    updated: 2026-03-26
    purpose: >
      Define runtime controls and supervision logic.
    ---
# Runtime Governance

## Mandatory controls

- root instruction file must always be loaded first
- human-critical decisions must remain human-owned
- use the minimum viable team, not minimum thought
- include executive owner and support functions
- include negotiation workstreams when counterparties or approvals exist

## Audit requirements (inferred)

- retain transcript source
- preserve explicit vs inferred logic separation
- track version date on generated files
- keep machine-readable routing registry in sync with Markdown instructions

## Release gates (inferred)

A package is release-ready when:
1. all required files exist
2. YAML frontmatter is present
3. transcript is included
4. routing file resolves correctly
5. zip bundle builds successfully
