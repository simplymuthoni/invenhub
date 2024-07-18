from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

db = SQLAlchemy()

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    size = Column(String(10), nullable=False)
    color = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
