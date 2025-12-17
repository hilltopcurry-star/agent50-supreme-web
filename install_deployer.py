import os

print("🔧 INSTALLING KING DEPLOYER MODULE...")

# The Content of king_deployer.py
code = """import os
import subprocess
import json
from pathlib import Path

# --- CONFIGURATION ---
DEPLOY_STATE_FILE = "deploy_state.json"

class KingDeployer:
    def __init__(self, project_dir):
        self.project_dir = Path(project_dir)
        self.state_file = self.project_dir / DEPLOY_STATE_FILE
        self.state = self.load_state()

    def load_state(self):
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return {
            "git_initialized": False,
            "docker_ready": False,
            "render_config_ready": False,
            "last_update": None
        }

    def save_state(self):
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=4)

    def run_command(self, command):
        try:
            print(f"  ⚡ Running: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=self.project_dir, 
                capture_output=True, 
                text=True,
                encoding='utf-8', 
                errors='replace'
            )
            if result.returncode == 0:
                print("    ✅ Success")
                return True, result.stdout
            else:
                print(f"    ❌ Failed: {result.stderr}")
                return False, result.stderr
        except Exception as e:
            return False, str(e)

    def init_git(self):
        print(f"\n🐙 [GIT] Initializing Repository in {self.project_dir.name}...")
        gitignore_content = ".venv\\n__pycache__\\n*.pyc\\ninstance/\\n*.db\\n.env\\n.DS_Store"
        with open(self.project_dir / ".gitignore", "w", encoding='utf-8') as f:
            f.write(gitignore_content.strip())
        
        if not (self.project_dir / ".git").exists():
            self.run_command("git init")
            self.state["git_initialized"] = True
        
        self.run_command("git add .")
        self.run_command('git commit -m "Initial commit by Agent 50 Supreme"')
        self.save_state()
        print("  ✅ Git Repository Ready.")

    def prepare_for_render(self):
        print(f"\n🚀 [RENDER] Preparing Deployment Assets...")
        with open(self.project_dir / "Procfile", "w", encoding='utf-8') as f:
            f.write("web: gunicorn app:app")
        
        render_yaml = f"services:\\n  - type: web\\n    name: {self.project_dir.name}\\n    env: python\\n    buildCommand: pip install -r requirements.txt\\n    startCommand: gunicorn app:app"
        with open(self.project_dir / "render.yaml", "w", encoding='utf-8') as f:
            f.write(render_yaml)
            
        self.state["render_config_ready"] = True
        self.save_state()
        print("  ✅ Render Configuration Ready.")

    def generate_guide(self):
        print(f"\n📘 [DOCS] Generating Deployment Guide...")
        guide = "# Deployment Guide\\n\\n1. Create GitHub Repo\\n2. Connect to Render.com"
        with open(self.project_dir / "README_DEPLOY.md", "w", encoding='utf-8') as f:
            f.write(guide)
        print("  ✅ README_DEPLOY.md Created.")

    def execute_pipeline(self):
        print(f"🏗️ STARTING DEPLOYMENT PREP FOR: {self.project_dir.name}")
        self.init_git()
        self.prepare_for_render()
        self.generate_guide()
        print("👑 DEPLOYMENT PREP COMPLETE.")
"""

# Force write the file correctly
with open("king_deployer.py", "w", encoding="utf-8") as f:
    f.write(code)

print("✅ SUCCESS: 'king_deployer.py' has been created correctly.")
"""

### Step 3: Run Karein 🚀

1.  Notepad **Save (`Ctrl+S`)** karein aur band kar dein.
2.  Terminal mein yeh commands chalayen:

```powershell
python install_deployer.py