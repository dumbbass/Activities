# Django REST API with Authentication and Rate Limiting

This project implements a RESTful API with user authentication, JWT tokens, and rate limiting.

## Features

- User authentication with JWT tokens
- Rate limiting for all API endpoints
- CRUD operations for Products, Orders, and Posts
- Like functionality for posts
- Modern UI for testing the API

## File Upload Feature

The API now supports file uploads for user profile photos during registration. The following restrictions apply:

- Only image files are accepted (JPG, JPEG, PNG, WebP)
- Maximum file size: 2MB
- Images are automatically cropped to a 1:1 aspect ratio

### Registration with Photo Upload

**Endpoint:** `POST /api/auth/register/`

**Headers:**
```
Content-Type: multipart/form-data
```

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string",
    "photo": file
}
```

**Sample Response (Success - 201 Created):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "username": "example_user",
        "email": "user@example.com",
        "photo": "/media/user_photos/example_user_photo.jpg"
    }
}
```

**Sample Response (Error - 400 Bad Request):**
```json
{
    "error": "Photo size must be no more than 2MB."
}
```
or
```json
{
    "error": "File must be an image."
}
```

## Rate Limiting

The API implements rate limiting to prevent abuse. Here are the current limits:

### Authentication Endpoints
- Register: 5 requests per 5 minutes
- Login: 10 requests per 5 minutes

### Protected Endpoints
- Protected Route: 60 requests per minute
- List Operations: 60 requests per minute
- Create Operations: 30 requests per minute
- Like Operations: 30 requests per minute

When rate limit is exceeded, the API returns:
- Status Code: 429 (Too Many Requests)
- Response Body:
```json
{
    "error": "Rate limit exceeded",
    "detail": "Too many requests. Maximum X requests per Y seconds."
}
```

## API Documentation

### Authentication Endpoints

#### Register User
- **Method**: POST
- **URL**: `/api/auth/register/`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response**:
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

#### Login
- **Method**: POST
- **URL**: `/api/auth/login/`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access": "string",
    "refresh": "string"
  }
  ```

#### Refresh Token
- **Method**: POST
- **URL**: `/api/auth/token/refresh/`
- **Headers**: 
  ```
  Content-Type: application/json
  ```
- **Request Body**:
  ```json
  {
    "refresh": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access": "string"
  }
  ```

### User Endpoints

All user endpoints require authentication. Include the JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

#### List User Profile
- **Method**: GET
- **URL**: `/api/users/`
- **Response**:
  ```json
  {
    "id": "integer",
    "username": "string",
    "email": "string",
    "first_name": "string",
    "last_name": "string"
  }
  ```

#### Update User Profile
- **Method**: PUT/PATCH
- **URL**: `/api/users/{id}/`
- **Request Body**:
  ```json
  {
    "first_name": "string",
    "last_name": "string",
    "email": "string"
  }
  ```

### Product Endpoints

All product endpoints require authentication.

#### List Products
- **Method**: GET
- **URL**: `/api/products/`
- **Response**:
  ```json
  [
    {
      "id": "integer",
      "name": "string",
      "description": "string",
      "price": "decimal",
      "stock": "integer",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```

#### Create Product
- **Method**: POST
- **URL**: `/api/products/`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "price": "decimal",
    "stock": "integer"
  }
  ```

#### Update Product
- **Method**: PUT/PATCH
- **URL**: `/api/products/{id}/`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "price": "decimal",
    "stock": "integer"
  }
  ```

#### Delete Product
- **Method**: DELETE
- **URL**: `/api/products/{id}/`

### Order Endpoints

All order endpoints require authentication.

#### List Orders
- **Method**: GET
- **URL**: `/api/orders/`
- **Response**:
  ```json
  [
    {
      "id": "integer",
      "user": {
        "id": "integer",
        "username": "string",
        "email": "string"
      },
      "product": {
        "id": "integer",
        "name": "string",
        "price": "decimal"
      },
      "quantity": "integer",
      "status": "string",
      "total_price": "decimal",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
  ```

#### Create Order
- **Method**: POST
- **URL**: `/api/orders/`
- **Request Body**:
  ```json
  {
    "product_id": "integer",
    "quantity": "integer",
    "status": "string"
  }
  ```

#### Update Order
- **Method**: PUT/PATCH
- **URL**: `/api/orders/{id}/`
- **Request Body**:
  ```json
  {
    "quantity": "integer",
    "status": "string"
  }
  ```

#### Delete Order
- **Method**: DELETE
- **URL**: `/api/orders/{id}/`

## Error Responses

All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Error message"
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "error": "Error message"
}
```

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Technologies Used

- Django
- Django REST Framework
- JWT Authentication
- SQLite Database 