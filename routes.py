from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Product

# --- YE LINE SABSE ZAROORI HAI (Iske bina error aata hai) ---
routes_bp = Blueprint('main_bp', __name__)

# --- HOMEPAGE ---
@routes_bp.route('/')
def index():
    try:
        products = Product.query.all()
        return render_template('index.html', products=products)
    except Exception as e:
        # Agar table nahi bana to crash hone ke bajaye ye dikhaye
        return "<h1>Database Setup in Progress... Refresh in 10 seconds.</h1>"

# --- LOGIN ROUTE ---
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('Login Failed. Check username/password.', 'danger')
            
    return render_template('login.html')

# --- ADMIN CREATE & DEBUG ROUTE ---
@routes_bp.route('/create-admin')
def create_admin():
    try:
        # Check agar admin pehle se hai
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            return "⚠️ Admin pehle se mojood hai! Login karein: admin / pass123"

        # Naya User Banayen
        new_user = User(username='admin', email='admin@example.com')
        new_user.set_password('pass123')
        
        db.session.add(new_user)
        db.session.commit()
        
        return "✅ SUCCESS: User Created! Go to /login and use: admin / pass123"

    except Exception as e:
        return f"🔥 ERROR: {str(e)}"

# --- DASHBOARD ---
@routes_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', products=Product.query.all())

# --- LOGOUT ---
@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
