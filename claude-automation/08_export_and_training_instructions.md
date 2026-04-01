---
title: Export and Training Instructions
version: 1.0.0
status: active
tags: [export, training, obsidian, claude]
---

# Export Modes
## Mode A — Claude Project
Use:
- `CLAUDE.md`
- all numbered Markdown files

## Mode B — Repo Root
Place:
- `CLAUDE.md` at repo root
- supporting notes in `/docs/claude/` or equivalent

## Mode C — Obsidian Vault
Store the Markdown files as notes and preserve filenames for link integrity.

## Mode D — Runtime Service
Use:
- `machine/`
- `python/`
- `migrations/`
- `sql/`
- `registry/`
- `tests/`

# Training Guidance
Train Claude on:
1. routing logic,
2. cost logic,
3. migration logic,
4. release governance,
5. benchmarking framework,
6. deployment playbook.

# Rule
Do not train on raw thread noise if distilled logic exists.
Use distilled artifacts first, then raw transcripts only if deeper reconstruction is required.
