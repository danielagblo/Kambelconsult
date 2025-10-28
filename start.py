#!/usr/bin/env python3
"""
Single entry point to start the Kambel Consult application
Everything runs on port 8000 - both website and admin panel
"""
import os
import sys
import subprocess

def main():
    print("=" * 60)
    print("🚀 Kambel Consult - Starting Application")
    print("=" * 60)
    print("📍 Website: http://localhost:8000")
    print("📍 Admin Panel: http://localhost:8000/admin")
    print("=" * 60)
    print("")
    
    # Change to django_admin directory
    os.chdir('django_admin')
    
    # Start Django development server
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'], check=True)
    except KeyboardInterrupt:
        print("\n\nStopping server...")
    except Exception as e:
        print(f"\nError: {e}")
        print("\nMake sure you've run: bash setup.sh")
        sys.exit(1)

if __name__ == '__main__':
    main()

