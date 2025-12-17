import os
import sys
import subprocess
import time
import webbrowser

def main():
    print("\n🚀 LAUNCHING AGENT 50 (FINAL STEP)...")
    
    # 1. Project Dhoondna
    base_dir = os.getcwd()
    project_path = None
    for root, dirs, files in os.walk(base_dir):
        if "delivery_production_v2" in dirs:
            project_path = os.path.join(root, "delivery_production_v2")
            break
            
    if not project_path:
        print("❌ Error: Project folder nahi mila.")
        return

    # 2. Node ko saaf karna (Python pehle hi saaf hai)
    if os.name == 'nt':
        os.system("taskkill /f /im node.exe >nul 2>&1")

    # 3. Backend Start
    print("🧠 Starting Backend (Clean Code)...")
    # Backend ko background mein chalayenge
    subprocess.Popen([sys.executable, "app.py"], cwd=project_path, shell=True)
    time.sleep(5)

    # 4. Frontend Start
    print("💻 Starting Frontend...")
    frontend_dir = os.path.join(project_path, "frontend")
    subprocess.Popen("npm start", cwd=frontend_dir, shell=True)

    print("✅ System Live. Opening Browser in 10 seconds...")
    time.sleep(10)
    webbrowser.open("http://localhost:3000/register")

if __name__ == "__main__":
    main()