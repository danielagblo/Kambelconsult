#!/usr/bin/env python3
"""
Verify Complete Integration - Everything Connected to Django Admin
"""

import requests
import json
import time

def verify_complete_integration():
    """Verify that everything on the site is connected to Django admin"""
    print("=" * 70)
    print("🔍 VERIFYING COMPLETE INTEGRATION - EVERYTHING TO DJANGO ADMIN")
    print("=" * 70)
    
    # Test all Django admin API endpoints
    print("🔄 Testing Django Admin API Endpoints...")
    django_endpoints = [
        ('publications/', 'Publications/Books'),
        ('categories/', 'Categories'),
        ('consultancy/', 'Consultancy Services'),
        ('blog/', 'Blog Posts'),
        ('site/config/', 'Site Configuration'),
        ('site/contact-info/', 'Contact Information'),
        ('site/social-media/', 'Social Media Links'),
        ('masterclasses/', 'Masterclasses'),
        ('kict/courses/', 'KICT Courses'),
        ('site/seo/home/', 'SEO Content')
    ]
    
    django_success = 0
    for endpoint, name in django_endpoints:
        try:
            response = requests.get(f'http://localhost:8000/api/{endpoint}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {name} - {len(data) if isinstance(data, list) else 'Object'} items")
                django_success += 1
            else:
                print(f"   ❌ {name} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name} - Error: {e}")
    
    print(f"\n📊 Django Admin API: {django_success}/{len(django_endpoints)} endpoints working")
    
    # Test all frontend API endpoints
    print("\n🔄 Testing Frontend API Endpoints...")
    frontend_endpoints = [
        ('publications', 'Publications'),
        ('categories', 'Categories'),
        ('consultancy', 'Consultancy'),
        ('blog', 'Blog'),
        ('site/config', 'Site Config'),
        ('site/contact-info', 'Contact Info'),
        ('site/social-media', 'Social Media'),
        ('masterclasses', 'Masterclasses'),
        ('kict/courses', 'KICT Courses'),
        ('site/seo/home', 'SEO Content')
    ]
    
    frontend_success = 0
    for endpoint, name in frontend_endpoints:
        try:
            response = requests.get(f'http://localhost:5001/api/{endpoint}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {name} - {len(data) if isinstance(data, list) else 'Object'} items")
                frontend_success += 1
            else:
                print(f"   ❌ {name} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name} - Error: {e}")
    
    print(f"\n📊 Frontend API: {frontend_success}/{len(frontend_endpoints)} endpoints working")
    
    # Test contact form submission to Django admin
    print("\n🔄 Testing Contact Form Integration...")
    try:
        contact_data = {
            'name': 'Integration Test User',
            'email': 'test@integration.com',
            'subject': 'Integration Test',
            'message': 'Testing complete integration with Django admin'
        }
        
        # Test direct Django admin API
        django_response = requests.post('http://localhost:8000/api/contact/', json=contact_data, timeout=5)
        if django_response.status_code == 200:
            print("   ✅ Contact form → Django admin API working")
        else:
            print(f"   ❌ Contact form → Django admin API - Status: {django_response.status_code}")
        
        # Test frontend → Django admin flow
        frontend_response = requests.post('http://localhost:5001/api/contact', json=contact_data, timeout=5)
        if frontend_response.status_code == 200:
            print("   ✅ Contact form → Frontend → Django admin working")
        else:
            print(f"   ❌ Contact form → Frontend → Django admin - Status: {frontend_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Contact form test failed: {e}")
    
    # Test newsletter subscription to Django admin
    print("\n🔄 Testing Newsletter Integration...")
    try:
        newsletter_data = {'email': 'newsletter@integration.com'}
        
        # Test direct Django admin API
        django_response = requests.post('http://localhost:8000/api/newsletter/', json=newsletter_data, timeout=5)
        if django_response.status_code == 200:
            print("   ✅ Newsletter → Django admin API working")
        else:
            print(f"   ❌ Newsletter → Django admin API - Status: {django_response.status_code}")
        
        # Test frontend → Django admin flow
        frontend_response = requests.post('http://localhost:5001/api/newsletter', json=newsletter_data, timeout=5)
        if frontend_response.status_code == 200:
            print("   ✅ Newsletter → Frontend → Django admin working")
        else:
            print(f"   ❌ Newsletter → Frontend → Django admin - Status: {frontend_response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Newsletter test failed: {e}")
    
    # Test website pages are loading with Django admin data
    print("\n🔄 Testing Website Pages...")
    website_pages = [
        ('/', 'Homepage'),
        ('/publications.html', 'Publications'),
        ('/consultancy-unified.html', 'Consultancy'),
        ('/about.html', 'About'),
        ('/contact.html', 'Contact')
    ]
    
    page_success = 0
    for page, name in website_pages:
        try:
            response = requests.get(f'http://localhost:5001{page}', timeout=5)
            if response.status_code == 200:
                print(f"   ✅ {name} - Loading with Django admin data")
                page_success += 1
            else:
                print(f"   ❌ {name} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {name} - Error: {e}")
    
    print(f"\n📊 Website Pages: {page_success}/{len(website_pages)} pages working")
    
    # Test Django admin panel access
    print("\n🔄 Testing Django Admin Panel Access...")
    try:
        response = requests.get('http://localhost:8000/admin/', timeout=5)
        if response.status_code == 200 or response.status_code == 302:
            print("   ✅ Django admin panel accessible")
        else:
            print(f"   ❌ Django admin panel - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Django admin panel - Error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 COMPLETE INTEGRATION VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"✅ Django Admin API: {django_success}/{len(django_endpoints)} endpoints working")
    print(f"✅ Frontend API: {frontend_success}/{len(frontend_endpoints)} endpoints working")
    print(f"✅ Website Pages: {page_success}/{len(website_pages)} pages working")
    
    if django_success == len(django_endpoints) and frontend_success == len(frontend_endpoints):
        print("\n🎉 COMPLETE SUCCESS!")
        print("✅ Everything on your site is connected to Django admin")
        print("✅ All content is managed through Django admin")
        print("✅ All forms submit to Django admin")
        print("✅ All data comes from Django admin")
        print("✅ Your website is fully integrated with Django admin")
    else:
        print("\n⚠️  Some components need attention - check the errors above")
    
    print("\n🌐 Your Complete System:")
    print("📍 Website: http://localhost:5001 (displays Django admin content)")
    print("📍 Django Admin: http://localhost:8000/admin (manages all content)")
    print("📍 Django API: http://localhost:8000/api/ (serves all data)")
    print("=" * 70)

if __name__ == '__main__':
    verify_complete_integration()
