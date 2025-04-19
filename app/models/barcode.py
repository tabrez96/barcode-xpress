from pydantic import BaseModel

class BarcodeData(BaseModel):
    barcode: str
