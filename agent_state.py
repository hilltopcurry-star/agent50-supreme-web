import json
import os
from pathlib import Path
from typing import Dict, Any

STATE_FILE = "agent_state.json"

class AgentState:
    def __init__(self):
        self.state = self.load_state()

    def load_state(self) -> Dict[str, Any]:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        # Default Empty State
        return {
            "project_name": "",
            "phase": "IDLE",  # PLAN, GENERATE, INSTALL, TEST, DEPLOY, COMPLETED
            "files_plan": [],
            "generated_files": [],
            "install_status": "PENDING",
            "server_status": "PENDING",
            "errors": []
        }

    def save(self):
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=4)

    def set_project(self, name):
        if self.state["project_name"] != name:
            self.state = {
                "project_name": name,
                "phase": "PLAN",
                "files_plan": [],
                "generated_files": [],
                "install_status": "PENDING",
                "server_status": "PENDING",
                "errors": []
            }
            self.save()

    def update_phase(self, phase):
        self.state["phase"] = phase
        self.save()

    def add_planned_file(self, filename, role):
        # Avoid duplicates
        for f in self.state["files_plan"]:
            if f['filename'] == filename:
                return
        self.state["files_plan"].append({"filename": filename, "role": role})
        self.save()

    def mark_file_generated(self, filename):
        if filename not in self.state["generated_files"]:
            self.state["generated_files"].append(filename)
            self.save()

    def is_file_done(self, filename):
        return filename in self.state["generated_files"]

    def log_error(self, step, error_msg):
        self.state["errors"].append({"step": step, "msg": str(error_msg)})
        self.save()

# Global Instance
state_manager = AgentState()