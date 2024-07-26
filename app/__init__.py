from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate
from flask_cors import CORS
from flask_session import Session
from flasgger import Swagger
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
sess = Session()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)

    # Load environment variables from .env file
    load_dotenv()
    
    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SESSION_TYPE'] = 'filesystem'  
    
    # Load additional config
    from app import config
    app_config = {
        'development': config.DevelopmentConfig,
        'testing': config.TestingConfig,
        'production': config.ProductionConfig,
    }
    
    if config_name not in app_config:
        raise KeyError(f"Configuration '{config_name}' is not a valid configuration name.")
    
    app.config.from_object(app_config[config_name])

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    CORS(app)
    migrate.init_app(app, db)
    Swagger(app)

    # Register blueprints
    from app.admin.routes import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')

    # Swagger setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Inventory Management"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    
    return app
