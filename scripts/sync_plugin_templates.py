"""Regenerate repository-hosted plugin prompt assets from canonical sources."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sdd_cli.agents import (  # noqa: E402
    CLAUDE_PLAN_MD,
    CLAUDE_SPECIFY_MD,
    CLAUDE_TASKS_MD,
    COPILOT_PLAN_MD,
    COPILOT_SPECIFY_MD,
    COPILOT_TASKS_MD,
)
from sdd_cli.templates import get_template  # noqa: E402


PLUGIN_ROOT = REPO_ROOT / "plugins" / "sdd-workflow"


def _replace_once(content: str, old: str, new: str) -> str:
    count = content.count(old)
    if count == 0:
        raise ValueError(f"Expected prompt snippet not found:\n{old}")
    if count > 1:
        raise ValueError(
            f"Expected prompt snippet to appear exactly once, but found {count} occurrences:\n{old}"
        )
    return content.replace(old, new, 1)


def _inline_template(name: str) -> str:
    return f"````md\n{get_template(name).rstrip('\n')}\n````"


def _build_claude_specify() -> str:
    content = _replace_once(
        CLAUDE_SPECIFY_MD,
        """4. **Get the specification template**:
   ```bash
   sdd template specification
   ```""",
        f"""4. **Use the canonical specification template embedded below**:
   {_inline_template("specification")}""",
    )
    return _replace_once(
        content,
        """9. **Write quality checklist** to `.sdd/{feature-dir}/checklists/requirements.md`:
   ```bash
   sdd template specification-checklist
   ```
   Fill it with pass/fail status based on the validation above.""",
        f"""9. **Write quality checklist** to `.sdd/{{feature-dir}}/checklists/requirements.md` using the embedded template below:
   {_inline_template("specification-checklist")}
   Fill it with pass/fail status based on the validation above.""",
    )


def _build_copilot_specify() -> str:
    content = _replace_once(
        COPILOT_SPECIFY_MD,
        """4. **Get the specification template**:
   ```bash
   sdd template specification
   ```""",
        f"""4. **Use the canonical specification template embedded below**:
   {_inline_template("specification")}""",
    )
    return _replace_once(
        content,
        """9. **Write quality checklist** to `.sdd/{feature-dir}/checklists/requirements.md`:
   ```bash
   sdd template specification-checklist
   ```""",
        f"""9. **Write quality checklist** to `.sdd/{{feature-dir}}/checklists/requirements.md` using the embedded template below:
   {_inline_template("specification-checklist")}""",
    )


def _build_claude_plan() -> str:
    return _replace_once(
        CLAUDE_PLAN_MD,
        """4. **Get the plan template**:
   ```bash
   sdd template plan
   ```""",
        f"""4. **Use the canonical plan template embedded below**:
   {_inline_template("plan")}""",
    )


def _build_copilot_plan() -> str:
    return _replace_once(
        COPILOT_PLAN_MD,
        """4. **Get the plan template**:
   ```bash
   sdd template plan
   ```""",
        f"""4. **Use the canonical plan template embedded below**:
   {_inline_template("plan")}""",
    )


def _build_claude_tasks() -> str:
    return _replace_once(
        CLAUDE_TASKS_MD,
        """4. **Get the tasks template**:
   ```bash
   sdd template tasks
   ```""",
        f"""4. **Use the canonical tasks template embedded below**:
   {_inline_template("tasks")}""",
    )


def _build_copilot_tasks() -> str:
    return _replace_once(
        COPILOT_TASKS_MD,
        """4. **Get the tasks template**:
   ```bash
   sdd template tasks
   ```""",
        f"""4. **Use the canonical tasks template embedded below**:
   {_inline_template("tasks")}""",
    )


PROMPT_ASSETS: tuple[tuple[Path, Callable[[], str]], ...] = (
    (Path("commands/sdd.specify.md"), _build_claude_specify),
    (Path("commands/sdd.plan.md"), _build_claude_plan),
    (Path("commands/sdd.tasks.md"), _build_claude_tasks),
    (Path("agents/sdd.specify.md"), _build_copilot_specify),
    (Path("agents/sdd.plan.md"), _build_copilot_plan),
    (Path("agents/sdd.tasks.md"), _build_copilot_tasks),
)


def sync_plugin_templates(plugin_root: Path = PLUGIN_ROOT) -> list[Path]:
    """Rewrite plugin prompt assets with inline canonical templates."""
    templates_dir = plugin_root / "templates"
    if templates_dir.exists():
        shutil.rmtree(templates_dir)

    rewritten_paths: list[Path] = []
    for relative_path, builder in PROMPT_ASSETS:
        output_path = plugin_root / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(builder(), encoding="utf-8")
        rewritten_paths.append(output_path)

    return rewritten_paths


def main() -> int:
    """Sync committed plugin prompt assets and print the rewritten paths."""
    for path in sync_plugin_templates():
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
