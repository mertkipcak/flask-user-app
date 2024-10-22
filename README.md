# Userbase API Documentation

## Overview

This project is a Flask-based web application that provides a **user management** system with **authentication** and **JWT-based authorization**. It supports user registration, authentication, and user management through API endpoints.

---

## Features

- **User Authentication**: Login with JWT-based access tokens.
- **Admin Authentication**: Secure access for admin with secret keys.
- **User Management**: Create, update, retrieve, and delete user accounts.
- **JWT Authorization**: User and admin role management using JWT claims.
- **JSON Schema Validation**: API request validation using JSON schemas.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/mertkipcak/flask-user-app.git
    cd flask-user-app
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the configuration in `./config/app_config.json`. Ensure you define:

    ```json
    {
        "database": { "url": "sqlite:///userbase.db" },
        "JWT_SECRET_KEY": "your-secret-key",
        "admin_secret": "your-admin-secret",
        "logging": { "level": "INFO", "format": "%(asctime)s - %(levelname)s - %(message)s" }
    }
    ```

5. Initialize the database:

    ```bash
    flask db upgrade
    ```

6. Run the application:

    ```bash
    export FLASK_APP=userbase.app
    flask run
    ```

---

## API Endpoints

### 1. **Authentication API** (`/auth`)

#### **POST /auth/login**
Authenticate a user and generate a JWT token.

- **Request Body**:
    ```json
    {
        "username": "user1",
        "password": "password123"
    }
    ```
- **Response**:
    ```json
    {
        "access_token": "<JWT_TOKEN>"
    }
    ```
- **Status Codes**:
  - `200 OK`: Token generated.
  - `401 Unauthorized`: Invalid credentials.

#### **POST /auth/admin?secret=<SECRET_KEY>**
Authenticate as admin and receive a JWT token.

- **Query Parameter**: `secret` (Admin secret key)
- **Response**:
    ```json
    {
        "access_token": "<JWT_TOKEN>"
    }
    ```
- **Status Codes**:
  - `200 OK`: Admin token generated.
  - `403 Forbidden`: Invalid secret key.

---

### 2. **User Management API** (`/users`)

#### **GET /users/** (Admin-only)
Retrieve a list of all users.

- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`

- **Response**:
    ```json
    [
        { "id": 1, "name": "John" },
        { "id": 2, "name": "Jane" }
    ]
    ```

#### **POST /users/**
Create a new user.

- **Request Body**:
    ```json
    {
        "username": "newuser",
        "name": "New",
        "last_name": "User",
        "password": "password123",
        "dob": "2000-01-01T00:00:00Z"
    }
    ```
- **Response**:
    ```json
    { "id": 3, "name": "New" }
    ```
- **Status Codes**:
  - `201 Created`: User created.
  - `400 Bad Request`: Username already exists.

#### **GET /users/<user_id>** (User or Admin)
Retrieve details of a specific user.

- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`

- **Response**:
    ```json
    {
        "id": 1,
        "username": "user1",
        "name": "John",
        "last_name": "Doe",
        "dob": "1995-06-15"
    }
    ```
- **Status Codes**:
  - `200 OK`: User found.
  - `404 Not Found`: User not found.

#### **PUT /users/<user_id>** (User or Admin)
Update details of a user.

- **Request Body**:
    ```json
    {
        "name": "Updated Name",
        "last_name": "Updated LastName"
    }
    ```
- **Response**:
    ```json
    { "message": "User updated successfully" }
    ```
- **Status Codes**:
  - `200 OK`: User updated.
  - `404 Not Found`: User not found.

#### **DELETE /users/<user_id>** (User or Admin)
Delete a user.

- **Headers**:
  - `Authorization: Bearer <JWT_TOKEN>`

- **Response**:
    ```json
    { "message": "user deleted" }
    ```
- **Status Codes**:
  - `200 OK`: User deleted.
  - `404 Not Found`: User not found.

---

## JWT Authorization

All routes (except `/auth/login`) require **JWT tokens** in the `Authorization` header.

**Example Header**:
```
Authorization: Bearer <JWT_TOKEN>
```

JWT tokens contain the following claims:
- `user_id`: ID of the user.
- `is_admin`: Indicates if the token belongs to an admin.

---

## JSON Schemas

**User Creation Schema**:
```json
{
    "type": "object",
    "properties": {
        "username": { "type": "string", "minLength": 1 },
        "name": { "type": "string", "minLength": 1 },
        "last_name": { "type": "string", "minLength": 1 },
        "password": { "type": "string", "minLength": 1 },
        "dob": { "type": "string", "format": "date-time" }
    },
    "required": ["username", "name", "last_name", "password"],
    "additionalProperties": false
}
```

---

## Error Handling

- `400 Bad Request`: Invalid input or JSON schema validation error.
- `401 Unauthorized`: Invalid credentials or missing token.
- `403 Forbidden`: Unauthorized access (admin-only or user access restrictions).
- `404 Not Found`: Requested resource not found.
- `500 Internal Server Error`: Database or server errors.

