import os
from pathlib import Path

# --- DEVELOPER CONFIGURATION ---
PROJECT_NAME = "delivery_production_v2"
BASE_DIR = Path(f"projects/{PROJECT_NAME}")

print(f"🚀 AGENT 50: DEPLOYING {PROJECT_NAME} (WEEK 2 ARCHITECTURE)")
print("Target: 100% Match with Developer Specifications")

# Ensure Directory Exists
os.makedirs(BASE_DIR, exist_ok=True)

# ==========================================
# 1. PAYMENT HANDLER (From Module 1.1)
# ==========================================
payment_code = '''"""
Stripe Payment Gateway Integration
Handles checkout, webhooks, and payment status
"""
import stripe
from flask import Blueprint, request, jsonify, current_app, url_for
from datetime import datetime
from extensions import db
from models import Order, Transaction, User
# from decorators import login_required # (Assuming decorators exist)

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

class PaymentManager:
    def __init__(self, app=None):
        self.stripe = None
        self.webhook_secret = None
        self.currency = 'usd'
        
    def init_app(self, app):
        stripe.api_key = app.config.get('STRIPE_SECRET_KEY')
        self.stripe = stripe
        self.webhook_secret = app.config.get('STRIPE_WEBHOOK_SECRET')
        print(f"[PAYMENT] Stripe initialized")
        
    def create_checkout_session(self, order_id, user_id, success_url=None, cancel_url=None):
        order = Order.query.get(order_id)
        if not order or order.customer_id != user_id:
            raise ValueError("Invalid order")
            
        line_items = []
        for item in order.items:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.product.name},
                    'unit_amount': int(item.product.price * 100)
                },
                'quantity': item.quantity
            })
            
        if order.delivery_fee > 0:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': 'Delivery Fee'},
                    'unit_amount': int(order.delivery_fee * 100)
                },
                'quantity': 1
            })
            
        session = self.stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url or 'http://localhost:5000/payment/success',
            cancel_url=cancel_url or 'http://localhost:5000/payment/cancel',
            metadata={'order_id': order.id, 'user_id': user_id}
        )
        
        transaction = Transaction(
            order_id=order.id,
            stripe_payment_intent_id=session.payment_intent,
            stripe_session_id=session.id,
            amount=order.total_amount + order.delivery_fee,
            status='pending',
            payment_method='card'
        )
        db.session.add(transaction)
        db.session.commit()
        return session

payment_manager = PaymentManager()
'''

# ==========================================
# 2. CART MANAGER (From Module 1.3)
# ==========================================
cart_code = '''"""
Shopping cart and checkout management
"""
from flask import session
from extensions import db
from models import Cart, CartItem, Product, Order, OrderItem

class CartManager:
    def get_or_create_cart(self, user_id=None):
        if user_id:
            cart = Cart.query.filter_by(user_id=user_id, status='active').first()
            if cart: return cart
        
        cart = Cart(user_id=user_id, status='active', session_id=session.get('sid'))
        db.session.add(cart)
        db.session.commit()
        return cart

    def add_to_cart(self, product_id, quantity=1, user_id=None):
        cart = self.get_or_create_cart(user_id)
        product = Product.query.get(product_id)
        if not product: raise ValueError("Product not found")
        
        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, price=product.price)
            db.session.add(cart_item)
        
        db.session.commit()
        return cart_item

    def convert_cart_to_order(self, cart_id, delivery_address, user_id):
        cart = Cart.query.get(cart_id)
        if not cart or cart.status != 'active': raise ValueError("Invalid cart")
        
        total_amount = sum(item.price * item.quantity for item in cart.items)
        order = Order(
            customer_id=user_id,
            total_amount=total_amount,
            delivery_address=delivery_address,
            status='pending_payment'
        )
        db.session.add(order)
        
        for cart_item in cart.items:
            order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, quantity=cart_item.quantity, price=cart_item.price)
            db.session.add(order_item)
            
            product = Product.query.get(cart_item.product_id)
            if product.stock_quantity is not None:
                product.stock_quantity -= cart_item.quantity
        
        cart.status = 'converted'
        cart.order_id = order.id
        db.session.commit()
        return order
'''

# ==========================================
# 3. SOCKETIO HANDLER (From Module 2.1)
# ==========================================
socket_code = '''"""
WebSocket/Socket.IO real-time communication
"""
from flask_socketio import SocketIO, emit, join_room
from flask import request
from extensions import db
from models import Order, User
from datetime import datetime

socketio = SocketIO(cors_allowed_origins="*")

def init_socketio(app):
    socketio.init_app(app)
    return socketio

@socketio.on('connect')
def handle_connect():
    user_id = request.args.get('user_id')
    if user_id:
        join_room(f"user_{user_id}")
        print(f"User {user_id} connected via WebSocket")
        return True
    return False

@socketio.on('driver_location_update')
def handle_driver_location(data):
    driver_id = request.args.get('user_id') # Simplified
    order_id = data.get('order_id')
    lat = data.get('lat')
    lng = data.get('lng')
    
    if all([order_id, lat, lng]):
        order = Order.query.get(order_id)
        if order:
            order.driver_latitude = lat
            order.driver_longitude = lng
            db.session.commit()
            
            emit('driver_location_updated', {
                'order_id': order_id,
                'lat': lat, 'lng': lng,
                'timestamp': datetime.utcnow().isoformat()
            }, room=f"order_{order_id}")

@socketio.on('join_order_room')
def handle_join_order_room(data):
    order_id = data.get('order_id')
    if order_id:
        join_room(f"order_{order_id}")
        emit('joined', {'msg': f'Joined order {order_id}'})
'''

# ==========================================
# 4. STATE MACHINE (From Module 3.1)
# ==========================================
state_code = '''"""
Order lifecycle state machine with validation rules
"""
from datetime import datetime
from extensions import db
from models import Order, InventoryLog, OrderStateChange, Transaction

class OrderStateMachine:
    TRANSITIONS = {
        'pending': ['pending_payment', 'cancelled'],
        'pending_payment': ['accepted', 'payment_failed', 'cancelled'],
        'payment_failed': ['pending_payment', 'cancelled'],
        'accepted': ['preparing', 'cancelled'],
        'preparing': ['ready', 'cancelled'],
        'ready': ['picked_up', 'cancelled'],
        'picked_up': ['delivered'],
        'delivered': [],
        'cancelled': ['refunded'],
        'refunded': []
    }

    @classmethod
    def can_transition(cls, from_state, to_state):
        return to_state in cls.TRANSITIONS.get(from_state, [])

    @classmethod
    def transition(cls, order, new_state, changed_by_user_id, reason=None):
        if not cls.can_transition(order.status, new_state):
            raise ValueError(f"Invalid transition: {order.status} -> {new_state}")
            
        old_state = order.status
        order.status = new_state
        
        # Log Change
        change = OrderStateChange(
            order_id=order.id, from_state=old_state, to_state=new_state,
            changed_by_user_id=changed_by_user_id, reason=reason
        )
        db.session.add(change)
        
        # Side Effects
        if new_state == 'cancelled':
            cls.restore_inventory(order)
            
        db.session.commit()
        return True

    @classmethod
    def restore_inventory(cls, order):
        for item in order.items:
            product = item.product
            if product.stock_quantity is not None:
                product.stock_quantity += item.quantity
                log = InventoryLog(product_id=product.id, quantity_change=item.quantity, reason=f"Restored order #{order.id}")
                db.session.add(log)
'''

# ==========================================
# 5. GEOLOCATION (From Module 4.1)
# ==========================================
geo_code = '''"""
Geolocation services for delivery calculations
"""
from math import radians, sin, cos, sqrt, atan2

class GeoLocationService:
    EARTH_RADIUS_KM = 6371
    
    @classmethod
    def haversine_distance(cls, lat1, lon1, lat2, lon2):
        if not all([lat1, lon1, lat2, lon2]): return 0.0
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return cls.EARTH_RADIUS_KM * c

    @classmethod
    def calculate_delivery_fee(cls, r_lat, r_lng, c_lat, c_lng, base=2.99, rate=1.50):
        dist = cls.haversine_distance(r_lat, r_lng, c_lat, c_lng)
        if dist <= 2: return base
        return round(base + (max(0, dist - 2) * rate), 2)
'''

# ==========================================
# 6. ENHANCED MODELS (From Developer Template)
# ==========================================
models_code = '''
from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='customer')
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    is_available = db.Column(db.Boolean, default=True) # Driver specific
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(50), default='pending_payment')
    total_amount = db.Column(db.Float)
    delivery_fee = db.Column(db.Float)
    payment_status = db.Column(db.String(20), default='pending')
    delivery_address = db.Column(db.String(200))
    driver_latitude = db.Column(db.Float)
    driver_longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    product = db.relationship('Product')

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    stripe_payment_intent_id = db.Column(db.String(100))
    stripe_session_id = db.Column(db.String(100))
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity_change = db.Column(db.Integer)
    reason = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class OrderStateChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    from_state = db.Column(db.String(50))
    to_state = db.Column(db.String(50))
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reason = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')
    items = db.relationship('CartItem', backref='cart')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
'''

# ==========================================
# 7. APP.PY (Updated with SocketIO)
# ==========================================
app_code = '''
import os
from flask import Flask
from extensions import db, jwt, socketio
from flask_cors import CORS
from payment_handler import payment_bp
from socketio_handler import init_socketio

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'delivery_v2.db')
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_placeholder'
    app.config['STRIPE_WEBHOOK_SECRET'] = 'whsec_placeholder'
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    init_socketio(app)
    
    app.register_blueprint(payment_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database Tables Created")
        
    print("🚀 Starting Production Server with Socket.IO...")
    socketio.run(app, debug=True, port=5000)
'''

# ==========================================
# 8. EXTENSIONS (With SocketIO)
# ==========================================
ext_code = '''from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()
'''

# WRITE ALL FILES
files_map = {
    "payment_handler.py": payment_code,
    "cart_manager.py": cart_code,
    "socketio_handler.py": socket_code,
    "state_machine.py": state_code,
    "geolocation.py": geo_code,
    "models.py": models_code,
    "app.py": app_code,
    "extensions.py": ext_code
}

for filename, content in files_map.items():
    path = BASE_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✅ Created: {filename}")

print("\n🎉 Week 2 Deployment Complete! Project created in: " + str(BASE_DIR))