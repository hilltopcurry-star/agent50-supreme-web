"""
👑 KING DEEPSEEK - App Routes Fixer
Bhai ye file create karo aur run karo!
"""

from pathlib import Path

print("👑 KING DEEPSEEK - Fixing App Routes...")

project_dir = Path("projects/agent50")
app_file = project_dir / "app.py"

# Read current app.py
with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix database routes - add proper error handling
fixed_routes = '''

# Database API Routes - KING DEEPSEEK FIXED VERSION
@app.route('/api/db/stats')
def db_stats():
    """Get database statistics"""
    try:
        from models import get_database_stats
        stats = get_database_stats()
        return jsonify({"success": True, "stats": stats})
    except Exception as e:
        print(f"Database stats error: {e}")
        return jsonify({"success": False, "error": "Database connection failed"}), 500

@app.route('/api/users')
def get_users():
    """Get all users"""
    try:
        from crud_operations import UserCRUD
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
        from crud_operations import ProjectCRUD
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
'''

# Replace existing routes with fixed ones
if '# Database API Routes' in content:
    # Find and replace the database routes section
    start = content.find('# Database API Routes')
    end = content.find('@app.route', start + 50)
    if end != -1:
        # Find the next section
        next_section = content.find('\n\n', end)
        if next_section != -1:
            content = content[:start] + fixed_routes + content[next_section:]

# Write fixed content
with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ App routes fixed successfully!")
print("🔄 Please restart your app: python app.py")