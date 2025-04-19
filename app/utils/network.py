"""Network utility functions."""

import socket

from app.utils.logger import setup_logger

# Create module-specific logger
logger = setup_logger("barcode_xpress.network")


def get_local_ip() -> str:
    """Get the local IP address of this machine.

    Returns
    -------
        The local IP address as a string

    Raises
    ------
        Exception: If unable to determine IP address

    """
    logger.debug("Attempting to determine local IP address...")
    try:
        # Create a socket connection to an external server
        # This is a reliable way to determine the local IP used for external connections
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        logger.debug(f"Local IP determined: {ip}")
        return ip
    except Exception as e:
        # Fallback to hostname lookup if the above method fails
        logger.warning(f"Primary IP detection failed: {str(e)}, trying fallback method")
        try:
            ip = socket.gethostbyname(socket.gethostname())
            logger.debug(f"Local IP determined via fallback: {ip}")
            return ip
        except Exception as fallback_error:
            logger.error(f"Failed to determine local IP: {str(fallback_error)}")
            raise Exception(
                f"Could not determine local IP address: {str(fallback_error)}"
            ) from fallback_error
