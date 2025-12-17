"""
KING DEEPSEEK - App Integration Fixer
Bhai ye file create karo aur run karo!
"""

from pathlib import Path

print("👑 KING DEEPSEEK - App Integration Fix Shuru!")

# Project directory
project_dir = Path("projects/agent50")
app_file = project_dir / "app.py"

# Read current app.py
with open(app_file, 'r', encoding='utf-8') as f:
    content = f.read()

print("🔧 Fixing database initialization in app.py...")

# Fix the database initialization - add import
if "from models import init_database" not in content:
    # Find where to add the import (after other imports)
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.strip() and not line.startswith(('import ', 'from ', '#', '"', "'")) and not line.strip().startswith('#'):
            # Insert import here
            lines.insert(i, "from models import init_database, get_db_session")
            break
    
    content = '\n'.join(lines)

# Fix the init_database call
if "init_database()" in content and "from models import init_database" not in content:
    # Add import at the top
    content = "from models import init_database, get_db_session\n" + content

# Write fixed content back
with open(app_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ App.py database integration fixed!")
print("📁 File updated: projects/agent50/app.py")