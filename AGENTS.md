# AI Agent Instructions for Barcode Xpress

This document provides guidelines for AI assistants (Claude, GitHub Copilot, Gemini, etc.) working on the Barcode Xpress project.

## Project Overview

**Barcode Xpress** is a FastAPI-based web application that scans barcodes and sends them to any active application by simulating keystrokes. It features both desktop and mobile interfaces with cross-platform support (Windows, macOS, Linux).

### Core Features
- Web-based barcode input interface
- QR code generation for mobile device connection
- Automatic keystroke simulation to focused applications
- Dark/light mode theming
- Desktop and mobile responsive UIs

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Jinja2** - Server-side templating
- **Pydantic** - Data validation
- **pynput** - Cross-platform keyboard control

### Frontend
- **HTMX** - Dynamic HTML interactions
- **Alpine.js** - Minimal JavaScript framework for UI reactivity
- **Tailwind CSS v3.4** - Utility-first CSS framework with custom theming

### Build & Distribution
- **PyInstaller** - Creating standalone executables
- **py2app** - macOS app bundling

## Project Architecture

### Directory Structure

```
barcode-xpress/
├── app/                        # Main application package
│   ├── config/                 # Configuration and settings
│   │   └── settings.py         # App settings, paths, and Jinja2 setup
│   ├── models/                 # Pydantic data models
│   │   └── barcode.py          # Barcode-related models
│   ├── routers/                # FastAPI route handlers
│   │   └── input.py            # Desktop UI, mobile UI, and barcode processing
│   ├── utils/                  # Utility modules
│   │   ├── input_simulator.py # Keystroke simulation logic
│   │   ├── logger.py           # Logging configuration
│   │   ├── network.py          # Network utilities (get local IP)
│   │   └── qr_generator.py     # QR code generation
│   ├── templates.py            # Template rendering helper
│   └── main.py                 # FastAPI app initialization and entry point
├── static/                     # Static assets (CSS, JS)
│   ├── css/style.css           # Compiled Tailwind CSS
│   └── js/                     # JavaScript files
│       ├── lib/                # Third-party libraries (HTMX, Alpine.js)
│       └── main.js             # Custom JavaScript
├── templates/                  # Jinja2 HTML templates
│   ├── partials/               # Reusable template components
│   ├── base.html               # Base layout template
│   ├── index.html              # Desktop UI (QR code display)
│   └── mobile_input.html       # Mobile barcode input UI
├── tailwindcss/                # Tailwind CSS workspace
│   ├── src/                    # Source CSS files
│   │   ├── main.css            # Main CSS entry point
│   │   └── theme.css           # Custom theme variables
│   ├── tailwind.config.js      # Tailwind configuration
│   └── postcss.config.js       # PostCSS configuration
├── main.py                     # CLI entry point
├── requirements.txt            # Production dependencies
└── requirements-dev.txt        # Development dependencies
```

## Code Conventions

### Python Style
- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Use **docstrings** for modules, classes, and functions (Google style preferred)
- Import order: standard library → third-party → local imports
- Use `from __future__ import annotations` for better type hint compatibility

### Naming Conventions
- **Variables/Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private/Internal**: Prefix with single underscore `_private_function`

### Logging
- Always use the project's logger from `app.utils.logger`
- Logger naming convention: `"barcode_xpress.{module_name}"`
- Example:
  ```python
  from app.utils.logger import setup_logger
  logger = setup_logger("barcode_xpress.router")
  ```

### Error Handling
- Use `try/except` blocks for external operations (keyboard simulation, network, file I/O)
- Log errors with appropriate severity levels
- Return user-friendly error messages in templates
- Use `Exception` catching with `# noqa: BLE001` only when necessary for broad error handling

## FastAPI Patterns

### Router Structure
- Each router should have a clear, focused purpose
- Use `APIRouter()` instances in router modules
- Include routers in `main.py` with `app.include_router()`
- Example:
  ```python
  from fastapi import APIRouter
  router = APIRouter()
  
  @router.get("/endpoint")
  async def handler():
      ...
  ```

### Request Handling
- Use `Request` object to access app state: `request.app.state.port`
- Use `Form()` for form data: `barcode: Annotated[str, Form()]`
- Return `HTMLResponse` for template responses
- Use `render_template()` helper from `app.templates` for all template rendering

### Template Rendering Pattern
```python
from app.templates import render_template

return render_template(
    request=request,
    template_name="template.html",
    context={"key": "value"},
    status_code=200  # optional
)
```

### Application State
- Store runtime configuration in `app.state` (e.g., `app.state.port`)
- Access in routes via `request.app.state.{attribute}`

## Frontend Patterns

### HTMX Usage
- Use `hx-post`, `hx-get` for AJAX requests
- Use `hx-target` to specify where responses should be inserted
- Use `hx-swap` to control how content is swapped
- Return HTML partials from POST endpoints for seamless updates

### Alpine.js Usage
- Use `x-data` for component state
- Use `x-on:` or `@` for event handlers
- Keep Alpine.js logic minimal and declarative
- Use for UI interactions like dropdowns, modals, toggles

### Tailwind CSS
- Use utility classes directly in HTML
- Custom theme variables in `tailwindcss/src/theme.css`
- Dark mode: Use `dark:` prefix for dark mode styles
- Build CSS: `cd tailwindcss && npm run css:build`
- Watch mode for development: `cd tailwindcss && npm run css:watch`

### Template Structure
- Extend `base.html` for all pages
- Use `{% block content %}` for page-specific content
- Place reusable components in `templates/partials/`
- Include HTMX and Alpine.js from local static files

## Configuration & Settings

### Environment Variables
- `BARCODEXPRESS_PORT` - Override default port (default: 8080)
- `BARCODEXPRESS_RELOAD` - Enable auto-reload in development (default: false)

### Resource Path Resolution
- Use `get_resource_path()` from `app.config.settings` for PyInstaller compatibility
- Automatically resolves paths for both development and bundled executables
- Example:
  ```python
  from app.config.settings import get_resource_path
  template_path = get_resource_path("templates")
  ```

## Common Development Tasks

### Adding a New Route
1. Define route in appropriate router file (or create new router in `app/routers/`)
2. Use type hints and docstrings
3. Add logging for key operations
4. Include router in `main.py` if it's new
5. Create corresponding template if needed

### Adding a New Template
1. Create template file in `templates/`
2. Extend `base.html` if it's a full page
3. Use Tailwind utility classes for styling
4. Test in both light and dark modes
5. Ensure mobile responsiveness

### Modifying Styles
1. Edit `tailwindcss/src/theme.css` for theme variables
2. Edit `tailwindcss/tailwind.config.js` for Tailwind configuration
3. Rebuild CSS: `cd tailwindcss && npm run css:build`
4. Use `npm run css:watch` during development

### Adding Dependencies
- Production: Add to `requirements.txt`
- Development: Add to `requirements-dev.txt`
- Specify version constraints (e.g., `fastapi>=0.104.0`)

## Things to Avoid

### ❌ Don't Do This
- **Don't** use `print()` for logging - use the logger
- **Don't** hardcode paths - use `get_resource_path()` or settings constants
- **Don't** hardcode the port - respect `request.app.state.port` or environment variables
- **Don't** create heavy JavaScript frameworks - keep frontend minimal (HTMX + Alpine.js)
- **Don't** use inline styles - use Tailwind utility classes
- **Don't** modify `static/css/style.css` directly - edit source files in `tailwindcss/src/`
- **Don't** forget to handle errors and edge cases
- **Don't** skip type hints and docstrings
- **Don't** commit built artifacts (bundled apps, compiled CSS without source)
- **Don't** use global state - use FastAPI's dependency injection or app.state

### ✅ Do This Instead
- **Do** use structured logging with appropriate levels
- **Do** use configuration from `app.config.settings`
- **Do** handle exceptions gracefully with user-friendly messages
- **Do** write type-safe code with full type hints
- **Do** test on multiple platforms when dealing with OS-specific code
- **Do** keep frontend interactions progressive (work without JS when possible)
- **Do** use semantic HTML and accessibility best practices
- **Do** update both light and dark mode styles
- **Do** follow the established project structure and patterns

## Git Commit Guidelines

### Commit Message Format
- Use clear, descriptive commit titles
- Include a body with bullet points for detailed changes
- Mention benefits when applicable
- **Do NOT include AI attribution** (no "Generated with Claude" or "Co-Authored-By: Claude")
- Keep commits focused on a single logical change

### Example Commit Message
```
Add feature for user authentication

Implement JWT-based authentication system with refresh tokens.

Changes:
- Add authentication middleware
- Create login and logout endpoints
- Implement token refresh logic

Benefits:
- Secure user sessions
- Token-based authentication
```

## Testing & Quality

### Development Dependencies
- **ruff** - Fast Python linter and formatter
- **mypy** - Static type checker
- **pre-commit** - Git hooks for code quality

### Pre-commit Hooks
Run `pre-commit install` to set up automatic checks before commits.

### Manual Checks
```bash
# Linting
ruff check .

# Formatting
ruff format .

# Type checking
mypy app/
```

## Platform-Specific Considerations

### macOS
- Uses `osascript` for native dialogs
- py2app for app bundling
- Special handling for `.app` bundle resources

### Windows
- Uses Tkinter for dialogs
- PyInstaller for executable creation
- Different keyboard simulation behavior

### Linux
- Tkinter dialogs
- May require X11 for keyboard simulation

When writing platform-specific code:
- Check `sys.platform` (`"darwin"`, `"win32"`, `"linux"`)
- Provide fallbacks for cross-platform compatibility
- Test on target platforms

## Useful Code Snippets

### Creating a New Router
```python
"""Router for [purpose]."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.templates import render_template
from app.utils.logger import setup_logger

logger = setup_logger("barcode_xpress.router_name")

router = APIRouter()


@router.get("/endpoint", response_class=HTMLResponse)
async def handler(request: Request):
    """Handle [description]."""
    logger.info("Processing request")
    return render_template(
        request=request,
        template_name="template.html",
        context={},
    )
```

### Template with HTMX
```html
{% extends "base.html" %}

{% block content %}
<div class="container mx-auto p-4">
  <form hx-post="/endpoint" hx-target="#result" hx-swap="innerHTML">
    <input type="text" name="field" class="input" />
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
  <div id="result"></div>
</div>
{% endblock %}
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Jinja2 Template Designer Documentation](https://jinja.palletsprojects.com/)

## Questions or Clarifications?

When uncertain about implementation details:
1. Check existing code patterns in similar modules
2. Refer to this document for architectural guidance
3. Follow the established conventions consistently
4. Prioritize maintainability and readability over cleverness

