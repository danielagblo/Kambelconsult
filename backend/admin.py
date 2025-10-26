from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from flask_admin.model import typefmt
from flask import redirect, url_for, flash, request, render_template
from flask_login import login_required, current_user, logout_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime

class SecureModelView(ModelView):
    """Base model view with authentication"""
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin.login'))

class UserAdmin(SecureModelView):
    """User admin view"""
    column_list = ['username', 'email', 'is_active', 'created_at']
    column_searchable_list = ['username', 'email']
    column_filters = ['is_active', 'created_at']
    form_excluded_columns = ['password_hash']
    
    def on_model_change(self, form, model, is_created):
        if is_created and form.password.data:
            model.set_password(form.password.data)

class CategoryAdmin(SecureModelView):
    """Category admin view"""
    column_list = ['name', 'description', 'is_active', 'created_at']
    column_searchable_list = ['name']
    column_filters = ['is_active', 'created_at']
    form_columns = ['name', 'description', 'is_active']

class BookAdmin(SecureModelView):
    """Book admin view"""
    column_list = ['title', 'author', 'category', 'price', 'is_active', 'created_at']
    column_searchable_list = ['title', 'author']
    column_filters = ['category', 'is_active', 'created_at']
    form_columns = ['title', 'author', 'description', 'category', 'pages', 'price', 'cover_image', 'purchase_link', 'is_active']
    
    form_extra_fields = {
        'cover_image': FileUploadField('Cover Image', base_path='uploads/publications', relative_path='publications/')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.cover_image.data:
            filename = secure_filename(form.cover_image.data.filename)
            if filename:
                model.cover_image = filename

class ConsultancyServiceAdmin(SecureModelView):
    """Consultancy service admin view"""
    column_list = ['name', 'service_type', 'is_active', 'order', 'created_at']
    column_searchable_list = ['name', 'service_type']
    column_filters = ['service_type', 'is_active', 'created_at']
    form_columns = ['name', 'service_type', 'description', 'icon', 'is_active', 'order']

class ServiceFeatureAdmin(SecureModelView):
    """Service feature admin view"""
    column_list = ['title', 'service', 'is_active', 'order', 'created_at']
    column_searchable_list = ['title']
    column_filters = ['service', 'is_active', 'created_at']
    form_columns = ['title', 'description', 'icon', 'service', 'is_active', 'order']

class BlogPostAdmin(SecureModelView):
    """Blog post admin view"""
    column_list = ['title', 'author', 'is_published', 'created_at']
    column_searchable_list = ['title', 'author']
    column_filters = ['is_published', 'created_at']
    form_columns = ['title', 'content', 'excerpt', 'author', 'cover_image', 'is_published']
    
    form_extra_fields = {
        'cover_image': FileUploadField('Cover Image', base_path='uploads/blog', relative_path='blog/')
    }
    
    def on_model_change(self, form, model, is_created):
        if form.cover_image.data:
            filename = secure_filename(form.cover_image.data.filename)
            if filename:
                model.cover_image = filename

class ContactMessageAdmin(SecureModelView):
    """Contact message admin view"""
    column_list = ['name', 'email', 'subject', 'is_read', 'created_at']
    column_searchable_list = ['name', 'email', 'subject']
    column_filters = ['is_read', 'created_at']
    form_columns = ['name', 'email', 'subject', 'message', 'is_read']
    can_create = False  # Contact messages are created via API

class NewsletterSubscriptionAdmin(SecureModelView):
    """Newsletter subscription admin view"""
    column_list = ['email', 'is_active', 'subscribed_at']
    column_searchable_list = ['email']
    column_filters = ['is_active', 'subscribed_at']
    form_columns = ['email', 'is_active']

class SiteConfigAdmin(SecureModelView):
    """Site configuration admin view"""
    column_list = ['site_name', 'tagline', 'contact_email', 'contact_phone', 'updated_at']
    form_columns = ['site_name', 'tagline', 'logo', 'favicon', 'contact_email', 'contact_phone', 'address']
    
    form_extra_fields = {
        'logo': FileUploadField('Logo', base_path='uploads', relative_path=''),
        'favicon': FileUploadField('Favicon', base_path='uploads', relative_path='')
    }

class DashboardView(BaseView):
    """Admin dashboard view"""
    @expose('/')
    @login_required
    def index(self):
        from .models import Book, BlogPost, ContactMessage, NewsletterSubscription
        
        # Get statistics
        stats = {
            'total_books': Book.query.count(),
            'total_blog_posts': BlogPost.query.count(),
            'unread_messages': ContactMessage.query.filter_by(is_read=False).count(),
            'newsletter_subscribers': NewsletterSubscription.query.filter_by(is_active=True).count(),
            'recent_books': Book.query.order_by(Book.created_at.desc()).limit(5).all(),
            'recent_messages': ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
        }
        
        return self.render('admin/dashboard.html', stats=stats)

class LoginView(BaseView):
    """Login view"""
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        
        from flask import request, flash
        from flask_login import login_user
        from .models import User
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('admin.index'))
            else:
                flash('Invalid username or password.', 'error')
        
        return self.render('admin/login.html')

class LogoutView(BaseView):
    """Logout view"""
    @expose('/')
    @login_required
    def index(self):
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('admin.login'))

def setup_admin(admin, db):
    """Setup admin panel"""
    from models import (
        User, Category, Book, ConsultancyService, ServiceFeature,
        BlogPost, ContactMessage, NewsletterSubscription, SiteConfig
    )
    
    # Add views
    admin.add_view(DashboardView(name='Dashboard', endpoint='dashboard'))
    admin.add_view(LoginView(name='Login', endpoint='login'))
    admin.add_view(LogoutView(name='Logout', endpoint='logout'))
    
    # Add model views
    admin.add_view(UserAdmin(User, db.session, name='Users'))
    admin.add_view(CategoryAdmin(Category, db.session, name='Categories'))
    admin.add_view(BookAdmin(Book, db.session, name='Books'))
    admin.add_view(ConsultancyServiceAdmin(ConsultancyService, db.session, name='Consultancy Services'))
    admin.add_view(ServiceFeatureAdmin(ServiceFeature, db.session, name='Service Features'))
    admin.add_view(BlogPostAdmin(BlogPost, db.session, name='Blog Posts'))
    admin.add_view(ContactMessageAdmin(ContactMessage, db.session, name='Contact Messages'))
    admin.add_view(NewsletterSubscriptionAdmin(NewsletterSubscription, db.session, name='Newsletter Subscriptions'))
    admin.add_view(SiteConfigAdmin(SiteConfig, db.session, name='Site Configuration'))
