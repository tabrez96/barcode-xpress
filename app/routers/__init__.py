"""API route handlers for the Barcode Xpress application.

This package contains the API endpoint definitions that handle various routes.
"""

from app.routers.input import router as input_router

__all__ = ["input_router"]
