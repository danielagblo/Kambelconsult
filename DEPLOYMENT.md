# 🚀 Deployment Guide - Kambel Consult

This guide covers deploying the Kambel Consult application to production.

## Architecture

The application consists of two main components:
1. **Flask Frontend** (Port 5001) - Serves HTML/CSS/JS
2. **Django Backend** (Port 8000) - Admin panel and API

## Pre-Deployment Checklist

- [ ] Change `DEBUG=False` in Django settings
- [ ] Set `ALLOWED_HOSTS` in Django settings
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure email service
- [ ] Set up proper media file serving
- [ ] Configure HTTPS/SSL certificates
- [ ] Set environment variables securely
- [ ] Set up automatic backups
- [ ] Configure monitoring and logging

## Quick Start (Local Development)

```bash
# Run automated setup
bash setup.sh

# Start both servers
bash start_servers.sh

# Or start manually:
# Terminal 1: Flask
python3 app.py

# Terminal 2: Django
cd django_admin && python3 manage.py runserver 8000
```

## Production Deployment Options

### Option 1: Heroku (Easiest)

**Deploy Django Backend:**
```bash
cd django_admin
heroku create kambel-backend
heroku addons:create heroku-postgresql:hobby-dev
git subtree push --prefix django_admin heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

**Deploy Flask Frontend:**
```bash
heroku create kambel-frontend
git subtree push --prefix . heroku main
```

### Option 2: DigitalOcean

**Use App Platform or VPS:**
- Deploy Django on one Droplet (or App Platform)
- Deploy Flask on another
- Use managed PostgreSQL database
- Set up load balancer

### Option 3: AWS

**Recommended Architecture:**
- **EC2** or **ECS** for Django backend
- **EC2** or **Elastic Beanstalk** for Flask frontend
- **RDS** for PostgreSQL database
- **S3** for media file storage
- **CloudFront** for static file CDN
- **Route 53** for DNS

### Option 4: Railway

**One-Click Deploy:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## Environment Variables

Create a `.env` file or set in hosting platform:

```env
# Security
DJANGO_SECRET_KEY=your-production-secret-key
FLASK_SECRET_KEY=your-flask-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://user:pass@host:port/dbname

# Email
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key

# AWS S3 (for media files)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name

# URLs
DJANGO_API_BASE=https://api.yourdomain.com/api
FRONTEND_URL=https://yourdomain.com
```

## Database Migration (Production)

```bash
cd django_admin
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

## Static Files

For Django:
```bash
python manage.py collectstatic --noinput
```

Configure your web server (Nginx) to serve static files:
```nginx
location /static/ {
    alias /path/to/staticfiles/;
}

location /media/ {
    alias /path/to/media/;
}
```

## Media Files (Cloud Storage)

Use AWS S3, Cloudinary, or similar:
1. Install `django-storages`
2. Configure in Django settings
3. Upload files will automatically go to cloud

## SSL/HTTPS

### Let's Encrypt (Free):
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Or use your hosting provider's SSL feature.

## Monitoring

Set up monitoring with:
- **Sentry** for error tracking
- **New Relic** or **Datadog** for performance
- **Uptime Robot** for uptime monitoring

## Backup Strategy

### Automated Backups:
```bash
# Database backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql

# Media files backup
aws s3 sync django_admin/media s3://backup-bucket/media
```

Schedule with cron:
```cron
# Daily backup at 2 AM
0 2 * * * /path/to/backup_script.sh
```

## Scaling

### For High Traffic:

1. **Use Load Balancer** (Nginx, HAProxy)
2. **Horizontal Scaling** (Multiple Flask/Django instances)
3. **CDN** for static files (CloudFront, Cloudflare)
4. **Caching** (Redis)
5. **Database Replication** (Read replicas)

### Recommended Hosting:

| Component | Hosting | Cost |
|-----------|---------|------|
| Small Project | Railway/Render | Free-$25/mo |
| Medium Project | DigitalOcean | $40-100/mo |
| Large Project | AWS/GCP | $200+/mo |

## Testing Before Deploy

```bash
# Run tests
python test_backend.py

# Test locally in production mode
export FLASK_ENV=production
python app.py

# Test Django
cd django_admin
python manage.py check --deploy
python manage.py test
```

## Post-Deployment

1. ✅ Test all features
2. ✅ Verify admin panel access
3. ✅ Test file uploads
4. ✅ Check email sending
5. ✅ Monitor error logs
6. ✅ Set up alerts
7. ✅ Document deployment process

## Rollback Plan

If something goes wrong:
```bash
# Revert to previous version
git revert HEAD
git push

# Or redeploy previous commit
git checkout <previous-commit-hash>
# Redeploy
```

## Support

For deployment issues:
- Check logs: `heroku logs --tail`
- Check Django logs
- Check Flask logs
- Verify environment variables

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secure
- [ ] Database credentials secure
- [ ] Admin password changed
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] File upload validation

## Performance Optimization

1. **Enable Gzip compression**
2. **Use CDN for static files**
3. **Enable database query caching**
4. **Optimize images** (WebP, compression)
5. **Minify CSS/JS**
6. **Use lazy loading**

## Maintenance

### Regular Tasks:
- Update dependencies monthly
- Monitor error logs weekly
- Backup database daily
- Test restore procedure monthly
- Review security quarterly

---

**Need help?** Check the main README.md or PROJECT_STRUCTURE.md

