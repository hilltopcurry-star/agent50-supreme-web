# load_balancer.py
from flask import Flask, request, jsonify
import requests
import threading
import time
from collections import deque
import logging

class LoadBalancer:
    def __init__(self):
        self.app = Flask(__name__)
        self.backend_servers = [
            "http://localhost:5001",
            "http://localhost:5002", 
            "http://localhost:5003"
        ]
        self.server_health = {server: True for server in self.backend_servers}
        self.request_count = {server: 0 for server in self.backend_servers}
        self.server_weights = {server: 1 for server in self.backend_servers}
        self.health_check_interval = 30  # seconds
        self.setup_routes()
        self.start_health_checks()
    
    def setup_routes(self):
        @self.app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def proxy(path):
            """Proxy requests to backend servers"""
            server = self.select_server()
            if not server:
                return jsonify({'error': 'No healthy servers available'}), 503
            
            try:
                # Forward request to selected server
                target_url = f"{server}/{path}"
                response = requests.request(
                    method=request.method,
                    url=target_url,
                    headers={key: value for key, value in request.headers if key != 'Host'},
                    data=request.get_data(),
                    cookies=request.cookies,
                    allow_redirects=False,
                    timeout=30
                )
                
                # Return response from backend
                return (response.content, response.status_code, response.headers.items())
            
            except requests.exceptions.RequestException as e:
                # Mark server as unhealthy
                self.server_health[server] = False
                logging.error(f"Server {server} failed: {e}")
                
                # Try another server
                return self.proxy(path)
        
        @self.app.route('/lb/health')
        def load_balancer_health():
            """Load balancer health endpoint"""
            return jsonify({
                'status': 'healthy',
                'healthy_servers': sum(self.server_health.values()),
                'total_servers': len(self.backend_servers),
                'server_status': self.server_health
            })
    
    def select_server(self):
        """Select server using weighted round-robin algorithm"""
        healthy_servers = [s for s in self.backend_servers if self.server_health[s]]
        if not healthy_servers:
            return None
        
        # Weighted round-robin selection
        total_weight = sum(self.server_weights[s] for s in healthy_servers)
        selection = self.request_count[healthy_servers[0]] % total_weight
        
        current = 0
        for server in healthy_servers:
            current += self.server_weights[server]
            if selection < current:
                self.request_count[server] += 1
                return server
        
        return healthy_servers[0]
    
    def health_check(self):
        """Perform health checks on backend servers"""
        for server in self.backend_servers:
            try:
                response = requests.get(f"{server}/api/advanced/features", timeout=5)
                self.server_health[server] = response.status_code == 200
                
                # Adjust weights based on response time
                if response.elapsed.total_seconds() > 2:
                    self.server_weights[server] = max(0.5, self.server_weights[server] - 0.1)
                else:
                    self.server_weights[server] = min(2.0, self.server_weights[server] + 0.1)
                    
            except requests.exceptions.RequestException:
                self.server_health[server] = False
                self.server_weights[server] = max(0.1, self.server_weights[server] - 0.2)
    
    def start_health_checks(self):
        """Start background health check thread"""
        def health_check_loop():
            while True:
                self.health_check()
                time.sleep(self.health_check_interval)
        
        thread = threading.Thread(target=health_check_loop, daemon=True)
        thread.start()
    
    def run(self, host='0.0.0.0', port=80):
        print(f"🚀 Load Balancer running on http://{host}:{port}")
        self.app.run(host=host, port=port, threaded=True)

# Multiple backend servers setup
def create_backend_server(port):
    """Create multiple backend server instances"""
    from web_interface_advanced import AdvancedWebInterface
    
    app = AdvancedWebInterface()
    app.app.config['SERVER_PORT'] = port
    return app

def start_backend_servers():
    """Start multiple backend servers for load testing"""
    servers = []
    for port in [5001, 5002, 5003]:
        server = create_backend_server(port)
        thread = threading.Thread(
            target=server.app.run,
            kwargs={'host': '0.0.0.0', 'port': port, 'debug': False, 'threaded': True},
            daemon=True
        )
        thread.start()
        servers.append(server)
        print(f"✅ Backend server started on port {port}")
    
    return servers