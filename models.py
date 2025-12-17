from extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime
from flask_login import UserMixin   # <--- Added for Login
from werkzeug.security import generate_password_hash, check_password_hash # <--- Added for Password

# --- User Model (Updated with Login features) ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='customer')  # e.g., 'customer', 'driver', 'admin'
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    is_available = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

# --- Driver Model (NEW: Added to fix Error) ---
class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), default='available')
    current_lat = db.Column(db.Float, default=0.0)
    current_lng = db.Column(db.Float, default=0.0)
    
    # Link Driver back to User
    user = db.relationship('User', backref='driver_profile')

# --- Product (Same as before + Alias for MenuItem) ---
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(300)) # Added for images
    category = db.Column(db.String(50), default='main')

    def __repr__(self):
        return f'<Product {self.name}>'

# Agar Agent "MenuItem" dhoondhe, to usay Product hi mile
MenuItem = Product 

# --- Order (Updated to link with Driver) ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    
    # Driver ID (Added so we can assign drivers)
    driver_id = db.Column(db.Integer, ForeignKey('driver.id'), nullable=True)
    
    status = db.Column(db.String(50), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, nullable=True)
    delivery_lat = db.Column(db.Float, nullable=True)
    delivery_lng = db.Column(db.Float, nullable=True)
    items_json = db.Column(db.Text) # To store list of items
    order_date = db.Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    customer = relationship("User", foreign_keys=[customer_id])
    driver = relationship("Driver", foreign_keys=[driver_id])
    
    def __repr__(self):
        return f'<Order {self.id}>'

# --- Existing Classes (Kept Safe) ---
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    order_id = db.Column(db.Integer, ForeignKey('order.id'), nullable=True)
    order = relationship("Order")

    def __repr__(self):
        return f'<Transaction {self.stripe_payment_intent_id}>'

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product")
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    timestamp = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InventoryLog {self.product_id} - {self.quantity_change}>'

class OrderStateChange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('order.id'), nullable=False)
    order = relationship("Order")
    from_state = db.Column(db.String(50), nullable=False)
    to_state = db.Column(db.String(50), nullable=False)
    changed_by = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    changed_by_user = relationship("User")
    timestamp = db.Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<OrderStateChange {self.order_id} - {self.from_state} to {self.to_state}>'
