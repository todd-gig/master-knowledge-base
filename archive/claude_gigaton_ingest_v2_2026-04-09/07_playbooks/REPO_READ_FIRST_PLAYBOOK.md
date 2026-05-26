# Repo Read-First Playbook

## Goal
Prevent hallucinated implementation and avoid breaking existing code.

## Steps
1. Inspect root files: README, package files, lock files, config, env examples.
2. Identify app framework and runtime.
3. Locate auth, routing, database, API, state management, UI components.
4. Locate existing AI integrations.
5. Locate billing/payment logic.
6. Locate tests and CI.
7. Create current-state map.
8. Create gap matrix against package specs.
9. Propose smallest safe implementation.

## Required Output
- Repository summary
- Existing system map
- Missing pieces
- Risk list
- First PR plan
