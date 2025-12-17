import os
import sys
from pathlib import Path

# ==========================================
# AGENT 50 SUPREME - CLOUD INSTALLER
# ==========================================

BASE_DIR = Path("agent50-supreme-cloud")

print("🚀 AGENT 50: Starting Cloud Structure Generation...")
print("==================================================")

# 1. CREATE DIRECTORIES
directories = [
    "backend/agent",
    "backend/api",
    "frontend/public",
    "frontend/src/api",
    "frontend/src/components",
    "frontend/src/hooks",
    "frontend/src/pages",
    "frontend/src/store",
    "frontend/src/styles",
    "frontend/src/types",
    "frontend/src/utils",
    "nginx"
]

for dir_path in directories:
    full_path = BASE_DIR / dir_path
    full_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created Folder: {full_path}")

# ==========================================
# 2. WRITE FILES (The Supreme Codes)
# ==========================================

# FILE 1: backend/app.py
f1_content = r'''"""
AGENT 50 SUPREME - Production Cloud Flask Application
Optimized for Railway, Render, Vercel with Gunicorn
"""
import os
import sys
from pathlib import Path
from datetime import datetime
import secrets

# Add agent module to path
sys.path.insert(0, str(Path(__file__).parent / "agent"))

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import jwt

# ========== PRODUCTION CONFIGURATION ==========
class ProductionConfig:
    """Cloud-optimized production configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))
    JWT_SECRET = os.environ.get('JWT_SECRET', secrets.token_hex(32))
    JWT_ALGORITHM = 'HS256'
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    API_PREFIX = '/api/v1'
    RATE_LIMIT = os.environ.get('RATE_LIMIT', '200/hour;50/minute')
    AGENT_NAME = 'Agent 50 Supreme'
    AGENT_VERSION = '3.0.0'
    CONSOLE_TITLE = 'AI & IT Specialist Engineer — ALI MARRI'
    PORT = int(os.environ.get('PORT', 5000))
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'info')
    DATA_DIR = Path(os.environ.get('DATA_DIR', '/data/agent50'))
    LOGS_DIR = DATA_DIR / 'logs'
    
    @classmethod
    def ensure_dirs(cls):
        cls.DATA_DIR.mkdir(exist_ok=True, parents=True)
        cls.LOGS_DIR.mkdir(exist_ok=True, parents=True)

# ========== APPLICATION FACTORY ==========
def create_app():
    ProductionConfig.ensure_dirs()
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    
    if ProductionConfig.ENVIRONMENT == 'production':
        CORS(app, supports_credentials=True, origins=ProductionConfig.CORS_ORIGINS)
    else:
        CORS(app, supports_credentials=True)
    
    csp = {
        'default-src': ["'self'"],
        'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        'font-src': ["'self'", "https://fonts.gstatic.com"],
        'script-src': ["'self'", "'unsafe-inline'"],
        'img-src': ["'self'", "data:", "https:"],
        'connect-src': ["'self'", "ws:", "wss:"]
    }
    
    Talisman(app, content_security_policy=csp, force_https=ProductionConfig.ENVIRONMENT == 'production', session_cookie_secure=ProductionConfig.ENVIRONMENT == 'production', frame_options='DENY')
    
    limiter = Limiter(key_func=get_remote_address, app=app, default_limits=[ProductionConfig.RATE_LIMIT], storage_uri="memory://", strategy="fixed-window", enabled=ProductionConfig.ENVIRONMENT == 'production')
    
    @app.route('/')
    def root():
        return jsonify({'status': 'online', 'service': ProductionConfig.AGENT_NAME, 'version': ProductionConfig.AGENT_VERSION, 'environment': ProductionConfig.ENVIRONMENT, 'timestamp': datetime.utcnow().isoformat()})
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

    # Auth API
    @app.route(f'{ProductionConfig.API_PREFIX}/auth/login', methods=['POST'])
    @limiter.limit("10/minute")
    def login():
        try:
            data = request.get_json()
            if not data: return jsonify({'error': 'No data provided'}), 400
            
            admin_user = os.environ.get('AGENT50_ADMIN_USER', 'alimarri')
            admin_pass = os.environ.get('AGENT50_ADMIN_PASS', 'supreme_agent50_2024')
            
            if data.get('username') == admin_user and data.get('password') == admin_pass:
                token = jwt.encode({'user_id': 1, 'username': admin_user, 'role': 'admin', 'exp': datetime.utcnow().timestamp() + (24 * 3600)}, ProductionConfig.JWT_SECRET, algorithm=ProductionConfig.JWT_ALGORITHM)
                return jsonify({'status': 'success', 'token': token, 'user': {'username': admin_user, 'full_name': 'ALI MARRI'}, 'agent_name': ProductionConfig.AGENT_NAME})
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
        except Exception as e: return jsonify({'error': str(e)}), 500

    return app

app = create_app()

if __name__ == '__main__':
    from waitress import serve
    print(f"\n🚀 Starting development server on port {ProductionConfig.PORT}")
    serve(app, host='0.0.0.0', port=ProductionConfig.PORT)
'''

# FILE 2: backend/requirements.txt
f2_content = """Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
gunicorn==21.2.0
gevent==23.9.1
waitress==2.1.2
Flask-CORS==4.0.0
Flask-Limiter==3.5.1
Flask-Talisman==1.1.0
PyJWT==2.8.0
python-dotenv==1.0.0
requests==2.31.0
python-dateutil==2.8.2
colorama==0.4.6
numpy==1.24.4
pandas==2.1.4
"""

# FILE 3: backend/gunicorn.conf.py
f3_content = r'''import os
import multiprocessing
bind = f"0.0.0.0:{os.environ.get('PORT', 5000)}"
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'gevent'
timeout = 120
accesslog = '-'
errorlog = '-'
loglevel = 'info'
'''

# FILE 4: backend/Procfile
f4_content = "web: gunicorn --config gunicorn.conf.py app:app"

# FILE 5: backend/Dockerfile
f5_content = r'''FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN apt-get update && apt-get install -y gcc g++ build-essential curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
COPY . .
RUN mkdir -p /data/agent50 && chown -R 1000:1000 /data/agent50 && chmod -R 755 /data/agent50
RUN useradd -m -u 1000 agent50 && chown -R agent50:agent50 /app /data/agent50
USER agent50
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 CMD curl -f http://localhost:5000/health || exit 1
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]
'''

# FILE 6: backend/railway.toml
f6_content = r'''[build]
builder = "nixpacks"
watchPatterns = ["backend/**", "requirements.txt"]
[deploy]
startCommand = "gunicorn --config gunicorn.conf.py app:app"
healthcheckPath = "/health"
[variables]
PORT = "5000"
ENVIRONMENT = "production"
AGENT50_ADMIN_USER = "alimarri"
[mounts]
source = "agent50-data"
destination = "/data/agent50"
'''

# FILE 8: frontend/vite.config.ts
f8_content = r'''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';
import { loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');
  const apiUrl = env.VITE_API_URL || (mode === 'production' ? 'https://agent50-backend.onrender.com' : 'http://localhost:5000');
  
  return {
    plugins: [react()],
    resolve: { alias: { '@': path.resolve(__dirname, './src') } },
    server: {
      port: 5173,
      host: true,
      proxy: { '/api': { target: apiUrl, changeOrigin: true, rewrite: (path) => path.replace(/^\/api/, '') } }
    },
    build: { outDir: 'dist', minify: 'terser' },
    define: { __APP_ENV__: JSON.stringify(env.APP_ENV), __API_URL__: JSON.stringify(apiUrl) }
  };
});
'''

# FILE 9: frontend/src/utils/apiClient.ts
f9_content = r'''import axios from 'axios';
const getApiUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  const isProduction = window.location.hostname !== 'localhost';
  return isProduction ? 'https://agent50-backend.onrender.com' : 'http://localhost:5000';
};
const apiClient = axios.create({
  baseURL: getApiUrl() + '/api/v1',
  headers: { 'Content-Type': 'application/json', 'X-Client': 'Agent50-Web-Console' }
});
export { apiClient };
'''

# FILE 10: frontend/vercel.json
f10_content = r'''{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "vite",
  "rewrites": [
    { "source": "/api/(.*)", "destination": "https://agent50-backend.onrender.com/api/$1" },
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
'''

# FILE 11: frontend/tailwind.config.js
f11_content = r'''/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: { 500: '#0ea5e9', 600: '#0284c7' },
        cyber: { 500: '#3b82f6', 600: '#2563eb' },
      },
      animation: {
        'glass-glow': 'glassGlow 3s ease-in-out infinite',
        'neon-flicker': 'neonFlicker 1.5s infinite',
      }
    },
  },
  plugins: [],
}
'''

# FILE 12: frontend/src/styles/globals.css
f12_content = r'''@tailwind base;
@tailwind components;
@tailwind utilities;

body {
    @apply h-full bg-gray-950 text-gray-100 antialiased;
    background-image: radial-gradient(circle at 15% 50%, rgba(14, 165, 233, 0.05), transparent 55%);
}
.glass-card {
    @apply relative overflow-hidden rounded-2xl border border-gray-800/50;
    background: linear-gradient(135deg, rgba(31, 41, 55, 0.7), rgba(17, 24, 39, 0.5));
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}
.neon-text { text-shadow: 0 0 10px currentColor; }
'''

# FILE 14: docker-compose.yml
f14_content = r'''version: '3.8'
services:
  backend:
    build: { context: ./backend, dockerfile: Dockerfile }
    ports: ["5000:5000"]
    environment:
      - ENVIRONMENT=production
      - AGENT50_ADMIN_USER=alimarri
      - CORS_ORIGINS=http://localhost:5173,http://localhost:3000
    volumes: ["agent_data:/data/agent50"]
  frontend:
    build: { context: ./frontend, dockerfile: Dockerfile }
    ports: ["80:80"]
    depends_on: ["backend"]
volumes: { agent_data: }
'''

# FILE 16: README.md
f16_content = r'''# 🚀 Agent 50 Supreme Cloud
## Production-Ready Deployment
1. **Railway:** Upload `backend` folder.
2. **Vercel:** Upload `frontend` folder.
Created by ALI MARRI
'''

# DICTIONARY MAPPING FILES TO CONTENT
files_to_create = {
    "backend/app.py": f1_content,
    "backend/requirements.txt": f2_content,
    "backend/gunicorn.conf.py": f3_content,
    "backend/Procfile": f4_content,
    "backend/Dockerfile": f5_content,
    "backend/railway.toml": f6_content,
    "frontend/vite.config.ts": f8_content,
    "frontend/src/utils/apiClient.ts": f9_content,
    "frontend/vercel.json": f10_content,
    "frontend/tailwind.config.js": f11_content,
    "frontend/src/styles/globals.css": f12_content,
    "docker-compose.yml": f14_content,
    "README.md": f16_content,
    "frontend/index.html": "<!DOCTYPE html><html lang='en'><head><title>Agent 50 Supreme</title></head><body><div id='root'></div><script type='module' src='/src/main.tsx'></script></body></html>",
    "frontend/package.json": '{"name":"agent50-cloud","version":"3.0.0","type":"module","scripts":{"dev":"vite","build":"vite build"},"dependencies":{"react":"^18.2.0","react-dom":"^18.2.0","framer-motion":"^10.16.4","axios":"^1.6.2"},"devDependencies":{"vite":"^4.4.5","tailwindcss":"^3.3.3","typescript":"^5.0.2"}}'
}

# 3. EXECUTE WRITING
for path, content in files_to_create.items():
    full_path = BASE_DIR / path
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Generated: {path}")

print("\n==================================================")
print("✅ SUCCESS! 'agent50-supreme-cloud' folder is READY.")
print("👉 Next Step: Copy your OLD 'agent 50' core files into 'agent50-supreme-cloud/backend/agent/'")
print("==================================================")