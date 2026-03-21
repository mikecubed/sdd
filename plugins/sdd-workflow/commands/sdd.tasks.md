---
description: "Generate an actionable, dependency-ordered task list from the feature plan."
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Check for headless mode**: If `$ARGUMENTS` contains `headless` or `--headless`, enable headless mode.

2. **Locate the feature directory**:
   - If a path or feature name is provided in `$ARGUMENTS`, use it
   - Otherwise, list `.sdd/` and ask the user (or auto-select most recent in headless mode)
   - If no plan exists: offer to run `/sdd.plan` first, proceed without it, or accept a manual path

3. **Load design documents** from `.sdd/{feature-dir}/`:
   - **Required**: `plan.md`, `spec.md`
   - **Optional**: `data-model.md`, `contracts/`, `research.md`

4. **Use the canonical tasks template embedded below**:
   ````md
# Tasks: [FEATURE NAME]

**Input**: Design documents from `.sdd/[feature-dir]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

## Format: `- [ ] T### [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize project with required dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational

**Purpose**: Core infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T004 Setup core infrastructure (database, auth, etc.)
- [ ] T005 [P] Implement shared utilities
- [ ] T006 Configure error handling and logging

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

- [ ] T007 [P] [US1] Create [Entity1] model in src/models/[entity1].py
- [ ] T008 [P] [US1] Create [Entity2] model in src/models/[entity2].py
- [ ] T009 [US1] Implement [Service] in src/services/[service].py
- [ ] T010 [US1] Implement [feature] in src/[location]/[file].py
- [ ] T011 [US1] Add validation and error handling

**Checkpoint**: User Story 1 fully functional and independently testable

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description]

**Independent Test**: [How to verify this story works on its own]

- [ ] T012 [P] [US2] Create [Entity] model in src/models/[entity].py
- [ ] T013 [US2] Implement [Service] in src/services/[service].py
- [ ] T014 [US2] Implement [feature] in src/[location]/[file].py

**Checkpoint**: User Stories 1 AND 2 work independently

---

[Add more user story phases as needed]

---

## Phase N: Polish

- [ ] TXXX [P] Documentation updates
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Security hardening

---

## Dependencies & Execution Order

- **Setup → Foundational → User Stories (in parallel) → Polish**
- User stories depend only on Foundational completion; they can run in parallel
- Within each story: Models → Services → Endpoints → Integration
````

5. **Generate the task list**:
   - Extract user stories from spec.md (with their priorities P1, P2, P3...)
   - Extract tech stack and project structure from plan.md
   - Organize tasks by user story — each story gets its own phase
   - Every task must follow the strict format: `- [ ] T### [P?] [US?] Description with file path`
   - Mark parallelizable tasks with `[P]`
   - Include dependency graph and parallel execution examples

6. **Write** tasks to `.sdd/{feature-dir}/tasks.md`

7. **Report**:
   - Total task count
   - Task count per user story
   - Parallel opportunities
   - Suggested MVP scope (typically User Story 1 only)

## Task Format

Every task MUST follow this exact format:
```
- [ ] T### [P?] [US?] Description with exact/file/path.ext
```

Examples:
- `- [ ] T001 Create project structure per implementation plan`
- `- [ ] T005 [P] Implement auth middleware in src/middleware/auth.py`
- `- [ ] T012 [P] [US1] Create User model in src/models/user.py`

## Next Steps (present after completion)

1. **Implement** — begin working through tasks.md in order
2. **Attempt Direct Implementation** — skip tasks and implement with this context:
   - Feature: [feature name]
   - Tech stack: [from plan]
   - Key requirements: [top FRs from spec]
   - Success criteria: [SC list from spec]
3. **Iterate on Tasks** — refine the task list
