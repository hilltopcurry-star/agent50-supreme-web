import os
import sys
import subprocess
import time
import webbrowser

# --- SUPREME DEVELOPER PATCH (NO EMOJIS, PURE LOGIC) ---

def write_file(path, content):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Fixed: {os.path.basename(path)}")
    except Exception as e:
        print(f"[ERROR] Could not write {path}: {e}")

def main():
    print("\n--- INSTALLING DEVELOPER CODES ---\n")

    # 1. Project Location Trace
    base_dir = os.getcwd()
    project_path = None
    for root, dirs, files in os.walk(base_dir):
        if "delivery_production_v2" in dirs:
            project_path = os.path.join(root, "delivery_production_v2")
            break
            
    if not project_path:
        print("Error: Project folder not found.")
        return

    # 2. OVERWRITE BACKEND (app.py) - 100% CLEAN
    app_code = '''
import os
from flask import Flask, jsonify
from extensions import db, jwt
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'delivery_v2.db')
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['JWT_SECRET_KEY'] = 'dev-jwt-key'
    
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    from auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    @app.route('/')
    def home():
        return "Backend is Running Successfully."

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database Connected.")
    print("Server Starting on Port 5000...")
    app.run(debug=True, port=5000)
'''
    write_file(os.path.join(project_path, "app.py"), app_code)

    # 3. OVERWRITE AUTH (auth.py) - 100% CLEAN
    auth_code = '''
from flask import Blueprint, request, jsonify
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400
            
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"error": "Email already exists"}), 400
            
        new_user = User(
            username=data.get('username', 'User'),
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data.get('role', 'customer')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success", "message": "User created"}), 201
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Server Error"}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password_hash, data.get('password')):
        return jsonify({"status": "success", "user": user.username}), 200
    return jsonify({"error": "Invalid credentials"}), 401
'''
    write_file(os.path.join(project_path, "auth.py"), auth_code)

    # 4. OVERWRITE FRONTEND API (api.js)
    api_js_code = '''
import axios from 'axios';
const api = axios.create({
  baseURL: 'http://127.0.0.1:5000',
  headers: { 'Content-Type': 'application/json' }
});
export default api;
'''
    write_file(os.path.join(project_path, "frontend", "src", "services", "api.js"), api_js_code)

    # 5. KILL OLD PROCESSES
    if os.name == 'nt':
        os.system("taskkill /f /im python.exe >nul 2>&1")
        os.system("taskkill /f /im node.exe >nul 2>&1")

    # 6. START SYSTEM
    print("Starting Backend...")
    subprocess.Popen([sys.executable, "app.py"], cwd=project_path, shell=True)
    time.sleep(3)

    print("Starting Frontend...")
    subprocess.Popen("npm start", cwd=os.path.join(project_path, "frontend"), shell=True)

    print("Opening Browser...")
    time.sleep(8)
    webbrowser.open("http://localhost:3000/register")

if __name__ == "__main__":
    main()