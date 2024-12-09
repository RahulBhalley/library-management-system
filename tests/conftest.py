import pytest
import os
import tempfile
from app import create_app
from app.models import Database

@pytest.fixture
def app():
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure app with test settings
    app = create_app({
        'TESTING': True,
        'DATABASE_PATH': db_path,
        'SECRET_KEY': 'test-secret-key',
        'ITEMS_PER_PAGE': 2  # Smaller pagination for easier testing
    })

    # Initialize database
    with app.app_context():
        db = Database(db_path)
    
    yield app

    # Cleanup
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    # Register a test user and get token
    response = client.post('/auth/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'} 