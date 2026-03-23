"""Tests for the shared repository-hosted plugin bundle."""

import importlib.util
import json
import tomllib
from pathlib import Path

import pytest


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
PLUGIN_SKILL_PATHS = {
    "claude-skill": PLUGIN_ROOT / "skills" / "sdd-feature-workflow" / "SKILL.md",
    "copilot-skill": PLUGIN_ROOT / "copilot-skills" / "sdd-feature-workflow" / "SKILL.md",
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


def _expected_embedded_template(prompt_name: str, template_name: str) -> str:
    module = _load_sync_module()
    embedded = module._inline_template(template_name)
    replacements = (
        module.CLAUDE_PLUGIN_REPLACEMENTS
        if prompt_name.startswith("claude-")
        else module.COPILOT_PLUGIN_REPLACEMENTS
    )
    return module._replace_all(embedded, replacements)


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
                assert _expected_embedded_template(prompt_name, template_name) in content

    def test_plugin_bundle_uses_plugin_specific_command_references(self):
        for path in [*PLUGIN_PROMPT_PATHS.values(), *PLUGIN_SKILL_PATHS.values()]:
            content = path.read_text(encoding="utf-8")

            assert "/sdd.specify" not in content
            assert "/sdd.plan" not in content
            assert "/sdd.tasks" not in content

        claude_content = (PLUGIN_ROOT / "commands" / "sdd.specify.md").read_text(encoding="utf-8")
        assert "/sdd-workflow:sdd.plan" in claude_content

        copilot_content = (PLUGIN_ROOT / "agents" / "sdd.specify.md").read_text(encoding="utf-8")
        assert "/agent`, choose `sdd.plan`" in copilot_content

    def test_claude_specify_prompt_renders_checklist_followup_as_list_text(self):
        expected_line = "   Fill it with pass/fail status based on the validation above."
        content = (PLUGIN_ROOT / "commands" / "sdd.specify.md").read_text(encoding="utf-8")

        assert expected_line in content
        assert f"\n    Fill it with pass/fail status based on the validation above." not in content

    def test_plugin_bundle_no_longer_ships_template_directory(self):
        assert not (PLUGIN_ROOT / "templates").exists()

    def test_sync_helper_rewrites_prompt_assets_deterministically(self, tmp_path):
        module = _load_sync_module()
        plugin_root = tmp_path / "plugins" / "sdd-workflow"
        expected_relative_paths = [
            relative_path
            for relative_path, _builder in module.PROMPT_ASSETS
        ]

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

    def test_replace_once_rejects_multiple_matches(self):
        module = _load_sync_module()

        with pytest.raises(ValueError, match="appear exactly once"):
            module._replace_once("x target y target z", "target", "replacement")

    def test_inline_template_only_strips_trailing_newlines(self, monkeypatch):
        module = _load_sync_module()
        monkeypatch.setattr(module, "get_template", lambda _: "line with break  \n\n")

        assert module._inline_template("specification") == "````md\nline with break  \n````"
