---
title: Artifact Template Pack v2
created: 2026-03-25
tags: [templates, agents, workflows, bundles]
status: ready
---

# Artifact Template Pack v2

## Scope Expansion
This pack extends v1 with:
- package/bundle templates
- agent templates
- workflow templates
- Google Sheets → MD auto-generation spec

## Objective
Enable Claude to:
- instantiate repeatable business artifacts
- orchestrate workflows
- deploy agents
- convert structured sheet data into executable markdown briefs

## File Groups
- `bundle_templates/`
- `agent_templates/`
- `workflow_templates/`
- `auto_generation_spec/`

## Usage Model
1. Populate MD template
2. Feed into Claude
3. Generate artifact / workflow / agent config
4. Execute or export
