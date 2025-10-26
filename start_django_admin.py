#!/usr/bin/env python3
"""
Start Django Admin Panel for Kambel Consult
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start Django admin panel"""
    print("=" * 60)
    print("🚀 Starting Django Admin Panel for Kambel Consult")
    print("=" * 60)
    
    # Change to Django admin directory
    django_dir = Path(__file__).parent / 'django_admin'
    os.chdir(django_dir)
    
    # Install Django if not already installed
    print("📦 Installing Django dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True)
        print("✅ Django dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return
    
    # Run migrations
    print("📊 Running database migrations...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✅ Database migrations completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Migration failed: {e}")
        return
    
    # Create superuser if it doesn't exist
    print("👤 Setting up admin user...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@kambelconsult.com', 'admin123')
            print("✅ Admin user created (username: admin, password: admin123)")
        else:
            print("✅ Admin user already exists")
    except Exception as e:
        print(f"⚠️  Could not create admin user: {e}")
    
    # Create default data
    print("📝 Creating default data...")
    try:
        from kambel_admin.models import Category, SiteConfig
        
        # Create default categories
        categories = [
            {'name': 'Course Books', 'description': 'Educational course materials'},
            {'name': 'Guidance Books', 'description': 'Personal and professional guidance'},
            {'name': 'Inspirational Books', 'description': 'Motivational and inspirational content'},
            {'name': 'Literature', 'description': 'Literary works and publications'}
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                print(f"✅ Created category: {category.name}")
        
        # Create site configuration
        if not SiteConfig.objects.exists():
            SiteConfig.objects.create(
                site_name="Kambel Consult",
                tagline="Professional Consulting and Training Services",
                contact_email="info@kambelconsult.com",
                contact_phone="+1 (555) 123-4567",
                address="123 Business Street, City, State 12345"
            )
            print("✅ Created site configuration")
        
        print("✅ Default data created successfully")
        
    except Exception as e:
        print(f"⚠️  Could not create default data: {e}")
    
    print("\n🎉 Django Admin Panel is ready!")
    print("📍 Admin Panel: http://localhost:8000/admin")
    print("🔐 Login: admin / admin123")
    print("=" * 60)
    
    # Start Django development server
    print("🚀 Starting Django development server...")
    try:
        subprocess.run([sys.executable, 'manage.py', 'runserver', '8000'])
    except KeyboardInterrupt:
        print("\n👋 Django admin panel stopped.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    main()
