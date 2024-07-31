from flask import Flask, jsonify
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
from .extensions import db
from flask_swagger_ui import get_swaggerui_blueprint

load_dotenv()


def create_app(config_name):
    app = Flask(__name__)
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

    # Load environment variables from .env file
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    
    bcrypt = Bcrypt()
    jwt = JWTManager()
    mail = Mail()
    sess = Session()
    migrate = Migrate()
    swagger = Swagger()

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    sess.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    # Enable CORS
    CORS(app)

    # Register blueprints
    from app.admin.routes import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/api/admin')
    from app.routes import rosee_blueprint
    app.register_blueprint(rosee_blueprint, url_prefix='/api/rosee')

    # Swagger setup
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Inventory Management"})
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Index route
    @app.route('/')
    def index():
        return jsonify({"message": "Welcome to Rosee Thrifts API"}), 200

    # Error handling
    @app.errorhandler(422)
    @app.errorhandler(400)
    def handle_error(err):
        headers = err.data.get("headers", None)
        messages = err.data.get("messages", ["Invalid request."])
        if headers:
            return jsonify({"errors": messages})
        else:
            return jsonify({"errors": messages})

    return app