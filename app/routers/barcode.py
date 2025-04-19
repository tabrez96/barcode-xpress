from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse

from app.config.settings import templates
from app.utils.browser import send_barcode_to_browser

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def serve_ui(request: Request):
    """
    Serves the main UI template.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/scan")
async def receive_barcode(barcode: str = Form(...)):
    """
    Receives a barcode via form submission and sends it to the browser.
    """
    if not barcode:
        raise HTTPException(status_code=400, detail="No barcode data received")

    try:
        result = send_barcode_to_browser(barcode)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
