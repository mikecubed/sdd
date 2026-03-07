"""Tests for sdd list command."""

import pytest
from click.testing import CliRunner

from sdd_cli.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tmp_project(tmp_path):
    return tmp_path


class TestListFeatures:
    def test_shows_feature_dirs(self, runner, tmp_project):
        runner.invoke(cli, ["init", str(tmp_project)])
        # Create a fake feature directory with spec.md
        feat_dir = tmp_project / ".sdd" / "my-feature-abc12345"
        feat_dir.mkdir()
        (feat_dir / "spec.md").write_text("# spec")

        result = runner.invoke(cli, ["list", str(tmp_project)])
        assert result.exit_code == 0
        assert "my-feature-abc12345" in result.output

    def test_shows_artifact_status(self, runner, tmp_project):
        runner.invoke(cli, ["init", str(tmp_project)])
        feat_dir = tmp_project / ".sdd" / "test-feature-aabbccdd"
        feat_dir.mkdir()
        (feat_dir / "spec.md").write_text("# spec")
        (feat_dir / "plan.md").write_text("# plan")

        result = runner.invoke(cli, ["list", str(tmp_project)])
        assert result.exit_code == 0
        assert "spec" in result.output
        assert "plan" in result.output

    def test_multiple_features_shown(self, runner, tmp_project):
        runner.invoke(cli, ["init", str(tmp_project)])
        for name in ("feature-one-aaaabbbb", "feature-two-ccccdddd"):
            feat = tmp_project / ".sdd" / name
            feat.mkdir()

        result = runner.invoke(cli, ["list", str(tmp_project)])
        assert result.exit_code == 0
        assert "feature-one" in result.output
        assert "feature-two" in result.output


class TestListEmpty:
    def test_empty_workspace_shows_message(self, runner, tmp_project):
        runner.invoke(cli, ["init", str(tmp_project)])
        result = runner.invoke(cli, ["list", str(tmp_project)])
        assert result.exit_code == 0
        assert "No feature" in result.output or "empty" in result.output.lower()

    def test_no_sdd_dir_shows_message(self, runner, tmp_project):
        result = runner.invoke(cli, ["list", str(tmp_project)])
        assert result.exit_code == 0
        assert ".sdd" in result.output or "init" in result.output.lower()
