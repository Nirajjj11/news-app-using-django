# Contributing to News App Django

First off, thank you for considering contributing to News App Django! It's people like you that make News App Django such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details**: Python version, Django version, OS, etc.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and the expected enhanced behavior**
* **Explain why this enhancement would be useful**
* **List similar features in other projects, if applicable**

### Pull Requests

* Fill in the required template
* Follow the Python/Django style guides (see below)
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
  * 🎨 `:art:` when improving the format/structure of the code
  * 🐛 `:bug:` when fixing a bug
  * ✨ `:sparkles:` when adding a new feature
  * 📝 `:memo:` when writing docs
  * ⚡ `:zap:` when improving performance
  * ✅ `:white_check_mark:` when adding tests
  * 🔒 `:lock:` when dealing with security
  * ⬆️ `:arrow_up:` when upgrading dependencies
  * ⬇️ `:arrow_down:` when downgrading dependencies

### Python Style Guide

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

* Use 4 spaces for indentation
* Use snake_case for variables and functions
* Use PascalCase for classes
* Maximum line length is 99 characters
* Use meaningful variable names
* Add docstrings to all functions and classes

Example:
```python
def get_article_sentiment(article_id):
    """
    Retrieve sentiment analysis for an article.
    
    Args:
        article_id (int): The ID of the article
        
    Returns:
        dict: Dictionary containing sentiment data
        
    Raises:
        Article.DoesNotExist: If article not found
    """
    article = Article.objects.get(id=article_id)
    return article.get_sentiment()
```

### Django Style Guide

* Follow [Django Coding Style](https://docs.djangoproject.com/en/stable/internals/contributing/coding-style/)
* Use Django ORM instead of raw SQL
* Use Django's class-based views when appropriate
* Use Django's built-in template tags and filters
* Keep models focused and single-purpose
* Use Django's built-in authentication system

### HTML/CSS Style Guide

* Use semantic HTML5 elements
* Follow BEM (Block Element Modifier) naming convention for CSS classes
* Use lowercase for HTML tags and attributes
* Use double quotes for attribute values
* Indent with 2 spaces in HTML/CSS files

### JavaScript Style Guide

* Use ES6+ standards
* Use `const` by default, `let` if you need to reassign
* Use meaningful variable names
* Add comments for complex logic
* Use arrow functions for callbacks

## Setting Up Your Development Environment

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/news-app-using-django.git
   cd news_app_django_by_book
   ```

3. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

4. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file from the template:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env  # macOS/Linux
   ```

6. Run migrations:
   ```bash
   cd django_project
   python manage.py migrate
   python manage.py createsuperuser
   ```

7. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Running Tests

Run the full test suite:
```bash
python manage.py test
```

Run tests for a specific app:
```bash
python manage.py test articles
```

Run a specific test class:
```bash
python manage.py test articles.tests.ArticleTests
```

Run with coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## Additional Notes

### Project Structure

* Keep models in `models.py`
* Keep views in `views.py`
* Keep forms in `forms.py`
* Keep utilities in `utils.py`
* Keep services (like sentiment analysis) in `services.py`
* Create new files only if they become too large (> 300 lines)

### Database Migrations

* Always create migrations for model changes:
  ```bash
  python manage.py makemigrations
  ```
* Review migration files before committing
* Use meaningful migration names
* Keep migrations small and focused

### Documentation

* Update README.md if adding new features
* Update docstrings for all new functions/classes
* Add inline comments for complex logic
* Update CHANGELOG if maintaining one

### Performance Considerations

* Use `select_related()` for ForeignKey relationships
* Use `prefetch_related()` for reverse relationships and M2M
* Use database indexing for frequently queried fields
* Cache expensive operations
* Avoid N+1 queries

## Recognition

Contributors will be recognized in:
* README.md contributors section
* Project releases/changelog
* GitHub contributor graphs

## Questions?

Feel free to create an issue or reach out to the project maintainers.

---

Thank you for your interest in contributing to News App Django! 🎉
