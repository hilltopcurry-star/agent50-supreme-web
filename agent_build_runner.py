"""
AGENT 50 SUPREME - Background Build Execution System
Runs Agent50 builds in background threads/subprocesses, tracks state, and updates self-awareness.
This ensures the Flask console API remains responsive while builds execute.
"""

import os
import sys
import json
import time
import uuid
import threading
import subprocess
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
from queue import Queue
import traceback

# ========== FIX APPLIED HERE ==========
# Try to import self-awareness system
try:
    # Humne path fix kiya hai taake ye core folder se uthaye
    from core.agent_identity import get_self_awareness
    HAS_SELF_AWARENESS = True
except ImportError:
    HAS_SELF_AWARENESS = False
    print("[BUILD RUNNER] Self-awareness system not available")
# ======================================

# ========== BUILD STATE MANAGEMENT ==========

class BuildStatus(Enum):
    """Status of a build execution"""
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

@dataclass
class BuildJob:
    """Represents a single build job"""
    build_id: str
    project_name: str
    project_type: str
    status: BuildStatus
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    exit_code: Optional[int] = None
    output: str = ""
    error: str = ""
    progress_percentage: float = 0.0
    current_phase: str = "queued"
    pid: Optional[int] = None
    thread_id: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['status'] = self.status.value
        return result
    
    @classmethod
    def create_new(cls, project_name: str, project_type: str = "food_delivery") -> 'BuildJob':
        """Create a new build job"""
        return cls(
            build_id=f"build_{uuid.uuid4().hex[:8]}",
            project_name=project_name,
            project_type=project_type,
            status=BuildStatus.QUEUED,
            created_at=datetime.now().isoformat()
        )

# ========== BUILD STORAGE ==========

class BuildStorage:
    """Persistent storage for build jobs"""
    
    def __init__(self, storage_path: Optional[Path] = None):
        self.storage_path = storage_path or Path.home() / ".agent50_builds"
        self.builds_file = self.storage_path / "builds.json"
        self.active_builds_file = self.storage_path / "active_builds.json"
        
        # Ensure storage directory exists
        self.storage_path.mkdir(exist_ok=True, parents=True)
        
        # Load existing builds
        self.builds: Dict[str, BuildJob] = self._load_builds()
        self.active_builds: Dict[str, BuildJob] = self._load_active_builds()
    
    def _load_builds(self) -> Dict[str, BuildJob]:
        """Load all builds from persistent storage"""
        if not self.builds_file.exists():
            return {}
        
        try:
            with open(self.builds_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            builds = {}
            for build_id, build_data in data.items():
                try:
                    # Convert status string to enum
                    status_str = build_data.get('status', 'queued')
                    build_data['status'] = BuildStatus(status_str)
                    builds[build_id] = BuildJob(**build_data)
                except Exception as e:
                    print(f"[STORAGE] Failed to load build {build_id}: {e}")
            
            return builds
        except Exception as e:
            print(f"[STORAGE] Error loading builds: {e}")
            return {}
    
    def _load_active_builds(self) -> Dict[str, BuildJob]:
        """Load active builds from persistent storage"""
        if not self.active_builds_file.exists():
            return {}
        
        try:
            with open(self.active_builds_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            active_builds = {}
            for build_id, build_data in data.items():
                try:
                    # Convert status string to enum
                    status_str = build_data.get('status', 'queued')
                    build_data['status'] = BuildStatus(status_str)
                    active_builds[build_id] = BuildJob(**build_data)
                except Exception as e:
                    print(f"[STORAGE] Failed to load active build {build_id}: {e}")
            
            return active_builds
        except Exception as e:
            print(f"[STORAGE] Error loading active builds: {e}")
            return {}
    
    def save_build(self, build: BuildJob) -> bool:
        """Save a build to persistent storage"""
        try:
            # Update in-memory dictionaries
            self.builds[build.build_id] = build
            
            if build.status in [BuildStatus.RUNNING, BuildStatus.QUEUED]:
                self.active_builds[build.build_id] = build
            else:
                self.active_builds.pop(build.build_id, None)
            
            # Save all builds
            with open(self.builds_file, 'w', encoding='utf-8') as f:
                builds_dict = {bid: b.to_dict() for bid, b in self.builds.items()}
                json.dump(builds_dict, f, indent=2)
            
            # Save active builds
            with open(self.active_builds_file, 'w', encoding='utf-8') as f:
                active_dict = {bid: b.to_dict() for bid, b in self.active_builds.items()}
                json.dump(active_dict, f, indent=2)
            
            return True
        except Exception as e:
            print(f"[STORAGE] Error saving build {build.build_id}: {e}")
            return False
    
    def get_build(self, build_id: str) -> Optional[BuildJob]:
        """Get a build by ID"""
        return self.builds.get(build_id)
    
    def get_all_builds(self) -> List[BuildJob]:
        """Get all builds, sorted by creation date (newest first)"""
        builds = list(self.builds.values())
        builds.sort(key=lambda x: x.created_at, reverse=True)
        return builds
    
    def get_active_builds(self) -> List[BuildJob]:
        """Get all active builds (queued or running)"""
        return [b for b in self.builds.values() 
                if b.status in [BuildStatus.QUEUED, BuildStatus.RUNNING]]
    
    def get_recent_builds(self, limit: int = 10) -> List[BuildJob]:
        """Get recent builds"""
        builds = self.get_all_builds()
        return builds[:limit]
    
    def cleanup_old_builds(self, days_old: int = 30) -> int:
        """Remove builds older than specified days"""
        cutoff_time = time.time() - (days_old * 24 * 3600)
        removed_count = 0
        
        builds_to_keep = {}
        for build_id, build in self.builds.items():
            try:
                build_time = datetime.fromisoformat(build.created_at.replace('Z', '+00:00')).timestamp()
                if build_time > cutoff_time:
                    builds_to_keep[build_id] = build
                else:
                    removed_count += 1
            except:
                builds_to_keep[build_id] = build
        
        self.builds = builds_to_keep
        self.save_build(list(self.builds.values())[0]) if self.builds else None
        
        return removed_count

# ========== BUILD EXECUTOR ==========

class BuildExecutor:
    """Executes Agent50 builds in background processes"""
    
    def __init__(self, max_concurrent_builds: int = 2):
        self.max_concurrent_builds = max_concurrent_builds
        self.storage = BuildStorage()
        self.build_queue = Queue()
        self.running_builds: Dict[str, subprocess.Popen] = {}
        self.executor_thread = None
        self.should_stop = False
        
        # Start executor thread
        self.start()
    
    def start(self):
        """Start the build executor thread"""
        if self.executor_thread and self.executor_thread.is_alive():
            return
        
        self.should_stop = False
        self.executor_thread = threading.Thread(
            target=self._executor_loop,
            name="BuildExecutor",
            daemon=True
        )
        self.executor_thread.start()
        print(f"[BUILD EXECUTOR] Started with max {self.max_concurrent_builds} concurrent builds")
    
    def stop(self):
        """Stop the build executor"""
        self.should_stop = True
        if self.executor_thread:
            self.executor_thread.join(timeout=5)
        
        # Terminate all running builds
        for build_id, process in list(self.running_builds.items()):
            self._terminate_build(build_id, process)
    
    def _executor_loop(self):
        """Main executor loop that processes build queue"""
        print("[BUILD EXECUTOR] Executor loop started")
        
        while not self.should_stop:
            try:
                # Check running builds
                self._monitor_running_builds()
                
                # Start new builds if we have capacity
                current_running = len(self.running_builds)
                if current_running < self.max_concurrent_builds:
                    self._start_next_build()
                
                # Sleep to prevent CPU spinning
                time.sleep(1)
                
            except Exception as e:
                print(f"[BUILD EXECUTOR] Error in executor loop: {e}")
                traceback.print_exc()
                time.sleep(5)
        
        print("[BUILD EXECUTOR] Executor loop stopped")
    
    def _monitor_running_builds(self):
        """Monitor currently running builds"""
        for build_id, process in list(self.running_builds.items()):
            # Check if process is still running
            return_code = process.poll()
            
            if return_code is not None:
                # Process has finished
                self._handle_build_completion(build_id, process, return_code)
    
    def _start_next_build(self):
        """Start the next build from the queue"""
        # Get next build from storage (not queue for persistence)
        active_builds = self.storage.get_active_builds()
        queued_builds = [b for b in active_builds if b.status == BuildStatus.QUEUED]
        
        if not queued_builds:
            return
        
        # Get the oldest queued build
        queued_builds.sort(key=lambda x: x.created_at)
        build = queued_builds[0]
        
        # Start the build
        self._execute_build(build)
    
    def _execute_build(self, build: BuildJob):
        """Execute a build in a subprocess"""
        try:
            print(f"[BUILD EXECUTOR] Starting build {build.build_id} for {build.project_name}")
            
            # Update build status
            build.status = BuildStatus.RUNNING
            build.started_at = datetime.now().isoformat()
            build.current_phase = "starting"
            self.storage.save_build(build)
            
            # Determine agent.py path
            agent_script = self._find_agent_script()
            if not agent_script:
                raise FileNotFoundError("agent.py not found")
            
            # Prepare command
            cmd = [sys.executable, str(agent_script), build.project_name]
            
            # Start subprocess
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True,
                cwd=agent_script.parent
            )
            
            # Store process reference
            build.pid = process.pid
            self.running_builds[build.build_id] = process
            self.storage.save_build(build)
            
            # Start output reader threads
            threading.Thread(
                target=self._read_output,
                args=(build.build_id, process.stdout, "stdout"),
                daemon=True
            ).start()
            
            threading.Thread(
                target=self._read_output,
                args=(build.build_id, process.stderr, "stderr"),
                daemon=True
            ).start()
            
            print(f"[BUILD EXECUTOR] Build {build.build_id} started with PID {process.pid}")
            
        except Exception as e:
            print(f"[BUILD EXECUTOR] Failed to start build {build.build_id}: {e}")
            traceback.print_exc()
            
            build.status = BuildStatus.FAILED
            build.completed_at = datetime.now().isoformat()
            build.error = f"Failed to start: {str(e)}"
            self.storage.save_build(build)
    
    def _read_output(self, build_id: str, pipe, pipe_type: str):
        """Read output from build process"""
        build = self.storage.get_build(build_id)
        if not build:
            return
        
        try:
            for line in iter(pipe.readline, ''):
                if not line:
                    break
                
                # Update build progress based on output
                self._update_build_from_output(build, line, pipe_type)
                
                # Append to output
                if pipe_type == "stdout":
                    build.output += line
                else:
                    build.error += line
                
                # Save periodically
                if len(build.output) % 1000 < 100:  # Save every ~1000 chars
                    self.storage.save_build(build)
            
        except Exception as e:
            print(f"[BUILD EXECUTOR] Error reading {pipe_type} for build {build_id}: {e}")
    
    def _update_build_from_output(self, build: BuildJob, line: str, pipe_type: str):
        """Update build progress based on output line"""
        line_lower = line.lower()
        
        # Detect phases
        if "[plan]" in line:
            build.current_phase = "planning"
            build.progress_percentage = 10.0
        elif "[gen]" in line:
            build.current_phase = "generating"
            build.progress_percentage = 30.0
        elif "[install]" in line:
            build.current_phase = "installing"
            build.progress_percentage = 40.0
        elif "[frontend]" in line:
            build.current_phase = "frontend"
            build.progress_percentage = 60.0
        elif "[qa]" in line:
            build.current_phase = "qa"
            build.progress_percentage = 80.0
        elif "[success]" in line:
            build.current_phase = "completed"
            build.progress_percentage = 100.0
        elif "[fail]" in line:
            build.current_phase = "failed"
        
        # Update self-awareness system if available
        if HAS_SELF_AWARENESS and "[IDENTITY]" in line:
            try:
                # Extract progress info if present
                if "Progress updated:" in line:
                    import re
                    match = re.search(r'(\d+\.?\d*)% complete', line)
                    if match:
                        build.progress_percentage = float(match.group(1))
            except:
                pass
    
    def _handle_build_completion(self, build_id: str, process: subprocess.Popen, return_code: int):
        """Handle build process completion"""
        build = self.storage.get_build(build_id)
        if not build:
            return
        
        # Read remaining output
        stdout, stderr = process.communicate()
        build.output += stdout or ""
        build.error += stderr or ""
        
        # Update build status
        build.completed_at = datetime.now().isoformat()
        build.exit_code = return_code
        
        if return_code == 0:
            build.status = BuildStatus.COMPLETED
            build.progress_percentage = 100.0
            build.current_phase = "completed"
            print(f"[BUILD EXECUTOR] Build {build_id} completed successfully")
        else:
            build.status = BuildStatus.FAILED
            build.current_phase = "failed"
            print(f"[BUILD EXECUTOR] Build {build_id} failed with code {return_code}")
        
        # Update self-awareness system
        if HAS_SELF_AWARENESS and return_code == 0:
            try:
                self_awareness = get_self_awareness()
                self_awareness.update_project_progress(
                    build.project_name,
                    completion_percentage=100.0,
                    generated_files=["BUILD_COMPLETED"]
                )
                self_awareness.save_state()
                print(f"[BUILD EXECUTOR] Updated self-awareness for {build.project_name}")
            except Exception as e:
                print(f"[BUILD EXECUTOR] Failed to update self-awareness: {e}")
        
        # Clean up
        self.running_builds.pop(build_id, None)
        self.storage.save_build(build)
    
    def _terminate_build(self, build_id: str, process: subprocess.Popen):
        """Terminate a running build"""
        try:
            build = self.storage.get_build(build_id)
            if build:
                build.status = BuildStatus.CANCELLED
                build.completed_at = datetime.now().isoformat()
                self.storage.save_build(build)
            
            if process.poll() is None:  # Process is still running
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            
            self.running_builds.pop(build_id, None)
            print(f"[BUILD EXECUTOR] Build {build_id} terminated")
            
        except Exception as e:
            print(f"[BUILD EXECUTOR] Error terminating build {build_id}: {e}")
    
    def _find_agent_script(self) -> Optional[Path]:
        """Find the agent.py script"""
        # Try current directory
        current_dir = Path(__file__).parent
        agent_py = current_dir / "agent.py"
        
        if agent_py.exists():
            return agent_py
        
        # Try parent directory
        parent_dir = current_dir.parent
        agent_py = parent_dir / "agent.py"
        
        if agent_py.exists():
            return agent_py
        
        # Try to find it in Python path
        for path in sys.path:
            agent_py = Path(path) / "agent.py"
            if agent_py.exists():
                return agent_py
        
        return None
    
    def submit_build(self, project_name: str, project_type: str = "food_delivery") -> Optional[BuildJob]:
        """Submit a new build job"""
        # Check if project is already building
        active_builds = self.storage.get_active_builds()
        for build in active_builds:
            if build.project_name == project_name and build.status in [BuildStatus.QUEUED, BuildStatus.RUNNING]:
                print(f"[BUILD EXECUTOR] Project {project_name} is already building (ID: {build.build_id})")
                return build
        
        # Create new build job
        build = BuildJob.create_new(project_name, project_type)
        self.storage.save_build(build)
        
        print(f"[BUILD EXECUTOR] Submitted build {build.build_id} for {project_name}")
        return build
    
    def get_build_status(self, build_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a build"""
        build = self.storage.get_build(build_id)
        if not build:
            return None
        
        result = build.to_dict()
        
        # Add runtime info
        if build.started_at and not build.completed_at:
            started = datetime.fromisoformat(build.started_at.replace('Z', '+00:00'))
            runtime = datetime.now() - started
            result['runtime_seconds'] = runtime.total_seconds()
        
        # Check if process is still running
        if build.build_id in self.running_builds:
            process = self.running_builds[build.build_id]
            result['process_alive'] = process.poll() is None
        
        return result
    
    def cancel_build(self, build_id: str) -> bool:
        """Cancel a build"""
        build = self.storage.get_build(build_id)
        if not build:
            return False
        
        if build.status == BuildStatus.RUNNING and build.build_id in self.running_builds:
            # Terminate running process
            process = self.running_builds[build.build_id]
            self._terminate_build(build_id, process)
            return True
        elif build.status == BuildStatus.QUEUED:
            # Mark as cancelled
            build.status = BuildStatus.CANCELLED
            build.completed_at = datetime.now().isoformat()
            self.storage.save_build(build)
            return True
        
        return False
    
    def get_all_builds_status(self) -> List[Dict[str, Any]]:
        """Get status of all builds"""
        builds = self.storage.get_all_builds()
        return [b.to_dict() for b in builds]
    
    def get_active_builds_status(self) -> List[Dict[str, Any]]:
        """Get status of active builds"""
        active_builds = self.storage.get_active_builds()
        return [b.to_dict() for b in active_builds]

# ========== GLOBAL BUILD EXECUTOR INSTANCE ==========

# Singleton instance
_build_executor: Optional[BuildExecutor] = None

def get_build_executor() -> BuildExecutor:
    """Get or create the global build executor instance"""
    global _build_executor
    if _build_executor is None:
        _build_executor = BuildExecutor(max_concurrent_builds=2)
    
    return _build_executor

def shutdown_build_executor():
    """Shutdown the build executor"""
    global _build_executor
    if _build_executor:
        _build_executor.stop()
        _build_executor = None

# ========== CONSOLE API INTEGRATION HELPER ==========

def submit_build_from_console(project_name: str, project_type: str = "food_delivery", 
                             request_user: str = "console") -> Dict[str, Any]:
    """
    Submit a build from the console API
    Returns a dict with build info for API response
    """
    executor = get_build_executor()
    build = executor.submit_build(project_name, project_type)
    
    if not build:
        return {
            "status": "error",
            "message": "Failed to submit build"
        }
    
    # Log build submission
    log_build_activity(build, "submitted", request_user)
    
    return {
        "status": "success",
        "message": f"Build submitted for {project_name}",
        "build_id": build.build_id,
        "project_name": build.project_name,
        "project_type": build.project_type,
        "status": build.status.value,
        "created_at": build.created_at,
        "queue_position": len(executor.storage.get_active_builds())
    }

def get_build_info_for_api(build_id: str) -> Optional[Dict[str, Any]]:
    """Get build info formatted for API response"""
    executor = get_build_executor()
    build_info = executor.get_build_status(build_id)
    
    if not build_info:
        return None
    
    # Add additional info
    build_info["api_endpoints"] = {
        "status": f"/api/v1/builds/{build_id}/status",
        "output": f"/api/v1/builds/{build_id}/output",
        "cancel": f"/api/v1/builds/{build_id}/cancel"
    }
    
    return build_info

def log_build_activity(build: BuildJob, action: str, user: str = "system"):
    """Log build activity"""
    log_dir = Path.home() / ".agent50_builds" / "logs"
    log_dir.mkdir(exist_ok=True, parents=True)
    
    log_file = log_dir / f"activity_{datetime.now().date()}.json"
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "build_id": build.build_id,
        "project": build.project_name,
        "action": action,
        "user": user,
        "status": build.status.value
    }
    
    logs = []
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    logs.append(log_entry)
    
    try:
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    except:
        pass

# ========== CLEANUP ON EXIT ==========

import atexit
atexit.register(shutdown_build_executor)

print("[BUILD RUNNER] Background build execution system initialized")