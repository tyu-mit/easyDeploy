"""Configuration settings for easyDeploy."""

import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml


class Settings:
    """Global settings manager for easyDeploy."""

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize settings.

        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or Path.home() / ".easydeploy" / "config.yaml"
        self.state_dir = Path.cwd() / "state"
        self.templates_dir = Path.cwd() / "templates"
        self.scripts_dir = Path.cwd() / "src" / "scripts"

        self._config = {}
        self._load_config()

    def _load_config(self):
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                self._config = yaml.safe_load(f) or {}
        else:
            self._config = self._default_config()

    def _default_config(self) -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "cloud": {
                "gcp": {
                    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT"),
                    "region": "us-central1",
                    "zone": "us-central1-a",
                },
                "azure": {
                    "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
                    "resource_group": "easydeploy-rg",
                    "location": "eastus",
                },
            },
            "defaults": {
                "instance_type": {"gcp": "n1-standard-4", "azure": "Standard_D4s_v3"},
                "gpu_instance_type": {
                    "gcp": "n1-standard-4",  # with GPU attachment
                    "azure": "Standard_NC6s_v3",
                },
            },
            "software": {"ros_version": "humble", "python_version": "3.11", "cuda_version": "12.0"},
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation key.

        Args:
            key: Configuration key (e.g., "cloud.gcp.project_id")
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value = self._config

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default

    def set(self, key: str, value: Any):
        """Set configuration value by dot-notation key.

        Args:
            key: Configuration key
            value: Value to set
        """
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def save(self):
        """Save configuration to file."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            yaml.dump(self._config, f, default_flow_style=False)


# Global settings instance
settings = Settings()
