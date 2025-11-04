Param(
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Set-Location $scriptDir

Write-Host "Building barcode-xpress with PyInstaller..."

# Constrain PyInstaller cache/config inside the repository to avoid permission issues.
$pyiRoot = Join-Path $scriptDir ".pyinstaller"
$env:PYINSTALLER_CONFIG_DIR = Join-Path $pyiRoot "config"
$env:PYINSTALLER_CACHE_DIR = Join-Path $pyiRoot "cache"
New-Item -ItemType Directory -Force -Path $env:PYINSTALLER_CONFIG_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $env:PYINSTALLER_CACHE_DIR | Out-Null

# Clean previous build artifacts for a fresh build.
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $scriptDir "build/barcode-xpress")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $scriptDir "dist/barcode-xpress")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $scriptDir "dist/barcode-xpress.app")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $scriptDir "dist/barcode-xpress.exe")

$iconDir = Join-Path $scriptDir "assets/icons"
$windowsIcon = Join-Path $iconDir "barcode-xpress.ico"

if (-not $env:VIRTUAL_ENV -and (Test-Path ".venv/Scripts/Activate.ps1")) {
    Write-Host "Activating virtual environment..."
    . ".venv/Scripts/Activate.ps1"
}

if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    throw "PyInstaller is not installed. Run 'pip install pyinstaller' in this environment."
}

$iconArgs = @()
if (Test-Path $windowsIcon) {
    $iconArgs = @("--icon", $windowsIcon)
} else {
    Write-Warning "Windows icon not found at $windowsIcon. Using default PyInstaller icon."
}

$arguments = @(
    "--noconsole", "--onefile",
    "--name", "barcode-xpress",
    "--add-data", "templates;templates",
    "--add-data", "static;static"
)

if ($iconArgs.Count -gt 0) {
    $arguments += $iconArgs
}

$arguments += "app/main.py"

if ($Clean.IsPresent) {
    $arguments = @("--clean") + $arguments
}

pyinstaller @arguments

Write-Host "Build complete. The executable can be found at 'dist\barcode-xpress.exe'."
