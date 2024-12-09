from flask import Blueprint, request, jsonify, current_app
from ..models import Database
from ..auth import generate_token
import sqlite3
from typing import Tuple, Dict, Any
import hashlib
import re

members = Blueprint('members', __name__)

def is_valid_email(email: str) -> bool:
    # Basic email validation pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@members.route('/auth/register', methods=['POST'])
def register() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    
    # Check required fields
    if not all(k in data for k in ['name', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Validate email format
    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400
    
    # Hash the password
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    db = Database(current_app.config['DATABASE_PATH'])
    
    try:
        with sqlite3.connect(db.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO members (name, email, password)
                VALUES (?, ?, ?)
            ''', (data['name'], data['email'], hashed_password))
            
            member_id = cursor.lastrowid
            token = generate_token(member_id)
            
            return jsonify({
                'message': 'Registration successful',
                'token': token
            }), 201
            
    except sqlite3.IntegrityError:
        return jsonify({'message': 'Email already exists'}), 400

@members.route('/auth/login', methods=['POST'])
def login() -> Tuple[Dict[str, Any], int]:
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing email or password'}), 400
    
    # Hash the password
    hashed_password = hashlib.sha256(data['password'].encode()).hexdigest()
    
    db = Database(current_app.config['DATABASE_PATH'])
    
    with sqlite3.connect(db.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id FROM members 
            WHERE email = ? AND password = ?
        ''', (data['email'], hashed_password))
        
        result = cursor.fetchone()
        
        if result:
            token = generate_token(result[0])
            return jsonify({
                'message': 'Login successful',
                'token': token
            }), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401 