from flask import Blueprint, request, jsonify, session
from app.schemas import AdminSchema
from app import db
from app.admin.models import Admin
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from flasgger import swag_from
from flask_session import Session
from app.models import User, ClothingItem, Cart, Payment, Delivery, GoodsReceivedNote
from datetime import datetime


admin_blueprint = Blueprint('admin', __name__, url_prefix='/api/admin')

admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)


@admin_blueprint.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Admin registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'admin': {
                        'type': 'object'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input, Missing required fields'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string'
                    },
                    'name': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    }
                }
            }
        }
    ]
})
def register_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    name = data.get('name')
    password = data.get('password')

    logging.debug(f"Received data - Email: {email}, Name: {name}, Password: {password}")

    if not all([email, name, password]):
        return jsonify({"error": "Missing required fields"}), 400

    if Admin.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email exists"}), 400

    if Admin.query.filter_by(name=name).first() is not None:
        return jsonify({"error": "Name already registered"}), 400

    if password is None:
        logging.error("Password is None before hashing")
        return jsonify({"error": "Password cannot be None"}), 400

    hashed_password = generate_password_hash(password)
    logging.debug(f"Hashed Password: {hashed_password}")

    admin = Admin(
        email=email,
        name=name,
        password=hashed_password)

    db.session.add(admin)
    db.session.commit()
    return jsonify({"message": "Admin registered successfully", "admin": admin.to_dict()}), 201

@admin_blueprint.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string'
                    },
                    'admin': {
                        'type': 'object'
                    }
                }
            }
        },
        400: {
            'description': 'Invalid input'
        },
        401: {
            'description': 'Unauthorized'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {
                        'type': 'string'
                    },
                    'password': {
                        'type': 'string'
                    }
                }
            }
        }
    ]
})
def login_admin():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    admin = Admin.query.filter_by(email=email).first()

    session['admin_id'] = admin.adminid
    session['admin_email'] = admin.email
    return jsonify({"message": "Login successful", "admin": admin.to_dict()}), 200

@admin_blueprint.route('/list', methods=['GET'])
def get_items():
    items = ClothingItem.query.all()
    return jsonify([item.as_dict() for item in items])

@admin_blueprint.route('/items', methods=['POST'])
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

@admin_blueprint.route('/items/<int:id>', methods=['PUT'])
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

@admin_blueprint.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = ClothingItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

# Route to get the number of logged-in users
@admin_blueprint.route('/logged_in_users', methods=['GET'])
def get_logged_in_users():
    logged_in_users = User.query.filter_by(logged_in=True).count()
    return jsonify({'logged_in_users': logged_in_users})

# Route to get user details
@admin_blueprint.route('/user_details', methods=['GET'])
def get_user_details():
    users = User.query.all()
    user_details = [{
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'email': user.email,
        'phone_number': user.phone_number,
        'address': user.address
    } for user in users]
    return jsonify(user_details)

# Route to track clothes quantity
@admin_blueprint.route('/clothes_quantity', methods=['GET'])
def get_clothes_quantity():
    clothes = Clothes.query.all()
    clothes_quantity = [{
        'id': item.id,
        'name': item.name,
        'quantity': item.quantity
    } for item in clothes]
    return jsonify(clothes_quantity)

# Route to show reports of number of purchases and profits
@admin_blueprint.route('/reports', methods=['GET'])
def get_reports():
    purchases = db.session.query(db.func.count(Payment.id)).scalar()
    total_profit = db.session.query(db.func.sum(Payment.amount)).scalar()
    return jsonify({'purchases': purchases, 'total_profit': total_profit})

# Route to assign delivery
@admin_blueprint.route('/assign_delivery', methods=['POST'])
def assign_delivery():
    data = request.get_json()
    user_id = data.get('user_id')
    delivery_cost = data.get('delivery_cost')
    
    new_delivery = Delivery(user_id=user_id, delivery_cost=delivery_cost, status='assigned', assigned_date=datetime.now())
    db.session.add(new_delivery)
    db.session.commit()
    
    return jsonify({'message': 'Delivery assigned successfully'}), 201

# Route to generate income statement
@admin_blueprint.route('/income_statement', methods=['GET'])
def generate_income_statement():
    total_sales = db.session.query(db.func.sum(Payment.amount)).scalar()
    delivery_costs = db.session.query(db.func.sum(Delivery.delivery_cost)).scalar()
    total_profit = total_sales - delivery_costs

    income_statement = {
        'total_sales': total_sales,
        'delivery_costs': delivery_costs,
        'total_profit': total_profit
    }
    return jsonify(income_statement)

# Balance Sheet
@admin_blueprint.route('/balance_sheet', methods=['GET'])
def balance_sheet():
    # Simplified example
    total_assets = db.session.query(db.func.sum(Clothes.price * Clothes.quantity)).scalar()
    total_liabilities = db.session.query(db.func.sum(Payment.amount)).scalar()  # This should be adjusted based on actual liabilities
    equity = total_assets - total_liabilities

    balance_sheet = {
        'total_assets': total_assets,
        'total_liabilities': total_liabilities,
        'equity': equity
    }
    return jsonify(balance_sheet)

# Sales Journal
@admin_blueprint.route('/sales_journal', methods=['GET'])
def sales_journal():
    sales = Payment.query.all()
    sales_data = [{
        'id': sale.id,
        'user_id': sale.user_id,
        'amount': sale.amount,
        'payment_method': sale.payment_method,
        'payment_date': sale.payment_date
    } for sale in sales]
    return jsonify(sales_data)

# Delivery Note
@admin_blueprint.route('/delivery_note/<int:delivery_id>', methods=['GET'])
def delivery_note(delivery_id):
    delivery = Delivery.query.get(delivery_id)
    if not delivery:
        return jsonify({'message': 'Delivery not found'}), 404

    delivery_note = {
        'id': delivery.id,
        'user_id': delivery.user_id,
        'delivery_cost': delivery.delivery_cost,
        'status': delivery.status,
        'assigned_date': delivery.assigned_date
    }
    return jsonify(delivery_note)

# Dispatch Register
@admin_blueprint.route('/dispatch_register', methods=['GET'])
def dispatch_register():
    deliveries = Delivery.query.all()
    dispatch_data = [{
        'id': delivery.id,
        'user_id': delivery.user_id,
        'delivery_cost': delivery.delivery_cost,
        'status': delivery.status,
        'assigned_date': delivery.assigned_date
    } for delivery in deliveries]
    return jsonify(dispatch_data)

# Income Statement
@admin_blueprint.route('/income_statement', methods=['GET'])
def income_statement():
    total_sales = db.session.query(db.func.sum(Payment.amount)).scalar()
    delivery_costs = db.session.query(db.func.sum(Delivery.delivery_cost)).scalar()
    total_profit = total_sales - delivery_costs

    income_statement = {
        'total_sales': total_sales,
        'delivery_costs': delivery_costs,
        'total_profit': total_profit
    }
    return jsonify(income_statement)

# Cash Flow Statement
@admin_blueprint.route('/cash_flow_statement', methods=['GET'])
def cash_flow_statement():
    total_inflows = db.session.query(db.func.sum(Payment.amount)).scalar()
    total_outflows = db.session.query(db.func.sum(Delivery.delivery_cost)).scalar()
    net_cash_flow = total_inflows - total_outflows

    cash_flow_statement = {
        'total_inflows': total_inflows,
        'total_outflows': total_outflows,
        'net_cash_flow': net_cash_flow
    }
    return jsonify(cash_flow_statement)

# Purchase Order
@admin_blueprint.route('/purchase_order', methods=['GET'])
def get_purchase_orders():
    purchase_orders = PurchaseOrder.query.all()
    po_data = [{
        'id': po.id,
        'supplier': po.supplier,
        'order_date': po.order_date,
        'total_amount': po.total_amount
    } for po in purchase_orders]
    return jsonify(po_data)

# Goods Received Note
@admin_blueprint.route('/goods_received_note/<int:grn_id>', methods=['GET'])
def goods_received_note(grn_id):
    grn = GoodsReceivedNote.query.get(grn_id)
    if not grn:
        return jsonify({'message': 'Goods received note not found'}), 404

    grn_data = {
        'id': grn.id,
        'purchase_order_id': grn.purchase_order_id,
        'received_date': grn.received_date,
        'items_received': grn.items_received
    }
    return jsonify(grn_data)

# Invoice
@admin_blueprint.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoice = Invoice.query.get(invoice_id)
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404

    invoice_data = {
        'id': invoice.id,
        'user_id': invoice.user_id,
        'amount': invoice.amount,
        'invoice_date': invoice.invoice_date
    }
    return jsonify(invoice_data)
@admin_blueprint.route('/logout', methods=['POST'])
def logout_admin():
    session.pop('admin_id', None)
    session.pop('admin_email', None)
    return jsonify({"message": "Logged out successfully"}), 200

@admin_blueprint.route('/session', methods=['GET'])
def get_session():
    if 'admin_id' in session:
        return jsonify({"admin_id": session['admin_id'], "admin_email": session['admin_email']}), 200
    return jsonify({"error": "No active session"}), 401
