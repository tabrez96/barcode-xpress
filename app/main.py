"""Main entry point for the Barcode Input Simulator application.

This module initializes and runs the FastAPI application using Uvicorn.
It includes helpers to improve the user experience when the app is bundled
as a desktop application (e.g., launching the browser automatically and
surfacing startup errors with a dialog instead of silently exiting).
"""

from __future__ import annotations

import errno
import json
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from contextlib import closing, suppress
from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.settings import HOST, PORT, STATIC_DIR
from app.routers import input as input_router
from app.utils.logger import build_uvicorn_log_config, setup_logger

# Create FastAPI app
app = FastAPI(
    title="Barcode Xpress",
    description=(
        "A barcode scanning application that can send input to any active application"
    ),
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Include routers
app.include_router(input_router.router)

# Application logger
logger = setup_logger("barcode_xpress.main")


def should_reload() -> bool:
    """Determine whether to enable auto-reload (disabled in bundled builds)."""
    return os.getenv("BARCODEXPRESS_RELOAD", "false").lower() == "true"


def get_requested_port() -> int:
    """Read desired port from environment, falling back to the default."""
    with suppress(ValueError):
        return int(os.getenv("BARCODEXPRESS_PORT", PORT))
    logger.warning("Invalid BARCODEXPRESS_PORT value. Falling back to %s.", PORT)
    return PORT


def open_browser_later(port: int) -> None:
    """Open the default browser to the local app URL after a short delay."""

    def _open() -> None:
        time.sleep(1)
        url = f"http://127.0.0.1:{port}/"
        try:
            webbrowser.open(url, new=1, autoraise=True)
            logger.info("Opened default browser at %s", url)
        except Exception as exc:
            logger.debug("Unable to open browser automatically: %s", exc)

    threading.Thread(target=_open, daemon=True).start()


def _show_tk_dialog(message: str) -> bool:
    """Try to display an error dialog using Tkinter."""
    try:
        import tkinter as tk
        from tkinter import messagebox
    except Exception as exc:
        logger.debug("Tkinter error dialog unavailable: %s", exc)
        return False

    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title="Barcode Xpress", message=message)
    root.destroy()
    return True


def _show_osascript_dialog(message: str) -> bool:
    """Display an alert dialog on macOS using AppleScript."""
    if sys.platform != "darwin":
        return False

    script = (
        'display alert "Barcode Xpress" '
        f"message {json.dumps(message)} as critical "
        'buttons {"OK"} default button "OK"'
    )
    try:
        subprocess.run(  # noqa: S603
            ["osascript", "-e", script],  # noqa: S607
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except Exception as exc:
        logger.debug("AppleScript dialog unavailable: %s", exc)
        return False


def show_error_dialog(message: str) -> None:
    """Display an error dialog, falling back to stderr when GUI is unavailable."""
    if _show_tk_dialog(message):
        return
    if _show_osascript_dialog(message):
        return

    logger.error("Unable to display GUI error dialog. Message: %s", message)
    sys.stderr.write(f"Error: {message}\n")


def prompt_for_alternate_port(current_port: int) -> Optional[int]:
    """Ask the user to pick a different port when the preferred one is unavailable."""
    try:
        import tkinter as tk
        from tkinter import simpledialog
    except Exception as exc:
        logger.error("Failed to import tkinter for port prompt: %s", exc)
        return None

    root = tk.Tk()
    root.withdraw()
    prompt = (
        f"Barcode Xpress could not listen on port {current_port}.\n"
        "Enter an alternate port between 1024 and 65535."
    )
    new_port = simpledialog.askinteger(
        title="Barcode Xpress",
        prompt=prompt,
        initialvalue=min(max(current_port, 1024), 65535),
        minvalue=1024,
        maxvalue=65535,
    )
    root.destroy()
    if new_port is None:
        logger.info("User canceled the alternate port prompt.")
        return None
    logger.info("User selected alternate port: %s", new_port)
    return int(new_port)


def check_port_available(port: int) -> tuple[bool, Optional[OSError]]:
    """Verify whether the desired port can be bound."""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((HOST, port))
        except OSError as exc:
            return False, exc
    return True, None


def run_server(port: int) -> None:
    """Run the Uvicorn server on the specified port."""
    app.state.port = port  # Track the bound port for routers/templates.
    open_browser_later(port)

    log_config = build_uvicorn_log_config()
    config = uvicorn.Config(
        app=app,
        host=HOST,
        port=port,
        reload=False,
        log_config=log_config,
    )
    server = uvicorn.Server(config)
    logger.info("Starting Barcode Xpress server on %s:%s", HOST, port)
    server.run()


def main() -> None:
    """Entry point used by both the CLI and bundled executable."""
    reload_enabled = should_reload()
    requested_port = get_requested_port()

    if reload_enabled:
        logger.info("Starting in reload mode on port %s.", requested_port)
        app.state.port = requested_port
        open_browser_later(requested_port)
        uvicorn.run(
            app=app,
            host=HOST,
            port=requested_port,
            reload=True,
            log_config=build_uvicorn_log_config(),
        )
        return

    port = requested_port
    while True:
        available, error = check_port_available(port)
        if not available:
            if error is None:  # Should never happen, but satisfy type checkers
                logger.error("Port %s is unavailable (unknown error)", port)
                break
            logger.error("Port %s is unavailable: %s", port, error)
            if error.errno not in (errno.EACCES, errno.EADDRINUSE, errno.EPERM):
                show_error_dialog(
                    f"Unexpected error while preparing Barcode Xpress:\n{error}"
                )
                break

            alternate_port = prompt_for_alternate_port(port)
            if alternate_port is None:
                show_error_dialog(
                    "Barcode Xpress could not start because the selected port is "
                    "unavailable or requires elevated permissions."
                )
                break
            port = alternate_port
            continue

        try:
            run_server(port)
            break
        except OSError as exc:
            logger.error("Failed to start server on port %s: %s", port, exc)
            show_error_dialog(
                f"Barcode Xpress encountered an unexpected error while starting:\n{exc}"
            )
            break


if __name__ == "__main__":
    main()
