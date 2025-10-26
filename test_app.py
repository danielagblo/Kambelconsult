#!/usr/bin/env python3
"""
Test script for Kambel Consult Website
This script tests the basic functionality of the Flask application.
"""

import requests
import json
import time
import subprocess
import sys
import os
from threading import Thread

def test_api_endpoints():
    """Test all API endpoints"""
    base_url = "http://localhost:5000"
    
    print("Testing API endpoints...")
    
    # Test blog endpoints
    try:
        response = requests.get(f"{base_url}/api/blog")
        assert response.status_code == 200
        print("✓ Blog posts endpoint working")
    except Exception as e:
        print(f"✗ Blog posts endpoint failed: {e}")
    
    # Test publications endpoints
    try:
        response = requests.get(f"{base_url}/api/publications")
        assert response.status_code == 200
        print("✓ Publications endpoint working")
    except Exception as e:
        print(f"✗ Publications endpoint failed: {e}")
    
    # Test masterclasses endpoints
    try:
        response = requests.get(f"{base_url}/api/masterclasses")
        assert response.status_code == 200
        print("✓ Masterclasses endpoint working")
    except Exception as e:
        print(f"✗ Masterclasses endpoint failed: {e}")
    
    # Test KICT courses endpoint
    try:
        response = requests.get(f"{base_url}/api/kict/courses")
        assert response.status_code == 200
        print("✓ KICT courses endpoint working")
    except Exception as e:
        print(f"✗ KICT courses endpoint failed: {e}")
    
    # Test contact form
    try:
        contact_data = {
            "name": "Test User",
            "email": "test@example.com",
            "subject": "Test Subject",
            "message": "Test message"
        }
        response = requests.post(f"{base_url}/api/contact", json=contact_data)
        assert response.status_code == 200
        print("✓ Contact form endpoint working")
    except Exception as e:
        print(f"✗ Contact form endpoint failed: {e}")
    
    # Test newsletter subscription
    try:
        newsletter_data = {"email": "test@example.com"}
        response = requests.post(f"{base_url}/api/newsletter", json=newsletter_data)
        assert response.status_code == 200
        print("✓ Newsletter subscription endpoint working")
    except Exception as e:
        print(f"✗ Newsletter subscription endpoint failed: {e}")

def test_main_page():
    """Test if the main page loads"""
    try:
        response = requests.get("http://localhost:5000/")
        assert response.status_code == 200
        assert "Kambel Consult" in response.text
        print("✓ Main page loads correctly")
    except Exception as e:
        print(f"✗ Main page failed to load: {e}")

def start_server():
    """Start the Flask server in a separate thread"""
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    """Main test function"""
    print("=" * 50)
    print("Kambel Consult Website - Test Suite")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ['app.py', 'index.html', 'requirements.txt']
    for file in required_files:
        if not os.path.exists(file):
            print(f"✗ Required file missing: {file}")
            sys.exit(1)
        else:
            print(f"✓ Found: {file}")
    
    print("\nStarting Flask server...")
    
    # Start server in background thread
    server_thread = Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    print("\nRunning tests...")
    
    # Test main page
    test_main_page()
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)
    print("\nTo run the website manually:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the server: python run.py")
    print("3. Open browser: http://localhost:5000")

if __name__ == '__main__':
    main()
