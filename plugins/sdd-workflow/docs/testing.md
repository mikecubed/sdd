# Test the sdd-workflow plugin locally

## Claude Code

1. Start Claude with the local plugin bundle:

   ```bash
   claude --plugin-dir ./plugins/sdd-workflow
   ```

2. Reload plugins if you edit the bundle while Claude is running:

   ```text
   /reload-plugins
   ```

3. Verify the workflow is available by running a namespaced command:

   ```text
   /sdd-workflow:sdd.specify Add user authentication
   ```

## GitHub Copilot CLI

1. Install the local bundle:

   ```bash
   copilot plugin install ./plugins/sdd-workflow
   ```

2. Confirm the plugin is installed:

   ```bash
   copilot plugin list
   ```

3. In an interactive session, confirm the bundled capabilities are loaded:

   ```text
   /plugin list
   /agent
   /skills list
   ```

4. Use `/agent`, select `sdd.specify`, and enter a prompt such as `Add user authentication`.

5. If you edit the local plugin, reinstall it to refresh Copilot CLI's cached copy:

   ```bash
   copilot plugin install ./plugins/sdd-workflow
   ```
