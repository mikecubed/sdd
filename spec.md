# Feature Specification: Fork Spec-Kit to Less-Opinionated Architecture

**Created**: 2026-03-03
**Status**: Draft
**Input**: User description: "Fork spec-kit and refactor it to follow a less-opinionated architecture: remove constitution management, cross-artifact analysis, implementation orchestration, and multi-agent adapter system. Replace the monolithic CLI with a modular source layout, embed templates as Python string constants instead of downloading from GitHub, eliminate shell script dependencies, decouple from git branching workflows, reduce runtime dependencies to just click, and support only Claude Code and GitHub Copilot as agents. Preserve the core specify/plan/tasks workflow and template content."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install and Initialize a Project (Priority: P1)

A developer installs the new tool and runs the `init` command in their project directory. The tool creates a workspace directory and installs slash command files for both supported agents (Claude Code and GitHub Copilot) without requiring any network access, git operations, or shell script execution. The developer immediately has specify, plan, and tasks slash commands available in their preferred AI agent, whether that's Claude Code in the terminal, GitHub Copilot in VS Code, or GitHub Copilot CLI in the terminal.

**Why this priority**: Without a working install-and-init flow, no other functionality is usable. This is the entry point for every user.

**Independent Test**: Can be tested by installing the package, running the init command in an empty directory, and verifying that the workspace directory, `.claude/commands/`, and `.github/agents/` all contain the expected files.

**Acceptance Scenarios**:

1. **Given** a Python 3.12+ environment with the tool installed, **When** a developer runs the init command in any directory, **Then** the tool creates a workspace directory and installs command files for Claude Code (`.claude/commands/`) and GitHub Copilot (`.github/agents/`) without making any network requests or running any shell scripts.
2. **Given** a project directory with no git repository, **When** the developer runs the init command, **Then** initialization succeeds without errors because the tool does not depend on git.
3. **Given** a project where the init command was previously run, **When** the developer runs it again, **Then** existing files are updated in place and status messages indicate "Updated" for each file.
4. **Given** a project directory with existing `.github/workflows/` or `.claude/settings/` content, **When** the developer runs the init command, **Then** only the agent command subdirectories are created or modified; all other content is left untouched.
5. **Given** the init command encounters a permission error writing to one agent directory (e.g., `.github/agents/`), **When** other agent directories are writable, **Then** the tool writes the files it can, reports the specific failure to stderr, and exits with a non-zero exit code.

---

### User Story 2 - Create a Feature Specification (Priority: P1)

A developer uses the specify slash command in their AI agent to describe a feature in natural language. The agent retrieves the specification template via the CLI's template command, fills it with structured requirements, user stories, and success criteria, and writes the result to the workspace feature directory. The workflow guides the developer through clarification questions if needed, then validates the spec against a quality checklist. Upon completion, the developer is offered next steps: iterate on the spec, proceed to planning, or attempt direct implementation.

**Why this priority**: Specification is the foundation of the entire workflow. Without it, planning and task generation have no input.

**Independent Test**: Can be tested by invoking the specify command with a feature description and verifying that `spec.md` and `requirements.md` are created in the feature directory with all mandatory sections filled and no unresolved `[NEEDS CLARIFICATION]` markers.

**Acceptance Scenarios**:

1. **Given** a project with the tool initialized, **When** a developer invokes the specify command with "Build a user login page," **Then** the agent creates a feature directory in the workspace containing `spec.md` with user stories, functional requirements, and success criteria derived from the description.
2. **Given** a generated specification, **When** the agent runs quality validation, **Then** a `requirements.md` checklist is created alongside the spec with pass/fail status for each quality criterion.
3. **Given** a specification with ambiguities, **When** the agent identifies unclear aspects, **Then** at most 3 clarification questions are presented to the user with suggested options before the spec is finalized.
4. **Given** a successful specification, **When** the agent presents next steps, **Then** the developer can choose to iterate on the spec, create an implementation plan, or attempt direct implementation.
5. **Given** the developer chooses "attempt to implement," **When** the agent dispatches implementation, **Then** it provides a structured context summary (feature summary, key requirements, success criteria) so the agent can proceed without a formal plan or task list.
6. **Given** the specify command is invoked with a "headless" flag or keyword, **When** the workflow encounters decision points or clarification needs, **Then** the agent auto-accepts recommended defaults and completes the entire workflow without pausing for user input.

---

### User Story 3 - Create an Implementation Plan (Priority: P1)

A developer uses the plan slash command after creating a specification. The agent retrieves the plan template, reads the existing spec and project context, and produces a `plan.md` with technical context, research findings, data models, and contracts. The plan is written to the same feature directory as the spec. Upon completion, the developer is offered next steps: iterate on the plan, generate tasks, or attempt direct implementation.

**Why this priority**: Planning bridges the gap between what to build (spec) and how to build it (tasks). Without it, task generation lacks technical grounding.

**Independent Test**: Can be tested by creating a spec first, then invoking the plan command and verifying that `plan.md` (and optionally `research.md`, `data-model.md`, `contracts/`) are created in the feature directory.

**Acceptance Scenarios**:

1. **Given** a feature directory containing `spec.md`, **When** a developer invokes the plan command, **Then** the agent creates `plan.md` in the same directory with technical context, research findings, and design artifacts.
2. **Given** no specification exists in conversation history, **When** a developer invokes the plan command, **Then** the agent offers three options: generate a new spec, plan without a spec (ad-hoc), or provide a spec location manually.
3. **Given** a completed plan, **When** the agent presents next steps, **Then** the developer can choose to iterate on the plan, generate tasks, or attempt immediate implementation.
4. **Given** the developer chooses "attempt to implement" from the plan, **When** the agent dispatches implementation, **Then** it provides a structured context summary from both the spec and plan so the agent can proceed without a formal task list.
5. **Given** the plan command is invoked with a "headless" flag, **When** the workflow encounters decision points, **Then** the agent auto-accepts defaults and completes the workflow without pausing.

---

### User Story 4 - Generate an Actionable Task List (Priority: P2)

A developer uses the tasks slash command after creating a specification and plan. The agent retrieves the tasks template, reads the existing spec and plan, and produces a `tasks.md` with dependency-ordered, checklist-formatted tasks organized by user story. Upon completion, the developer is offered next steps: iterate on the tasks or attempt implementation.

**Why this priority**: Task generation is the final pre-implementation step. It depends on both spec and plan being complete, making it naturally lower priority than those foundational capabilities.

**Independent Test**: Can be tested by having spec.md and plan.md in a feature directory, invoking the tasks command, and verifying that `tasks.md` is created with properly formatted task items organized by user story phases.

**Acceptance Scenarios**:

1. **Given** a feature directory containing `spec.md` and `plan.md`, **When** a developer invokes the tasks command, **Then** the agent creates `tasks.md` with tasks organized by user story in priority order, each task having a checkbox, task ID, and file path.
2. **Given** a specification exists but no plan, **When** a developer invokes the tasks command, **Then** the agent offers to generate a plan first or provide a plan location manually.
3. **Given** a generated task list, **When** inspecting `tasks.md`, **Then** every task follows the format `- [ ] [TaskID] [optional markers] Description with file path`.
4. **Given** the tasks command is invoked with a "headless" flag, **When** the workflow encounters decision points, **Then** the agent auto-accepts defaults and completes the workflow without pausing.

---

### User Story 5 - Retrieve Templates Independently (Priority: P2)

A developer uses the CLI's template command from the command line to retrieve any template (specification, plan, tasks, specification-checklist) as plain text on stdout. This enables scripting, piping, and inspection without launching an AI agent.

**Why this priority**: Template retrieval is a supporting capability. It enables the slash commands to work and gives developers direct access, but it is not the primary workflow.

**Independent Test**: Can be tested by running the template command with "specification" and verifying valid Markdown template content is printed to stdout, and running with `--list` shows all available templates.

**Acceptance Scenarios**:

1. **Given** the tool is installed, **When** a developer runs the template command with "specification," **Then** the specification template Markdown is printed to stdout.
2. **Given** the tool is installed, **When** a developer runs the template command with `--list`, **Then** all available templates are listed with their names and descriptions.
3. **Given** an invalid template name, **When** a developer runs the template command with "nonexistent," **Then** an error message is printed to stderr listing available templates and the process exits with a non-zero code.

---

### User Story 6 - Automatic Feature Workflow Activation (Priority: P3)

When a developer asks their AI agent to "implement a new feature" or "build X" without explicitly invoking a slash command, the agent's feature-workflow skill auto-activates and offers to run the specification workflow first. This prevents developers from skipping the structured process.

**Why this priority**: This is a convenience enhancement. Developers can always manually invoke the specify command. The skill just makes discovery easier.

**Independent Test**: Can be tested by verifying that skill definition files exist in the correct agent-specific directories after initialization and contain appropriate activation triggers.

**Acceptance Scenarios**:

1. **Given** a project with the tool initialized, **When** a developer asks the AI agent "build a dashboard feature" without invoking a slash command, **Then** the feature-workflow skill activates and asks if the developer wants to create a specification first.
2. **Given** the skill has activated, **When** the developer declines the specification workflow, **Then** the agent proceeds with the original request without blocking.

---

### User Story 7 - List Feature Workspaces (Priority: P3)

A developer returning to a project wants to find existing feature specifications. Since feature directories use random suffixes, the developer needs a way to discover what features exist in the workspace.

**Why this priority**: This is a convenience for returning developers. The workspace directory can always be browsed manually with filesystem tools, but a built-in list command provides a better experience.

**Independent Test**: Can be tested by creating multiple features, then running the list command and verifying all feature directories are shown with their names.

**Acceptance Scenarios**:

1. **Given** a workspace with multiple feature directories, **When** a developer runs a list or status command, **Then** the tool displays all feature directories with their short names.
2. **Given** an empty workspace with no features, **When** a developer runs the list command, **Then** the tool displays a message indicating no features exist.

---

### Edge Cases

- What happens when a developer has spec-kit and the new tool both initialized in the same project? The tools use different directory structures (`.specify/` vs the new workspace dir) and different command prefixes (`/speckit.*` vs the new prefix), so they coexist without conflict.
- What happens when the init command is run with no write permissions to the current directory? The tool reports the error to stderr and exits with a non-zero exit code.
- What happens when the init command can write to `.claude/` but not `.github/`? The tool writes the files it can, reports the specific failure to stderr, and exits with a non-zero exit code (partial success is still an error).
- What happens when a developer runs the template command with no arguments? The tool displays the list of available templates (same as `--list`).
- What happens when a spec-kit user migrates? Existing `.specify/` artifacts are not touched. The developer must manually reference old specs if they want to continue iterating on them.
- What happens when a developer uses Copilot CLI (`copilot` binary) vs Copilot in VS Code? Both read from the same `.github/agents/` directory, so the same command files work in both environments without any special handling.

## Requirements *(mandatory)*

### Functional Requirements

#### Removal Requirements (from spec-kit)

- **FR-001**: System MUST NOT include a constitution management command or workflow. Project principles are managed manually by the developer.
- **FR-002**: System MUST NOT include a standalone clarify command. Clarification is handled inline within the specify workflow's validation loop.
- **FR-003**: System MUST NOT include an analyze command for cross-artifact consistency checking.
- **FR-004**: System MUST NOT include a formal implement command for orchestrated task execution. Instead, each command MUST offer an "attempt to implement" option that dispatches the agent with a structured context summary.
- **FR-005**: System MUST NOT include a standalone checklist command. Quality checklists are embedded in the specify workflow.
- **FR-006**: System MUST NOT depend on shell scripts (bash or PowerShell) at runtime. All functionality MUST be implemented in Python.
- **FR-007**: System MUST NOT require git for any functionality. Git branching, feature numbering, and branch detection MUST be removed.
- **FR-008**: System MUST NOT make network requests during initialization or template retrieval. All templates MUST be embedded in the package.
- **FR-009**: System MUST NOT include agent adapters beyond Claude Code and GitHub Copilot. GitHub Copilot support covers both VS Code and Copilot CLI (the `copilot` binary), which share the same `.github/agents/` directory.

#### Preservation Requirements (from spec-kit)

- **FR-010**: System MUST preserve the core three-command workflow: specify, plan, and tasks.
- **FR-011**: System MUST preserve the structural sections of the specification template (user stories with priorities, functional requirements, success criteria). The baseline is the current forked template content, not spec-kit's raw templates.
- **FR-012**: System MUST preserve the structural sections of the plan template (technical context, research phases, design phases). The baseline is the current forked template content.
- **FR-013**: System MUST preserve the structural sections of the tasks template (dependency-ordered, checklist-formatted, organized by user story). The baseline is the current forked template content.
- **FR-014**: System MUST support a template CLI command for retrieving templates to stdout.

#### Workflow Behavior Requirements

- **FR-015**: Each slash command (specify, plan, tasks) MUST present next-step options upon successful completion: iterate on the current artifact, proceed to the next command in the workflow, or attempt direct implementation.
- **FR-016**: The "attempt to implement" option MUST provide the agent with a structured context summary (feature summary, key requirements from the spec, success criteria) so the agent can proceed without requiring the full specify → plan → tasks pipeline.
- **FR-017**: Each slash command MUST support a headless mode (triggered by "headless" or "--headless" in the user input) that auto-accepts all recommended defaults, skips user confirmation prompts, and completes the workflow without interruption.
- **FR-018**: When a prerequisite artifact is missing (e.g., plan command invoked with no spec), the command MUST offer graceful fallback options: generate the missing artifact, proceed without it (ad-hoc), or accept a manual file path.

#### Architecture Requirements

- **FR-019**: System MUST use a modular source layout with separate Python files for CLI entry point, initialization logic, template registry, and agent command content.
- **FR-020**: System MUST store all templates and command content as embedded Python string constants, not as external files.
- **FR-021**: System MUST have exactly one runtime dependency: click (version 8.0 or higher).
- **FR-022**: System MUST support Python 3.12 or higher.
- **FR-023**: System MUST use hatchling as the build backend.
- **FR-024**: System MUST store feature artifacts in a workspace directory using random alphanumeric suffixes instead of sequential numbered directories.

#### CLI Requirements

- **FR-025**: The CLI MUST support a `--version` flag that displays the current version.
- **FR-026**: The CLI MUST support a `--help` flag that displays usage information for all commands.
- **FR-027**: The CLI MUST exit with code 0 on success and a non-zero code on any error.
- **FR-028**: All error messages MUST be written to stderr, not stdout.

#### Agent Support Requirements

- **FR-029**: System MUST install Claude Code command files to `.claude/commands/` using dot-separated names (e.g., `{prefix}.specify.md`, `{prefix}.plan.md`, `{prefix}.tasks.md`).
- **FR-030**: System MUST install Claude Code skill files to `.claude/skills/{tool}-feature-workflow/SKILL.md`.
- **FR-031**: System MUST install GitHub Copilot command files to `.github/agents/` using dot-separated names (e.g., `{prefix}.specify.md`, `{prefix}.plan.md`, `{prefix}.tasks.md`). These files serve both Copilot in VS Code and Copilot CLI.
- **FR-032**: System MUST install GitHub Copilot skill files to `.github/agents/{tool}-feature-workflow/SKILL.md`.
- **FR-033**: The init command MUST install files for both agents (Claude Code and GitHub Copilot) in a single invocation without requiring the user to select an agent.

### Key Entities

- **Feature Workspace**: A directory within the tool's workspace named with a feature name and random suffix that contains all artifacts for a single feature (spec.md, plan.md, tasks.md, research.md, etc.).
- **Agent Command**: A Markdown file with YAML frontmatter installed into an agent-specific directory that defines a slash command for that agent.
- **Agent Skill**: A directory containing a skill definition file that enables auto-activation of the specification workflow when a developer requests a new feature.
- **Template**: A Markdown document structure stored as a Python string constant, retrievable via the CLI template command, that defines the format for specifications, plans, or task lists.
- **Next-Step Handoff**: A structured prompt presented after each command completes, offering the developer choices to iterate, proceed to the next workflow stage, or attempt direct implementation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A developer can go from zero to a working installation in under 2 minutes using a single install command.
- **SC-002**: The init command completes in under 1 second because it performs no network requests, no git operations, and no shell script execution.
- **SC-003**: The complete specify → plan → tasks workflow produces the same quality of output artifacts (user stories, requirements, plans, tasks) as spec-kit's workflow.
- **SC-004**: The tool has exactly 1 runtime dependency, compared to spec-kit's 8+ runtime dependencies.
- **SC-005**: The tool installs command files for both supported agents in a single init invocation, compared to spec-kit requiring agent selection.
- **SC-006**: A developer using either supported agent (Claude Code or GitHub Copilot, including Copilot CLI) can complete a full specify → plan → tasks cycle without encountering references to unsupported agents or spec-kit-specific concepts (`.specify/`, `/speckit.*`, constitution, etc.).
- **SC-007**: The source codebase uses a modular layout where logic is distributed across focused, single-responsibility modules rather than concentrated in monolithic files.

## Assumptions

- The current forked template content (already derived from spec-kit with improvements like headless mode, inline clarification, and next-step handoffs) is the baseline for preservation requirements, not spec-kit's raw templates.
- GitHub Copilot reads agent command files from `.github/agents/` using YAML frontmatter + Markdown body format. Both Copilot in VS Code and Copilot CLI (the `copilot` binary) share this same directory and file format — they are the same agent platform on different surfaces.
- The `$ARGUMENTS` placeholder mechanism works identically in Claude Code and GitHub Copilot.
- Developers who need constitution management, cross-artifact analysis, or implementation orchestration will continue to use spec-kit directly. This tool intentionally does not replace those capabilities.
- The random alphanumeric suffix for feature directories provides sufficient uniqueness for single-developer and small-team workflows without requiring git-based sequential numbering.
- The tool name, CLI command name, slash command prefix, and workspace directory name are implementation decisions to be determined during planning. This spec uses generic terms (e.g., "the tool," "the init command," "the workspace directory") to avoid prescribing a name.
