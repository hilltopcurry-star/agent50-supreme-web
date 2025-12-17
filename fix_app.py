import os

# Kyunki aap already 'delivery_production_v2' folder mein hain,
# hum seedha 'app.py' ko target karenge.
file_path = "app.py"

# Ye Sahi Wala Code hai (Correct Imports ke sath)
new_app_code = '''
import os
from flask import Flask
from extensions import db, jwt
from flask_cors import CORS
from payment_handler import payment_bp
# ✅ CORRECT IMPORT: socketio_handler se 'socketio' aur 'init_socketio' le rahe hain
from socketio_handler import init_socketio, socketio

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'delivery_v2.db')
    app.config['SECRET_KEY'] = 'dev-secret-key-week2'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-week2'
    app.config['STRIPE_SECRET_KEY'] = 'sk_test_placeholder'
    app.config['STRIPE_WEBHOOK_SECRET'] = 'whsec_placeholder'
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Initialize the REAL SocketIO instance
    init_socketio(app)
    
    app.register_blueprint(payment_bp)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("✅ Database Tables Created for Week 2")
        
    print("🚀 Starting Production Server with Socket.IO...")
    # Run the REAL SocketIO instance
    socketio.run(app, debug=True, port=5000)
'''

# File ko overwrite karen
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_app_code)

print("✅ FIXED: app.py has been updated successfully!")