"""Tests for sdd CLI basics: version, help, exit codes, stderr."""

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from sdd_cli.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestVersion:
    def test_version_flag(self, runner):
        """FR-025: --version flag works."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "sdd" in result.output.lower() or result.output.strip()  # version string present

    def test_short_version_flag(self, runner):
        result = runner.invoke(cli, ["-V"])
        assert result.exit_code == 0


class TestHelp:
    def test_help_flag(self, runner):
        """FR-026: --help flag works."""
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.output
        assert "template" in result.output
        assert "list" in result.output

    def test_help_does_not_show_plugin_command(self, runner):
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "\n  plugin" not in result.output

    def test_init_help(self, runner):
        result = runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0

    def test_init_help_shows_claude_flag(self, runner):
        result = runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0
        assert "--claude" in result.output

    def test_init_help_shows_copilot_flag(self, runner):
        result = runner.invoke(cli, ["init", "--help"])
        assert result.exit_code == 0
        assert "--copilot" in result.output

    def test_template_help(self, runner):
        result = runner.invoke(cli, ["template", "--help"])
        assert result.exit_code == 0

    def test_list_help(self, runner):
        result = runner.invoke(cli, ["list", "--help"])
        assert result.exit_code == 0


class TestExitCodes:
    def test_success_exit_zero_with_claude_flag(self, runner, tmp_path):
        """FR-027: exit 0 on success."""
        result = runner.invoke(cli, ["init", "--claude", str(tmp_path)])
        assert result.exit_code == 0

    def test_template_success_exit_zero(self, runner):
        result = runner.invoke(cli, ["template", "specification"])
        assert result.exit_code == 0

    def test_unknown_command_exits_nonzero(self, runner):
        result = runner.invoke(cli, ["bogus-command"])
        assert result.exit_code != 0

    def test_plugin_command_exits_nonzero(self, runner):
        result = runner.invoke(cli, ["plugin"])
        assert result.exit_code != 0


class TestNoDependencyLeaks:
    def test_only_click_imported_at_module_level(self):
        """FR-021: only click as runtime dep — no typer, rich, httpx, etc."""
        import sdd_cli.cli as cli_module
        import inspect
        source = inspect.getsource(cli_module)
        for forbidden in ("typer", "rich", "httpx", "platformdirs", "readchar", "truststore"):
            assert forbidden not in source, f"Forbidden import '{forbidden}' found in cli.py"

    def test_no_git_operations_in_init(self):
        """FR-007: no subprocess/git CLI calls in init logic."""
        import sdd_cli.init as init_module
        import inspect
        source = inspect.getsource(init_module)
        assert "subprocess" not in source
        # No git CLI invocations (e.g., "git checkout", "git branch")
        assert '"git ' not in source
        assert "'git " not in source


class TestInitFlags:
    def test_claude_flag_installs_only_claude_files(self, runner, tmp_path):
        result = runner.invoke(cli, ["init", "--claude", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "sdd.specify.md").exists()
        assert not (tmp_path / ".github").exists()

    def test_copilot_flag_installs_only_copilot_files(self, runner, tmp_path):
        result = runner.invoke(cli, ["init", "--copilot", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".github" / "agents" / "sdd.specify.md").exists()
        assert not (tmp_path / ".claude").exists()

    def test_both_flags_installs_both(self, runner, tmp_path):
        result = runner.invoke(cli, ["init", "--claude", "--copilot", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "sdd.specify.md").exists()
        assert (tmp_path / ".github" / "agents" / "sdd.specify.md").exists()

    def test_both_flags_no_detection_output(self, runner, tmp_path):
        result = runner.invoke(cli, ["init", "--claude", "--copilot", str(tmp_path)])
        assert result.exit_code == 0
        assert "found in PATH" not in result.output
        assert "not found in PATH" not in result.output


class TestInitDetectionFlow:
    def test_default_installs_claude_when_detected(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=True), \
             patch("sdd_cli.cli.detect_copilot", return_value=False):
            result = runner.invoke(cli, ["init", str(tmp_path)], input="n\n")
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "sdd.specify.md").exists()
        assert "\u2713 claude found" in result.output

    def test_default_skips_claude_when_not_detected(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=False), \
             patch("sdd_cli.cli.detect_copilot", return_value=False):
            result = runner.invoke(cli, ["init", str(tmp_path)], input="n\n")
        assert result.exit_code != 0
        assert "\u2717 claude not found" in result.output

    def test_default_installs_copilot_when_detected(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=False), \
             patch("sdd_cli.cli.detect_copilot", return_value=True):
            result = runner.invoke(cli, ["init", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".github" / "agents" / "sdd.specify.md").exists()
        assert "\u2713 copilot found" in result.output

    def test_default_prompts_for_copilot_when_not_detected(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=True), \
             patch("sdd_cli.cli.detect_copilot", return_value=False):
            result = runner.invoke(cli, ["init", str(tmp_path)], input="y\n")
        assert result.exit_code == 0
        assert (tmp_path / ".github" / "agents" / "sdd.specify.md").exists()

    def test_nothing_to_install_exits_nonzero(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=False), \
             patch("sdd_cli.cli.detect_copilot", return_value=False):
            result = runner.invoke(cli, ["init", str(tmp_path)], input="n\n")
        assert result.exit_code != 0
        assert "Nothing to install" in result.output

    def test_nothing_to_install_shows_flag_hints(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=False), \
             patch("sdd_cli.cli.detect_copilot", return_value=False):
            result = runner.invoke(cli, ["init", str(tmp_path)], input="n\n")
        assert "--claude" in result.output
        assert "--copilot" in result.output

    def test_both_detected_no_prompt_shown(self, runner, tmp_path):
        with patch("sdd_cli.cli.detect_claude", return_value=True), \
             patch("sdd_cli.cli.detect_copilot", return_value=True):
            result = runner.invoke(cli, ["init", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / ".claude" / "commands" / "sdd.specify.md").exists()
        assert (tmp_path / ".github" / "agents" / "sdd.specify.md").exists()
        assert "install GitHub Copilot agents anyway" not in result.output
