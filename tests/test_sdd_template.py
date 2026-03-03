"""Tests for sdd template command."""

import pytest
from click.testing import CliRunner

from sdd_cli.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


class TestTemplateOutput:
    def test_specification_template_printed_to_stdout(self, runner):
        result = runner.invoke(cli, ["template", "specification"])
        assert result.exit_code == 0
        assert "Feature Specification" in result.output
        assert "User Scenarios" in result.output
        assert "Requirements" in result.output
        assert "Success Criteria" in result.output

    def test_plan_template_printed_to_stdout(self, runner):
        result = runner.invoke(cli, ["template", "plan"])
        assert result.exit_code == 0
        assert "Implementation Plan" in result.output
        assert "Technical Context" in result.output

    def test_tasks_template_printed_to_stdout(self, runner):
        result = runner.invoke(cli, ["template", "tasks"])
        assert result.exit_code == 0
        assert "Tasks:" in result.output
        assert "- [ ]" in result.output

    def test_specification_checklist_template(self, runner):
        result = runner.invoke(cli, ["template", "specification-checklist"])
        assert result.exit_code == 0
        assert "Checklist" in result.output


class TestTemplateList:
    def test_list_flag_shows_all_templates(self, runner):
        result = runner.invoke(cli, ["template", "--list"])
        assert result.exit_code == 0
        assert "specification" in result.output
        assert "plan" in result.output
        assert "tasks" in result.output
        assert "specification-checklist" in result.output

    def test_no_args_shows_list(self, runner):
        """FR-014: template with no args shows list."""
        result = runner.invoke(cli, ["template"])
        assert result.exit_code == 0
        assert "specification" in result.output

    def test_short_flag_works(self, runner):
        result = runner.invoke(cli, ["template", "-l"])
        assert result.exit_code == 0
        assert "specification" in result.output


class TestTemplateInvalidName:
    def test_invalid_name_exits_nonzero(self, runner):
        """FR-027: non-zero exit on error."""
        result = runner.invoke(cli, ["template", "nonexistent"])
        assert result.exit_code != 0

    def test_invalid_name_lists_available_in_output(self, runner):
        result = runner.invoke(cli, ["template", "nonexistent"])
        # Error message should mention available templates
        assert "specification" in result.output or "specification" in (result.exception or "")
