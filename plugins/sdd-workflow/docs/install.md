# Install the sdd-workflow plugin

The plugin bundle is self-contained at runtime. After installation, Claude Code and GitHub Copilot read generated workflow prompts from `plugins/sdd-workflow/`; those prompt assets carry the canonical templates inline, so they do not invoke `sdd template ...` or require the `sdd` binary on `PATH`.

## Claude Code

From a local checkout:

```bash
claude --plugin-dir ./plugins/sdd-workflow
```

After Claude starts, reload plugins if needed:

```text
/reload-plugins
```

Then invoke the workflow with namespaced commands such as:

```text
/sdd-workflow:sdd.specify Add user authentication
```

From the repository marketplace:

```text
/plugin marketplace add mikecubed/sdd
/plugin install sdd-workflow@sdd-cli
```

Smoke-test the self-contained bundle with `sdd` absent from `PATH`:

```bash
CLAUDE_BIN="$(command -v claude)"
PATH="/usr/bin:/bin" "$CLAUDE_BIN" --plugin-dir ./plugins/sdd-workflow
```

Then run:

```text
/sdd-workflow:sdd.specify Add user authentication
```

and confirm the workflow opens the inlined canonical specification template content without any dependency on a local `sdd` executable.

## GitHub Copilot CLI

From a local checkout:

```bash
copilot plugin install ./plugins/sdd-workflow
```

From the repository marketplace:

```bash
copilot plugin marketplace add mikecubed/sdd
copilot plugin install sdd-workflow@sdd-cli
```

After installation, verify availability with:

```bash
copilot plugin list
```

In interactive mode, run `/agent`, choose `sdd.specify`, `sdd.plan`, or `sdd.tasks`, and then enter your prompt.

Smoke-test the self-contained bundle with `sdd` absent from `PATH`:

```bash
COPILOT_BIN="$(command -v copilot)"
PATH="/usr/bin:/bin" "$COPILOT_BIN" plugin install ./plugins/sdd-workflow
PATH="/usr/bin:/bin" "$COPILOT_BIN"
```

Then use `/agent` to run `sdd.specify`, `sdd.plan`, or `sdd.tasks` and confirm the plugin operates from bundled files only.
