"""Tests for the shared repository-hosted plugin bundle."""

import json
import tomllib
from pathlib import Path

from sdd_cli.agents import (
    CLAUDE_PLAN_MD,
    CLAUDE_SKILL_MD,
    CLAUDE_SPECIFY_MD,
    CLAUDE_TASKS_MD,
    COPILOT_PLAN_MD,
    COPILOT_SKILL_MD,
    COPILOT_SPECIFY_MD,
    COPILOT_TASKS_MD,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "sdd-workflow"


def _load_project_version() -> str:
    with (REPO_ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


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
    def test_claude_plugin_assets_match_embedded_assets(self):
        assert (PLUGIN_ROOT / "commands" / "sdd.specify.md").read_text(encoding="utf-8") == CLAUDE_SPECIFY_MD
        assert (PLUGIN_ROOT / "commands" / "sdd.plan.md").read_text(encoding="utf-8") == CLAUDE_PLAN_MD
        assert (PLUGIN_ROOT / "commands" / "sdd.tasks.md").read_text(encoding="utf-8") == CLAUDE_TASKS_MD
        assert (
            PLUGIN_ROOT / "skills" / "sdd-feature-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8") == CLAUDE_SKILL_MD

    def test_copilot_plugin_assets_match_embedded_assets(self):
        assert (PLUGIN_ROOT / "agents" / "sdd.specify.md").read_text(encoding="utf-8") == COPILOT_SPECIFY_MD
        assert (PLUGIN_ROOT / "agents" / "sdd.plan.md").read_text(encoding="utf-8") == COPILOT_PLAN_MD
        assert (PLUGIN_ROOT / "agents" / "sdd.tasks.md").read_text(encoding="utf-8") == COPILOT_TASKS_MD
        assert (
            PLUGIN_ROOT / "copilot-skills" / "sdd-feature-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8") == COPILOT_SKILL_MD
