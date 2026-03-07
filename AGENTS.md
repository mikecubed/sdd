# AGENTS.md

## About sdd-cli

**sdd-cli** (`sdd`) is a lightweight Spec-Driven Development (SDD) tool that installs a three-command workflow into your project for **Claude Code** and **GitHub Copilot**.

The tool creates slash command files that guide an AI agent through a structured specify → plan → tasks workflow before implementation.

---

## General Practices

- Any changes to `src/sdd_cli/` require a version bump in `pyproject.toml` and a new entry in `CHANGELOG.md`.
- All templates are embedded as Python string constants in `src/sdd_cli/templates.py` — no external template files.
- Agent command content is embedded in `src/sdd_cli/agents.py`.

## Source Layout

```
src/sdd_cli/
  __init__.py    # exposes main()
  cli.py         # click app: init, template, list commands
  init.py        # file-writing logic (no git, no network)
  templates.py   # embedded Python string constants: spec, plan, tasks, checklist
  agents.py      # embedded Claude Code + GitHub Copilot command/skill content
```

## Supported Agents

| Agent | Directory | Format |
|---|---|---|
| **Claude Code** | `.claude/commands/` | Markdown |
| **GitHub Copilot** | `.github/agents/` | Markdown |

Both agents use `$ARGUMENTS` as the placeholder for user input and the same Markdown+YAML frontmatter format.

## Slash Commands

| Command | File (both agents) | What it does |
|---|---|---|
| `/sdd.specify` | `sdd.specify.md` | Create feature spec from natural language |
| `/sdd.plan` | `sdd.plan.md` | Create implementation plan from spec |
| `/sdd.tasks` | `sdd.tasks.md` | Generate dependency-ordered task list |

Skills (auto-activation):
- Claude Code: `.claude/skills/sdd-feature-workflow/SKILL.md`
- GitHub Copilot: `.github/agents/sdd-feature-workflow/SKILL.md`

## CLI Commands

```bash
sdd init [DIRECTORY]        # Install command files for both agents + create .sdd/
sdd template <name>         # Print a template to stdout
sdd template --list         # List all available templates
sdd list [DIRECTORY]        # List feature workspaces in .sdd/
sdd --version               # Show version
sdd --help                  # Show help
```

## Feature Workspace

Feature artifacts are stored in `.sdd/{slug}-{random8}/`:

```
.sdd/
  user-auth-a3f9b2c1/
    spec.md
    plan.md
    tasks.md
    research.md        (optional)
    data-model.md      (optional)
    contracts/         (optional)
    checklists/
      requirements.md
```

## Development

### Setup

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[test]"
```

### Run tests

```bash
python -m pytest tests/
```

### Install globally

```bash
uv tool install .
# or after changes:
uv tool install --force .
```

### Key constraints

- **No network calls** — templates are embedded, `sdd init` writes only local files
- **No git operations** — works in any directory without a git repo
- **No shell scripts** — pure Python
- **Exit 0 on success, non-zero on any error**
- **All errors → stderr**
- `sdd init` installs both agents without prompting

## Adding or Modifying Templates

Edit `src/sdd_cli/templates.py`. Templates are plain Python string constants — no special build step required.

## Modifying Agent Commands

Edit `src/sdd_cli/agents.py`. After changes, re-run `sdd init` in any project to update installed files.

The `$ARGUMENTS` placeholder is passed through as-is to both Claude Code and GitHub Copilot.
