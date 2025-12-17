from flask import Flask, render_template, redirect, url_for, request, session, Blueprint, flash
from extensions import db
from models import User, Product, Order
from cart_manager import CartManager
from state_machine import OrderStateMachine
from functools import wraps
import bcrypt

main_bp = Blueprint('main_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('main_bp.login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return render_template('register.html')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user = User(username=username, email=email, password_hash=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main_bp.login'))
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('main_bp.index'))
        else:
            flash('Invalid username or password.')
            return render_template('login.html')

    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('main_bp.index'))

@main_bp.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@main_bp.route('/cart')
@login_required
def cart():
    cart_manager = CartManager(session)
    cart_items = cart_manager.get_cart_items()
    total = cart_manager.get_cart_total()
    return render_template('cart.html', cart_items=cart_items, total=total)

@main_bp.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    cart_manager = CartManager(session)
    cart_manager.add_product(product_id)
    return redirect(url_for('main_bp.cart'))

@main_bp.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart_manager = CartManager(session)
    cart_manager.remove_product(product_id)
    return redirect(url_for('main_bp.cart'))

@main_bp.route('/clear_cart')
@login_required
def clear_cart():
    cart_manager = CartManager(session)
    cart_manager.clear_cart()
    return redirect(url_for('main_bp.cart'))

@main_bp.route('/checkout')
@login_required
def checkout():
    cart_manager = CartManager(session)
    cart_items = cart_manager.get_cart_items()
    total = cart_manager.get_cart_total()

    if not cart_items:
        flash("Your cart is empty.")
        return redirect(url_for('main_bp.cart'))

    return render_template('checkout.html', cart_items=cart_items, total=total)

@main_bp.route('/orders')
@login_required
def orders():
    user_id = session['user_id']
    orders = Order.query.filter_by(customer_id=user_id).all()
    return render_template('orders.html', orders=orders)