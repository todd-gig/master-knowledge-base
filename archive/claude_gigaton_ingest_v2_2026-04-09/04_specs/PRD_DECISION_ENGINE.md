# PRD — Decision Engine

## Objective
Create a decision engine that ranks, routes, and governs work using ROI, urgency, confidence, dependency status, human impact, and reusability.

## Inputs
- user goal
- project context
- repo state
- source confidence
- cost estimate
- expected ROI
- time-to-impact
- risk
- reversibility

## Outputs
- recommended action
- priority score
- confidence score
- required approvals
- affected files/systems
- validation plan

## Decision Score Formula
priority_score = (roi_score * 0.30) + (speed_score * 0.20) + (reuse_score * 0.20) + (dependency_unblock_score * 0.15) + (risk_adjusted_confidence * 0.15)

## Approval Gates
Require human approval for:
- production deployment
- billing/payment changes
- auth/security changes
- destructive data operations
- client-facing commitments
- irreversible repo operations
