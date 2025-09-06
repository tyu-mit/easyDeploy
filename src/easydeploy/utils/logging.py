"""Logging utilities for easyDeploy."""

import logging

from rich.console import Console
from rich.logging import RichHandler


def setup_logging(verbose: bool = False) -> logging.Logger:
    """Set up logging with Rich formatting.

    Args:
        verbose: Enable debug level logging

    Returns:
        Configured logger
    """
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(), show_path=False)],
    )

    return logging.getLogger("easydeploy")
