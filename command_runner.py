from __future__ import annotations
import subprocess
import sys
from pathlib import Path
import os

class CommandRunner:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.projects_dir = self.base_dir / "projects"
        self.allowed_commands = [
            "python", "pip", "npm", "node", "git",
            "echo", "dir", "ls", "cd"
        ]
    
    def run_safe_command(self, command: str, project_name: str, cwd: Path = None) -> dict:
        """
        Safe command execution with error handling
        """
        try:
            # Set working directory
            if not cwd:
                cwd = self.projects_dir / project_name
            
            # Basic security check
            cmd_parts = command.split()
            if cmd_parts[0] not in self.allowed_commands:
                return {
                    "success": False,
                    "error": f"Command not allowed: {cmd_parts[0]}",
                    "output": ""
                }
            
            print(f"🚀 Running: {command}")
            print(f"📁 Directory: {cwd}")
            
            # Run command
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "output": result.stdout,
                "error": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Command timed out after 30 seconds",
                "output": ""
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution failed: {str(e)}",
                "output": ""
            }
    
    def install_dependencies(self, project_name: str) -> dict:
        """
        Auto-detect and install Python dependencies
        """
        project_dir = self.projects_dir / project_name
        
        # Check for requirements.txt
        requirements_file = project_dir / "requirements.txt"
        if requirements_file.exists():
            print("📦 Installing dependencies from requirements.txt...")
            return self.run_safe_command("pip install -r requirements.txt", project_name)
        
        # Check for common dependencies in code
        python_files = list(project_dir.glob("*.py"))
        dependencies = set()
        
        for py_file in python_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "import flask" in content or "from flask" in content:
                    dependencies.add("flask")
                if "import requests" in content:
                    dependencies.add("requests")
                if "import numpy" in content:
                    dependencies.add("numpy")
        
        if dependencies:
            deps_str = " ".join(dependencies)
            print(f"📦 Installing detected dependencies: {deps_str}")
            return self.run_safe_command(f"pip install {deps_str}", project_name)
        
        return {
            "success": True,
            "output": "No dependencies detected to install",
            "error": ""
        }
    
    def test_project(self, project_name: str) -> dict:
        """
        Auto-test the generated project
        """
        project_dir = self.projects_dir / project_name
        
        # Try to find main Python file
        python_files = list(project_dir.glob("*.py"))
        if not python_files:
            return {
                "success": False,
                "error": "No Python files found to test",
                "output": ""
            }
        
        # Try app.py, main.py, or first Python file
        main_file = None
        for preferred in ["app.py", "main.py"]:
            if (project_dir / preferred).exists():
                main_file = preferred
                break
        
        if not main_file:
            main_file = python_files[0].name
        
        print(f"🧪 Testing project: {main_file}")
        
        # First install dependencies
        install_result = self.install_dependencies(project_name)
        if not install_result["success"]:
            return install_result
        
        # Try to run the Python file
        return self.run_safe_command(f"python {main_file}", project_name)

def main():
    runner = CommandRunner()
    
    print("=== 🛠️ AI DEV AGENT - COMMAND RUNNER ===")
    print("Ye automatically generated code ko run aur test karta hai!\n")
    
    project_name = input("Project ka naam likhen (e.g. agent50): ").strip()
    if not project_name:
        print("❌ Project name required!")
        return
    
    project_dir = runner.projects_dir / project_name
    if not project_dir.exists():
        print(f"❌ Project '{project_name}' not found!")
        return
    
    print(f"\n🔍 Project found: {project_name}")
    print("Files in project:")
    for file in project_dir.iterdir():
        print(f"  - {file.name}")
    
    print("\n1. Install dependencies")
    print("2. Test/Run project")
    print("3. Custom command")
    
    choice = input("\nChoose option (1/2/3): ").strip()
    
    if choice == "1":
        result = runner.install_dependencies(project_name)
    elif choice == "2":
        result = runner.test_project(project_name)
    elif choice == "3":
        custom_cmd = input("Enter custom command: ").strip()
        result = runner.run_safe_command(custom_cmd, project_name)
    else:
        print("❌ Invalid choice!")
        return
    
    print(f"\n📊 Command Result:")
    print(f"Success: {result['success']}")
    if result['output']:
        print(f"Output:\n{result['output']}")
    if result['error']:
        print(f"Errors:\n{result['error']}")

if __name__ == "__main__":
    main()