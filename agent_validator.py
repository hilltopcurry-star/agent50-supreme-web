"""
AGENT 50 SUPREME VALIDATOR
Self-validating, self-correcting validation engine.
Prevents errors BEFORE they are saved to disk.
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
import hashlib

class SupremeValidator:
    """
    ULTIMATE Validation System for Agent 50
    Validates ALL generated code against structural rules BEFORE saving.
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.validation_rules = self._load_validation_rules()
        self.validation_history = []
        
        # Critical file patterns and their required content
        self.critical_file_patterns = {
            "extensions.py": {
                "required_imports": [
                    "from flask_sqlalchemy import SQLAlchemy",
                    "from flask_migrate import Migrate", 
                    "from flask_bootstrap import Bootstrap"
                ],
                "required_variables": ["db", "migrate", "bootstrap"],
                "prohibited_patterns": ["Bootstrap5"],
                "file_type": "extension"
            },
            "config.py": {
                "required_sections": ["SECRET_KEY", "SQLALCHEMY_DATABASE_URI"],
                "prohibited_patterns": ["password123", "secret123"],
                "file_type": "config"
            },
            "app.py": {
                "required_imports_context": True,  # Must match actual imports
                "required_blueprint": "main_bp",
                "prohibited_patterns": ["Bootstrap5", "bp,", "url_prefix='/auth'"],
                "file_type": "app"
            },
            "routes.py": {
                "required_blueprint_declaration": "main_bp = Blueprint",
                "required_login_route": ["/login", "methods=['GET', 'POST']"],
                "prohibited_patterns": ["bp = Blueprint", "/auth/login"],
                "file_type": "routes"
            }
        }
    
    def _load_validation_rules(self) -> Dict:
        """Load validation rules from file or default"""
        rules_file = self.project_path / ".validation_rules.json"
        if rules_file.exists():
            try:
                with open(rules_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default validation rules
        return {
            "strict_import_validation": True,
            "structural_dependency_check": True,
            "proactive_error_prevention": True,
            "auto_correction_level": "aggressive",
            "memory_integration": True
        }
    
    def validate_before_save(self, filename: str, content: str) -> Tuple[bool, str, str]:
        """
        MAIN VALIDATION FUNCTION
        Validates content BEFORE it is saved to disk.
        Returns: (is_valid, corrected_content, validation_report)
        """
        print(f"  [VALIDATOR] Validating {filename} before save...")
        
        validation_errors = []
        corrected_content = content
        validation_warnings = []
        
        # ========== PHASE 1: BASIC SYNTAX VALIDATION ==========
        syntax_valid, syntax_error = self._validate_syntax(content)
        if not syntax_valid:
            validation_errors.append(f"Syntax error: {syntax_error}")
        
        # ========== PHASE 2: FILE-SPECIFIC VALIDATION ==========
        if filename in self.critical_file_patterns:
            file_errors, file_warnings, fixed_content = self._validate_critical_file(
                filename, corrected_content
            )
            validation_errors.extend(file_errors)
            validation_warnings.extend(file_warnings)
            corrected_content = fixed_content
        
        # ========== PHASE 3: STRUCTURAL DEPENDENCY VALIDATION ==========
        if self.validation_rules.get("structural_dependency_check", True):
            struct_errors, struct_warnings = self._validate_structural_dependencies(
                filename, corrected_content
            )
            validation_errors.extend(struct_errors)
            validation_warnings.extend(struct_warnings)
        
        # ========== PHASE 4: IMPORT VALIDATION ==========
        if self.validation_rules.get("strict_import_validation", True):
            import_errors, import_warnings, fixed_imports = self._validate_imports(
                filename, corrected_content
            )
            validation_errors.extend(import_errors)
            validation_warnings.extend(import_warnings)
            corrected_content = fixed_imports
        
        # ========== PHASE 5: PROACTIVE ERROR PREVENTION ==========
        if self.validation_rules.get("proactive_error_prevention", True):
            prevention_errors, prevention_fixes = self._prevent_known_errors(
                filename, corrected_content
            )
            validation_errors.extend(prevention_errors)
            if prevention_fixes:
                corrected_content = prevention_fixes
        
        # ========== PHASE 6: AUTO-CORRECTION ==========
        if corrected_content != content and self._should_auto_correct():
            auto_corrected, correction_report = self._auto_correct(
                filename, corrected_content, validation_errors
            )
            corrected_content = auto_corrected
            validation_warnings.append(f"Auto-corrected: {correction_report}")
        
        # ========== FINAL DECISION ==========
        is_valid = len(validation_errors) == 0
        
        # Build validation report
        validation_report = self._build_validation_report(
            filename, is_valid, validation_errors, validation_warnings, 
            content != corrected_content
        )
        
        # Record validation history
        self._record_validation(
            filename, is_valid, validation_errors, validation_warnings,
            content_hash := hashlib.md5(content.encode()).hexdigest()[:8]
        )
        
        return is_valid, corrected_content, validation_report
    
    def _validate_syntax(self, content: str) -> Tuple[bool, str]:
        """Validate Python syntax"""
        try:
            ast.parse(content)
            return True, ""
        except SyntaxError as e:
            return False, f"Line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def _validate_critical_file(self, filename: str, content: str) -> Tuple[List[str], List[str], str]:
        """Validate critical files against their specific patterns"""
        errors = []
        warnings = []
        corrected_content = content
        
        patterns = self.critical_file_patterns[filename]
        
        # Check prohibited patterns
        for prohibited in patterns.get("prohibited_patterns", []):
            if prohibited in content:
                errors.append(f"Prohibited pattern found: {prohibited}")
                # Auto-correct
                if prohibited == "Bootstrap5":
                    corrected_content = corrected_content.replace("Bootstrap5", "Bootstrap")
                elif prohibited == "bp,":
                    corrected_content = corrected_content.replace("bp,", "main_bp,")
        
        # Check required imports (for extensions.py)
        if filename == "extensions.py":
            required_vars = patterns.get("required_variables", [])
            for var in required_vars:
                if f"{var} =" not in content and f"{var}=" not in content:
                    errors.append(f"Missing required variable: {var}")
                    
                    # Auto-add missing variables
                    if var == "migrate" and "migrate = Migrate()" not in content:
                        if "from flask_migrate import Migrate" not in content:
                            corrected_content = "from flask_migrate import Migrate\n" + corrected_content
                        corrected_content = corrected_content.replace(
                            "db = SQLAlchemy()",
                            "db = SQLAlchemy()\nmigrate = Migrate()"
                        )
                    elif var == "bootstrap" and "bootstrap = Bootstrap()" not in content:
                        if "from flask_bootstrap import Bootstrap" not in content:
                            corrected_content = "from flask_bootstrap import Bootstrap\n" + corrected_content
                        corrected_content = corrected_content.replace(
                            "migrate = Migrate()",
                            "migrate = Migrate()\nbootstrap = Bootstrap()"
                        )
        
        # Check for blueprint declaration
        if filename == "routes.py":
            if "main_bp = Blueprint" not in content and "bp = Blueprint" in content:
                warnings.append("Using 'bp' instead of 'main_bp' - auto-correcting")
                corrected_content = corrected_content.replace("bp = Blueprint", "main_bp = Blueprint")
                corrected_content = corrected_content.replace("@bp.route", "@main_bp.route")
        
        return errors, warnings, corrected_content
    
    def _validate_structural_dependencies(self, filename: str, content: str) -> Tuple[List[str], List[str]]:
        """Validate structural dependencies between files"""
        errors = []
        warnings = []
        
        # Analyze imports in content
        imports = self._extract_imports(content)
        
        for imp in imports:
            # Check if import references local files that exist
            if self._is_local_import(imp):
                imported_file = self._extract_imported_filename(imp)
                if imported_file:
                    imported_path = self.project_path / imported_file
                    if not imported_path.exists():
                        errors.append(f"Imports non-existent file: {imported_file}")
        
        # Special case: app.py importing from extensions.py
        if filename == "app.py" and "from extensions import" in content:
            # Check what extensions.py actually exports
            extensions_path = self.project_path / "extensions.py"
            if extensions_path.exists():
                with open(extensions_path, 'r') as f:
                    extensions_content = f.read()
                
                # Extract what extensions.py actually defines
                defined_vars = self._extract_defined_variables(extensions_content)
                
                # Check if app.py is importing undefined variables
                imported_vars = self._extract_imported_variables(content, "extensions")
                for var in imported_vars:
                    if var not in defined_vars:
                        errors.append(f"app.py imports '{var}' but extensions.py doesn't define it")
        
        return errors, warnings
    
    def _validate_imports(self, filename: str, content: str) -> Tuple[List[str], List[str], str]:
        """Validate and correct import statements"""
        errors = []
        warnings = []
        corrected_content = content
        
        # Common import issues to fix
        import_fixes = [
            ("from flask_bootstrap import Bootstrap5", "from flask_bootstrap import Bootstrap", "Bootstrap5 → Bootstrap"),
            ("from main import bp", "from routes import main_bp", "main.py → routes.py, bp → main_bp"),
            ("from routes import bp", "from routes import main_bp", "bp → main_bp"),
            ("import Bootstrap5", "from flask_bootstrap import Bootstrap", "Bootstrap5 → Bootstrap"),
        ]
        
        for wrong, right, description in import_fixes:
            if wrong in corrected_content:
                warnings.append(f"Import issue: {description}")
                corrected_content = corrected_content.replace(wrong, right)
        
        # Check for flask_login (not installed)
        if "flask_login" in corrected_content.lower():
            warnings.append("flask_login detected - not installed, may cause errors")
        
        return errors, warnings, corrected_content
    
    def _prevent_known_errors(self, filename: str, content: str) -> Tuple[List[str], str]:
        """Prevent known common errors proactively"""
        errors = []
        corrected_content = content
        
        # Known error patterns and their fixes
        error_patterns = [
            # Bootstrap5 errors
            (r'Bootstrap5\(\)', 'Bootstrap()', 'Bootstrap5() constructor'),
            (r'Bootstrap5\(app\)', 'Bootstrap(app)', 'Bootstrap5(app) init'),
            
            # Blueprint registration errors
            (r'app\.register_blueprint\(bp', 'app.register_blueprint(main_bp', 'bp → main_bp registration'),
            (r'url_prefix=[\'"][^\'"]+[\'"]', "url_prefix='/'", 'Custom URL prefix removal'),
            
            # Method specification errors
            (r'@main_bp\.route\(\'/login\'\)', '@main_bp.route(\'/login\', methods=[\'GET\', \'POST\'])', 'Missing HTTP methods'),
            
            # Template rendering errors
            (r'render_template\(\s*\)', 'render_template(\'index.html\')', 'Empty render_template'),
        ]
        
        for pattern, replacement, description in error_patterns:
            if re.search(pattern, corrected_content):
                errors.append(f"Prevented: {description}")
                corrected_content = re.sub(pattern, replacement, corrected_content)
        
        return errors, corrected_content
    
    def _auto_correct(self, filename: str, content: str, errors: List[str]) -> Tuple[str, str]:
        """Apply automatic corrections based on errors"""
        corrected_content = content
        corrections_applied = []
        
        # Apply corrections based on error types
        for error in errors:
            if "Bootstrap5" in error:
                corrected_content = corrected_content.replace("Bootstrap5", "Bootstrap")
                corrections_applied.append("Bootstrap5 → Bootstrap")
            
            if "bp" in error and "main_bp" not in error:
                corrected_content = corrected_content.replace("from routes import bp", "from routes import main_bp")
                corrected_content = corrected_content.replace("app.register_blueprint(bp", "app.register_blueprint(main_bp")
                corrections_applied.append("bp → main_bp")
            
            if "migrate" in error and "not define" in error:
                # Add migrate to extensions.py
                if filename == "extensions.py":
                    corrected_content = corrected_content.replace(
                        "db = SQLAlchemy()",
                        "db = SQLAlchemy()\nmigrate = Migrate()"
                    )
                    corrections_applied.append("Added migrate = Migrate()")
        
        correction_report = ", ".join(corrections_applied) if corrections_applied else "No corrections needed"
        return corrected_content, correction_report
    
    def _should_auto_correct(self) -> bool:
        """Determine if auto-correction should be applied"""
        level = self.validation_rules.get("auto_correction_level", "conservative")
        return level in ["aggressive", "moderate"]
    
    def _build_validation_report(self, filename: str, is_valid: bool, 
                               errors: List[str], warnings: List[str], 
                               was_corrected: bool) -> str:
        """Build a detailed validation report"""
        status = "✅ PASS" if is_valid else "❌ FAIL"
        report = f"""
╔═══════════════════════════════════════════════════╗
║           AGENT 50 VALIDATION REPORT             ║
║           File: {filename:30} ║
╚═══════════════════════════════════════════════════╝

STATUS: {status}
CORRECTED: {'Yes' if was_corrected else 'No'}

ERRORS ({len(errors)}):
"""
        for i, error in enumerate(errors, 1):
            report += f"  {i}. {error}\n"
        
        report += f"\nWARNINGS ({len(warnings)}):\n"
        for i, warning in enumerate(warnings, 1):
            report += f"  {i}. {warning}\n"
        
        if not errors and not warnings:
            report += "\n🎯 PERFECT: No issues found!\n"
        
        return report
    
    def _record_validation(self, filename: str, is_valid: bool, 
                          errors: List[str], warnings: List[str],
                          content_hash: str):
        """Record validation results to history"""
        entry = {
            "filename": filename,
            "timestamp": str(Path(__file__).stat().st_mtime),
            "valid": is_valid,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "content_hash": content_hash,
            "project": self.project_name
        }
        self.validation_history.append(entry)
        
        # Save to file (keep last 100 validations)
        history_file = self.project_path / ".validation_history.json"
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]
        
        try:
            with open(history_file, 'w') as f:
                json.dump(self.validation_history, f, indent=2)
        except:
            pass
    
    # ========== HELPER METHODS ==========
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract all import statements from content"""
        imports = []
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith(('import ', 'from ')):
                imports.append(line)
        return imports
    
    def _is_local_import(self, import_stmt: str) -> bool:
        """Check if import is for a local file"""
        # Skip standard library and known packages
        skip_prefixes = ['os', 'sys', 'json', 're', 'datetime', 'flask', 
                        'requests', 'sqlalchemy', 'werkzeug']
        
        for prefix in skip_prefixes:
            if import_stmt.startswith(f'import {prefix}') or import_stmt.startswith(f'from {prefix}'):
                return False
        
        # Check for .py imports or local module names
        if '.py' in import_stmt or (import_stmt.split()[1] if len(import_stmt.split()) > 1 else '').isidentifier():
            return True
        
        return False
    
    def _extract_imported_filename(self, import_stmt: str) -> Optional[str]:
        """Extract filename from import statement"""
        # from X import Y → X.py
        # import X → X.py
        
        if import_stmt.startswith('from '):
            parts = import_stmt.split()
            if len(parts) >= 2:
                module = parts[1]
                if module.endswith('.py'):
                    return module
                return f"{module}.py"
        elif import_stmt.startswith('import '):
            parts = import_stmt.split()
            if len(parts) >= 2:
                module = parts[1].split('.')[0]
                return f"{module}.py"
        
        return None
    
    def _extract_defined_variables(self, content: str) -> List[str]:
        """Extract variables defined at module level"""
        variables = []
        
        # Simple regex for variable assignments at module level
        pattern = r'^(\w+)\s*='
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                variables.append(match.group(1))
        
        return variables
    
    def _extract_imported_variables(self, content: str, module: str) -> List[str]:
        """Extract variables imported from a specific module"""
        variables = []
        
        pattern = rf'from {module} import (.*)'
        match = re.search(pattern, content)
        if match:
            import_list = match.group(1)
            # Split by commas, handle "as" aliases
            parts = [p.strip() for p in import_list.split(',')]
            for part in parts:
                if ' as ' in part:
                    variable = part.split(' as ')[0].strip()
                else:
                    variable = part.strip()
                variables.append(variable)
        
        return variables
    
    def get_validation_stats(self) -> Dict:
        """Get validation statistics"""
        total = len(self.validation_history)
        passed = len([v for v in self.validation_history if v.get("valid", False)])
        failed = total - passed
        
        return {
            "total_validations": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "most_common_error": self._get_most_common_error()
        }
    
    def _get_most_common_error(self) -> str:
        """Get the most common validation error"""
        # Would need error categorization - simplified for now
        return "Import mismatch"
    
    def enforce_validation_in_phase(self, phase: str) -> bool:
        """Determine if validation should be enforced in a phase"""
        phases_requiring_validation = ["GENERATE", "FRONTEND_WEB", "QA_LOOP"]
        return phase in phases_requiring_validation


# Global validator instance cache
_validator_cache = {}

def get_validator(project_name: str) -> SupremeValidator:
    """Get or create validator for project"""
    if project_name not in _validator_cache:
        _validator_cache[project_name] = SupremeValidator(project_name)
    return _validator_cache[project_name]

def validate_and_correct(project_name: str, filename: str, content: str) -> Tuple[bool, str, str]:
    """Quick validation function for Agent 50 integration"""
    validator = get_validator(project_name)
    return validator.validate_before_save(filename, content)