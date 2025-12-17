"""
AGENT 50 SUPREME - LLM Constraint Enforcer
Forces LLM to follow file awareness rules and prevents hallucinations
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
import ast
import hashlib

# FIX: Import the standalone function needed for file checking
try:
    from file_awareness import get_actual_python_files, SupremeFileAwareness
except ImportError:
    # Fallback to prevent crash if file missing
    def get_actual_python_files(p): return []
    class SupremeFileAwareness:
        def __init__(self, p): pass

class LLMConstraintEnforcer:
    """
    ULTIMATE CONSTRAINT ENGINE FOR LLM
    Ensures LLM never hallucinates, always follows file awareness
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.constraint_rules = self._load_constraint_rules()
        self.violation_history = []
        
        # Import file awareness system
        self.file_awareness = SupremeFileAwareness(project_name)
        
        print(f"[CONSTRAINT] LLM Constraint Enforcer initialized for {project_name}")
    
    def _load_constraint_rules(self) -> Dict:
        """Load constraint rules from file or defaults"""
        rules_file = self.project_path / ".constraint_rules.json"
        if rules_file.exists():
            try:
                with open(rules_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default constraint rules
        return {
            "enforce_file_existence": True,
            "prevent_hallucination": True,
            "enforce_import_rules": True,
            "validate_structure": True,
            "strict_mode": True,
            "auto_correction": True
        }
    
    def enforce_on_prompt(self, prompt: str, phase: str) -> Tuple[str, List[str]]:
        """
        Enforce constraints on PROMPT before sending to LLM
        Returns: (modified_prompt, warnings)
        """
        warnings = []
        modified_prompt = prompt
        
        # Add file awareness context
        if self.constraint_rules.get("enforce_file_existence", True):
            modified_prompt = self._add_file_awareness_context(modified_prompt)
        
        # Add specific constraints based on phase
        phase_constraints = self._get_phase_constraints(phase)
        if phase_constraints:
            modified_prompt = self._add_phase_constraints(modified_prompt, phase_constraints)
        
        # Add recent violation warnings
        recent_violations = self._get_recent_violations()
        if recent_violations and self.constraint_rules.get("strict_mode", True):
            modified_prompt = self._add_violation_warnings(modified_prompt, recent_violations)
            warnings.append(f"Added {len(recent_violations)} violation warnings")
        
        return modified_prompt, warnings
    
    def enforce_on_response(self, filename: str, response: str) -> Tuple[str, List[str], List[str]]:
        """
        Enforce constraints on LLM RESPONSE before saving
        Returns: (corrected_response, violations, corrections)
        """
        violations = []
        corrections = []
        corrected_response = response
        
        print(f"[CONSTRAINT] Enforcing constraints on {filename}...")
        
        # ========== RULE 1: NO HALLUCINATED FILES ==========
        if self.constraint_rules.get("prevent_hallucination", True):
            file_violations, file_corrections = self._enforce_no_hallucination(
                filename, corrected_response
            )
            violations.extend(file_violations)
            corrections.extend(file_corrections)
        
        # ========== RULE 2: VALID IMPORTS ONLY ==========
        if self.constraint_rules.get("enforce_import_rules", True):
            import_violations, import_corrections = self._enforce_valid_imports(
                filename, corrected_response
            )
            violations.extend(import_violations)
            corrections.extend(import_corrections)
        
        # ========== RULE 3: STRUCTURAL CONSISTENCY ==========
        if self.constraint_rules.get("validate_structure", True):
            struct_violations, struct_corrections = self._enforce_structural_consistency(
                filename, corrected_response
            )
            violations.extend(struct_violations)
            corrections.extend(struct_corrections)
        
        # ========== RULE 4: FOLLOW PROJECT PATTERNS ==========
        pattern_violations, pattern_corrections = self._enforce_project_patterns(
            filename, corrected_response
        )
        violations.extend(pattern_violations)
        corrections.extend(pattern_corrections)
        
        # ========== AUTO-CORRECTION ==========
        if violations and self.constraint_rules.get("auto_correction", True):
            auto_corrected = self._auto_correct_violations(
                filename, corrected_response, violations
            )
            if auto_corrected != corrected_response:
                corrected_response = auto_corrected
                corrections.append("Auto-corrected constraint violations")
        
        # Record violations
        if violations:
            self._record_violations(filename, violations)
        
        return corrected_response, violations, corrections
    
    def _enforce_no_hallucination(self, filename: str, content: str) -> Tuple[List[str], List[str]]:
        """Enforce: No hallucinated/non-existent files"""
        violations = []
        corrections = []
        
        # FIX APPLIED HERE: Use standalone function instead of missing class method
        try:
            actual_files = get_actual_python_files(self.project_name)
        except:
            actual_files = []
        
        # Pattern to find imports of local files
        import_patterns = [
            r'from\s+(\w+)\s+import',
            r'import\s+(\w+)',
            r'from\s+(\w+)\.'
        ]
        
        for pattern in import_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                imported_module = match.group(1)
                
                # Skip standard library and known packages
                if imported_module in ['os', 'sys', 'json', 're', 'flask', 'datetime', 'math', 'random', 'time']:
                    continue
                
                # Check if this is a local file that should exist
                possible_files = [
                    f"{imported_module}.py",
                    f"{imported_module}/__init__.py",
                    imported_module
                ]
                
                file_exists = False
                for possible_file in possible_files:
                    if (self.project_path / possible_file).exists():
                        file_exists = True
                        break
                
                if not file_exists and imported_module not in actual_files:
                    violation_msg = f"HALLUCINATION: Imports non-existent module '{imported_module}'"
                    violations.append(violation_msg)
                    
                    # Suggest correction
                    if imported_module == 'app' and filename != 'app.py':
                        # Common hallucination: from app import ...
                        corrections.append(f"Replace 'from app import' with actual module")
        
        return violations, corrections
    
    def _enforce_valid_imports(self, filename: str, content: str) -> Tuple[List[str], List[str]]:
        """Enforce: Valid imports only (no Bootstrap5, etc.)"""
        violations = []
        corrections = []
        
        # Common invalid imports
        invalid_imports = [
            ("Bootstrap5", "Bootstrap", "flask-bootstrap4 has only Bootstrap class"),
            ("flask_login", "session auth", "flask-login not installed, use session auth"),
            ("bp", "main_bp", "Blueprint should be named main_bp not bp"),
        ]
        
        for wrong, correct, reason in invalid_imports:
            if wrong in content:
                violation_msg = f"INVALID IMPORT: {wrong} → {correct} ({reason})"
                violations.append(violation_msg)
                
                # Auto-correction
                if wrong == "Bootstrap5":
                    content = content.replace("Bootstrap5", "Bootstrap")
                    corrections.append("Fixed Bootstrap5 → Bootstrap")
                elif wrong == "bp" and "main_bp" not in content:
                    # Don't correct if main_bp already present
                    content = content.replace("bp = Blueprint", "main_bp = Blueprint")
                    content = content.replace("from routes import bp", "from routes import main_bp")
                    corrections.append("Fixed bp → main_bp")
        
        return violations, corrections
    
    def _enforce_structural_consistency(self, filename: str, content: str) -> Tuple[List[str], List[str]]:
        """Enforce: Structural consistency with project"""
        violations = []
        corrections = []
        
        # Check for Application Factory Pattern compliance
        if filename == "app.py":
            # Must use create_app() pattern
            if "def create_app" not in content and "app = Flask" in content:
                violations.append("STRUCTURE: app.py should use create_app() pattern, not global app")
                
            # Must import from extensions, not create new instances
            if "db = SQLAlchemy()" in content and "from extensions import db" not in content:
                violations.append("STRUCTURE: app.py should import db from extensions.py")
        
        # Check for proper blueprint usage
        if filename == "routes.py":
            if "bp = Blueprint" in content:
                violations.append("STRUCTURE: Use main_bp not bp for blueprint")
            if "/auth/login" in content:
                violations.append("STRUCTURE: Use simple URLs (/login) not /auth/login")
        
        return violations, corrections
    
    def _enforce_project_patterns(self, filename: str, content: str) -> Tuple[List[str], List[str]]:
        """Enforce: Follow established project patterns"""
        violations = []
        corrections = []
        
        # Load project patterns if they exist
        patterns_file = self.project_path / ".project_patterns.json"
        if patterns_file.exists():
            try:
                with open(patterns_file, 'r') as f:
                    patterns = json.load(f)
                
                for pattern_name, pattern_data in patterns.items():
                    pattern = pattern_data.get("pattern", "")
                    required = pattern_data.get("required", False)
                    message = pattern_data.get("message", "")
                    
                    if required and pattern not in content:
                        violations.append(f"PATTERN: Missing required pattern: {message}")
            except:
                pass
        
        # Default patterns for Agent 50
        default_patterns = [
            ("app.py", "if __name__ == '__main__':", "Missing app runner block"),
            ("extensions.py", "db = SQLAlchemy()", "Missing db initialization"),
            ("config.py", "SECRET_KEY =", "Missing SECRET_KEY"),
            ("config.py", "SQLALCHEMY_DATABASE_URI =", "Missing database URI"),
        ]
        
        for pattern_file, pattern, message in default_patterns:
            if filename == pattern_file and pattern not in content:
                violations.append(f"DEFAULT PATTERN: {message}")
        
        return violations, corrections
    
    def _auto_correct_violations(self, filename: str, content: str, violations: List[str]) -> str:
        """Automatically correct common violations"""
        corrected_content = content
        
        for violation in violations:
            if "Bootstrap5" in violation:
                corrected_content = corrected_content.replace("Bootstrap5", "Bootstrap")
            if "bp = Blueprint" in violation and "main_bp" not in corrected_content:
                corrected_content = corrected_content.replace("bp = Blueprint", "main_bp = Blueprint")
                corrected_content = corrected_content.replace("@bp.route", "@main_bp.route")
            if "from app import" in violation and filename != "app.py":
                # Try to guess correct import
                if "db" in violation:
                    corrected_content = corrected_content.replace("from app import db", "from extensions import db")
                if "User" in violation:
                    corrected_content = corrected_content.replace("from app import User", "from models import User")
        
        return corrected_content
    
    def _add_file_awareness_context(self, prompt: str) -> str:
        """Add file awareness context to prompt"""
        
        # FIX APPLIED HERE: Use standalone function
        try:
            actual_files = get_actual_python_files(self.project_name)
        except:
            actual_files = []
        
        if actual_files:
            context = f"\n\n=== FILE AWARENESS CONTEXT ===\n"
            context += f"ACTUAL EXISTING FILES: {', '.join(actual_files)}\n"
            context += "CRITICAL RULES:\n"
            context += "1. NEVER hallucinate non-existent files\n"
            context += "2. NEVER write 'from app import ...' (flat structure)\n"
            context += "3. ALWAYS use existing modules from above list\n"
            context += "4. Use 'Bootstrap' NOT 'Bootstrap5'\n"
            context += "5. Use 'main_bp' NOT 'bp' for blueprint\n"
            
            return prompt + context
        
        return prompt
    
    def _get_phase_constraints(self, phase: str) -> Dict:
        """Get constraints specific to current phase"""
        phase_constraints = {
            "GENERATE": {
                "title": "GENERATION PHASE CONSTRAINTS",
                "rules": [
                    "Generate ONLY the requested file",
                    "Follow EXACT file structure shown in context",
                    "Use imports ONLY from existing files",
                    "Implement Application Factory Pattern",
                    "Use simple URLs (/login, /orders)"
                ]
            },
            "FRONTEND_WEB": {
                "title": "FRONTEND PHASE CONSTRAINTS", 
                "rules": [
                    "Use Bootstrap 5 classes",
                    "Make responsive design",
                    "Connect to backend API endpoints",
                    "Use proper form submissions",
                    "Include navigation"
                ]
            },
            "QA_LOOP": {
                "title": "QA & HEALING PHASE CONSTRAINTS",
                "rules": [
                    "Fix SPECIFIC errors mentioned",
                    "Maintain existing patterns",
                    "Don't break working functionality",
                    "Test changes locally",
                    "Keep fixes minimal and focused"
                ]
            }
        }
        
        return phase_constraints.get(phase, {})
    
    def _add_phase_constraints(self, prompt: str, constraints: Dict) -> str:
        """Add phase-specific constraints to prompt"""
        constraint_text = f"\n\n=== {constraints['title']} ===\n"
        for i, rule in enumerate(constraints.get('rules', []), 1):
            constraint_text += f"{i}. {rule}\n"
        
        return prompt + constraint_text
    
    def _get_recent_violations(self) -> List[str]:
        """Get recent constraint violations"""
        recent = []
        for violation in self.violation_history[-5:]:  # Last 5 violations
            recent.append(f"{violation.get('filename')}: {violation.get('violation', '')[:50]}")
        return recent
    
    def _add_violation_warnings(self, prompt: str, violations: List[str]) -> str:
        """Add warnings about recent violations"""
        warning_text = "\n\n=== RECENT VIOLATION WARNINGS ===\n"
        warning_text += "These violations were recently caught:\n"
        for i, violation in enumerate(violations, 1):
            warning_text += f"{i}. {violation}\n"
        warning_text += "\nDO NOT REPEAT THESE MISTAKES!\n"
        
        return prompt + warning_text
    
    def _record_violations(self, filename: str, violations: List[str]):
        """Record constraint violations"""
        for violation in violations:
            violation_record = {
                "filename": filename,
                "violation": violation,
                "timestamp": str(Path(__file__).stat().st_mtime),
                "project": self.project_name
            }
            self.violation_history.append(violation_record)
        
        # Save to file (keep last 50)
        history_file = self.project_path / ".constraint_violations.json"
        if len(self.violation_history) > 50:
            self.violation_history = self.violation_history[-50:]
        
        try:
            with open(history_file, 'w') as f:
                json.dump(self.violation_history, f, indent=2)
        except:
            pass
    
    def generate_constraint_report(self) -> str:
        """Generate constraint enforcement report"""
        total_violations = len(self.violation_history)
        recent_violations = len([v for v in self.violation_history[-10:]])  # Last 10
        
        report = f"""
╔═══════════════════════════════════════════════════╗
║           LLM CONSTRAINT ENFORCEMENT             ║
║           Project: {self.project_name:30} ║
╚═══════════════════════════════════════════════════╝

ENFORCEMENT STATISTICS:
  Total Violations: {total_violations}
  Recent Violations (last 10): {recent_violations}
  Strict Mode: {'ON' if self.constraint_rules.get('strict_mode') else 'OFF'}
  Auto-Correction: {'ON' if self.constraint_rules.get('auto_correction') else 'OFF'}

ACTIVE CONSTRAINTS:
  1. Prevent Hallucination: {'✓' if self.constraint_rules.get('prevent_hallucination') else '✗'}
  2. Enforce Import Rules: {'✓' if self.constraint_rules.get('enforce_import_rules') else '✗'}
  3. Validate Structure: {'✓' if self.constraint_rules.get('validate_structure') else '✗'}

RECENT VIOLATIONS:
"""
        if self.violation_history:
            for violation in self.violation_history[-5:]:
                report += f"  • {violation.get('filename')}: {violation.get('violation', '')[:60]}...\n"
        else:
            report += "  No violations recorded. Perfect compliance! 🎯\n"
        
        return report


# Global enforcer cache
_enforcer_cache = {}

def get_constraint_enforcer(project_name: str) -> LLMConstraintEnforcer:
    """Get or create constraint enforcer for project"""
    if project_name not in _enforcer_cache:
        _enforcer_cache[project_name] = LLMConstraintEnforcer(project_name)
    return _enforcer_cache[project_name]

def enforce_llm_constraints(project_name: str, filename: str, response: str) -> Tuple[str, List[str], List[str]]:
    """Quick enforcement function"""
    enforcer = get_constraint_enforcer(project_name)
    return enforcer.enforce_on_response(filename, response)

def enforce_prompt_constraints(project_name: str, prompt: str, phase: str) -> Tuple[str, List[str]]:
    """Enforce constraints on prompt"""
    enforcer = get_constraint_enforcer(project_name)
    return enforcer.enforce_on_prompt(prompt, phase)