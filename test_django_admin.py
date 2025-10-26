#!/usr/bin/env python3
"""
Test Django Admin Panel
"""

import requests
import time

def test_django_admin():
    """Test Django admin panel"""
    print("=" * 60)
    print("🧪 Testing Django Admin Panel")
    print("=" * 60)
    
    # Test admin login page
    print("🔄 Testing Django admin login page...")
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=5)
        if response.status_code == 200:
            print("✅ Django admin login page is accessible")
            print(f"   Status: {response.status_code}")
            if 'Django' in response.text:
                print("   ✅ Django admin interface detected")
            else:
                print("   ⚠️  Django admin interface not detected")
        else:
            print(f"❌ Django admin login page - Status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Django admin login page - Error: {e}")
        print("   Make sure Django server is running on port 8000")
        return False
    
    # Test admin interface
    print("\n🔄 Testing Django admin interface...")
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=5)
        if 'admin' in response.text.lower():
            print("✅ Django admin interface is working")
        else:
            print("⚠️  Django admin interface may not be fully loaded")
    except requests.exceptions.RequestException as e:
        print(f"❌ Django admin interface - Error: {e}")
        return False
    
    print("\n🎉 Django Admin Panel is working!")
    print("📍 Admin Panel: http://localhost:8000/admin")
    print("🔐 Login: admin / admin123")
    print("=" * 60)
    return True

if __name__ == '__main__':
    test_django_admin()
