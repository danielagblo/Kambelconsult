#!/usr/bin/env python3
"""
Install and test the Kambel Consult Backend
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main installation function"""
    print("=" * 60)
    print("🚀 Kambel Consult Backend Installation")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found. Please run this script from the project root.")
        sys.exit(1)
    
    # Install Python dependencies
    print("\n📦 Installing Python dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies. Please check your Python environment.")
        sys.exit(1)
    
    # Test backend import
    print("\n🧪 Testing backend imports...")
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        from backend import create_app, db
        from backend.models import User, Category, Book
        print("✅ Backend imports successful")
    except ImportError as e:
        print(f"❌ Backend import failed: {e}")
        print("Please check that all dependencies are installed correctly.")
        sys.exit(1)
    
    print("\n🎉 Backend installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the backend server: python backend/app.py")
    print("2. Access admin panel: http://localhost:5000/admin")
    print("3. Login credentials: admin / admin123")
    print("4. API endpoints: http://localhost:5000/api/")
    print("\n🌐 Your frontend website will continue to work at: http://localhost:5001")
    print("=" * 60)

if __name__ == '__main__':
    main()
