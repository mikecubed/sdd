"""Embedded agent command and skill content for Claude Code and GitHub Copilot."""

# ---------------------------------------------------------------------------
# Claude Code — .claude/commands/
# ---------------------------------------------------------------------------

CLAUDE_SPECIFY_MD = """\
---
description: "Create a feature specification from a natural language description."
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Given the feature description in `$ARGUMENTS`, do this:

1. **Check for headless mode**: If `$ARGUMENTS` contains `headless` or `--headless`, enable headless mode — auto-accept all recommended defaults and complete without pausing for user input.

2. **Generate a feature directory name**:
   - Derive a short 2-4 word slug from the feature description (e.g., "user-auth", "analytics-dashboard")
   - Append an 8-character random alphanumeric suffix separated by a dash (e.g., `user-auth-a3f9b2c1`)
   - Full path: `.sdd/{slug}-{suffix}/`

3. **Create the feature directory** and all required parent directories.

4. **Get the specification template**:
   ```bash
   sdd template specification
   ```

5. **Generate the specification** by filling the template:
   - Replace `[FEATURE NAME]` with a human-readable feature name
   - Replace `[DATE]` with today's date
   - Replace `$ARGUMENTS` placeholder with the actual user description
   - Fill in user stories (at least 2), functional requirements, and success criteria
   - Mark genuinely unclear decisions as `[NEEDS CLARIFICATION: specific question]` — maximum 3 markers
   - Document assumptions in the spec

6. **Write** the filled specification to `.sdd/{feature-dir}/spec.md`.

7. **Quality validation** — validate the spec against these criteria:
   - No implementation details (no languages, frameworks, APIs in spec)
   - All mandatory sections completed (user stories, requirements, success criteria)
   - Requirements are testable and unambiguous
   - Success criteria are measurable and technology-agnostic
   - No more than 3 `[NEEDS CLARIFICATION]` markers

8. **Handle clarifications** (skip in headless mode — auto-resolve with reasonable defaults):
   - If `[NEEDS CLARIFICATION]` markers remain, present at most 3 questions to the user
   - Wait for answers, update spec, re-validate
   - If after 3 iterations issues remain, document them in spec notes and continue

9. **Write quality checklist** to `.sdd/{feature-dir}/checklists/requirements.md`:
   ```bash
   sdd template specification-checklist
   ```
   Fill it with pass/fail status based on the validation above.

10. **Report completion** with:
    - Feature directory path
    - Spec file path
    - Checklist summary

## Next Steps (present after completion)

Present these options to the user (auto-select option 1 in headless mode):

1. **Create Implementation Plan** — run `/sdd.plan` to produce a technical design
2. **Attempt Direct Implementation** — proceed to implement based on spec alone, with this context:
   - Feature: [feature name]
   - Key requirements: [top 3 FRs from spec]
   - Success criteria: [SC list from spec]
3. **Iterate on Spec** — refine the specification further

## Guidelines

- Focus on **WHAT** users need and **WHY** — avoid HOW to implement
- No technology choices, frameworks, or code structure in specs
- Every requirement must be independently testable
- Limit clarifications to decisions that genuinely impact scope or security
"""

CLAUDE_PLAN_MD = """\
---
description: "Create an implementation plan from a feature specification."
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
   - Otherwise, list `.sdd/` and ask the user which feature to plan (or auto-select the most recent in headless mode)
   - If no spec exists: offer to run `/sdd.specify` first, proceed ad-hoc, or accept a manual path

3. **Load the specification**: Read `.sdd/{feature-dir}/spec.md`

4. **Get the plan template**:
   ```bash
   sdd template plan
   ```

5. **Research phase** — for each NEEDS CLARIFICATION in the technical context:
   - Research the unknown using available context and best practices
   - Document decisions in a `research.md` file in the feature directory
   - Resolve ALL unknowns before proceeding

6. **Fill the plan template**:
   - Technical context (language, deps, storage, testing, platform, type, goals, constraints)
   - Project structure (source layout with real paths)
   - Research findings (key decisions and rationale)
   - Data model (entities, relationships, validation rules)
   - Interface contracts (what this feature exposes to users or other systems)

7. **Write** the plan to `.sdd/{feature-dir}/plan.md`

8. **Generate supporting artifacts** (as needed):
   - `data-model.md` — if the feature involves significant data entities
   - `contracts/` — if the feature exposes public interfaces (APIs, CLI schemas, etc.)
   - `research.md` — technical decisions and alternatives considered

9. **Report completion** with paths to all generated artifacts.

## Next Steps (present after completion)

1. **Generate Task List** — run `/sdd.tasks` to break the plan into actionable tasks
2. **Attempt Direct Implementation** — proceed now with this context:
   - Feature: [feature name]
   - Tech stack: [from plan technical context]
   - Key requirements: [top FRs from spec]
   - Success criteria: [SC list]
3. **Iterate on Plan** — refine the plan further
"""

CLAUDE_TASKS_MD = """\
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

4. **Get the tasks template**:
   ```bash
   sdd template tasks
   ```

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
"""

CLAUDE_SKILL_MD = """\
---
description: "Auto-activate the sdd specification workflow when a developer requests a new feature."
---

## Activation Triggers

Activate this skill when the user's message matches patterns like:
- "build a [X] feature"
- "implement [X]"
- "create a [X]"
- "I need to add [X]"
- "add [X] to the project"

## Behavior

When triggered:

1. Recognize the user wants to build something new
2. Ask: "Would you like to start with a feature specification? Running `/sdd.specify` will create a structured spec with user stories and requirements — this usually leads to better implementations. Or I can proceed directly."
3. If the user agrees: run `/sdd.specify` with their feature description
4. If the user declines: proceed with the original request without blocking
"""

# Claude Code: map of relative paths (from .claude/) to content
CLAUDE_COMMANDS: dict[str, str] = {
    "commands/sdd.specify.md": CLAUDE_SPECIFY_MD,
    "commands/sdd.plan.md": CLAUDE_PLAN_MD,
    "commands/sdd.tasks.md": CLAUDE_TASKS_MD,
    "skills/sdd-feature-workflow/SKILL.md": CLAUDE_SKILL_MD,
}

# ---------------------------------------------------------------------------
# GitHub Copilot — .github/agents/
# ---------------------------------------------------------------------------

COPILOT_SPECIFY_MD = """\
---
description: "Create a feature specification from a natural language description."
handoffs:
  - label: Create Implementation Plan
    agent: sdd.plan
    prompt: Create a plan for this spec
    send: true
  - label: Iterate on Spec
    agent: sdd.specify
    prompt: Refine the specification
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Given the feature description in `$ARGUMENTS`, do this:

1. **Check for headless mode**: If `$ARGUMENTS` contains `headless` or `--headless`, enable headless mode — auto-accept all recommended defaults and complete without pausing for user input.

2. **Generate a feature directory name**:
   - Derive a short 2-4 word slug from the feature description (e.g., "user-auth", "analytics-dashboard")
   - Append an 8-character random alphanumeric suffix (e.g., `user-auth-a3f9b2c1`)
   - Full path: `.sdd/{slug}-{suffix}/`

3. **Create the feature directory** and all required parent directories.

4. **Get the specification template**:
   ```bash
   sdd template specification
   ```

5. **Generate the specification** by filling the template:
   - Replace `[FEATURE NAME]` with a human-readable feature name
   - Replace `[DATE]` with today's date
   - Fill in user stories (at least 2), functional requirements, and success criteria
   - Mark genuinely unclear decisions as `[NEEDS CLARIFICATION: specific question]` — maximum 3 markers

6. **Write** the filled specification to `.sdd/{feature-dir}/spec.md`.

7. **Quality validation** — validate the spec:
   - No implementation details (no languages, frameworks, APIs)
   - All mandatory sections completed
   - Requirements are testable and success criteria are measurable

8. **Handle clarifications** (skip in headless mode — auto-resolve with defaults):
   - Present at most 3 questions, wait for answers, update spec, re-validate

9. **Write quality checklist** to `.sdd/{feature-dir}/checklists/requirements.md`:
   ```bash
   sdd template specification-checklist
   ```

10. **Report completion** with feature directory path, spec file path, and checklist summary.

## Next Steps

Present these options (auto-select "Create Implementation Plan" in headless mode):

1. **Create Implementation Plan** — run `/sdd.plan`
2. **Attempt Direct Implementation** — proceed with this context:
   - Feature: [feature name]
   - Key requirements: [top 3 FRs from spec]
   - Success criteria: [SC list from spec]
3. **Iterate on Spec** — refine further

## Guidelines

- Focus on **WHAT** and **WHY** — no HOW (no tech stack, APIs, code structure)
- Every requirement must be independently testable
- Limit clarifications to decisions that genuinely impact scope or security
"""

COPILOT_PLAN_MD = """\
---
description: "Create an implementation plan from a feature specification."
handoffs:
  - label: Generate Task List
    agent: sdd.tasks
    prompt: Break the plan into actionable tasks
    send: true
  - label: Iterate on Plan
    agent: sdd.plan
    prompt: Refine the implementation plan
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Check for headless mode**: If `$ARGUMENTS` contains `headless` or `--headless`, enable headless mode.

2. **Locate the feature directory**:
   - Use path/name from `$ARGUMENTS` if provided
   - Otherwise list `.sdd/` and ask the user (or auto-select most recent in headless mode)
   - If no spec exists: offer to run `/sdd.specify` first, proceed ad-hoc, or accept a manual path

3. **Load the specification**: Read `.sdd/{feature-dir}/spec.md`

4. **Get the plan template**:
   ```bash
   sdd template plan
   ```

5. **Fill the plan template**:
   - Technical context (language, deps, storage, testing, platform, type, goals, constraints)
   - Project structure with real paths
   - Research findings (key decisions and rationale)
   - Data model and interface contracts

6. **Write** the plan to `.sdd/{feature-dir}/plan.md`

7. **Generate supporting artifacts** as needed:
   - `data-model.md`, `contracts/`, `research.md`

8. **Report completion** with paths to all generated artifacts.

## Next Steps

1. **Generate Task List** — run `/sdd.tasks`
2. **Attempt Direct Implementation** — proceed now with this context:
   - Feature: [feature name]
   - Tech stack: [from plan technical context]
   - Key requirements: [top FRs from spec]
   - Success criteria: [SC list from spec]
3. **Iterate on Plan** — refine further
"""

COPILOT_TASKS_MD = """\
---
description: "Generate an actionable, dependency-ordered task list from the feature plan."
handoffs:
  - label: Iterate on Tasks
    agent: sdd.tasks
    prompt: Refine the task list
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Check for headless mode**: If `$ARGUMENTS` contains `headless` or `--headless`, enable headless mode.

2. **Locate the feature directory**:
   - Use path/name from `$ARGUMENTS` if provided
   - Otherwise list `.sdd/` and ask the user (or auto-select most recent in headless mode)
   - If no plan exists: offer to run `/sdd.plan` first, proceed without it, or accept a manual path

3. **Load design documents** from `.sdd/{feature-dir}/`:
   - **Required**: `plan.md`, `spec.md`
   - **Optional**: `data-model.md`, `contracts/`, `research.md`

4. **Get the tasks template**:
   ```bash
   sdd template tasks
   ```

5. **Generate the task list** organized by user story. Every task must follow:
   ```
   - [ ] T### [P?] [US?] Description with exact/file/path.ext
   ```

6. **Write** tasks to `.sdd/{feature-dir}/tasks.md`

7. **Report** total task count, per-story breakdown, and suggested MVP scope.

## Next Steps

1. **Implement** — work through tasks.md in order
2. **Attempt Direct Implementation** — skip formal tasks and implement with this context:
   - Feature: [feature name]
   - Tech stack: [from plan]
   - Key requirements: [top FRs from spec]
   - Success criteria: [SC list from spec]
3. **Iterate on Tasks** — refine the task list
"""

COPILOT_SKILL_MD = """\
---
description: "Auto-activate the sdd specification workflow when a developer requests a new feature."
---

## Activation Triggers

Activate this skill when the user's message matches patterns like:
- "build a [X] feature"
- "implement [X]"
- "create a [X]"
- "I need to add [X]"
- "add [X] to the project"

## Behavior

When triggered:

1. Recognize the user wants to build something new
2. Ask: "Would you like to start with a feature specification? Running `/sdd.specify` will create a structured spec with user stories and requirements. Or I can proceed directly."
3. If the user agrees: run `/sdd.specify` with their feature description
4. If the user declines: proceed with the original request without blocking
"""

# GitHub Copilot: map of relative paths (from .github/) to content
COPILOT_COMMANDS: dict[str, str] = {
    "agents/sdd.specify.md": COPILOT_SPECIFY_MD,
    "agents/sdd.plan.md": COPILOT_PLAN_MD,
    "agents/sdd.tasks.md": COPILOT_TASKS_MD,
    "agents/sdd-feature-workflow/SKILL.md": COPILOT_SKILL_MD,
}
