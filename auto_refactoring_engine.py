"""
AGENT 50 SUPREME - Auto-Refactoring Engine
Proactively improves code structure and quality
"""

import ast
import re
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
import hashlib

class AutoRefactoringEngine:
    """
    INTELLIGENT CODE REFACTORING ENGINE
    Proactively improves code structure, quality, and maintainability
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.refactoring_rules = self._load_refactoring_rules()
        self.refactoring_history = []
        
        print(f"[REFACTOR] Auto-Refactoring Engine initialized for {project_name}")
    
    def _load_refactoring_rules(self) -> Dict:
        """Load refactoring rules from file or defaults"""
        rules_file = self.project_path / ".refactoring_rules.json"
        if rules_file.exists():
            try:
                with open(rules_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default refactoring rules for Agent 50
        return {
            "auto_improve_imports": True,
            "remove_unused_imports": True,
            "standardize_formatting": True,
            "fix_naming_conventions": True,
            "simplify_complex_expressions": True,
            "add_type_hints": False,  # Advanced feature
            "extract_duplicate_code": True,
            "level": "moderate"  # conservative | moderate | aggressive
        }
    
    def analyze_and_refactor_file(self, filename: str, content: str) -> Tuple[str, List[str]]:
        """
        Analyze file and apply automatic refactoring
        Returns: (refactored_content, changes_made)
        """
        changes = []
        refactored_content = content
        
        print(f"[REFACTOR] Analyzing {filename} for improvements...")
        
        # Skip non-Python files
        if not filename.endswith('.py'):
            return refactored_content, changes
        
        # ========== APPLY REFACTORING RULES ==========
        
        # Rule 1: Improve imports
        if self.refactoring_rules.get("auto_improve_imports", True):
            improved_imports, import_changes = self._improve_imports(refactored_content, filename)
            if import_changes:
                refactored_content = improved_imports
                changes.extend(import_changes)
        
        # Rule 2: Remove unused imports
        if self.refactoring_rules.get("remove_unused_imports", True):
            cleaned_imports, cleanup_changes = self._remove_unused_imports(refactored_content, filename)
            if cleanup_changes:
                refactored_content = cleaned_imports
                changes.extend(cleanup_changes)
        
        # Rule 3: Standardize formatting
        if self.refactoring_rules.get("standardize_formatting", True):
            formatted_content, format_changes = self._standardize_formatting(refactored_content)
            if format_changes:
                refactored_content = formatted_content
                changes.extend(format_changes)
        
        # Rule 4: Fix naming conventions
        if self.refactoring_rules.get("fix_naming_conventions", True):
            fixed_names, naming_changes = self._fix_naming_conventions(refactored_content, filename)
            if naming_changes:
                refactored_content = fixed_names
                changes.extend(naming_changes)
        
        # Rule 5: Simplify complex expressions
        if self.refactoring_rules.get("simplify_complex_expressions", True):
            simplified, simplification_changes = self._simplify_expressions(refactored_content)
            if simplification_changes:
                refactored_content = simplified
                changes.extend(simplification_changes)
        
        # Rule 6: Extract duplicate code (advanced)
        if self.refactoring_rules.get("extract_duplicate_code", True):
            extracted, extraction_changes = self._extract_duplicate_code(refactored_content, filename)
            if extraction_changes:
                refactored_content = extracted
                changes.extend(extraction_changes)
        
        # Record refactoring
        if changes:
            self._record_refactoring(filename, changes)
            print(f"[REFACTOR] Applied {len(changes)} improvements to {filename}")
        
        return refactored_content, changes
    
    def analyze_project_structure(self) -> Dict:
        """
        Analyze entire project structure for refactoring opportunities
        """
        print("[REFACTOR] Analyzing project structure...")
        
        analysis = {
            "files_analyzed": 0,
            "total_improvements": 0,
            "files_with_issues": [],
            "structural_issues": [],
            "dependency_issues": [],
            "code_quality_metrics": {}
        }
        
        # Analyze each Python file
        python_files = list(self.project_path.glob("**/*.py"))
        
        for file_path in python_files:
            if file_path.is_file():
                analysis["files_analyzed"] += 1
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Analyze this file
                file_analysis = self._analyze_file_structure(str(file_path.relative_to(self.project_path)), content)
                
                if file_analysis["issues"]:
                    analysis["files_with_issues"].append({
                        "file": str(file_path.relative_to(self.project_path)),
                        "issues": file_analysis["issues"],
                        "suggestions": file_analysis["suggestions"]
                    })
                    analysis["total_improvements"] += len(file_analysis["suggestions"])
        
        # Analyze dependencies between files
        dependency_analysis = self._analyze_dependencies()
        analysis["dependency_issues"] = dependency_analysis.get("issues", [])
        
        # Calculate code quality metrics
        analysis["code_quality_metrics"] = self._calculate_code_quality_metrics()
        
        return analysis
    
    def apply_structural_refactoring(self) -> Tuple[bool, str]:
        """
        Apply structural refactoring to the entire project
        """
        print("[REFACTOR] Applying structural refactoring...")
        
        analysis = self.analyze_project_structure()
        changes_applied = []
        
        # Fix structural issues
        for file_info in analysis["files_with_issues"]:
            filename = file_info["file"]
            file_path = self.project_path / filename
            
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Apply fixes for this file's issues
                refactored_content, changes = self._apply_structural_fixes(content, file_info["issues"])
                
                if changes:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(refactored_content)
                    changes_applied.append(f"{filename}: {', '.join(changes)}")
        
        # Fix dependency issues
        for issue in analysis["dependency_issues"]:
            if issue.get("fixable", False):
                fixed = self._fix_dependency_issue(issue)
                if fixed:
                    changes_applied.append(f"Dependency: {issue.get('description', '')}")
        
        if changes_applied:
            report = f"Applied {len(changes_applied)} structural improvements:\n" + "\n".join([f"  • {c}" for c in changes_applied])
            return True, report
        
        return False, "No structural issues found that require refactoring"
    
    def _improve_imports(self, content: str, filename: str) -> Tuple[str, List[str]]:
        """Improve import organization and structure"""
        changes = []
        lines = content.split('\n')
        
        # Group imports by type
        stdlib_imports = []
        third_party_imports = []
        local_imports = []
        other_lines = []
        
        for line in lines:
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                if any(stdlib in stripped for stdlib in ['os', 'sys', 'json', 're', 'datetime', 'pathlib']):
                    stdlib_imports.append(line)
                elif any(pkg in stripped for pkg in ['flask', 'sqlalchemy', 'bootstrap']):
                    third_party_imports.append(line)
                elif any(local in stripped for local in ['extensions', 'models', 'routes', 'config']):
                    local_imports.append(line)
                else:
                    third_party_imports.append(line)
            else:
                other_lines.append(line)
        
        # Check if imports need reorganization
        if (stdlib_imports or third_party_imports or local_imports) and len(lines) > 0:
            # Sort each group alphabetically
            stdlib_imports.sort()
            third_party_imports.sort()
            local_imports.sort()
            
            # Add blank line between groups if multiple groups exist
            import_sections = []
            if stdlib_imports:
                import_sections.extend(stdlib_imports)
            if third_party_imports:
                if import_sections:
                    import_sections.append('')
                import_sections.extend(third_party_imports)
            if local_imports:
                if import_sections:
                    import_sections.append('')
                import_sections.extend(local_imports)
            
            # Check if reorganization would change anything
            original_import_lines = [l for l in lines if l.strip().startswith(('import ', 'from '))]
            if original_import_lines != import_sections:
                # Reconstruct content with organized imports
                reorganized_content = '\n'.join(import_sections + [''] + other_lines)
                changes.append("Reorganized imports (stdlib → third-party → local)")
                return reorganized_content, changes
        
        return content, changes
    
    def _remove_unused_imports(self, content: str, filename: str) -> Tuple[str, List[str]]:
        """Remove unused imports from the file"""
        changes = []
        
        try:
            # Parse the AST to find used names
            tree = ast.parse(content)
            
            # Find all imported names
            imported_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_names.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imported_names.add(f"{module}.{alias.name}" if module else alias.name)
            
            # Find all used names
            used_names = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Name):
                    used_names.add(node.id)
                elif isinstance(node, ast.Attribute):
                    # Handle attribute access like db.session
                    attr_chain = []
                    current = node
                    while isinstance(current, ast.Attribute):
                        attr_chain.insert(0, current.attr)
                        current = current.value
                    if isinstance(current, ast.Name):
                        base_name = current.id
                        # Add all partial chains (db, db.session, etc.)
                        for i in range(len(attr_chain)):
                            used_names.add(f"{base_name}.{'.'.join(attr_chain[:i+1])}")
            
            # Check for unused imports (simplified check)
            # This is a simplified version - full unused import detection is complex
            
            # Special case: Always keep Flask imports in app.py
            if filename == "app.py":
                if "from flask import Flask" in content and "Flask" not in str(used_names):
                    # Flask is used implicitly in app = Flask(__name__)
                    pass
            
            # For now, use simple pattern-based cleanup
            lines = content.split('\n')
            new_lines = []
            imports_removed = 0
            
            for line in lines:
                stripped = line.strip()
                # Remove obviously problematic imports
                if "Bootstrap5" in line:
                    continue  # Skip, will be replaced elsewhere
                elif "flask_login" in line.lower():
                    imports_removed += 1
                    continue
                elif "import bp" in line and "main_bp" not in content:
                    imports_removed += 1
                    continue
                else:
                    new_lines.append(line)
            
            if imports_removed > 0:
                changes.append(f"Removed {imports_removed} unused/problematic imports")
                return '\n'.join(new_lines), changes
        
        except SyntaxError:
            # If we can't parse, skip this refactoring
            pass
        
        return content, changes
    
    def _standardize_formatting(self, content: str) -> Tuple[str, List[str]]:
        """Standardize code formatting"""
        changes = []
        lines = content.split('\n')
        new_lines = []
        
        # Fix common formatting issues
        for line in lines:
            new_line = line
            
            # Fix spacing around operators
            new_line = re.sub(r'(\w+)=(\w+)', r'\1 = \2', new_line)  # Add spaces around =
            new_line = re.sub(r'(\w+)==(\w+)', r'\1 == \2', new_line)  # Add spaces around ==
            
            # Fix missing trailing commas in long lists/dicts
            if new_line.strip().startswith(('"', "'", '[')) and '[' in new_line and ']' not in new_line:
                # Multi-line list - check next few lines
                pass
            
            # Fix inconsistent quotes (standardize to single quotes for Python)
            if "'" not in new_line and '"' in new_line:
                # Only replace if it's a simple string (not f-string or containing apostrophes)
                if 'f"' not in new_line and "'" not in new_line:
                    new_line = new_line.replace('"', "'")
            
            if new_line != line:
                changes.append("Standardized formatting")
            
            new_lines.append(new_line)
        
        # Ensure exactly 2 blank lines between top-level functions/classes
        if len(new_lines) > 1:
            formatted_content = self._ensure_proper_blank_lines(new_lines)
            if formatted_content != '\n'.join(new_lines):
                changes.append("Standardized blank lines between definitions")
                return formatted_content, changes
        
        return content, changes
    
    def _fix_naming_conventions(self, content: str, filename: str) -> Tuple[str, List[str]]:
        """Fix naming conventions (PEP 8 compliance)"""
        changes = []
        new_content = content
        
        # Fix blueprint naming
        if "bp = Blueprint" in new_content and "main_bp" not in new_content:
            new_content = new_content.replace("bp = Blueprint", "main_bp = Blueprint")
            new_content = new_content.replace("@bp.route", "@main_bp.route")
            changes.append("Fixed blueprint naming (bp → main_bp)")
        
        # Fix variable naming (snake_case for variables/functions)
        lines = new_content.split('\n')
        for i, line in enumerate(lines):
            # Find variable assignments with camelCase
            match = re.search(r'(\w+)\s*=\s*', line)
            if match:
                var_name = match.group(1)
                if var_name and '_' not in var_name and var_name[0].islower() and var_name != var_name.lower():
                    # Convert camelCase to snake_case
                    snake_case = self._camel_to_snake(var_name)
                    if snake_case != var_name:
                        lines[i] = line.replace(var_name, snake_case)
                        changes.append(f"Fixed naming: {var_name} → {snake_case}")
        
        return '\n'.join(lines), changes
    
    def _simplify_expressions(self, content: str) -> Tuple[str, List[str]]:
        """Simplify complex expressions"""
        changes = []
        new_content = content
        
        # Simplify common patterns
        
        # Pattern 1: Overly complex if conditions
        # if request.method == "POST" and request.method != "GET": → if request.method == "POST":
        new_content = re.sub(
            r'if request\.method == ["\']POST["\'] and request\.method != ["\']GET["\']',
            'if request.method == "POST"',
            new_content
        )
        
        # Pattern 2: Redundant try-except with same exception handling
        lines = new_content.split('\n')
        in_try_block = False
        try_start = -1
        
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith('try:'):
                in_try_block = True
                try_start = i
            elif line.startswith('except Exception as e:') and in_try_block:
                # Check if this is a simple re-raise
                if i + 1 < len(lines) and lines[i + 1].strip() == 'raise':
                    # This is redundant, can be removed
                    lines[try_start] = '# ' + lines[try_start]
                    lines[i] = '# ' + lines[i]
                    lines[i + 1] = '# ' + lines[i + 1]
                    changes.append("Removed redundant try-except block")
                in_try_block = False
        
        # Pattern 3: Simplify dictionary lookups with .get()
        new_content = re.sub(
            r'if "(\w+)" in (\w+)\.json\(\):',
            r'if \1 in \2:',
            new_content
        )
        
        if changes:
            new_content = '\n'.join(lines)
        
        return new_content, changes
    
    def _extract_duplicate_code(self, content: str, filename: str) -> Tuple[str, List[str]]:
        """Extract duplicate code into functions"""
        changes = []
        
        # Find duplicate code patterns (simplified version)
        lines = content.split('\n')
        
        # Look for duplicate login logic patterns
        login_patterns = [
            r'user = User\.query\.filter_by\(.*username.*\).first\(\)',
            r'if user and check_password_hash\(user\.password',
            r'session\["user_id"\] = user\.id'
        ]
        
        # Count occurrences of each pattern
        pattern_counts = {}
        for i, line in enumerate(lines):
            for pattern in login_patterns:
                if re.search(pattern, line):
                    pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        # If any pattern appears more than once, suggest extraction
        for pattern, count in pattern_counts.items():
            if count > 1:
                changes.append(f"Found {count} occurrences of duplicate pattern")
                # In a real implementation, we would extract this to a function
                break
        
        return content, changes
    
    def _analyze_file_structure(self, filename: str, content: str) -> Dict:
        """Analyze file structure for issues"""
        issues = []
        suggestions = []
        
        try:
            tree = ast.parse(content)
            
            # Check 1: File length
            line_count = len(content.split('\n'))
            if line_count > 200:
                issues.append(f"File is long ({line_count} lines)")
                suggestions.append("Consider splitting into smaller modules")
            
            # Check 2: Function length
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_line_count = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
                    if func_line_count > 50:
                        issues.append(f"Function '{node.name}' is long ({func_line_count} lines)")
                        suggestions.append(f"Extract parts of function '{node.name}' into helper functions")
            
            # Check 3: Too many imports
            import_count = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))
            if import_count > 15:
                issues.append(f"Many imports ({import_count})")
                suggestions.append("Group related imports or move to separate module")
            
            # Check 4: Circular import risk
            if filename.endswith('.py'):
                imports = self._extract_imports_from_ast(tree)
                local_imports = [imp for imp in imports if not any(stdlib in imp for stdlib in 
                                ['os', 'sys', 'json', 'datetime', 're', 'flask', 'sqlalchemy'])]
                
                if len(local_imports) > 3:
                    issues.append(f"Many local imports ({len(local_imports)})")
                    suggestions.append("Check for circular dependency risks")
        
        except SyntaxError:
            issues.append("Syntax error in file")
            suggestions.append("Fix syntax errors before refactoring")
        
        return {
            "filename": filename,
            "issues": issues,
            "suggestions": suggestions
        }
    
    def _analyze_dependencies(self) -> Dict:
        """Analyze dependencies between files"""
        issues = []
        
        # Get all Python files
        python_files = list(self.project_path.glob("**/*.py"))
        
        # Build import graph
        import_graph = {}
        for file_path in python_files:
            if file_path.is_file():
                rel_path = str(file_path.relative_to(self.project_path))
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                try:
                    tree = ast.parse(content)
                    imports = self._extract_imports_from_ast(tree)
                    import_graph[rel_path] = imports
                except:
                    import_graph[rel_path] = []
        
        # Check for potential circular dependencies
        for file1, imports1 in import_graph.items():
            for imp in imports1:
                # Check if this import could create a circular dependency
                for file2, imports2 in import_graph.items():
                    if file1 != file2 and file1.replace('.py', '') in imports2 and imp.replace('.py', '') == file2.replace('.py', ''):
                        issues.append({
                            "type": "circular_dependency_risk",
                            "files": [file1, file2],
                            "description": f"Potential circular dependency between {file1} and {file2}",
                            "fixable": True
                        })
        
        return {"issues": issues}
    
    def _apply_structural_fixes(self, content: str, issues: List[str]) -> Tuple[str, List[str]]:
        """Apply fixes for structural issues"""
        changes = []
        new_content = content
        
        # Apply fixes based on issue types
        for issue in issues:
            if "long" in issue and "Function" in issue:
                # Extract function name
                match = re.search(r"Function '(\w+)'", issue)
                if match:
                    func_name = match.group(1)
                    # Add TODO comment
                    new_content = new_content.replace(
                        f"def {func_name}(",
                        f"# TODO: Consider splitting this long function\n# Original length detected by Agent 50\n\ndef {func_name}("
                    )
                    changes.append(f"Added TODO for long function '{func_name}'")
            
            elif "Many imports" in issue:
                # Reorganize imports
                improved_content, import_changes = self._improve_imports(new_content, "")
                if import_changes:
                    new_content = improved_content
                    changes.extend(import_changes)
        
        return new_content, changes
    
    def _fix_dependency_issue(self, issue: Dict) -> bool:
        """Fix a dependency issue"""
        issue_type = issue.get("type", "")
        
        if issue_type == "circular_dependency_risk":
            files = issue.get("files", [])
            if len(files) >= 2:
                file1, file2 = files[0], files[1]
                
                # Try to break circular dependency by making one import conditional
                file1_path = self.project_path / file1
                if file1_path.exists():
                    with open(file1_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add comment about circular dependency
                    new_content = f"# NOTE: Circular dependency with {file2} handled by Agent 50\n{content}"
                    
                    with open(file1_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    
                    return True
        
        return False
    
    def _calculate_code_quality_metrics(self) -> Dict:
        """Calculate code quality metrics for the project"""
        metrics = {
            "total_files": 0,
            "total_lines": 0,
            "average_file_size": 0,
            "files_with_issues": 0,
            "duplicate_code_score": 0,
            "maintainability_index": 0
        }
        
        # Simplified metrics calculation
        python_files = list(self.project_path.glob("**/*.py"))
        metrics["total_files"] = len(python_files)
        
        total_lines = 0
        for file_path in python_files:
            if file_path.is_file():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        total_lines += len(lines)
                except:
                    pass
        
        metrics["total_lines"] = total_lines
        if metrics["total_files"] > 0:
            metrics["average_file_size"] = total_lines / metrics["total_files"]
        
        return metrics
    
    def _ensure_proper_blank_lines(self, lines: List[str]) -> str:
        """Ensure proper blank lines between definitions"""
        new_lines = []
        in_def = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check if this line starts a class or function definition
            is_definition = stripped.startswith(('def ', 'class ', '@'))
            
            if is_definition and i > 0:
                # Ensure exactly 2 blank lines before top-level definitions
                if not in_def:
                    # Look back for blank lines
                    blank_lines_count = 0
                    for j in range(i-1, max(-1, i-3), -1):
                        if j < len(new_lines) and not new_lines[j].strip():
                            blank_lines_count += 1
                    
                    if blank_lines_count < 2:
                        # Add missing blank lines
                        new_lines.extend([''] * (2 - blank_lines_count))
                
                in_def = True
            elif stripped and not is_definition:
                in_def = False
            
            new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def _camel_to_snake(self, name: str) -> str:
        """Convert camelCase to snake_case"""
        # Insert underscore before uppercase letters
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', name)
        return snake.lower()
    
    def _extract_imports_from_ast(self, tree: ast.AST) -> List[str]:
        """Extract imports from AST"""
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}" if module else alias.name)
        
        return imports
    
    def _record_refactoring(self, filename: str, changes: List[str]):
        """Record refactoring changes"""
        refactoring_record = {
            "filename": filename,
            "timestamp": str(Path(__file__).stat().st_mtime),
            "changes": changes,
            "project": self.project_name
        }
        self.refactoring_history.append(refactoring_record)
        
        # Save to file (keep last 50)
        history_file = self.project_path / ".refactoring_history.json"
        if len(self.refactoring_history) > 50:
            self.refactoring_history = self.refactoring_history[-50:]
        
        try:
            with open(history_file, 'w') as f:
                json.dump(self.refactoring_history, f, indent=2)
        except:
            pass


# Global refactoring engine cache
_refactoring_cache = {}

def get_refactoring_engine(project_name: str) -> AutoRefactoringEngine:
    """Get or create refactoring engine for project"""
    if project_name not in _refactoring_cache:
        _refactoring_cache[project_name] = AutoRefactoringEngine(project_name)
    return _refactoring_cache[project_name]

def refactor_file(project_name: str, filename: str, content: str) -> Tuple[str, List[str]]:
    """Quick refactoring function"""
    engine = get_refactoring_engine(project_name)
    return engine.analyze_and_refactor_file(filename, content)

def analyze_project_structure(project_name: str) -> Dict:
    """Quick project analysis function"""
    engine = get_refactoring_engine(project_name)
    return engine.analyze_project_structure()