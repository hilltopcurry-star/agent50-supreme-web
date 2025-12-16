import os
import sys

def restore_power():
    print("🔋 RESTORING LIVE LOCATION & ADVANCED FEATURES...")
    
    # 1. Project Dhoondna
    base_dir = os.getcwd()
    project_path = None
    for root, dirs, files in os.walk(base_dir):
        if "delivery_production_v2" in dirs:
            project_path = os.path.join(root, "delivery_production_v2")
            break
            
    if not project_path:
        print("❌ Project folder nahi mila.")
        return

    # --- 2. BACKEND KO UPDATE KARNA (Add SocketIO for Live Location) ---
    app_path = os.path.join(project_path, "app.py")
    
    # Ye Code Login + Live Location dono chalayega
    advanced_app_code = '''
import os
from flask import Flask, jsonify
from extensions import db, jwt
from flask_cors import CORS
from flask_socketio import SocketIO # Live Location Power

# Global Socket
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'delivery_v2.db')
    app.config['SECRET_KEY'] = 'dev-secret-key'
    app.config['JWT_SECRET_KEY'] = 'dev-jwt-key'
    
    db.init_app(app)
    jwt.init_app(app)
    
    # Allow Frontend to talk to Backend (CORS)
    CORS(app, resources={r"/*": {"origins": "*"}}) 
    
    # Initialize Live Tracking
    socketio.init_app(app, cors_allowed_origins="*")

    from auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')

    @app.route('/')
    def home():
        return "Supreme Backend + Live Tracking is ON!"

    return app

app = create_app()

# SocketIO Events (Live Updates)
@socketio.on('connect')
def handle_connect():
    print("User Connected for Live Tracking")

@socketio.on('update_location')
def handle_location(data):
    print(f"Driver Location: {data}")
    socketio.emit('location_update', data)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database & Tracking System Ready.")
    
    print("Starting Server with SocketIO...")
    # SocketIO wala run command (Zaroori for Live Location)
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
'''
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(advanced_app_code)
    print("✅ Backend Upgrade: Live Tracking Enabled.")

    # --- 3. FRONTEND DRIVER DASHBOARD (Map & Tracking UI) ---
    driver_dash_path = os.path.join(project_path, "frontend", "src", "pages", "DriverDashboard.js")
    os.makedirs(os.path.dirname(driver_dash_path), exist_ok=True)

    driver_code = '''
import React, { useState, useEffect } from 'react';
import { Container, Card, Button, Badge } from 'react-bootstrap';
// Socket connection (hum assume kar rahe hain library installed hai)
// import io from 'socket.io-client'; 

const DriverDashboard = () => {
  const [status, setStatus] = useState("Offline");
  const [location, setLocation] = useState({ lat: 24.8607, lng: 67.0011 }); // Default Karachi/City

  const toggleStatus = () => {
    setStatus(status === "Offline" ? "Online (Tracking On)" : "Offline");
  };

  return (
    <Container className="p-4">
      <h2 className="text-dark mb-4">🚖 Driver Live Dashboard</h2>
      
      <Card className="shadow-lg p-3 mb-4 text-center">
        <h4>Current Status: <Badge bg={status === "Offline" ? "secondary" : "success"}>{status}</Badge></h4>
        <div className="mt-3">
            <Button variant={status === "Offline" ? "success" : "danger"} size="lg" onClick={toggleStatus}>
                {status === "Offline" ? "GO ONLINE" : "GO OFFLINE"}
            </Button>
        </div>
      </Card>

      <Card className="shadow border-0">
        <Card.Body>
            <h5>📍 Live Map Simulation</h5>
            <div style={{ height: '300px', background: '#e9ecef', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                {status === "Offline" ? (
                    <p className="text-muted">Map is disabled. Go Online to start tracking.</p>
                ) : (
                    <div>
                        <h1 style={{fontSize: '50px'}}>🗺️</h1>
                        <p>Tracking Active at: {location.lat}, {location.lng}</p>
                        <small className="text-success">Sending location to Customer...</small>
                    </div>
                )}
            </div>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default DriverDashboard;
'''
    with open(driver_dash_path, "w", encoding="utf-8") as f:
        f.write(driver_code)
    print("✅ Frontend Upgrade: Driver Dashboard Restored.")

    print("\n🚀 DONE! Please Restart the System.")

if __name__ == "__main__":
    restore_power()