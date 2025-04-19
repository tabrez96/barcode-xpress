"""Router handling barcode input processing.

This module defines endpoints for serving the UI and processing barcode input.
"""
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from app.config.settings import templates
from app.utils.input_simulator import send_text_to_active_app

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    """Serve the main UI template."""
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/scan")
async def receive_barcode(barcode: Annotated[str, Form()]):
    """Receives a barcode via form submission and sends it to the browser."""
    if not barcode:
        raise HTTPException(status_code=400, detail="No barcode data received")

    try:
        return send_text_to_active_app(barcode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
