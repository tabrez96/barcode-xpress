"""Utilities for simulating keyboard input to applications.

This module provides functionality to send keystrokes to the currently
focused application across different operating systems using pynput.
"""

import time
from typing import Dict

# Import pynput for cross-platform keyboard simulation
from pynput.keyboard import Controller, Key


def send_text_to_active_app(text: str) -> Dict[str, str]:
    """Send text to the currently focused application by simulating keyboard input.

    Uses pynput for cross-platform support on Windows, macOS, and Linux.

    Args:
        text: The text string to send

    Returns
    -------
        dict: Result status and message

    Raises
    ------
        Exception: If there's an error with the keystroke simulation

    """
    try:
        keyboard = Controller()

        # Type the text
        keyboard.type(text)

        # Press Enter
        time.sleep(0.1)  # Small delay before pressing Enter
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        return {
            "status": "success",
            "message": f"Barcode '{text}' sent to active application",
        }
    except Exception as e:
        raise Exception(f"Error simulating keyboard input: {str(e)}") from e
