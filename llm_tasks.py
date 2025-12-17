import time
import uuid

# --- SUPREME INTELLIGENCE IMPORT SYSTEM ---
# Hum check karenge ke kya 'services' module available hai?
# Agar haan, to Real AI use karenge. Agar nahi, to Server crash hone se bachayenge.

try:
    from services.llm_client import call_llm
    AI_STATUS = "🟢 ONLINE (Real Gemini AI)"
except ImportError:
    # Fallback: Agar services file nahi mili to Simulation Mode
    AI_STATUS = "🟠 OFFLINE (Simulation Mode)"
    print("\n[WARNING] 'services.llm_client' not found. Switching to Simulation Mode.")
    
    def call_llm(prompt):
        """Nakli AI response taake server chalta rahe"""
        return f"[SIMULATED AI] Processed your request: {prompt[:30]}..."

# --- TASKS FUNCTIONS ---

def run_llm_sync(prompt: str) -> str:
    """
    Synchronous LLM call. Used by the Flask endpoint /llm/ask_sync.
    Args:
        prompt: The user's query.
    Returns:
        AI Response string.
    """
    print(f"\n--- [AGENT 50 INTELLIGENCE] ---")
    print(f"System Status: {AI_STATUS}")
    print(f"Executing Task: {prompt[:80]}...")
    
    try:
        # Asli ya Simulated function ko call karein
        response = call_llm(prompt)
        print("Status: Success ✅")
        return response
    except Exception as e:
        print(f"Status: Failed ❌ ({str(e)})")
        return "Error processing request."

def run_llm_task(payload: dict):
    """
    Background Task Runner.
    """
    task_id = payload.get("id", str(uuid.uuid4()))
    prompt = payload.get("prompt", "No prompt provided.")
    
    print(f"Starting Background Task {task_id}...")
    
    try:
        result = call_llm(prompt)
        print(f"Task {task_id} Completed.")
        return result
    except Exception as e:
        print(f"Task {task_id} Failed: {e}")
        raise e