from flask import Blueprint, request, jsonify, session
from app.schemas import AdminSchema
from app import db
from app.admin.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flasgger import swag_from
from flask_session import Session
from app.models import db, ClothingItem

admin_blueprint = Blueprint('admin', __name__, url_prefix='/api/admin')

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


@admin_blueprint.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Admin registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'admin': {
                        'type': 'object'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input, Missing required fields'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    }
                }
            }
        }
    ]
})
def register_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    logging.debug(f"Received data - Email: {email}, Name: {name}, Password: {password}")

    if not all([email, name, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if Admin.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email exists"}), 400

    if Admin.query.filter_by(name=name).first() is not None:
        return jsonify({"error": "Name already registered"}), 400

    if password is None:
        logging.error("Password is None before hashing")
        return jsonify({"error": "Password cannot be None"}), 400

    hashed_password = generate_password_hash(password)
    logging.debug(f"Hashed Password: {hashed_password}")

    admin = Admin(
        email=email,
        name=name,
        password=hashed_password)

    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin registered successfully", "admin": admin.to_dict()}), 201

@admin_blueprint.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'admin': {
                        'type': 'object'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        401: {
            'description': 'Unauthorized'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    }
                }
            }
        }
    ]
})
def login_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    admin = Admin.query.filter_by(email=email).first()

    session['admin_id'] = admin.adminid
    session['admin_email'] = admin.email
    return jsonify({"message": "Login successful", "admin": admin.to_dict()}), 200

@admin_blueprint('/items', methods=['GET'])
def get_items():
    items = ClothingItem.query.all()
    return jsonify([item.as_dict() for item in items])

@admin_blueprint('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = ClothingItem(
        name=data['name'],
        category=data['category'],
        size=data['size'],
        color=data['color'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.as_dict()), 201

@admin_blueprint('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = ClothingItem.query.get_or_404(id)
    item.name = data['name']
    item.category = data['category']
    item.size = data['size']
    item.color = data['color']
    item.price = data['price']
    item.stock = data['stock']
    db.session.commit()
    return jsonify(item.as_dict())

@admin_blueprint('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = ClothingItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

@admin_blueprint.route('/logout', methods=['POST'])
def logout_admin():
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    return jsonify({"message": "Logged out successfully"}), 200

@admin_blueprint.route('/session', methods=['GET'])
def get_session():
    if 'admin_id' in session:
        return jsonify({"admin_id": session['admin_id'], "admin_email": session['admin_email']}), 200
    return jsonify({"error": "No active session"}), 401
