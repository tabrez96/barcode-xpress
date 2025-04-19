"""Utilities for simulating keyboard input to applications.

This module provides functionality to send keystrokes to the currently
focused application.
"""
import subprocess


def send_text_to_active_app(text: str) -> dict:
    """Send text to the currently focused application by simulating keyboard input.

    Args:
        text: The text string to send

    Returns
    -------
        dict: Result status and message

    Raises
    ------
        Exception: If there's an error with the AppleScript execution
    """
    # AppleScript to simulate typing in the currently focused application
    script = f"""
    tell application "System Events"
        keystroke "{text}"
        keystroke return
    end tell
    """

    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"AppleScript error: {result.stderr}")

    return {
        "status": "success",
        "message": f"Barcode '{text}' sent to active application",
    }
