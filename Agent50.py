import os
import sys
import subprocess
import time
import webbrowser
import threading

# --- AGENT 50: SUPREME CONTROLLER (FIXED) ---

def print_agent(msg):
    print(f"🤖 [AGENT 50]: {msg}")

def find_project_dirs():
    base_dir = os.getcwd()
    print_agent(f"Scanning area: {base_dir}...")
    
    for root, dirs, files in os.walk(base_dir):
        if "delivery_production_v2" in dirs:
            project_path = os.path.join(root, "delivery_production_v2")
            print_agent(f"✅ Project Found at: {project_path}")
            return project_path
    
    print_agent("❌ Project folder nahi mila. Make sure I am in 'agent 50' folder.")
    return None

def start_backend(project_path):
    print_agent("🧠 Starting Backend (Brain)...")
    app_py = os.path.join(project_path, "app.py")
    
    if not os.path.exists(app_py):
        print_agent("⚠️ Critical: app.py missing!")
        return None

    # Server start kar raha hoon
    process = subprocess.Popen([sys.executable, "app.py"], cwd=project_path, shell=True)
    return process

def start_frontend(project_path):
    print_agent("💻 Starting Frontend (Face)...")
    frontend_path = os.path.join(project_path, "frontend")
    
    if not os.path.exists(frontend_path):
        print_agent("❌ Frontend folder missing!")
        return None
        
    # NPM Start command
    npm_cmd = "npm start"
    process = subprocess.Popen(npm_cmd, cwd=frontend_path, shell=True)
    return process

def main():
    print("\n" + "="*40)
    print("   🚀 AGENT 50: RELOADED")
    print("   Boss, main kaam shuru kar raha hoon.")
    print("="*40 + "\n")

    # 1. Location Trace
    project_path = find_project_dirs()
    
    if not project_path:
        return

    # 2. Kill Only Node (React), Python ko zinda rakho
    # (Hum sirf purana frontend saaf karenge taake port 3000 free ho)
    if os.name == 'nt': 
        os.system("taskkill /f /im node.exe >nul 2>&1")

    # 3. Backend Launch
    backend_proc = start_backend(project_path)
    print_agent("⏳ Backend initializing (5 sec)...")
    time.sleep(5) 

    # 4. Frontend Launch
    frontend_proc = start_frontend(project_path)
    print_agent("⏳ Frontend initializing (10 sec)...")
    time.sleep(10)

    # 5. OPEN BROWSER
    target_url = "http://localhost:3000/login"
    print_agent(f"🎉 Opening Portal: {target_url}")
    webbrowser.open(target_url)

    print("\n" + "="*40)
    print("✅ MISSION SUCCESS.")
    print("Agent 50 is running. Is window ko band mat karna.")
    print("="*40 + "\n")

    try:
        # Script ko rok ke rakho taake server chalta rahe
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        print_agent("Shutting down...")

if __name__ == "__main__":
    main()