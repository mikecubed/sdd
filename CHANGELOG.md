# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0/).

## [0.2.0] - 2026-03-21

### Added

- Repository-hosted marketplace metadata for Claude Code and GitHub Copilot CLI
- Shared `plugins/sdd-workflow/` bundle for reusable plugin installation across both agents
- A maintainer sync script to regenerate repository-hosted plugin prompt assets from canonical sources
- Self-contained plugin prompt assets with canonical spec, plan, tasks, and checklist templates inlined at sync time

### Changed

- Repository-hosted plugin workflows no longer depend on the `sdd` binary at runtime for template retrieval
- Repository and bundle docs now cover direct install vs marketplace/plugin install, sync, validation, and smoke testing
- `.sdd/` workspaces are no longer gitignored by default so they remain visible for `@` file selection

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
- Python 3.12+ support
