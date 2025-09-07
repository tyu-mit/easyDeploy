"""
GCP Authentication Module for easyDeploy

This module provides OAuth2-based authentication for Google Cloud Platform,
specifically designed for the easyDeploy automation toolkit.

Features:
- Browser-based OAuth2 authentication flow
- Token storage and management
- Authentication validation for GCP operations

Author: Claude (AI Assistant)
Created: 2025-09-06
"""

import json
import os
import subprocess
from typing import Optional


def get_token_path() -> str:
    """Get the path for storing GCP authentication tokens."""
    home_dir = os.path.expanduser("~")
    easydeploy_dir = os.path.join(home_dir, ".easydeploy")

    # Create directory if it doesn't exist
    os.makedirs(easydeploy_dir, mode=0o700, exist_ok=True)

    return os.path.join(easydeploy_dir, "gcp-token.json")


def is_authenticated() -> bool:
    """Check if user is currently authenticated with GCP."""
    try:
        # Check if gcloud user credentials exist
        subprocess.run(
            ["gcloud", "auth", "print-access-token"],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def authenticate() -> bool:
    """
    Perform OAuth2 authentication flow using gcloud CLI.

    Returns:
        bool: True if authentication successful, False otherwise
    """
    try:
        # Use gcloud auth login with --no-launch-browser for WSL compatibility
        print("🌐 Starting GCP authentication...")
        print("💡 Please copy the URL and open it in your browser manually")
        subprocess.run(
            ["gcloud", "auth", "login", "--no-launch-browser"],
            check=True,
        )

        print("✅ GCP authentication successful!")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Authentication failed: {e.stderr}")
        return False

    except FileNotFoundError:
        print("❌ gcloud CLI not found. Please install Google Cloud SDK first.")
        print("Visit: https://cloud.google.com/sdk/docs/install")
        return False


def load_credentials() -> Optional[dict]:
    """
    Load stored GCP credentials using Google's default credentials.

    Returns:
        dict: Credentials dictionary if available, None otherwise
    """
    try:
        from google.auth import default

        credentials, project = default()
        return {"credentials": credentials, "project": project}
    except Exception:
        return None


def refresh_token() -> bool:
    """
    Refresh the current authentication token.

    Returns:
        bool: True if refresh successful, False otherwise
    """
    try:
        subprocess.run(
            ["gcloud", "auth", "application-default", "print-access-token"],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def list_projects() -> list:
    """
    List available GCP projects for the authenticated user.

    Returns:
        list: List of project dictionaries with 'project_id' and 'name'
    """
    try:
        result = subprocess.run(
            ["gcloud", "projects", "list", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
        )

        projects = json.loads(result.stdout)
        return [
            {"project_id": project["projectId"], "name": project.get("name", project["projectId"])}
            for project in projects
        ]
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return []


def set_project(project_id: str) -> bool:
    """
    Set the current GCP project.

    Args:
        project_id: The GCP project ID to set as current

    Returns:
        bool: True if project set successfully, False otherwise
    """
    try:
        subprocess.run(
            ["gcloud", "config", "set", "project", project_id],
            capture_output=True,
            text=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_current_project() -> Optional[str]:
    """
    Get the current GCP project ID.

    Returns:
        str: Current project ID if set, None otherwise
    """
    try:
        result = subprocess.run(
            ["gcloud", "config", "get-value", "project"],
            capture_output=True,
            text=True,
            check=True,
        )
        project_id = result.stdout.strip()
        return project_id if project_id and project_id != "(unset)" else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
