"""Logging utility for the application."""

from __future__ import annotations

import logging
import sys
from copy import deepcopy
from typing import Any, Optional, TextIO

from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG

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


def _stream_supports_tty(stream: Optional[TextIO]) -> bool:
    """Return True if the provided stream exposes a TTY."""
    if stream is None:
        return False
    isatty = getattr(stream, "isatty", None)
    if callable(isatty):
        try:
            return bool(isatty())
        except Exception:  # pragma: no cover - defensive only
            return False
    return False


def build_uvicorn_log_config() -> dict[str, Any]:
    """Return a Uvicorn logging config that works without an attached terminal."""
    log_config = deepcopy(UVICORN_LOGGING_CONFIG)

    if not _stream_supports_tty(sys.stderr):
        formatter = log_config["formatters"].get("default")
        if isinstance(formatter, dict):
            formatter["use_colors"] = False

    if not _stream_supports_tty(sys.stdout):
        formatter = log_config["formatters"].get("access")
        if isinstance(formatter, dict):
            formatter["use_colors"] = False

    return log_config
