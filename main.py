"""Main entry point for the Barcode Xpress application."""

import uvicorn

from app.config.settings import HOST, PORT
from app.utils.logger import app_logger as logger
from app.utils.network import get_local_ip

if __name__ == "__main__":
    logger.info("Server starting - Access the app at:")
    logger.info(f"  Local URL: http://localhost:{PORT}")

    # Log the URL to access from other devices
    try:
        ip = get_local_ip()
        logger.info(f"  Network URL: http://{ip}:{PORT}")
        logger.info("  Use this URL or scan the QR code to connect from your phone")
    except Exception as e:
        logger.error(f"Could not determine network URL: {e}")

    # Make sure to set host to 0.0.0.0 to allow external connections
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
