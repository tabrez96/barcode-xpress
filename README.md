# Barcode Xpress

A fully functional FastAPI-based application that scans barcodes and sends them to any active application by simulating keystrokes. Works on Windows, macOS, and Linux.

## Features

- Web-based UI for barcode input
- Automatic keystroke simulation to any focused application
- Cross-platform support for Windows, macOS, and Linux
- Works with any application that accepts keyboard input (e.g., Notepad, Word, Excel, etc.)
- Built with FastAPI, Jinja2, HTMX, Alpine.js, and Tailwind CSS v3.4
- Supports dark and light mode with a custom theme
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
├── static/             # Static files
│   └── css/            # CSS files including compiled Tailwind
├── tailwindcss/        # Tailwind CSS configuration
│   ├── src/            # Source CSS files
│   ├── package.json    # NPM dependencies for Tailwind
│   ├── tailwind.config.js # Tailwind configuration
│   └── postcss.config.js  # PostCSS configuration
├── templates/          # Jinja2 templates
│   ├── partials/       # Reusable template components
│   ├── base.html       # Base template with layout
│   └── index.html      # Main page template
├── main.py             # Application entry point
└── requirements.txt    # Project dependencies
```

## Installation

1. Clone the repository
2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install and build Tailwind CSS:

```bash
cd tailwindcss
npm install
npm run css:build
```

## Developer Setup

If you're developing or contributing to this project:

1. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

2. Set up pre-commit hooks:

```bash
pre-commit install
```

3. Start Tailwind CSS watcher for development:

```bash
cd tailwindcss
npm run css:watch
```

## Tailwind CSS Customization

The project uses a custom themed configuration for Tailwind CSS with both light and dark mode support. To customize:

1. Edit `tailwindcss/src/theme.css` to modify theme variables
2. Edit `tailwindcss/tailwind.config.js` to add new theme elements
3. Rebuild the CSS:

```bash
cd tailwindcss
npm run css:build
```

The dark mode is activated by toggling a class on the html element and is automatically set based on user preference or system settings.

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

The application uses the pynput library to simulate keyboard input to whatever application is currently in focus on your system. When you click "Scan", the barcode is sent as keystrokes to the active application, followed by a return key press.

## Requirements

- Python 3.8+
- pynput library (for cross-platform keyboard control)
- FastAPI and related packages
- Node.js and npm (for Tailwind CSS)

## License

MIT
