"""Utilities for simulating keyboard input to applications.

This module provides functionality to send keystrokes to the currently
focused application across different operating systems using pynput.
"""

import platform
import subprocess
import time
from typing import Dict, Optional

# Import pynput for cross-platform keyboard simulation
from pynput.keyboard import Controller, Key

from app.utils.logger import setup_logger

# Create module-specific logger
logger = setup_logger("barcode_xpress.input_simulator")

# Keep track of whether we've warned about permissions
_has_warned_about_permissions = False


def is_admin_windows() -> bool:
    """Check if the application is running with administrator privileges on Windows."""
    if platform.system() != "Windows":
        return False

    try:
        import ctypes

        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False


def check_accessibility_permissions() -> Optional[bool]:
    """Check if the application has accessibility permissions on macOS.

    Returns
    -------
        True if permissions granted, False if denied, None if unknown/non-macOS
    """
    if platform.system() != "Darwin":
        return None  # Not applicable on non-macOS systems

    try:
        # Try to execute an AppleScript to check permissions
        script = """
        tell application "System Events"
            set frontApp to name of first application process whose frontmost is true
            return frontApp
        end tell
        """

        result = subprocess.run(
            ["osascript", "-e", script], capture_output=True, text=True
        )

        if result.returncode == 0:
            logger.info("Accessibility permissions are granted")
            return True

        logger.warning(f"Accessibility permissions check failed: {result.stderr}")
        # Error about "not allowed assistive access" indicates permission denied
        if "not allowed assistive access" in result.stderr:
            return False

        return None
    except Exception as e:
        logger.error(f"Error checking accessibility permissions: {e}")
        return None


def send_text_to_active_app(text: str) -> Dict[str, str]:
    """Send text to the currently focused application by simulating keyboard input.

    Uses pynput for cross-platform support on Windows, macOS, and Linux.

    Args:
        text: The text string to send

    Returns
    -------
        dict: Result status and message
    """
    global _has_warned_about_permissions
    logger.info(f"Sending text to active application: '{text}'")

    # Check for platform-specific permissions
    system = platform.system()

    # macOS permission check
    if system == "Darwin" and not _has_warned_about_permissions:
        permissions = check_accessibility_permissions()
        if permissions is False:
            _has_warned_about_permissions = True
            logger.error("ACCESSIBILITY PERMISSIONS REQUIRED")
            logger.error("This app needs accessibility permissions to send keystrokes.")
            logger.error(
                "Please go to System Preferences > Security & Privacy > Privacy > Accessibility"  # noqa: E501
            )
            logger.error("Add this application to the allowed applications list.")

            # Show a more user-friendly message in the result
            return {
                "status": "error",
                "message": "Accessibility permissions required. Please check the app logs and grant permissions in System Settings.",  # noqa: E501
            }

    # Windows admin check
    elif system == "Windows" and not _has_warned_about_permissions:
        if not is_admin_windows():
            _has_warned_about_permissions = True
            logger.warning("Application may need administrator privileges on Windows")
            logger.warning("Try running the application as Administrator")
            # We don't return an error here because
            # Windows might work without admin rights in some cases

    try:
        keyboard = Controller()

        # Type the text
        keyboard.type(text)
        logger.debug(f"Text typed: '{text}'")

        # Press Enter
        time.sleep(0.1)  # Small delay before pressing Enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        logger.debug("Enter key pressed")

        logger.info(f"Successfully sent barcode: '{text}'")
        return {
            "status": "success",
            "message": f"Barcode '{text}' sent to active application",
        }
    except Exception as e:
        error_msg = f"Error simulating keyboard input: {str(e)}"

        # Add platform-specific error help
        if system == "Darwin" and not _has_warned_about_permissions:
            _has_warned_about_permissions = True
            logger.error("This may be due to missing accessibility permissions.")
            logger.error(
                "Please grant permissions in System Preferences > Security & Privacy > Privacy > Accessibility"  # noqa: E501
            )
            error_msg += " (This may be due to missing accessibility permissions)"

        elif system == "Windows" and not _has_warned_about_permissions:
            _has_warned_about_permissions = True
            logger.error("This may be due to insufficient permissions on Windows.")
            logger.error("Try running the application as Administrator.")
            error_msg += " (Try running as Administrator)"

        logger.error(error_msg)
        return {
            "status": "error",
            "message": error_msg,
        }
