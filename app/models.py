from typing import Optional, Dict, Any
import sqlite3
import json
from datetime import datetime

class Book:
    def __init__(self, id: int, title: str, author: str, isbn: str, 
                 quantity: int, available: int):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.available = available

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quantity': self.quantity,
            'available': self.available
        }

class Member:
    def __init__(self, id: int, name: str, email: str, password: str):
        self.id = id
        self.name = name
        self.email = email
        self.password = password  # This should be hashed in production

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create books table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    isbn TEXT UNIQUE NOT NULL,
                    quantity INTEGER NOT NULL,
                    available INTEGER NOT NULL
                )
            ''')
            
            # Create members table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            
            conn.commit() 