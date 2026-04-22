# Development Guide

This guide provides detailed instructions for setting up a development environment and best practices for contributing to the News App Django project.

---

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Architecture](#project-architecture)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Debugging](#debugging)
- [Code Style & Quality](#code-style--quality)
- [Common Development Tasks](#common-development-tasks)
- [Troubleshooting](#troubleshooting)

---

## Development Environment Setup

### Prerequisites

- Python 3.8+
- Git
- pip
- Virtual environment support

### Step-by-Step Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/Nirajjj11/news-app-using-django.git
   cd news_app_django_by_book
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create Environment File**
   ```bash
   # Copy example to .env
   copy .env.example .env  # Windows
   cp .env.example .env   # macOS/Linux
   
   # Edit .env with your configuration
   ```

5. **Navigate to Project**
   ```bash
   cd django_project
   ```

6. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

Access the application at `http://localhost:8000`

---

## Project Architecture

### App Structure

#### accounts/
- User registration
- Authentication
- Profile management
- Password management

Key files:
- `models.py`: User profile extensions (if any)
- `views.py`: Auth views (signup, login, logout)
- `forms.py`: Registration and login forms
- `urls.py`: Auth URL patterns

#### articles/
- Article CRUD operations
- Comments management
- Sentiment analysis integration

Key files:
- `models.py`: Article and Comment models
- `views.py`: ListView, DetailView, CreateView, UpdateView, DeleteView
- `forms.py`: Article and Comment forms
- `admin.py`: Article and Comment admin configuration
- `urls.py`: Article URL patterns
- `services.py`: Business logic for articles

#### analysis/
- Sentiment analysis
- Analytics dashboard
- Trending data

Key files:
- `views.py`: Dashboard view
- `services.py`: Sentiment analysis logic
- `utils.py`: Data aggregation utilities
- `urls.py`: Analysis URL patterns

#### pages/
- Static pages (Home, About)
- Navigation

Key files:
- `views.py`: Page views
- `urls.py`: Page URL patterns

### Design Patterns

#### Class-Based Views
```python
# List View
class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'

# Detail View with Login
class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article_detail.html'

# Update with Permission Check
class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['title', 'body']
    
    def test_func(self):
        return self.get_object().author == self.request.user
```

#### Form Handling
```python
# In Views
class CommentCreateView(LoginRequiredMixin, CreateView):
    form_class = CommentForm
    template_name = 'comment_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

---

## Development Workflow

### Creating a New Feature

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   ```bash
   # Edit files
   # Create tests
   # Update documentation
   ```

3. **Run Tests**
   ```bash
   python manage.py test
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "🎨 Add your feature"
   ```

5. **Push to GitHub**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in description
   - Request reviewers

### Branch Naming Convention

- Feature: `feature/short-description`
- Bug fix: `fix/short-description`
- Documentation: `docs/short-description`
- Performance: `perf/short-description`
- Refactor: `refactor/short-description`

---

## Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test articles

# Run specific test class
python manage.py test articles.tests.ArticleModelTests

# Run with verbosity
python manage.py test --verbosity=2

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report in htmlcov/
```

### Writing Tests

#### Model Tests
```python
# articles/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Article

class ArticleModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_article_creation(self):
        article = Article.objects.create(
            title='Test Article',
            body='Test body',
            author=self.user
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.user)
```

#### View Tests
```python
from django.test import Client, TestCase
from django.urls import reverse

class ArticleViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.article = Article.objects.create(
            title='Test',
            body='Body',
            author=self.user
        )
    
    def test_article_list_view(self):
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test')
    
    def test_article_detail_requires_login(self):
        response = self.client.get(reverse('article_detail', args=[self.article.pk]))
        self.assertEqual(response.status_code, 302)  # Redirect
```

---

## Debugging

### Django Debug Toolbar

1. **Install**
   ```bash
   pip install django-debug-toolbar
   ```

2. **Add to INSTALLED_APPS** (in `settings.py`)
   ```python
   INSTALLED_APPS = [
       ...
       'debug_toolbar',
   ]
   ```

3. **Add to MIDDLEWARE**
   ```python
   MIDDLEWARE = [
       ...
       'debug_toolbar.middleware.DebugToolbarMiddleware',
   ]
   ```

4. **Configure URLs** (in `urls.py`)
   ```python
   from django.conf import settings
   
   if settings.DEBUG:
       import debug_toolbar
       urlpatterns = [
           path('__debug__/', include(debug_toolbar.urls)),
       ] + urlpatterns
   ```

### Using Logging

```python
import logging

logger = logging.getLogger(__name__)

# In views
def my_view(request):
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
```

### Using Python Debugger (pdb)

```python
import pdb

def problematic_function():
    pdb.set_trace()  # Execution will pause here
    # Use: n (next), s (step), c (continue), p variable
```

### Django Shell

```bash
python manage.py shell

# In shell
from articles.models import Article
articles = Article.objects.all()
article = articles.first()
print(article.title)
```

---

## Code Style & Quality

### PEP 8 Compliance

Use `flake8`:
```bash
pip install flake8
flake8 django_project/
```

Configure in `setup.cfg`:
```ini
[flake8]
max-line-length = 99
exclude = .git,__pycache__,.venv
```

### Import Organization

Use `isort`:
```bash
pip install isort
isort django_project/
```

Correct import order:
1. Standard library
2. Third-party packages
3. Local imports

```python
# Good
from django.shortcuts import render
from django.http import HttpResponse
from articles.models import Article
from .views import my_view
```

### Type Hints

Add type annotations:
```python
from typing import Optional, List
from django.contrib.auth.models import User

def get_user_articles(user: User) -> List[Article]:
    return Article.objects.filter(author=user)

def get_optional_value() -> Optional[str]:
    return None
```

### Docstrings

Follow PEP 257:
```python
def calculate_sentiment(text: str) -> str:
    """
    Analyze and classify text sentiment.
    
    Args:
        text: The input text to analyze
        
    Returns:
        Sentiment classification: 'Positive', 'Negative', or 'Neutral'
        
    Raises:
        ValueError: If text is empty
        
    Example:
        >>> calculate_sentiment("I love this!")
        'Positive'
    """
    if not text:
        raise ValueError("Text cannot be empty")
    # Implementation...
```

---

## Common Development Tasks

### Creating a Migration

```bash
# After modifying models
python manage.py makemigrations

# Review the migration file
cat django_project/articles/migrations/000X_*.py

# Apply migrations
python manage.py migrate

# Specific app migration
python manage.py migrate articles
```

### Creating a New App

```bash
python manage.py startapp myapp

# Register in settings.py
INSTALLED_APPS = [
    ...
    'myapp',
]
```

### Running Specific Commands

```bash
# Create admin user
python manage.py createsuperuser

# Change password
python manage.py changepassword username

# Clear cache
python manage.py clear_cache

# Collect static files
python manage.py collectstatic

# Load fixtures
python manage.py loaddata fixture_name

# Dump data
python manage.py dumpdata articles > articles_backup.json
```

### Database Operations

```bash
# Reset database (development only)
python manage.py flush

# Check database state
python manage.py dbshell

# SQL for migrations
python manage.py sqlmigrate articles 0001
```

---

## Troubleshooting

### Common Issues

#### 1. Migration Conflicts
```bash
# Solution: Check migration history
python manage.py showmigrations

# Fake migration if needed (use carefully!)
python manage.py migrate --fake
```

#### 2. Import Errors
```bash
# Solution: Ensure virtual environment is activated
which python  # Should show .venv path

# Re-install dependencies
pip install -r requirements.txt
```

#### 3. Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Clear cache
rm -rf staticfiles/
```

#### 4. Database Locked (SQLite)
```bash
# Solution: Remove and recreate
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

#### 5. Port Already in Use
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

---

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)

---

**Last Updated**: April 22, 2026
