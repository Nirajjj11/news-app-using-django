# Project Structure Documentation

Complete overview of the News App Django project directory structure, file purposes, and organization.

---

## Table of Contents

- [Directory Overview](#directory-overview)
- [Root Level Files](#root-level-files)
- [django_project Directory](#django_project-directory)
- [Application Modules](#application-modules)
- [Templates Directory](#templates-directory)
- [Static Files](#static-files)
- [Database & Migrations](#database--migrations)
- [File Naming Conventions](#file-naming-conventions)
- [Adding New Features](#adding-new-features)

---

## Directory Overview

```
news_app_django_by_book/
├── django_project/              # Main Django project container
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── README.md                    # Main documentation
├── CONTRIBUTING.md              # Contributing guidelines
├── DEVELOPMENT.md               # Development guide
├── DEPLOYMENT.md                # Deployment instructions
├── API_DOCUMENTATION.md         # API reference
├── CHANGELOG.md                 # Version history
├── SECURITY.md                  # Security policy
└── LICENSE                      # MIT License
```

---

## Root Level Files

### Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Main project documentation | Everyone |
| `CONTRIBUTING.md` | Contribution guidelines | Contributors |
| `DEVELOPMENT.md` | Development setup & workflow | Developers |
| `DEPLOYMENT.md` | Production deployment guide | DevOps/Admins |
| `API_DOCUMENTATION.md` | API endpoints reference | API users |
| `SECURITY.md` | Security policies & practices | Security team |
| `CHANGELOG.md` | Version history & releases | Everyone |

### Configuration Files

| File | Purpose |
|------|---------|
| `.env.example` | Environment variables template |
| `.gitignore` | Git ignore patterns |
| `LICENSE` | MIT License |

### Virtual Environment
| Directory | Purpose |
|-----------|---------|
| `.venv/` | Virtual environment (ignored in git) |

---

## django_project Directory

The main Django project directory containing all application code.

```
django_project/
├── manage.py                    # Django CLI
├── db.sqlite3                   # SQLite database (dev only)
├── requirements.txt             # Python dependencies
├── django_project/              # Project settings package
├── accounts/                    # User authentication app
├── articles/                    # Article management app
├── analysis/                    # Sentiment analysis app
├── pages/                       # Static pages app
├── templates/                   # HTML templates
├── static/                      # Static files (CSS, JS, images)
├── staticfiles/                 # Collected static files
└── media/                       # User-uploaded files
```

---

## Application Modules

### 1. django_project/ (Project Configuration)

**Location**: `django_project/django_project/`

Contains core Django project settings and configuration.

#### Files:

```
django_project/
├── __init__.py                  # Package marker
├── asgi.py                      # ASGI configuration for async servers
├── wsgi.py                      # WSGI configuration for production
├── settings.py                  # Main project settings (5 + KB)
└── urls.py                      # Root URL router
```

#### settings.py Structure
```python
# Imports & paths
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

# Django configuration
DEBUG = True
SECRET_KEY = 'xxx'
ALLOWED_HOSTS = []

# Installed apps
INSTALLED_APPS = [
    'django.contrib.*',
    'crispy_forms',
    'accounts',
    'articles',
    'analysis',
    'pages',
]

# Middleware (request/response processors)
MIDDLEWARE = [...]

# Templates
TEMPLATES = [...]

# Database
DATABASES = {'default': {...}}

# Password validation
AUTH_PASSWORD_VALIDATORS = [...]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'IST'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles/'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap5'
```

#### urls.py Structure
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
    path('analysis/', include('analysis.urls')),
    path('', include('pages.urls')),
]
```

---

### 2. accounts/ (User Authentication)

**Location**: `django_project/accounts/`

User registration, login, logout, and profile management.

#### Files:

```
accounts/
├── __init__.py
├── admin.py                     # Register models in admin
├── apps.py                      # App configuration
├── forms.py                     # Registration/Login forms
├── models.py                    # User profile models
├── tests.py                     # Unit tests
├── urls.py                      # Auth URL patterns
├── views.py                     # Auth views
└── migrations/                  # Database migrations
    ├── __init__.py
    └── 0001_initial.py
```

#### Key Views
- `SignUpView` - User registration
- `LoginView` - User login
- `LogoutView` - User logout
- `PasswordChangeView` - Change password
- `PasswordResetView` - Reset password

#### Key URLs
```
/accounts/signup/                - Registration page
/accounts/login/                 - Login page
/accounts/logout/                - Logout
/accounts/password_change/       - Change password
/accounts/password_reset/        - Reset password
```

#### models.py
```python
# Django's built-in User model is used
# No custom model needed (extensible for future use)
```

#### forms.py
```python
# UserCreationForm - Register new user
# AuthenticationForm - Login form
# PasswordChangeForm - Change password
# PasswordResetForm - Initiate password reset
```

---

### 3. articles/ (Article Management)

**Location**: `django_project/articles/`

Core app for article CRUD operations, comments, and sentiment tracking.

#### Files:

```
articles/
├── __init__.py
├── admin.py                     # Article & Comment admin config
├── apps.py                      # App configuration
├── forms.py                     # Article & Comment forms
├── models.py                    # Article & Comment models
├── tests.py                     # Unit tests
├── urls.py                      # Article URL patterns
├── views.py                     # Article views (CRUD operations)
├── utils.py                     # Utility functions
└── migrations/                  # Database migrations
    ├── __init__.py
    ├── 0001_initial.py
    ├── 0002_rename_articles_article.py
    ├── 0003_comment.py
    ├── 0004_article_dislikes_article_likes.py
    ├── 0005_remove_article_dislikes_remove_article_likes.py
    ├── 0006_comment_date.py
    ├── 0007_remove_comment_date.py
    └── 0008_article_sentiment_comment_sentiment.py
```

#### models.py

```python
class Article(models.Model):
    """
    Article model for news/blog posts.
    
    Fields:
    - title: CharField(255) - Article headline
    - body: TextField() - Full article content
    - date: DateTimeField(auto_now_add=True) - Creation timestamp
    - author: ForeignKey(User) - Article creator
    - sentiment: CharField(20) - Sentiment classification
    """
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    sentiment = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    """
    Comment model for article discussions.
    
    Fields:
    - article: ForeignKey(Article) - Associated article
    - comment: CharField(140) - Comment text
    - author: ForeignKey(User) - Comment creator
    - sentiment: CharField(20) - Sentiment classification
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=140)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    sentiment = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.comment[:50]
```

#### views.py

```python
class ArticleListView(ListView):
    """Display all articles publicly."""
    model = Article
    template_name = 'article_list.html'

class ArticleDetailView(LoginRequiredMixin, DetailView):
    """Display single article with comments."""
    model = Article
    template_name = 'article_detail.html'

class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Create new article."""
    model = Article
    fields = ['title', 'body']
    template_name = 'article_new.html'

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit article (author only)."""
    model = Article
    fields = ['title', 'body']
    template_name = 'article_edit.html'
    
    def test_func(self):
        return self.get_object().author == self.request.user

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete article (author only)."""
    model = Article
    template_name = 'article_delete.html'
    success_url = reverse_lazy('article_list')
```

#### forms.py

```python
class ArticleForm(forms.ModelForm):
    """Form for creating/editing articles."""
    class Meta:
        model = Article
        fields = ['title', 'body']

class CommentForm(forms.ModelForm):
    """Form for creating comments."""
    class Meta:
        model = Comment
        fields = ['comment']
```

#### Key URLs
```
/articles/                       - List articles
/articles/<id>/                  - View article
/articles/new/                   - Create article
/articles/<id>/edit/             - Edit article
/articles/<id>/delete/           - Delete article
/articles/<id>/comment/          - Add comment
```

---

### 4. analysis/ (Sentiment Analysis)

**Location**: `django_project/analysis/`

Sentiment analysis, analytics dashboard, and trend visualization.

#### Files:

```
analysis/
├── __init__.py
├── admin.py                     # Analysis admin config
├── apps.py                      # App configuration
├── models.py                    # Analysis models (if needed)
├── tests.py                     # Unit tests
├── urls.py                      # Analysis URL patterns
├── views.py                     # Dashboard & analysis views
├── services.py                  # Sentiment analysis logic
├── utils.py                     # Data aggregation utilities
└── migrations/                  # Database migrations
    └── __init__.py
```

#### services.py

```python
from textblob import TextBlob

def get_sentiment(text):
    """
    Analyze text sentiment using TextBlob.
    
    Returns: 'Positive', 'Negative', or 'Neutral'
    """
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

def get_user_sentiment_summary(user):
    """Get sentiment statistics for user."""
    articles = Article.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)
    
    data = {
        "positive": 0,
        "negative": 0,
        "neutral": 0
    }
    
    for item in list(articles) + list(comments):
        if item.sentiment == "Positive":
            data["positive"] += 1
        elif item.sentiment == "Negative":
            data["negative"] += 1
        else:
            data["neutral"] += 1
    
    return data
```

#### views.py

```python
class DashboardView(LoginRequiredMixin, TemplateView):
    """Analytics dashboard view."""
    template_name = 'analysis/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add sentiment analysis data
        context['sentiment_stats'] = self.get_sentiment_stats()
        return context
    
    def get_sentiment_stats(self):
        """Aggregate sentiment data for dashboard."""
        # Fetch and process sentiment data
        pass
```

#### Key URLs
```
/analysis/dashboard/             - Analytics dashboard
/analysis/sentiment-stats/       - Sentiment statistics
```

---

### 5. pages/ (Static Pages)

**Location**: `django_project/pages/`

Static pages like home and about.

#### Files:

```
pages/
├── __init__.py
├── admin.py                     # Pages admin config
├── apps.py                      # App configuration
├── models.py                    # Page models (if needed)
├── tests.py                     # Unit tests
├── urls.py                      # Page URL patterns
├── views.py                     # Page views
└── migrations/
    └── __init__.py
```

#### views.py

```python
class HomePageView(TemplateView):
    """Home page view."""
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Featured articles
        context['featured_articles'] = Article.objects.all()[:5]
        return context
```

#### Key URLs
```
/                                - Home page
/about/                          - About page (if exists)
```

---

## Templates Directory

**Location**: `django_project/templates/`

Django HTML templates using Bootstrap 5 for styling.

```
templates/
├── base.html                    # Base layout template
├── home.html                    # Homepage
├── article_list.html            # Article listing
├── article_detail.html          # Single article view
├── article_new.html             # Create article form
├── article_edit.html            # Edit article form
├── article_delete.html          # Delete confirmation
│
├── analysis/
│   └── dashboard.html           # Sentiment analysis dashboard
│
└── registration/                # Authentication templates
    ├── login.html               # Login form
    ├── signup.html              # Registration form
    ├── password_change_form.html
    ├── password_change_done.html
    ├── password_reset_form.html
    ├── password_reset_done.html
    ├── password_reset_confirm.html
    └── password_reset_complete.html
```

### Template Hierarchy

```
base.html (Master layout)
├── Page title block
├── Navigation block
├── Content block
├── Sidebar block (optional)
└── Footer block
```

### base.html Structure

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Meta tags -->
    <!-- Bootstrap CSS -->
    <!-- Custom CSS -->
</head>
<body>
    <!-- Navigation bar -->
    <!-- Messages/Alerts -->
    {% block content %}
    <!-- Page content -->
    {% endblock %}
    <!-- Footer -->
    <!-- Bootstrap JS -->
</body>
</html>
```

---

## Static Files

**Location**: `django_project/static/`

CSS, JavaScript, and image files.

```
static/
├── css/
│   └── style.css                # Custom CSS styles
│       - Navigation styles
│       - Form styles
│       - Button styles
│       - Responsive styles
│       - Dark theme
│
└── js/
    └── theme.js                 # Theme toggle functionality
        - Dark/Light mode toggle
        - Local storage persistence
        - DOM manipulation
```

### staticfiles/ (Collected for Production)

```
staticfiles/
├── admin/                       # Django admin static files
│   ├── css/
│   ├── js/
│   └── img/
├── css/
│   └── style.css
└── js/
    └── theme.js
```

Run to collect static files:
```bash
python manage.py collectstatic
```

---

## Database & Migrations

### db.sqlite3 (Development Only)

SQLite database for development. **Never commit to Git.**

### migrations/ Directory

Each app has a migrations folder:

```
articles/migrations/
├── __init__.py
├── 0001_initial.py              # Create Article & Comment models
├── 0002_rename_articles_article.py
├── 0003_comment.py              # Add Comment model
├── 0004_article_dislikes_article_likes.py
├── 0005_remove_article_dislikes_remove_article_likes.py
├── 0006_comment_date.py
├── 0007_remove_comment_date.py
└── 0008_article_sentiment_comment_sentiment.py
```

### Migration Workflow

```bash
# 1. Create migration after model changes
python manage.py makemigrations articles

# 2. Review migration file
cat articles/migrations/000X_auto_xxxx.py

# 3. Apply migration
python manage.py migrate articles

# 4. Show migration status
python manage.py showmigrations articles
```

---

## Media Directory

**Location**: `django_project/media/`

User-uploaded files (images, documents).

```
media/
├── articles/                    # Article images
├── profiles/                    # User profile pictures
└── uploads/                     # General uploads
```

---

## File Naming Conventions

### Python Files

- **Models**: `models.py` (singular model class names)
- **Views**: `views.py` (PascalCase for classes)
- **Forms**: `forms.py` (PascalCase for form classes)
- **Tests**: `tests.py` (PascalCase for test classes)
- **URLs**: `urls.py` (snake_case for URL names)
- **Utilities**: `utils.py` or `services.py`

### HTML Templates

- **Base**: `base.html`
- **Models**: `modelname_list.html`, `modelname_detail.html`
- **Actions**: `modelname_new.html`, `modelname_edit.html`, `modelname_delete.html`

### CSS/JavaScript

- Use kebab-case for class names
- Use snake_case for file names
- Prefix theme styles: `theme.js`

---

## Adding New Features

### 1. Create New App

```bash
python manage.py startapp myfeature
```

### 2. App Structure

```
myfeature/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── views.py
└── migrations/
    └── __init__.py
```

### 3. Register App

**File**: `django_project/settings.py`

```python
INSTALLED_APPS = [
    ...
    'myfeature',
]
```

### 4. Create Models

**File**: `myfeature/models.py`

### 5. Create Migrations

```bash
python manage.py makemigrations myfeature
python manage.py migrate
```

### 6. Create Views

**File**: `myfeature/views.py`

### 7. Create Forms

**File**: `myfeature/forms.py`

### 8. Create URLs

**File**: `myfeature/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MyView.as_view(), name='my_view'),
]
```

### 9. Include in Root URLs

**File**: `django_project/urls.py`

```python
urlpatterns = [
    path('myfeature/', include('myfeature.urls')),
]
```

### 10. Create Templates

```
templates/
└── myfeature/
    ├── myfeature_list.html
    ├── myfeature_detail.html
    └── myfeature_form.html
```

---

## Best Practices

### Organization
- Keep models focused and single-purpose
- Use separate files for large views/forms
- Organize templates by app
- Use static file structure for scalability

### Code Style
- Follow PEP 8 for Python
- Use meaningful variable names
- Add docstrings to functions/classes
- Comment complex logic

### Performance
- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for M2M relationships
- Index frequently queried fields
- Implement caching for expensive operations

### Testing
- Write tests for all models
- Write tests for all views
- Aim for 80%+ code coverage
- Use fixtures for test data

---

**Last Updated**: April 22, 2026
