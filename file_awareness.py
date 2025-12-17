"""
FILE AWARENESS MODULE - Agent 50 Supreme Level
Detects actual files, prevents hallucinations, ensures real file awareness.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set
import json

class SupremeFileAwareness:
    """ULTIMATE File Awareness System for Agent 50"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.scan_results = {}
        self.memory_file = self.project_path / ".file_awareness_memory.json"
        
    def scan_project_files(self) -> Dict:
        """
        Scan ALL files in project and return detailed analysis
        """
        print(f"  [AWARE] Supreme Scanning: {self.project_name}")
        
        if not self.project_path.exists():
            return {"error": "Project directory not found", "files": []}
        
        # Comprehensive scanning
        all_files = []
        python_files = []
        template_files = []
        config_files = []
        
        for root, dirs, files in os.walk(self.project_path):
            for file in files:
                full_path = Path(root) / file
                rel_path = full_path.relative_to(self.project_path)
                
                file_info = {
                    "name": file,
                    "path": str(rel_path),
                    "full_path": str(full_path),
                    "size": os.path.getsize(full_path),
                    "extension": Path(file).suffix.lower(),
                    "is_python": file.endswith('.py'),
                    "is_template": 'templates' in str(rel_path),
                    "is_config": any(keyword in file.lower() for keyword in 
                                   ['config', 'settings', '.env', 'requirements'])
                }
                
                all_files.append(file_info)
                
                if file_info["is_python"]:
                    python_files.append(file_info)
                if file_info["is_template"]:
                    template_files.append(file_info)
                if file_info["is_config"]:
                    config_files.append(file_info)
        
        # Analyze Python imports
        import_analysis = self._analyze_python_imports(python_files)
        
        # Critical file detection
        critical_files = self._detect_critical_files(python_files)
        
        # Save scan results
        self.scan_results = {
            "total_files": len(all_files),
            "python_files": len(python_files),
            "template_files": len(template_files),
            "config_files": len(config_files),
            "all_files": all_files,
            "python_file_names": [f["name"] for f in python_files],
            "template_file_names": [f["path"] for f in template_files],
            "critical_files": critical_files,
            "import_analysis": import_analysis,
            "has_main_py": any(f["name"] == "main.py" for f in python_files),
            "has_routes_py": any(f["name"] == "routes.py" for f in python_files),
            "has_app_py": any(f["name"] == "app.py" for f in python_files),
            "scan_timestamp": str(os.path.getctime(self.project_path))
        }
        
        # Save to memory
        self._save_scan_memory()
        
        return self.scan_results
    
    def _analyze_python_imports(self, python_files: List[Dict]) -> Dict:
        """Analyze import statements in Python files"""
        imports_map = {}
        import_errors = []
        
        for file_info in python_files:
            try:
                with open(file_info["full_path"], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Extract import statements
                import_lines = []
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith(('import ', 'from ')):
                        import_lines.append(line)
                
                # Check for problematic imports
                problems = []
                for imp in import_lines:
                    if 'from main import' in imp and 'routes.py' in [f["name"] for f in python_files]:
                        problems.append(f"Importing from 'main' but routes.py exists")
                    if 'Bootstrap5' in imp:
                        problems.append(f"Using Bootstrap5 (should be Bootstrap)")
                    if 'bp' in imp and 'main_bp' not in imp and 'routes.py' in [f["name"] for f in python_files]:
                        problems.append(f"Importing 'bp' but should be 'main_bp'")
                
                imports_map[file_info["name"]] = {
                    "imports": import_lines,
                    "problems": problems,
                    "line_count": len(content.split('\n'))
                }
                
                if problems:
                    import_errors.extend(problems)
                    
            except Exception as e:
                imports_map[file_info["name"]] = {
                    "error": str(e),
                    "imports": [],
                    "problems": []
                }
        
        return {
            "imports_by_file": imports_map,
            "total_errors": len(import_errors),
            "errors": import_errors[:10]  # Top 10 errors
        }
    
    def _detect_critical_files(self, python_files: List[Dict]) -> Dict:
        """Detect which critical files actually exist"""
        critical_files_list = [
            "config.py", "extensions.py", "models.py", 
            "routes.py", "app.py", "__init__.py"
        ]
        
        templates_list = [
            "templates/index.html", "templates/login.html",
            "templates/base.html", "templates/layout.html"
        ]
        
        existing = {}
        missing = {}
        
        # Check Python files
        for critical_file in critical_files_list:
            exists = any(f["name"] == critical_file for f in python_files)
            existing[critical_file] = exists
            if not exists:
                missing[critical_file] = "MISSING"
        
        # Check template files
        templates_path = self.project_path / "templates"
        if templates_path.exists():
            for template in templates_list:
                template_name = template.split('/')[-1]
                template_exists = (templates_path / template_name).exists()
                existing[template] = template_exists
                if not template_exists:
                    missing[template] = "MISSING"
        else:
            existing["templates/"] = False
            missing["templates/"] = "TEMPLATES DIRECTORY MISSING"
        
        return {
            "existing": {k: v for k, v in existing.items() if v},
            "missing": missing,
            "critical_count": len([v for v in existing.values() if v]),
            "missing_count": len(missing)
        }
    
    def get_file_recommendations(self) -> List[str]:
        """Generate intelligent recommendations based on scan"""
        recommendations = []
        
        if not self.scan_results:
            self.scan_project_files()
        
        crit = self.scan_results.get("critical_files", {})
        
        # Missing files recommendations
        for missing_file, reason in crit.get("missing", {}).items():
            recommendations.append(f"CREATE: {missing_file} ({reason})")
        
        # Import fix recommendations
        for error in self.scan_results.get("import_analysis", {}).get("errors", []):
            recommendations.append(f"FIX IMPORT: {error}")
        
        # Blueprint confusion detection
        has_main = self.scan_results.get("has_main_py", False)
        has_routes = self.scan_results.get("has_routes_py", False)
        
        if has_routes and not has_main:
            recommendations.append("USE: routes.py (main.py doesn't exist)")
        elif has_main and not has_routes:
            recommendations.append("USE: main.py (routes.py doesn't exist)")
        elif has_routes and has_main:
            recommendations.append("CONFLICT: Both main.py and routes.py exist - PREFER routes.py")
        
        # Template issues
        if not self.scan_results.get("template_files", 0):
            recommendations.append("WARNING: No HTML templates found")
        
        return recommendations
    
    def validate_before_generation(self, target_file: str) -> Tuple[bool, str]:
        """
        Validate if we should generate a file or use existing
        Returns: (should_generate, reason)
        """
        if not self.scan_results:
            self.scan_project_files()
        
        # If file already exists
        for file_info in self.scan_results.get("all_files", []):
            if file_info["name"] == target_file or file_info["path"] == target_file:
                return (False, f"File already exists: {file_info['path']}")
        
        # Special cases
        if target_file == "main.py" and self.scan_results.get("has_routes_py", False):
            return (False, "routes.py already exists - use routes.py instead of main.py")
        
        if target_file == "routes.py" and self.scan_results.get("has_main_py", False):
            return (False, "main.py already exists - use main.py instead of routes.py")
        
        return (True, "File can be generated")
    
    def _save_scan_memory(self):
        """Save scan results to memory file"""
        try:
            with open(self.memory_file, 'w', encoding='utf-8') as f:
                json.dump(self.scan_results, f, indent=2, default=str)
        except:
            pass
    
    def get_previous_scan(self):
        """Load previous scan results"""
        if self.memory_file.exists():
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

# Quick utility function for Agent 50
def get_project_file_awareness(project_name: str) -> Dict:
    """Quick scan for Agent 50 integration"""
    scanner = SupremeFileAwareness(project_name)
    return scanner.scan_project_files()

def should_use_main_or_routes(project_name: str) -> str:
    """Intelligent decision: main.py or routes.py?"""
    scanner = SupremeFileAwareness(project_name)
    scan = scanner.scan_project_files()
    
    has_main = scan.get("has_main_py", False)
    has_routes = scan.get("has_routes_py", False)
    
    if has_routes:
        return "routes"  # Prefer routes.py
    elif has_main:
        return "main"    # Use main.py if routes doesn't exist
    else:
        return "routes"  # Default to routes.py

def get_actual_python_files(project_name: str) -> List[str]:
    """Get actual Python files that exist (not hallucinations)"""
    scanner = SupremeFileAwareness(project_name)
    scan = scanner.scan_project_files()
    return scan.get("python_file_names", [])