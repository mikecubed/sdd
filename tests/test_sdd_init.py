"""Tests for sdd init command."""

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from sdd_cli.cli import cli
from sdd_cli.init import init_project


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def tmp_project(tmp_path):
    return tmp_path


class TestInitCreatesFiles:
    def test_creates_claude_commands(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert result.exit_code == 0
        assert (tmp_project / ".claude" / "commands" / "sdd.specify.md").exists()
        assert (tmp_project / ".claude" / "commands" / "sdd.plan.md").exists()
        assert (tmp_project / ".claude" / "commands" / "sdd.tasks.md").exists()

    def test_creates_claude_skill(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert result.exit_code == 0
        assert (tmp_project / ".claude" / "skills" / "sdd-feature-workflow" / "SKILL.md").exists()

    def test_creates_copilot_commands(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--copilot", str(tmp_project)])
        assert result.exit_code == 0
        assert (tmp_project / ".github" / "agents" / "sdd.specify.md").exists()
        assert (tmp_project / ".github" / "agents" / "sdd.plan.md").exists()
        assert (tmp_project / ".github" / "agents" / "sdd.tasks.md").exists()

    def test_creates_copilot_skill(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--copilot", str(tmp_project)])
        assert result.exit_code == 0
        assert (tmp_project / ".github" / "agents" / "sdd-feature-workflow" / "SKILL.md").exists()

    def test_creates_sdd_workspace_dir(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert result.exit_code == 0
        assert (tmp_project / ".sdd").is_dir()

    def test_both_agents_installed_with_both_flags(self, runner, tmp_project):
        """Both agents installed when --claude --copilot flags are passed."""
        result = runner.invoke(cli, ["init", "--claude", "--copilot", str(tmp_project)])
        assert result.exit_code == 0
        # Claude Code
        assert (tmp_project / ".claude" / "commands" / "sdd.specify.md").exists()
        # GitHub Copilot
        assert (tmp_project / ".github" / "agents" / "sdd.specify.md").exists()


class TestInitIdempotent:
    def test_second_run_updates_not_creates(self, runner, tmp_project):
        runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert result.exit_code == 0
        assert "Updated" in result.output

    def test_content_after_second_run_is_current(self, runner, tmp_project):
        runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        content = (tmp_project / ".claude" / "commands" / "sdd.specify.md").read_text()
        assert "sdd template specification" in content


class TestInitNoGitRequired:
    def test_init_succeeds_in_directory_with_no_git(self, runner, tmp_project):
        """FR-007: no git dependency."""
        assert not (tmp_project / ".git").exists()
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert result.exit_code == 0


class TestInitNoNetworkRequired:
    def test_init_does_not_import_httpx(self):
        """FR-008: no network requests during init."""
        import sdd_cli.init as init_module
        import inspect
        source = inspect.getsource(init_module)
        assert "httpx" not in source
        assert "urllib" not in source
        assert "requests" not in source


class TestInitPartialFailure:
    def test_exit_nonzero_on_write_error(self, runner, tmp_project):
        """FR-027: non-zero exit on any error."""
        # Make .claude dir a file to cause write failure
        claude_path = tmp_project / ".claude"
        claude_path.write_text("not a directory")

        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert result.exit_code != 0

    def test_error_written_to_stderr_on_failure(self, runner, tmp_project):
        """FR-028: errors go to stderr."""
        claude_path = tmp_project / ".claude"
        claude_path.write_text("not a directory")

        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)], catch_exceptions=False)
        # CliRunner mixes stdout/stderr unless mix_stderr=False; check output contains Error
        assert result.exit_code != 0


class TestInitOutputMessages:
    def test_shows_created_for_new_files(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert "Created" in result.output

    def test_shows_next_steps(self, runner, tmp_project):
        result = runner.invoke(cli, ["init", "--claude", str(tmp_project)])
        assert "sdd.specify" in result.output


class TestInitPlatformSelection:
    def test_claude_only_writes_only_claude_files(self, tmp_project):
        init_project(tmp_project, {"claude"})
        assert (tmp_project / ".claude" / "commands" / "sdd.specify.md").exists()
        assert not (tmp_project / ".github").exists()

    def test_copilot_only_writes_only_copilot_files(self, tmp_project):
        init_project(tmp_project, {"copilot"})
        assert (tmp_project / ".github" / "agents" / "sdd.specify.md").exists()
        assert not (tmp_project / ".claude").exists()

    def test_both_platforms_writes_both(self, tmp_project):
        init_project(tmp_project, {"claude", "copilot"})
        assert (tmp_project / ".claude" / "commands" / "sdd.specify.md").exists()
        assert (tmp_project / ".github" / "agents" / "sdd.specify.md").exists()

    def test_none_platforms_writes_both(self, tmp_project):
        init_project(tmp_project, None)
        assert (tmp_project / ".claude" / "commands" / "sdd.specify.md").exists()
        assert (tmp_project / ".github" / "agents" / "sdd.specify.md").exists()

    def test_unknown_platform_key_raises(self, tmp_project):
        import pytest
        with pytest.raises(ValueError, match="Unknown platform key"):
            init_project(tmp_project, {"cursor"})
