import os
import sys

def fix_structure():
    print("🏗️ FIXING FOLDER STRUCTURE & MISSING FILES...")
    
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

    # Paths define kar rahe hain
    src_path = os.path.join(project_path, "frontend", "src")
    pages_dir = os.path.join(src_path, "pages")
    auth_dir = os.path.join(src_path, "Auth")

    # 2. Folders Create karna (Forcefully)
    os.makedirs(pages_dir, exist_ok=True)
    os.makedirs(auth_dir, exist_ok=True)
    print(f"✅ Folders Verified: {pages_dir}")

    # 3. Customer Dashboard File Create (SUPREME VERSION)
    customer_code = '''
import React from 'react';
import { Container, Row, Col, Card, Button, Table, Badge } from 'react-bootstrap';

const CustomerDashboard = () => {
  return (
    <Container fluid className="p-4 bg-light min-vh-100">
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div><h2 className="fw-bold text-dark">Supreme Dashboard</h2><p className="text-muted">Welcome back, Boss!</p></div>
        <Button variant="success" size="lg">+ Create New Order</Button>
      </div>
      <Row className="mb-4">
        <Col md={3}><Card className="text-white bg-primary shadow border-0"><Card.Body><h3>150</h3><h6>Total Orders</h6></Card.Body></Card></Col>
        <Col md={3}><Card className="text-white bg-success shadow border-0"><Card.Body><h3>$5,400</h3><h6>Total Revenue</h6></Card.Body></Card></Col>
        <Col md={3}><Card className="text-white bg-warning shadow border-0"><Card.Body><h3>12</h3><h6>Pending Delivery</h6></Card.Body></Card></Col>
        <Col md={3}><Card className="text-white bg-danger shadow border-0"><Card.Body><h3>5</h3><h6>Cancelled</h6></Card.Body></Card></Col>
      </Row>
      <Card className="shadow-sm border-0">
        <Card.Header className="bg-white py-3"><h5 className="mb-0 fw-bold">Recent Orders</h5></Card.Header>
        <Card.Body>
            <Table hover responsive>
                <thead className="bg-light"><tr><th>Order ID</th><th>Item</th><th>Status</th><th>Price</th><th>Actions</th></tr></thead>
                <tbody>
                    <tr><td>#ORD-001</td><td>Spicy Burger</td><td><Badge bg="warning">Cooking</Badge></td><td>$15.00</td><td><Button variant="outline-primary" size="sm">Edit</Button></td></tr>
                    <tr><td>#ORD-002</td><td>Pizza Large</td><td><Badge bg="info">On Way</Badge></td><td>$25.00</td><td><Button variant="outline-primary" size="sm">Edit</Button></td></tr>
                </tbody>
            </Table>
        </Card.Body>
      </Card>
    </Container>
  );
};
export default CustomerDashboard;
'''
    with open(os.path.join(pages_dir, "CustomerDashboard.js"), "w", encoding="utf-8") as f:
        f.write(customer_code)
    print("✅ CustomerDashboard.js restored.")

    # 4. Driver Dashboard File Create
    driver_code = '''
import React, { useState } from 'react';
import { Container, Card, Button, Badge } from 'react-bootstrap';

const DriverDashboard = () => {
  const [status, setStatus] = useState("Offline");
  return (
    <Container className="p-4">
      <h2 className="text-dark mb-4">🚖 Driver Live Dashboard</h2>
      <Card className="shadow-lg p-3 mb-4 text-center">
        <h4>Current Status: <Badge bg={status === "Offline" ? "secondary" : "success"}>{status}</Badge></h4>
        <div className="mt-3">
            <Button variant={status === "Offline" ? "success" : "danger"} size="lg" onClick={() => setStatus(status === "Offline" ? "Online" : "Offline")}>
                {status === "Offline" ? "GO ONLINE" : "GO OFFLINE"}
            </Button>
        </div>
      </Card>
      <Card className="shadow border-0"><Card.Body><h5>📍 Live Map Simulation</h5><div style={{ height: '300px', background: '#e9ecef', display: 'flex', alignItems: 'center', justifyContent: 'center' }}><h1>🗺️</h1></div></Card.Body></Card>
    </Container>
  );
};
export default DriverDashboard;
'''
    with open(os.path.join(pages_dir, "DriverDashboard.js"), "w", encoding="utf-8") as f:
        f.write(driver_code)
    print("✅ DriverDashboard.js restored.")

    # 5. Fix App.js Import Paths
    app_code = '''
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

// Importing from correct folders
import Login from './Auth/Login';
import Register from './Auth/Register';
// Ye hain wo files jo missing thin
import CustomerDashboard from './pages/CustomerDashboard';
import DriverDashboard from './pages/DriverDashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/customer/dashboard" element={<CustomerDashboard />} />
        <Route path="/driver/dashboard" element={<DriverDashboard />} />
      </Routes>
    </Router>
  );
}
export default App;
'''
    with open(os.path.join(src_path, "App.js"), "w", encoding="utf-8") as f:
        f.write(app_code)
    print("✅ App.js Fixed (Paths corrected).")

    print("\n🚀 ALL FIXED. Restarting System...")
    
if __name__ == "__main__":
    fix_structure()