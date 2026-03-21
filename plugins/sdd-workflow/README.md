# sdd-workflow plugin bundle

This directory is the reusable plugin bundle for the `sdd` workflow.

It is intended for:

- Claude Code plugin loading
- GitHub Copilot CLI plugin installation
- local validation before wider marketplace use

The bundle is self-contained for runtime template access. Claude Code and GitHub Copilot load the workflow from the files in this directory, so the installed plugin does not need the `sdd` binary on `PATH` to read spec, plan, or task templates.

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

The bundled template payload lives under `templates/` and is referenced directly by the Claude and Copilot prompt assets.

## Install

See `docs/install.md`.

## Validate

See `docs/testing.md`.

## Maintainer refresh workflow

When the canonical templates in `src/sdd_cli/templates.py` change, refresh the bundled plugin copies from the repository root with:

```bash
uv run python scripts/sync_plugin_templates.py
```

Then validate the bundle with:

```bash
uv run --extra test python -m pytest tests/
```
