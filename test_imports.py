import sys
print("Python version:", sys.version)

print("\n--- Testing Imports ---")

try:
    from file_awareness import SupremeFileAwareness
    print("✅ file_awareness.py imported successfully")
except ImportError as e:
    print(f"❌ file_awareness.py import error: {e}")

try:
    from smart_import_detector import SupremeImportDetector
    print("✅ smart_import_detector.py imported successfully")
except ImportError as e:
    print(f"❌ smart_import_detector.py import error: {e}")

try:
    from memory_tracker import get_memory_tracker
    print("✅ memory_tracker.py imported successfully")
except ImportError as e:
    print(f"❌ memory_tracker.py import error: {e}")

try:
    from agent_validator import validate_and_correct
    print("✅ agent_validator.py imported successfully")
except ImportError as e:
    print(f"❌ agent_validator.py import error: {e}")

try:
    from agent_state import state_manager
    print("✅ agent_state.py imported successfully")
except ImportError as e:
    print(f"❌ agent_state.py import error: {e}")

try:
    from llm_client import call_llm
    print("✅ llm_client.py imported successfully")
except ImportError as e:
    print(f"❌ llm_client.py import error: {e}")