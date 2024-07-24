from flask import Flask, request, jsonify, Blueprint, session
from flasgger import Swagger
from app.models import User
from app import mail, db, bcrypt
from app.schemas import UserSchema
from flask_session import Session
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
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
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  # Add JWT secret key
Session(app)
jwt = JWTManager(app)  # Initialize JWTManager

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
    temp_password = generate_temporary_password()
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

@users.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user is None or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    if user.password_reset_required:
        return jsonify({'message': 'Password reset required'}), 403
    
    # Create JWT token
    access_token = create_access_token(identity={'username': user.username, 'email': user.email})
    
    return jsonify({'message': 'Login successful', 'access_token': access_token}), 200

@users.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    user.password = generate_password_hash(data['new_password'])
    user.password_reset_required = False
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200

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

@users.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': 'Protected route', 'user': current_user}), 200

app.register_blueprint(users)

if __name__ == "__main__":
    app.run(debug=True)
