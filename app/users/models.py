from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    phone_number = Column(String(12))
    email = Column(String(30), unique=True, nullable=False)
    address = Column(String(30), unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    def __init__(self, name, phone_number, email, address, username, password):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.username = username
        self.password = generate_password_hash(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
        }
