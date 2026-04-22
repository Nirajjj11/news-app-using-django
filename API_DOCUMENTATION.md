# API Documentation

Complete API reference for the News App Django application. While currently implemented as traditional views, this documentation covers the existing endpoints and their functionality.

---

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Response Format](#response-format)
- [Status Codes](#status-codes)
- [Endpoints](#endpoints)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Examples](#examples)

---

## Overview

The News App Django provides a complete article management system with sentiment analysis. The API supports:

- Article CRUD operations
- User authentication
- Comment management
- Sentiment analysis
- Analytics data retrieval

**Current Implementation**: Django Class-Based Views with template rendering
**Future**: Django REST Framework API endpoints

---

## Authentication

### Session-Based Authentication (Current)

The application uses Django's session-based authentication:

1. User registers via `/accounts/signup/`
2. User logs in via `/accounts/login/`
3. Session cookie is set
4. Authenticated requests include the session cookie

### Protected Endpoints

Endpoints requiring authentication redirect to login page:
- All article detail pages
- All article edit/delete pages
- Comment creation
- Analytics dashboard

---

## Base URL

```
Development: http://localhost:8000
Production: https://yourdomain.com
```

---

## Response Format

### HTML Response (Current)
```html
<!DOCTYPE html>
<html>
<head>
    <!-- Page content -->
</head>
<body>
    <!-- Rendered template -->
</body>
</html>
```

### Future JSON Response Format
```json
{
    "status": "success|error",
    "data": {},
    "message": "Human-readable message",
    "timestamp": "2026-04-22T10:30:00Z"
}
```

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 302 | Redirect | Redirecting to another page |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Permission denied |
| 404 | Not Found | Resource not found |
| 500 | Server Error | Internal server error |

---

## Endpoints

### Articles

#### 1. List Articles
**Endpoint**: `GET /articles/`  
**Authentication**: Not required  
**Description**: Display all published articles  

**Response**: HTML page listing all articles

**Query Parameters**:
- `page` (integer): Page number for pagination
- `search` (string): Search articles by title or body

**Example**:
```bash
curl http://localhost:8000/articles/
curl http://localhost:8000/articles/?page=2
curl http://localhost:8000/articles/?search=django
```

---

#### 2. Get Article Detail
**Endpoint**: `GET /articles/<id>/`  
**Authentication**: Required (Login)  
**Description**: Display full article with comments  

**Parameters**:
- `id` (integer): Article primary key

**Response**: HTML page with article details

**Example**:
```bash
curl -b cookies.txt http://localhost:8000/articles/1/
```

**Error Responses**:
- 404: Article not found
- 302: Not authenticated (redirects to login)

---

#### 3. Create Article
**Endpoint**: `GET/POST /articles/new/`  
**Authentication**: Required  
**Description**: Create new article  

**GET Response**: Article creation form (HTML)

**POST Parameters**:
- `title` (string, required): Article title (max 255 chars)
- `body` (string, required): Article body content
- `csrfmiddlewaretoken` (string, required): CSRF token

**Example**:
```bash
# GET - Display form
curl -b cookies.txt http://localhost:8000/articles/new/

# POST - Create article
curl -X POST \
  -b cookies.txt \
  -d "title=My Article&body=Article content&csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/articles/new/
```

**Response on Success**: 
- Redirect (302) to article detail page
- Sentiment analysis runs automatically

**Error Responses**:
- 400: Form validation failed
- 401: User not authenticated

---

#### 4. Update Article
**Endpoint**: `GET/POST /articles/<id>/edit/`  
**Authentication**: Required (Author only)  
**Description**: Edit article (author only)  

**Parameters**:
- `id` (integer): Article primary key
- `title` (string): Updated title
- `body` (string): Updated content

**Example**:
```bash
curl -X POST \
  -b cookies.txt \
  -d "title=Updated Title&body=Updated body&csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/articles/1/edit/
```

**Response on Success**: Redirect to article detail page

**Error Responses**:
- 404: Article not found
- 403: User not author of article
- 401: User not authenticated

---

#### 5. Delete Article
**Endpoint**: `GET/POST /articles/<id>/delete/`  
**Authentication**: Required (Author only)  
**Description**: Delete article (author only)  

**Parameters**:
- `id` (integer): Article primary key

**Example**:
```bash
# GET - Confirmation page
curl -b cookies.txt http://localhost:8000/articles/1/delete/

# POST - Confirm deletion
curl -X POST \
  -b cookies.txt \
  -d "csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/articles/1/delete/
```

**Response on Success**: Redirect to article list page (302)

**Error Responses**:
- 404: Article not found
- 403: User not author
- 401: User not authenticated

---

### Comments

#### 1. Create Comment
**Endpoint**: `POST /articles/<article_id>/comments/`  
**Authentication**: Required  
**Description**: Add comment to article  

**Parameters**:
- `article_id` (integer): Article primary key
- `comment` (string, required): Comment text (max 140 chars)
- `csrfmiddlewaretoken` (string, required): CSRF token

**Example**:
```bash
curl -X POST \
  -b cookies.txt \
  -d "comment=Great article!&csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/articles/1/comments/
```

**Response on Success**: 
- Redirect (302) to article detail page
- Sentiment analysis runs automatically on comment

**Error Responses**:
- 400: Comment text too long (max 140 chars)
- 401: User not authenticated
- 404: Article not found

---

#### 2. Delete Comment
**Endpoint**: `POST /comments/<id>/delete/`  
**Authentication**: Required (Author only)  
**Description**: Delete comment (author only)  

**Parameters**:
- `id` (integer): Comment primary key

**Example**:
```bash
curl -X POST \
  -b cookies.txt \
  -d "csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/comments/1/delete/
```

**Response on Success**: Redirect to article detail page (302)

**Error Responses**:
- 404: Comment not found
- 403: User not comment author
- 401: User not authenticated

---

### Authentication

#### 1. Register (Sign Up)
**Endpoint**: `GET/POST /accounts/signup/`  
**Authentication**: Not required  
**Description**: Create new user account  

**POST Parameters**:
- `username` (string, required): Unique username
- `email` (string, required): Valid email address
- `password1` (string, required): Password
- `password2` (string, required): Password confirmation
- `csrfmiddlewaretoken` (string, required): CSRF token

**Example**:
```bash
curl -X POST \
  -d "username=newuser&email=user@example.com&password1=Pass123&password2=Pass123&csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/accounts/signup/
```

**Response on Success**: Redirect to login page (302)

**Error Responses**:
- 400: Username already exists
- 400: Password confirmation mismatch
- 400: Invalid email format

---

#### 2. Login
**Endpoint**: `GET/POST /accounts/login/`  
**Authentication**: Not required  
**Description**: Authenticate user  

**POST Parameters**:
- `username` (string, required): Username or email
- `password` (string, required): Password
- `csrfmiddlewaretoken` (string, required): CSRF token

**Example**:
```bash
curl -c cookies.txt -X POST \
  -d "username=testuser&password=Pass123&csrfmiddlewaretoken=TOKEN" \
  http://localhost:8000/accounts/login/
```

**Response on Success**: 
- Sets session cookie
- Redirect to home page (302)

**Error Responses**:
- 401: Invalid credentials

---

#### 3. Logout
**Endpoint**: `GET/POST /accounts/logout/`  
**Authentication**: Required  
**Description**: Logout user  

**Example**:
```bash
curl -b cookies.txt http://localhost:8000/accounts/logout/
```

**Response on Success**: Redirect to home page (302)

---

#### 4. Password Change
**Endpoint**: `GET/POST /accounts/password_change/`  
**Authentication**: Required  
**Description**: Change user password  

**Parameters**:
- `old_password` (string, required): Current password
- `new_password1` (string, required): New password
- `new_password2` (string, required): Confirmation

**Example**:
```bash
curl -b cookies.txt -X POST \
  -d "old_password=OldPass&new_password1=NewPass123&new_password2=NewPass123" \
  http://localhost:8000/accounts/password_change/
```

**Response on Success**: Redirect to password change done page

**Error Responses**:
- 400: Incorrect old password
- 400: Password mismatch

---

#### 5. Password Reset
**Endpoint**: `GET/POST /accounts/password_reset/`  
**Authentication**: Not required  
**Description**: Initiate password reset  

**Parameters**:
- `email` (string, required): User email address

**Example**:
```bash
curl -X POST \
  -d "email=user@example.com" \
  http://localhost:8000/accounts/password_reset/
```

**Response on Success**: Email sent with reset link

---

### Analysis

#### 1. Dashboard
**Endpoint**: `GET /analysis/dashboard/`  
**Authentication**: Required  
**Description**: View sentiment analytics dashboard  

**Response**: HTML dashboard with:
- Sentiment distribution chart
- Sentiment trends over time
- User engagement metrics
- Comment sentiment breakdown

**Example**:
```bash
curl -b cookies.txt http://localhost:8000/analysis/dashboard/
```

**Error Responses**:
- 401: User not authenticated

---

### Static Pages

#### 1. Home Page
**Endpoint**: `GET /`  
**Authentication**: Not required  
**Description**: Homepage with featured articles  

**Example**:
```bash
curl http://localhost:8000/
```

---

## Error Handling

### Error Response Format (HTML)

The application returns HTML error pages:

```html
<!-- 404 Not Found -->
<html>
    <body>
        <h1>404 - Page Not Found</h1>
        <p>The requested resource was not found.</p>
    </body>
</html>

<!-- 403 Forbidden -->
<html>
    <body>
        <h1>403 - Permission Denied</h1>
        <p>You don't have permission to access this resource.</p>
    </body>
</html>
```

### Common Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| 404 Not Found | Article/resource doesn't exist | Check article ID, try listing articles |
| 403 Forbidden | Not article author | Only article author can edit/delete |
| 401 Unauthorized | Not logged in | Log in first via `/accounts/login/` |
| 400 Bad Request | Invalid form data | Check form parameters |
| 302 Redirect | Post successful | Follow redirect to view result |

---

## Rate Limiting

Currently not implemented. Recommended for production:

```python
# settings.py with django-ratelimit
RATELIMIT_ENABLE = True
RATELIMIT_DEFAULT = '100/h'  # 100 requests per hour
```

---

## Examples

### Complete User Flow

```bash
# 1. Register new user
curl -c cookies.txt -X POST \
  http://localhost:8000/accounts/signup/ \
  -d "username=testuser&email=test@example.com&password1=Test123&password2=Test123"

# 2. Login
curl -b cookies.txt -c cookies.txt -X POST \
  http://localhost:8000/accounts/login/ \
  -d "username=testuser&password=Test123"

# 3. View articles
curl -b cookies.txt http://localhost:8000/articles/

# 4. Create article (need CSRF token from form page)
curl -b cookies.txt -X POST \
  http://localhost:8000/articles/new/ \
  -d "title=My First Article&body=This is my article content&csrfmiddlewaretoken=TOKEN"

# 5. View article
curl -b cookies.txt http://localhost:8000/articles/1/

# 6. Add comment
curl -b cookies.txt -X POST \
  http://localhost:8000/articles/1/comments/ \
  -d "comment=Great article!&csrfmiddlewaretoken=TOKEN"

# 7. View analytics
curl -b cookies.txt http://localhost:8000/analysis/dashboard/

# 8. Logout
curl -b cookies.txt http://localhost:8000/accounts/logout/
```

### Using Python Requests

```python
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://localhost:8000'

# Create session
session = requests.Session()

# 1. Signup
signup_data = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password1': 'Test123',
    'password2': 'Test123',
}
response = session.post(f'{BASE_URL}/accounts/signup/', data=signup_data)
print(f"Signup: {response.status_code}")

# 2. Login
login_data = {
    'username': 'testuser',
    'password': 'Test123',
}
response = session.post(f'{BASE_URL}/accounts/login/', data=login_data)
print(f"Login: {response.status_code}")

# 3. Get CSRF token from form
response = session.get(f'{BASE_URL}/articles/new/')
soup = BeautifulSoup(response.content, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

# 4. Create article
article_data = {
    'title': 'My Article',
    'body': 'Article content here',
    'csrfmiddlewaretoken': csrf_token,
}
response = session.post(f'{BASE_URL}/articles/new/', data=article_data)
print(f"Create Article: {response.status_code}")

# 5. List articles
response = session.get(f'{BASE_URL}/articles/')
print(f"List Articles: {response.status_code}")
```

---

## Future REST API

A Django REST Framework API is planned with the following endpoints:

```
# Articles
GET    /api/articles/                 - List articles
POST   /api/articles/                 - Create article
GET    /api/articles/<id>/            - Get article
PUT    /api/articles/<id>/            - Update article
DELETE /api/articles/<id>/            - Delete article

# Comments
GET    /api/articles/<id>/comments/   - List comments
POST   /api/articles/<id>/comments/   - Create comment
DELETE /api/comments/<id>/            - Delete comment

# Analytics
GET    /api/analytics/sentiment/      - Sentiment stats
GET    /api/analytics/trends/         - Sentiment trends

# Authentication (Token)
POST   /api/token/                    - Get access token
POST   /api/token/refresh/            - Refresh token
```

---

## SDK/Client Libraries

### JavaScript (Coming Soon)
```javascript
const client = new NewsAppClient('http://localhost:8000');

// List articles
const articles = await client.articles.list();

// Create article
const article = await client.articles.create({
    title: 'My Article',
    body: 'Content...'
});
```

### Python (Coming Soon)
```python
from newsapp import Client

client = Client('http://localhost:8000')

# List articles
articles = client.articles.list()

# Create article
article = client.articles.create(
    title='My Article',
    body='Content...'
)
```

---

## Support & Issues

- **Report Issues**: [GitHub Issues](https://github.com/Nirajjj11/news-app-using-django/issues)
- **Documentation**: [Main README](README.md)
- **Development**: [Development Guide](DEVELOPMENT.md)

---

**Last Updated**: April 22, 2026  
**API Version**: 1.0 (HTML/Template based)
