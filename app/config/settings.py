"""Application settings and configuration variables.

This module contains settings for server configuration and template setup.
"""

from fastapi.templating import Jinja2Templates

# Server configuration
HOST = "0.0.0.0"  # noqa: S104
PORT = 5000

# Templates setup
templates = Jinja2Templates(directory="templates")
