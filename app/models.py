from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Enum
from flask import flash
from sqlalchemy.types import DateTime as TimezoneAwareDateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import uuid


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

    feedbacks = db.relationship('Feedback', back_populates='user')

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

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'size': self.size,
            'color': self.color,
            'price': self.price,
            'stock': self.stock
        }

class Cart(db.Model):

    __tablename__= 'cart'

    id = db.Column(db.Integer, primary_key=True)
    clothes_id = db.Column(db.Integer, db.ForeignKey('clothes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"Cart('Clothes id:{self.clothes_id}','id: {self.id}','User id:{self.user_id}'')"
    
class Payment(db.Model):

    __tablename__='payment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(Enum('credit_card', 'paypal', 'bank_transfer', name='payment_method'))
    payment_status = db.Column(Enum('pending', 'success', 'failed', name='payment_status'))
    payment_date = db.Column(TimezoneAwareDateTime, nullable=False, default=datetime.utcnow)

    def as_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'payment_date': self.payment_date
        }

class Packaging(db.Model):

    __tablename__ = 'packaging'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    packaging_type = db.Column(db.String(50), nullable=False)
    packaging_instructions = db.Column(db.Text, nullable=True)

class Arrival(db.Model):

    __tablename__='arrival'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'), nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)

class Feedback(db.Model):
    __tablename__ ='feedback'

    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    feedback_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='feedbacks')

class Admin(db.Model):

    __tablename__ = 'admin'
    
    adminid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password   

    def to_dict(self):
        return {
            "adminid": self.adminid,
            "email": self.email,
            "name": self.name,
            # "password": self.password
        }
    
class Delivery(db.Model):

    __tablename__='delivery'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    delivery_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='assigned')
    assigned_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Employee(db.Model):

    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    date_hired = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'
    
class Supplier(db.Model):

    __tablename__ = 'supplier'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    # One-to-One relationship with BankDetail
    bank_detail = db.relationship('BankDetail', backref='supplier', uselist=False)

    # One-to-Many relationship with Goods
    goods = db.relationship('Goods', backref='supplier', lazy=True)

class BankDetail(db.Model):

    __tablename__ = 'bankdetail'

    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)
    branch_code = db.Column(db.String(20), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

class Goods(db.Model):

    __tablename__ = 'goods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.Float, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)

class PurchaseOrder(db.Model):

    __tablename__='purchaseorder'

    id = db.Column(db.Integer, primary_key=True)
    supplier = db.Column(db.String(50), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total_amount = db.Column(db.Float, nullable=False)

class GoodsReceivedNote(db.Model):

    __tablename__='goodsreceivednote'

    id = db.Column(db.Integer, primary_key=True)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey('purchase_order.id'), nullable=False)
    received_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    items_received = db.Column(db.JSON, nullable=False)

class Invoice(db.Model):
    
    __tablename__='invoice'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    invoice_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
