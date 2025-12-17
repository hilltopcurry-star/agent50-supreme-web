from extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='customer')  # e.g., 'customer', 'delivery_person', 'admin'
    lat = db.Column(db.Float, nullable=True)
    lng = db.Column(db.Float, nullable=True)
    is_available = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock_quantity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    customer = relationship("User")
    status = db.Column(db.String(50), default='pending')  # e.g., 'pending', 'processing', 'delivered', 'cancelled'
    total_amount = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, nullable=True)
    delivery_lat = db.Column(db.Float, nullable=True)
    delivery_lng = db.Column(db.Float, nullable=True)
    order_date = db.Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Order {self.id}>'

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stripe_payment_intent_id = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., 'pending', 'succeeded', 'failed'
    order_id = db.Column(db.Integer, ForeignKey('order.id'), nullable=True)
    order = relationship("Order")

    def __repr__(self):
        return f'<Transaction {self.stripe_payment_intent_id}>'

class InventoryLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('product.id'), nullable=False)
    product = relationship("Product")
    quantity_change = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=True)  # e.g., 'order', 'restock', 'adjustment'
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