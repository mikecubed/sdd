# sdd — Spec-Driven Development

A lightweight CLI tool that installs the spec-driven development workflow into your project for **Claude Code** and **GitHub Copilot**.  Forked from spec-kit.

## What it does

`sdd init` installs three slash commands into your project:

| Command | What it does |
|---|---|
| `/sdd.specify` | Create a feature specification with user stories and requirements |
| `/sdd.plan` | Create an implementation plan from the specification |
| `/sdd.tasks` | Generate a dependency-ordered task list from the plan |

Files are installed for both **Claude Code** (`.claude/commands/`) and **GitHub Copilot** (`.github/agents/`) in a single command — no agent selection needed.

## Install

```bash
uv tool install sdd-cli --from git+https://github.com/mikecubed/spec-kit.git
```

Or in a project venv:
```bash
pip install sdd-cli
```

## Quick start

```bash
# Initialize sdd in your project
sdd init

# In Claude Code:
/sdd.specify Add user authentication

# In GitHub Copilot (VS Code or CLI):
@workspace /sdd.specify Add user authentication
```

## Commands

### `sdd init [DIRECTORY]`

Installs agent command files and creates the `.sdd/` workspace directory. Safe to re-run — existing files are updated in place.

```
.claude/commands/
  sdd.specify.md
  sdd.plan.md
  sdd.tasks.md
  skills/sdd-feature-workflow/SKILL.md

.github/agents/
  sdd.specify.md
  sdd.plan.md
  sdd.tasks.md
  sdd-feature-workflow/SKILL.md

.sdd/   ← feature workspace directory
```

### `sdd template [NAME]`

Print a template to stdout. Useful for scripting or inspection.

```bash
sdd template specification        # spec template
sdd template plan                 # plan template
sdd template tasks                # tasks template
sdd template specification-checklist
sdd template --list               # list all templates
```

### `sdd list [DIRECTORY]`

List feature workspaces in `.sdd/`.

```bash
sdd list
# Feature workspaces in .sdd/:
#   user-auth-a3f9b2c1        [spec, plan, tasks]
#   analytics-dashboard-ff00ab12  [spec]
```

## Workflow

Feature artifacts are stored in `.sdd/{feature-name}-{random8}/`:

```
.sdd/
  user-auth-a3f9b2c1/
    spec.md
    plan.md
    tasks.md
    research.md          (optional, from /sdd.plan)
    data-model.md        (optional, from /sdd.plan)
    contracts/           (optional, from /sdd.plan)
    checklists/
      requirements.md    (from /sdd.specify)
```

Each command offers **next-step handoffs** on completion — iterate, proceed to the next command, or attempt direct implementation. Every command also supports **headless mode** (add `headless` to your message) to auto-accept defaults without prompts.

## Design principles

- **1 runtime dependency**: `click` only
- **No network calls**: all templates embedded in the package
- **No git required**: works in any directory, no branch detection
- **No shell scripts**: pure Python
- **2 supported agents**: Claude Code + GitHub Copilot (covers both VS Code and Copilot CLI)
- **Python 3.12+**

## License

MIT
