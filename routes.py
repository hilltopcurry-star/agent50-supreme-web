from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db
from models import User, Product

# --- YE DEKHEIN: Pehle Blueprint bana, phir use hoga ---
routes_bp = Blueprint('main_bp', __name__)

# --- HOMEPAGE ---
@routes_bp.route('/')
def index():
    try:
        # Check agar database khali hai to crash na ho
        products = Product.query.all()
        return render_template('index.html', products=products)
    except:
        return "<h1>Database ban raha hai... 10 second baad refresh karein.</h1>"

# --- LOGIN ROUTE (Fixed) ---
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # User dhoondo
        user = User.query.filter_by(username=username).first()
        
        # Agar user mil gaya aur password sahi hai
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main_bp.dashboard'))
        else:
            flash('Login Failed. Check username/password.', 'danger')
            
    return render_template('login.html')

# --- CREATE ADMIN (Smart Way) ---
@routes_bp.route('/create-admin')
def create_admin():
    try:
        # Check karein agar admin pehle se hai
        existing_user = User.query.filter_by(username='admin').first()
        if existing_user:
            return "⚠️ Admin pehle se mojood hai! Login karein: admin / pass123"

        # Naya Admin banayen
        user = User(username='admin', email='admin@example.com')
        user.set_password('pass123')
        db.session.add(user)
        db.session.commit()
        
        return "✅ User Created Successfully! Ab Login page par jayen."
        
    except Exception as e:
        return f"🔥 Error: {str(e)}"

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
