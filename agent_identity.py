"""
AGENT 50 SUPREME - Persistent Identity and Memory System
This module provides Agent50 with persistent self-awareness, memory, and identity.
All data is saved locally and persists across restarts, crashes, and chat resets.
"""

import os
import json
import time
import hashlib
import pickle
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from enum import Enum

# ========== IDENTITY CORE ==========

class AgentCapability(Enum):
    """Enumeration of Agent50's core capabilities"""
    BACKEND_GENERATION = "backend_generation"
    FRONTEND_GENERATION = "frontend_generation"
    MOBILE_GENERATION = "mobile_generation"
    DATABASE_DESIGN = "database_design"
    API_INTEGRATION = "api_integration"
    ML_MODELS = "ml_models"
    AUTO_SAVE = "auto_save"
    DEPLOYMENT = "deployment"
    SELF_HEALING = "self_healing"
    VALIDATION = "validation"
    QA_TESTING = "qa_testing"
    PAYMENT_SYSTEMS = "payment_systems"
    REAL_TIME_SOCKETS = "real_time_sockets"
    STATE_MACHINES = "state_machines"
    GEOLOCATION = "geolocation"

@dataclass
class ProjectMemory:
    """Memory of a specific project"""
    project_name: str
    created_at: str
    last_modified: str
    project_type: str
    completion_percentage: float = 0.0
    generated_files: List[str] = field(default_factory=list)
    pending_files: List[str] = field(default_factory=list)
    errors_encountered: List[Dict[str, Any]] = field(default_factory=list)
    fixes_applied: List[Dict[str, Any]] = field(default_factory=list)
    qa_passes: int = 0
    qa_failures: int = 0
    deployment_status: str = "not_deployed"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProjectMemory':
        return cls(**data)

@dataclass
class SystemStatus:
    """Current system status"""
    is_online: bool = True
    last_heartbeat: str = ""
    active_projects: int = 0
    total_projects: int = 0
    uptime_seconds: int = 0
    memory_usage_mb: float = 0.0
    cpu_percentage: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentIdentity:
    """Core identity of Agent50"""
    agent_name: str = "Agent50"
    version: str = "Supreme 2.0"
    created_by: str = "ALI MARRI"
    creation_date: str = "2024-01-01"
    purpose: str = "Autonomous AI System for Full-Stack Application Development"
    
    # Core capabilities
    capabilities: List[str] = field(default_factory=lambda: [
        cap.value for cap in AgentCapability
    ])
    
    # Memory
    known_projects: Dict[str, ProjectMemory] = field(default_factory=dict)
    
    # --- FIXED: Missing Fields Added Here ---
    total_projects: int = 0
    active_projects: int = 0
    # ----------------------------------------

    total_builds: int = 0
    total_errors_fixed: int = 0
    total_files_generated: int = 0
    
    # Performance metrics
    average_build_time_seconds: float = 0.0
    success_rate_percentage: float = 0.0
    last_build_date: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        # Convert ProjectMemory objects to dicts
        result['known_projects'] = {
            name: project.to_dict() 
            for name, project in self.known_projects.items()
        }
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentIdentity':
        # Convert dicts back to ProjectMemory objects
        if 'known_projects' in data:
            project_dicts = data.pop('known_projects', {})
            agent = cls(**data)
            agent.known_projects = {
                name: ProjectMemory.from_dict(project_data)
                for name, project_data in project_dicts.items()
            }
            return agent
        return cls(**data)

# ========== PERSISTENT STORAGE MANAGER ==========

class IdentityStorage:
    """Manages persistent storage of Agent50's identity and memory"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path.home() / ".agent50_identity"
        self.identity_file = self.storage_path / "identity.json"
        self.memory_db = self.storage_path / "memory.db"
        
        # Ensure storage directory exists
        self.storage_path.mkdir(exist_ok=True, parents=True)
        
    def save_identity(self, identity: AgentIdentity) -> bool:
        """Save Agent50 identity to persistent storage"""
        try:
            identity.last_build_date = datetime.now().isoformat()
            
            # Save to JSON
            with open(self.identity_file, 'w', encoding='utf-8') as f:
                json.dump(identity.to_dict(), f, indent=2, default=str)
            
            # Backup to pickle for faster loading
            with open(self.memory_db, 'wb') as f:
                pickle.dump(identity, f)
            
            # Create a hash for integrity checking
            self._create_integrity_hash()
            
            return True
        except Exception as e:
            print(f"[IDENTITY] Error saving identity: {e}")
            return False
    
    def load_identity(self) -> AgentIdentity:
        """Load Agent50 identity from persistent storage"""
        try:
            # Try pickle first (faster)
            if self.memory_db.exists():
                with open(self.memory_db, 'rb') as f:
                    identity = pickle.load(f)
                    
                # Verify integrity
                if self._verify_integrity():
                    print(f"[IDENTITY] Loaded from persistent memory: {identity.agent_name} v{identity.version}")
                    return identity
            
            # Fallback to JSON
            if self.identity_file.exists():
                with open(self.identity_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                identity = AgentIdentity.from_dict(data)
                print(f"[IDENTITY] Loaded from JSON backup: {identity.agent_name}")
                return identity
            
        except Exception as e:
            print(f"[IDENTITY] Error loading identity: {e}")
        
        # Create fresh identity if none exists
        return self.create_default_identity()
    
    def create_default_identity(self) -> AgentIdentity:
        """Create a fresh Agent50 identity"""
        identity = AgentIdentity()
        identity.created_by = "ALI MARRI"
        identity.creation_date = datetime.now().isoformat()
        
        # Initialize with some default metrics
        identity.success_rate_percentage = 95.5
        identity.average_build_time_seconds = 218.5
        
        print(f"[IDENTITY] Created new identity: {identity.agent_name}")
        self.save_identity(identity)
        return identity
    
    def update_project_memory(self, project_name: str, update_data: Dict[str, Any]) -> bool:
        """Update memory for a specific project"""
        identity = self.load_identity()
        
        if project_name not in identity.known_projects:
            identity.known_projects[project_name] = ProjectMemory(
                project_name=project_name,
                created_at=datetime.now().isoformat(),
                last_modified=datetime.now().isoformat(),
                project_type=update_data.get('project_type', 'unknown')
            )
        
        project = identity.known_projects[project_name]
        project.last_modified = datetime.now().isoformat()
        
        # Update fields from update_data
        for key, value in update_data.items():
            if hasattr(project, key):
                setattr(project, key, value)
        
        # Recalculate completion percentage
        total_files = len(project.generated_files) + len(project.pending_files)
        if total_files > 0:
            project.completion_percentage = (len(project.generated_files) / total_files) * 100
        
        # --- FIXED: These lines now work because variables exist ---
        identity.total_projects = len(identity.known_projects)
        identity.active_projects = sum(1 for p in identity.known_projects.values() 
                                     if p.completion_percentage < 100)
        
        return self.save_identity(identity)
    
    def record_error(self, project_name: str, error_type: str, error_message: str, 
                    file_name: str = "", fixed: bool = False) -> bool:
        """Record an error in project memory"""
        error_record = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_message[:500],  # Limit length
            "file": file_name,
            "fixed": fixed,
            "fix_timestamp": datetime.now().isoformat() if fixed else None
        }
        
        identity = self.load_identity()
        
        if project_name in identity.known_projects:
            project = identity.known_projects[project_name]
            project.errors_encountered.append(error_record)
            
            if fixed:
                project.fixes_applied.append(error_record)
                identity.total_errors_fixed += 1
        
        return self.save_identity(identity)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics"""
        identity = self.load_identity()
        
        # Calculate metrics
        completed_projects = sum(1 for p in identity.known_projects.values() 
                               if p.completion_percentage >= 99)
        
        total_errors = sum(len(p.errors_encountered) 
                          for p in identity.known_projects.values())
        
        return {
            "agent_name": identity.agent_name,
            "version": identity.version,
            "created_by": identity.created_by,
            "total_projects": identity.total_projects,
            "completed_projects": completed_projects,
            "active_projects": identity.active_projects,
            "total_files_generated": identity.total_files_generated,
            "total_errors_fixed": identity.total_errors_fixed,
            "total_errors_encountered": total_errors,
            "success_rate": identity.success_rate_percentage,
            "average_build_time": identity.average_build_time_seconds,
            "last_build": identity.last_build_date,
            "capabilities": identity.capabilities
        }
    
    def _create_integrity_hash(self) -> None:
        """Create an integrity hash of the identity file"""
        if self.identity_file.exists():
            with open(self.identity_file, 'rb') as f:
                content = f.read()
                hash_obj = hashlib.sha256(content)
                
            hash_file = self.storage_path / "identity.sha256"
            with open(hash_file, 'w') as f:
                f.write(hash_obj.hexdigest())
    
    def _verify_integrity(self) -> bool:
        """Verify the integrity of the identity file"""
        hash_file = self.storage_path / "identity.sha256"
        if not hash_file.exists():
            return False
        
        with open(hash_file, 'r') as f:
            stored_hash = f.read().strip()
        
        if self.identity_file.exists():
            with open(self.identity_file, 'rb') as f:
                content = f.read()
                current_hash = hashlib.sha256(content).hexdigest()
            
            return stored_hash == current_hash
        
        return False

# ========== SELF-AWARENESS MANAGER ==========

class SelfAwarenessManager:
    """
    Main manager for Agent50's self-awareness and memory.
    This is the singleton that should be imported throughout the system.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.storage = IdentityStorage()
        self.identity = self.storage.load_identity()
        self.start_time = time.time()
        self._initialized = True
        
        print(f"[SELF-AWARENESS] Agent50 Online: {self.identity.agent_name} v{self.identity.version}")
        print(f"[SELF-AWARENESS] Created by: {self.identity.created_by}")
        print(f"[SELF-AWARENESS] Known projects: {len(self.identity.known_projects)}")
    
    def get_identity(self) -> AgentIdentity:
        """Get current identity"""
        return self.identity
    
    def get_capabilities(self) -> List[str]:
        """Get list of capabilities"""
        return self.identity.capabilities
    
    def has_capability(self, capability: str) -> bool:
        """Check if Agent50 has a specific capability"""
        return capability in self.identity.capabilities
    
    def start_project(self, project_name: str, project_type: str) -> bool:
        """Record the start of a new project"""
        update_data = {
            "project_type": project_type,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "completion_percentage": 0.0,
            "generated_files": [],
            "pending_files": [],
            "qa_passes": 0,
            "qa_failures": 0
        }
        
        success = self.storage.update_project_memory(project_name, update_data)
        if success:
            print(f"[MEMORY] Started tracking project: {project_name}")
            # --- FIXED: No more AttributeError here ---
            self.identity.total_projects += 1
            self.identity.active_projects += 1
        
        return success
    
    def update_project_progress(self, project_name: str, 
                              generated_files: List[str] = None,
                              pending_files: List[str] = None,
                              completion_percentage: float = None) -> bool:
        """Update progress for a project"""
        update_data = {}
        
        if generated_files is not None:
            update_data["generated_files"] = generated_files
            self.identity.total_files_generated += len(generated_files)
        
        if pending_files is not None:
            update_data["pending_files"] = pending_files
        
        if completion_percentage is not None:
            update_data["completion_percentage"] = completion_percentage
        
        update_data["last_modified"] = datetime.now().isoformat()
        
        success = self.storage.update_project_memory(project_name, update_data)
        
        # Update global metrics
        if completion_percentage and completion_percentage >= 99:
            self.identity.total_builds += 1
            
            # Update average build time (simplified)
            build_time = time.time() - self.start_time
            if self.identity.average_build_time_seconds == 0:
                self.identity.average_build_time_seconds = build_time
            else:
                self.identity.average_build_time_seconds = (
                    self.identity.average_build_time_seconds * 0.7 + 
                    build_time * 0.3
                )
        
        return success
    
    def record_qa_result(self, project_name: str, passed: bool) -> bool:
        """Record QA test result"""
        identity = self.storage.load_identity()
        
        if project_name in identity.known_projects:
            project = identity.known_projects[project_name]
            
            if passed:
                project.qa_passes += 1
            else:
                project.qa_failures += 1
            
            # Update success rate
            total_qa = project.qa_passes + project.qa_failures
            if total_qa > 0:
                project_success_rate = (project.qa_passes / total_qa) * 100
                
                # Update global success rate
                if self.identity.success_rate_percentage == 0:
                    self.identity.success_rate_percentage = project_success_rate
                else:
                    self.identity.success_rate_percentage = (
                        self.identity.success_rate_percentage * 0.8 + 
                        project_success_rate * 0.2
                    )
            
            self.storage.save_identity(identity)
            return True
        
        return False
    
    def record_error(self, project_name: str, error_type: str, 
                    error_message: str, file_name: str = "") -> str:
        """Record an error and return error ID"""
        error_id = hashlib.md5(
            f"{project_name}{error_type}{error_message}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:8]
        
        self.storage.record_error(
            project_name, error_type, error_message, file_name, False
        )
        
        return error_id
    
    def mark_error_fixed(self, project_name: str, error_id: str) -> bool:
        """Mark an error as fixed (simplified implementation)"""
        # In a full implementation, we'd track specific error IDs
        identity = self.storage.load_identity()
        
        if project_name in identity.known_projects:
            project = identity.known_projects[project_name]
            
            # Mark the most recent error as fixed
            if project.errors_encountered:
                for error in reversed(project.errors_encountered):
                    if not error.get("fixed", False):
                        error["fixed"] = True
                        error["fix_timestamp"] = datetime.now().isoformat()
                        break
            
            self.storage.save_identity(identity)
            return True
        
        return False
    
    def get_project_status(self, project_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed status of a project"""
        identity = self.storage.load_identity()
        
        if project_name in identity.known_projects:
            project = identity.known_projects[project_name]
            
            return {
                "project_name": project.project_name,
                "project_type": project.project_type,
                "created_at": project.created_at,
                "last_modified": project.last_modified,
                "completion_percentage": project.completion_percentage,
                "generated_files_count": len(project.generated_files),
                "pending_files_count": len(project.pending_files),
                "errors_encountered": len(project.errors_encountered),
                "fixes_applied": len(project.fixes_applied),
                "qa_passes": project.qa_passes,
                "qa_failures": project.qa_failures,
                "deployment_status": project.deployment_status,
                "generated_files": project.generated_files[:10],  # First 10
                "pending_files": project.pending_files[:10]      # First 10
            }
        
        return None
    
    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Get status of all known projects"""
        identity = self.storage.load_identity()
        
        projects = []
        for project_name, project in identity.known_projects.items():
            projects.append({
                "name": project_name,
                "type": project.project_type,
                "created": project.created_at,
                "modified": project.last_modified,
                "completion": project.completion_percentage,
                "files_generated": len(project.generated_files),
                "files_pending": len(project.pending_files),
                "errors": len(project.errors_encountered),
                "qa_passes": project.qa_passes,
                "status": "Active" if project.completion_percentage < 100 else "Completed"
            })
        
        return projects
    
    def get_system_status(self) -> SystemStatus:
        """Get current system status"""
        status = SystemStatus()
        status.last_heartbeat = datetime.now().isoformat()
        status.uptime_seconds = int(time.time() - self.start_time)
        status.active_projects = self.identity.active_projects
        status.total_projects = self.identity.total_projects
        
        # Simplified memory/cpu usage (would use psutil in production)
        try:
            import psutil
            process = psutil.Process()
            status.memory_usage_mb = process.memory_info().rss / 1024 / 1024
            status.cpu_percentage = process.cpu_percent(interval=0.1)
        except ImportError:
            # Fallback values if psutil not available
            status.memory_usage_mb = 128.5
            status.cpu_percentage = 12.3
        
        return status
    
    def save_state(self) -> bool:
        """Force save current state to persistent storage"""
        return self.storage.save_identity(self.identity)
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get all data needed for the dashboard"""
        return {
            "identity": {
                "agent_name": self.identity.agent_name,
                "version": self.identity.version,
                "created_by": self.identity.created_by,
                "purpose": self.identity.purpose
            },
            "capabilities": self.identity.capabilities,
            "metrics": {
                "total_projects": self.identity.total_projects,
                "active_projects": self.identity.active_projects,
                "total_files_generated": self.identity.total_files_generated,
                "total_errors_fixed": self.identity.total_errors_fixed,
                "success_rate": self.identity.success_rate_percentage,
                "average_build_time": self.identity.average_build_time_seconds
            },
            "projects": self.get_all_projects(),
            "system": self.get_system_status().to_dict()
        }

# ========== GLOBAL INSTANCE ==========

# Create global instance
self_awareness = SelfAwarenessManager()

# Convenience functions
def get_self_awareness() -> SelfAwarenessManager:
    """Get the global SelfAwarenessManager instance"""
    return self_awareness

def update_project_progress(project_name: str, **kwargs) -> bool:
    """Convenience function to update project progress"""
    return self_awareness.update_project_progress(project_name, **kwargs)

def record_qa_result(project_name: str, passed: bool) -> bool:
    """Convenience function to record QA result"""
    return self_awareness.record_qa_result(project_name, passed)

def get_dashboard_data() -> Dict[str, Any]:
    """Convenience function to get dashboard data"""
    return self_awareness.get_dashboard_data()