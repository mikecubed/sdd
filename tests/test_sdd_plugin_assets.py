"""Tests for the shared repository-hosted plugin bundle."""

import importlib.util
import json
import tomllib
from pathlib import Path

from sdd_cli.agents import CLAUDE_SKILL_MD, COPILOT_SKILL_MD
from sdd_cli.templates import get_template


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "sdd-workflow"
PLUGIN_PROMPT_PATHS = {
    "claude-specify": PLUGIN_ROOT / "commands" / "sdd.specify.md",
    "claude-plan": PLUGIN_ROOT / "commands" / "sdd.plan.md",
    "claude-tasks": PLUGIN_ROOT / "commands" / "sdd.tasks.md",
    "copilot-specify": PLUGIN_ROOT / "agents" / "sdd.specify.md",
    "copilot-plan": PLUGIN_ROOT / "agents" / "sdd.plan.md",
    "copilot-tasks": PLUGIN_ROOT / "agents" / "sdd.tasks.md",
}
PLUGIN_PROMPT_TEMPLATE_NAMES = {
    "claude-specify": ["specification", "specification-checklist"],
    "claude-plan": ["plan"],
    "claude-tasks": ["tasks"],
    "copilot-specify": ["specification", "specification-checklist"],
    "copilot-plan": ["plan"],
    "copilot-tasks": ["tasks"],
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
    def test_plugin_prompt_assets_inline_canonical_templates(self):
        for prompt_name, path in PLUGIN_PROMPT_PATHS.items():
            content = path.read_text(encoding="utf-8")

            assert "sdd template" not in content
            assert "../templates/" not in content
            assert "templates/" not in content
            for template_name in PLUGIN_PROMPT_TEMPLATE_NAMES[prompt_name]:
                assert get_template(template_name) in content

    def test_claude_plugin_skill_matches_embedded_asset(self):
        assert (
            PLUGIN_ROOT / "skills" / "sdd-feature-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8") == CLAUDE_SKILL_MD

    def test_copilot_plugin_skill_matches_embedded_asset(self):
        assert (
            PLUGIN_ROOT / "copilot-skills" / "sdd-feature-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8") == COPILOT_SKILL_MD

    def test_plugin_bundle_no_longer_ships_template_directory(self):
        assert not (PLUGIN_ROOT / "templates").exists()

    def test_sync_helper_rewrites_prompt_assets_deterministically(self, tmp_path):
        module = _load_sync_module()
        plugin_root = tmp_path / "plugins" / "sdd-workflow"
        expected_relative_paths = [path.relative_to(PLUGIN_ROOT) for path in PLUGIN_PROMPT_PATHS.values()]

        for relative_path in expected_relative_paths:
            output_path = plugin_root / relative_path
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text("stale content\n", encoding="utf-8")

        rewritten_paths = module.sync_plugin_templates(plugin_root)

        assert [path.relative_to(plugin_root) for path in rewritten_paths] == expected_relative_paths

        for relative_path in expected_relative_paths:
            assert (plugin_root / relative_path).read_text(encoding="utf-8") == (
                PLUGIN_ROOT / relative_path
            ).read_text(encoding="utf-8")
