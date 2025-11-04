#!/bin/bash

# Exit immediately on failure and ensure unset variables cause errors.
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "Building barcode-xpress with PyInstaller..."

ICON_DIR="${ROOT_DIR}/assets/icons"
MAC_ICON="${ICON_DIR}/barcode-xpress.icns"
WIN_ICON="${ICON_DIR}/barcode-xpress.ico"
LINUX_ICON="${ICON_DIR}/barcode-xpress.png"

# Constrain PyInstaller cache/config inside the repository to avoid permission issues.
export PYINSTALLER_CONFIG_DIR="${ROOT_DIR}/.pyinstaller/config"
export PYINSTALLER_CACHE_DIR="${ROOT_DIR}/.pyinstaller/cache"
mkdir -p "${PYINSTALLER_CONFIG_DIR}" "${PYINSTALLER_CACHE_DIR}"

# Clean previous build artifacts for a fresh build.
rm -rf "${ROOT_DIR}/build/barcode-xpress" \
       "${ROOT_DIR}/dist/barcode-xpress" \
       "${ROOT_DIR}/dist/barcode-xpress.app" \
       "${ROOT_DIR}/dist/barcode-xpress.exe"

# Ensure the virtual environment is activated (if not already)
if [ -z "${VIRTUAL_ENV:-}" ] && [ -f ".venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    # shellcheck disable=SC1091
    source .venv/bin/activate
fi

if ! command -v pyinstaller >/dev/null 2>&1; then
    echo "PyInstaller is not installed in the current environment."
    echo "Install it with 'pip install pyinstaller' and re-run this script."
    exit 1
fi

PLATFORM="$(uname -s)"
OUTPUT_PATH=""

case "$PLATFORM" in
    Darwin)
        echo "Detected macOS. Using PyInstaller spec for .app bundle."
        if [ ! -f "${MAC_ICON}" ]; then
            echo "Warning: macOS icon not found at ${MAC_ICON}. Using default PyInstaller icon."
        fi
        pyinstaller --clean barcode-xpress.spec
        OUTPUT_PATH="dist/barcode-xpress.app"
        ;;
    Linux)
        echo "Detected Linux. Building standalone executable."
        pyinstaller --clean --noconsole --onefile \
            --name "barcode-xpress" \
            --add-data "templates:templates" \
            --add-data "static:static" \
            ${LINUX_ICON:+--icon "${LINUX_ICON}"} \
            app/main.py
        OUTPUT_PATH="dist/barcode-xpress"
        ;;
    CYGWIN*|MINGW*|MSYS*|Windows_NT)
        echo "Detected Windows environment. Building standalone executable."
        if [ ! -f "${WIN_ICON}" ]; then
            echo "Warning: Windows icon not found at ${WIN_ICON}. Using default PyInstaller icon."
        fi
        pyinstaller --clean --noconsole --onefile \
            --name "barcode-xpress" \
            --add-data "templates;templates" \
            --add-data "static;static" \
            ${WIN_ICON:+--icon "${WIN_ICON}"} \
            app/main.py
        OUTPUT_PATH="dist/barcode-xpress.exe"
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

echo "Build complete. The executable can be found at '${OUTPUT_PATH}'."
