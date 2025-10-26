#!/usr/bin/env python3
"""
Kambel Consult Backend Application
Flask backend with admin panel and API endpoints
"""

import os
import sys
from flask import Flask, send_from_directory
from flask_login import login_user
from werkzeug.security import generate_password_hash

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from __init__ import create_app, db
from models import User, Category, Book, ConsultancyService, ServiceFeature, BlogPost, ContactMessage, NewsletterSubscription, SiteConfig

def create_default_data():
    """Create default data for the application"""
    try:
        # Create default admin user
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@kambelconsult.com',
                is_active=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("✅ Created admin user (username: admin, password: admin123)")
        
        # Create default categories
        categories_data = [
            {'name': 'Course Books', 'description': 'Educational course materials'},
            {'name': 'Guidance Books', 'description': 'Personal and professional guidance'},
            {'name': 'Inspirational Books', 'description': 'Motivational and inspirational content'},
            {'name': 'Literature', 'description': 'Literary works and publications'}
        ]
        
        for cat_data in categories_data:
            category = Category.query.filter_by(name=cat_data['name']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
        
        # Create default consultancy services
        services_data = [
            {
                'name': 'Career Development',
                'service_type': 'career',
                'description': 'Professional career guidance and development services',
                'icon': 'fas fa-briefcase',
                'features': [
                    {'title': 'Career Assessment', 'description': 'Comprehensive career evaluation', 'icon': 'fas fa-clipboard-check'},
                    {'title': 'Resume Building', 'description': 'Professional resume creation', 'icon': 'fas fa-file-alt'},
                    {'title': 'Interview Prep', 'description': 'Interview skills training', 'icon': 'fas fa-handshake'}
                ]
            },
            {
                'name': 'Business Consulting',
                'service_type': 'business',
                'description': 'Strategic business consulting and advisory services',
                'icon': 'fas fa-chart-line',
                'features': [
                    {'title': 'Strategic Planning', 'description': 'Business strategy development', 'icon': 'fas fa-chess'},
                    {'title': 'Market Analysis', 'description': 'Market research and analysis', 'icon': 'fas fa-search'},
                    {'title': 'Growth Strategy', 'description': 'Business growth planning', 'icon': 'fas fa-rocket'}
                ]
            },
            {
                'name': 'Personal Development',
                'service_type': 'personal',
                'description': 'Personal growth and development programs',
                'icon': 'fas fa-user-graduate',
                'features': [
                    {'title': 'Goal Setting', 'description': 'Personal goal achievement', 'icon': 'fas fa-bullseye'},
                    {'title': 'Time Management', 'description': 'Productivity and time optimization', 'icon': 'fas fa-clock'},
                    {'title': 'Leadership Skills', 'description': 'Leadership development', 'icon': 'fas fa-crown'}
                ]
            },
            {
                'name': 'Education & Training',
                'service_type': 'education',
                'description': 'Educational programs and training services',
                'icon': 'fas fa-graduation-cap',
                'features': [
                    {'title': 'Workshops', 'description': 'Interactive training workshops', 'icon': 'fas fa-chalkboard-teacher'},
                    {'title': 'Online Courses', 'description': 'Digital learning programs', 'icon': 'fas fa-laptop'},
                    {'title': 'Certification', 'description': 'Professional certification', 'icon': 'fas fa-certificate'}
                ]
            }
        ]
        
        for service_data in services_data:
            service = ConsultancyService.query.filter_by(name=service_data['name']).first()
            if not service:
                features_data = service_data.pop('features')
                service = ConsultancyService(**service_data)
                db.session.add(service)
                db.session.flush()  # Get the service ID
                
                # Add features
                for feature_data in features_data:
                    feature = ServiceFeature(service_id=service.id, **feature_data)
                    db.session.add(feature)
        
        # Create default site configuration
        site_config = SiteConfig.query.first()
        if not site_config:
            site_config = SiteConfig(
                site_name="Kambel Consult",
                tagline="Professional Consulting and Training Services",
                contact_email="info@kambelconsult.com",
                contact_phone="+1 (555) 123-4567",
                address="123 Business Street, City, State 12345"
            )
            db.session.add(site_config)
        
        # Create sample blog posts
        blog_posts_data = [
            {
                'title': 'Welcome to Kambel Consult',
                'content': 'Welcome to our professional consulting and training services. We are committed to helping individuals and organizations achieve their goals through expert guidance and support.',
                'excerpt': 'Welcome to our professional consulting and training services.',
                'author': 'Kambel Team',
                'is_published': True
            },
            {
                'title': 'The Importance of Professional Development',
                'content': 'Professional development is crucial for career growth and personal success. In today\'s competitive world, continuous learning and skill development are essential for staying relevant and achieving your goals.',
                'excerpt': 'Professional development is crucial for career growth and personal success.',
                'author': 'Kambel Team',
                'is_published': True
            }
        ]
        
        for post_data in blog_posts_data:
            post = BlogPost.query.filter_by(title=post_data['title']).first()
            if not post:
                post = BlogPost(**post_data)
                db.session.add(post)
        
        db.session.commit()
        print("✅ Default data created successfully")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating default data: {e}")

def main():
    """Main application entry point"""
    print("=" * 50)
    print("Kambel Consult Backend Server")
    print("=" * 50)
    
    # Create Flask app
    app = create_app()
    
    with app.app_context():
        # Create database tables
        print("📊 Creating database tables...")
        db.create_all()
        print("✅ Database tables created")
        
        # Create default data
        print("📝 Creating default data...")
        create_default_data()
        
        print("\n🚀 Starting Kambel Consult Backend Server...")
        print("📍 Backend API: http://localhost:5000")
        print("📍 Admin Panel: http://localhost:5000/admin")
        print("🔐 Admin Login: admin / admin123")
        print("=" * 50)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )

if __name__ == '__main__':
    main()
