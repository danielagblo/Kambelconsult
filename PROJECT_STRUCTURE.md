# 📁 Project Structure - Kambel Consult

## Overview

This project uses a **hybrid architecture** with Flask serving the frontend and Django providing the backend/admin panel.

```
┌─────────────────────────────────────────────────┐
│              Frontend (Flask)                  │
│  - Serves HTML pages on port 5001              │
│  - Handles routing and static files            │
│  - Proxies API requests to Django              │
└───────────────────┬─────────────────────────────┘
                    │
                    │ HTTP Requests
                    ▼
┌─────────────────────────────────────────────────┐
│           Backend (Django)                      │
│  - Admin panel on port 8000                     │
│  - REST API for all content                     │
│  - Database models and business logic            │
│  - File uploads and media management           │
└─────────────────────────────────────────────────┘
```

## Directory Structure

```
kambelconsult/
│
├── 📄 app.py                      # Flask frontend app (main entry point)
├── 📄 requirements.txt             # Flask dependencies
├── 📄 setup.sh                    # Setup script (macOS/Linux)
├── 📄 setup.bat                   # Setup script (Windows)
├── 📄 .env.example                # Environment variables template
├── 📄 .gitignore                  # Git ignore rules
│
├── 📁 static/                      # Static files (served by Flask)
│   ├── css/
│   │   ├── style.css              # Main stylesheet
│   │   ├── klogo.jpeg             # Site logo
│   │   └── profilepicture.jpeg    # Profile picture
│   ├── js/
│   │   └── script.js              # Frontend JavaScript
│   ├── favicon.png                # Site favicon
│   └── apple-touch-icon.png       # iOS touch icon
│
├── 📁 HTML Files/                  # Frontend pages
│   ├── index.html                 # Homepage
│   ├── masterclass.html           # Masterclass page
│   ├── publications.html          # Publications page
│   ├── consultancy-unified.html   # Consultancy services
│   ├── gallery.html               # Gallery page
│   ├── about.html                 # About page
│   ├── privacy-policy.html       # Privacy policy
│   └── terms-conditions.html      # Terms & conditions
│
├── 📁 django_admin/                # Django backend
│   ├── 📄 manage.py               # Django management script
│   ├── 📄 requirements.txt        # Django dependencies
│   │
│   ├── 📁 kambel_admin/           # Django app
│   │   ├── 📄 models.py           # Database models
│   │   ├── 📄 admin.py            # Admin panel configuration
│   │   ├── 📄 views.py            # API views
│   │   ├── 📄 urls.py             # URL routing
│   │   ├── 📄 settings.py         # Django settings
│   │   │
│   │   ├── 📁 management/         # Custom commands
│   │   │   └── commands/
│   │   │       ├── populate_about.py
│   │   │       └── populate_legal_pages.py
│   │   │
│   │   └── 📁 migrations/         # Database migrations
│   │
│   ├── 📁 media/                  # Uploaded files
│   │   ├── blog/covers/           # Blog cover images
│   │   ├── publications/covers/    # Book cover images
│   │   ├── consultancy/covers/     # Service cover images
│   │   ├── masterclasses/covers/   # Masterclass cover images
│   │   ├── gallery/images/        # Gallery images
│   │   └── hero/                  # Hero section images
│   │
│   ├── 📁 templates/              # Django templates
│   │   └── admin/
│   │       └── base_site.html     # Custom admin template
│   │
│   └── 📁 db.sqlite3              # SQLite database
│
└── 📁 Documentation/              # Docs
    ├── README.md                  # Main readme
    ├── QUICK_START.md             # Quick start guide
    └── PROJECT_STRUCTURE.md       # This file
```

## Data Flow

### 1. User Visits Website
```
User → http://localhost:5001/index.html
     → Flask serves HTML
     → Browser loads CSS/JS
```

### 2. JavaScript Fetches Data
```javascript
fetch('http://localhost:5001/api/blog')
     → Flask proxies to Django
     → Django API returns JSON
     → Frontend renders content
```

### 3. Admin Manages Content
```
Admin → http://localhost:8000/admin
      → Django admin interface
      → Edit models (Publications, Blog, etc.)
      → Save to database
      → API updates automatically
```

## Key Files

### Frontend (Flask)

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application, serves pages and proxies API |
| `index.html` | Homepage with dynamic content |
| `static/css/style.css` | All styling |
| `static/js/script.js` | Frontend logic and API calls |

### Backend (Django)

| File | Purpose |
|------|---------|
| `django_admin/manage.py` | Django management script |
| `models.py` | Database models (Publications, Blog, etc.) |
| `admin.py` | Admin panel configuration |
| `views.py` | API endpoints |
| `urls.py` | URL routing |

## Configuration

### Flask (`app.py`)
- **Port**: 5001
- **Debug**: Enabled in development
- **CORS**: Enabled for API access

### Django (`settings.py`)
- **Port**: 8000
- **Database**: SQLite (db.sqlite3)
- **Media**: django_admin/media/
- **Static**: django_admin/staticfiles/

## Adding New Features

### 1. New Content Type
1. Add model to `django_admin/kambel_admin/models.py`
2. Register in `django_admin/kambel_admin/admin.py`
3. Create migration: `python manage.py makemigrations`
4. Run migration: `python manage.py migrate`
5. Add API endpoint in `views.py`

### 2. New Page
1. Create HTML file in root
2. Add route in `app.py`
3. Add navigation link in relevant HTML files
4. Style in `static/css/style.css`

### 3. New API Endpoint
1. Add view in `views.py`
2. Add URL in `urls.py`
3. Optional: Add proxy in Flask `app.py`

## Common Tasks

### Starting Development
```bash
bash start_servers.sh
```

### Creating Admin User
```bash
cd django_admin
python manage.py createsuperuser
```

### Database Migration
```bash
cd django_admin
python manage.py makemigrations
python manage.py migrate
```

### Running Tests
```bash
python test_backend.py
```

## Tips

1. **Always use Django admin for content**, not direct database edits
2. **Check browser console** for API errors
3. **Keep both servers running** during development
4. **Use migrations** when changing models
5. **Clear browser cache** if changes don't show

## Security Notes

- `.gitignore` excludes sensitive files
- `.env` file with secrets should never be committed
- Always use environment variables for production
- Change default admin credentials immediately

