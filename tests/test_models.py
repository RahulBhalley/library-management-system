import pytest
from app.models import Book, Member, Database

def test_book_model():
    book = Book(
        id=1,
        title='Test Book',
        author='Test Author',
        isbn='1234567890',
        quantity=5,
        available=5
    )
    
    book_dict = book.to_dict()
    assert book_dict['id'] == 1
    assert book_dict['title'] == 'Test Book'
    assert book_dict['author'] == 'Test Author'
    assert book_dict['isbn'] == '1234567890'
    assert book_dict['quantity'] == 5
    assert book_dict['available'] == 5

def test_member_model():
    member = Member(
        id=1,
        name='Test User',
        email='test@example.com',
        password='hashed_password'
    )
    
    member_dict = member.to_dict()
    assert member_dict['id'] == 1
    assert member_dict['name'] == 'Test User'
    assert member_dict['email'] == 'test@example.com'
    assert 'password' not in member_dict  # Password should not be in dict

def test_database_initialization(app):
    with app.app_context():
        db = Database(app.config['DATABASE_PATH'])
        
        # Test if tables exist
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Check books table
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='books'
            """)
            assert cursor.fetchone() is not None
            
            # Check members table
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='members'
            """)
            assert cursor.fetchone() is not None 