"""
SMART IMPORT DETECTOR - Agent 50 Supreme Level
Intelligent import analysis and automatic correction.
"""

import re
import ast
import importlib
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import subprocess

class SupremeImportDetector:
    """ULTIMATE Import Detection and Correction System"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.detected_issues = []
        self.auto_fixes_applied = []
        
    def analyze_file_imports(self, filename: str) -> Dict:
        """
        Deep analysis of imports in a specific file
        """
        file_path = self.project_path / filename
        
        if not file_path.exists():
            return {"error": f"File not found: {filename}", "issues": []}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for better accuracy
            tree = ast.parse(content)
            
            issues = []
            suggestions = []
            imports_found = []
            
            # AST analysis
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports_found.append(f"import {alias.name}")
                        issues.extend(self._check_import_module(alias.name))
                        
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports_found.append(f"from {module} import {alias.name}")
                        issues.extend(self._check_from_import(module, alias.name))
            
            # Regex fallback for complex cases
            regex_issues = self._regex_import_analysis(content)
            issues.extend(regex_issues)
            
            # Check if imports actually exist
            actual_issues = self._validate_imports_exist(content)
            issues.extend(actual_issues)
            
            # Generate suggestions
            for issue in issues:
                suggestion = self._generate_fix_suggestion(issue, content, filename)
                if suggestion:
                    suggestions.append(suggestion)
            
            return {
                "filename": filename,
                "imports": imports_found,
                "issues": issues,
                "suggestions": suggestions,
                "line_count": len(content.split('\n')),
                "has_bootstrap5": "Bootstrap5" in content,
                "has_main_import": "from main import" in content or "import main" in content,
                "has_bp_issue": ("bp" in content and "main_bp" not in content) and filename == "app.py"
            }
            
        except Exception as e:
            return {
                "filename": filename,
                "error": str(e),
                "issues": [f"Parse error: {str(e)}"],
                "suggestions": []
            }
    
    def _check_import_module(self, module_name: str) -> List[str]:
        """Check import statement for common issues"""
        issues = []
        
        # Check for Bootstrap5
        if module_name == "flask_bootstrap" or "bootstrap" in module_name.lower():
            issues.append("CHECK: Ensure using 'Bootstrap' not 'Bootstrap5'")
        
        # Check for flask_login (not installed)
        if module_name == "flask_login":
            issues.append("WARNING: flask_login not installed - use session auth")
        
        # Check for circular imports
        if module_name == "app" and self.project_name:
            issues.append("CRITICAL: Circular import 'import app' - use relative imports")
        
        return issues
    
    def _check_from_import(self, module: str, name: str) -> List[str]:
        """Check 'from X import Y' statements"""
        issues = []
        
        # Bootstrap5 detection
        if name == "Bootstrap5":
            issues.append("ERROR: Bootstrap5 doesn't exist in flask-bootstrap4")
        
        # bp vs main_bp confusion
        if module == "main" and name == "bp":
            issues.append("CRITICAL: 'from main import bp' but routes.py uses 'main_bp'")
        
        if module == "routes" and name == "bp":
            issues.append("CRITICAL: 'from routes import bp' but should be 'main_bp'")
        
        # Check if module exists
        if module and module.endswith('.py'):
            module_file = self.project_path / module
            if not module_file.exists():
                issues.append(f"MODULE NOT FOUND: {module} doesn't exist")
        
        return issues
    
    def _regex_import_analysis(self, content: str) -> List[str]:
        """Regex-based import analysis"""
        issues = []
        
        patterns = [
            (r'from flask_bootstrap import Bootstrap5', 
             "Bootstrap5 doesn't exist - use 'Bootstrap'"),
            (r'Bootstrap5\(\)', 
             "Bootstrap5() constructor doesn't exist - use Bootstrap()"),
            (r'from main import (bp|main_bp|blueprint)', 
             "Importing from main.py but should import from routes.py"),
            (r'from routes import bp\b', 
             "routes.py exports 'main_bp' not 'bp'"),
            (r'app\.register_blueprint\(bp', 
             "Should be 'app.register_blueprint(main_bp'"),
            (r'url_prefix=[\'"][^\'"]+[\'"]', 
             "Custom URL prefixes can cause 404 errors"),
            (r'flask_login\.', 
             "flask_login not installed - remove or use sessions"),
            (r'from app import', 
             "Circular import detected - avoid 'from app import'"),
        ]
        
        for pattern, message in patterns:
            if re.search(pattern, content):
                issues.append(message)
        
        return issues
    
    def _validate_imports_exist(self, content: str) -> List[str]:
        """Validate if imported modules/files actually exist"""
        issues = []
        
        # Find all import statements
        import_lines = re.findall(r'^(?:from|import)\s+([^\s#]+)', content, re.MULTILINE)
        
        for imp in import_lines:
            # Skip standard library and pip packages
            if any(std in imp for std in ['os', 'sys', 'json', 're', 'datetime', 'flask']):
                continue
            
            # Check if it's a local file
            if imp.endswith('.py') or ('.' not in imp and len(imp) < 20):
                possible_paths = [
                    self.project_path / f"{imp}.py",
                    self.project_path / imp.replace('.', '/') / "__init__.py",
                    Path.cwd() / f"{imp}.py"
                ]
                
                exists = any(p.exists() for p in possible_paths)
                if not exists:
                    issues.append(f"LOCAL MODULE NOT FOUND: {imp}")
        
        return issues
    
    def _generate_fix_suggestion(self, issue: str, content: str, filename: str) -> Dict:
        """Generate automatic fix for an import issue"""
        fixes = {
            "Bootstrap5 doesn't exist - use 'Bootstrap'": {
                "find": ["Bootstrap5", "from flask_bootstrap import Bootstrap5"],
                "replace": ["Bootstrap", "from flask_bootstrap import Bootstrap"],
                "description": "Fixed Bootstrap5 import"
            },
            "Bootstrap5() constructor doesn't exist - use Bootstrap()": {
                "find": ["Bootstrap5()", "Bootstrap5(app)"],
                "replace": ["Bootstrap()", "Bootstrap(app)"],
                "description": "Fixed Bootstrap5 constructor"
            },
            "Importing from main.py but should import from routes.py": {
                "find": ["from main import", "import main"],
                "replace": ["from routes import", "import routes"],
                "description": "Changed main.py imports to routes.py"
            },
            "routes.py exports 'main_bp' not 'bp'": {
                "find": ["from routes import bp", "import routes.bp"],
                "replace": ["from routes import main_bp", "import routes.main_bp"],
                "description": "Fixed bp vs main_bp import"
            },
            "Should be 'app.register_blueprint(main_bp'": {
                "find": ["app.register_blueprint(bp", "bp,"],
                "replace": ["app.register_blueprint(main_bp", "main_bp,"],
                "description": "Fixed blueprint registration"
            },
            "flask_login not installed - remove or use sessions": {
                "find": ["from flask_login import", "flask_login."],
                "replace": ["# flask_login not installed - using sessions", "# flask_login not installed"],
                "description": "Removed flask_login imports"
            }
        }
        
        for key, fix in fixes.items():
            if key in issue:
                return {
                    "issue": issue,
                    "fix": fix,
                    "file": filename,
                    "auto_fixable": True
                }
        
        return {
            "issue": issue,
            "fix": None,
            "file": filename,
            "auto_fixable": False
        }
    
    def apply_auto_fix(self, filename: str, fix_suggestion: Dict) -> bool:
        """Apply automatic fix to a file"""
        if not fix_suggestion.get("auto_fixable", False):
            return False
        
        file_path = self.project_path / filename
        if not file_path.exists():
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            fix = fix_suggestion["fix"]
            original_content = content
            
            for find_str, replace_str in zip(fix["find"], fix["replace"]):
                if find_str in content:
                    content = content.replace(find_str, replace_str)
            
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.auto_fixes_applied.append({
                    "file": filename,
                    "fix": fix["description"],
                    "timestamp": str(Path(file_path).stat().st_mtime)
                })
                
                return True
        
        except Exception as e:
            print(f"  [ERROR] Auto-fix failed for {filename}: {e}")
        
        return False
    
    def scan_all_project_files(self) -> Dict:
        """Scan ALL Python files in project for import issues"""
        all_issues = []
        all_suggestions = []
        
        python_files = list(self.project_path.glob("*.py"))
        python_files.extend(self.project_path.rglob("*.py"))
        
        for py_file in python_files:
            if py_file.is_file():
                rel_path = py_file.relative_to(self.project_path)
                result = self.analyze_file_imports(str(rel_path))
                
                if result.get("issues"):
                    all_issues.extend(result["issues"])
                
                if result.get("suggestions"):
                    all_suggestions.extend(result["suggestions"])
        
        # Apply auto-fixes
        fixes_applied = []
        for suggestion in all_suggestions:
            if suggestion.get("auto_fixable", False):
                if self.apply_auto_fix(suggestion["file"], suggestion):
                    fixes_applied.append(suggestion["fix"]["description"])
        
        return {
            "total_files_scanned": len(python_files),
            "total_issues": len(all_issues),
            "issues": all_issues[:20],  # Limit to 20 issues
            "total_suggestions": len(all_suggestions),
            "auto_fixes_applied": fixes_applied,
            "fix_count": len(fixes_applied)
        }
    
    def get_critical_import_warnings(self) -> List[str]:
        """Get only CRITICAL import warnings"""
        scan = self.scan_all_project_files()
        critical = []
        
        for issue in scan.get("issues", []):
            if any(keyword in issue.lower() for keyword in 
                  ['critical', 'error', 'doesn\'t exist', 'not found', 'circular']):
                critical.append(issue)
        
        return critical

# Quick utility functions
def detect_and_fix_imports(project_name: str) -> Dict:
    """One-shot import detection and auto-fix"""
    detector = SupremeImportDetector(project_name)
    return detector.scan_all_project_files()

def check_bootstrap5_issues(project_name: str) -> List[str]:
    """Specifically check for Bootstrap5 issues"""
    detector = SupremeImportDetector(project_name)
    scan = detector.scan_all_project_files()
    
    bootstrap_issues = []
    for issue in scan.get("issues", []):
        if "bootstrap5" in issue.lower():
            bootstrap_issues.append(issue)
    
    return bootstrap_issues