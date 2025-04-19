import subprocess
from app.config.settings import BROWSER_NAME

def send_barcode_to_browser(barcode: str) -> dict:
    """
    Sends the barcode to the active browser by simulating keyboard input.

    Args:
        barcode: The barcode string to send

    Returns:
        dict: Result status and message

    Raises:
        Exception: If there's an error with the AppleScript execution
    """
    # AppleScript to activate browser and simulate typing
    script = f'''
    tell application "{BROWSER_NAME}"
        activate
        delay 0.1
        tell application "System Events"
            keystroke "{barcode}"
            keystroke return
        end tell
    end tell
    '''

    result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"AppleScript error: {result.stderr}")

    return {"status": "success", "message": f"Barcode {barcode} sent"}
