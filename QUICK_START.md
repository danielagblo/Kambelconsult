# 🚀 Quick Start Guide - Kambel Consult

Get up and running in 3 easy steps!

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

## Step 2: Start the Servers

### Terminal 1 - Frontend (Flask)
```bash
python3 app.py
```
Website will be at: http://localhost:5001

### Terminal 2 - Backend (Django Admin)
```bash
cd django_admin
python3 manage.py runserver 8000
```
Admin panel will be at: http://localhost:8000/admin

## Step 3: Create Admin Account

```bash
cd django_admin
python3 manage.py createsuperuser
```

Follow the prompts to create your admin username and password.

## ✅ You're Ready!

- **Website**: http://localhost:5001
- **Admin Panel**: http://localhost:8000/admin
- **Username**: (the one you just created)
- **Password**: (the one you just set)

## 📚 Next Steps

1. Log into the admin panel
2. Add your content (publications, blog posts, masterclasses, etc.)
3. Customize the site configuration
4. Upload cover images and media

## 🆘 Troubleshooting

**Port already in use?**
- Change ports in `app.py` (FLASK_PORT) and Django settings (PORT)

**Dependencies not installing?**
- Make sure you have Python 3.8+ installed
- Try: `pip install --upgrade pip` first

**Database errors?**
- Run: `cd django_admin && python3 manage.py migrate`

**Forgot admin password?**
- Create a new superuser or use Django shell to reset

## 💡 Tips

- Keep both servers running while developing
- Use Django admin for all content management
- Check browser console for API errors
- Media files are stored in `django_admin/media/`

Happy coding! 🎉

