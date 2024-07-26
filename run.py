from app import create_app, db
import os

if __name__ == '__main__':
    config_name = os.getenv('FLASK_CONFIG', 'development')
    app = create_app(config_name)
    with app.app_context():
        db.create_all()
    app.run(debug=True)