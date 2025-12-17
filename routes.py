from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Product, Order, Cart, CartItem # Models ab mojood hain

# --- YE RAHA FIX: Variable ka naam 'routes_bp' hona chahiye ---
routes_bp = Blueprint('main_bp', __name__)

# --- Routes ---

@routes_bp.route('/')
def index():
    # Show all products on Homepage
    products = Product.query.all()
    return render_template('index.html', products=products)

@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Placeholder for Login (Agent ne template banaya hoga)
    return render_template('login.html')

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome {current_user.username} to your Dashboard!"

@routes_bp.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    # Simple logic to test database connection
    product = Product.query.get_or_404(product_id)
    flash(f'Added {product.name} to cart!', 'success')
    return redirect(url_for('routes_bp.index'))

@routes_bp.route('/cart')
@login_required
def view_cart():
    return "Cart Page (Under Construction)"

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('routes_bp.index'))
