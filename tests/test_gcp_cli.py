"""Tests for GCP CLI commands."""

from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from easydeploy.cli.gcp import login, logout, require_gcp_auth, status


class TestGCPCLI:
    """Test cases for GCP CLI commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    @patch("easydeploy.cli.gcp.is_authenticated")
    @patch("easydeploy.cli.gcp.authenticate")
    @patch("easydeploy.cli.gcp.load_credentials")
    def test_login_command_new_user(self, mock_load_creds, mock_auth, mock_is_auth):
        """Test login command for new user."""
        mock_is_auth.return_value = False
        mock_auth.return_value = True
        mock_load_creds.return_value = {"project": "test-project"}

        result = self.runner.invoke(login)

        assert result.exit_code == 0
        assert "🔐 Starting GCP authentication..." in result.output
        assert "🎉 GCP authentication successful!" in result.output
        assert "📋 Project: test-project" in result.output
        mock_auth.assert_called_once()

    @patch("easydeploy.cli.gcp.is_authenticated")
    @patch("easydeploy.cli.gcp.load_credentials")
    def test_login_command_already_authenticated(self, mock_load_creds, mock_is_auth):
        """Test login command when already authenticated."""
        mock_is_auth.return_value = True
        mock_load_creds.return_value = {"project": "test-project"}

        # Simulate user choosing not to re-authenticate
        result = self.runner.invoke(login, input="n\n")

        assert result.exit_code == 0
        assert "✅ Already authenticated with GCP" in result.output
        assert "📋 Current project: test-project" in result.output

    @patch("easydeploy.cli.gcp.is_authenticated")
    @patch("easydeploy.cli.gcp.authenticate")
    def test_login_command_auth_failure(self, mock_auth, mock_is_auth):
        """Test login command when authentication fails."""
        mock_is_auth.return_value = False
        mock_auth.return_value = False

        result = self.runner.invoke(login)

        assert result.exit_code == 1
        assert "❌ Authentication failed" in result.output
        assert "💡 Please try again or check your internet connection" in result.output

    @patch("easydeploy.cli.gcp.is_authenticated")
    def test_logout_command_not_authenticated(self, mock_is_auth):
        """Test logout command when not authenticated."""
        mock_is_auth.return_value = False

        result = self.runner.invoke(logout)

        assert result.exit_code == 0
        assert "ℹ️  Not currently authenticated with GCP" in result.output

    @patch("easydeploy.cli.gcp.is_authenticated")
    @patch("subprocess.run")
    def test_logout_command_success(self, mock_run, mock_is_auth):
        """Test logout command success."""
        mock_is_auth.return_value = True
        mock_run.return_value = Mock()

        result = self.runner.invoke(logout)

        assert result.exit_code == 0
        assert "🔓 Logging out from GCP..." in result.output
        assert "✅ Successfully logged out from GCP" in result.output

    @patch("easydeploy.cli.gcp.is_authenticated")
    @patch("easydeploy.cli.gcp.load_credentials")
    def test_status_command_authenticated(self, mock_load_creds, mock_is_auth):
        """Test status command when authenticated."""
        mock_is_auth.return_value = True
        mock_load_creds.return_value = {"project": "test-project"}

        result = self.runner.invoke(status)

        assert result.exit_code == 0
        assert "🔍 Checking GCP authentication status..." in result.output
        assert "✅ Authenticated with GCP" in result.output
        assert "📋 Project: test-project" in result.output

    @patch("easydeploy.cli.gcp.is_authenticated")
    def test_status_command_not_authenticated(self, mock_is_auth):
        """Test status command when not authenticated."""
        mock_is_auth.return_value = False

        result = self.runner.invoke(status)

        assert result.exit_code == 0
        assert "❌ Not authenticated with GCP" in result.output
        assert "💡 Run: easydeploy gcp login" in result.output

    @patch("easydeploy.cli.gcp.is_authenticated")
    def test_require_gcp_auth_decorator_authenticated(self, mock_is_auth):
        """Test require_gcp_auth decorator when authenticated."""
        mock_is_auth.return_value = True

        @require_gcp_auth
        def test_func():
            return "success"

        result = test_func()
        assert result == "success"

    @patch("easydeploy.cli.gcp.is_authenticated")
    @patch("easydeploy.cli.gcp.console")
    def test_require_gcp_auth_decorator_not_authenticated(self, mock_console, mock_is_auth):
        """Test require_gcp_auth decorator when not authenticated."""
        mock_is_auth.return_value = False

        @require_gcp_auth
        def test_func():
            return "success"

        with pytest.raises(SystemExit) as exc_info:
            test_func()

        assert exc_info.value.code == 1
        mock_console.print.assert_any_call("❌ Not authenticated with GCP")
        mock_console.print.assert_any_call("💡 Please run: easydeploy gcp login")
