from fastapi.templating import Jinja2Templates

# Browser configuration
BROWSER_NAME = "Google Chrome"  # Change to "Safari" or your browser if needed

# Server configuration
HOST = "0.0.0.0"
PORT = 5000

# Templates setup
templates = Jinja2Templates(directory="templates")
