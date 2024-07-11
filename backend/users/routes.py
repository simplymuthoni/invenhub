from flask import Flask, request, jsonify, Blueprint, session
from flasgger import Swagger
from users.models import User
from schemas import UserSchema
from . import db
from flask_session import Session

app = Flask(__name__)
swagger = Swagger(app)

# Initialize Flask-Session
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'supersecretkey'
Session(app)

auth = Blueprint('auth', __name__, url_prefix='/api/auth')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@auth.route('/login', methods=['POST'])
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
            - email
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

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.filter_by(email=email).first()

    # if user is None or not check_password_hash(user.password, password):
    #     return jsonify({"error": "Invalid email or password"}), 400

    session['user_id'] = user.id
    session['user_email'] = user.email

    return jsonify({"message": "Login successful", "user": user.to_dict()}), 200

@auth.route('/logout', methods=['POST'])
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

app.register_blueprint(auth)

if __name__='__main__':
    app.run(debug=True)
