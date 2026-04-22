# Deployment Guide

Complete guide for deploying the News App Django application to production environments.

---

## Table of Contents

- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Deployment Options](#deployment-options)
- [Traditional Server Deployment](#traditional-server-deployment)
- [Cloud Platform Deployment](#cloud-platform-deployment)
- [Docker Deployment](#docker-deployment)
- [Production Configuration](#production-configuration)
- [Database Setup](#database-setup)
- [Static Files & Media](#static-files--media)
- [Email Configuration](#email-configuration)
- [Monitoring & Logging](#monitoring--logging)
- [Backup & Recovery](#backup--recovery)
- [Performance Optimization](#performance-optimization)

---

## Pre-Deployment Checklist

Before deploying to production, complete the following:

```
Security
- [ ] Set DEBUG = False
- [ ] Change SECRET_KEY to a new random value
- [ ] Configure ALLOWED_HOSTS with domain names
- [ ] Enable HTTPS/SSL certificates
- [ ] Set SECURE_SSL_REDIRECT = True
- [ ] Set SESSION_COOKIE_SECURE = True
- [ ] Set CSRF_COOKIE_SECURE = True
- [ ] Configure CORS appropriately
- [ ] Review authentication settings
- [ ] Implement rate limiting

Database
- [ ] Migrate to PostgreSQL (recommended)
- [ ] Configure database backups
- [ ] Set up database replication (if needed)
- [ ] Enable database encryption
- [ ] Test database recovery
- [ ] Configure connection pooling

Static Files & Media
- [ ] Collect static files (python manage.py collectstatic)
- [ ] Configure static file serving (CDN or web server)
- [ ] Configure media file serving
- [ ] Set up S3 or similar for file storage (optional)

Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up performance monitoring
- [ ] Configure alert notifications
- [ ] Test error reporting

Testing
- [ ] Run full test suite
- [ ] Run security checks (python manage.py check --deploy)
- [ ] Load testing
- [ ] Security penetration testing
- [ ] Accessibility testing

Documentation
- [ ] Update deployment documentation
- [ ] Document server configuration
- [ ] Create runbook for common tasks
- [ ] Document backup procedures
```

---

## Deployment Options

### Option 1: Traditional Linux Server
**Best for**: Medium to large applications, full control
**Complexity**: Medium-High
**Cost**: Low-Medium

### Option 2: Platform-as-a-Service (PaaS)
**Options**: Heroku, PythonAnywhere, Railway
**Best for**: Quick deployments, low maintenance
**Complexity**: Low
**Cost**: Medium-High

### Option 3: Cloud Containers
**Options**: AWS ECS, Google Cloud Run, Azure Container Instances
**Best for**: Scalable applications
**Complexity**: High
**Cost**: Pay-as-you-go

### Option 4: Cloud Virtual Machines
**Options**: AWS EC2, Google Compute Engine, Azure VMs
**Best for**: Maximum control
**Complexity**: High
**Cost**: Medium

---

## Traditional Server Deployment

### System Requirements

- Ubuntu 20.04 LTS or similar
- 2+ GB RAM
- 20+ GB disk space
- Python 3.8+
- PostgreSQL 12+
- Nginx or Apache

### Step 1: Server Setup

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv nginx postgresql postgresql-contrib git curl

# Create application user
sudo useradd -m -s /bin/bash newsapp
sudo su - newsapp
```

### Step 2: Clone Repository

```bash
cd /home/newsapp
git clone https://github.com/Nirajjj11/news-app-using-django.git
cd news_app_django_by_book
```

### Step 3: Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd django_project
```

### Step 4: Configure Environment

```bash
# Create .env file
nano .env

# Add production settings:
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_ENGINE=django.db.backends.postgresql
DB_NAME=newsapp_db
DB_USER=newsapp_user
DB_PASSWORD=strong-password-here
DB_HOST=localhost
DB_PORT=5432
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Step 5: Database Setup

```bash
# Create PostgreSQL database and user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE newsapp_db;
CREATE USER newsapp_user WITH PASSWORD 'strong-password-here';
ALTER ROLE newsapp_user SET client_encoding TO 'utf8';
ALTER ROLE newsapp_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE newsapp_user SET default_transaction_deferrable TO on;
ALTER ROLE newsapp_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE newsapp_db TO newsapp_user;
\q
```

### Step 6: Run Migrations

```bash
cd /home/newsapp/news_app_django_by_book/django_project
source ../venv/bin/activate

python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Configure Gunicorn

```bash
# Install Gunicorn
pip install gunicorn

# Create systemd service file
sudo nano /etc/systemd/system/newsapp.service
```

Add:
```ini
[Unit]
Description=News App Django Application
After=network.target

[Service]
User=newsapp
Group=www-data
WorkingDirectory=/home/newsapp/news_app_django_by_book/django_project
Environment="PATH=/home/newsapp/news_app_django_by_book/venv/bin"
ExecStart=/home/newsapp/news_app_django_by_book/venv/bin/gunicorn \
    --workers 4 \
    --bind 127.0.0.1:8000 \
    django_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable newsapp
sudo systemctl start newsapp
sudo systemctl status newsapp
```

### Step 8: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/newsapp
```

Add:
```nginx
upstream newsapp {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    client_max_body_size 20M;

    location /static/ {
        alias /home/newsapp/news_app_django_by_book/django_project/staticfiles/;
    }

    location /media/ {
        alias /home/newsapp/news_app_django_by_book/django_project/media/;
    }

    location / {
        proxy_pass http://newsapp;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/newsapp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 9: SSL Certificate Setup (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Cloud Platform Deployment

### Heroku Deployment

```bash
# Install Heroku CLI
curl https://cli.heroku.com/install.sh | sh

# Login
heroku login

# Create app
heroku create newsapp-django

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=yourdomain.com

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# View logs
heroku logs --tail
```

### PythonAnywhere

1. Create account at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload code via Git or ZIP
3. Configure virtual environment
4. Set environment variables in web app configuration
5. Configure database
6. Set up static files mapping
7. Enable HTTPS

---

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY django_project .

# Create non-root user
RUN useradd -m newsapp && chown -R newsapp:newsapp /app
USER newsapp

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn django_project.wsgi:application --bind 0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=newsapp_db
      - POSTGRES_USER=newsapp_user
      - POSTGRES_PASSWORD=strong-password

  web:
    build: .
    command: gunicorn django_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=postgresql://newsapp_user:strong-password@db:5432/newsapp_db
    depends_on:
      - db

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - web
```

Deploy:
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## Production Configuration

### settings.py Production Settings

```python
# Security
DEBUG = False
SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,
        'OPTIONS': {
            'sslmode': 'require',
        }
    }
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = '/home/newsapp/staticfiles/'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
```

---

## Database Setup

### PostgreSQL Configuration

```bash
# Backup
pg_dump newsapp_db > backup.sql

# Restore
psql newsapp_db < backup.sql

# Connection pooling with PgBouncer
pip install psycopg2-pool

# In settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'newsapp_db',
        'USER': 'newsapp_user',
        'PASSWORD': 'password',
        'HOST': 'pgbouncer-host',  # PgBouncer instead of direct DB
        'PORT': '6432',
        'CONN_MAX_AGE': 600,
    }
}
```

---

## Static Files & Media

### AWS S3 Configuration

```bash
# Install
pip install boto3 django-storages

# settings.py
if not DEBUG:
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

---

## Email Configuration

### Gmail Setup

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # App password, not account password
DEFAULT_FROM_EMAIL = 'your-email@gmail.com'
```

---

## Monitoring & Logging

### Sentry Error Tracking

```bash
# Install
pip install sentry-sdk

# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://your-sentry-dsn@sentry.io/project-id",
    integrations=[DjangoIntegration()],
    traces_sample_rate=0.1,
    send_default_pii=False
)
```

### Application Performance Monitoring

```bash
pip install django-extensions django-silk

# settings.py
INSTALLED_APPS = [
    ...
    'silk',
]

MIDDLEWARE = [
    ...
    'silk.middleware.SilkyMiddleware',
]

# urls.py
urlpatterns = [
    path('silk/', include('silk.urls', namespace='silk')),
]
```

---

## Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup.sh
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="newsapp_db"

# Database backup
pg_dump $DB_NAME | gzip > $BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz

# Media files backup
tar -czf $BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz /home/newsapp/media/

# Keep only last 30 days
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
```

Schedule with cron:
```bash
# Daily backup at 2 AM
0 2 * * * /home/newsapp/backup.sh
```

---

## Performance Optimization

### Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Query Optimization

```python
# Use select_related for ForeignKey
articles = Article.objects.select_related('author').all()

# Use prefetch_related for M2M and reverse relations
articles = Article.objects.prefetch_related('comments').all()

# Use only() to fetch specific fields
articles = Article.objects.only('id', 'title', 'author_id').all()

# Use values() for dictionary results
articles = Article.objects.values('id', 'title').all()
```

---

**Last Updated**: April 22, 2026
