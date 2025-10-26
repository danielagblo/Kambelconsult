from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for admin authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    """Category model for publications"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    books = db.relationship('Book', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Book(db.Model):
    """Book model for publications"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), default="Moses Agbesi Katamani")
    description = db.Column(db.Text)
    pages = db.Column(db.Integer, default=0)
    price = db.Column(db.Numeric(10, 2), default=0)
    cover_image = db.Column(db.String(255))
    purchase_link = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    
    @property
    def cover_image_url(self):
        """Get cover image URL"""
        if self.cover_image:
            return f"/uploads/publications/{self.cover_image}"
        return None
    
    def __repr__(self):
        return f'<Book {self.title}>'

class ConsultancyService(db.Model):
    """Consultancy service model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    features = db.relationship('ServiceFeature', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<ConsultancyService {self.name}>'

class ServiceFeature(db.Model):
    """Service feature model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key
    service_id = db.Column(db.Integer, db.ForeignKey('consultancy_service.id'), nullable=False)
    
    def __repr__(self):
        return f'<ServiceFeature {self.title}>'

class BlogPost(db.Model):
    """Blog post model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.Text)
    author = db.Column(db.String(100), default="Kambel Team")
    cover_image = db.Column(db.String(255))
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def cover_image_url(self):
        """Get cover image URL"""
        if self.cover_image:
            return f"/uploads/blog/{self.cover_image}"
        return None
    
    @property
    def date(self):
        """Get formatted date"""
        return self.created_at.strftime('%B %d, %Y')
    
    def __repr__(self):
        return f'<BlogPost {self.title}>'

class ContactMessage(db.Model):
    """Contact message model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.name}>'

class NewsletterSubscription(db.Model):
    """Newsletter subscription model"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    is_active = db.Column(db.Boolean, default=True)
    subscribed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NewsletterSubscription {self.email}>'

class SiteConfig(db.Model):
    """Site configuration model"""
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default="Kambel Consult")
    tagline = db.Column(db.String(200), default="Professional Consulting and Training Services")
    logo = db.Column(db.String(255))
    favicon = db.Column(db.String(255))
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def logo_url(self):
        """Get logo URL"""
        if self.logo:
            return f"/uploads/{self.logo}"
        return None
    
    @property
    def favicon_url(self):
        """Get favicon URL"""
        if self.favicon:
            return f"/uploads/{self.favicon}"
        return None
    
    def __repr__(self):
        return f'<SiteConfig {self.site_name}>'
