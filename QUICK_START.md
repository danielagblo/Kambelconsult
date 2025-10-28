# 🚀 Quick Start Guide - Kambel Consult

Get up and running in 2 easy steps!

## Step 1: Run Setup Script

**macOS/Linux:**
```bash
bash setup.sh
```

**Windows:**
```bash
setup.bat
```

This will install all dependencies and set up the database.

## Step 2: Start the Application

### Simple Method (Recommended)
```bash
python3 start.py
```

### Manual Method
```bash
cd django_admin
python3 manage.py runserver 8000
```

**Everything runs on ONE port now!**

## ✅ You're Ready!

- **Website**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Step 3: Create Admin Account

```bash
cd django_admin
python3 manage.py createsuperuser
```

Follow the prompts to create your admin username and password.

## 📚 What's Available

| Page | URL |
|------|-----|
| Homepage | http://localhost:8000 |
| Publications | http://localhost:8000/publications |
| Consultancy | http://localhost:8000/consultancy |
| Masterclass | http://localhost:8000/masterclass |
| Gallery | http://localhost:8000/gallery |
| About | http://localhost:8000/about |
| Privacy Policy | http://localhost:8000/privacy-policy |
| Terms & Conditions | http://localhost:8000/terms-conditions |
| Admin Panel | http://localhost:8000/admin |

## 🆘 Troubleshooting

**Port already in use?**
- Kill the process using port 8000: `lsof -ti:8000 | xargs kill`

**Database errors?**
- Run: `cd django_admin && python3 manage.py migrate`

**Static files not loading?**
- Run: `cd django_admin && python3 manage.py collectstatic`

**Forgot admin password?**
- Create a new superuser or reset in Django shell

## 💡 Tips

- Everything runs on port 8000 now (single unified server)
- Use Django admin for all content management
- Check browser console for any errors
- Media files are in `django_admin/media/`

Happy coding! 🎉
