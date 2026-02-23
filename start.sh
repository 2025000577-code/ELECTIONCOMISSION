#!/bin/bash

echo ""
echo "========================================"
echo "  Django Online Voting System - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not available"
    echo "Please ensure pip is installed with Python"
    exit 1
fi

echo "Installing required packages..."
python3 install_dependencies.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Installation failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "Starting Django voting system with SQLite..."
echo "No MySQL setup required!"
echo ""

# Run the simple setup script
python3 run_simple.py