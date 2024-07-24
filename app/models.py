from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from flask import flash
from models import Cart

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True, nullable=False)
    phone_number = Column(String(12))
    email = Column(String(30), unique=True, nullable=False)
    address = Column(String(30), unique=True, nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    password_reset_required = db.Column(db.Boolean, default=True)
    cart = db.relationship('Cart', backref='buyer', lazy=True)

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
    
    def add_to_cart(self,clothes_id):
        item_to_add = Cart(clothes_id=clothes_id, user_id=self.id)
        db.session.add(item_to_add)
        db.session.commit()
        flash('Your item has been added to your cart!', 'success')

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            'password_reset_required': self.password_reset_required
        }

class ClothingItem(db.Model):
    
    __tablename__= 'clothes'

    id = db.Column(db.Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    size = Column(String(10), nullable=False)
    color = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

class Cart(db.Model):

    __tablename__= 'cart'

    id = db.Column(db.Integer, primary_key=True)
    clothes_id = db.Column(db.Integer, db.ForeignKey('clothes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Cart('Clothes id:{self.clothes_id}','id: {self.id}','User id:{self.user_id}'')"