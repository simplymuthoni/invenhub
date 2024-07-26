from flask import Flask, request, jsonify, Blueprint, session, url_for
from flasgger import Swagger
from app.models import User, ClothingItem, Cart, Payment, Packaging, Arrival, Feedback
from app import mail, db, bcrypt
from app.schemas import UserSchema
from flask_session import Session
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
import string
import random
import os
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Mail, Message

user_schema = UserSchema()
users_schema = UserSchema(many=True)

app = Flask(__name__)
swagger = Swagger(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')  
Session(app)
jwt = JWTManager(app)  # Initialize JWTManager

# Initialize Flask-Mail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)
s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

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
    """
    Homepage
    ---
    responses:
      200:
        description: Welcome message
    """
    return jsonify({'message': 'Welcome to Rosee Thrifts '}), 200

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - phone_number
            - email
            - address
            - username
          properties:
            name:
              type: string
            phone_number:
              type: string
            email:
              type: string
            address:
              type: string
            username:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input
    """
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
    """
    Login a user
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
      403:
        description: Password reset required
    """
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
    """
    Reset user password
    ---
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - username
            - new_password
          properties:
            username:
              type: string
            new_password:
              type: string
    responses:
      200:
        description: Password reset successful
      404:
        description: User not found
    """
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
@app.route('/items', methods=['GET'])
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
@app.route('/cart', methods=['POST'])
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
@app.route('/cart', methods=['GET'])
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
@app.route('/cart/<int:cart_item_id>', methods=['DELETE'])
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

@app.route('/payment', methods=['POST'])
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

@app.route('/payment/<int:id>', methods=['GET'])
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

@app.route('/payment/<int:id>', methods=['PUT'])
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

@app.route('/payment/<int:id>', methods=['DELETE'])
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
    
@app.route('/payment/success', methods=['POST'])
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

@app.route('/payment/packaging', methods=['POST'])
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

@app.route('/payment/arrival', methods=['POST'])
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
    
# Route to handle forgotten password
@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        token = s.dumps(email, salt='password-reset-salt')
        link = url_for('users.reset_password', token=token, _external=True)

        msg = Message('Password Reset Request', sender=os.getenv('MAIL_USERNAME'), recipients=[email])
        msg.body = f'Your password reset link is: {link}'
        mail.send(msg)

        return jsonify({'message': 'Password reset link has been sent to your email.'}), 200
    else:
        return jsonify({'message': 'Email not found.'}), 404

# Route to reset the password
@app.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return jsonify({'message': 'The token is expired.'}), 400
    except BadTimeSignature:
        return jsonify({'message': 'Invalid token.'}), 400

    data = request.get_json()
    new_password = data.get('new_password')
    hashed_password = generate_password_hash(new_password)

    user = User.query.filter_by(email=email).first()
    user.password = hashed_password
    db.session.commit()

    return jsonify({'message': 'Password has been reset successfully.'}), 200

# Route to update user details
@app.route('/update_user', methods=['PUT'])
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

@app.route('/feedback', methods=['POST'])
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
