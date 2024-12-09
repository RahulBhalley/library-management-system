# Library Management System

## A. Running the Project & Tests

- Create and activate virtual environment:
```
python -m venv venv
source venv/bin/activate  # Unix
venv\Scripts\activate     # Windows
```

- Install package in editable mode:
```
pip install -e .
```

- Run the server on port 5001 (please disable System Preferences > General > AirDrop & Handoff > AirPlay Receiver, if on macOS):
```
python run.py --port 5001
```

- Run tests:
```
pytest
```

## B. Design Choices

**Architecture**
- Flask-based REST API with Blueprint organization
- SQLite for simplicity (referenced in app/models.py)
- JWT-based authentication (see app/auth.py)
- CLI client for easy testing/interaction (library_cli.py)

**Key Patterns**
- Repository pattern for database operations
- Decorator pattern for auth middleware
- Factory pattern for app creation

## C. Assumptions & Limitations

**Assumptions**
- Single-user admin system
- Books can only be added/removed (no borrowing system)
- Simple search by title/author only

**Limitations**
- SQLite doesn't handle concurrent access well
- No password reset functionality
- Basic error handling
- No rate limiting
- No proper logging system
