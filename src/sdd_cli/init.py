"""Initialization logic: write agent command and skill files to a project directory."""

from pathlib import Path
from typing import Literal

import click

from .agents import CLAUDE_COMMANDS, COPILOT_COMMANDS

Status = Literal["created", "updated"]


def _write_file(path: Path, content: str) -> Status:
    """Write content to path, creating parent dirs as needed. Return status."""
    path.parent.mkdir(parents=True, exist_ok=True)
    status: Status = "updated" if path.exists() else "created"
    path.write_text(content, encoding="utf-8")
    return status


def init_project(
    project_dir: Path,
    platforms: set[str] | None = None,
) -> tuple[list[tuple[Path, Status]], list[tuple[Path, str]]]:
    """
    Write agent command and skill files into project_dir.

    Args:
        project_dir: The project root directory.
        platforms: Set of platform keys to install (``"claude"``, ``"copilot"``).
                   Pass ``None`` to install all platforms.

    Returns:
        (successes, failures) where:
          successes = list of (path, status) for files written successfully
          failures  = list of (path, error_message) for files that could not be written
    """
    successes: list[tuple[Path, Status]] = []
    failures: list[tuple[Path, str]] = []

    all_platforms = {
        "claude":  (project_dir / ".claude",  CLAUDE_COMMANDS),
        "copilot": (project_dir / ".github",   COPILOT_COMMANDS),
    }
    valid_keys = set(all_platforms)
    if platforms is not None:
        unknown = platforms - valid_keys
        if unknown:
            unknown_list = ", ".join(sorted(unknown))
            valid_list = ", ".join(sorted(valid_keys))
            raise ValueError(
                f"Unknown platform key(s): {unknown_list}. "
                f"Valid platforms are: {valid_list}."
            )
    selected = platforms if platforms is not None else valid_keys
    agent_dirs = {base: cmds for k, (base, cmds) in all_platforms.items() if k in selected}

    for base_dir, commands in agent_dirs.items():
        for rel_path, content in commands.items():
            target = base_dir / rel_path
            try:
                status = _write_file(target, content)
                successes.append((target, status))
            except OSError as exc:
                failures.append((target, str(exc)))

    # Create the .sdd/ workspace directory (no files, just the dir)
    sdd_dir = project_dir / ".sdd"
    try:
        sdd_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        failures.append((sdd_dir, str(exc)))

    return successes, failures


def print_results(
    successes: list[tuple[Path, Status]],
    failures: list[tuple[Path, str]],
    project_dir: Path,
) -> None:
    """Print init results to stdout (successes) and stderr (failures)."""
    for path, status in successes:
        rel = path.relative_to(project_dir)
        label = "Created" if status == "created" else "Updated"
        click.echo(f"  {label}: {rel}")

    for path, error in failures:
        try:
            rel = str(path.relative_to(project_dir))
        except ValueError:
            rel = str(path)
        click.echo(f"  Error: {rel}: {error}", err=True)
