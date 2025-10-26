from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
from .models import (
    db, Category, Book, ConsultancyService, ServiceFeature,
    BlogPost, ContactMessage, NewsletterSubscription, SiteConfig
)

api_bp = Blueprint('api', __name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(file, folder):
    """Save uploaded file"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid conflicts
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, filename)
        file.save(file_path)
        return filename
    return None

# Publications API
@api_bp.route('/publications/', methods=['GET'])
def get_publications():
    """Get all publications"""
    try:
        books = Book.query.filter_by(is_active=True).all()
        publications = []
        
        for book in books:
            publication = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'pages': book.pages,
                'price': float(book.price),
                'cover_image_url': book.cover_image_url,
                'purchase_link': book.purchase_link,
                'category': book.category.name if book.category else None
            }
            publications.append(publication)
        
        return jsonify(publications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/publications/', methods=['POST'])
def create_publication():
    """Create new publication"""
    try:
        data = request.get_json()
        
        book = Book(
            title=data.get('title'),
            author=data.get('author', 'Moses Agbesi Katamani'),
            description=data.get('description'),
            pages=data.get('pages', 0),
            price=data.get('price', 0),
            purchase_link=data.get('purchase_link'),
            category_id=data.get('category_id')
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify({'message': 'Publication created successfully', 'id': book.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/publications/<int:book_id>/', methods=['PUT'])
def update_publication(book_id):
    """Update publication"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.description = data.get('description', book.description)
        book.pages = data.get('pages', book.pages)
        book.price = data.get('price', book.price)
        book.purchase_link = data.get('purchase_link', book.purchase_link)
        book.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Publication updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@api_bp.route('/publications/<int:book_id>/', methods=['DELETE'])
def delete_publication(book_id):
    """Delete publication"""
    try:
        book = Book.query.get_or_404(book_id)
        book.is_active = False
        db.session.commit()
        
        return jsonify({'message': 'Publication deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Categories API
@api_bp.route('/categories/', methods=['GET'])
def get_categories():
    """Get all categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify([{
            'id': cat.id,
            'name': cat.name,
            'description': cat.description
        } for cat in categories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Consultancy API
@api_bp.route('/consultancy/', methods=['GET'])
def get_consultancy_services():
    """Get all consultancy services"""
    try:
        services = ConsultancyService.query.filter_by(is_active=True).order_by(ConsultancyService.order).all()
        consultancy_data = []
        
        for service in services:
            service_data = {
                'id': service.id,
                'name': service.name,
                'service_type': service.service_type,
                'description': service.description,
                'icon': service.icon,
                'features': []
            }
            
            for feature in service.features:
                if feature.is_active:
                    service_data['features'].append({
                        'id': feature.id,
                        'title': feature.title,
                        'description': feature.description,
                        'icon': feature.icon
                    })
            
            consultancy_data.append(service_data)
        
        return jsonify(consultancy_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Blog API
@api_bp.route('/blog/', methods=['GET'])
def get_blog_posts():
    """Get all blog posts"""
    try:
        posts = BlogPost.query.filter_by(is_published=True).order_by(BlogPost.created_at.desc()).all()
        blog_data = []
        
        for post in posts:
            blog_data.append({
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'excerpt': post.excerpt,
                'author': post.author,
                'date': post.date,
                'cover_image_url': post.cover_image_url
            })
        
        return jsonify(blog_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Contact API
@api_bp.route('/contact/', methods=['POST'])
def submit_contact():
    """Submit contact form"""
    try:
        data = request.get_json()
        
        contact = ContactMessage(
            name=data.get('name'),
            email=data.get('email'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        
        db.session.add(contact)
        db.session.commit()
        
        return jsonify({'message': 'Contact message submitted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Newsletter API
@api_bp.route('/newsletter/', methods=['POST'])
def subscribe_newsletter():
    """Subscribe to newsletter"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Check if email already exists
        existing = NewsletterSubscription.query.filter_by(email=email).first()
        if existing:
            if existing.is_active:
                return jsonify({'message': 'Email is already subscribed'})
            else:
                existing.is_active = True
                db.session.commit()
                return jsonify({'message': 'Email resubscribed successfully'})
        
        subscription = NewsletterSubscription(email=email)
        db.session.add(subscription)
        db.session.commit()
        
        return jsonify({'message': 'Successfully subscribed to newsletter'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Site Configuration API
@api_bp.route('/site/config/', methods=['GET'])
def get_site_config():
    """Get site configuration"""
    try:
        config = SiteConfig.query.first()
        if not config:
            # Create default config
            config = SiteConfig()
            db.session.add(config)
            db.session.commit()
        
        return jsonify({
            'site_name': config.site_name,
            'tagline': config.tagline,
            'logo_url': config.logo_url,
            'favicon_url': config.favicon_url,
            'contact_email': config.contact_email,
            'contact_phone': config.contact_phone,
            'address': config.address
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# File Upload API
@api_bp.route('/upload/', methods=['POST'])
def upload_file():
    """Upload file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        folder = request.form.get('folder', 'uploads')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filename = save_file(file, folder)
        if filename:
            return jsonify({
                'message': 'File uploaded successfully',
                'filename': filename,
                'url': f'/uploads/{folder}/{filename}'
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
