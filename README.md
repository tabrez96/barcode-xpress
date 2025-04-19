# Barcode Xpress

A fully functional FastAPI-based application that scans barcodes and sends them to any active application by simulating keystrokes.

## Features

- Web-based UI for barcode input
- Automatic keystroke simulation to any focused application
- Works with any application that accepts keyboard input (e.g., Notepad, Word, Excel, etc.)
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

1. Run the server with:

```bash
python main.py
```

2. Navigate to http://localhost:5000 in your browser to access the barcode scanner interface.
3. Open any application where you want to input the barcode (make sure it's focused)
4. Enter the barcode in the web interface and click "Scan"
5. The barcode will be automatically typed into the focused application

## How It Works

The application uses AppleScript to simulate keyboard input to whatever application is currently in focus on your Mac. When you click "Scan", the barcode is sent as keystrokes to the active application, followed by a return key press.

## License

MIT
