import os
from flask import Flask, render_template
from flask_cors import CORS
from extensions import db, jwt  # Import extensions
from models import User

# Import Blueprints
# Note: You might need to adjust import based on where api_routes.py is located
try:
    from api_routes import api_bp
except ImportError:
    print("Warning: api_routes not found yet")
    api_bp = None

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'final_db.sqlite')
    app.config['SECRET_KEY'] = 'final-secret-key'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-key-agent50'  # NEW: For Mobile Security

    # Initialize Plugins
    db.init_app(app)
    jwt.init_app(app)  # Initialize JWT
    CORS(app)

    # Register Blueprints
    if api_bp:
        app.register_blueprint(api_bp)

    # Web Routes (Legacy)
    @app.route('/')
    def home():
        return render_template('login.html')

    @app.route('/customer/home')
    def customer_home():
        return render_template('customer/home.html')

    @app.route('/restaurant/dashboard')
    def restaurant_dashboard():
        return render_template('restaurant/dashboard.html')

    @app.route('/driver/dashboard')
    def driver_dashboard():
        return render_template('driver/dashboard.html')

    return app

# Entry Point
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create Admin User if not exists
        if not User.query.filter_by(email='admin@example.com').first():
            print("⚡ Creating Test Users...")
            admin = User(username='admin', email='admin@example.com', role='restaurant')
            admin.set_password('123456')
            
            driver = User(username='driver', email='driver@example.com', role='driver')
            driver.set_password('123456')
            
            customer = User(username='customer', email='customer@example.com', role='customer')
            customer.set_password('123456')
            
            db.session.add_all([admin, driver, customer])
            db.session.commit()
            
    print("🏆 AGENT 50 UPGRADED APP ONLINE: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)