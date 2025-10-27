#!/usr/bin/env python3
"""
Simple HTTP Server for Bus Tracking Web App
This script starts a local web server to serve the bus tracking application.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# Configuration
PORT = 8080
HOST = 'localhost'

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler to serve the web app with proper MIME types"""
    
    def end_headers(self):
        # Add CORS headers for local development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def guess_type(self, path):
        """Override to handle additional file types"""
        mimetype, encoding = super().guess_type(path)
        
        # Handle JavaScript modules
        if path.endswith('.js'):
            return 'application/javascript'
        elif path.endswith('.mjs'):
            return 'application/javascript'
        
        return mimetype, encoding

def check_files():
    """Check if required files exist"""
    required_files = [
        'index.html',
        'style.css',
        'script.js',
        'test_data_generator.html'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease ensure all web app files are in the current directory.")
        return False
    
    return True

def check_api_key():
    """Check if Google Maps API key is configured"""
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'YOUR_GOOGLE_MAPS_API_KEY' in content:
                print("⚠️  Warning: Google Maps API key not configured!")
                print("   Please replace 'YOUR_GOOGLE_MAPS_API_KEY' in index.html with your actual API key.")
                print("   The map will not work without a valid API key.\n")
                return False
    except Exception as e:
        print(f"Error checking API key: {e}")
    
    return True

def start_server():
    """Start the HTTP server"""
    try:
        # Change to the web app directory
        web_app_dir = Path(__file__).parent
        os.chdir(web_app_dir)
        
        print("🚌 Bus Tracking System - Local Web Server")
        print("=" * 50)
        
        # Check required files
        if not check_files():
            return
        
        # Check API key configuration
        api_key_ok = check_api_key()
        
        # Create server
        with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
            print(f"✅ Server starting on http://{HOST}:{PORT}")
            print(f"📁 Serving files from: {os.getcwd()}")
            print("\n📋 Available pages:")
            print(f"   🗺️  Main App: http://{HOST}:{PORT}/index.html")
            print(f"   🧪 Test Data: http://{HOST}:{PORT}/test_data_generator.html")
            
            if api_key_ok:
                print("\n🎯 Setup Status: ✅ Ready to use")
            else:
                print("\n🎯 Setup Status: ⚠️  Needs Google Maps API key")
            
            print("\n🔧 Instructions:")
            print("   1. Open the main app in your browser")
            print("   2. Use the test data generator to simulate buses")
            print("   3. Watch real-time tracking on the map")
            print("   4. Press Ctrl+C to stop the server")
            
            # Try to open browser automatically
            try:
                webbrowser.open(f'http://{HOST}:{PORT}/index.html')
                print(f"\n🌐 Opening browser automatically...")
            except Exception as e:
                print(f"\n🌐 Could not open browser automatically: {e}")
                print(f"   Please open http://{HOST}:{PORT}/index.html manually")
            
            print(f"\n🚀 Server running... Press Ctrl+C to stop")
            print("=" * 50)
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: Port {PORT} is already in use")
            print("   Try using a different port or stop the other server")
        else:
            print(f"❌ Error starting server: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    start_server()
