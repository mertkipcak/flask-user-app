import json
import logging
from flask import Flask
from flask_jwt_extended import JWTManager

from userbase.apis.auth import auth_bp
from userbase.utils.config import CONFIG
from userbase.utils.db import init_extensions
from userbase.apis.users import users_bp

with open('./config/app_config.json') as config_file:
    config = json.load(config_file)

def create_app():
    app = Flask(__name__)

    # Set the database URI and other config values
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.get('database')['url']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = CONFIG.get('JWT_SECRET_KEY', 'default-secret')

    # Initialize extensions
    init_extensions(app)
    JWTManager(app)

    # Set up logging
    logging.basicConfig(
        level=getattr(logging, config['logging']['level']),
        format=config['logging']['format']
    )

    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
