from __future__ import annotations
from datetime import datetime
from pathlib import Path
import os

print("=== 🔥 UPDATED AI DEV AGENT - REAL AI POWER 🔥 ===")

# ---------- AI Client Import ----------
try:
    from agent.ai_client import ai_client
    AI_AVAILABLE = True
    print("✅ AI Client loaded successfully!")
except ImportError as e:
    print(f"❌ AI Client import error: {e}")
    AI_AVAILABLE = False

# ---------- Paths & directories ----------
BASE_DIR = Path(__file__).resolve().parents[1]
PROJECTS_DIR = BASE_DIR / "projects"
LOGS_DIR = BASE_DIR / "logs"

def ensure_dirs() -> None:
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)

def log_message(message: str) -> None:
    ensure_dirs()
    log_file = LOGS_DIR / "agent.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}\n"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(line)

def sanitize_project_name(raw_name: str) -> str:
    name = raw_name.strip()
    if not name:
        return "demo_project"
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, "_")
    name = name.replace(" ", "_").lower()
    return name or "project"

def ask_ai(task_description: str, filename: str, project_name: str) -> str:
    """Real AI se code generate karta hai"""
    if not AI_AVAILABLE:
        print("❌ AI not available - using fallback")
        return fallback_code(project_name, filename, task_description)
    
    # Check API key
    if not hasattr(ai_client, 'api_key') or not ai_client.api_key:
        print("❌ API Key not found - using fallback")
        return fallback_code(project_name, filename, task_description)
    
    print("🤖 Real AI se code generate ho raha hai...")
    
    prompt = f"""You are an expert Python developer. Create complete, working code for this task.

PROJECT: {project_name}
FILENAME: {filename}
TASK: {task_description}

Return ONLY the Python code without any explanation or markdown formatting."""
    
    response = ai_client.ask_ai(prompt)
    
    if response.startswith("# Error:") or "Error:" in response:
        print(f"⚠️ AI Error: {response[:100]}...")
        return fallback_code(project_name, filename, task_description)
    
    print("✅ Real AI code generated successfully!")
    return response

def fallback_code(project_name: str, filename: str, task_description: str) -> str:
    """Fallback code when AI is unavailable"""
    return f'''
# Auto-generated file by AI Dev Agent
# Project: {project_name}
# File: {filename}
# Task: {task_description}
# NOTE: AI service unavailable, using fallback code

print("Hello from AI-generated code!")
print("Project: {project_name}")
print("File: {filename}")
print("Task: {task_description}")
'''

def save_code(project_name: str, filename: str, code: str) -> Path:
    ensure_dirs()
    project_dir = PROJECTS_DIR / project_name
    project_dir.mkdir(parents=True, exist_ok=True)
    file_path = project_dir / filename
    with file_path.open("w", encoding="utf-8") as f:
        f.write(code)
    log_message(f"[{project_name}] Saved file: {file_path}")
    return file_path

def main() -> None:
    ensure_dirs()
    print("=== AI Dev Agent – REAL AI VERSION ===")
    print("Ye version REAL AI se code generate karta hai!\n")

    raw_project_name = input("Project ka naam likhen (e.g. demo_project):\n> ").strip()
    if not raw_project_name:
        raw_project_name = "demo_project"
    project_name = sanitize_project_name(raw_project_name)

    task = input("\nTask likhen (short description, e.g. 'simple hello world app'):\n> ").strip()
    if not task:
        print("Task khali nahi ho sakta. Program exit ho raha hai.")
        return

    filename = input("\nFilename likhen (e.g. app.py):\n> ").strip()
    if not filename:
        filename = "app.py"

    log_message(f"[{project_name}] New task: {task} | file: {filename}")

    code = ask_ai(task_description=task, filename=filename, project_name=project_name)

    file_path = save_code(project_name=project_name, filename=filename, code=code)

    print(f"\n✅ Code save ho gaya: {file_path}")
    
    # File content show karen
    print(f"\n📁 Generated File Content:")
    print("=" * 50)
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)
    print("=" * 50)

if __name__ == "__main__":
    main()