"""Utilities for generating QR codes."""

import base64
import io

import qrcode
from qrcode.image.pil import PilImage

from app.utils.logger import setup_logger

# Create module-specific logger
logger = setup_logger("barcode_xpress.qr_generator")


def generate_qr_code(data: str) -> PilImage:
    """Generate a QR code for the given data.

    Args:
        data: The data to encode in the QR code

    Returns:
    -------
        A PIL image containing the QR code

    """
    logger.debug(f"Generating QR code for data: {data}")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    logger.debug("QR code image generated successfully")
    return image


def get_qr_code_as_base64(data: str) -> str:
    """Generate a QR code and return it as a base64-encoded string.

    Args:
        data: The data to encode in the QR code

    Returns:
    -------
        A base64-encoded string containing the QR code image

    """
    logger.info(f"Creating base64 QR code for URL: {data}")
    img = generate_qr_code(data)

    # Save image to a bytes buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
    result = f"data:image/png;base64,{img_str}"

    logger.debug("Base64 QR code created successfully")
    return result
