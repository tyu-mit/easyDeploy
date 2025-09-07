# easyDeploy

**easyDeploy** is an automation deployment toolkit designed to simplify the setup of cloud services and software environments for robotics AI development.

## Features

- 🚀 **Fast Deployment**: Quick setup of robotics AI development environments
- ☁️ **Multi-Cloud Support**: Deploy to Google Cloud Platform (Azure support coming soon)
- 🤖 **Robotics-Focused**: Optimized for robotics research and development workflows
- 🔐 **Simple Authentication**: Easy GCP authentication and project management

## Installation

### Prerequisites

- Python 3.11 or higher
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (for GCP deployments)
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Install easyDeploy

```bash
# Clone the repository
git clone https://github.com/tyu-mit/easyDeploy.git
cd easyDeploy

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

## Quick Start

### GCP Authentication

Before deploying to GCP, you need to authenticate:

```bash
# Authenticate with your Google account
uv run easydeploy gcp login

# Check authentication status
uv run easydeploy gcp status

# List available GCP projects
uv run easydeploy gcp list-projects

# Select a project to work with
uv run easydeploy gcp select-project

# Logout when done
uv run easydeploy gcp logout
```

### Basic Usage

```bash
# Show all available commands
uv run easydeploy --help

# Show GCP-specific commands
uv run easydeploy gcp --help
```

## GCP Authentication Commands

| Command | Description |
|---------|-------------|
| `easydeploy gcp login` | Authenticate with Google Cloud Platform |
| `easydeploy gcp logout` | Remove GCP authentication |
| `easydeploy gcp status` | Show current authentication status and selected project |
| `easydeploy gcp list-projects` | List all available GCP projects |
| `easydeploy gcp select-project` | Interactively select a GCP project |

## Project Structure

```
easyDeploy/
├── src/easydeploy/
│   ├── cli/                    # Command-line interface
│   ├── cloud/                  # Cloud provider integrations
│   │   └── gcp/               # Google Cloud Platform
│   │       ├── auth.py        # GCP authentication
│   │       └── compute.py     # GCP resource management
│   ├── config/                # Configuration management
│   └── utils/                 # Common utilities
├── scripts/                   # Deployment scripts
└── tests/                     # Test suite
```

## Development

### Setting up Development Environment

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run linting
uv run ruff check

# Format code
uv run ruff format
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions and support, please open an issue on GitHub.
