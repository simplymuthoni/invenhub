from flask import Flask, request, jsonify, Blueprint, session
from flasgger import Swagger
from app.users.models import User
from app import mail, db, bcrypt
from app.schemas import UserSchema
from flask_session import Session
from flask_mail import Message
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import string
import random
import os
users = Blueprint('users', __name__, url_prefix='/api/users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

app = Flask(__name__)
swagger = Swagger(app)
# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
Session(app)

def generate_temporary_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))

def send_email(recipient, subject, body):
    msg = Message(subject, sender='nonreply@gmail.com', recipients=[recipient])
    msg.body = body
    mail.send(msg)


@users.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    name = data.get('name')
    phone_number = data.get('phone_number')
    email = data.get('email')
    address = data.get('address')
    username = data.get('username')
    
    # Generate temporary password
    temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    hashed_password = bcrypt.generate_password_hash(temp_password).decode('utf-8')
    
    # Create new user
    new_user = User(name=name, phone_number=phone_number, email=email, address=address, username=username, password=hashed_password)
    
    # Add new user to the database
    db.session.add(new_user)
    db.session.commit()
    
    # Send email with temporary password
    msg = Message('Your Account Registration', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
    msg.body = f'Hello {username},\n\nYour account has been created successfully. Your temporary password is: {temp_password}\nPlease login and change your password.'
    mail.send(msg)
    
    return jsonify({'message': 'User registered successfully. Please check your email for the temporary password.'}), 201

@users.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return jsonify(message="User not found"), 404

    temporary_password = generate_temporary_password()
    user.password = bcrypt.generate_password_hash(temporary_password).decode('utf-8')
    db.session.commit()

    msg = Message('Password Reset Request',
                  recipients=[user.username])
    msg.body = f'Your temporary password is: {temporary_password}\nPlease use it to log in and change your password immediately.'
    mail.send(msg)

    return jsonify(message="Temporary password sent to your email"), 200

@users.route('/change_password', methods=['POST'])
@jwt_required()
def change_password():
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()

    if not user:
        return jsonify(message="User not found"), 404

    if not bcrypt.check_password_hash(user.password, data['old_password']):
        return jsonify(message="Old password is incorrect"), 401

    new_password_hashed = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
    user.password = new_password_hashed
    db.session.commit()

    return jsonify(message="Password changed successfully"), 200
    
@users.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: Login
          required:
            - username
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      400:
        description: Invalid input or missing required fields
      401:
        description: Unauthorized
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()

    # if user is None or not check_password_hash(user.password, password):
    #     return jsonify({"error": "Invalid email or password"}), 400

    session['user_id'] = user.id
    session['user_username'] = user.username

    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

@users.route('/logout', methods=['POST'])
def logout():
    """
    User logout
    ---
    responses:
      200:
        description: Logout successful
    """
    session.pop('user_id', None)
    session.pop('user_email', None)
    return jsonify({"message": "Logout successful"}), 200

app.register_blueprint(users)
