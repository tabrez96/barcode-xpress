import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.settings import HOST, PORT
from app.routers import barcode

# Create FastAPI app
app = FastAPI(
    title="Barcode Xpress",
    description="A simple barcode scanning application",
    version="0.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(barcode.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
