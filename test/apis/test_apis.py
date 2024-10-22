import json

from flask_jwt_extended import decode_token


def test_create_user(client):
    # Create a new user
    response = client.post('/users/', json={
        "username": "testuser",
        "name": "Test",
        "last_name": "User",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test"

def test_create_duplicate_user(client):
    # Try creating the same user again
    response = client.post('/users/', json={
        "username": "testuser",
        "name": "Test",
        "last_name": "User",
        "password": "password123"
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "Username already exists"

def test_get_users_unauthorized(client):
    # Attempt to get users without an admin token
    response = client.get('/users/')


def test_get_users_with_admin_token(client):
    # Login as admin and use the token to access users
    response = client.post('/auth/admin?secret=what-a-secret')
    access_token = response.get_json()["access_token"]

    response = client.get('/users/', headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) > 0

def test_update_user(client):
    # Login as the created user
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "password123"
    })
    access_token = response.get_json()["access_token"]

    # Update the user information
    response = client.put('/users/1', headers={
        "Authorization": f"Bearer {access_token}"
    }, json={
        "name": "Updated Test",
        "last_name": "User"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User updated successfully"

def test_delete_user(client):
    # Login as the created user
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "password123"
    })
    access_token = response.get_json()["access_token"]

    # Delete the user
    response = client.delete('/users/1', headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "user deleted"

    # Verify the user is gone
    response = client.get('/users/1', headers={
        "Authorization": f"Bearer {access_token}"
    })
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "User not found"

def test_invalid_login(client):
    # Attempt to login with wrong password
    response = client.post('/auth/login', json={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 403
    data = response.get_json()
    assert data["error"] == "Invalid username or password"
