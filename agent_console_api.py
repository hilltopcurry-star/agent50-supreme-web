from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sys
import os

# --- 1. ABSOLUTE PATH FIX ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

if not os.path.exists(TEMPLATE_DIR):
    print(f"ERROR: Templates folder nahi mila! Yahan hona chahiye: {TEMPLATE_DIR}")
else:
    print(f"SUCCESS: Templates folder mil gaya: {TEMPLATE_DIR}")

# --- PATH FIX FOR IMPORTS ---
sys.path.append(BASE_DIR)

# Import Core Systems
try:
    from core.agent_identity import get_self_awareness, get_dashboard_data
    from agent_build_runner import submit_build_from_console, get_build_info_for_api, get_build_executor
    SYSTEM_MODE = "REAL"
except ImportError as e:
    print("Running in UI TEST MODE (Mock Data)")
    SYSTEM_MODE = "MOCK"
    class MockObj:
        def get_identity(self): return type('obj', (object,), {'agent_name': 'AGENT 50'})
    def get_self_awareness(): return MockObj()
    def get_build_executor(): return type('obj', (object,), {'storage': type('obj', (object,), {'get_active_builds': lambda: []}), 'get_active_builds_status': lambda: []})
    agent = get_self_awareness()
    executor = get_build_executor()

# --- FLASK SETUP ---
app = Flask(__name__, template_folder=TEMPLATE_DIR)
CORS(app)

# Security
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["1000 per day", "200 per hour"],
    storage_uri="memory://"
)

# Initialize Systems
if SYSTEM_MODE == "REAL":
    agent = get_self_awareness()
    executor = get_build_executor()

# --- AUTH HELPER ---
def check_token():
    token = request.headers.get('Authorization')
    if token != "Bearer SUPREME-ACCESS-TOKEN-786":
        return False
    return True

# --- ROUTES ---
@app.route('/')
def index():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        return f"<h1>Error Loading Dashboard</h1><p>{str(e)}</p><p>Check terminal for path details.</p>"

@app.route('/api/v1/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "mode": SYSTEM_MODE})

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.json
    if data.get("username") == "alimarri" and data.get("password") == "supreme_agent50_2024":
        return jsonify({
            "token": "SUPREME-ACCESS-TOKEN-786",
            "console_title": "IT Engineer ALI MARRI",
            "status": "success"
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/v1/dashboard', methods=['GET'])
def get_dashboard():
    if not check_token(): return jsonify({"error": "Unauthorized"}), 401
    
    if SYSTEM_MODE == "REAL":
        data = get_dashboard_data()
        data["active_builds"] = executor.get_active_builds_status()
        return jsonify(data), 200
    
    return jsonify({
        "active_builds": [],
        "recent_logs": ["System Ready", "Waiting..."]
    }), 200

@app.route('/api/v1/build/submit', methods=['POST'])
def submit_build():
    if not check_token(): return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": "Build command received"}), 200

# --- SERVER START ---
if __name__ == '__main__':
    print("\n-------------------------------------------")
    print("AGENT 50 SUPREME CONSOLE")
    print(f"Templates Path: {TEMPLATE_DIR}")
    print("Open this link in browser: http://localhost:5050")
    print("-------------------------------------------\n")
    app.run(port=5050, debug=True, use_reloader=False)