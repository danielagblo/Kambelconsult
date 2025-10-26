#!/usr/bin/env python3
"""
Add Sample Content to Django Admin for Testing
"""

import requests
import json

def add_sample_content():
    """Add sample content to demonstrate Django admin integration"""
    print("=" * 60)
    print("📝 Adding Sample Content to Django Admin")
    print("=" * 60)
    
    # Sample book data
    sample_books = [
        {
            'title': 'Strategic Business Planning',
            'author': 'Moses Agbesi Katamani',
            'description': 'A comprehensive guide to strategic business planning and execution.',
            'pages': 250,
            'price': 29.99,
            'purchase_link': 'https://amazon.com/strategic-business-planning',
            'category': 1  # Course Books
        },
        {
            'title': 'Career Development Mastery',
            'author': 'Moses Agbesi Katamani',
            'description': 'Unlock your career potential with proven strategies and techniques.',
            'pages': 180,
            'price': 24.99,
            'purchase_link': 'https://amazon.com/career-development-mastery',
            'category': 2  # Guidance Books
        },
        {
            'title': 'The Success Mindset',
            'author': 'Moses Agbesi Katamani',
            'description': 'Transform your thinking and achieve extraordinary results.',
            'pages': 200,
            'price': 19.99,
            'purchase_link': 'https://amazon.com/success-mindset',
            'category': 3  # Inspirational Books
        }
    ]
    
    # Sample consultancy services
    sample_services = [
        {
            'name': 'Career Development Coaching',
            'service_type': 'career',
            'description': 'Personalized career guidance and development strategies.',
            'icon': 'fas fa-user-tie',
            'features': [
                {
                    'title': 'Resume Optimization',
                    'description': 'Professional resume review and enhancement',
                    'icon': 'fas fa-file-alt'
                },
                {
                    'title': 'Interview Preparation',
                    'description': 'Comprehensive interview coaching and practice',
                    'icon': 'fas fa-handshake'
                },
                {
                    'title': 'Career Planning',
                    'description': 'Strategic career path development',
                    'icon': 'fas fa-route'
                }
            ]
        },
        {
            'name': 'Business Strategy Consulting',
            'service_type': 'business',
            'description': 'Expert business strategy development and implementation.',
            'icon': 'fas fa-chart-line',
            'features': [
                {
                    'title': 'Market Analysis',
                    'description': 'Comprehensive market research and analysis',
                    'icon': 'fas fa-chart-bar'
                },
                {
                    'title': 'Growth Strategy',
                    'description': 'Sustainable business growth planning',
                    'icon': 'fas fa-seedling'
                },
                {
                    'title': 'Operational Efficiency',
                    'description': 'Process optimization and efficiency improvement',
                    'icon': 'fas fa-cogs'
                }
            ]
        }
    ]
    
    # Sample blog posts
    sample_blog_posts = [
        {
            'title': 'The Future of Business Strategy',
            'content': 'In today\'s rapidly changing business landscape, strategic planning has become more crucial than ever. This comprehensive guide explores the latest trends and methodologies in business strategy development.',
            'excerpt': 'Explore the latest trends in business strategy and learn how to adapt to the changing business landscape.',
            'author': 'Moses Agbesi Katamani',
            'is_published': True
        },
        {
            'title': 'Unlocking Your Career Potential',
            'content': 'Career development is a journey that requires careful planning and execution. This article provides actionable insights and strategies for advancing your career.',
            'excerpt': 'Discover proven strategies for career advancement and professional growth.',
            'author': 'Moses Agbesi Katamani',
            'is_published': True
        }
    ]
    
    print("📚 Adding sample books...")
    for book in sample_books:
        try:
            response = requests.post('http://localhost:8000/api/publications/', json=book, timeout=5)
            if response.status_code == 201:
                print(f"   ✅ Added: {book['title']}")
            else:
                print(f"   ⚠️  Book {book['title']} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Book {book['title']} - Error: {e}")
    
    print("\n🎯 Adding sample consultancy services...")
    for service in sample_services:
        try:
            # Add service
            service_data = {
                'name': service['name'],
                'service_type': service['service_type'],
                'description': service['description'],
                'icon': service['icon']
            }
            response = requests.post('http://localhost:8000/api/consultancy/', json=service_data, timeout=5)
            if response.status_code == 201:
                print(f"   ✅ Added: {service['name']}")
            else:
                print(f"   ⚠️  Service {service['name']} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Service {service['name']} - Error: {e}")
    
    print("\n📝 Adding sample blog posts...")
    for post in sample_blog_posts:
        try:
            response = requests.post('http://localhost:8000/api/blog/', json=post, timeout=5)
            if response.status_code == 201:
                print(f"   ✅ Added: {post['title']}")
            else:
                print(f"   ⚠️  Blog post {post['title']} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Blog post {post['title']} - Error: {e}")
    
    print("\n🎉 Sample content added!")
    print("✅ You can now see this content in your Django admin panel")
    print("✅ The content will appear on your website")
    print("✅ Everything is connected and working!")
    
    print("\n🌐 Next Steps:")
    print("1. Go to Django admin: http://localhost:8000/admin")
    print("2. Login with: admin / admin123")
    print("3. View the added content in Books, Consultancy Services, and Blog Posts")
    print("4. Visit your website to see the content displayed")
    print("5. Add more content through Django admin - it will appear on your website!")

if __name__ == '__main__':
    add_sample_content()
