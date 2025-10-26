#!/usr/bin/env python3
"""
Simple Flask Backend for Kambel Consult
This is a simplified version that focuses on core functionality
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
from datetime import datetime

# Create Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'kambel-consult-secret-key-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'publications'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'blog'), exist_ok=True)

# Data storage (in production, use a real database)
DATA_FILE = 'data/backend_data.json'

def load_data():
    """Load data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {
        'books': [],
        'categories': [
            {'id': 1, 'name': 'Course Books', 'description': 'Educational course materials'},
            {'id': 2, 'name': 'Guidance Books', 'description': 'Personal and professional guidance'},
            {'id': 3, 'name': 'Inspirational Books', 'description': 'Motivational and inspirational content'},
            {'id': 4, 'name': 'Literature', 'description': 'Literary works and publications'}
        ],
        'consultancy_services': [
            {
                'id': 1,
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
                'id': 2,
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
                'id': 3,
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
                'id': 4,
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
        ],
        'blog_posts': [
            {
                'id': 1,
                'title': 'Welcome to Kambel Consult',
                'content': 'Welcome to our professional consulting and training services. We are committed to helping individuals and organizations achieve their goals through expert guidance and support.',
                'excerpt': 'Welcome to our professional consulting and training services.',
                'author': 'Kambel Team',
                'date': 'January 15, 2024',
                'is_published': True
            },
            {
                'id': 2,
                'title': 'The Importance of Professional Development',
                'content': 'Professional development is crucial for career growth and personal success. In today\'s competitive world, continuous learning and skill development are essential for staying relevant and achieving your goals.',
                'excerpt': 'Professional development is crucial for career growth and personal success.',
                'author': 'Kambel Team',
                'date': 'January 20, 2024',
                'is_published': True
            }
        ],
        'contact_messages': [],
        'newsletter_subscriptions': [],
        'site_config': {
            'site_name': 'Kambel Consult',
            'tagline': 'Professional Consulting and Training Services',
            'contact_email': 'info@kambelconsult.com',
            'contact_phone': '+1 (555) 123-4567',
            'address': '123 Business Street, City, State 12345'
        }
    }

def save_data(data):
    """Save data to JSON file"""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# API Routes

@app.route('/')
def home():
    """Home route"""
    return jsonify({
        'message': 'Kambel Consult Backend API',
        'version': '1.0.0',
        'endpoints': {
            'publications': '/api/publications/',
            'categories': '/api/categories/',
            'consultancy': '/api/consultancy/',
            'blog': '/api/blog/',
            'contact': '/api/contact/',
            'newsletter': '/api/newsletter/',
            'site_config': '/api/site/config/'
        }
    })

@app.route('/api/publications/', methods=['GET'])
def get_publications():
    """Get all publications"""
    data = load_data()
    return jsonify(data['books'])

@app.route('/api/publications/', methods=['POST'])
def create_publication():
    """Create new publication"""
    data = load_data()
    book_data = request.get_json()
    
    # Generate new ID
    new_id = max([book.get('id', 0) for book in data['books']], default=0) + 1
    
    book = {
        'id': new_id,
        'title': book_data.get('title', ''),
        'author': book_data.get('author', 'Moses Agbesi Katamani'),
        'description': book_data.get('description', ''),
        'pages': book_data.get('pages', 0),
        'price': book_data.get('price', 0),
        'cover_image_url': book_data.get('cover_image_url'),
        'purchase_link': book_data.get('purchase_link'),
        'category': book_data.get('category', 'General'),
        'created_at': datetime.now().isoformat()
    }
    
    data['books'].append(book)
    save_data(data)
    
    return jsonify({'message': 'Publication created successfully', 'id': new_id}), 201

@app.route('/api/categories/', methods=['GET'])
def get_categories():
    """Get all categories"""
    data = load_data()
    return jsonify(data['categories'])

@app.route('/api/consultancy/', methods=['GET'])
def get_consultancy_services():
    """Get all consultancy services"""
    data = load_data()
    return jsonify(data['consultancy_services'])

@app.route('/api/blog/', methods=['GET'])
def get_blog_posts():
    """Get all blog posts"""
    data = load_data()
    published_posts = [post for post in data['blog_posts'] if post.get('is_published', True)]
    return jsonify(published_posts)

@app.route('/api/contact/', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    data = load_data()
    contact_data = request.get_json()
    
    # Generate new ID
    new_id = max([msg.get('id', 0) for msg in data['contact_messages']], default=0) + 1
    
    message = {
        'id': new_id,
        'name': contact_data.get('name', ''),
        'email': contact_data.get('email', ''),
        'subject': contact_data.get('subject', ''),
        'message': contact_data.get('message', ''),
        'is_read': False,
        'created_at': datetime.now().isoformat()
    }
    
    data['contact_messages'].append(message)
    save_data(data)
    
    return jsonify({'message': 'Contact message submitted successfully'})

@app.route('/api/newsletter/', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    data = load_data()
    newsletter_data = request.get_json()
    email = newsletter_data.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if email already exists
    existing = next((sub for sub in data['newsletter_subscriptions'] if sub['email'] == email), None)
    if existing:
        if existing.get('is_active', True):
            return jsonify({'message': 'Email is already subscribed'})
        else:
            existing['is_active'] = True
            save_data(data)
            return jsonify({'message': 'Email resubscribed successfully'})
    
    # Generate new ID
    new_id = max([sub.get('id', 0) for sub in data['newsletter_subscriptions']], default=0) + 1
    
    subscription = {
        'id': new_id,
        'email': email,
        'is_active': True,
        'subscribed_at': datetime.now().isoformat()
    }
    
    data['newsletter_subscriptions'].append(subscription)
    save_data(data)
    
    return jsonify({'message': 'Successfully subscribed to newsletter'})

@app.route('/api/site/config/', methods=['GET'])
def get_site_config():
    """Get site configuration"""
    data = load_data()
    return jsonify(data['site_config'])

@app.route('/api/site/contact-info/', methods=['GET'])
def get_contact_info():
    """Get contact information"""
    data = load_data()
    config = data['site_config']
    return jsonify([
        {'type': 'email', 'value': config.get('contact_email', ''), 'icon': 'fas fa-envelope'},
        {'type': 'phone', 'value': config.get('contact_phone', ''), 'icon': 'fas fa-phone'},
        {'type': 'address', 'value': config.get('address', ''), 'icon': 'fas fa-map-marker-alt'}
    ])

@app.route('/api/site/social-media/', methods=['GET'])
def get_social_media():
    """Get social media links"""
    return jsonify([
        {'platform': 'facebook', 'url': 'https://facebook.com/kambelconsult', 'icon': 'fab fa-facebook'},
        {'platform': 'twitter', 'url': 'https://twitter.com/kambelconsult', 'icon': 'fab fa-twitter'},
        {'platform': 'linkedin', 'url': 'https://linkedin.com/company/kambelconsult', 'icon': 'fab fa-linkedin'},
        {'platform': 'instagram', 'url': 'https://instagram.com/kambelconsult', 'icon': 'fab fa-instagram'}
    ])

@app.route('/api/site/about', methods=['GET'])
@app.route('/api/site/about/', methods=['GET'])
def get_about_config():
    """Get about page configuration from Django API"""
    try:
        import requests
        response = requests.get('http://localhost:8000/api/site/about/', timeout=5)
        if response.status_code == 200:
            return jsonify(response.json())
    except Exception as e:
        print(f"Error fetching about config: {e}")
    
    # Return default values if API fails
    return jsonify({
        'hero_years': '15+',
        'hero_clients': '500+',
        'hero_publications': '50+',
        'hero_speaking': '100+',
        'profile_name': 'Moses Agbesi Katamani',
        'profile_title': 'Founder & CEO, Kambel Consult',
        'profile_picture_url': None,
        'bio_summary': 'A visionary leader and expert consultant with over 15 years of experience in education, career development, and business advisory services.',
        'tags': ['Education Expert', 'Career Coach', 'Business Advisor', 'Author', 'Speaker'],
        'philosophy_quote': 'Education is the foundation of all progress. Through knowledge, guidance, and strategic thinking, we can unlock the potential within every individual and organization.',
        'cta_title': 'Ready to Work Together?',
        'cta_description': "Let's discuss how I can help you achieve your goals and unlock your potential.",
        'journey': [],
        'education': [],
        'achievements': [],
        'speaking': []
    })

# Admin Panel Routes (Simple HTML interface)
@app.route('/admin')
def admin_panel():
    """Simple admin panel"""
    data = load_data()
    
    stats = {
        'total_books': len(data['books']),
        'total_blog_posts': len(data['blog_posts']),
        'unread_messages': len([msg for msg in data['contact_messages'] if not msg.get('is_read', False)]),
        'newsletter_subscribers': len([sub for sub in data['newsletter_subscriptions'] if sub.get('is_active', True)])
    }
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kambel Consult Admin</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{ background: #f8f9fa; }}
            .stat-card {{ background: white; border-radius: 15px; padding: 2rem; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            .stat-number {{ font-size: 2.5rem; font-weight: 700; color: #10b981; }}
        </style>
    </head>
    <body>
        <div class="container mt-5">
            <div class="row">
                <div class="col-12">
                    <h1 class="text-center mb-5">
                        <i class="fas fa-tachometer-alt me-3"></i>
                        Kambel Consult Admin Panel
                    </h1>
                </div>
            </div>
            
            <div class="row">
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <i class="fas fa-book fa-3x text-primary mb-3"></i>
                        <div class="stat-number">{stats['total_books']}</div>
                        <div class="text-muted">Total Books</div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <i class="fas fa-blog fa-3x text-success mb-3"></i>
                        <div class="stat-number">{stats['total_blog_posts']}</div>
                        <div class="text-muted">Blog Posts</div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <i class="fas fa-envelope fa-3x text-warning mb-3"></i>
                        <div class="stat-number">{stats['unread_messages']}</div>
                        <div class="text-muted">Unread Messages</div>
                    </div>
                </div>
                <div class="col-md-3 mb-4">
                    <div class="stat-card text-center">
                        <i class="fas fa-users fa-3x text-info mb-3"></i>
                        <div class="stat-number">{stats['newsletter_subscribers']}</div>
                        <div class="text-muted">Newsletter Subscribers</div>
                    </div>
                </div>
            </div>
            
            <div class="row">
                <div class="col-12">
                    <div class="card">
                        <div class="card-header">
                            <h5><i class="fas fa-cog me-2"></i>Quick Actions</h5>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-3 mb-3">
                                    <a href="/api/publications/" class="btn btn-outline-primary w-100">
                                        <i class="fas fa-book me-2"></i>View Publications
                                    </a>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <a href="/api/blog/" class="btn btn-outline-success w-100">
                                        <i class="fas fa-edit me-2"></i>View Blog Posts
                                    </a>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <a href="/api/consultancy/" class="btn btn-outline-warning w-100">
                                        <i class="fas fa-briefcase me-2"></i>View Services
                                    </a>
                                </div>
                                <div class="col-md-3 mb-3">
                                    <a href="/api/site/config/" class="btn btn-outline-info w-100">
                                        <i class="fas fa-cog me-2"></i>Site Config
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Kambel Consult Backend Server")
    print("=" * 60)
    print("📍 Backend API: http://localhost:5000")
    print("📍 Admin Panel: http://localhost:5000/admin")
    print("📍 API Documentation: http://localhost:5000")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )
