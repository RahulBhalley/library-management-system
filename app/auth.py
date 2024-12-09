from typing import Optional, Tuple
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app
import sqlite3

def generate_token(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(seconds=current_app.config['TOKEN_EXPIRATION'])
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            token = token.split('Bearer ')[1]
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except:
            return jsonify({'message': 'Invalid token'}), 401
            
        return f(current_user_id, *args, **kwargs)
    
    return decorated 