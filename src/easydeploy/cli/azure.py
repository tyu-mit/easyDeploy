"""Azure-specific CLI entry point for easyDeploy."""

import sys

from easydeploy.cli.main import main as main_cli
from easydeploy.utils.logging import setup_logging


def main():
    """Entry point for Azure deployments."""
    # Setup logging
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    setup_logging(verbose)

    # If it's a deploy command, add Azure platform by default
    if len(sys.argv) > 1 and sys.argv[1] == "deploy":
        if "--platform" not in sys.argv:
            # Insert platform option after 'deploy' command
            sys.argv.insert(2, "--platform")
            sys.argv.insert(3, "azure")

    # Run main CLI
    main_cli()


if __name__ == "__main__":
    main()
