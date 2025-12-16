import sys
import os
sys.path.append('.')  # Agent 50 ke folder ko include karein

from agent_skills import skill_lint_login_flow
from pathlib import Path

print("🧠 AGENT 50 BRAIN TEST - Name Mismatch Fix\n")

# Test project
project_name = "supreme_delivery_app"

print("1. Brain ko activate karna...")
result = skill_lint_login_flow(project_name)

if result:
    print("✅ Brain ne fix kiya!")
else:
    print("❌ Brain ne kuch nahi fix kiya")

print("\n2. Ab dekhte hain files ka haal...")
project_dir = Path("projects/supreme_delivery_app")

# Check app.py
print("\n📄 app.py check:")
with open(project_dir / "app.py", "r") as f:
    app_content = f.read()
    if "from routes import bp" in app_content:
        print("   ❌ Masla hai: 'from routes import bp' (abhi bhi galat)")
    elif "from routes import main_bp" in app_content:
        print("   ✅ Theek hai: 'from routes import main_bp'")
    else:
        print("   ⚠️ Kuch aur import hai")

# Check routes.py
print("\n📄 routes.py check:")
with open(project_dir / "routes.py", "r") as f:
    routes_content = f.read()
    if "bp = Blueprint" in routes_content:
        print("   ❌ Masla: routes.py mein 'bp' hai")
    elif "main_bp = Blueprint" in routes_content:
        print("   ✅ Theek: routes.py mein 'main_bp' hai")
    else:
        print("   ⚠️ Blueprint ka pata nahi")

print("\n🧪 Ab manual test karein:")
os.chdir(project_dir)
os.system("python app.py")