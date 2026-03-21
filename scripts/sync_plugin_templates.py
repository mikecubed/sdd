"""Rewrite bundled plugin template files from canonical template definitions."""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from sdd_cli.templates import get_template


PLUGIN_ROOT = REPO_ROOT / "plugins" / "sdd-workflow"
TEMPLATE_FILES: tuple[tuple[str, str], ...] = (
    ("specification", "specification.md"),
    ("specification-checklist", "specification-checklist.md"),
    ("plan", "plan.md"),
    ("tasks", "tasks.md"),
)


def sync_plugin_templates(plugin_root: Path = PLUGIN_ROOT) -> list[Path]:
    """Rewrite bundled plugin templates from canonical template content."""
    templates_dir = plugin_root / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)

    rewritten_paths: list[Path] = []
    for template_name, file_name in TEMPLATE_FILES:
        path = templates_dir / file_name
        path.write_text(get_template(template_name), encoding="utf-8")
        rewritten_paths.append(path)

    return rewritten_paths


def main() -> int:
    """Sync committed plugin templates and print the rewritten paths."""
    for path in sync_plugin_templates():
        print(path.relative_to(REPO_ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
