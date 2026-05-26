# Gigaton AI OS Architecture

## Architecture Thesis
Gigaton is an AI OS for business creation.

## Layers

### 1. Identity + Access Layer
- Google auth
- tenant/user model
- role-based permissions
- account linking

### 2. Data + Memory Layer
- Google Drive
- GitHub repos
- documents/transcripts
- client namespace files
- memory registry

### 3. Intelligence Layer
- Claude orchestration
- decision engine
- retrieval policy
- trust/value scoring
- first-principles variable registry

### 4. Execution Layer
- task generation
- code generation
- workflow automation
- approval queues
- deployment triggers

### 5. Productization Layer
- brand engine
- interaction management engine
- proposal generator
- client onboarding generator
- billing/payment hooks

### 6. Control Plane UI
- dashboard
- messenger
- approvals
- repo/access status
- payment/status panels
- provider health

## Architecture Rule
Every external dependency must be behind an adapter or interface. No provider-specific leakage into product logic.
