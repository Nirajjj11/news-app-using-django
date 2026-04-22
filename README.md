# 📰 News App Django

A full-featured Django-based news and article management platform with user authentication, real-time sentiment analysis, and advanced analytics dashboard. Built with Django 6.0+, Bootstrap 5, and TextBlob NLP.

[![Django Version](https://img.shields.io/badge/Django-6.0.4-green.svg)](https://docs.djangoproject.com/en/6.0/)
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](#)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation Guide](#installation-guide)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Database Schema](#database-schema)
- [Usage Guide](#usage-guide)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## 🎯 Overview

The **News App Django** is a modern, scalable web application designed for publishing, managing, and analyzing news articles. It features comprehensive user authentication, real-time sentiment analysis using NLP (Natural Language Processing), and an intelligent analytics dashboard to track content performance and user sentiment trends.

### Key Highlights
- ✅ Full CRUD operations for articles and comments
- ✅ Real-time sentiment analysis on articles and comments
- ✅ User role-based access control
- ✅ Interactive analytics dashboard
- ✅ Responsive design with Bootstrap 5
- ✅ Email notification system
- ✅ Security best practices implemented

---

## ✨ Features

### Authentication & Authorization
- User registration and account creation
- Secure login/logout system
- Password reset and change functionality
- Role-based permissions (Author, Editor, Admin)
- Profile management

### Article Management
- Create, read, update, and delete articles
- Rich text editor support
- Author attribution
- Automatic timestamp tracking
- Draft and publish functionality
- Article search and filtering

### Comments & Engagement
- Add comments to articles
- Edit and delete your comments
- Nested comment support (for future enhancements)
- Real-time comment moderation

### Sentiment Analysis
- Automatic sentiment classification (Positive/Negative/Neutral)
- Article sentiment tracking
- Comment sentiment analysis
- Historical sentiment trends
- Sentiment-based content filtering

### Analytics Dashboard
- Real-time sentiment statistics
- User engagement metrics
- Sentiment trend visualization
- Author performance tracking
- Comment sentiment breakdown
- Date-range filtering

### User Interface
- Responsive Bootstrap 5 design
- Dark/Light theme toggle
- Mobile-friendly navigation
- Intuitive dashboard layout
- Clean and modern aesthetic

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 6.0.4 | Web framework |
| **Python** | 3.8+ | Programming language |
| **SQLite** | Latest | Database (Development) |
| **PostgreSQL** | 12+ | Database (Production) |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Bootstrap** | 5.x | CSS framework |
| **HTML5** | - | Markup |
| **CSS3** | - | Styling |
| **JavaScript** | ES6+ | Client-side scripting |

### Libraries & Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| Django-Crispy-Forms | 2.x | Form rendering |
| TextBlob | Latest | NLP & Sentiment Analysis |
| Gunicorn | Latest | WSGI server |
| python-decouple | Latest | Environment configuration |
| Pillow | Latest | Image processing |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **pip** - Package manager (included with Python)
- **Virtual Environment** - `venv` (included with Python 3.3+)

### System Requirements
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 500MB free space
- **Internet**: Required for downloading dependencies

### Development Tools (Optional but Recommended)
- **Visual Studio Code** or any code editor
- **PostgreSQL** for production database
- **Docker** for containerized deployment

---

## 🚀 Installation Guide

### Step 1: Clone the Repository

```bash
git clone https://github.com/Nirajjj11/news-app-using-django.git
cd news_app_django_by_book
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Navigate to Django Project

```bash
cd django_project
```

### Step 5: Configure Environment Variables

Create a `.env` file in the `django_project` directory:

```env
# Django Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Step 6: Database Migrations

```bash
# Apply migrations to create database tables
python manage.py migrate

# Create superuser for admin panel
python manage.py createsuperuser
# Follow the prompts to set username, email, and password
```

### Step 7: Load Sample Data (Optional)

```bash
python manage.py loaddata sample_articles.json
```

### Step 8: Run Development Server

```bash
python manage.py runserver
```

**Access the application:**
- Main Application: http://localhost:8000
- Admin Panel: http://localhost:8000/admin
- Analysis Dashboard: http://localhost:8000/analysis/dashboard

---

## 📁 Project Structure

```
news_app_django_by_book/
│
├── django_project/                    # Main Django project directory
│   ├── manage.py                       # Django command-line utility
│   ├── db.sqlite3                      # SQLite database (development)
│   ├── requirements.txt                # Python dependencies
│   │
│   ├── django_project/                 # Project configuration package
│   │   ├── __init__.py
│   │   ├── asgi.py                    # ASGI configuration for deployment
│   │   ├── wsgi.py                    # WSGI configuration for production
│   │   ├── settings.py                # Project settings and configuration
│   │   └── urls.py                    # Main URL router
│   │
│   ├── accounts/                       # User authentication app
│   │   ├── __init__.py
│   │   ├── admin.py                   # Admin panel configuration
│   │   ├── apps.py                    # App configuration
│   │   ├── forms.py                   # User registration/login forms
│   │   ├── models.py                  # User models
│   │   ├── views.py                   # Authentication views
│   │   ├── urls.py                    # App URL patterns
│   │   ├── tests.py                   # Unit tests
│   │   └── migrations/                # Database migrations
│   │
│   ├── articles/                       # Article management app
│   │   ├── __init__.py
│   │   ├── admin.py                   # Article admin configuration
│   │   ├── apps.py                    # App configuration
│   │   ├── forms.py                   # Article and comment forms
│   │   ├── models.py                  # Article and Comment models
│   │   ├── views.py                   # CRUD views and logic
│   │   ├── urls.py                    # Article URL patterns
│   │   ├── tests.py                   # Article tests
│   │   ├── utils.py                   # Utility functions
│   │   └── migrations/                # Database migrations
│   │
│   ├── analysis/                       # Sentiment analysis app
│   │   ├── __init__.py
│   │   ├── admin.py                   # Analysis admin config
│   │   ├── apps.py                    # App configuration
│   │   ├── models.py                  # Analysis models (if any)
│   │   ├── views.py                   # Dashboard and analysis views
│   │   ├── services.py                # NLP and sentiment analysis logic
│   │   ├── urls.py                    # Analysis URL patterns
│   │   ├── utils.py                   # Helper functions
│   │   ├── tests.py                   # Analysis tests
│   │   └── migrations/                # Database migrations
│   │
│   ├── pages/                          # Static pages app
│   │   ├── __init__.py
│   │   ├── admin.py                   # Pages admin config
│   │   ├── apps.py                    # App configuration
│   │   ├── models.py                  # Page models (if any)
│   │   ├── views.py                   # Page views (Home, About)
│   │   ├── urls.py                    # Page URL patterns
│   │   ├── tests.py                   # Page tests
│   │   └── migrations/
│   │
│   ├── templates/                      # HTML templates
│   │   ├── base.html                  # Base template (layout)
│   │   ├── home.html                  # Homepage
│   │   ├── article_list.html          # List all articles
│   │   ├── article_detail.html        # Single article view
│   │   ├── article_new.html           # Create new article
│   │   ├── article_edit.html          # Edit article
│   │   ├── article_delete.html        # Delete confirmation
│   │   │
│   │   ├── analysis/
│   │   │   └── dashboard.html         # Analytics dashboard
│   │   │
│   │   └── registration/              # Authentication templates
│   │       ├── login.html             # Login form
│   │       ├── signup.html            # User registration
│   │       ├── password_change_form.html
│   │       ├── password_change_done.html
│   │       ├── password_reset_form.html
│   │       ├── password_reset_done.html
│   │       ├── password_reset_confirm.html
│   │       └── password_reset_complete.html
│   │
│   ├── static/                         # Static files
│   │   ├── css/
│   │   │   └── style.css              # Custom CSS styles
│   │   └── js/
│   │       └── theme.js               # Theme toggle script
│   │
│   ├── staticfiles/                    # Collected static files (production)
│   │   ├── admin/                     # Django admin static files
│   │   ├── css/
│   │   └── js/
│   │
│   └── media/                          # User-uploaded files (images, etc.)
│
├── .gitignore                          # Git ignore file
├── .env                                # Environment variables (DO NOT COMMIT)
├── .env.example                        # Environment template
├── README.md                           # This file
├── LICENSE                             # Project license
└── .venv/                              # Virtual environment (NOT in repo)
```

### Directory Descriptions

| Directory | Purpose |
|-----------|---------|
| `accounts/` | Handles user authentication, registration, and profile management |
| `articles/` | Core app for article CRUD operations and comments |
| `analysis/` | Sentiment analysis and analytics dashboard functionality |
| `pages/` | Static pages and navigation |
| `templates/` | Django HTML templates for rendering UI |
| `static/` | CSS, JavaScript, and image assets |
| `django_project/` | Main project configuration and settings |

---

## ⚙️ Configuration

### Django Settings Overview

**Key Configuration Points** in `settings.py`:

```python
# Application Installation
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'accounts',
    'articles',
    'analysis',
    'pages',
]

# Crispy Forms Configuration
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_USE_SSL = True
EMAIL_PORT = 465

# Timezone Configuration
TIME_ZONE = 'IST'
USE_TZ = True
```

### Environment Variables

Create a `.env` file for sensitive configuration:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration

#### Development (SQLite - Default)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Production (PostgreSQL - Recommended)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'news_app_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 🗄️ Database Schema

### Article Model
```
Article
├── title (CharField, max_length=255)
├── body (TextField)
├── date (DateTimeField, auto_now_add=True)
├── author (ForeignKey → User)
└── sentiment (CharField, max_length=20) [Positive|Negative|Neutral]
```

### Comment Model
```
Comment
├── article (ForeignKey → Article, CASCADE)
├── comment (CharField, max_length=140)
├── author (ForeignKey → User)
└── sentiment (CharField, max_length=20) [Positive|Negative|Neutral]
```

### User Model (Django Built-in)
```
User
├── username (CharField, unique=True)
├── email (EmailField)
├── password (CharField, hashed)
├── first_name (CharField)
├── last_name (CharField)
├── is_active (BooleanField)
├── is_staff (BooleanField)
├── date_joined (DateTimeField)
└── last_login (DateTimeField)
```

### Entity Relationship Diagram (ERD)
```
┌─────────────────┐
│      User       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ email           │
│ password        │
└────────┬────────┘
         │
         │ (1:N)
         │
    ┌────▼──────────┐         ┌──────────────┐
    │   Article     ├────────→│   Comment    │
    ├───────────────┤         ├──────────────┤
    │ id (PK)       │ (1:N)   │ id (PK)      │
    │ title         │         │ comment      │
    │ body          │         │ sentiment    │
    │ date          │         │ author_id(FK)│
    │ author_id(FK) │         └──────────────┘
    │ sentiment     │
    └───────────────┘
```

---

## 💻 Usage Guide

### Creating Your First Article

1. **Sign Up / Login**
   - Navigate to `/accounts/signup/` or `/accounts/login/`
   - Create account or log in with credentials

2. **Create Article**
   - Click "New Article" in navigation
   - Fill in title and content
   - Click "Save" to publish
   - Sentiment analysis runs automatically

3. **View Articles**
   - All articles visible on article list page
   - Click any article to view details
   - Add comments to engage with content

### Managing Articles

#### Edit Article
```bash
Navigate to: /articles/<id>/edit/
```

#### Delete Article
```bash
Navigate to: /articles/<id>/delete/
Confirm deletion
```

#### Add Comment
```bash
View article detail page → Fill comment form → Submit
Sentiment automatically analyzed
```

### Accessing Analytics Dashboard

```
URL: /analysis/dashboard/
Requires: Login
Shows: Sentiment trends, user stats, engagement metrics
```

---

## 🔌 API Endpoints

### Articles Endpoints
| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|----------------|
| GET | `/articles/` | List all articles | ❌ |
| GET | `/articles/<id>/` | Get article detail | ✅ |
| POST | `/articles/new/` | Create new article | ✅ |
| PUT | `/articles/<id>/edit/` | Update article | ✅ (Author only) |
| DELETE | `/articles/<id>/delete/` | Delete article | ✅ (Author only) |

### Authentication Endpoints
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/accounts/signup/` | User registration |
| GET/POST | `/accounts/login/` | User login |
| GET | `/accounts/logout/` | User logout |
| POST | `/accounts/password_change/` | Change password |
| POST | `/accounts/password_reset/` | Reset password |

### Analysis Endpoints
| Method | Endpoint | Purpose | Auth Required |
|--------|----------|---------|----------------|
| GET | `/analysis/dashboard/` | Analytics dashboard | ✅ |
| GET | `/analysis/sentiment-stats/` | Sentiment statistics | ✅ |

---

## 📸 Screenshots

### 1. Home Page
```
[SCREENSHOT PLACEHOLDER: Home page with navigation and featured articles]
- Featured articles display
- Navigation bar with authentication links
- Search functionality
- Dark/Light theme toggle
```

### 2. Article List Page
```
[SCREENSHOT PLACEHOLDER: Article listing page]
- All published articles
- Author information
- Publication date
- Sentiment indicator badge
- View/Edit/Delete buttons for own articles
```

### 3. Article Detail Page
```
[SCREENSHOT PLACEHOLDER: Single article view]
- Full article content
- Author profile section
- Comment section
- Add new comment form
- Sentiment analysis badge
```

### 4. Create/Edit Article
```
[SCREENSHOT PLACEHOLDER: Article creation form]
- Title input field
- Rich text editor for body
- Submit and Cancel buttons
- Preview functionality
```

### 5. User Authentication Pages
```
[SCREENSHOT PLACEHOLDER: Login & Registration]
- Login form (username/email + password)
- Sign up form (email, username, password confirmation)
- Password reset flow
- Password change form
```

### 6. Analytics Dashboard
```
[SCREENSHOT PLACEHOLDER: Sentiment analysis dashboard]
- Sentiment distribution pie chart (Positive/Negative/Neutral)
- Sentiment trends over time (line chart)
- User engagement metrics
- Top performing articles
- Comment sentiment breakdown
- Date range filters
```

### 7. Admin Panel
```
[SCREENSHOT PLACEHOLDER: Django admin interface]
- User management
- Article management
- Comment moderation
- Bulk operations
```

### 8. Theme Toggle
```
[SCREENSHOT PLACEHOLDER: Dark/Light theme]
- Dark theme version of all pages
- Light theme version of all pages
- Smooth theme transitions
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **ImportError: No module named 'django'**
```bash
# Solution: Ensure virtual environment is activated and packages installed
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

#### 2. **No such table: articles_article**
```bash
# Solution: Run database migrations
cd django_project
python manage.py migrate
```

#### 3. **Static files not loading (404 errors)**
```bash
# Solution: Collect static files
python manage.py collectstatic --noinput
```

#### 4. **STATIC_ROOT Error: ImproperlyConfigured**
```python
# Add to settings.py
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

#### 5. **Database is locked (SQLite)**
```bash
# Solution: Delete db.sqlite3 and run migrations again
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### 6. **Port 8000 already in use**
```bash
# Solution: Use different port
python manage.py runserver 8001
```

#### 7. **TextBlob Download Required (Sentiment Analysis)**
```bash
# Solution: Download required NLP data
python -m textblob.download_corpora
```

#### 8. **Permission Denied on Linux/macOS**
```bash
# Solution: Make files executable
chmod +x manage.py
chmod -R 755 django_project/
```

### Debug Mode

Enable detailed error messages during development:

```python
# In settings.py
DEBUG = True
ALLOWED_HOSTS = ['*']  # Only in development!
```

### Logging Configuration

```python
# In settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

## 🤝 Contributing

We welcome contributions from the community! Here's how to contribute:

### Getting Started

1. **Fork the Repository**
   ```bash
   Click "Fork" button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/news-app-using-django.git
   cd news_app_django_by_book
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Make Your Changes**
   - Follow PEP 8 code style
   - Write descriptive commit messages
   - Add tests for new functionality
   - Update documentation

5. **Commit Your Changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```

6. **Push to Your Branch**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Provide clear description of changes
   - Reference any related issues
   - Ensure all tests pass

### Code Style Guidelines

- **Python**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- **Django**: Follow [Django Coding Style](https://docs.djangoproject.com/en/stable/internals/contributing/coding-style/)
- **HTML/CSS**: Use semantic HTML and BEM methodology
- **JavaScript**: Use ES6+ standards

### Commit Message Format

```
[TYPE] Brief description (50 chars max)

Detailed explanation of changes (if needed)

- Bullet point 1
- Bullet point 2

Fixes #123
```

**Types**: feat, fix, docs, style, refactor, perf, test, chore

---

## 📄 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

### MIT License Summary
- ✅ Use for commercial purposes
- ✅ Modify the code
- ✅ Distribute the software
- ❌ Hold liability
- ❌ Provide warranty

---

## 👨‍💻 Author

**Niraj** - [GitHub Profile](https://github.com/Nirajjj11)

### Project Information
- **Repository**: [news-app-using-django](https://github.com/Nirajjj11/news-app-using-django)
- **Author**: Niraj
- **Created**: 2024
- **Last Updated**: April 2026
- **Status**: Active Development

---

## 📞 Support & Contact

- **Report Issues**: [GitHub Issues](https://github.com/Nirajjj11/news-app-using-django/issues)
- **Email**: niraj@example.com
- **Documentation**: [Django Official Docs](https://docs.djangoproject.com/)
- **TextBlob Docs**: [TextBlob](https://textblob.readthedocs.io/)

---

## 🎓 Learning Resources

### Django
- [Django Official Tutorial](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
- [Django for Beginners](https://djangoforbeginners.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)

### Sentiment Analysis
- [TextBlob Documentation](https://textblob.readthedocs.io/)
- [VADER Sentiment Analysis](https://github.com/cjhutto/vaderSentiment)
- [Natural Language Processing with Python](https://www.nltk.org/)

### Web Development
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.0/)
- [Python Official Guide](https://www.python.org/doc/)
- [Web Development Best Practices](https://developer.mozilla.org/)

---

## 🗺️ Roadmap

### Planned Features
- [ ] Advanced search with filters
- [ ] User notifications system
- [ ] Article recommendations engine
- [ ] Social sharing functionality
- [ ] Mobile app (React Native)
- [ ] API (Django REST Framework)
- [ ] Real-time notifications (WebSockets)
- [ ] Multi-language support
- [ ] SEO optimization
- [ ] Performance analytics

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Language** | Python |
| **Framework** | Django 6.0.4 |
| **License** | MIT |
| **Contributors** | 1 |
| **Last Update** | April 2026 |
| **Python Version** | 3.8+ |

---

## 🙏 Acknowledgments

- Django community for the amazing framework
- Bootstrap team for the responsive CSS framework
- TextBlob for NLP and sentiment analysis
- All contributors and supporters

---

## ⭐ Show Your Support

If this project helped you, please consider giving it a star! ⭐

```
https://github.com/Nirajjj11/news-app-using-django
```

---

**Happy Coding! 🚀**

---

*Last Updated: April 2026*
*For the latest updates, visit the [GitHub Repository](https://github.com/Nirajjj11/news-app-using-django)*
