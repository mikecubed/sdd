# Plugin distribution

`sdd` now supports two distribution modes for the same workflow content.

## Choose the right mode

Use direct installation when:

- you want `.claude/` and `.github/` workflow files committed directly into a project
- you want project-local customization
- you want the existing `sdd init` experience

Use the repository-hosted plugin bundle when:

- you want one shared install source across multiple repositories
- you want to install into Claude Code, GitHub Copilot CLI, or both without copying files into each target project
- you want to test locally before publishing anywhere else
- you want a self-contained plugin bundle that does not require the `sdd` binary at runtime

## Direct project install

Install the CLI and write workflow files into the target repository:

```bash
uv tool install sdd-cli --from git+https://github.com/mikecubed/sdd.git
sdd init
```

This writes:

```text
.claude/commands/
.claude/skills/
.github/agents/
.sdd/
```

## Repository-hosted marketplace install

This repository exposes marketplace metadata at:

```text
.claude-plugin/marketplace.json
.github/plugin/marketplace.json
```

and a shared plugin bundle at:

```text
plugins/sdd-workflow/
```

### Claude Code

Add the marketplace and install the plugin:

```text
/plugin marketplace add mikecubed/sdd
/plugin install sdd-workflow@sdd-cli
/reload-plugins
```

Local checkout testing:

```bash
claude --plugin-dir ./plugins/sdd-workflow
```

The bundle is self-contained at runtime. Claude loads generated prompt assets from `plugins/sdd-workflow/` with the canonical templates already inlined, so runtime execution does not require `sdd` on `PATH`.

The Claude commands are namespaced under the plugin name:

```text
/sdd-workflow:sdd.specify Add user authentication
/sdd-workflow:sdd.plan .sdd/your-feature/spec.md
/sdd-workflow:sdd.tasks .sdd/your-feature/plan.md
```

Smoke-test without `sdd` on `PATH`:

```bash
CLAUDE_BIN="$(command -v claude)"
PATH="/usr/bin:/bin" "$CLAUDE_BIN" --plugin-dir ./plugins/sdd-workflow
```

### GitHub Copilot CLI

Add the marketplace and install the plugin:

```bash
copilot plugin marketplace add mikecubed/sdd
copilot plugin install sdd-workflow@sdd-cli
```

Local checkout testing:

```bash
copilot plugin install ./plugins/sdd-workflow
```

The installed Copilot plugin is also self-contained at runtime and does not shell out to `sdd template ...` or load separate bundled template files.

After installation, verify the plugin is loaded:

```bash
copilot plugin list
```

Or in an interactive session:

```text
/plugin list
/agent
/skills list
```

To use the workflow in interactive mode, run `/agent`, choose `sdd.specify`, `sdd.plan`, or `sdd.tasks`, and then enter the prompt for that agent.

For example:

```text
/agent
# choose sdd.specify
Add user authentication
```

Smoke-test without `sdd` on `PATH`:

```bash
COPILOT_BIN="$(command -v copilot)"
PATH="/usr/bin:/bin" "$COPILOT_BIN" plugin install ./plugins/sdd-workflow
PATH="/usr/bin:/bin" "$COPILOT_BIN"
```

## Shared bundle contents

The reusable plugin bundle contains:

```text
plugins/sdd-workflow/
  .claude-plugin/plugin.json
  plugin.json
  commands/
  skills/
  copilot-skills/
  agents/
  README.md
  docs/
```

The shared bundle keeps only generated prompt assets under `commands/` and `agents/`; each prompt carries the current canonical template content inline.

## Maintainer workflow

If canonical templates or direct-install prompt sources change, regenerate the plugin prompt assets from the repository root with:

```bash
uv run python scripts/sync_plugin_templates.py
```

Validate the refresh with:

```bash
uv run --extra test python -m pytest tests/
```

## Scope note

Version 1 of the marketplace-first flow covers:

- repository-hosted marketplace metadata
- repository-hosted plugin bundle files
- local install and local validation guidance

It does not yet cover publish or release automation.
