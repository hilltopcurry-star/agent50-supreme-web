from __future__ import annotations
from datetime import datetime
from pathlib import Path
import os
import requests
import json

print("=== 🤖 AI DEV AGENT - REAL AI POWERED 🤖 ===")

# ---------- Paths & directories ----------
BASE_DIR = Path(__file__).parent
PROJECTS_DIR = BASE_DIR / "projects"
LOGS_DIR = BASE_DIR / "logs"

def ensure_dirs():
    PROJECTS_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)

def log_message(message: str):
    ensure_dirs()
    log_file = LOGS_DIR / "agent.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with log_file.open("a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def ask_ai(task_description: str, filename: str, project_name: str) -> str:
    """Real DeepSeek API se code generate karta hai"""
    print("🤖 Real AI se code generate ho raha hai...")
    
    API_KEY = "sk-9214c5054a7f4b828cf3f9d608a88f6a"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    prompt = f"""You are an expert Python developer. Create complete, working code for this task.

PROJECT: {project_name}
FILENAME: {filename}
TASK: {task_description}

Return ONLY the Python code without any explanation or markdown formatting."""
    
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            code = result["choices"][0]["message"]["content"]
            print("✅ Real AI code generated successfully!")
            return code
        else:
            print(f"❌ API Error: {response.status_code}")
            return f"# API Error\nprint('API Error occurred')"
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return f"# Error\nprint('Request failed: {e}')"

def main():
    ensure_dirs()
    print("Ye version REAL AI se code generate karta hai!\n")

    project_name = input("Project ka naam likhen: ").strip() or "demo_project"
    task = input("Task likhen: ").strip() or "simple hello world app"
    filename = input("Filename likhen: ").strip() or "app.py"

    code = ask_ai(task, filename, project_name)
    
    # Save code
    project_dir = PROJECTS_DIR / project_name
    project_dir.mkdir(exist_ok=True)
    file_path = project_dir / filename
    
    with file_path.open("w", encoding="utf-8") as f:
        f.write(code)
    
    print(f"\n✅ Code save ho gaya: {file_path}")
    print(f"\n📁 Generated Code:")
    print("=" * 50)
    print(code)
    print("=" * 50)

if __name__ == "__main__":
    main()