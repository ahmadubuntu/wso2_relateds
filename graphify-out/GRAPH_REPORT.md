# Graph Report - wso2_relateds  (2026-09-29)

## Corpus Check
- 36 files · ~34,158 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 304 nodes · 382 edges · 24 communities
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)
- AGENTS
- Kibana dashboard: APIM top users over time
- Any
- common.sh
- Tasks: [FEATURE NAME]
- speckit-analyze/SKILL.md
- Execution Steps
- Feature Specification: [FEATURE NAME]
- speckit-plan/SKILL.md
- speckit-specify/SKILL.md
- speckit-tasks/SKILL.md
- Core Principles
- Core Principles
- create-new-feature.sh script
- Implementation Plan: [FEATURE]
- speckit-checklist/SKILL.md
- CharismaInsurance File/download → 404 (bidirectional Unicode in resource)
- speckit-clarify/SKILL.md
- speckit-implement/SKILL.md
- speckit-constitution/SKILL.md
- speckit-taskstoissues/SKILL.md
- CharismaInsurance File/download — fix applied
- [CHECKLIST TYPE] Checklist: [FEATURE NAME]

## God Nodes (most connected - your core abstractions)
1. `PublisherClient` - 16 edges
2. `_http()` - 13 edges
3. `Tasks: [FEATURE NAME]` - 13 edges
4. `ApimError` - 11 edges
5. `راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)` - 11 edges
6. `create-new-feature.sh script` - 10 edges
7. `get_repo_root()` - 8 edges
8. `get_feature_paths()` - 8 edges
9. `resolve_template_content()` - 8 edges
10. `setup-tasks.sh script` - 8 edges

## Surprising Connections (you probably didn't know these)
- `create-new-feature.sh script` --calls--> `get_repo_root()`  [EXTRACTED]
  .specify/scripts/bash/create-new-feature.sh → .specify/scripts/bash/common.sh
- `create-new-feature.sh script` --calls--> `_persist_feature_json()`  [EXTRACTED]
  .specify/scripts/bash/create-new-feature.sh → .specify/scripts/bash/common.sh
- `create-new-feature.sh script` --calls--> `resolve_template_content()`  [EXTRACTED]
  .specify/scripts/bash/create-new-feature.sh → .specify/scripts/bash/common.sh
- `check-prerequisites.sh script` --calls--> `check_dir()`  [EXTRACTED]
  .specify/scripts/bash/check-prerequisites.sh → .specify/scripts/bash/common.sh
- `check-prerequisites.sh script` --calls--> `check_file()`  [EXTRACTED]
  .specify/scripts/bash/check-prerequisites.sh → .specify/scripts/bash/common.sh

## Import Cycles
- None detected.

## Communities (24 total, 0 thin omitted)

### Community 0 - "راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)"
Cohesion: 0.11
Nodes (18): اثبات با curl (مستقیم به Rayan), اختیاری (سخت‌گیرانه / دفاعی), تغییر پیشنهادی, خلاصه مشکل, خلاصه یک‌خطی برای همکار, راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI), ریپو و برنچ, علت ریشه‌ای (Root Cause) (+10 more)

### Community 1 - "AGENTS"
Cohesion: 0.12
Nodes (14): AGENTS, Configure / run, Current focus, Landmines, Layout, Plans, Purpose, Secrets (+6 more)

### Community 2 - "Kibana dashboard: APIM top users over time"
Cohesion: 0.40
Nodes (4): Constraints, Decisions, Kibana dashboard: APIM top users over time, Steps

### Community 3 - "Any"
Cohesion: 0.18
Nodes (17): Any, RuntimeError, ApimError, build_deploy_payload(), ensure_api_scope(), ensure_revision_capacity(), grant_scope_on_ops(), _http() (+9 more)

### Community 4 - "common.sh"
Cohesion: 0.17
Nodes (22): check-prerequisites.sh script, check_dir(), check_file(), find_specify_root(), format_speckit_command(), get_current_branch(), get_feature_paths(), get_invoke_separator() (+14 more)

### Community 5 - "Tasks: [FEATURE NAME]"
Cohesion: 0.07
Nodes (26): Dependencies & Execution Order, Format: `[ID] [P?] [Story] Description`, Implementation for User Story 1, Implementation for User Story 2, Implementation for User Story 3, Implementation Strategy, Incremental Delivery, MVP First (User Story 1 Only) (+18 more)

### Community 6 - "speckit-analyze/SKILL.md"
Cohesion: 0.08
Nodes (25): 1. Initialize Analysis Context, 2. Load Artifacts (Progressive Disclosure), 3. Build Semantic Models, 4. Detection Passes (Token-Efficient Analysis), 5. Severity Assignment, 6. Produce Compact Analysis Report, 7. Provide Next Actions, 8. Offer Remediation (+17 more)

### Community 7 - "Execution Steps"
Cohesion: 0.12
Nodes (15): 1. Initialize Convergence Context, 2. Load Artifacts (Progressive Disclosure), 3. Build the Intent Inventory, 4. Assess the Codebase and Classify Findings, 5. Assign Severity, 6. Present the In-Session Findings Summary, 7. Append Convergence Tasks (or report converged), 8. Provide Next Actions (Handoff) (+7 more)

### Community 8 - "Feature Specification: [FEATURE NAME]"
Cohesion: 0.15
Nodes (12): Assumptions, Edge Cases, Feature Specification: [FEATURE NAME], Functional Requirements, Key Entities *(include if feature involves data)*, Measurable Outcomes, Requirements *(mandatory)*, Success Criteria *(mandatory)* (+4 more)

### Community 9 - "speckit-plan/SKILL.md"
Cohesion: 0.18
Nodes (10): Completion Report, Done When, Key rules, Mandatory Post-Execution Hooks, Outline, Phase 0: Outline & Research, Phase 1: Design & Contracts, Phases (+2 more)

### Community 10 - "speckit-specify/SKILL.md"
Cohesion: 0.18
Nodes (10): Completion Report, Done When, For AI Generation, Mandatory Post-Execution Hooks, Outline, Pre-Execution Checks, Quick Guidelines, Section Requirements (+2 more)

### Community 11 - "speckit-tasks/SKILL.md"
Cohesion: 0.18
Nodes (10): Checklist Format (REQUIRED), Completion Report, Done When, Mandatory Post-Execution Hooks, Outline, Phase Structure, Pre-Execution Checks, Task Generation Rules (+2 more)

### Community 12 - "Core Principles"
Cohesion: 0.18
Nodes (10): Core Principles, Governance, [PRINCIPLE_1_NAME], [PRINCIPLE_2_NAME], [PRINCIPLE_3_NAME], [PRINCIPLE_4_NAME], [PRINCIPLE_5_NAME], [PROJECT_NAME] Constitution (+2 more)

### Community 13 - "Core Principles"
Cohesion: 0.18
Nodes (10): Core Principles, Governance, [PRINCIPLE_1_NAME], [PRINCIPLE_2_NAME], [PRINCIPLE_3_NAME], [PRINCIPLE_4_NAME], [PRINCIPLE_5_NAME], [PROJECT_NAME] Constitution (+2 more)

### Community 14 - "create-new-feature.sh script"
Cohesion: 0.44
Nodes (7): clean_branch_name(), fit_branch_name(), generate_branch_name(), get_highest_from_specs(), is_feature_number_in_range(), create-new-feature.sh script, spec_prefix_exists()

### Community 15 - "Implementation Plan: [FEATURE]"
Cohesion: 0.22
Nodes (8): Complexity Tracking, Constitution Check, Documentation (this feature), Implementation Plan: [FEATURE], Project Structure, Source Code (repository root), Summary, Technical Context

### Community 16 - "speckit-checklist/SKILL.md"
Cohesion: 0.25
Nodes (7): Anti-Examples: What NOT To Do, Checklist Purpose: "Unit Tests for English", Example Checklist Types & Sample Items, Execution Steps, Post-Execution Checks, Pre-Execution Checks, User Input

### Community 17 - "CharismaInsurance File/download → 404 (bidirectional Unicode in resource)"
Cohesion: 0.25
Nodes (7): CharismaInsurance File/download → 404 (bidirectional Unicode in resource), Constraints, Corrupted definition in Publisher / swagger, Evidence (logged in with `WSO2_PRD_USER` / `WSO2_PRD_PASS`), Fix (Publisher — do not leave bidi in path), Open, Verdict

### Community 18 - "speckit-clarify/SKILL.md"
Cohesion: 0.29
Nodes (6): Completion Report, Done When, Mandatory Post-Execution Hooks, Outline, Pre-Execution Checks, User Input

### Community 19 - "speckit-implement/SKILL.md"
Cohesion: 0.29
Nodes (6): Completion Report, Done When, Mandatory Post-Execution Hooks, Outline, Pre-Execution Checks, User Input

### Community 20 - "speckit-constitution/SKILL.md"
Cohesion: 0.33
Nodes (5): Outline, Post-Execution Checks, Pre-Execution Checks, Scope Guard, User Input

### Community 21 - "speckit-taskstoissues/SKILL.md"
Cohesion: 0.40
Nodes (4): Outline, Post-Execution Checks, Pre-Execution Checks, User Input

### Community 22 - "CharismaInsurance File/download — fix applied"
Cohesion: 0.40
Nodes (4): CharismaInsurance File/download — fix applied, Client note, Done, Verify

### Community 23 - "[CHECKLIST TYPE] Checklist: [FEATURE NAME]"
Cohesion: 0.40
Nodes (4): [Category 1], [Category 2], [CHECKLIST TYPE] Checklist: [FEATURE NAME], Notes

## Knowledge Gaps
- **179 isolated node(s):** `common.sh script`, `User Input`, `Pre-Execution Checks`, `Goal`, `Operating Constraints` (+174 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 195 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `common.sh script`, `User Input`, `Pre-Execution Checks` to the rest of the system?**
  _179 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `راهنمای رفع 403 سرویس `lastWorkingDate` (Rayan Portfolio / WSO2 MI)` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `AGENTS` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `Tasks: [FEATURE NAME]` be split into smaller, more focused modules?**
  _Cohesion score 0.07407407407407407 - nodes in this community are weakly interconnected._
- **Should `speckit-analyze/SKILL.md` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Should `Execution Steps` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._