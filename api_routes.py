from flask import Blueprint, request, jsonify, session
from models import User, Order
from extensions import db
from functools import wraps

api_bp = Blueprint('api_bp', __name__, url_prefix='/')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'message': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'message': 'Invalid request'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session['user_id'] = user.id
        return jsonify({'message': 'Login successful', 'user_id': user.id}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@api_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logout successful'}), 200


@api_bp.route('/orders', methods=['GET'])
@login_required
def get_orders():
    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    orders = Order.query.filter_by(user_id=user.id).all()
    order_list = []
    for order in orders:
        order_data = {
            'id': order.id,
            'order_date': order.order_date.isoformat(),
            'total_amount': float(order.total_amount),
            'status': order.status
            # Add other order details as needed
        }
        order_list.append(order_data)

    return jsonify(order_list), 200