import os
import atexit
import logging

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required
from flask_mail import Mail
from dotenv import load_dotenv
from app import config
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flasgger import Swagger
from flask_bcrypt import Bcrypt
from flask_session import Session

load_dotenv()

jwt = JWTManager()
mail = Mail()
db = SQLAlchemy() 
bcrypt = Bcrypt()
sess = Session()

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def create_app(config_name):
    """Function wraps the creation of a new Flask object, and returns it after it's
        loaded up with configuration settings
    """
    app = Flask(__name__)
    app_config={
        'development':config.DevelopmentConfig,
        'testing': config.TestingConfig,
        'production' :config.ProductionConfig, 
    }
   
    if config_name not in app_config:
        raise KeyError(f"Configuration '{config_name}' is not a valid configuration name.")
    
    app.config.from_object(app_config[config_name])
    app.config['SECRET_KEY'] = os.getenv('secret_key')
    if __name__ == "__main__":
        config_name = os.getenv('FLASK_CONFIG', 'development')
    CORS(app)    
     
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    mail.init_app(app)
    swagger = Swagger(app)
    jwt = JWTManager(app)
    bcrypt.init_app(app)
    sess.init_app(app)
    
    from .users.routes import auth 
    app.register_blueprint(auth)
