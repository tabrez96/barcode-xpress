"""Application settings and configuration variables.

This module contains settings for server configuration and template setup.
"""
from fastapi.templating import Jinja2Templates

# Server configuration
HOST = "127.0.0.1"  # Only bind to localhost for security
PORT = 5000

# Templates setup
templates = Jinja2Templates(directory="templates")
