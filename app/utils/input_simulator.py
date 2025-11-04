"""Utilities for simulating keyboard input to applications.

This module provides functionality to send keystrokes to the currently
focused application across different operating systems using pynput.
"""

import time

# Import pynput for cross-platform keyboard simulation
from pynput.keyboard import Controller, Key

from app.utils.logger import setup_logger

# Create module-specific logger
logger = setup_logger("barcode_xpress.input_simulator")


def send_text_to_active_app(text: str) -> bool:
    """Send text to the currently focused application by simulating keyboard input.

    Uses pynput for cross-platform support on Windows, macOS, and Linux.

    Args:
        text: The text string to send

    Returns:
    -------
        bool: True if successful

    Raises:
    ------
        Exception: If there's an error with the keystroke simulation

    """
    logger.info(f"Sending text to active application: '{text}'")
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
        return True
    except Exception as e:
        error_msg = f"Error simulating keyboard input: {str(e)}"
        logger.error(error_msg)
        raise Exception(error_msg) from e
