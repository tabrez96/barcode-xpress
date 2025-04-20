"""Logging utility for the application."""

import logging
import sys
from typing import Optional

# Set up logging format
LOGGER_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Set up and return a logger with the given name and level.

    Args:
        name: The logger name
        level: The logging level (defaults to INFO)

    Returns:
    -------
        A configured logger instance

    """
    if level is None:
        level = logging.INFO

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if not logger.handlers:
        # Create console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)

        # Create formatter
        formatter = logging.Formatter(LOGGER_FORMAT, DATE_FORMAT)
        handler.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(handler)

    return logger


# Create a default application logger
app_logger = setup_logger("barcode_xpress")
