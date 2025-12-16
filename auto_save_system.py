"""
AGENT 50 - AUTO SAVE SYSTEM
خودکار فائل سیونگ اور مینجمنٹ سسٹم
"""

from pathlib import Path
import json
from datetime import datetime

ROOT = Path(__file__).resolve().parent
PROJECTS_DIR = ROOT / "projects"

def ensure_project_folder(project_name: str):
    """پروجیکٹ فولڈر بنائیں اگر موجود نہ ہو"""
    folder = PROJECTS_DIR / project_name
    folder.mkdir(parents=True, exist_ok=True)
    return folder

def save_file(project_name: str, relative_path: str, content: str, encoding="utf-8"):
    """کسی بھی فائل کو سیو کریں"""
    root = ensure_project_folder(project_name)
    file_path = root / relative_path
    
    # ڈائریکٹری بنائیں اگر موجود نہ ہو
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # فائل لکھیں
    file_path.write_text(content, encoding=encoding)
    
    # لاگ بنائیں
    log_save_operation(project_name, relative_path, len(content))
    
    return str(file_path)

def list_project_files(project_name: str):
    """پروجیکٹ کی تمام فائلوں کی فہرست دیں"""
    folder = PROJECTS_DIR / project_name
    if not folder.exists():
        return []
    
    files = []
    for file_path in folder.rglob("*"):
        if file_path.is_file():
            relative_path = str(file_path.relative_to(folder))
            file_info = {
                'path': relative_path,
                'size': file_path.stat().st_size,
                'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
            files.append(file_info)
    
    return files

def read_file(project_name: str, relative_path: str, encoding="utf-8"):
    """فائل پڑھیں"""
    folder = PROJECTS_DIR / project_name
    file_path = folder / relative_path
    
    if not file_path.exists():
        return None
    
    return file_path.read_text(encoding=encoding)

def delete_file(project_name: str, relative_path: str):
    """فائل ڈیلیٹ کریں"""
    folder = PROJECTS_DIR / project_name
    file_path = folder / relative_path
    
    if file_path.exists():
        file_path.unlink()
        return True
    return False

def get_project_stats(project_name: str):
    """پروجیکٹ کے اعداد و شمار دیں"""
    files = list_project_files(project_name)
    total_size = sum(f['size'] for f in files)
    
    return {
        'project_name': project_name,
        'total_files': len(files),
        'total_size_bytes': total_size,
        'files': files
    }

def log_save_operation(project_name: str, file_path: str, content_length: int):
    """فائل سیو آپریشن لاگ کریں"""
    log_file = ROOT / "file_operations.log"
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'project': project_name,
        'file': file_path,
        'size': content_length,
        'operation': 'save'
    }
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')

def create_project_structure(project_name: str, structure: dict):
    """خود بخود پروجیکٹ ڈھانچہ بنائیں"""
    results = []
    for file_path, content in structure.items():
        try:
            result = save_file(project_name, file_path, content)
            results.append({
                'file': file_path,
                'status': 'created',
                'path': result
            })
        except Exception as e:
            results.append({
                'file': file_path,
                'status': 'error',
                'error': str(e)
            })
    
    return results

# Example project structures
WEB_APP_STRUCTURE = {
    "app.py": "# Main Flask Application\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/')\ndef home():\n    return 'Hello from Agent50!'\n\nif __name__ == '__main__':\n    app.run(debug=True)",
    "models.py": "# Database Models\nfrom flask_sqlalchemy import SQLAlchemy\n\ndb = SQLAlchemy()\n\nclass User(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    username = db.Column(db.String(80), unique=True, nullable=False)",
    "requirements.txt": "flask==2.3.3\nflask-sqlalchemy==3.0.5\npython-dotenv==1.0.0",
    "config.py": "# Configuration\nimport os\n\nclass Config:\n    SECRET_KEY = os.environ.get('SECRET_KEY') or 'agent50-super-king'",
    "static/css/style.css": "body { font-family: Arial, sans-serif; margin: 40px; }",
    "templates/index.html": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Agent50 App</title>\n    <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/style.css') }}\">\n</head>\n<body>\n    <h1>👑 AGENT 50 Generated App</h1>\n    <p>This app was created automatically by Agent50</p>\n</body>\n</html>"
}

API_STRUCTURE = {
    "main.py": "# FastAPI Application\nfrom fastapi import FastAPI\n\napp = FastAPI(title=\"Agent50 API\")\n\n@app.get(\"/\")\ndef read_root():\n    return {\"message\": \"Agent50 API is running\"}\n\n@app.get(\"/health\")\ndef health_check():\n    return {\"status\": \"healthy\"}",
    "models.py": "# Pydantic Models\nfrom pydantic import BaseModel\n\nclass User(BaseModel):\n    username: str\n    email: str",
    "requirements.txt": "fastapi==0.104.1\nuvicorn==0.24.0\npydantic==2.5.0"
}

if __name__ == "__main__":
    # ٹیسٹ کے لیے
    print("🧪 Testing Auto Save System...")
    
    # ٹیسٹ فائل سیو کریں
    test_path = save_file("test_project", "hello.txt", "Hello from Agent50 Auto Save System!")
    print(f"✅ File saved: {test_path}")
    
    # فائلوں کی فہرست دیکھیں
    files = list_project_files("test_project")
    print(f"📁 Files: {files}")
    
    # پروجیکٹ اعداد و شمار
    stats = get_project_stats("test_project")
    print(f"📊 Stats: {stats}")