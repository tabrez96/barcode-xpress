"""Template rendering utilities.

This module provides helper functions for rendering Jinja2 templates.
"""

from typing import Any

from fastapi import Request
from fastapi.responses import HTMLResponse

from app.config.settings import templates


def render_template(
    request: Request,
    template_name: str,
    context: dict[str, Any] | None = None,
    status_code: int = 200,
) -> HTMLResponse:
    """Render a Jinja2 template with the given context.

    Args:
        request: The FastAPI request object
        template_name: Name of the template file to render
        context: Dictionary of context variables to pass to the template
        status_code: HTTP status code for the response (default: 200)

    Returns:
        HTMLResponse with the rendered template

    """
    template_context = {"request": request}
    if context:
        template_context.update(context)

    return templates.TemplateResponse(
        template_name,
        template_context,
        status_code=status_code,
    )
