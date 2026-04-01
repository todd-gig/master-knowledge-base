---
registry_name: gigaton_project_memory_registry
version: 2.0.0
format: json_md_hybrid
canonical: true
project: Gigaton
namespace_model: global_plus_client_overlays
---

# Memory Registry v2

This file mirrors the machine registry with a human-readable audit layer.

## MEM-001 — Trust Matrix + Value Matrix Integration
- **Tier**: 1
- **Category**: decision_systems
- **Type**: foundational_logic
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.96 (high)
- **Summary**: Core scoring and validation primitive combining trust qualification logic with the value matrix.
- **Tags**: trust_matrix, value_matrix, qualification, certification, validation_engine
- **Apply When**: building scoring engines, evaluating evidence, designing trust certificates, structuring decision workflows
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-002 — Executive Decision Engine
- **Tier**: 1
- **Category**: decision_systems
- **Type**: system_architecture
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.95 (high)
- **Summary**: Claude-oriented frontier decision engine for trust certificate to decision execution automation.
- **Tags**: executive_decision_model, authority_matrix, decision_state_machine, trust_certificate
- **Apply When**: building autonomous decision systems, designing approval logic, architecting execution governance
- **Dependencies**: MEM-001, MEM-003, MEM-005
- **Supersedes**: None
- **Deprecated**: False

## MEM-003 — Decision Execution Engine
- **Tier**: 1
- **Category**: decision_systems
- **Type**: service_layer
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.93 (high)
- **Summary**: Service layer that converts validated intelligence into actions, workflows, and outputs.
- **Tags**: decision_execution, service_layer, workflow_execution, action_engine
- **Apply When**: turning decisions into workflows, building service orchestration, mapping outputs to action
- **Dependencies**: MEM-002
- **Supersedes**: None
- **Deprecated**: False

## MEM-004 — First Principles Variable Registry
- **Tier**: 1
- **Category**: ontology_and_data_models
- **Type**: input_schema
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.94 (high)
- **Summary**: Universal categorized input schema for surveys, org modeling, and decision inputs.
- **Tags**: first_principles, input_schema, survey_model, org_inputs
- **Apply When**: creating templates, building data collection systems, modeling organizations, structuring decision inputs
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-005 — EO System
- **Tier**: 1
- **Category**: ontology_and_data_models
- **Type**: self_improving_intelligence_system
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.92 (medium_high)
- **Summary**: Ethnographic Object system with confidence scoring, self-healing question loops, research tasks, and router/code generation.
- **Tags**: EO, ethnographic_object, confidence_engine, self_healing_system, research_tasks
- **Apply When**: designing adaptive interviews, building recursive learning systems, creating research-backed routing logic
- **Dependencies**: MEM-004
- **Supersedes**: None
- **Deprecated**: False

## MEM-006 — Value of Human Contribution Matrix
- **Tier**: 1
- **Category**: commercial_systems
- **Type**: valuation_model
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.94 (high)
- **Summary**: Valuation model for time, effort, uniqueness, quality, network, and risk reduction across compensation and partnership contexts.
- **Tags**: human_value_matrix, compensation, equity, valuation, contribution_scoring
- **Apply When**: designing compensation, allocating equity, valuing partnerships, evaluating contributor impact
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-007 — Probabilistic Simulation Models
- **Tier**: 2
- **Category**: simulation_and_financial_models
- **Type**: forecasting_system
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.9 (medium_high)
- **Summary**: Monte Carlo and probabilistic modeling for adoption, retention, growth, and partner value.
- **Tags**: monte_carlo, forecasting, retention, adoption, portfolio_growth
- **Apply When**: forecasting growth, simulating deal outcomes, testing scenarios
- **Dependencies**: MEM-006
- **Supersedes**: None
- **Deprecated**: False

## MEM-008 — Experience Engineering Equation
- **Tier**: 2
- **Category**: simulation_and_financial_models
- **Type**: economic_model
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.91 (medium_high)
- **Summary**: Core equation linking brand and interaction management to revenue and predictable profitability.
- **Tags**: experience_engineering, brand_interaction, profitability_model, scenario_analysis
- **Apply When**: building dashboards, modeling revenue, designing CX systems
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-009 — Organizational Intelligence Structure
- **Tier**: 2
- **Category**: organizational_models
- **Type**: org_template
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.89 (medium_high)
- **Summary**: CEO plus 6 C-suite functional model with structured sub-entities and support agents.
- **Tags**: org_structure, c_suite_model, resource_template, entity_architecture
- **Apply When**: designing org charts, mapping responsibilities, identifying structural gaps
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-010 — Structure vs Framework vs Harness Model
- **Tier**: 3
- **Category**: organizational_models
- **Type**: conceptual_architecture
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.86 (medium)
- **Summary**: Model defining the difference between static organization, reusable system logic, and execution control layers.
- **Tags**: structure, framework, harness, system_design
- **Apply When**: explaining architecture, defining system layers, mapping business components
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-011 — Obsidian MD System Standard
- **Tier**: 1
- **Category**: knowledge_infrastructure
- **Type**: documentation_standard
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.97 (high)
- **Summary**: Project-wide markdown system requiring YAML frontmatter, Templater readiness, and maximum data capture with minimum leakage.
- **Tags**: obsidian, markdown_standard, templater, knowledge_capture
- **Apply When**: creating markdown files, building project docs, structuring reusable notes
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-012 — Universal MD Response Contract
- **Tier**: 1
- **Category**: knowledge_infrastructure
- **Type**: output_standard
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.96 (high)
- **Summary**: Universal output contract requiring structure, reusability, and machine-ingestibility in markdown.
- **Tags**: md_contract, output_standard, machine_ingestible, structured_output
- **Apply When**: responding with files, creating artifacts, designing reusable outputs
- **Dependencies**: MEM-011
- **Supersedes**: None
- **Deprecated**: False

## MEM-013 — MD Transformation Engine
- **Tier**: 2
- **Category**: platform_and_tooling
- **Type**: productizable_tool
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.88 (medium_high)
- **Summary**: Firebase-based app that transforms raw markdown into optimized Obsidian-ready markdown through a Python pipeline.
- **Tags**: firebase, markdown_transformer, obsidian_optimizer, python_pipeline
- **Apply When**: designing FE tools, automating markdown cleanup, productizing knowledge workflows
- **Dependencies**: MEM-011, MEM-012
- **Supersedes**: None
- **Deprecated**: False

## MEM-014 — Claude + External Systems Integration
- **Tier**: 2
- **Category**: platform_and_tooling
- **Type**: integration_pattern
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.87 (medium)
- **Summary**: Integration logic for Firebase, deployment pipelines, and connector-based intelligence workflows.
- **Tags**: claude_integration, firebase, deployment, connectors
- **Apply When**: connecting AI to platforms, building deployment flows, architecting automation
- **Dependencies**: MEM-013
- **Supersedes**: None
- **Deprecated**: False

## MEM-015 — Gigaton Value Matrix
- **Tier**: 1
- **Category**: commercial_systems
- **Type**: core_ip
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.97 (high)
- **Summary**: Core monetization logic driving partnerships, contracts, and performance engineering.
- **Tags**: gigaton_value_matrix, core_ip, partnerships, performance_logic
- **Apply When**: structuring deals, building contracts, evaluating commercial value
- **Dependencies**: MEM-001, MEM-006
- **Supersedes**: None
- **Deprecated**: False

## MEM-016 — Cross-Licensing + Term Sheet Structures
- **Tier**: 2
- **Category**: commercial_systems
- **Type**: deal_framework
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.9 (medium_high)
- **Summary**: Commercial structures for investor, SMB, operator, and Blue Ocean deal variants.
- **Tags**: cross_licensing, term_sheet, deal_structure, commercial_framework
- **Apply When**: drafting commercial terms, structuring partner agreements, designing licensing models
- **Dependencies**: MEM-015
- **Supersedes**: None
- **Deprecated**: False

## MEM-017 — Negotiation + Operator Playbook
- **Tier**: 2
- **Category**: commercial_systems
- **Type**: execution_playbook
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.89 (medium_high)
- **Summary**: Simulation-backed negotiation framework for operator deals and value-based structuring.
- **Tags**: negotiation, operator_playbook, deal_strategy, simulation_backed_terms
- **Apply When**: preparing negotiations, optimizing commercial leverage, running deal scenarios
- **Dependencies**: MEM-007, MEM-016
- **Supersedes**: None
- **Deprecated**: False

## MEM-018 — Gigaton Axiom Registry + Constitution
- **Tier**: 1
- **Category**: foundational_doctrine
- **Type**: doctrinal_system
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.98 (high)
- **Summary**: Foundational philosophical and logical core of the ecosystem, including first principles, constitutions, multi-language logic expansion, and proof-oriented structure.
- **Tags**: axiom_registry, constitution, first_principles, doctrine, proof_structure
- **Apply When**: deriving principles, resolving conflicts, building foundational systems
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-019 — Human-Tech Co-Evolution Framework
- **Tier**: 1
- **Category**: foundational_doctrine
- **Type**: guiding_framework
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.98 (high)
- **Summary**: Connect, Create, Thrive, Evolve framework embedded across all systems.
- **Tags**: connect_create_thrive_evolve, human_tech_coevolution, guiding_framework
- **Apply When**: framing strategy, aligning systems, evaluating mission fit
- **Dependencies**: None
- **Supersedes**: None
- **Deprecated**: False

## MEM-020 — Portable System Prompt Contract
- **Tier**: 1
- **Category**: knowledge_infrastructure
- **Type**: root_control_layer
- **Status**: active
- **Namespace**: global
- **Confidence**: 0.97 (high)
- **Summary**: Portable control layer encoding project logic, constraints, frameworks, and behavior into reusable system prompts.
- **Tags**: system_prompt_contract, portable_prompt, root_control_layer, behavioral_logic
- **Apply When**: creating AI prompt layers, encoding behavior, porting system logic between models
- **Dependencies**: MEM-011, MEM-012, MEM-018, MEM-019
- **Supersedes**: None
- **Deprecated**: False
