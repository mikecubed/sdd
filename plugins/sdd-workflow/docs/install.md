# Install the sdd-workflow plugin

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
