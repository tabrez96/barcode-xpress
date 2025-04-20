"""Main entry point for the Barcode Input Simulator application.

This module initializes and runs the FastAPI application using Uvicorn.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.settings import HOST, PORT
from app.routers import input as input_router

# Create FastAPI app
app = FastAPI(
    title="Barcode Xpress",
    description=(
        "A barcode scanning application that can send input to any active application"
    ),
    version="0.1.0",
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(input_router.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
