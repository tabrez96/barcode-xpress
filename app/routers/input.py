"""Router handling barcode input processing.

This module defines endpoints for serving the UI and processing barcode input.
"""

from typing import Annotated

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from app.config.settings import PORT
from app.templates import render_template
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
    runtime_port = getattr(request.app.state, "port", PORT)
    mobile_url = f"http://{local_ip}:{runtime_port}"
    logger.info(f"Generated mobile URL: {mobile_url}/scan")

    qr_code = get_qr_code_as_base64(f"{mobile_url}/scan")

    return render_template(
        request=request,
        template_name="index.html",
        context={"qr_code": qr_code, "mobile_url": mobile_url},
    )


@router.get("/scan", response_class=HTMLResponse)
async def serve_mobile_ui(request: Request):
    """Serve the mobile UI with barcode input."""
    client = request.client.host if request.client else "unknown"
    logger.info(f"Serving mobile UI to client: {client}")

    return render_template(request=request, template_name="mobile_input.html")


@router.post("/scan", response_class=HTMLResponse)
async def receive_barcode(request: Request, barcode: Annotated[str, Form()] = ""):
    """Receive barcode via HTMX and send it to the active application.

    Returns a partial HTML fragment with success/error message.
    """
    if not barcode.strip():
        logger.warning("Received empty barcode")
        return render_template(
            request=request,
            template_name="partials/message.html",
            context={"message": "No barcode data received", "message_type": "error"},
        )

    try:
        logger.info(f"Processing barcode: {barcode}")
        send_text_to_active_app(barcode)
    except Exception as exc:
        error_msg = str(exc)
        logger.error(f"Error processing barcode: {error_msg}")
        return render_template(
            request=request,
            template_name="partials/message.html",
            context={
                "message": error_msg,
                "message_type": "error",
            },
            status_code=500,
        )

    return render_template(
        request=request,
        template_name="partials/message.html",
        context={
            "message": f"Barcode '{barcode}' sent to active application",
            "message_type": "success",
        },
    )
