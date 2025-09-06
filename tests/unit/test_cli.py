"""Unit tests for CLI module."""

from click.testing import CliRunner

from easydeploy.cli.main import main


class TestCLI:
    """Test CLI functionality."""

    def test_help_command(self):
        """Test that help command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "easyDeploy" in result.output
        assert "deploy" in result.output

    def test_version_command(self):
        """Test that version command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert "0.1.0" in result.output

    def test_deploy_command_help(self):
        """Test deploy command help."""
        runner = CliRunner()
        result = runner.invoke(main, ["deploy", "--help"])

        assert result.exit_code == 0
        assert "Deploy a new robotics development environment" in result.output

    def test_list_command(self):
        """Test list command."""
        runner = CliRunner()
        result = runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "Active deployments" in result.output
