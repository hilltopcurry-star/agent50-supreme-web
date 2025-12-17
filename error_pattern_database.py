"""
AGENT 50 SUPREME - Error Pattern Database
Persistent memory of all past errors to prevent repetition
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
import re

class ErrorPatternDatabase:
    """
    PERMANENT MEMORY FOR AGENT 50
    Remembers every error ever made, learns patterns, prevents repetition
    """
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path("projects") / project_name
        self.database_file = self.project_path / ".error_database.json"
        self.patterns_file = self.project_path / ".error_patterns.json"
        
        # Load existing database
        self.error_database = self._load_database()
        self.error_patterns = self._load_patterns()
        
        # Statistics
        self.stats = {
            "total_errors": len(self.error_database),
            "unique_errors": len(set(e.get("hash") for e in self.error_database if e.get("hash"))),
            "auto_fixed": len([e for e in self.error_database if e.get("auto_fixed", False)]),
            "repeated_errors": self._count_repeated_errors()
        }
        
        print(f"[ERROR DB] Loaded {self.stats['total_errors']} errors for {project_name}")
    
    def _load_database(self) -> List[Dict]:
        """Load error database from file"""
        if self.database_file.exists():
            try:
                with open(self.database_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _load_patterns(self) -> Dict:
        """Load error patterns from file"""
        if self.patterns_file.exists():
            try:
                with open(self.patterns_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        
        # Default patterns based on Agent 50 experience
        return {
            "import_errors": {
                "Bootstrap5_not_found": {
                    "pattern": "cannot import name 'Bootstrap5'",
                    "solution": "Use 'Bootstrap' instead of 'Bootstrap5'",
                    "prevention": "Never use Bootstrap5 in any code",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                },
                "bp_not_found": {
                    "pattern": "cannot import name 'bp'",
                    "solution": "Use 'main_bp' instead of 'bp'",
                    "prevention": "Always name blueprint 'main_bp'",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                },
                "flask_login_missing": {
                    "pattern": "No module named 'flask_login'",
                    "solution": "Use session-based authentication",
                    "prevention": "Never import flask_login",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                },
                "main_import_error": {
                    "pattern": "cannot import name 'main_bp' from 'main'",
                    "solution": "Import from 'routes' not 'main'",
                    "prevention": "Use 'from routes import main_bp'",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                }
            },
            "runtime_errors": {
                "template_not_found": {
                    "pattern": "jinja2.exceptions.TemplateNotFound",
                    "solution": "Create missing template file",
                    "prevention": "Ensure all templates exist before running",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                },
                "app_context_error": {
                    "pattern": "Working outside of application context",
                    "solution": "Initialize db within app context",
                    "prevention": "Use create_app() pattern correctly",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                },
                "method_not_allowed": {
                    "pattern": "405 Method Not Allowed",
                    "solution": "Add methods=['GET', 'POST'] to route",
                    "prevention": "Always specify HTTP methods",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                }
            },
            "structural_errors": {
                "circular_import": {
                    "pattern": "ImportError: cannot import name",
                    "solution": "Break circular dependency",
                    "prevention": "Avoid mutual imports between files",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": False
                },
                "missing_dependency": {
                    "pattern": "ModuleNotFoundError",
                    "solution": "Install missing package",
                    "prevention": "Check imports before generation",
                    "occurrences": 0,
                    "first_seen": None,
                    "last_seen": None,
                    "auto_fixable": True
                }
            }
        }
    
    def record_error(self, error_message: str, error_type: str, filename: str, 
                     phase: str, fixed: bool = False, fix_applied: str = None) -> str:
        """
        Record a new error in the database
        Returns: error_hash
        """
        # Generate unique hash for this error
        error_hash = hashlib.md5(f"{error_message[:200]}_{filename}".encode()).hexdigest()[:16]
        
        # Check if this is a repeated error
        is_repeated = self._is_error_repeated(error_hash)
        
        # Extract key information
        error_info = {
            "hash": error_hash,
            "message": error_message[:500],  # Truncate long messages
            "type": error_type,
            "filename": filename,
            "phase": phase,
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name,
            "fixed": fixed,
            "fix_applied": fix_applied,
            "repeated": is_repeated,
            "auto_fixed": False
        }
        
        # Add to database
        self.error_database.append(error_info)
        
        # Update patterns
        self._update_patterns(error_message, error_type, error_hash)
        
        # Save to file
        self._save_database()
        
        # Update statistics
        self.stats["total_errors"] = len(self.error_database)
        if is_repeated:
            self.stats["repeated_errors"] = self._count_repeated_errors()
        
        print(f"[ERROR DB] Recorded {'repeated ' if is_repeated else ''}error: {error_type} in {filename}")
        
        return error_hash
    
    def find_similar_errors(self, error_message: str, max_results: int = 5) -> List[Dict]:
        """
        Find similar errors from the past
        """
        similar_errors = []
        
        for error in self.error_database:
            similarity = self._calculate_similarity(error_message, error.get("message", ""))
            if similarity > 0.3:  # 30% similarity threshold
                error["similarity"] = similarity
                similar_errors.append(error)
        
        # Sort by similarity and return top results
        similar_errors.sort(key=lambda x: x.get("similarity", 0), reverse=True)
        return similar_errors[:max_results]
    
    def get_prevention_hint(self, phase: str, filename: str) -> str:
        """
        Get prevention hints based on past errors in this phase/file
        """
        past_errors = [
            e for e in self.error_database 
            if e.get("phase") == phase and e.get("filename") == filename
        ]
        
        if not past_errors:
            return ""
        
        # Group by type
        error_types = {}
        for error in past_errors:
            error_type = error.get("type", "unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
        
        # Generate hints
        hints = []
        for error_type, count in error_types.items():
            if count >= 2:  # Only mention if occurred multiple times
                pattern = self._get_pattern_for_error_type(error_type)
                if pattern and pattern.get("prevention"):
                    hints.append(f"⚠️ Prevent: {pattern['prevention']} (occurred {count} times)")
        
        if hints:
            return "\n".join(hints)
        return ""
    
    def get_most_common_errors(self, limit: int = 5) -> List[Dict]:
        """Get most common error types"""
        error_counts = {}
        
        for error in self.error_database:
            error_type = error.get("type", "unknown")
            error_counts[error_type] = error_counts.get(error_type, 0) + 1
        
        # Convert to list and sort
        common_errors = [
            {"type": error_type, "count": count}
            for error_type, count in error_counts.items()
        ]
        common_errors.sort(key=lambda x: x["count"], reverse=True)
        
        return common_errors[:limit]
    
    def mark_error_fixed(self, error_hash: str, fix_method: str, auto_fixed: bool = False):
        """Mark an error as fixed"""
        for error in self.error_database:
            if error.get("hash") == error_hash:
                error["fixed"] = True
                error["fix_applied"] = fix_method
                error["auto_fixed"] = auto_fixed
                error["fixed_timestamp"] = datetime.now().isoformat()
                break
        
        self._save_database()
        
        if auto_fixed:
            self.stats["auto_fixed"] += 1
    
    def get_success_rate(self) -> float:
        """Calculate error fix success rate"""
        if not self.error_database:
            return 100.0
        
        fixed_errors = len([e for e in self.error_database if e.get("fixed", False)])
        return (fixed_errors / len(self.error_database)) * 100
    
    def generate_report(self) -> str:
        """Generate comprehensive error report"""
        report = f"""
╔═══════════════════════════════════════════════════╗
║           AGENT 50 ERROR DATABASE REPORT          ║
║           Project: {self.project_name:30} ║
╚═══════════════════════════════════════════════════╝

OVERALL STATISTICS:
  Total Errors Recorded: {self.stats['total_errors']}
  Unique Errors: {self.stats['unique_errors']}
  Auto-Fixed Errors: {self.stats['auto_fixed']}
  Repeated Errors: {self.stats['repeated_errors']}
  Success Rate: {self.get_success_rate():.1f}%

MOST COMMON ERRORS:
"""
        common_errors = self.get_most_common_errors(5)
        for i, error in enumerate(common_errors, 1):
            report += f"  {i}. {error['type']}: {error['count']} occurrences\n"
        
        # Error patterns
        report += "\nERROR PATTERNS DETECTED:\n"
        for category, patterns in self.error_patterns.items():
            for pattern_name, pattern_data in patterns.items():
                if pattern_data.get("occurrences", 0) > 0:
                    report += f"  • {pattern_name}: {pattern_data['occurrences']}x\n"
        
        # Recent errors
        recent_errors = self.error_database[-5:] if self.error_database else []
        if recent_errors:
            report += "\nRECENT ERRORS (last 5):\n"
            for error in recent_errors:
                status = "✅" if error.get("fixed") else "❌"
                repeated = "🔄" if error.get("repeated") else ""
                report += f"  {status}{repeated} {error.get('type', 'unknown')}: {error.get('message', '')[:60]}...\n"
        
        # Prevention advice
        report += "\nPREVENTION ADVICE:\n"
        advice = self._generate_prevention_advice()
        if advice:
            report += advice
        else:
            report += "  No specific advice - keep up the good work! 🎯\n"
        
        return report
    
    def _is_error_repeated(self, error_hash: str) -> bool:
        """Check if this error has occurred before"""
        for error in self.error_database:
            if error.get("hash") == error_hash:
                return True
        return False
    
    def _count_repeated_errors(self) -> int:
        """Count how many errors are repeats"""
        seen_hashes = set()
        repeated_count = 0
        
        for error in self.error_database:
            error_hash = error.get("hash")
            if error_hash:
                if error_hash in seen_hashes:
                    repeated_count += 1
                else:
                    seen_hashes.add(error_hash)
        
        return repeated_count
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two error messages"""
        if not text1 or not text2:
            return 0.0
        
        # Simple word-based similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return intersection / union if union > 0 else 0.0
    
    def _update_patterns(self, error_message: str, error_type: str, error_hash: str):
        """Update error patterns based on new error"""
        # Check if matches existing pattern
        for category, patterns in self.error_patterns.items():
            for pattern_name, pattern_data in patterns.items():
                pattern_text = pattern_data.get("pattern", "")
                if pattern_text and pattern_text in error_message:
                    # Update pattern statistics
                    pattern_data["occurrences"] = pattern_data.get("occurrences", 0) + 1
                    pattern_data["last_seen"] = datetime.now().isoformat()
                    
                    if not pattern_data.get("first_seen"):
                        pattern_data["first_seen"] = datetime.now().isoformat()
                    
                    # Save updated patterns
                    self._save_patterns()
                    return
        
        # If no pattern matches, check if we should create a new pattern
        if len(error_message) > 20:  # Only create patterns for meaningful errors
            # Extract key phrase (first line or key part)
            lines = error_message.split('\n')
            key_phrase = lines[0] if lines else error_message[:100]
            
            # Clean up key phrase
            key_phrase = re.sub(r'File "[^"]+"', '', key_phrase)
            key_phrase = re.sub(r'line \d+', '', key_phrase)
            key_phrase = key_phrase.strip()
            
            if key_phrase and len(key_phrase) > 10:
                # Determine category
                category = "other_errors"
                if "import" in error_message.lower() or "module" in error_message.lower():
                    category = "import_errors"
                elif "jinja" in error_message.lower() or "template" in error_message.lower():
                    category = "runtime_errors"
                elif "circular" in error_message.lower() or "dependency" in error_message.lower():
                    category = "structural_errors"
                
                # Create new pattern
                pattern_name = f"pattern_{len(self.error_patterns.get(category, {})) + 1}"
                
                if category not in self.error_patterns:
                    self.error_patterns[category] = {}
                
                self.error_patterns[category][pattern_name] = {
                    "pattern": key_phrase[:100],
                    "solution": "Auto-detected by Agent 50",
                    "prevention": "To be determined",
                    "occurrences": 1,
                    "first_seen": datetime.now().isoformat(),
                    "last_seen": datetime.now().isoformat(),
                    "auto_fixable": False
                }
                
                self._save_patterns()
    
    def _get_pattern_for_error_type(self, error_type: str) -> Optional[Dict]:
        """Get pattern for error type"""
        for category, patterns in self.error_patterns.items():
            for pattern_name, pattern_data in patterns.items():
                if pattern_data.get("pattern", "") in error_type or error_type in pattern_name:
                    return pattern_data
        return None
    
    def _generate_prevention_advice(self) -> str:
        """Generate prevention advice based on patterns"""
        advice = []
        
        for category, patterns in self.error_patterns.items():
            for pattern_name, pattern_data in patterns.items():
                occurrences = pattern_data.get("occurrences", 0)
                if occurrences >= 2:  # Only give advice for recurring patterns
                    prevention = pattern_data.get("prevention", "")
                    if prevention:
                        advice.append(f"  • {prevention} (occurred {occurrences}x)")
        
        if advice:
            return "\n".join(advice) + "\n"
        return ""
    
    def _save_database(self):
        """Save error database to file"""
        try:
            with open(self.database_file, 'w') as f:
                json.dump(self.error_database[-1000:], f, indent=2)  # Keep last 1000 errors
        except:
            pass
    
    def _save_patterns(self):
        """Save error patterns to file"""
        try:
            with open(self.patterns_file, 'w') as f:
                json.dump(self.error_patterns, f, indent=2)
        except:
            pass


# Global database cache
_error_db_cache = {}

def get_error_database(project_name: str) -> ErrorPatternDatabase:
    """Get or create error database for project"""
    if project_name not in _error_db_cache:
        _error_db_cache[project_name] = ErrorPatternDatabase(project_name)
    return _error_db_cache[project_name]

def record_error_to_db(project_name: str, error_message: str, error_type: str, 
                       filename: str, phase: str) -> str:
    """Quick function to record error"""
    db = get_error_database(project_name)
    return db.record_error(error_message, error_type, filename, phase)

def get_error_prevention_hints(project_name: str, phase: str, filename: str) -> str:
    """Get prevention hints for current phase/file"""
    db = get_error_database(project_name)
    return db.get_prevention_hint(phase, filename)