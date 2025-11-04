"""Application settings and configuration variables.

This module contains settings for server configuration and template setup.
It also handles resolving resource paths when the app is bundled with PyInstaller.
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.templating import Jinja2Templates

# Base paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def get_resource_path(relative_path: str) -> Path:
    """Resolve resource path for both development and PyInstaller bundles."""
    if hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = PROJECT_ROOT
    return base_path / relative_path


# Server configuration
HOST = "0.0.0.0"  # noqa: S104 # Listen on all interfaces
PORT = 8080

# Resource directories
TEMPLATES_DIR = get_resource_path("templates")
STATIC_DIR = get_resource_path("static")

# Templates setup
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
