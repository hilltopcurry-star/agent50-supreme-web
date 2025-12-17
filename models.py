from extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# --- 1. User Model ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='customer')
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    is_available = db.Column(db.Boolean, default=False)
    
    # Cart Relationship
    cart = db.relationship('Cart', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- 2. Driver Model ---
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='available')
    current_lat = db.Column(db.Float, default=0.0)
    current_lng = db.Column(db.Float, default=0.0)
    user = db.relationship('User', backref='driver_profile')

# --- 3. Product Model ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False, default=100)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(300))
    category = db.Column(db.String(50), default='main')

    def __repr__(self):
        return f'<Product {self.name}>'

# Alias for compatibility
MenuItem = Product

# --- 4. Cart Models (NEW: Added to fix Error) ---
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Nullable for guest carts
    created_at = db.Column(DateTime, default=datetime.utcnow)
    items = db.relationship('CartItem', backref='cart', lazy='dynamic')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product')

# --- 5. Order Models ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    driver_id = db.Column(db.Integer, ForeignKey('driver.id'), nullable=True)
    status = db.Column(db.String(50), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, nullable=True)
    order_date = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("User", foreign_keys=[customer_id])
    driver = relationship("Driver", foreign_keys=[driver_id])
    items = db.relationship('OrderItem', backref='order', lazy='dynamic')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False) # Price at time of order
    product = db.relationship('Product')

# --- 6. Other Logs ---
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, ForeignKey('order.id'), nullable=True)
    order = relationship("Order")

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product")
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(DateTime, default=datetime.utcnow)

class OrderStateChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('order.id'), nullable=False)
    order = relationship("Order")
    from_state = db.Column(db.String(50), nullable=False)
    to_state = db.Column(db.String(50), nullable=False)
    changed_by = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    changed_by_user = relationship("User")
    timestamp = db.Column(DateTime, default=datetime.utcnow)
