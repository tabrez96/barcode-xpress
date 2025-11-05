"""Middleware configurations for the application."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class TemplateContextMiddleware(BaseHTTPMiddleware):
    """Middleware that adds request to app.state for template access."""

    def __init__(self, app: ASGIApp):
        """Initialize the middleware."""
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request, storing it in app.state.

        Args:
            request: The incoming request
            call_next: The next handler in the chain

        Returns:
            The response from downstream handlers

        """
        # Store request in app.state
        request.app.state.request = request
        # Continue processing the request
        return await call_next(request)
