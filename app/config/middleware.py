"""Middleware configurations for the application."""

from contextvars import ContextVar

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

# Per-request context variable for storing the current request
_request_context: ContextVar[Request | None] = ContextVar(
    "_request_context", default=None
)


def get_current_request() -> Request | None:
    """Get the current request from context.

    Returns:
        The current request or None if not in a request context.

    """
    return _request_context.get()


class TemplateContextMiddleware(BaseHTTPMiddleware):
    """Middleware that adds request to per-request context for template access."""

    def __init__(self, app: ASGIApp):
        """Initialize the middleware."""
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process the request, storing it in per-request context.

        Args:
            request: The incoming request
            call_next: The next handler in the chain

        Returns:
            The response from downstream handlers

        """
        # Store request in per-request context variable
        token = _request_context.set(request)
        try:
            # Continue processing the request
            return await call_next(request)
        finally:
            # Clear the context variable after request completes
            _request_context.reset(token)
