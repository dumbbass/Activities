# User Authentication API

This is a Django-based REST API that provides user authentication functionality using JWT tokens.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Start the server:
```bash
python manage.py runserver
```

## API Endpoints

### Register User
- **Method**: POST
- **URL**: `/api/auth/register/`
- **Headers**: 
  - Content-Type: application/json
- **Request Body**:
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```
- **Response** (200 OK):
```json
{
    "message": "User registered successfully",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string"
    }
}
```

### Login
- **Method**: POST
- **URL**: `/api/auth/login/`
- **Headers**: 
  - Content-Type: application/json
- **Request Body**:
```json
{
    "username": "string",
    "password": "string"
}
```
- **Response** (200 OK):
```json
{
    "access": "string (JWT token)",
    "refresh": "string (JWT refresh token)"
}
```

### Protected Route Example
- **Method**: GET
- **URL**: `/api/protected/`
- **Headers**: 
  - Authorization: Bearer <access_token>
- **Response** (200 OK):
```json
{
    "message": "This is a protected route",
    "user": {
        "id": "integer",
        "username": "string",
        "email": "string"
    }
}
```

### Refresh Token
- **Method**: POST
- **URL**: `/api/auth/token/refresh/`
- **Headers**: 
  - Content-Type: application/json
- **Request Body**:
```json
{
    "refresh": "string (JWT refresh token)"
}
```
- **Response** (200 OK):
```json
{
    "access": "string (new JWT token)"
}
```

## Error Responses

### Invalid Credentials (401 Unauthorized)
```json
{
    "detail": "Invalid credentials"
}
```

### Missing Token (401 Unauthorized)
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### Invalid Token (401 Unauthorized)
```json
{
    "detail": "Token is invalid or expired"
}
``` 