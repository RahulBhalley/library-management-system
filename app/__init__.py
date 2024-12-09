from flask import Flask
from config import Config

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Load default config
    app.config.from_object(Config)
    
    # Override config with test config if provided
    if test_config:
        app.config.update(test_config)
    
    # Register blueprints
    from app.routes.books import books
    from app.routes.members import members
    
    app.register_blueprint(books)
    app.register_blueprint(members)
    
    return app 