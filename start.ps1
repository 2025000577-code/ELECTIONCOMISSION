# PowerShell script for Django Online Voting System
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Django Online Voting System - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if pip is available
try {
    $pipVersion = pip --version 2>&1
    Write-Host "pip found: $pipVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: pip is not available" -ForegroundColor Red
    Write-Host "Please ensure pip is installed with Python" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Installing required packages..." -ForegroundColor Yellow
try {
    python install_dependencies.py
    if ($LASTEXITCODE -ne 0) {
        throw "Installation failed"
    }
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Installation failed. Please check the error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Starting Django voting system with SQLite..." -ForegroundColor Green
Write-Host "No MySQL setup required!" -ForegroundColor Cyan
Write-Host ""

# Run the simple setup script
try {
    python run_simple.py
} catch {
    Write-Host "Failed to start the application" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit"