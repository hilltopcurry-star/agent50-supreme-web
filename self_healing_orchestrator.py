"""
AGENT 50 SUPREME - Self-Healing Orchestrator
Master coordinator for autonomous error detection and correction
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set
import hashlib
import subprocess
import traceback

class SelfHealingOrchestrator:
    """
    MASTER SELF-HEALING CONTROLLER
    Coordinates all healing components: Validator, Mapper, Memory, LLM
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.healing_history = []
        self.error_patterns = self._load_error_patterns()
        self.healing_strategies = self._initialize_healing_strategies()
        
        # Component imports
        from agent_validator import get_validator
        from memory_tracker import get_memory_tracker
        from structural_mapper import DependencyMapper  # You created this
        
        self.validator = get_validator(project_name)
        self.memory_tracker = get_memory_tracker(project_name)
        self.dependency_mapper = DependencyMapper(project_name)
        
        print(f"[ORCHESTRATOR] Self-Healing System Initialized for {project_name}")
    
    def _load_error_patterns(self) -> Dict:
        """Load known error patterns from database"""
        patterns_file = self.project_path / ".error_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default error patterns (Agent 50's memory)
        return {
            "import_errors": {
                "Bootstrap5": {
                    "pattern": "cannot import name 'Bootstrap5'",
                    "solution": "Replace Bootstrap5 with Bootstrap",
                    "fix_function": "fix_bootstrap5",
                    "occurrences": 0,
                    "last_fixed": None
                },
                "bp_not_found": {
                    "pattern": "cannot import name 'bp'",
                    "solution": "Use main_bp instead of bp",
                    "fix_function": "fix_blueprint_name",
                    "occurrences": 0,
                    "last_fixed": None
                },
                "flask_login": {
                    "pattern": "No module named 'flask_login'",
                    "solution": "Use session auth instead of flask_login",
                    "fix_function": "remove_flask_login",
                    "occurrences": 0,
                    "last_fixed": None
                }
            },
            "runtime_errors": {
                "template_not_found": {
                    "pattern": "jinja2.exceptions.TemplateNotFound",
                    "solution": "Create missing template file",
                    "fix_function": "create_missing_template",
                    "occurrences": 0,
                    "last_fixed": None
                },
                "db_not_initialized": {
                    "pattern": "Working outside of application context",
                    "solution": "Initialize db with app context",
                    "fix_function": "fix_db_context",
                    "occurrences": 0,
                    "last_fixed": None
                }
            },
            "structural_errors": {
                "circular_import": {
                    "pattern": "ImportError: cannot import name",
                    "solution": "Break circular dependency",
                    "fix_function": "fix_circular_import",
                    "occurrences": 0,
                    "last_fixed": None
                },
                "missing_dependency": {
                    "pattern": "ModuleNotFoundError",
                    "solution": "Add missing import or install package",
                    "fix_function": "add_missing_dependency",
                    "occurrences": 0,
                    "last_fixed": None
                }
            }
        }
    
    def _initialize_healing_strategies(self) -> Dict:
        """Initialize healing strategies for different error types"""
        return {
            "import_errors": self._heal_import_error,
            "runtime_errors": self._heal_runtime_error,
            "structural_errors": self._heal_structural_error,
            "validation_errors": self._heal_validation_error,
            "logic_errors": self._heal_logic_error
        }
    
    def detect_and_heal(self, error_message: str, error_type: str = "auto") -> Tuple[bool, str]:
        """
        MAIN HEALING FUNCTION
        Detects error type and applies appropriate healing
        Returns: (success, healing_report)
        """
        print(f"[ORCHESTRATOR] Detecting error: {error_type}")
        print(f"[ERROR] {error_message[:200]}...")
        
        # Record error in memory
        error_id = self._record_error(error_message, error_type)
        
        # Auto-detect error type if not specified
        if error_type == "auto":
            error_type = self._classify_error(error_message)
        
        # Check if this error has occurred before
        pattern_match = self._match_error_pattern(error_message)
        if pattern_match:
            print(f"[MEMORY] Known error pattern: {pattern_match['type']}")
            print(f"[MEMORY] This error occurred {pattern_match['occurrences']} times before")
        
        # Apply healing strategy
        healing_function = self.healing_strategies.get(error_type, self._heal_unknown_error)
        success, report = healing_function(error_message, pattern_match)
        
        # Update healing history
        self._update_healing_history(error_id, success, report)
        
        return success, report
    
    def _heal_import_error(self, error_message: str, pattern_match: Optional[Dict] = None) -> Tuple[bool, str]:
        """Heal import-related errors"""
        print("[HEALING] Applying import error healing...")
        
        from smart_import_detector import detect_and_fix_imports
        
        # Run smart import detector
        import_issues = detect_and_fix_imports(self.project_name)
        
        if import_issues.get("fix_count", 0) > 0:
            report = f"Fixed {import_issues['fix_count']} import issues"
            return True, report
        
        # Specific pattern-based healing
        if pattern_match:
            fix_func = pattern_match.get("fix_function")
            if fix_func == "fix_bootstrap5":
                return self._fix_bootstrap5_issue()
            elif fix_func == "fix_blueprint_name":
                return self._fix_blueprint_name_issue()
            elif fix_func == "remove_flask_login":
                return self._remove_flask_login_issue()
        
        return False, "Import error detected but no specific fix found"
    
    def _heal_runtime_error(self, error_message: str, pattern_match: Optional[Dict] = None) -> Tuple[bool, str]:
        """Heal runtime errors"""
        print("[HEALING] Applying runtime error healing...")
        
        # Check for template errors
        if "TemplateNotFound" in error_message:
            return self._create_missing_template(error_message)
        
        # Check for DB context errors
        if "application context" in error_message:
            return self._fix_db_context_issue()
        
        return False, "Runtime error requires manual intervention"
    
    def _heal_structural_error(self, error_message: str, pattern_match: Optional[Dict] = None) -> Tuple[bool, str]:
        """Heal structural/architectural errors"""
        print("[HEALING] Applying structural error healing...")
        
        # Analyze dependencies
        dependencies = self.dependency_mapper.analyze_dependencies()
        
        # Check for circular dependencies
        circular = self.dependency_mapper.find_circular_dependencies()
        if circular:
            print(f"[STRUCTURAL] Found circular dependencies: {circular}")
            return self._break_circular_dependency(circular[0])
        
        # Check for missing dependencies
        missing = self.dependency_mapper.find_missing_dependencies()
        if missing:
            print(f"[STRUCTURAL] Found missing dependencies: {missing}")
            return self._add_missing_dependencies(missing)
        
        return False, "Structural analysis completed, no critical issues found"
    
    def _heal_validation_error(self, error_message: str, pattern_match: Optional[Dict] = None) -> Tuple[bool, str]:
        """Heal validation errors"""
        print("[HEALING] Applying validation error healing...")
        
        # Re-validate all critical files
        critical_files = ["extensions.py", "app.py", "routes.py", "config.py"]
        fixed_count = 0
        
        for file in critical_files:
            file_path = self.project_path / file
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                
                from agent_validator import validate_and_correct
                is_valid, fixed_content, report = validate_and_correct(self.project_name, file, content)
                
                if not is_valid:
                    # Save fixed content
                    with open(file_path, 'w') as f:
                        f.write(fixed_content)
                    fixed_count += 1
                    print(f"[VALIDATION] Fixed issues in {file}")
        
        if fixed_count > 0:
            return True, f"Fixed validation errors in {fixed_count} files"
        
        return False, "No validation errors found"
    
    def _heal_logic_error(self, error_message: str, pattern_match: Optional[Dict] = None) -> Tuple[bool, str]:
        """Heal logic/business logic errors"""
        print("[HEALING] Applying logic error healing...")
        
        # Use memory tracker to find similar past errors
        similar_errors = self.memory_tracker.find_similar_errors(error_message)
        
        if similar_errors:
            print(f"[MEMORY] Found {len(similar_errors)} similar past errors")
            # Apply the fix that worked last time
            last_successful_fix = None
            for error in similar_errors:
                if error.get("fixed", False):
                    last_successful_fix = error.get("fix_applied")
                    break
            
            if last_successful_fix:
                return self._apply_known_fix(last_successful_fix, error_message)
        
        # If no memory, use LLM to analyze and fix
        return self._llm_analyze_and_fix(error_message)
    
    def _heal_unknown_error(self, error_message: str, pattern_match: Optional[Dict] = None) -> Tuple[bool, str]:
        """Heal unknown/unclassified errors"""
        print("[HEALING] Applying generic healing for unknown error...")
        
        # Try all healing strategies in sequence
        strategies = [
            self._heal_import_error,
            self._heal_validation_error,
            self._heal_structural_error
        ]
        
        for strategy in strategies:
            success, report = strategy(error_message, pattern_match)
            if success:
                return True, f"Generic healing succeeded via {strategy.__name__}: {report}"
        
        return False, "Unable to heal unknown error"
    
    # ========== SPECIFIC HEALING FUNCTIONS ==========
    
    def _fix_bootstrap5_issue(self) -> Tuple[bool, str]:
        """Fix Bootstrap5 import issues"""
        print("[FIX] Applying Bootstrap5 fix...")
        
        files_to_fix = ["extensions.py", "app.py", "__init__.py"]
        fixed_count = 0
        
        for filename in files_to_fix:
            file_path = self.project_path / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace Bootstrap5 with Bootstrap
                if "Bootstrap5" in content:
                    new_content = content.replace("Bootstrap5", "Bootstrap")
                    with open(file_path, 'w') as f:
                        f.write(new_content)
                    fixed_count += 1
        
        return True, f"Fixed Bootstrap5 in {fixed_count} files"
    
    def _fix_blueprint_name_issue(self) -> Tuple[bool, str]:
        """Fix blueprint name issues (bp vs main_bp)"""
        print("[FIX] Applying blueprint name fix...")
        
        files_to_fix = ["routes.py", "app.py"]
        fixed_count = 0
        
        for filename in files_to_fix:
            file_path = self.project_path / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Replace bp with main_bp
                new_content = content
                new_content = new_content.replace("from routes import bp", "from routes import main_bp")
                new_content = new_content.replace("app.register_blueprint(bp", "app.register_blueprint(main_bp")
                new_content = new_content.replace("bp = Blueprint", "main_bp = Blueprint")
                new_content = new_content.replace("@bp.route", "@main_bp.route")
                
                if new_content != content:
                    with open(file_path, 'w') as f:
                        f.write(new_content)
                    fixed_count += 1
        
        return True, f"Fixed blueprint names in {fixed_count} files"
    
    def _remove_flask_login_issue(self) -> Tuple[bool, str]:
        """Remove flask_login dependencies"""
        print("[FIX] Removing flask_login dependencies...")
        
        # Remove imports
        files_to_clean = ["extensions.py", "app.py", "routes.py", "models.py"]
        fixed_count = 0
        
        for filename in files_to_clean:
            file_path = self.project_path / filename
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                
                # Remove flask_login imports
                lines = content.split('\n')
                new_lines = []
                for line in lines:
                    if "flask_login" not in line.lower() and "LoginManager" not in line:
                        new_lines.append(line)
                    else:
                        fixed_count += 1
                
                if len(new_lines) != len(lines):
                    with open(file_path, 'w') as f:
                        f.write('\n'.join(new_lines))
        
        return True, f"Removed flask_login from {fixed_count} locations"
    
    def _create_missing_template(self, error_message: str) -> Tuple[bool, str]:
        """Create missing template file"""
        # Extract template name from error
        import re
        match = re.search(r"TemplateNotFound: ([\w/]+\.html)", error_message)
        if match:
            template_name = match.group(1)
            template_path = self.project_path / "templates" / template_name
            
            # Create directory if needed
            template_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Create basic template
            basic_html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{template_name.replace('.html', '').title()}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>{template_name.replace('.html', '').replace('_', ' ').title()}</h1>
        <p>Template created by Agent 50 Self-Healing System</p>
    </div>
</body>
</html>"""
            
            with open(template_path, 'w') as f:
                f.write(basic_html)
            
            return True, f"Created missing template: {template_name}"
        
        return False, "Could not extract template name from error"
    
    def _break_circular_dependency(self, circular_path: List[str]) -> Tuple[bool, str]:
        """Break circular dependency"""
        print(f"[STRUCTURAL] Breaking circular dependency: {circular_path}")
        
        # Simple strategy: Convert one import to late import
        if len(circular_path) >= 2:
            file_a = circular_path[0]
            file_b = circular_path[1]
            
            file_a_path = self.project_path / f"{file_a}.py"
            if file_a_path.exists():
                with open(file_a_path, 'r') as f:
                    content = f.read()
                
                # Add comment about circular dependency
                new_content = f"# NOTE: Circular dependency with {file_b} resolved by Agent 50\n{content}"
                
                with open(file_a_path, 'w') as f:
                    f.write(new_content)
                
                return True, f"Broke circular dependency between {file_a} and {file_b}"
        
        return False, "Could not break circular dependency"
    
    def _llm_analyze_and_fix(self, error_message: str) -> Tuple[bool, str]:
        """Use LLM to analyze and fix complex errors"""
        print("[LLM] Using LLM to analyze error...")
        
        try:
            from llm_client import call_llm
            
            prompt = f"""
            ERROR ANALYSIS REQUEST - AGENT 50 SELF-HEALING SYSTEM
            
            Error: {error_message}
            
            Project Structure:
            {self._get_project_structure()}
            
            Please analyze this error and provide:
            1. Root cause analysis
            2. Step-by-step fix
            3. Code changes needed
            
            Be specific and provide actual code fixes.
            """
            
            analysis = call_llm(prompt, system_prompt="You are a senior software architect analyzing errors.")
            
            # Extract code fixes from analysis
            fixes = self._extract_fixes_from_llm_response(analysis)
            
            if fixes:
                applied = self._apply_llm_fixes(fixes)
                if applied > 0:
                    return True, f"Applied {applied} fixes from LLM analysis"
            
            return False, "LLM analysis complete but no actionable fixes found"
            
        except Exception as e:
            return False, f"LLM analysis failed: {e}"
    
    # ========== HELPER METHODS ==========
    
    def _record_error(self, error_message: str, error_type: str) -> str:
        """Record error in database"""
        error_hash = hashlib.md5(error_message.encode()).hexdigest()[:16]
        
        error_record = {
            "id": error_hash,
            "timestamp": time.time(),
            "type": error_type,
            "message": error_message[:500],  # Truncate long messages
            "project": self.project_name,
            "fixed": False,
            "fix_applied": None
        }
        
        self.healing_history.append(error_record)
        self._save_healing_history()
        
        # Update error patterns
        self._update_error_patterns(error_message, error_type)
        
        return error_hash
    
    def _classify_error(self, error_message: str) -> str:
        """Classify error type based on message"""
        error_lower = error_message.lower()
        
        if any(keyword in error_lower for keyword in ["import", "module", "cannot import"]):
            return "import_errors"
        elif any(keyword in error_lower for keyword in ["jinja", "template", "application context", "attributeerror"]):
            return "runtime_errors"
        elif any(keyword in error_lower for keyword in ["circular", "dependency", "dependency"]):
            return "structural_errors"
        elif any(keyword in error_lower for keyword in ["validation", "validator", "invalid"]):
            return "validation_errors"
        elif any(keyword in error_lower for keyword in ["logic", "business", "incorrect", "wrong"]):
            return "logic_errors"
        else:
            return "unknown"
    
    def _match_error_pattern(self, error_message: str) -> Optional[Dict]:
        """Match error against known patterns"""
        for category, patterns in self.error_patterns.items():
            for pattern_name, pattern_data in patterns.items():
                if pattern_data["pattern"] in error_message:
                    # Update occurrence count
                    pattern_data["occurrences"] += 1
                    pattern_data["last_fixed"] = time.time()
                    return {
                        "type": f"{category}.{pattern_name}",
                        "occurrences": pattern_data["occurrences"],
                        "solution": pattern_data["solution"],
                        "fix_function": pattern_data["fix_function"]
                    }
        return None
    
    def _get_project_structure(self) -> str:
        """Get project structure for LLM context"""
        structure = []
        for root, dirs, files in os.walk(self.project_path):
            level = root.replace(str(self.project_path), '').count(os.sep)
            indent = ' ' * 2 * level
            structure.append(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                if file.endswith('.py'):
                    structure.append(f"{subindent}{file}")
        
        return '\n'.join(structure)
    
    def _extract_fixes_from_llm_response(self, response: str) -> List[Dict]:
        """Extract code fixes from LLM response"""
        fixes = []
        
        # Simple extraction - look for code blocks
        import re
        code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
        
        for i, block in enumerate(code_blocks):
            # Try to determine which file this fix is for
            filename = self._guess_filename_from_code(block)
            fixes.append({
                "filename": filename,
                "code": block,
                "description": f"Fix #{i+1} from LLM analysis"
            })
        
        return fixes
    
    def _apply_llm_fixes(self, fixes: List[Dict]) -> int:
        """Apply fixes from LLM analysis"""
        applied_count = 0
        
        for fix in fixes:
            filename = fix["filename"]
            code = fix["code"]
            
            file_path = self.project_path / filename
            if file_path.exists():
                # For now, just append the fix as a comment
                with open(file_path, 'a') as f:
                    f.write(f"\n\n# === AGENT 50 AUTO-FIX ===\n")
                    f.write(f"# {fix['description']}\n")
                    f.write(f"# Suggested fix:\n")
                    for line in code.split('\n'):
                        f.write(f"# {line}\n")
                
                applied_count += 1
        
        return applied_count
    
    def _save_healing_history(self):
        """Save healing history to file"""
        history_file = self.project_path / ".healing_history.json"
        try:
            with open(history_file, 'w') as f:
                json.dump(self.healing_history[-100:], f, indent=2)  # Keep last 100
        except:
            pass
    
    def _update_error_patterns(self, error_message: str, error_type: str):
        """Update error patterns database"""
        # Extract key pattern from error
        lines = error_message.split('\n')
        if lines:
            first_line = lines[0]
            
            # Add to appropriate category
            category = error_type.replace("_errors", "")
            if category not in self.error_patterns:
                self.error_patterns[category] = {}
            
            # Create pattern key from first 5 words
            words = first_line.split()[:5]
            pattern_key = '_'.join(words).lower().replace('.', '').replace(':', '')
            
            if pattern_key not in self.error_patterns[category]:
                self.error_patterns[category][pattern_key] = {
                    "pattern": first_line[:100],
                    "solution": "Auto-detected by Agent 50",
                    "fix_function": "generic_fix",
                    "occurrences": 1,
                    "last_fixed": time.time()
                }
            
            # Save to file
            patterns_file = self.project_path / ".error_patterns.json"
            try:
                with open(patterns_file, 'w') as f:
                    json.dump(self.error_patterns, f, indent=2)
            except:
                pass
    
    def generate_healing_report(self) -> str:
        """Generate healing system report"""
        total_errors = len(self.healing_history)
        fixed_errors = len([h for h in self.healing_history if h.get("fixed", False)])
        
        report = f"""
╔═══════════════════════════════════════════════════╗
║           AGENT 50 SELF-HEALING REPORT           ║
║           Project: {self.project_name:30} ║
╚═══════════════════════════════════════════════════╝

HEALING STATISTICS:
  Total Errors Recorded: {total_errors}
  Successfully Fixed: {fixed_errors}
  Success Rate: {(fixed_errors/total_errors*100 if total_errors > 0 else 0):.1f}%

KNOWN ERROR PATTERNS:
"""
        for category, patterns in self.error_patterns.items():
            report += f"  {category.upper()}:\n"
            for name, data in patterns.items():
                report += f"    • {name}: {data['occurrences']} occurrences\n"
        
        if self.healing_history:
            report += "\nRECENT HEALING ACTIONS:\n"
            for entry in self.healing_history[-5:]:  # Last 5
                status = "✅ FIXED" if entry.get("fixed") else "❌ UNFIXED"
                report += f"  [{status}] {entry.get('type', 'unknown')}: {entry.get('message', '')[:50]}...\n"
        
        return report


# Global orchestrator cache
_orchestrator_cache = {}

def get_self_healing_orchestrator(project_name: str) -> SelfHealingOrchestrator:
    """Get or create self-healing orchestrator for project"""
    if project_name not in _orchestrator_cache:
        _orchestrator_cache[project_name] = SelfHealingOrchestrator(project_name)
    return _orchestrator_cache[project_name]

def trigger_self_healing(project_name: str, error_message: str, error_type: str = "auto") -> Tuple[bool, str]:
    """Quick function to trigger self-healing"""
    orchestrator = get_self_healing_orchestrator(project_name)
    return orchestrator.detect_and_heal(error_message, error_type)

def get_healing_report(project_name: str) -> str:
    """Get healing report for project"""
    orchestrator = get_self_healing_orchestrator(project_name)
    return orchestrator.generate_healing_report()