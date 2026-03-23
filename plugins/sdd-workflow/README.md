# sdd-workflow plugin bundle

This directory is the reusable plugin bundle for the `sdd` workflow.

It is intended for:

- Claude Code plugin loading
- GitHub Copilot CLI plugin installation
- local validation before wider marketplace use

The bundle is self-contained at runtime. Claude Code and GitHub Copilot load the workflow from the files in this directory, and the generated prompt assets already include the canonical spec, plan, tasks, and checklist templates inline.

## Contents

```text
.claude-plugin/plugin.json
plugin.json
commands/
skills/
copilot-skills/
agents/
docs/
```

## Install

See `docs/install.md`.

## Validate

See `docs/testing.md`.

## Maintainer refresh workflow

When the canonical templates in `src/sdd_cli/templates.py` or the direct-install prompt sources in `src/sdd_cli/agents.py` change, regenerate the plugin prompt assets from the repository root with:

```bash
uv run python scripts/sync_plugin_templates.py
```

Then validate the bundle with:

```bash
uv run --extra test python -m pytest tests/
```
