"""
STRUCTURAL MAPPER - Agent 50 Supreme Level
Analyzes and enforces file dependencies, prevents circular imports,
ensures structural integrity of generated projects.
"""

import os
import re
import ast
import json
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any, DefaultDict
from collections import defaultdict, deque
import networkx as nx
import matplotlib.pyplot as plt

class StructuralMapper:
    """
    ULTIMATE Dependency Analysis System for Agent 50
    Maps and enforces structural dependencies between all project files.
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.dependency_graph = nx.DiGraph()  # Directed graph for dependencies
        self.circular_deps = []
        self.missing_deps = []
        self.structural_issues = []
        self.dependency_map_file = self.project_path / ".dependency_map.json"
        
        # Known dependency patterns for Flask projects
        self.known_dependency_patterns = {
            "app.py": {
                "imports_from": ["extensions.py", "config.py", "routes.py"],
                "exports_to": [],
                "must_contain": ["create_app", "app = create_app()"],
                "prohibited_imports": ["from app import"]
            },
            "extensions.py": {
                "imports_from": [],  # Only imports from packages
                "exports_to": ["app.py", "models.py", "routes.py"],
                "must_contain": ["db = SQLAlchemy()", "migrate = Migrate()", "bootstrap = Bootstrap()"],
                "prohibited_imports": ["from app import", "from routes import", "from models import"]
            },
            "models.py": {
                "imports_from": ["extensions.py"],
                "exports_to": ["routes.py"],
                "must_contain": ["from extensions import db", "class User", "class Order"],
                "prohibited_imports": ["from app import", "from routes import"]
            },
            "routes.py": {
                "imports_from": ["extensions.py", "models.py"],
                "exports_to": ["app.py"],
                "must_contain": ["main_bp = Blueprint", "@main_bp.route"],
                "prohibited_imports": ["from app import"]
            },
            "config.py": {
                "imports_from": [],
                "exports_to": ["app.py"],
                "must_contain": ["SECRET_KEY", "SQLALCHEMY_DATABASE_URI"],
                "prohibited_imports": []
            }
        }
    
    def analyze_project_structure(self) -> Dict:
        """
        MAIN ANALYSIS FUNCTION
        Analyzes entire project structure and returns dependency analysis.
        """
        print(f"  [STRUCTURE] Analyzing project structure for {self.project_name}...")
        
        # Reset analysis data
        self.dependency_graph.clear()
        self.circular_deps = []
        self.missing_deps = []
        self.structural_issues = []
        
        # Get all Python files
        python_files = list(self.project_path.glob("*.py"))
        
        if not python_files:
            return {"error": "No Python files found in project"}
        
        # Add all files as nodes
        for py_file in python_files:
            self.dependency_graph.add_node(py_file.name)
        
        # Analyze each file
        file_analyses = {}
        for py_file in python_files:
            analysis = self._analyze_file(py_file)
            file_analyses[py_file.name] = analysis
            
            # Add dependencies to graph
            for dep in analysis.get("dependencies", []):
                if dep in [f.name for f in python_files]:
                    self.dependency_graph.add_edge(py_file.name, dep)
        
        # Run structural checks
        self._detect_circular_dependencies()
        self._detect_missing_dependencies(file_analyses)
        self._validate_structural_patterns(file_analyses)
        
        # Generate dependency report
        report = self._generate_structural_report(file_analyses)
        
        # Save analysis
        self._save_dependency_map(file_analyses)
        
        return {
            "total_files": len(python_files),
            "file_analyses": file_analyses,
            "circular_dependencies": self.circular_deps,
            "missing_dependencies": self.missing_deps,
            "structural_issues": self.structural_issues,
            "dependency_graph": self._get_graph_summary(),
            "report": report
        }
    
    def _analyze_file(self, file_path: Path) -> Dict:
        """
        Analyze a single Python file for dependencies and structure.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = file_path.name
            
            # Parse AST for accurate analysis
            try:
                tree = ast.parse(content)
            except SyntaxError:
                # If syntax error, fall back to regex analysis
                return self._regex_analyze_file(filename, content)
            
            # Extract imports using AST
            imports = []
            imported_modules = []
            imported_entities = defaultdict(list)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(f"import {alias.name}")
                        imported_modules.append(alias.name)
                        imported_entities[alias.name].append("*")
                
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    level = node.level
                    
                    # Convert relative imports to absolute
                    if level > 0:
                        # Handle relative imports
                        rel_path = self._resolve_relative_import(module, level, file_path)
                        imports.append(f"from {rel_path} import {[alias.name for alias in node.names]}")
                        imported_modules.append(rel_path)
                        for alias in node.names:
                            imported_entities[rel_path].append(alias.name)
                    else:
                        imports.append(f"from {module} import {[alias.name for alias in node.names]}")
                        imported_modules.append(module)
                        for alias in node.names:
                            imported_entities[module].append(alias.name)
            
            # Extract defined functions and classes
            defined_entities = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    defined_entities.append(f"function:{node.name}")
                elif isinstance(node, ast.ClassDef):
                    defined_entities.append(f"class:{node.name}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            defined_entities.append(f"variable:{target.id}")
            
            # Check for known patterns
            pattern_violations = []
            if filename in self.known_dependency_patterns:
                patterns = self.known_dependency_patterns[filename]
                
                # Check must_contain patterns
                for required in patterns.get("must_contain", []):
                    if required not in content:
                        pattern_violations.append(f"Missing required: {required}")
                
                # Check prohibited imports
                for prohibited in patterns.get("prohibited_imports", []):
                    if prohibited in content:
                        pattern_violations.append(f"Prohibited import: {prohibited}")
            
            # Extract local file dependencies (not packages)
            local_deps = []
            package_deps = []
            
            for imp in imported_modules:
                # Check if it's a local file
                if self._is_local_module(imp, file_path):
                    local_deps.append(imp)
                else:
                    package_deps.append(imp)
            
            # Check if imported local files exist
            missing_local_deps = []
            for dep in local_deps:
                dep_path = self._resolve_dependency_path(dep, file_path)
                if not dep_path.exists():
                    missing_local_deps.append(dep)
            
            return {
                "filename": filename,
                "imports": imports,
                "imported_modules": imported_modules,
                "imported_entities": dict(imported_entities),
                "defined_entities": defined_entities,
                "local_dependencies": local_deps,
                "package_dependencies": package_deps,
                "missing_dependencies": missing_local_deps,
                "pattern_violations": pattern_violations,
                "line_count": len(content.split('\n')),
                "has_syntax_errors": False
            }
            
        except Exception as e:
            return {
                "filename": file_path.name,
                "error": str(e),
                "imports": [],
                "imported_modules": [],
                "local_dependencies": [],
                "package_dependencies": [],
                "missing_dependencies": [],
                "pattern_violations": [],
                "has_syntax_errors": True
            }
    
    def _regex_analyze_file(self, filename: str, content: str) -> Dict:
        """
        Fallback regex analysis when AST parsing fails.
        """
        imports = []
        imported_modules = []
        
        # Regex patterns for imports
        import_pattern = r'^import\s+([^\s#]+)'
        from_import_pattern = r'^from\s+([^\s#]+)\s+import'
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            
            # Match import statements
            import_match = re.match(import_pattern, line)
            if import_match:
                module = import_match.group(1)
                imports.append(f"import {module}")
                imported_modules.append(module)
            
            # Match from ... import statements
            from_match = re.match(from_import_pattern, line)
            if from_match:
                module = from_match.group(1)
                imports.append(f"from {module} import ...")
                imported_modules.append(module)
        
        # Determine local vs package dependencies
        local_deps = []
        package_deps = []
        
        for imp in imported_modules:
            if self._is_local_module_by_name(imp):
                local_deps.append(imp)
            else:
                package_deps.append(imp)
        
        return {
            "filename": filename,
            "imports": imports,
            "imported_modules": imported_modules,
            "imported_entities": {},
            "defined_entities": [],
            "local_dependencies": local_deps,
            "package_dependencies": package_deps,
            "missing_dependencies": [],
            "pattern_violations": [],
            "line_count": len(lines),
            "has_syntax_errors": False
        }
    
    def _resolve_relative_import(self, module: str, level: int, file_path: Path) -> str:
        """
        Resolve relative imports to absolute paths.
        """
        if level == 0:
            return module
        
        # Start from the directory containing the file
        current_dir = file_path.parent
        
        # Go up 'level' directories
        for _ in range(level - 1):
            current_dir = current_dir.parent
        
        # If module is empty, it's a relative import of the package
        if not module:
            return str(current_dir.relative_to(self.project_path)).replace('/', '.')
        
        # Otherwise, combine the path with the module
        return str((current_dir / module.replace('.', '/')).relative_to(self.project_path)).replace('/', '.')
    
    def _is_local_module(self, module: str, file_path: Path) -> bool:
        """
        Check if a module is a local project file (not a package).
        """
        # Skip standard library and known packages
        standard_packages = [
            'os', 'sys', 'json', 're', 'datetime', 'time', 'typing',
            'flask', 'flask_sqlalchemy', 'flask_migrate', 'flask_bootstrap',
            'requests', 'sqlalchemy', 'werkzeug'
        ]
        
        if module in standard_packages or any(module.startswith(pkg) for pkg in standard_packages):
            return False
        
        # Check if it's a .py file in the project
        possible_paths = [
            self.project_path / f"{module}.py",
            self.project_path / module.replace('.', '/') / "__init__.py",
            file_path.parent / f"{module}.py"
        ]
        
        return any(p.exists() for p in possible_paths)
    
    def _is_local_module_by_name(self, module: str) -> bool:
        """
        Simplified check for local module by name only.
        """
        # Common packages that are definitely not local
        non_local = [
            'os', 'sys', 'json', 're', 'datetime', 'flask', 'requests',
            'sqlalchemy', 'werkzeug', 'typing', 'pathlib', 'subprocess',
            'hashlib', 'ast', 'networkx', 'matplotlib'
        ]
        
        if module in non_local or any(module.startswith(f"{pkg}.") for pkg in non_local):
            return False
        
        # If it's short and doesn't look like a package, assume local
        if '.' not in module and len(module) < 20 and module.isidentifier():
            return True
        
        return False
    
    def _resolve_dependency_path(self, module: str, file_path: Path) -> Path:
        """
        Resolve a module name to a file path.
        """
        # Try different possible paths
        possible_paths = [
            self.project_path / f"{module}.py",
            self.project_path / module.replace('.', '/') / "__init__.py",
            self.project_path / module.replace('.', '/') / ".py",
            file_path.parent / f"{module}.py",
            file_path.parent / module.replace('.', '/') / "__init__.py"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        
        # Return the most likely path (even if it doesn't exist)
        return self.project_path / f"{module}.py"
    
    def _detect_circular_dependencies(self):
        """
        Detect circular dependencies in the project.
        """
        try:
            # Find cycles in the dependency graph
            cycles = list(nx.simple_cycles(self.dependency_graph))
            
            for cycle in cycles:
                if len(cycle) > 1:  # Only report meaningful cycles
                    self.circular_deps.append({
                        "cycle": cycle,
                        "description": f"Circular dependency: {' -> '.join(cycle)} -> {cycle[0]}"
                    })
        except Exception as e:
            self.circular_deps.append({
                "error": f"Cycle detection failed: {e}",
                "cycle": []
            })
    
    def _detect_missing_dependencies(self, file_analyses: Dict):
        """
        Detect missing dependencies that are imported but don't exist.
        """
        for filename, analysis in file_analyses.items():
            missing_deps = analysis.get("missing_dependencies", [])
            if missing_deps:
                self.missing_deps.append({
                    "file": filename,
                    "missing": missing_deps,
                    "description": f"{filename} imports non-existent files: {', '.join(missing_deps)}"
                })
    
    def _validate_structural_patterns(self, file_analyses: Dict):
        """
        Validate files against known structural patterns.
        """
        for filename, analysis in file_analyses.items():
            if filename in self.known_dependency_patterns:
                patterns = self.known_dependency_patterns[filename]
                
                # Check import sources
                allowed_imports = patterns.get("imports_from", [])
                local_deps = analysis.get("local_dependencies", [])
                
                for dep in local_deps:
                    dep_name = dep.split('.')[0] if '.' in dep else dep
                    if allowed_imports and dep_name not in allowed_imports:
                        self.structural_issues.append({
                            "file": filename,
                            "issue": f"Imports from {dep_name} but should only import from: {', '.join(allowed_imports)}",
                            "severity": "WARNING"
                        })
                
                # Check pattern violations
                violations = analysis.get("pattern_violations", [])
                for violation in violations:
                    self.structural_issues.append({
                        "file": filename,
                        "issue": violation,
                        "severity": "ERROR"
                    })
    
    def _generate_structural_report(self, file_analyses: Dict) -> str:
        """
        Generate a comprehensive structural report.
        """
        report = f"""
╔═══════════════════════════════════════════════════════╗
║           AGENT 50 STRUCTURAL ANALYSIS               ║
║           Project: {self.project_name:30} ║
╚═══════════════════════════════════════════════════════╝

📁 PROJECT OVERVIEW:
  • Total Files Analyzed: {len(file_analyses)}
  • Circular Dependencies: {len(self.circular_deps)}
  • Missing Dependencies: {len(self.missing_deps)}
  • Structural Issues: {len(self.structural_issues)}

🔍 DEPENDENCY GRAPH SUMMARY:
"""
        
        # Add graph statistics
        if len(self.dependency_graph.nodes()) > 0:
            report += f"  • Nodes (Files): {len(self.dependency_graph.nodes())}\n"
            report += f"  • Edges (Dependencies): {len(self.dependency_graph.edges())}\n"
            
            # Calculate in/out degrees
            if self.dependency_graph.nodes():
                avg_out_degree = sum(dict(self.dependency_graph.out_degree()).values()) / len(self.dependency_graph.nodes())
                report += f"  • Average Dependencies per File: {avg_out_degree:.1f}\n"
        
        # Critical issues section
        if self.circular_deps or self.missing_deps:
            report += "\n⚠️ CRITICAL ISSUES:\n"
            
            for circ in self.circular_deps:
                report += f"  • {circ.get('description', 'Circular dependency')}\n"
            
            for missing in self.missing_deps:
                report += f"  • {missing.get('description', 'Missing dependency')}\n"
        
        # File-by-file analysis
        report += "\n📄 FILE ANALYSIS:\n"
        
        for filename, analysis in file_analyses.items():
            if analysis.get("has_syntax_errors", False):
                report += f"  • {filename}: ⚠️ SYNTAX ERRORS\n"
                continue
            
            local_deps = analysis.get("local_dependencies", [])
            package_deps = analysis.get("package_dependencies", [])
            violations = analysis.get("pattern_violations", [])
            
            report += f"  • {filename}:\n"
            report += f"      Dependencies: {len(local_deps)} local, {len(package_deps)} packages\n"
            
            if local_deps:
                report += f"      Local: {', '.join(local_deps[:3])}"
                if len(local_deps) > 3:
                    report += f" (+{len(local_deps)-3} more)"
                report += "\n"
            
            if violations:
                report += f"      Issues: {len(violations)} pattern violations\n"
        
        # Recommendations
        report += "\n🎯 RECOMMENDATIONS:\n"
        
        if self.circular_deps:
            report += "  1. Break circular dependencies by refactoring\n"
        
        if self.missing_deps:
            report += "  2. Create missing files or fix import statements\n"
        
        if self.structural_issues:
            report += "  3. Fix structural pattern violations\n"
        
        if not (self.circular_deps or self.missing_deps or self.structural_issues):
            report += "  ✅ Project structure is clean! No issues found.\n"
        
        report += f"\n📅 Analysis completed at: {self._get_timestamp()}\n"
        
        return report
    
    def _get_graph_summary(self) -> Dict:
        """
        Get summary statistics of the dependency graph.
        """
        if len(self.dependency_graph.nodes()) == 0:
            return {"nodes": 0, "edges": 0, "density": 0}
        
        return {
            "nodes": len(self.dependency_graph.nodes()),
            "edges": len(self.dependency_graph.edges()),
            "density": nx.density(self.dependency_graph),
            "is_dag": nx.is_directed_acyclic_graph(self.dependency_graph),
            "connected_components": nx.number_weakly_connected_components(self.dependency_graph)
        }
    
    def _save_dependency_map(self, file_analyses: Dict):
        """
        Save dependency analysis to file.
        """
        save_data = {
            "project": self.project_name,
            "timestamp": self._get_timestamp(),
            "file_analyses": file_analyses,
            "circular_dependencies": self.circular_deps,
            "missing_dependencies": self.missing_deps,
            "structural_issues": self.structural_issues,
            "graph_summary": self._get_graph_summary()
        }
        
        try:
            with open(self.dependency_map_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, default=str)
        except Exception as e:
            print(f"  [WARN] Failed to save dependency map: {e}")
    
    def _get_timestamp(self) -> str:
        """
        Get current timestamp for reports.
        """
        import datetime
        return datetime.datetime.now().isoformat()
    
    def get_recommended_fixes(self) -> List[Dict]:
        """
        Get recommended fixes for structural issues.
        """
        fixes = []
        
        # Fix for circular dependencies
        for circ in self.circular_deps:
            cycle = circ.get("cycle", [])
            if len(cycle) >= 2:
                fixes.append({
                    "type": "CIRCULAR_DEPENDENCY",
                    "files": cycle,
                    "fix": f"Break cycle by moving common code from {cycle[0]} to a new file",
                    "priority": "HIGH"
                })
        
        # Fix for missing dependencies
        for missing in self.missing_deps:
            file = missing.get("file", "")
            missing_list = missing.get("missing", [])
            
            for dep in missing_list:
                fixes.append({
                    "type": "MISSING_DEPENDENCY",
                    "file": file,
                    "missing": dep,
                    "fix": f"Create {dep}.py or fix import statement in {file}",
                    "priority": "HIGH"
                })
        
        # Fix for structural issues
        for issue in self.structural_issues:
            file = issue.get("file", "")
            issue_desc = issue.get("issue", "")
            
            fixes.append({
                "type": "STRUCTURAL_ISSUE",
                "file": file,
                "issue": issue_desc,
                "fix": f"Fix structural issue in {file}: {issue_desc}",
                "priority": "MEDIUM"
            })
        
        return fixes
    
    def enforce_dependency_rules(self, filename: str, content: str) -> Tuple[bool, List[str], str]:
        """
        Enforce dependency rules BEFORE file is saved.
        Returns: (is_valid, warnings, fixed_content)
        """
        warnings = []
        fixed_content = content
        
        if filename not in self.known_dependency_patterns:
            return True, warnings, fixed_content
        
        patterns = self.known_dependency_patterns[filename]
        
        # Check prohibited imports
        for prohibited in patterns.get("prohibited_imports", []):
            if prohibited in content:
                warnings.append(f"Prohibited import pattern: {prohibited}")
                # Auto-remove or comment out
                fixed_content = fixed_content.replace(prohibited, f"# {prohibited}  # AUTO-REMOVED: prohibited import")
        
        # Check if importing from allowed sources
        # Extract imports from content
        import_lines = []
        lines = content.split('\n')
        for line in lines:
            if line.strip().startswith(('from ', 'import ')):
                import_lines.append(line.strip())
        
        allowed_imports = patterns.get("imports_from", [])
        for imp_line in import_lines:
            # Check if it's importing from a local file
            for allowed in allowed_imports:
                if allowed and f"from {allowed}" in imp_line:
                    break
            else:
                # Not importing from allowed source
                if 'from ' in imp_line and not any(pkg in imp_line for pkg in ['flask', 'os', 'sys', 'json']):
                    imported_module = imp_line.split('from ')[1].split(' import')[0].strip()
                    if imported_module and '.' not in imported_module:  # Likely local file
                        warnings.append(f"Importing from {imported_module} but should only import from: {', '.join(allowed_imports)}")
        
        return len(warnings) == 0, warnings, fixed_content
    
    def visualize_dependencies(self, save_path: Optional[Path] = None):
        """
        Generate visualization of dependency graph.
        """
        if len(self.dependency_graph.nodes()) == 0:
            return None
        
        try:
            plt.figure(figsize=(12, 8))
            
            # Use spring layout
            pos = nx.spring_layout(self.dependency_graph, k=2, iterations=50)
            
            # Draw nodes
            nx.draw_networkx_nodes(self.dependency_graph, pos, node_size=2000, 
                                 node_color='lightblue', alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(self.dependency_graph, pos, alpha=0.5, 
                                 edge_color='gray', arrowsize=20)
            
            # Draw labels
            nx.draw_networkx_labels(self.dependency_graph, pos, font_size=10, 
                                  font_weight='bold')
            
            plt.title(f"Dependency Graph: {self.project_name}", fontsize=16)
            plt.axis('off')
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                plt.close()
                return str(save_path)
            else:
                plt.tight_layout()
                return plt
            
        except Exception as e:
            print(f"  [WARN] Failed to visualize dependencies: {e}")
            return None


# Global mapper instance cache
_mapper_cache = {}

def get_structural_mapper(project_name: str) -> StructuralMapper:
    """Get or create structural mapper for project"""
    if project_name not in _mapper_cache:
        _mapper_cache[project_name] = StructuralMapper(project_name)
    return _mapper_cache[project_name]

def analyze_project_structure(project_name: str) -> Dict:
    """Quick analysis function for Agent 50 integration"""
    mapper = get_structural_mapper(project_name)
    return mapper.analyze_project_structure()

def enforce_dependency_rules(project_name: str, filename: str, content: str) -> Tuple[bool, List[str], str]:
    """Quick dependency enforcement for Agent 50 integration"""
    mapper = get_structural_mapper(project_name)
    return mapper.enforce_dependency_rules(filename, content)