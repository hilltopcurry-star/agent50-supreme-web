import os
import sys

def connect_pages():
    print("🔗 CONNECTING ALL PAGES (ROUTING FIX)...")
    
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

    # 2. App.js ko overwrite karna (Taake wo nayi files use kare)
    app_js_path = os.path.join(project_path, "frontend", "src", "App.js")
    
    # Ye code saare Links ko sahi jagah jod dega
    router_code = '''
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// Importing Pages
import Login from './Auth/Login'; // Agar ye folder alag hai to adjust karega
import Register from './Auth/Register';
import CustomerDashboard from './pages/CustomerDashboard';
import DriverDashboard from './pages/DriverDashboard';

function App() {
  return (
    <Router>
      <Routes>
        {/* Default Route -> Login */}
        <Route path="/" element={<Navigate to="/login" />} />
        
        {/* Auth Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        {/* Main Dashboards */}
        <Route path="/customer/dashboard" element={<CustomerDashboard />} />
        <Route path="/driver/dashboard" element={<DriverDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
'''
    # File save karna
    with open(app_js_path, "w", encoding="utf-8") as f:
        f.write(router_code)
        
    print("✅ ROUTING FIXED: All pages are now connected.")
    print("👉 Customer Dashboard is at: /customer/dashboard")
    print("👉 Driver Dashboard is at: /driver/dashboard")

if __name__ == "__main__":
    connect_pages()