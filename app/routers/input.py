"""Router handling barcode input processing.

This module defines endpoints for serving the UI and processing barcode input.
"""

from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.config.settings import PORT, templates
from app.utils.input_simulator import send_text_to_active_app
from app.utils.logger import setup_logger
from app.utils.network import get_local_ip
from app.utils.qr_generator import get_qr_code_as_base64

# Create module-specific logger
logger = setup_logger("barcode_xpress.router")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def serve_desktop_ui(request: Request):
    """Serve the desktop UI with QR code."""
    logger.info("Serving desktop UI with QR code")

    # Generate QR code URL for connecting from mobile devices
    local_ip = get_local_ip()
    mobile_url = f"http://{local_ip}:{PORT}"
    logger.info(f"Generated mobile URL: {mobile_url}/scan")

    qr_code = get_qr_code_as_base64(f"{mobile_url}/scan")

    return templates.TemplateResponse(
        "index.html", {"request": request, "qr_code": qr_code, "mobile_url": mobile_url}
    )


@router.get("/scan", response_class=HTMLResponse)
async def serve_mobile_ui(request: Request):
    """Serve the mobile UI with barcode input."""
    client = request.client.host if request.client else "unknown"
    logger.info(f"Serving mobile UI to client: {client}")

    return templates.TemplateResponse("mobile_input.html", {"request": request})


@router.post("/scan")
async def receive_barcode(barcode: Annotated[str, Form()]):
    """Receives a barcode via form submission and sends it to the active application."""
    if not barcode:
        logger.warning("Received empty barcode")
        raise HTTPException(status_code=400, detail="No barcode data received")

    logger.info(f"Processing barcode: {barcode}")
    result = send_text_to_active_app(barcode)

    # Check if there was an error
    if result.get("status") == "error":
        logger.error(f"Error sending barcode: {result.get('message')}")
        raise HTTPException(
            status_code=500, detail=result.get("message", "Unknown error")
        )

    return result
