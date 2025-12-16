import os
import sys
import subprocess
import time
import webbrowser

# --- REALITY CHECK SCRIPT ---

def print_agent(msg):
    print(f"🤖 [AGENT 50]: {msg}")

def install_dependencies():
    print_agent("Checking Internet & Installing Real Tools...")
    # Ye Dummy nahi hai - Ye internet se Asal Libraries download karega
    tools = ["flask", "flask-cors", "flask-sqlalchemy", "flask-socketio", "flask-jwt-extended", "requests"]
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + tools)
        print_agent("✅ Real Tools Installed Successfully.")
    except Exception as e:
        print_agent(f"❌ Internet Error: {e}")

def main():
    print("\n" + "="*40)
    print("   ⚡ AGENT 50: REALITY CHECK ⚡")
    print("="*40 + "\n")

    # 1. Project Dhoondna
    base_dir = os.getcwd()
    project_path = None
    for root, dirs, files in os.walk(base_dir):
        if "delivery_production_v2" in dirs:
            project_path = os.path.join(root, "delivery_production_v2")
            break
    
    if not project_path:
        print_agent("❌ ERROR: Project folder hi nahi mila! (Agent 50 khali hai)")
        return

    # 2. Asli Tools Install Karna (Proof of Life)
    install_dependencies()

    # 3. Backend (Dimaagh) Start Karna
    print_agent("🧠 Starting Brain (Backend)...")
    app_process = subprocess.Popen(
        [sys.executable, "app.py"], 
        cwd=project_path,
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )

    # 4. Frontend (Chehra) Start Karna
    print_agent("💻 Starting Face (Frontend)...")
    frontend_dir = os.path.join(project_path, "frontend")
    subprocess.Popen("npm start", cwd=frontend_dir, shell=True)

    print_agent("⏳ Waiting for connection (10 sec)...")
    time.sleep(10)

    # 5. Check Output (Truth)
    if app_process.poll() is not None:
        stdout, stderr = app_process.communicate()
        print("\n" + "!"*40)
        print("❌ AGENT DIED. HERE IS THE REAL REASON:")
        print(stderr) # Ye hai Asal Wajah
        print("!"*40 + "\n")
    else:
        print_agent("✅ AGENT IS ALIVE! Backend chal raha hai.")
        webbrowser.open("http://localhost:3000/register")

if __name__ == "__main__":
    main()