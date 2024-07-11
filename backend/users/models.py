from . import db
from werkzeug.security import generate_password_hash,
check_password_hash

class User(db.Model):

    __tablename__ ='user'

    id = db.Column(db.Integer, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(30), unique=True, nullable=False)
    phone_number = db.Column(db.String(12))
    email = db.Column(db.String(30), unique=True, nullable=False)
    address = db.Column(db.String(30), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    
    def set_password(self, password):
	self.password_hash = generate_password_hash(password)
	
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __init__(self, name, phone_number, email, address, username, password):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address= address
        self.username = username
        self.password = password

    def to_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "username": self.username,
            "password": self.password
        }
