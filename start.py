"""
StudBot Startup Script
Simple script to start the StudBot application
"""

import os
import sys
import webbrowser
import time
import threading
from flask import Flask

def start_flask_app():
    """Start the Flask application"""
    try:
        from app import app
        print("Starting StudBot Flask server...")
        app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
    except ImportError:
        print("Error: Flask app not found. Make sure app.py exists.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        sys.exit(1)

def open_browser():
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

def main():
    """Main startup function"""
    print("=" * 50)
    print("🤖 STUDBOT - AI Learning Companion")
    print("=" * 50)
    print()
    print("Starting the application...")
    print("This will start a local web server.")
    print("The application will open in your default browser.")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    print()
    
    # Check if required files exist
    required_files = ['app.py', 'index.html', 'styles.css', 'script.js']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Error: Missing required files: {', '.join(missing_files)}")
        print("Please make sure all files are in the current directory.")
        sys.exit(1)
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app
    try:
        start_flask_app()
    except KeyboardInterrupt:
        print("\n\nShutting down StudBot...")
        print("Thank you for using StudBot!")
        sys.exit(0)

if __name__ == "__main__":
    main()
