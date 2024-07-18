from flask import Blueprint, request, jsonify
from app.models import db, ClothingItem

main = Blueprint('main', __name__)

@main.route('/items', methods=['GET'])
def get_items():
    items = ClothingItem.query.all()
    return jsonify([item.as_dict() for item in items])

@main.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = ClothingItem(
        name=data['name'],
        category=data['category'],
        size=data['size'],
        color=data['color'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.as_dict()), 201

@main.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = ClothingItem.query.get_or_404(id)
    item.name = data['name']
    item.category = data['category']
    item.size = data['size']
    item.color = data['color']
    item.price = data['price']
    item.stock = data['stock']
    db.session.commit()
    return jsonify(item.as_dict())

@main.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = ClothingItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204
