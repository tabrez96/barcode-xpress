"""Barcode data models for the application."""

from pydantic import BaseModel


class BarcodeData(BaseModel):
    """Model representing barcode data sent from client."""

    barcode: str
