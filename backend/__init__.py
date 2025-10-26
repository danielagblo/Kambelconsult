from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
admin = Admin()

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///kambel_consult.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'publications'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'blog'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profile'), exist_ok=True)
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    admin.init_app(app)
    CORS(app)
    
    # Configure login manager
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access the admin panel.'
    login_manager.login_message_category = 'info'
    
    # Import models
    from models import User, Category, Book, ConsultancyService, ServiceFeature, BlogPost, ContactMessage, NewsletterSubscription
    
    # Import admin views
    from admin import setup_admin
    
    # Setup admin panel
    setup_admin(admin, db)
    
    # Import API routes
    from api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
