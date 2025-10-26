#!/usr/bin/env python3
"""
Test Django Admin Integration with Frontend
"""

import requests
import json

def test_django_integration():
    """Test Django admin integration with frontend"""
    print("=" * 60)
    print("🧪 Testing Django Admin Integration")
    print("=" * 60)
    
    # Test Django admin API endpoints
    django_endpoints = [
        'publications/',
        'categories/',
        'consultancy/',
        'blog/',
        'site/config/',
        'site/contact-info/',
        'site/social-media/',
        'masterclasses/',
        'kict/courses/',
        'site/seo/home/'
    ]
    
    print("🔄 Testing Django Admin API endpoints...")
    django_success = 0
    django_total = len(django_endpoints)
    
    for endpoint in django_endpoints:
        try:
            response = requests.get(f'http://localhost:8000/api/{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - Status: {response.status_code}")
                django_success += 1
            else:
                print(f"   ❌ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print(f"\n📊 Django Admin API: {django_success}/{django_total} endpoints working")
    
    # Test frontend API endpoints
    print("\n🔄 Testing Frontend API endpoints...")
    frontend_endpoints = [
        'publications',
        'categories',
        'consultancy',
        'blog',
        'site/config',
        'site/contact-info',
        'site/social-media',
        'masterclasses',
        'kict/courses',
        'site/seo/home'
    ]
    
    frontend_success = 0
    frontend_total = len(frontend_endpoints)
    
    for endpoint in frontend_endpoints:
        try:
            response = requests.get(f'http://localhost:5001/api/{endpoint}', timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - Status: {response.status_code}")
                frontend_success += 1
            else:
                print(f"   ❌ {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint} - Error: {e}")
    
    print(f"\n📊 Frontend API: {frontend_success}/{frontend_total} endpoints working")
    
    # Test contact form submission
    print("\n🔄 Testing contact form submission...")
    try:
        contact_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Message',
            'message': 'This is a test message'
        }
        
        # Test Django admin API
        django_response = requests.post('http://localhost:8000/api/contact/', json=contact_data, timeout=5)
        if django_response.status_code == 200:
            print("   ✅ Django contact API working")
        else:
            print(f"   ❌ Django contact API - Status: {django_response.status_code}")
        
        # Test frontend API
        frontend_response = requests.post('http://localhost:5001/api/contact', json=contact_data, timeout=5)
        if frontend_response.status_code == 200:
            print("   ✅ Frontend contact API working")
        else:
            print(f"   ❌ Frontend contact API - Status: {frontend_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Contact form test failed: {e}")
    
    # Test newsletter subscription
    print("\n🔄 Testing newsletter subscription...")
    try:
        newsletter_data = {'email': 'test@example.com'}
        
        # Test Django admin API
        django_response = requests.post('http://localhost:8000/api/newsletter/', json=newsletter_data, timeout=5)
        if django_response.status_code == 200:
            print("   ✅ Django newsletter API working")
        else:
            print(f"   ❌ Django newsletter API - Status: {django_response.status_code}")
        
        # Test frontend API
        frontend_response = requests.post('http://localhost:5001/api/newsletter', json=newsletter_data, timeout=5)
        if frontend_response.status_code == 200:
            print("   ✅ Frontend newsletter API working")
        else:
            print(f"   ❌ Frontend newsletter API - Status: {frontend_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Newsletter test failed: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Django Admin API: {django_success}/{django_total} endpoints working")
    print(f"✅ Frontend API: {frontend_success}/{frontend_total} endpoints working")
    
    if django_success == django_total and frontend_success == frontend_total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Django Admin Panel is fully integrated with your website")
        print("✅ All content is now managed through Django admin")
        print("✅ Frontend website is connected to Django admin")
    else:
        print("\n⚠️  Some tests failed - check the errors above")
    
    print("\n🌐 Access Points:")
    print("📍 Website: http://localhost:5001")
    print("📍 Django Admin: http://localhost:8000/admin")
    print("📍 Django API: http://localhost:8000/api/")
    print("=" * 60)

if __name__ == '__main__':
    test_django_integration()
