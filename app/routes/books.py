from flask import Blueprint, request, jsonify, current_app
from typing import Tuple, Dict, Any
from ..auth import token_required
from ..models import Database
import sqlite3

books = Blueprint('books', __name__)

@books.route('/books', methods=['GET'])
@token_required
def get_books(current_user_id: int) -> Tuple[Dict[str, Any], int]:
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    search_query = request.args.get('q', '')
    
    db = Database(current_app.config['DATABASE_PATH'])
    offset = (page - 1) * per_page
    
    with sqlite3.connect(db.db_path) as conn:
        conn.row_factory = sqlite3.Row  # Enable row factory for dict-like rows
        cursor = conn.cursor()
        
        if search_query:
            cursor.execute('''
                SELECT * FROM books 
                WHERE title LIKE ? OR author LIKE ?
                LIMIT ? OFFSET ?
            ''', (f'%{search_query}%', f'%{search_query}%', per_page, offset))
        else:
            cursor.execute('SELECT * FROM books LIMIT ? OFFSET ?', 
                         (per_page, offset))
        
        books = cursor.fetchall()
        
        # Get total count for pagination
        if search_query:
            cursor.execute('''
                SELECT COUNT(*) FROM books 
                WHERE title LIKE ? OR author LIKE ?
            ''', (f'%{search_query}%', f'%{search_query}%'))
        else:
            cursor.execute('SELECT COUNT(*) FROM books')
        
        total = cursor.fetchone()[0]
    
    return jsonify({
        'books': [dict(book) for book in books],  # Simplified dict conversion using row factory
        'total': total,
        'pages': (total + per_page - 1) // per_page,
        'current_page': page
    }), 200

@books.route('/books', methods=['POST'])
@token_required
def add_book(current_user_id: int) -> Tuple[Dict[str, Any], int]:
    if not request.is_json:
        return jsonify({'message': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    
    if data is None:
        return jsonify({'message': 'Invalid JSON'}), 400
    
    required_fields = ['title', 'author', 'isbn', 'quantity']
    if not all(field in data for field in required_fields):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Validate quantity is a positive integer
    try:
        quantity = int(data['quantity'])
        if quantity <= 0:
            return jsonify({'message': 'Quantity must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'message': 'Quantity must be a valid number'}), 400
    
    db = Database(current_app.config['DATABASE_PATH'])
    
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO books (title, author, isbn, quantity, available)
                VALUES (?, ?, ?, ?, ?)
            ''', (data['title'], data['author'], data['isbn'], 
                 quantity, quantity))
            
            book_id = cursor.lastrowid
            
        return jsonify({
            'message': 'Book added successfully',
            'book_id': book_id
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({'message': 'ISBN already exists'}), 400