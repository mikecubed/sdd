"""Click CLI application for sdd-cli."""

from pathlib import Path

import click

from .detect import detect_claude, detect_copilot
from .init import init_project, print_results
from .templates import get_template, list_templates

# Injected by hatchling at build time; fallback for editable installs.
try:
    from importlib.metadata import PackageNotFoundError, version as _meta_version
except ImportError:
    _VERSION = "0.0.0"
else:
    try:
        _VERSION = _meta_version("sdd-cli")
    except PackageNotFoundError:
        _VERSION = "0.0.0"


@click.group()
@click.version_option(_VERSION, "--version", "-V", prog_name="sdd")
def cli() -> None:
    """sdd — Spec-Driven Development workflow tool."""


@cli.command()
@click.argument("directory", default=".", type=click.Path(file_okay=False))
@click.option("--claude", "force_claude", is_flag=True,
              help="Install Claude Code files (skips detection).")
@click.option("--copilot", "force_copilot", is_flag=True,
              help="Install GitHub Copilot files (skips prompts).")
def init(directory: str, force_claude: bool, force_copilot: bool) -> None:
    """Initialize sdd in a project directory.

    Installs agent command files and creates the .sdd/ workspace directory.
    Safe to re-run — existing files are updated in place.

    By default, detects installed agents automatically. Use --claude or
    --copilot to install specific agents without detection or prompts.

    DIRECTORY defaults to the current directory.
    """
    project_dir = Path(directory).resolve()

    click.echo(f"\nInitializing sdd in {project_dir}\n")

    if force_claude or force_copilot:
        platforms: set[str] = set()
        if force_claude:
            platforms.add("claude")
        if force_copilot:
            platforms.add("copilot")
    else:
        platforms = set()

        if detect_claude():
            click.echo("  \u2713 claude found \u2014 installing Claude Code commands")
            platforms.add("claude")
        else:
            click.echo("  \u2717 claude not found in PATH \u2014 skipping Claude Code files")
            click.echo("    (use --claude to install anyway)")

        if detect_copilot():
            click.echo("  \u2713 copilot found \u2014 installing GitHub Copilot agents")
            platforms.add("copilot")
        elif click.confirm(
            "\n  copilot not found in PATH \u2014 install GitHub Copilot agents anyway?",
            default=False,
        ):
            platforms.add("copilot")

    if not platforms:
        click.echo("\nNothing to install. No supported agents were detected or selected.")
        click.echo("\nTo install manually, specify which agents to configure:")
        click.echo("  sdd init --claude          Claude Code commands")
        click.echo("  sdd init --copilot         GitHub Copilot agents")
        click.echo("  sdd init --claude --copilot  Both")
        raise SystemExit(1)

    click.echo()
    successes, failures = init_project(project_dir, platforms)
    print_results(successes, failures, project_dir)

    if failures:
        raise click.ClickException(
            f"{len(successes)} file(s) written, {len(failures)} error(s). See stderr for details."
        )

    click.echo(f"\n{len(successes)} file(s) written successfully.")
    click.echo("\nNext steps:")
    click.echo("  • In Claude Code:    /sdd.specify <your feature description>")
    click.echo("  • In GitHub Copilot: @workspace /sdd.specify <your feature description>")


@cli.command()
@click.argument("name", required=False)
@click.option("--list", "-l", "list_all", is_flag=True, help="List all available templates.")
def template(name: str | None, list_all: bool) -> None:
    """Print a template to stdout.

    NAME is the template name (e.g., specification, plan, tasks).
    Use --list to show all available templates.
    """
    if list_all or name is None:
        click.echo("Available templates:\n")
        for tname, description in list_templates():
            click.echo(f"  {tname:<28}  {description}")
        return

    try:
        content = get_template(name)
    except KeyError:
        available = ", ".join(n for n, _ in list_templates())
        raise click.UsageError(
            f"Unknown template '{name}'. Available: {available}. "
            "Run 'sdd template --list' to see all available templates."
        )

    click.echo(content, nl=False)


@cli.command("list")
@click.argument("directory", default=".", type=click.Path(file_okay=False))
def list_features(directory: str) -> None:
    """List feature workspaces in the .sdd/ directory.

    DIRECTORY defaults to the current directory.
    """
    sdd_dir = Path(directory).resolve() / ".sdd"

    if not sdd_dir.exists():
        click.echo("No .sdd/ workspace found. Run `sdd init` first.")
        return

    features = sorted(
        [d for d in sdd_dir.iterdir() if d.is_dir()],
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )

    if not features:
        click.echo("No feature workspaces found in .sdd/")
        return

    click.echo(f"Feature workspaces in {sdd_dir}:\n")
    for feat in features:
        spec_exists = (feat / "spec.md").exists()
        plan_exists = (feat / "plan.md").exists()
        tasks_exists = (feat / "tasks.md").exists()

        artifacts = []
        if spec_exists:
            artifacts.append("spec")
        if plan_exists:
            artifacts.append("plan")
        if tasks_exists:
            artifacts.append("tasks")

        status = ", ".join(artifacts) if artifacts else "empty"
        click.echo(f"  {feat.name:<40}  [{status}]")


def main() -> None:
    """Entry point for the sdd CLI."""
    cli()
