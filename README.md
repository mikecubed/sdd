# sdd — Spec-Driven Development

A lightweight CLI tool that installs the spec-driven development workflow into your project for **Claude Code** and **GitHub Copilot**. Forked from spec-kit.

## What it does

`sdd` supports two installation paths:

- `sdd init` installs project-local workflow files directly into a repository.
- This repository also ships a reusable marketplace/plugin bundle under `plugins/sdd-workflow/` for Claude Code and GitHub Copilot CLI.

`sdd init` installs three slash commands into your project:

| Command | What it does |
|---|---|
| `/sdd.specify` | Create a feature specification with user stories and requirements |
| `/sdd.plan` | Create an implementation plan from the specification |
| `/sdd.tasks` | Generate a dependency-ordered task list from the plan |

Files are installed for both **Claude Code** (`.claude/commands/`) and **GitHub Copilot** (`.github/agents/`) in a single command — no agent selection needed.

## Install

```bash
uv tool install sdd-cli --from git+https://github.com/mikecubed/sdd.git
```

Or in a project venv:
```bash
pip install sdd-cli
```

## Quick start

```bash
# Direct install into a project
sdd init

# In Claude Code:
/sdd.specify Add user authentication

# In GitHub Copilot (VS Code or CLI):
@workspace /sdd.specify Add user authentication
```

## Plugin and marketplace install

Use the repository-hosted plugin bundle when you want the workflow available across multiple projects without writing `.claude/` or `.github/` files into each repo.

### Claude Code

Add this repository as a marketplace:

```text
/plugin marketplace add mikecubed/sdd
/plugin install sdd-workflow@sdd-cli
/reload-plugins
```

For local testing from a checkout:

```bash
claude --plugin-dir ./plugins/sdd-workflow
```

Then try:

```text
/sdd-workflow:sdd.specify Add user authentication
```

### GitHub Copilot CLI

Add this repository as a marketplace:

```bash
copilot plugin marketplace add mikecubed/sdd
copilot plugin install sdd-workflow@sdd-cli
```

For local testing from a checkout:

```bash
copilot plugin install ./plugins/sdd-workflow
```

Then verify the bundled workflow is available with:

```text
/plugin list
/agent
/skills list
```

Then select `sdd.specify`, `sdd.plan`, or `sdd.tasks` from `/agent` and enter your prompt.

See `docs/plugin-distribution.md` for the full direct-vs-plugin guidance and local validation steps.

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

## Repository-hosted plugin layout

This repository can also act as a plugin marketplace source:

```text
.claude-plugin/marketplace.json
.github/plugin/marketplace.json
plugins/
  sdd-workflow/
    .claude-plugin/plugin.json
    plugin.json
    commands/
    skills/
    copilot-skills/
    agents/
```

Use direct installation when the workflow should live inside a specific repository. Use the plugin bundle when you want one reusable install source for Claude Code, GitHub Copilot CLI, or both.

## Design principles

- **1 runtime dependency**: `click` only
- **No network calls**: all templates embedded in the package
- **No git required**: works in any directory, no branch detection
- **No shell scripts**: pure Python
- **2 supported agents**: Claude Code + GitHub Copilot (covers both VS Code and Copilot CLI)
- **Python 3.12+**

## License

MIT
