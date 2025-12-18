from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Product

# Blueprint ka naam 'main_bp' hi rakhna zaroori hai (Settings ke hisaab se)
routes_bp = Blueprint('main_bp', __name__)

@routes_bp.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# --- LOGIN LOGIC (FIXED) ---
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Form se data uthao
        username = request.form.get('username')
        password = request.form.get('password')
        
        # User dhoondo
        user = User.query.filter_by(username=username).first()
        
        # Check password
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('Login Failed. Check username/password.', 'danger')
            
    return render_template('login.html')

# --- TEMPORARY: USER CREATE KARNE KA RAASTA ---
@routes_bp.route('/create-admin')
def create_admin():
    # Check agar admin pehle se hai
    if User.query.filter_by(username='admin').first():
        return "Admin already exists! Login with: admin / pass123"
        
    # Naya user banao
    user = User(username='admin', email='admin@example.com')
    user.set_password('pass123') # Password ye hoga
    db.session.add(user)
    db.session.commit()
    return "User Created! Go to /login and use: admin / pass123"

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', products=Product.query.all()) # Filhal index dikhayega login ke baad

@routes_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))
