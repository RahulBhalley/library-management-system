def test_member_registration_validation(client):
    # Test missing fields
    response = client.post('/auth/register', json={
        'name': 'John Doe',
        'email': 'john@example.com'
        # missing password
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Missing required fields'
    
    # Test invalid email format
    response = client.post('/auth/register', json={
        'name': 'John Doe',
        'email': 'invalid-email',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email format'

    # Test successful registration
    response = client.post('/auth/register', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert 'token' in response.json

def test_member_authentication(client):
    # Register a user
    client.post('/auth/register', json={
        'name': 'John Doe',
        'email': 'john@example.com',
        'password': 'password123'
    })
    
    # Test login with correct credentials
    response = client.post('/auth/login', json={
        'email': 'john@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'token' in response.json
    
    # Test login with incorrect password
    response = client.post('/auth/login', json={
        'email': 'john@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401 