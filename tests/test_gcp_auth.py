"""Tests for GCP authentication module."""

import subprocess
from unittest.mock import Mock, patch

from easydeploy.gcp_auth import authenticate, is_authenticated, load_credentials, refresh_token


class TestGCPAuth:
    """Test cases for GCP authentication functions."""

    @patch("subprocess.run")
    def test_is_authenticated_true(self, mock_run):
        """Test is_authenticated returns True when gcloud succeeds."""
        mock_run.return_value = Mock()

        result = is_authenticated()

        assert result is True
        mock_run.assert_called_once_with(
            ["gcloud", "auth", "application-default", "print-access-token"],
            capture_output=True,
            text=True,
            check=True,
        )

    @patch("subprocess.run")
    def test_is_authenticated_false_on_error(self, mock_run):
        """Test is_authenticated returns False when gcloud fails."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "gcloud")

        result = is_authenticated()

        assert result is False

    @patch("subprocess.run")
    def test_is_authenticated_false_on_file_not_found(self, mock_run):
        """Test is_authenticated returns False when gcloud not found."""
        mock_run.side_effect = FileNotFoundError()

        result = is_authenticated()

        assert result is False

    @patch("subprocess.run")
    @patch("builtins.print")
    def test_authenticate_success(self, mock_print, mock_run):
        """Test authenticate returns True on successful authentication."""
        mock_run.return_value = Mock()

        result = authenticate()

        assert result is True
        mock_run.assert_called_once_with(
            ["gcloud", "auth", "application-default", "login"],
            capture_output=True,
            text=True,
            check=True,
        )
        mock_print.assert_any_call("🌐 Opening browser for GCP authentication...")
        mock_print.assert_any_call("✅ GCP authentication successful!")

    @patch("subprocess.run")
    @patch("builtins.print")
    def test_authenticate_failure(self, mock_print, mock_run):
        """Test authenticate returns False on authentication failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "gcloud", stderr="Error")

        result = authenticate()

        assert result is False
        mock_print.assert_any_call("❌ Authentication failed: Error")

    @patch("subprocess.run")
    @patch("builtins.print")
    def test_authenticate_gcloud_not_found(self, mock_print, mock_run):
        """Test authenticate handles gcloud not found."""
        mock_run.side_effect = FileNotFoundError()

        result = authenticate()

        assert result is False
        mock_print.assert_any_call(
            "❌ gcloud CLI not found. Please install Google Cloud SDK first."
        )

    @patch("google.auth.default")
    def test_load_credentials_success(self, mock_default):
        """Test load_credentials returns credentials on success."""
        mock_credentials = Mock()
        mock_project = "test-project"
        mock_default.return_value = (mock_credentials, mock_project)

        result = load_credentials()

        assert result == {"credentials": mock_credentials, "project": mock_project}

    @patch("google.auth.default")
    def test_load_credentials_failure(self, mock_default):
        """Test load_credentials returns None on failure."""
        mock_default.side_effect = Exception("Auth error")

        result = load_credentials()

        assert result is None

    @patch("subprocess.run")
    def test_refresh_token_success(self, mock_run):
        """Test refresh_token returns True on success."""
        mock_run.return_value = Mock()

        result = refresh_token()

        assert result is True

    @patch("subprocess.run")
    def test_refresh_token_failure(self, mock_run):
        """Test refresh_token returns False on failure."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "gcloud")

        result = refresh_token()

        assert result is False
