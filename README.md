# Barcode Xpress

A fully functional FastAPI-based barcode scanning application that forwards scanned barcodes to an active browser window.

## Features

- Web-based UI for barcode input
- Automatic browser simulation to input scanned barcodes
- Built with FastAPI, Jinja2, HTMX, and Alpine.js
- Ready to run with Uvicorn

## Project Structure

```
barcode-xpress/
├── app/                # Main application package
│   ├── config/         # Configuration settings
│   ├── models/         # Data models
│   ├── routers/        # API routes
│   ├── utils/          # Utility functions
│   └── main.py         # FastAPI application setup
├── static/             # Static files (CSS, JS)
├── templates/          # Jinja2 templates
│   ├── partials/       # Reusable template components
│   ├── base.html       # Base template with layout
│   └── index.html      # Main page template
├── main.py             # Application entry point
└── requirements.txt    # Project dependencies
```

## Installation

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the server with:

```bash
python main.py
```

Navigate to http://localhost:5000 in your browser to access the barcode scanner interface.

## Configuration

You can configure the browser used for barcode insertion in `app/config/settings.py`:

```python
BROWSER_NAME = "Google Chrome"  # Change to "Safari" or your browser if needed
```

## License

MIT
