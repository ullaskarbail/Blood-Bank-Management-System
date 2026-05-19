import os
from flask import Flask
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_secret')
    
    from .routes.auth import auth_bp
    from .routes.donors import donors_bp
    from .routes.inventory import inventory_bp
    from .routes.requests import requests_bp
    from .routes.hospitals import hospitals_bp
    from .routes.main import main_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(donors_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(requests_bp)
    app.register_blueprint(hospitals_bp)
    app.register_blueprint(main_bp)
    
    return app
