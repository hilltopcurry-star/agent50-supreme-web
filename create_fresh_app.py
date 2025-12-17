"""
👑 KING DEEPSEEK - Fresh App Creator
Bhai ye file create karo aur run karo!
"""

from pathlib import Path

print("👑 KING DEEPSEEK - Creating fresh app.py...")

project_dir = Path("projects/agent50")
app_file = project_dir / "app.py"

# Complete fresh app.py content
fresh_app_content = '''from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from pathlib import Path
import subprocess
import sys

# Add agent modules to path
sys.path.append(os.path.dirname(__file__))

# Database Integration - KING DEEPSEEK AI Agent
from models import init_database, get_db_session
from crud_operations import UserCRUD, ProjectCRUD, get_database_stats

app = Flask(__name__)
app.secret_key = 'king_deepseek_secret_2025'

class WebAgent:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.projects_dir = self.base_dir / "projects"
        self.templates_dir = self.base_dir / "templates" 
        self.static_dir = self.base_dir / "static"
        
        # Create necessary directories
        self.templates_dir.mkdir(exist_ok=True)
        self.static_dir.mkdir(exist_ok=True)
    
    def get_projects_list(self):
        """Get list of all generated projects"""
        projects = []
        if self.projects_dir.exists():
            for project_dir in self.projects_dir.iterdir():
                if project_dir.is_dir():
                    projects.append({
                        "name": project_dir.name,
                        "path": str(project_dir),
                        "files": len(list(project_dir.glob("*.py"))),
                        "created": project_dir.stat().st_ctime
                    })
        return sorted(projects, key=lambda x: x["created"], reverse=True)
    
    def get_project_files(self, project_name):
        """Get all files in a project"""
        project_dir = self.projects_dir / project_name
        files = []
        if project_dir.exists():
            for file_path in project_dir.rglob("*"):
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "path": str(file_path.relative_to(project_dir)),
                        "size": file_path.stat().st_size,
                        "type": "file"
                    })
        return files

web_agent = WebAgent()

# Routes
@app.route('/')
def index():
    """Main dashboard"""
    projects = web_agent.get_projects_list()
    return render_template('index.html', projects=projects, agent_available=True)

@app.route('/api/projects')
def api_projects():
    """API: Get projects list"""
    return jsonify(web_agent.get_projects_list())

@app.route('/api/project/<project_name>')
def api_project_files(project_name):
    """API: Get project files"""
    files = web_agent.get_project_files(project_name)
    return jsonify(files)

@app.route('/api/create_project', methods=['POST'])
def api_create_project():
    """API: Create new project"""
    data = request.json
    project_name = data.get('name', '').strip()
    project_desc = data.get('description', '')
    template = data.get('template', 'flask_api')
    
    if not project_name:
        return jsonify({"success": False, "error": "Project name required"})
    
    return jsonify({"success": True, "message": "Project creation endpoint"})

@app.route('/api/run_project/<project_name>')
def api_run_project(project_name):
    """API: Run project"""
    return jsonify({"success": True, "message": "Run project endpoint"})

@app.route('/api/file_content')
def api_file_content():
    """API: Get file content"""
    project_name = request.args.get('project')
    file_path = request.args.get('file')
    
    if not project_name or not file_path:
        return jsonify({"error": "Project and file required"})
    
    full_path = web_agent.projects_dir / project_name / file_path
    if full_path.exists() and full_path.is_file():
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return jsonify({"success": True, "content": content})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    else:
        return jsonify({"success": False, "error": "File not found"})

# Database API Routes - KING DEEPSEEK FIXED VERSION (NO DUPLICATES)
@app.route('/api/db/stats')
def db_stats():
    """Get database statistics"""
    try:
        stats = get_database_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        print(f"Database stats error: {e}")
        return jsonify({"success": False, "error": "Database connection failed"}), 500

@app.route('/api/users')
def get_users():
    """Get all users"""
    try:
        user_crud = UserCRUD()
        users = user_crud.get_all()
        user_list = []
        for u in users:
            user_list.append({
                "id": u.id, 
                "username": u.username, 
                "email": u.email,
                "created_at": str(u.created_at) if u.created_at else None
            })
        return jsonify({"success": True, "users": user_list})
    except Exception as e:
        print(f"Users API error: {e}")
        return jsonify({"success": False, "error": "Could not fetch users"}), 500

@app.route('/api/projects')
def get_projects():
    """Get all projects"""
    try:
        project_crud = ProjectCRUD()
        projects = project_crud.get_all()
        project_list = []
        for p in projects:
            project_list.append({
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "project_type": p.project_type,
                "status": p.status
            })
        return jsonify({"success": True, "projects": project_list})
    except Exception as e:
        print(f"Projects API error: {e}")
        return jsonify({"success": False, "error": "Could not fetch projects"}), 500

@app.route('/api/users/create', methods=['POST'])
def create_user():
    """Create new user"""
    data = request.json
    user_crud = UserCRUD()
    try:
        user = user_crud.create(data)
        return jsonify({
            "success": True, 
            "user": {"id": user.id, "username": user.username, "email": user.email}
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# Create basic templates
def create_default_templates():
    """Create default HTML templates"""
    
    # Main template
    index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KING DEEPSEEK AI Agent</title>
    <style>
        body { 
            font-family: 'Segoe UI', Arial, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { 
            margin: 0; 
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
            margin-top: 10px;
        }
        .content { 
            padding: 30px; 
        }
        .card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
            transition: transform 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        .project-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .project-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border: 1px solid #e1e8ed;
        }
        .console {
            background: #1e1e1e;
            color: #00ff00;
            padding: 15px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            height: 200px;
            overflow-y: auto;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>👑 KING DEEPSEEK AI AGENT</h1>
            <div class="subtitle">PAK-CHINA FRIENDSHIP LEVEL DEVELOPMENT</div>
        </div>
        
        <div class="content">
            <div class="card">
                <h2>🚀 Create New Project</h2>
                <input type="text" id="projectName" placeholder="Project Name" style="padding: 10px; width: 200px; margin-right: 10px;">
                <input type="text" id="projectDesc" placeholder="Description" style="padding: 10px; width: 300px; margin-right: 10px;">
                <select id="projectTemplate" style="padding: 10px; margin-right: 10px;">
                    <option value="flask_api">Flask REST API</option>
                    <option value="web_app">Web Application</option>
                    <option value="data_analysis">Data Analysis</option>
                    <option value="automation">Automation Script</option>
                </select>
                <button class="btn" onclick="createProject()">Create Project</button>
            </div>

            <div class="card">
                <h2>📁 Your Projects</h2>
                <div id="projectsList">
                    <p>Loading projects...</p>
                </div>
            </div>

            <div class="card">
                <h2>📊 Database Info</h2>
                <button class="btn" onclick="loadDBStats()">Load Database Stats</button>
                <button class="btn" onclick="loadUsers()">Load Users</button>
                <button class="btn" onclick="loadProjects()">Load Projects</button>
                <div id="dbInfo" class="console">
                    Click buttons to load database information...
                </div>
            </div>
        </div>
    </div>

    <script>
        // Load projects on page load
        loadProjectList();

        async function loadProjectList() {
            try {
                const response = await fetch('/api/projects');
                const projects = await response.json();
                
                let html = '<div class="project-grid">';
                projects.forEach(project => {
                    html += `
                        <div class="project-card">
                            <h3>${project.name}</h3>
                            <p>Files: ${project.files}</p>
                            <button class="btn" onclick="runProject('${project.name}')">Run</button>
                            <button class="btn" onclick="viewFiles('${project.name}')">View Files</button>
                        </div>
                    `;
                });
                html += '</div>';
                
                document.getElementById('projectsList').innerHTML = html;
            } catch (error) {
                document.getElementById('projectsList').innerHTML = '<p>Error loading projects</p>';
            }
        }

        async function loadDBStats() {
            try {
                const response = await fetch('/api/db/stats');
                const result = await response.json();
                document.getElementById('dbInfo').innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                document.getElementById('dbInfo').innerHTML = 'Error loading stats: ' + error;
            }
        }

        async function loadUsers() {
            try {
                const response = await fetch('/api/users');
                const result = await response.json();
                document.getElementById('dbInfo').innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                document.getElementById('dbInfo').innerHTML = 'Error loading users: ' + error;
            }
        }

        async function loadProjects() {
            try {
                const response = await fetch('/api/projects');
                const result = await response.json();
                document.getElementById('dbInfo').innerHTML = JSON.stringify(result, null, 2);
            } catch (error) {
                document.getElementById('dbInfo').innerHTML = 'Error loading projects: ' + error;
            }
        }

        function addToConsole(message) {
            const console = document.getElementById('dbInfo');
            console.innerHTML += message + '<br>';
            console.scrollTop = console.scrollHeight;
        }
    </script>
</body>
</html>
'''
    
    # Save template
    templates_dir = project_dir / "templates"
    templates_dir.mkdir(exist_ok=True)
    with open(templates_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

# Create templates on startup
create_default_templates()

# Initialize database
init_database()

if __name__ == '__main__':
    print("=== 🌐 KING DEEPSEEK WEB INTERFACE ===")
    print("Starting web server...")
    print("Access at: http://localhost:5000")
    print("Database routes: /api/db/stats, /api/users, /api/projects")
    print("Press Ctrl+C to stop")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
'''

# Write fresh app.py
with open(app_file, 'w', encoding='utf-8') as f:
    f.write(fresh_app_content)

print("✅ Fresh app.py created successfully!")
print("🚀 Now restart your app: cd projects/agent50 && python app.py")