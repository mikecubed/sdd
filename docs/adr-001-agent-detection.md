# ADR-001: Agent Detection & Selection for `sdd init`

**Status:** Accepted
**Date:** 2026-03-10

---

## Problem

`sdd init` previously wrote all agent config files for both Claude Code and GitHub Copilot
unconditionally, regardless of whether the user had either tool installed. This caused two
problems:

1. **Noise** — Claude-only projects received `.github/agents/` files they'd never use, and
   vice versa.
2. **No control** — users in CI or scripted environments had no way to limit installation to
   specific platforms.

---

## Decision

Make `sdd init` smart by default, with explicit override flags for scripting:

- **Claude Code**: detected via `shutil.which("claude")`. Binary presence is authoritative —
  if found, install silently; if not found, skip silently. No prompt needed.
- **GitHub Copilot**: no reliable CLI binary exists (Copilot is typically a VS Code extension).
  Detection via `shutil.which("copilot")` runs first; if not found, fall back to a
  `click.confirm()` prompt since the user may still want the files.
- **Explicit flags** (`--claude`, `--copilot`): bypass detection and prompts entirely, for
  scripting and CI reproducibility.

---

## Behaviour Matrix

| Invocation                      | Claude files        | Copilot files              |
|---------------------------------|---------------------|----------------------------|
| `sdd init`                      | if `claude` in PATH | if `copilot` in PATH, else prompt |
| `sdd init --claude`             | always              | never                      |
| `sdd init --copilot`            | never               | always                     |
| `sdd init --claude --copilot`   | always              | always                     |
| `sdd init` (nothing detected, prompt=no) | — | — → exit 1          |

---

## Rationale

### Why binary detection for Claude?

The `claude` CLI is installed as a standalone binary that ends up in PATH. Its presence is a
reliable signal that the user is actively using Claude Code. No prompt is needed — install
silently, skip silently.

### Why prompt for Copilot?

GitHub Copilot has no canonical CLI binary. It is primarily delivered as a VS Code extension,
a JetBrains plugin, or through `gh copilot` (a `gh` extension, not a top-level `copilot`
binary). Relying on `shutil.which("copilot")` alone would miss the majority of Copilot users.
The prompt lets users opt in even when no binary is found.

### Why explicit flags?

CI pipelines and developer bootstrap scripts need deterministic, non-interactive behaviour.
`--claude` and `--copilot` bypass all detection and prompts, making the install fully
scriptable.

### Non-TTY / piped behaviour

When stdin is not a TTY and no explicit flags are given:
- Binary detection runs for both agents.
- The Copilot `click.confirm()` defaults to `False` (click's non-TTY behaviour).
- If neither binary is found, the command exits with code 1 and prints usage hints.

---

## Alternatives Considered

| Alternative | Rejected because |
|---|---|
| Keep unconditional install | Creates noise; no user control |
| Prompt for both agents | Unnecessary friction for Claude; binary is authoritative |
| Interactive TUI selection | Over-engineered; flags cover the CI use case more cleanly |
| `--no-claude` / `--no-copilot` negation flags | Awkward UX; positive flags are clearer |

---

## Consequences

- **Breaking change**: `sdd init` without flags no longer installs everything unconditionally.
  Users who relied on the old behaviour should use `sdd init --claude --copilot`.
- Detection is isolated in `sdd_cli/detect.py` for easy extension (e.g., Cursor, Windsurf)
  and easy mocking in tests.
- The `init_project()` function now accepts a `platforms` parameter, keeping the core write
  logic independent of detection.
