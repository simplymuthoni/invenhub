from flask import Flask, request, jsonify, Blueprint, session, url_for, redirect
from flasgger import Swagger
from app.models import User, ClothingItem, Cart, Payment, Packaging, Arrival, Feedback
from app import mail, bcrypt
from app.schemas import UserSchema
from flask_session import Session
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
import string
import random
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user,login_required
from sqlalchemy import func, update
from datetime import datetime, timedelta
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Mail, Message
from app.extensions import db
import logging

app=Flask(__name__)
swagger = Swagger(app)
mail = Mail(app)
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

login_manager = LoginManager(app)
login_manager.login_view = 'login'


rosee_blueprint = Blueprint('rosee', __name__, url_prefix='/api/rosee')

user_schema = UserSchema()
users_schema = UserSchema(many=True)

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

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

@app.errorhandler(ExpiredSignatureError)
def handle_expired_error(e):
    return jsonify({"error": "Token has expired"}), 401

@app.errorhandler(InvalidSignatureError)
def handle_invalid_signature_error(e):
    return jsonify({"error": "Invalid token signature"}), 401

@app.errorhandler(NoAuthorizationError)
def handle_missing_token_error(e):
    return jsonify({"error": "Authorization token is missing"}), 401


# Homepage Route
@rosee_blueprint.route('/', methods=['GET'])
def homepage():
    """
    Homepage
    ---
    responses:
      200:
        description: Welcome message
    """
    return jsonify({'message': 'Welcome to Rosee Thrifts '}), 200

@rosee_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    # Get the identity of the currently logged-in user
    current_user = get_jwt_identity()
    return jsonify({"logged_in_as": current_user}), 200

# Login Route
@rosee_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error":"Invalid input"}), 400
    
    email = data.get('email')
    full_name = data.get('full_name')
    username = data.get('username')
    password = data.get('password')
    repeat_password = data.get('repeat_password') 

    logging.debug(f"Received data - Email: {email}, Full_Name {full_name}, Username {username}")

    if not all([email, full_name, username, password]):
        return jsonify({"error": "Missing required fields"}), 400
    
    if password != repeat_password:
        return jsonify({"error":"Passwords do not match"}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(full_name=full_name).first() is not None:
        return jsonify({"error": "Name already registered"}), 400

    hashed_password = generate_password_hash(password)
    logging.debug(f"Hashed Password: {hashed_password}")

    user = User(
        email=email,
        full_name=full_name,
        username=username,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message":"User registered successfully"}), 201


@rosee_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    logging.debug(f"Received data - {data}")

    if not data:
        return jsonify({"error":"Invalid input"}), 400
    
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 401

    session['userid'] = user.userid

     # Generate JWT token
    access_token = create_access_token(identity={'email': user.email})
    
    # Log in the user with Flask-Login
    login_user(user)
    
    return jsonify({"message":"Login successful", "access_token": access_token}), 200


@rosee_blueprint.route('/request-password-reset', methods=['POST'])
def request_password_reset():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()

    if user:
        # Create a password reset token using JWT
        reset_token = create_access_token(identity=user.email, expires_delta=timedelta(hours=1))
        send_reset_email(user.email, reset_token)

    # Always return this response to avoid revealing if an email is registered or not
    return jsonify({"message": "If the email exists, a password reset link has been sent"}), 200

def send_reset_email(email, token):
    reset_url = url_for('rosee_blueprint.reset_password-reset', token=token, _external=True)
    subject = "Password Reset Request"
    body = f"Click the link to reset your password: {reset_url}"
    send_email(subject, [email], body)

@rosee_blueprint.route('/reset-password', methods=['POST'])
@jwt_required()
def reset_password():
    current_user_email = get_jwt_identity()

    data = request.get_json()
    password = data.get('password')
    repeat_password = data.get('repeat_password')

    if not password or not repeat_password:
        return jsonify({"error": "Password and repeat password are required"}), 400
    
    if password != repeat_password:
        return jsonify({"error": "Passwords do not match"}), 400

    user = User.query.filter_by(email=current_user_email).first()

    if user:
        user.password = generate_password_hash(password)
        db.session.commit()
        return jsonify({"message": "Password reset successfully"}), 200

    return jsonify({"error": "User not found"}), 404

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

  
@rosee_blueprint.route('/dashboard')
def dashboard():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return f'Hello, {current_user.username}!'

@rosee_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# How It Works Route
@rosee_blueprint.route('/how-it-works', methods=['GET'])
def how_it_works():
    """
    How it works
    ---
    responses:
      200:
        description: How it works steps
    """
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
@rosee_blueprint.route('/items', methods=['GET'])
def get_items():
    """
    Get all clothing items
    ---
    responses:
      200:
        description: List of all clothing items
    """
    items = ClothingItem.query.all()
    return jsonify([item.as_dict() for item in items]), 200

# Add to Cart Route
@rosee_blueprint.route('/cart', methods=['POST'])
def add_to_cart():
    """
    Add item to cart
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - item_id
            - quantity
          properties:
            item_id:
              type: integer
            quantity:
              type: integer
              default: 1
    responses:
      201:
        description: Item added to cart
    """
    data = request.get_json()
    item_id = data.get('item_id')
    quantity = data.get('quantity', 1)
    
    item = ClothingItem.query.get_or_404(item_id)
    
    cart_item = Cart(item_id=item.id, quantity=quantity)
    db.session.add(cart_item)
    db.session.commit()
    
    return jsonify({'message': f'Added {quantity} of {item.name} to the cart.'}), 201

# Display Cart Route
@rosee_blueprint.route('/cart', methods=['GET'])
def display_cart():
    """
    Display all cart items
    ---
    responses:
      200:
        description: List of all cart items
    """
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
@rosee_blueprint.route('/cart/<int:cart_item_id>', methods=['DELETE'])
def remove_cart_item(cart_item_id):
    """
    Remove item from cart
    ---
    parameters:
      - in: path
        name: cart_item_id
        required: true
        type: integer
    responses:
      204:
        description: Item removed from cart
    """
    cart_item = Cart.query.get_or_404(cart_item_id)
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from cart.'}), 204

@rosee_blueprint.route('/payment', methods=['POST'])
def create_payment():
    """
    Create a new payment
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - user_id
            - amount
            - payment_method
            - payment_status
          properties:
            user_id:
              type: integer
            amount:
              type: number
            payment_method:
              type: string
              enum: [credit_card, paypal, bank_transfer]
            payment_status:
              type: string
              enum: [pending, success, failed]
    responses:
      201:
        description: Payment created successfully
      400:
        description: Error in creating payment
    """
    data = request.get_json()
    
    user_id = data.get('user_id')
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    payment_status = data.get('payment_status')

    new_payment = Payment(
        user_id=user_id,
        amount=amount,
        payment_method=payment_method,
        payment_status=payment_status
    )

    try:
        db.session.add(new_payment)
        db.session.commit()
        return jsonify({'message': 'Payment created successfully'}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@rosee_blueprint.route('/payment/<int:id>', methods=['GET'])
def get_payment(id):
    """
    Get a payment by ID
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Payment details
      404:
        description: Payment not found
    """
    payment = Payment.query.get(id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    return jsonify({
        'id': payment.id,
        'user_id': payment.user_id,
        'amount': payment.amount,
        'payment_method': payment.payment_method,
        'payment_status': payment.payment_status,
        'payment_date': payment.payment_date
    }), 200

@rosee_blueprint.route('/payment/<int:id>', methods=['PUT'])
def update_payment(id):
    """
    Update a payment by ID
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        schema:
          type: object
          properties:
            user_id:
              type: integer
            amount:
              type: number
            payment_method:
              type: string
              enum: [credit_card, paypal, bank_transfer]
            payment_status:
              type: string
              enum: [pending, success, failed]
    responses:
      200:
        description: Payment updated successfully
      404:
        description: Payment not found
      400:
        description: Error in updating payment
    """
    data = request.get_json()
    
    payment = Payment.query.get(id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    payment.user_id = data.get('user_id', payment.user_id)
    payment.amount = data.get('amount', payment.amount)
    payment.payment_method = data.get('payment_method', payment.payment_method)
    payment.payment_status = data.get('payment_status', payment.payment_status)

    try:
        db.session.commit()
        return jsonify({'message': 'Payment updated successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@rosee_blueprint.route('/payment/<int:id>', methods=['DELETE'])
def delete_payment(id):
    """
    Delete a payment by ID
    ---
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Payment deleted successfully
      404:
        description: Payment not found
      400:
        description: Error in deleting payment
    """
    payment = Payment.query.get(id)
    
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
    
    try:
        db.session.delete(payment)
        db.session.commit()
        return jsonify({'message': 'Payment deleted successfully'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
@rosee_blueprint.route('/payment/success', methods=['POST'])
def payment_success():
    data = request.get_json()
    
    user_id = data.get('user_id')
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    payment_status = 'success'
    payment_date = datetime.now()
    
    new_payment = Payment(
        user_id=user_id,
        amount=amount,
        payment_method=payment_method,
        payment_status=payment_status,
        payment_date=payment_date
    )
    
    db.session.add(new_payment)
    db.session.commit()
    
    return jsonify({'message': 'Payment processed successfully. Please provide packaging details and arrival time/date.'}), 201

@rosee_blueprint.route('/payment/packaging', methods=['POST'])
def add_packaging_details():
    data = request.get_json()
    
    payment_id = data.get('payment_id')
    packaging_type = data.get('packaging_type')
    packaging_instructions = data.get('packaging_instructions')
    
    new_packaging = Packaging(
        payment_id=payment_id,
        packaging_type=packaging_type,
        packaging_instructions=packaging_instructions
    )
    
    db.session.add(new_packaging)
    db.session.commit()
    
    return jsonify({'message': 'Packaging details added successfully.'}), 201

@rosee_blueprint.route('/payment/arrival', methods=['POST'])
def add_arrival_details():
    data = request.get_json()
    
    payment_id = data.get('payment_id')
    arrival_time = data.get('arrival_time')
    arrival_date = data.get('arrival_date')
    
    new_arrival = Arrival(
        payment_id=payment_id,
        arrival_time=arrival_time,
        arrival_date=arrival_date
    )
    
    db.session.add(new_arrival)
    db.session.commit()
    
    return jsonify({'message': 'Arrival details added successfully.'}), 201
    
# # Route to handle forgotten password
# @rosee_blueprint.route('/forgot_password', methods=['POST'])
# def forgot_password():
#     data = request.get_json()
#     email = data.get('email')
#     user = User.query.filter_by(email=email).first()
#     if user:
#         token = s.dumps(email, salt='password-reset-salt')
#         link = url_for('users.reset_password', token=token, _external=True)

#         msg = Message('Password Reset Request', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
#         msg.body = f'Your password reset link is: {link}'
#         mail.send(msg)

#         return jsonify({'message': 'Password reset link has been sent to your email.'}), 200
#     else:
#         return jsonify({'message': 'Email not found.'}), 404

# # Route to reset the password
# @rosee_blueprint.route('/reset_password/<token>', methods=['POST'])
# def reset_password(token):
#     try:
#         email = s.loads(token, salt='password-reset-salt', max_age=3600)
#     except SignatureExpired:
#         return jsonify({'message': 'The token is expired.'}), 400
#     except BadTimeSignature:
#         return jsonify({'message': 'Invalid token.'}), 400

#     data = request.get_json()
#     new_password = data.get('new_password')
#     hashed_password = generate_password_hash(new_password)

#     user = User.query.filter_by(email=email).first()
#     user.password = hashed_password
#     db.session.commit()

#     return jsonify({'message': 'Password has been reset successfully.'}), 200

# Route to update user details
@rosee_blueprint.route('/update_user', methods=['PUT'])
def update_user():
    data = request.get_json()
    user_id = data.get('id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found.'}), 404

    user.name = data.get('name', user.name)
    user.phone_number = data.get('phone_number', user.phone_number)
    user.email = data.get('email', user.email)
    user.address = data.get('address', user.address)
    user.username = data.get('username', user.username)

    db.session.commit()

    return jsonify({'message': 'User details updated successfully.'}), 200

@rosee_blueprint.route('/feedback', methods=['POST'])
def give_feedback():
    data = request.get_json()

    user_id = data.get('user_id')
    feedback_text = data.get('feedback_text')

    if not user_id or not feedback_text:
        return jsonify({'error': 'User ID and feedback text are required.'}), 400

    new_feedback = Feedback(user_id=user_id, feedback_text=feedback_text)

    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback submitted successfully.'}), 201
@rosee_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected route
    ---
    responses:
      200:
        description: Access granted to protected route
    """
    current_user = get_jwt_identity()
    return jsonify({'message': 'Protected route', 'user': current_user}), 200


if __name__ == "__main__":
    app.run(debug=True)
