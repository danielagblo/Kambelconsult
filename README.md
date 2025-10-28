# Kambel Consult - Professional Development & Consultancy Platform

A comprehensive website and content management system for Kambel Consult featuring publications, consultancy services, blog, masterclasses, and KICT programs.

## 🚀 Quick Start

### Automated Setup (Recommended)

**For macOS/Linux:**
```bash
bash setup.sh
```

**For Windows:**
```bash
setup.bat
```

The setup script will:
- Create a virtual environment
- Install all Python dependencies
- Set up Django database and migrations
- Create necessary directories

### Manual Setup

If you prefer to set up manually:

1. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   cd django_admin && pip install -r requirements.txt && cd ..
   ```

3. **Set up Django database**
   ```bash
   cd django_admin
   python3 manage.py migrate
   python3 manage.py createsuperuser  # Optional: Create admin user
   cd ..
   ```

4. **Configure environment (optional)**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 📁 Project Structure

```
kambelconsult/
├── app.py                      # Flask frontend application (Port 5001)
├── django_admin/              # Django admin backend (Port 8000)
│   ├── kambel_admin/          # Django app
│   │   ├── models.py           # Database models
│   │   ├── admin.py           # Admin panel configuration
│   │   ├── views.py           # API views
│   │   ├── urls.py            # URL routing
│   │   └── settings.py        # Django settings
│   ├── manage.py              # Django management script
│   ├── media/                 # Media files (uploads)
│   └── db.sqlite3             # SQLite database
├── static/                    # Static files (CSS, JS, images)
├── index.html                 # Homepage
├── masterclass.html           # Masterclass page
├── publications.html          # Publications page
├── consultancy-unified.html   # Consultancy page
├── gallery.html               # Gallery page
├── about.html                 # About page
├── requirements.txt           # Python dependencies
├── setup.sh                   # Setup script (macOS/Linux)
└── setup.bat                  # Setup script (Windows)
```

## 🔧 Running the Application

### Start the Flask Frontend

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Start Flask server
python3 app.py
```

The website will be available at: **http://localhost:5001**

### Start the Django Admin Backend

```bash
# In a new terminal
cd django_admin
python3 manage.py runserver 8000
```

The admin panel will be available at: **http://localhost:8000/admin**

## 📖 Features

### Frontend (Flask)
- ✅ Responsive Bootstrap 5 design
- ✅ Dynamic content loading from Django API
- ✅ Publications management
- ✅ Consultancy services
- ✅ Blog system
- ✅ Masterclass registration
- ✅ Gallery with images and videos
- ✅ Contact forms
- ✅ Newsletter subscription
- ✅ Social media integration
- ✅ Custom favicon and branding

### Backend (Django Admin)
- ✅ Complete admin panel for content management
- ✅ Publications with categories and cover images
- ✅ Consultancy services with cover images
- ✅ Blog posts with cover images
- ✅ Masterclasses with registration system
- ✅ Gallery items with media upload
- ✅ Newsletter subscription management
- ✅ Contact message management
- ✅ Site configuration (hero, about, SEO)
- ✅ Social media links management
- ✅ Legal pages (Privacy Policy, Terms & Conditions)

## 🗄️ Database Models

All data is managed through Django admin:

- **Publications**: Books with categories and purchase links
- **Consultancy Services**: Service offerings with cover images
- **Blog Posts**: Blog content with cover images
- **Masterclasses**: Training sessions with registration
- **Gallery Items**: Images and videos with captions
- **Newsletter Subscriptions**: Email subscriptions
- **Contact Messages**: Contact form submissions
- **Site Configuration**: Hero section, about page, SEO
- **Social Media Links**: Social media platform links

## 🔐 Django Admin Access

### Create Superuser

```bash
cd django_admin
python3 manage.py createsuperuser
```

Follow the prompts to create your admin account.

### Default Admin Credentials

If you've run the populate commands, the default credentials might be:
- Username: `admin`
- Password: `admin123` (please change this!)

**Important**: Always change the default password in production!

## 🌐 API Endpoints

### Django Admin API (Port 8000)

- `GET /api/blog/` - Get all blog posts
- `GET /api/publications/` - Get all publications
- `GET /api/consultancy/` - Get all consultancy services
- `GET /api/masterclasses/` - Get all masterclasses
- `GET /api/gallery/` - Get gallery items
- `GET /api/site/config/` - Get site configuration
- `GET /api/site/hero/` - Get hero section content
- `GET /api/site/contact-info/` - Get contact information
- `GET /api/site/social-media/` - Get social media links

### Frontend (Port 5001)

The Flask app proxies requests to the Django API and serves the HTML pages.

## 🛠️ Development

### Making Changes

1. **Content Changes**: Use Django admin panel at http://localhost:8000/admin
2. **Frontend Changes**: Edit HTML files (index.html, masterclass.html, etc.)
3. **Styling**: Edit `static/css/style.css`
4. **JavaScript**: Edit `static/js/script.js`
5. **Backend Logic**: Edit `django_admin/kambel_admin/models.py`, `views.py`, `admin.py`

### Database Migrations

When you change models in Django:

```bash
cd django_admin
python3 manage.py makemigrations
python3 manage.py migrate
```

## 📝 Environment Variables

Create a `.env` file in the root directory:

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Django Configuration
DJANGO_SECRET_KEY=your-django-secret-key
DJANGO_DEBUG=True

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Port Configuration
FLASK_PORT=5001
DJANGO_PORT=8000
```

## 🚀 Production Deployment

### Recommended Hosting

- **Frontend**: Vercel, Netlify, or any static hosting
- **Backend**: Heroku, Railway, DigitalOcean, AWS
- **Database**: PostgreSQL (recommended) or SQLite for small projects
- **Media Files**: AWS S3, Cloudinary, or any CDN

### Production Checklist

- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up proper email configuration
- [ ] Configure static file serving
- [ ] Set up HTTPS/SSL
- [ ] Use environment variables for secrets
- [ ] Set up automatic backups
- [ ] Configure monitoring and logging

## 📞 Support

For issues and questions:
- Check existing documentation files in the project
- Review Django and Flask documentation
- Contact: info@kambelconsult.com

## 📄 License

This project is proprietary and confidential.

## 🎉 Acknowledgments

Built with:
- Flask - Python web framework
- Django - High-level Python web framework
- Bootstrap 5 - CSS framework
- Font Awesome - Icon library

---

**Made with ❤️ for Kambel Consult**
