from __future__ import annotations
import subprocess
import re
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

try:
    from command_runner import CommandRunner
    COMMAND_RUNNER_AVAILABLE = True
except ImportError:
    COMMAND_RUNNER_AVAILABLE = False
    print("⚠️ CommandRunner not available - using basic functions")

class ErrorHandler:
    def __init__(self):
        if COMMAND_RUNNER_AVAILABLE:
            self.runner = CommandRunner()
        else:
            self.runner = None
        
        self.base_dir = Path(__file__).parent
        self.projects_dir = self.base_dir / "projects"
    
    def run_safe_command(self, command: str, project_name: str) -> dict:
        """Basic command execution"""
        try:
            project_dir = self.projects_dir / project_name
            result = subprocess.run(
                command,
                shell=True,
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": ""
            }
    
    def detect_errors(self, command_output: str) -> list:
        """
        Common errors detect karta hai command output se
        """
        errors = []
        
        # Module not found errors
        module_matches = re.findall(r"ModuleNotFoundError: No module named '(\w+)'", command_output)
        for module in module_matches:
            errors.append({
                "type": "missing_dependency",
                "module": module,
                "solution": f"pip install {module}",
                "description": f"Python module '{module}' is missing"
            })
        
        # Import errors
        import_matches = re.findall(r"ImportError: (.*)", command_output)
        for imp_error in import_matches:
            errors.append({
                "type": "import_error", 
                "description": imp_error,
                "solution": "Check import statements and dependencies"
            })
        
        # Syntax errors
        if "SyntaxError" in command_output:
            syntax_match = re.search(r"SyntaxError: (.*)", command_output)
            description = syntax_match.group(1) if syntax_match else "Invalid Python syntax"
            errors.append({
                "type": "syntax_error",
                "description": description,
                "solution": "Fix Python syntax errors in code"
            })
        
        # File not found errors
        if "FileNotFoundError" in command_output:
            errors.append({
                "type": "file_not_found",
                "description": "Required file not found",
                "solution": "Check file paths and names"
            })
        
        # Permission errors
        if "PermissionError" in command_output:
            errors.append({
                "type": "permission_error", 
                "description": "File permission issue",
                "solution": "Check file permissions and access rights"
            })
        
        return errors
    
    def auto_fix_errors(self, project_name: str, errors: list) -> dict:
        """
        Common errors automatically fix karta hai
        """
        fixes_applied = []
        
        for error in errors:
            if error["type"] == "missing_dependency":
                print(f"🔧 Installing missing dependency: {error['module']}")
                fix_result = self.run_safe_command(
                    f"pip install {error['module']}", 
                    project_name
                )
                fixes_applied.append({
                    "error": error,
                    "fix_result": fix_result,
                    "fixed": fix_result["success"]
                })
            
            elif error["type"] == "import_error":
                print(f"⚠️ Import error detected: {error['description']}")
                print(f"💡 Solution: {error['solution']}")
                fixes_applied.append({
                    "error": error,
                    "fix_result": {"success": False, "output": "Manual fix required"},
                    "fixed": False
                })
        
        return {
            "total_errors": len(errors),
            "fixes_applied": fixes_applied,
            "successful_fixes": len([f for f in fixes_applied if f["fixed"]])
        }
    
    def analyze_project(self, project_name: str) -> dict:
        """
        Complete project analysis with error detection and fixing
        """
        print(f"🔍 Analyzing project: {project_name}")
        
        # Step 1: Try to run the project
        test_result = self.run_safe_command("python app.py", project_name)
        
        # Step 2: Detect errors
        errors = self.detect_errors(test_result["error"] or test_result["output"])
        
        # Step 3: Auto-fix errors
        if errors:
            print(f"📋 Found {len(errors)} errors:")
            for error in errors:
                print(f"   - {error['type']}: {error['description']}")
            
            fix_result = self.auto_fix_errors(project_name, errors)
            
            # Step 4: Test again after fixes
            if fix_result["successful_fixes"] > 0:
                print("🔄 Testing after fixes...")
                retest_result = self.run_safe_command("python app.py", project_name)
                test_result = retest_result
        
        return {
            "project": project_name,
            "initial_test": test_result,
            "errors_detected": errors,
            "fixes_applied": self.auto_fix_errors(project_name, errors) if errors else {"fixes_applied": []}
        }

def main():
    handler = ErrorHandler()
    
    print("=== 🛠️ AI DEV AGENT - ERROR HANDLER ===")
    print("Ye automatically errors detect aur fix karta hai!\n")
    
    project_name = input("Project ka naam likhen (e.g. agent50): ").strip()
    if not project_name:
        project_name = "agent50"
    
    project_dir = handler.projects_dir / project_name
    if not project_dir.exists():
        print(f"❌ Project '{project_name}' not found!")
        return
    
    print(f"\n🎯 Analyzing project: {project_name}")
    
    analysis = handler.analyze_project(project_name)
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"Project: {analysis['project']}")
    print(f"Errors detected: {len(analysis['errors_detected'])}")
    print(f"Fixes applied: {analysis['fixes_applied']['successful_fixes']}")
    
    if analysis['initial_test']['success']:
        print("✅ Project runs successfully!")
    else:
        print("❌ Project has issues that need manual fixing")

if __name__ == "__main__":
    main()