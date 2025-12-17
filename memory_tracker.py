"""
MEMORY TRACKER - Agent 50 Supreme Level
Remembers past mistakes, prevents repetition, learns from history.
"""

import json
import time
import hashlib
import re
import sys
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple  # <-- CRITICAL IMPORT

class SupremeMemoryTracker:
    """ULTIMATE Memory System for Agent 50 - Learns from Past Mistakes"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.memory_dir = Path("projects") / project_name / ".agent_memory"
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Memory files
        self.error_memory_file = self.memory_dir / "errors.json"
        self.fix_memory_file = self.memory_dir / "fixes.json"
        self.pattern_memory_file = self.memory_dir / "patterns.json"
        self.learning_file = self.memory_dir / "learning.pkl"
        
        # Load existing memories
        self.error_memory = self._load_json(self.error_memory_file, [])
        self.fix_memory = self._load_json(self.fix_memory_file, [])
        self.pattern_memory = self._load_json(self.pattern_memory_file, {})
        self.learned_patterns = self._load_learned_patterns()
        
        # Statistics
        self.stats = {
            "total_errors": len(self.error_memory),
            "unique_errors": len(set(e.get("error_hash", "") for e in self.error_memory)),
            "successful_fixes": len([f for f in self.fix_memory if f.get("success", False)]),
            "prevented_repeats": 0
        }
    
    def _load_json(self, file_path: Path, default):
        """Load JSON file with error handling"""
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return default
    
    def _save_json(self, file_path: Path, data):
        """Save JSON file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, default=str)
            return True
        except:
            return False
    
    def _load_learned_patterns(self) -> Dict:
        """Load machine-learned patterns"""
        try:
            if self.learning_file.exists():
                with open(self.learning_file, 'rb') as f:
                    return pickle.load(f)
        except:
            pass
        return {
            "error_patterns": {},
            "fix_patterns": {},
            "prevention_rules": []
        }
    
    def _save_learned_patterns(self):
        """Save learned patterns"""
        try:
            with open(self.learning_file, 'wb') as f:
                pickle.dump(self.learned_patterns, f)
            return True
        except:
            return False
    
    def record_error(self, error_type: str, error_message: str, 
                    file: str = "", line: int = 0) -> str:
        """
        Record an error with intelligent hashing
        Returns: error_hash
        """
        # Create unique hash for this error
        error_hash = hashlib.md5(
            f"{error_type}:{error_message[:100]}:{file}".encode()
        ).hexdigest()[:12]
        
        # Check if we've seen this before
        seen_before = False
        for existing in self.error_memory:
            if existing.get("error_hash") == error_hash:
                seen_before = True
                existing["count"] = existing.get("count", 0) + 1
                existing["last_seen"] = datetime.now().isoformat()
                break
        
        if not seen_before:
            error_record = {
                "error_hash": error_hash,
                "error_type": error_type,
                "error_message": error_message[:500],
                "file": file,
                "line": line,
                "first_seen": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "count": 1,
                "project": self.project_name,
                "environment": {
                    "python": sys.version,
                    "platform": sys.platform
                }
            }
            self.error_memory.append(error_record)
        
        # Update pattern memory
        self._update_pattern_memory(error_type, error_message, error_hash)
        
        # Save
        self._save_json(self.error_memory_file, self.error_memory)
        self.stats["total_errors"] = len(self.error_memory)
        
        return error_hash
    
    def record_fix(self, error_hash: str, fix_applied: str, 
                  success: bool = True, details: Dict = None) -> bool:
        """
        Record a fix applied to an error
        """
        fix_record = {
            "error_hash": error_hash,
            "fix_applied": fix_applied,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
            "fix_hash": hashlib.md5(fix_applied.encode()).hexdigest()[:12]
        }
        
        self.fix_memory.append(fix_record)
        
        # Learn from successful fixes
        if success:
            self._learn_from_fix(error_hash, fix_applied)
        
        # Save
        self._save_json(self.fix_memory_file, self.fix_memory)
        
        if success:
            self.stats["successful_fixes"] += 1
        
        return True
    
    def _update_pattern_memory(self, error_type: str, error_message: str, error_hash: str):
        """Update pattern recognition memory"""
        # Extract patterns from error message
        patterns = self._extract_patterns(error_message)
        
        for pattern in patterns:
            if pattern not in self.pattern_memory:
                self.pattern_memory[pattern] = {
                    "first_seen": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat(),
                    "count": 1,
                    "error_hashes": [error_hash],
                    "error_types": [error_type]
                }
            else:
                self.pattern_memory[pattern]["count"] += 1
                self.pattern_memory[pattern]["last_seen"] = datetime.now().isoformat()
                if error_hash not in self.pattern_memory[pattern]["error_hashes"]:
                    self.pattern_memory[pattern]["error_hashes"].append(error_hash)
                if error_type not in self.pattern_memory[pattern]["error_types"]:
                    self.pattern_memory[pattern]["error_types"].append(error_type)
        
        self._save_json(self.pattern_memory_file, self.pattern_memory)
    
    def _extract_patterns(self, error_message: str) -> List[str]:
        """Extract meaningful patterns from error message"""
        patterns = []
        
        # Common error patterns
        common_patterns = [
            ("cannot import name", "import_error"),
            ("ModuleNotFoundError", "module_not_found"),
            ("TemplateNotFound", "template_missing"),
            ("404 Not Found", "url_not_found"),
            ("405 Method Not Allowed", "method_not_allowed"),
            ("500 Internal Server Error", "server_error"),
            ("Bootstrap5", "bootstrap5_error"),
            ("bp", "blueprint_error"),
            ("main.py", "main_routes_confusion"),
            ("url_prefix", "url_prefix_issue"),
            ("flask_login", "flask_login_missing"),
            ("SQLAlchemy", "database_error"),
            ("JSON", "json_error"),
        ]
        
        error_lower = error_message.lower()
        
        for pattern, pattern_id in common_patterns:
            if pattern.lower() in error_lower:
                patterns.append(pattern_id)
        
        # Extract specific module names
        import_match = re.search(r"No module named ['\"]([^'\"]+)['\"]", error_message)
        if import_match:
            patterns.append(f"missing_module:{import_match.group(1)}")
        
        # Extract specific import names
        import_name_match = re.search(r"cannot import name ['\"]([^'\"]+)['\"]", error_message)
        if import_name_match:
            patterns.append(f"cannot_import:{import_name_match.group(1)}")
        
        return list(set(patterns))
    
    def _learn_from_fix(self, error_hash: str, fix_applied: str):
        """Learn from successful fixes to prevent future errors"""
        # Find the error
        error_record = None
        for err in self.error_memory:
            if err.get("error_hash") == error_hash:
                error_record = err
                break
        
        if not error_record:
            return
        
        # Extract error pattern
        error_patterns = self._extract_patterns(error_record.get("error_message", ""))
        
        for pattern in error_patterns:
            if pattern not in self.learned_patterns["fix_patterns"]:
                self.learned_patterns["fix_patterns"][pattern] = []
            
            # Add fix if not already recorded
            if fix_applied not in self.learned_patterns["fix_patterns"][pattern]:
                self.learned_patterns["fix_patterns"][pattern].append(fix_applied)
        
        # Create prevention rule
        prevention_rule = {
            "pattern": error_patterns[0] if error_patterns else "generic",
            "fix": fix_applied,
            "confidence": 1.0,
            "applied_count": 1
        }
        
        # Update or add rule
        rule_exists = False
        for i, rule in enumerate(self.learned_patterns["prevention_rules"]):
            if rule["pattern"] == prevention_rule["pattern"] and rule["fix"] == prevention_rule["fix"]:
                self.learned_patterns["prevention_rules"][i]["applied_count"] += 1
                self.learned_patterns["prevention_rules"][i]["confidence"] = min(
                    1.0, self.learned_patterns["prevention_rules"][i]["applied_count"] / 10
                )
                rule_exists = True
                break
        
        if not rule_exists:
            self.learned_patterns["prevention_rules"].append(prevention_rule)
        
        # Save learned patterns
        self._save_learned_patterns()
    
    def should_prevent_operation(self, operation: str, context: Dict = None) -> Tuple[bool, str]:
        """
        Check if we should prevent an operation based on past mistakes
        Returns: (should_prevent, reason)
        """
        context = context or {}
        
        # Check prevention rules
        for rule in self.learned_patterns["prevention_rules"]:
            # Check if rule applies to this operation
            if self._rule_matches(rule, operation, context):
                self.stats["prevented_repeats"] += 1
                return (True, f"Prevented by rule: {rule['pattern']} (confidence: {rule['confidence']:.2f})")
        
        return (False, "")
    
    def _rule_matches(self, rule: Dict, operation: str, context: Dict) -> bool:
        """Check if a prevention rule matches the current operation"""
        pattern = rule.get("pattern", "")
        
        # Check based on operation type
        if "import_error" in pattern and "import" in operation.lower():
            return True
        
        if "bootstrap5_error" in pattern and "bootstrap" in operation.lower():
            return True
        
        if "blueprint_error" in pattern and ("bp" in operation.lower() or "blueprint" in operation.lower()):
            return True
        
        if "main_routes_confusion" in pattern and ("main.py" in str(context) or "routes.py" in str(context)):
            return True
        
        # Check context
        context_str = str(context).lower()
        if pattern.lower() in context_str:
            return True
        
        return False
    
    def get_recommended_fix(self, error_message: str) -> Optional[str]:
        """
        Get recommended fix based on past successful fixes
        """
        error_patterns = self._extract_patterns(error_message)
        
        for pattern in error_patterns:
            if pattern in self.learned_patterns["fix_patterns"]:
                fixes = self.learned_patterns["fix_patterns"][pattern]
                if fixes:
                    # Return the most frequently used fix
                    return fixes[0]
        
        # Check similar errors
        for stored_error in self.error_memory:
            if self._errors_are_similar(error_message, stored_error.get("error_message", "")):
                # Find fixes for this error
                error_hash = stored_error.get("error_hash")
                for fix in self.fix_memory:
                    if fix.get("error_hash") == error_hash and fix.get("success"):
                        return fix.get("fix_applied")
        
        return None
    
    def _errors_are_similar(self, error1: str, error2: str) -> bool:
        """Check if two errors are similar"""
        # Simple similarity check
        error1_lower = error1.lower()
        error2_lower = error2.lower()
        
        # Check for common keywords
        common_keywords = ["import", "module", "template", "bootstrap", "bp", "404", "405", "500"]
        
        matching_keywords = 0
        for keyword in common_keywords:
            if keyword in error1_lower and keyword in error2_lower:
                matching_keywords += 1
        
        return matching_keywords >= 2
    
    def get_statistics(self) -> Dict:
        """Get memory statistics"""
        return {
            **self.stats,
            "unique_patterns": len(self.pattern_memory),
            "prevention_rules": len(self.learned_patterns["prevention_rules"]),
            "memory_size": {
                "errors": len(self.error_memory),
                "fixes": len(self.fix_memory),
                "patterns": len(self.pattern_memory)
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_report(self) -> str:
        """Generate a human-readable report"""
        stats = self.get_statistics()
        
        report = f"""
╔═══════════════════════════════════════════════════╗
║         AGENT 50 MEMORY TRACKER REPORT           ║
║         Project: {self.project_name:30} ║
╚═══════════════════════════════════════════════════╝

📊 STATISTICS:
  • Total Errors Recorded: {stats['total_errors']}
  • Unique Error Patterns: {stats['unique_errors']}
  • Successful Fixes: {stats['successful_fixes']}
  • Prevented Repeat Errors: {stats['prevented_repeats']}
  • Learned Prevention Rules: {stats['prevention_rules']}

🔍 TOP ERROR PATTERNS:
"""
        
        # Get top 5 patterns
        sorted_patterns = sorted(
            self.pattern_memory.items(),
            key=lambda x: x[1].get("count", 0),
            reverse=True
        )[:5]
        
        for pattern, data in sorted_patterns:
            report += f"  • {pattern}: {data.get('count', 0)} occurrences\n"
        
        report += f"\n🎯 PREVENTION RULES (Active):\n"
        for rule in self.learned_patterns["prevention_rules"][:5]:
            report += f"  • {rule['pattern']} → {rule['fix'][:50]}... (conf: {rule['confidence']:.2f})\n"
        
        report += f"\n📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return report

# Global memory tracker instance
_memory_trackers = {}

def get_memory_tracker(project_name: str) -> SupremeMemoryTracker:
    """Get or create memory tracker for project"""
    if project_name not in _memory_trackers:
        _memory_trackers[project_name] = SupremeMemoryTracker(project_name)
    return _memory_trackers[project_name]

def record_agent_error(project_name: str, error_type: str, error_msg: str, 
                      file: str = "", line: int = 0) -> str:
    """Quick function to record agent error"""
    tracker = get_memory_tracker(project_name)
    return tracker.record_error(error_type, error_msg, file, line)

def get_agent_recommendation(project_name: str, error_msg: str) -> Optional[str]:
    """Quick function to get recommendation"""
    tracker = get_memory_tracker(project_name)
    return tracker.get_recommended_fix(error_msg)