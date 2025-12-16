"""
API Routes for Mobile Applications (Flutter)
Returns JSON only, uses JWT authentication
"""

from flask import Blueprint, request, jsonify
from extensions import db
from models import User, Order, Restaurant
from werkzeug.security import check_password_hash
from jwt_manager import jwt_auth
from decorators import jwt_required

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API login endpoint - returns JWT tokens"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        # Create JWT tokens
        tokens = jwt_auth.create_tokens(user.id)
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'user': user.to_dict(),
            **tokens
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    """API registration endpoint"""
    data = request.get_json()
    
    # Validation
    required_fields = ['username', 'email', 'password', 'role']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    # Create user
    from werkzeug.security import generate_password_hash
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data.get('role', 'customer')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Generate tokens
    tokens = jwt_auth.create_tokens(user.id)
    
    return jsonify({
        'status': 'success',
        'message': 'Registration successful',
        'user': user.to_dict(),
        **tokens
    }), 201

@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def api_refresh():
    """Refresh access token using refresh token"""
    from flask_jwt_extended import get_jwt_identity, create_access_token
    
    user_id = get_jwt_identity()
    new_token = create_access_token(identity=user_id)
    
    return jsonify({
        'access_token': new_token,
        'token_type': 'bearer',
        'expires_in': 3600
    }), 200

@api_bp.route('/profile', methods=['GET'])
@jwt_required()
def api_profile():
    """Get current user profile"""
    from flask_jwt_extended import get_jwt_identity
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'status': 'success',
        'user': user.to_dict()
    }), 200

@api_bp.route('/orders', methods=['GET'])
@jwt_required()
def api_orders():
    """Get user's orders (JSON format for mobile)"""
    from flask_jwt_extended import get_jwt_identity
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Determine which orders to show based on role
    if user.role == 'customer':
        orders = Order.query.filter_by(customer_id=user_id).all()
    elif user.role == 'driver':
        orders = Order.query.filter_by(driver_id=user_id).all()
    elif user.role == 'restaurant':
        # Get restaurant owned by user, then its orders
        restaurant = Restaurant.query.filter_by(owner_id=user_id).first()
        orders = Order.query.filter_by(restaurant_id=restaurant.id).all() if restaurant else []
    else:
        orders = []
    
    # Serialize orders to JSON
    orders_data = []
    for order in orders:
        orders_data.append({
            'id': order.id,
            'status': order.status,
            'total_amount': order.total_amount,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'items': [item.to_dict() for item in order.items]
        })
    
    return jsonify({
        'status': 'success',
        'count': len(orders_data),
        'orders': orders_data
    }), 200

@api_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def api_order_detail(order_id):
    """Get specific order details"""
    from flask_jwt_extended import get_jwt_identity
    
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check permission
    can_view = False
    if user.role == 'admin':
        can_view = True
    elif user.role == 'customer' and order.customer_id == user_id:
        can_view = True
    elif user.role == 'driver' and order.driver_id == user_id:
        can_view = True
    elif user.role == 'restaurant':
        restaurant = Restaurant.query.filter_by(owner_id=user_id).first()
        if restaurant and order.restaurant_id == restaurant.id:
            can_view = True
    
    if not can_view:
        return jsonify({'error': 'Permission denied'}), 403
    
    return jsonify({
        'status': 'success',
        'order': order.to_dict()
    }), 200