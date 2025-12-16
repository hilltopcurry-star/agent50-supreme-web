import os
from pathlib import Path

# --- CONFIGURATION ---
BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "projects"

def get_project_path(project_name):
    """Returns the full path to a project."""
    return PROJECTS_DIR / project_name

def ensure_dirs(project_name):
    """Creates the project folder if it doesn't exist."""
    p_dir = PROJECTS_DIR / project_name
    p_dir.mkdir(parents=True, exist_ok=True)
    return p_dir

def get_template_path(project_name, filename):
    """Returns path to a template file."""
    return PROJECTS_DIR / project_name / "templates" / filename