# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0/). 

## [0.1.0] - 2026-03-03

### Added

- Initial release of `sdd-cli`, a lightweight Spec-Driven Development workflow tool
- `sdd init` — installs Claude Code (`.claude/commands/`) and GitHub Copilot (`.github/agents/`) slash commands in one invocation
- `sdd template` — retrieves embedded templates (specification, plan, tasks, specification-checklist) to stdout
- `sdd list` — lists feature workspaces in `.sdd/`
- Embedded specification, plan, tasks, and checklist templates (no network required)
- Agent skill files for auto-activation of spec workflow (`sdd-feature-workflow`)
- Headless mode support in all slash commands (`--headless`)
- Next-step handoffs after each command (iterate, proceed, or attempt direct implementation)
- Single runtime dependency: `click>=8.0`
- Python 3.10+ support
