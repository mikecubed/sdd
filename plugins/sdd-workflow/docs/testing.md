# Test the sdd-workflow plugin locally

The plugin should be validated as a self-contained bundle. Runtime workflow execution must succeed even when the `sdd` binary is not available on `PATH`.

## Automated validation

Run the focused plugin asset test:

```bash
uv run --extra test python -m pytest tests/test_sdd_plugin_assets.py
```

For the broader maintainer validation path, run the full test suite:

```bash
uv run --extra test python -m pytest tests/
```

If canonical templates in `src/sdd_cli/templates.py` or direct-install prompt sources in `src/sdd_cli/agents.py` changed, regenerate the plugin prompt assets first:

```bash
uv run python scripts/sync_plugin_templates.py
```

## Claude Code

1. Start Claude with the local plugin bundle:

   ```bash
   CLAUDE_BIN="$(command -v claude)"
   PATH="/usr/bin:/bin" "$CLAUDE_BIN" --plugin-dir ./plugins/sdd-workflow
   ```

2. Reload plugins if you edit the bundle while Claude is running:

   ```text
   /reload-plugins
   ```

3. Verify the workflow is available by running a namespaced command:

   ```text
   /sdd-workflow:sdd.specify Add user authentication
   ```

4. Confirm the workflow renders the inlined canonical template content successfully even though `sdd` is absent from `PATH`.

## GitHub Copilot CLI

1. Install the local bundle:

   ```bash
   COPILOT_BIN="$(command -v copilot)"
   PATH="/usr/bin:/bin" "$COPILOT_BIN" plugin install ./plugins/sdd-workflow
   ```

2. Confirm the plugin is installed:

   ```bash
   PATH="/usr/bin:/bin" "$COPILOT_BIN" plugin list
   ```

3. In an interactive session, confirm the bundled capabilities are loaded:

   ```text
   /plugin list
   /agent
   /skills list
   ```

4. Use `/agent`, select `sdd.specify`, and enter a prompt such as `Add user authentication`.

5. Confirm the selected workflow runs successfully with `sdd` absent from `PATH`, proving the installed plugin uses the inlined canonical templates directly.

6. If you edit the local plugin, reinstall it to refresh Copilot CLI's cached copy:

   ```bash
   "$COPILOT_BIN" plugin install ./plugins/sdd-workflow
   ```
