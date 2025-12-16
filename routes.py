from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models import User, Order, Restaurant, MenuItem
from extensions import db

# Blueprint define kar rahe hain (Taake app.py isay pehchan sake)
main_bp = Blueprint('main', __name__)

# ==========================================
# 1. PUBLIC ROUTES
# ==========================================

@main_bp.route('/')
def index():
    """Home Page - Landing Page"""
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    SMART LOGIN SYSTEM (DUAL MODE)
    - Agar Mobile App se request aayi -> Return JSON Token
    - Agar Browser se request aayi -> Redirect to Dashboard
    """
    # Agar user pehle se login hai
    if 'user_id' in session and not request.is_json:
        return redirect(url_for('main.dashboard'))

    # POST REQUEST HANDLE KARNA
    if request.method == 'POST':
        # Data fetch karo (JSON ya Form)
        if request.is_json:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        # User dhoondo
        user = User.query.filter_by(email=email).first()

        # Password check karo (Secure Hash)
        if user and user.check_password(password):
            
            # --- MOBILE APP RESPONSE (JSON) ---
            if request.is_json:
                return jsonify({
                    "status": "success",
                    "message": "Login successful",
                    "user": user.to_dict(),
                    "token": "simulated-jwt-token-xyz" # Asal token api_routes.py mein generate hoga
                }), 200

            # --- WEBSITE RESPONSE (Session) ---
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            
            flash(f"Welcome back, {user.username}!", "success")
            return redirect(url_for('main.dashboard'))
        
        else:
            # Login Failed
            if request.is_json:
                return jsonify({"status": "error", "message": "Invalid credentials"}), 401
            else:
                flash("Invalid email or password", "danger")

    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registration Route for Browser"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role', 'customer')

        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
        else:
            new_user = User(username=username, email=email, role=role)
            new_user.password = password  # Hash automatically set hoga models.py ki wajah se
            db.session.add(new_user)
            db.session.commit()
            flash("Account created! Please login.", "success")
            return redirect(url_for('main.login'))

    return render_template('register.html') # Agent ko register.html banana padega agar nahi hai

# ==========================================
# 2. PROTECTED DASHBOARDS (Role Based)
# ==========================================

@main_bp.route('/dashboard')
def dashboard():
    """Traffic Controller - Sabko unki jagah bhejta hai"""
    if 'user_id' not in session:
        flash("Please login to access dashboard", "warning")
        return redirect(url_for('main.login'))
    
    role = session.get('role')
    username = session.get('username')

    # Logic: Kisko kahan bhejna hai
    if role == 'admin':
        return render_template('dashboard_admin.html', user=username)
    elif role == 'driver':
        return render_template('dashboard_driver.html', user=username)
    elif role == 'restaurant':
        return render_template('dashboard_restaurant.html', user=username)
    else:
        # Customer
        return render_template('customer_home.html', user=username)

# ==========================================
# 3. DUAL-MODE DATA ROUTES (Developer Request #7)
# ==========================================

@main_bp.route('/orders')
def orders():
    """
    Ye route Mobile ko JSON dega aur Website ko HTML dega.
    """
    # Security check
    user_id = session.get('user_id')
    if not user_id and not request.is_json:
        return redirect(url_for('main.login'))

    # Data fetch karo
    my_orders = Order.query.filter_by(customer_id=user_id).all() if user_id else []

    # --- MOBILE APP KO JSON BHEJO ---
    if request.is_json or request.headers.get('Accept') == 'application/json':
        return jsonify({
            "status": "success",
            "count": len(my_orders),
            "orders": [order.to_dict() for order in my_orders]
        })

    # --- BROWSER KO HTML BHEJO ---
    return render_template('orders.html', orders=my_orders)

@main_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for('main.index'))