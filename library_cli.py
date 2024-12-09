#!/usr/bin/env python3
import argparse
import requests
import json
import os
from typing import Optional, Dict, Any
from pathlib import Path

class LibraryClient:
    def __init__(self):
        self.base_url = 'http://localhost:5000/api'
        self.token_file = Path.home() / '.library_token'
        self.token = self._load_token()

    def _load_token(self) -> Optional[str]:
        if self.token_file.exists():
            return self.token_file.read_text().strip()
        return None

    def _save_token(self, token: str) -> None:
        self.token_file.write_text(token)
        self.token = token

    def _clear_token(self) -> None:
        if self.token_file.exists():
            self.token_file.unlink()
        self.token = None

    def _get_headers(self) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        return headers

    def register(self, name: str, email: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f'{self.base_url}/auth/register',
            json={'name': name, 'email': email, 'password': password}
        )
        if response.status_code == 201:
            self._save_token(response.json()['token'])
        return response.json()

    def login(self, email: str, password: str) -> Dict[str, Any]:
        response = requests.post(
            f'{self.base_url}/auth/login',
            json={'email': email, 'password': password}
        )
        if response.status_code == 200:
            self._save_token(response.json()['token'])
        return response.json()

    def logout(self) -> Dict[str, str]:
        self._clear_token()
        return {'message': 'Logged out successfully'}

    def add_book(self, title: str, author: str, isbn: str, quantity: int) -> Dict[str, Any]:
        response = requests.post(
            f'{self.base_url}/books',
            headers=self._get_headers(),
            json={
                'title': title,
                'author': author,
                'isbn': isbn,
                'quantity': quantity
            }
        )
        return response.json()

    def get_books(self, search: Optional[str] = None, page: int = 1) -> Dict[str, Any]:
        params = {'page': page}
        if search:
            params['q'] = search
        
        response = requests.get(
            f'{self.base_url}/books',
            headers=self._get_headers(),
            params=params
        )
        return response.json()

def main():
    parser = argparse.ArgumentParser(description='Library Management System CLI')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Register parser
    register_parser = subparsers.add_parser('register', help='Register a new user')
    register_parser.add_argument('--name', required=True, help='User name')
    register_parser.add_argument('--email', required=True, help='User email')
    register_parser.add_argument('--password', required=True, help='User password')

    # Login parser
    login_parser = subparsers.add_parser('login', help='Login to the system')
    login_parser.add_argument('--email', required=True, help='User email')
    login_parser.add_argument('--password', required=True, help='User password')

    # Logout parser
    subparsers.add_parser('logout', help='Logout from the system')

    # Add book parser
    add_book_parser = subparsers.add_parser('add-book', help='Add a new book')
    add_book_parser.add_argument('--title', required=True, help='Book title')
    add_book_parser.add_argument('--author', required=True, help='Book author')
    add_book_parser.add_argument('--isbn', required=True, help='Book ISBN')
    add_book_parser.add_argument('--quantity', required=True, type=int, help='Book quantity')

    # List books parser
    list_books_parser = subparsers.add_parser('list-books', help='List all books')
    list_books_parser.add_argument('--search', help='Search term')
    list_books_parser.add_argument('--page', type=int, default=1, help='Page number')

    args = parser.parse_args()
    client = LibraryClient()

    try:
        if args.command == 'register':
            result = client.register(args.name, args.email, args.password)
            print('Registration successful!')
            print(f'Token: {result.get("token")}')

        elif args.command == 'login':
            result = client.login(args.email, args.password)
            print('Login successful!')
            print(f'Token: {result.get("token")}')

        elif args.command == 'logout':
            result = client.logout()
            print(result['message'])

        elif args.command == 'add-book':
            result = client.add_book(args.title, args.author, args.isbn, args.quantity)
            print(json.dumps(result, indent=2))

        elif args.command == 'list-books':
            result = client.get_books(args.search, args.page)
            print(json.dumps(result, indent=2))

        else:
            parser.print_help()

    except requests.exceptions.RequestException as e:
        print(f'Error: {str(e)}')
    except json.JSONDecodeError:
        print('Error: Invalid response from server')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    main() 