from flask import Flask, request, jsonify, Blueprint, session
from flasgger import Swagger
from app.models import User, ClothingItem, Cart, Payment
from app import mail, db, bcrypt
from app.schemas import UserSchema
from flask_session import Session
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import string
import random
import os
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update
from datetime import datetime

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

def getLoginDetails():
    if current_user.is_authenticated:
        noOfItems = Cart.query.filter_by(buyer=current_user).count()
    else:
        noOfItems = 0
    return noOfItems

@app.route("/")

# Homepage Route
@app.route('/', methods=['GET'])
def homepage():
    return jsonify({'message': 'Welcome to Rosee Thrifts '}), 200

@app.route('/register', methods=['POST'])
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

@app.route('/login', methods=['POST'])
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

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if user is None:
        return jsonify({'message': 'User not found'}), 404
    
    user.password = generate_password_hash(data['new_password'])
    user.password_reset_required = False
    db.session.commit()

    return jsonify({'message': 'Password reset successful'}), 200

# How It Works Route
@app.route('/how-it-works', methods=['GET'])
def how_it_works():
    return jsonify({
        'message': 'How It Works',
        'steps': [
            '1. Browse the available clothing items.',
            '2. Select the clothes you like and add them to your cart.',
            '3. View and manage items in your cart.',
            '4. Proceed to checkout to complete your purchase.'
        ]
    }), 200

# Select Clothes Route
@app.route('/items', methods=['GET'])
def get_items():
    items = ClothingItem.query.all()
    return jsonify([item.as_dict() for item in items]), 200

# Add to Cart Route
@app.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)
    
    item = ClothingItem.query.get_or_404(item_id)
    
    cart_item = Cart(item_id=item.id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    
    return jsonify({'message': f'Added {quantity} of {item.name} to the cart.'}), 201

# Display Cart Route
@app.route('/cart', methods=['GET'])
def display_cart():
    cart_items = Cart.query.all()
    cart_details = []
    
    for cart_item in cart_items:
        item = ClothingItem.query.get(cart_item.item_id)
        cart_details.append({
            'item': item.as_dict(),
            'quantity': cart_item.quantity
        })
    
    return jsonify(cart_details), 200

# Remove Cart Item Route
@app.route('/cart/<int:cart_item_id>', methods=['DELETE'])
def remove_cart_item(cart_item_id):
    cart_item = Cart.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from cart.'}), 204

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    new_payment = Payment(
        user_id=data['user_id'],
        amount=data['amount'],
        payment_method=data['payment_method'],
        payment_status='Pending',  # Initial status
        payment_date=datetime.utcnow()
    )
    db.session.add(new_payment)
    db.session.commit()
    return jsonify(new_payment.as_dict()), 201

@app.route('/payments/<int:id>', methods=['GET'])
def get_payment(id):
    payment = Payment.query.get_or_404(id)
    return jsonify(payment.as_dict())

@app.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([payment.as_dict() for payment in payments])

@app.route('/payments/<int:id>', methods=['PUT'])
def update_payment(id):
    data = request.get_json()
    payment = Payment.query.get_or_404(id)
    payment.payment_status = data.get('payment_status', payment.payment_status)
    db.session.commit()
    return jsonify(payment.as_dict())

@app.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    payment = Payment.query.get_or_404(id)
    db.session.delete(payment)
    db.session.commit()
    return '', 204

@app.route('/logout', methods=['POST'])
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

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify({'message': 'Protected route', 'user': current_user}), 200


if __name__ == "__main__":
    app.run(debug=True)
