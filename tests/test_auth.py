import pytest
import jwt
from datetime import datetime, timedelta

def test_register_success(client):
    response = client.post('/auth/register', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    assert response.status_code == 201
    assert 'token' in response.json
    assert 'message' in response.json
    assert response.json['message'] == 'Registration successful'

def test_register_duplicate_email(client):
    # Register first user
    client.post('/auth/register', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    # Try to register with same email
    response = client.post('/auth/register', json={
        'name': 'Jane Doe',
        'email': 'john@example.com',
        'password': 'password456'
    })
    
    assert response.status_code == 400
    assert response.json['message'] == 'Email already exists'

def test_token_validation(client, auth_headers):
    # Test valid token
    response = client.get('/books', headers=auth_headers)
    assert response.status_code == 200
    
    # Test invalid token
    response = client.get('/books', headers={'Authorization': 'Bearer invalid-token'})
    assert response.status_code == 401
    
    # Test missing token
    response = client.get('/books')
    assert response.status_code == 401 