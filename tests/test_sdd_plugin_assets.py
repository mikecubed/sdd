"""Tests for the shared repository-hosted plugin bundle."""

import importlib.util
import json
import tomllib
from pathlib import Path

from sdd_cli.agents import CLAUDE_SKILL_MD, COPILOT_SKILL_MD
from sdd_cli.templates import get_template


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "sdd-workflow"
PLUGIN_TEMPLATE_PATHS = {
    "specification": PLUGIN_ROOT / "templates" / "specification.md",
    "specification-checklist": PLUGIN_ROOT / "templates" / "specification-checklist.md",
    "plan": PLUGIN_ROOT / "templates" / "plan.md",
    "tasks": PLUGIN_ROOT / "templates" / "tasks.md",
}
PLUGIN_PROMPT_PATHS = {
    "claude-specify": PLUGIN_ROOT / "commands" / "sdd.specify.md",
    "claude-plan": PLUGIN_ROOT / "commands" / "sdd.plan.md",
    "claude-tasks": PLUGIN_ROOT / "commands" / "sdd.tasks.md",
    "copilot-specify": PLUGIN_ROOT / "agents" / "sdd.specify.md",
    "copilot-plan": PLUGIN_ROOT / "agents" / "sdd.plan.md",
    "copilot-tasks": PLUGIN_ROOT / "agents" / "sdd.tasks.md",
}
PLUGIN_PROMPT_TEMPLATE_REFS = {
    "claude-specify": [
        "templates/specification.md",
        "templates/specification-checklist.md",
    ],
    "claude-plan": ["templates/plan.md"],
    "claude-tasks": ["templates/tasks.md"],
    "copilot-specify": [
        "templates/specification.md",
        "templates/specification-checklist.md",
    ],
    "copilot-plan": ["templates/plan.md"],
    "copilot-tasks": ["templates/tasks.md"],
}


def _load_project_version() -> str:
    with (REPO_ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _load_sync_module():
    spec = importlib.util.spec_from_file_location(
        "sync_plugin_templates",
        REPO_ROOT / "scripts" / "sync_plugin_templates.py",
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestSharedPluginBundle:
    def test_shared_plugin_root_exists(self):
        assert PLUGIN_ROOT.exists()

    def test_claude_plugin_manifest_exists(self):
        assert (PLUGIN_ROOT / ".claude-plugin" / "plugin.json").exists()

    def test_copilot_plugin_manifest_exists(self):
        assert (PLUGIN_ROOT / "plugin.json").exists()

    def test_claude_plugin_manifest_metadata(self):
        payload = _load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")

        assert payload == {
            "name": "sdd-workflow",
            "description": "Spec-driven development workflow plugin for Claude Code.",
            "version": _load_project_version(),
            "author": {"name": "mikecubed"},
        }

    def test_copilot_plugin_manifest_metadata(self):
        payload = _load_json(PLUGIN_ROOT / "plugin.json")

        assert payload == {
            "name": "sdd-workflow",
            "description": "Spec-driven development workflow plugin for GitHub Copilot CLI.",
            "version": _load_project_version(),
            "author": {"name": "mikecubed"},
            "agents": "agents/",
            "skills": ["copilot-skills/"],
        }


class TestSharedPluginContent:
    def test_plugin_prompt_assets_use_bundled_templates(self):
        for prompt_name, path in PLUGIN_PROMPT_PATHS.items():
            content = path.read_text(encoding="utf-8")

            assert "sdd template" not in content
            for template_reference in PLUGIN_PROMPT_TEMPLATE_REFS[prompt_name]:
                assert template_reference in content

    def test_claude_plugin_skill_matches_embedded_asset(self):
        assert (
            PLUGIN_ROOT / "skills" / "sdd-feature-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8") == CLAUDE_SKILL_MD

    def test_copilot_plugin_skill_matches_embedded_asset(self):
        assert (
            PLUGIN_ROOT / "copilot-skills" / "sdd-feature-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8") == COPILOT_SKILL_MD

    def test_bundled_template_files_exist(self):
        for path in PLUGIN_TEMPLATE_PATHS.values():
            assert path.exists()

    def test_bundled_template_files_match_canonical_templates(self):
        for template_name, path in PLUGIN_TEMPLATE_PATHS.items():
            assert path.read_text(encoding="utf-8") == get_template(template_name)

    def test_sync_helper_rewrites_templates_deterministically(self, tmp_path):
        module = _load_sync_module()
        plugin_root = tmp_path / "plugins" / "sdd-workflow"
        templates_dir = plugin_root / "templates"
        templates_dir.mkdir(parents=True)

        for path in PLUGIN_TEMPLATE_PATHS.values():
            (templates_dir / path.name).write_text("stale content\n", encoding="utf-8")

        rewritten_paths = module.sync_plugin_templates(plugin_root)

        assert [path.name for path in rewritten_paths] == [path.name for path in PLUGIN_TEMPLATE_PATHS.values()]

        for template_name, path in PLUGIN_TEMPLATE_PATHS.items():
            assert (templates_dir / path.name).read_text(encoding="utf-8") == get_template(template_name)
