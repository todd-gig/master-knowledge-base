# PRD — Gigaton Platform UI

## Objective
Create a unified control plane where operators can authenticate, communicate with Claude, manage users, review generated outputs, approve decisions, and monitor project execution.

## MVP Scope
- Google sign-in
- user profile creation
- tenant selection
- central messenger interface
- file/work sync status
- approvals queue
- decision engine output viewer
- client namespace viewer

## Acceptance Criteria
- User can log in with Google.
- User can access a dashboard.
- User can send a message to the configured AI endpoint.
- System stores message metadata.
- Generated outputs can be marked proposed/approved/rejected.
- Dashboard exposes current task/backlog state.

## Exclusions for MVP
- Complex billing
- Full multi-agent orchestration
- Full deployment automation
- Perfect visual design

## ROI Logic
This UI is the control surface that unlocks all downstream automation. Without it, Claude remains a disconnected tool instead of an operating system layer.
