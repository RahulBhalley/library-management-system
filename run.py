from flask import Flask, jsonify
from app.routes.books import books
from app.routes.members import members
from config import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.update(config_class.to_dict())

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'Library Management System API',
            'version': '1.0',
            'endpoints': {
                'register': '/api/auth/register',
                'login': '/api/auth/login',
                'books': '/api/books',
                'search': '/api/books?q=search_term',
                'pagination': '/api/books?page=1'
            }
        })

    # Register blueprints
    app.register_blueprint(books, url_prefix='/api')
    app.register_blueprint(members, url_prefix='/api')
    
    # Basic error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error has occurred.'
        }), 500

    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)