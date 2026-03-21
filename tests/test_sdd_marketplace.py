"""Tests for repository-hosted marketplace metadata."""

import json
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = REPO_ROOT / "pyproject.toml"
CLAUDE_MARKETPLACE = REPO_ROOT / ".claude-plugin" / "marketplace.json"
COPILOT_MARKETPLACE = REPO_ROOT / ".github" / "plugin" / "marketplace.json"


def _load_project_version() -> str:
    with PYPROJECT.open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def _load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class TestRepositoryMarketplaceFiles:
    def test_claude_marketplace_exists(self):
        assert CLAUDE_MARKETPLACE.exists()

    def test_copilot_marketplace_exists(self):
        assert COPILOT_MARKETPLACE.exists()


class TestRepositoryMarketplaceMetadata:
    def test_claude_marketplace_lists_shared_plugin_bundle(self):
        payload = _load_json(CLAUDE_MARKETPLACE)

        assert payload["name"] == "sdd-cli"
        assert payload["owner"]["name"] == "mikecubed"
        assert payload["metadata"]["version"] == _load_project_version()
        assert payload["plugins"] == [
            {
                "name": "sdd-workflow",
                "source": "./plugins/sdd-workflow",
                "description": (
                    "Spec-driven development workflow plugin for Claude Code "
                    "and GitHub Copilot CLI."
                ),
                "version": _load_project_version(),
            }
        ]
        assert (REPO_ROOT / "plugins" / "sdd-workflow").exists()

    def test_copilot_marketplace_lists_shared_plugin_bundle(self):
        payload = _load_json(COPILOT_MARKETPLACE)

        assert payload["name"] == "sdd-cli"
        assert payload["owner"]["name"] == "mikecubed"
        assert payload["metadata"]["version"] == _load_project_version()
        assert payload["plugins"] == [
            {
                "name": "sdd-workflow",
                "source": "./plugins/sdd-workflow",
                "description": (
                    "Spec-driven development workflow plugin for Claude Code "
                    "and GitHub Copilot CLI."
                ),
                "version": _load_project_version(),
            }
        ]
        assert (REPO_ROOT / "plugins" / "sdd-workflow").exists()
