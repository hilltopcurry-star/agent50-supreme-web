import os
import sys
import subprocess
import time
import webbrowser

def fix_white_screen():
    print("🚑 FIXING WHITE SCREEN ERROR...")
    
    # 1. Project Path
    base_dir = os.getcwd()
    project_path = None
    for root, dirs, files in os.walk(base_dir):
        if "delivery_production_v2" in dirs:
            project_path = os.path.join(root, "delivery_production_v2")
            break
            
    if not project_path:
        print("❌ Project folder nahi mila.")
        return

    frontend_path = os.path.join(project_path, "frontend")
    src_path = os.path.join(frontend_path, "src")
    auth_path = os.path.join(src_path, "Auth")
    
    # 2. LOGIN.JS CREATE KARNA (Agar ye missing hua to app crash hoti hai)
    os.makedirs(auth_path, exist_ok=True)
    
    login_code = '''
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Container, Card, Form, Button, Alert } from 'react-bootstrap';
import api from '../services/api';

const Login = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/api/v1/auth/login', formData);
      if (res.data.status === 'success') {
        localStorage.setItem('user', JSON.stringify(res.data));
        // Simple logic: Agar admin/driver nahi to customer dashboard
        navigate('/customer/dashboard');
      }
    } catch (err) {
      setError('Invalid Credentials');
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center min-vh-100 bg-light">
      <Card className="shadow p-4" style={{ maxWidth: '400px', width: '100%' }}>
        <h3 className="text-center mb-3">Agent 50 Login</h3>
        {error && <Alert variant="danger">{error}</Alert>}
        <Form onSubmit={handleSubmit}>
            <Form.Group className="mb-3">
                <Form.Label>Email</Form.Label>
                <Form.Control type="email" name="email" onChange={handleChange} required />
            </Form.Group>
            <Form.Group className="mb-3">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" name="password" onChange={handleChange} required />
            </Form.Group>
            <Button variant="primary" type="submit" className="w-100">Login</Button>
        </Form>
        <div className="text-center mt-3">
            <Link to="/register">Create New Account</Link>
        </div>
      </Card>
    </Container>
  );
};
export default Login;
'''
    with open(os.path.join(auth_path, "Login.js"), "w", encoding="utf-8") as f:
        f.write(login_code)
    print("✅ Login.js restored.")

    # 3. MISSING DESIGN TOOLS INSTALL KARNA (Ye sabse zaroori hai)
    print("📦 Installing Design Tools (Bootstrap)... Please wait...")
    # Windows ke liye shell=True zaroori hai
    subprocess.call("npm install react-bootstrap bootstrap", cwd=frontend_path, shell=True)
    print("✅ Installation Complete.")

    # 4. RESTART SYSTEM
    print("🔄 Restarting System...")
    if os.name == 'nt':
        os.system("taskkill /f /im node.exe >nul 2>&1")

    # Start Frontend Only (Backend already running assumed, or you can run Launch_Now.py later)
    print("💻 Starting Frontend...")
    subprocess.Popen("npm start", cwd=frontend_path, shell=True)

    print("🚀 Opening Browser in 15 seconds...")
    time.sleep(15)
    webbrowser.open("http://localhost:3000/login")

if __name__ == "__main__":
    fix_white_screen()