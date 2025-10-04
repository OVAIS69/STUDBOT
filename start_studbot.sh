#!/bin/bash

# StudBot Startup Script for Linux/Mac
# Make sure to run: chmod +x start_studbot.sh

echo ""
echo "================================================"
echo "    STUDBOT - AI Learning Companion"
echo "================================================"
echo ""
echo "Starting StudBot application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ and try again"
    echo ""
    exit 1
fi

# Check if required files exist
if [ ! -f "app.py" ]; then
    echo "ERROR: app.py not found"
    echo "Please make sure you're in the correct directory"
    echo ""
    exit 1
fi

if [ ! -f "index.html" ]; then
    echo "ERROR: index.html not found"
    echo "Please make sure you're in the correct directory"
    echo ""
    exit 1
fi

# Install requirements if needed
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip3 install -r requirements.txt
    echo ""
fi

# Start the application
echo "Starting StudBot server..."
echo "The application will open in your default browser."
echo "Press Ctrl+C to stop the server."
echo ""
echo "================================================"
echo ""

python3 start.py

echo ""
echo "StudBot has been stopped."
echo "Thank you for using StudBot!"
echo ""
