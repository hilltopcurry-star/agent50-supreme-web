import os
from agent_qa import AgentQA

# Target Project
PROJECT_NAME = "Supreme_Food_Auto_Fix"
PROJECT_DIR = os.path.join("projects", PROJECT_NAME)

print(f"\n🤖 AGENT 50 DOCTOR: DIAGNOSING {PROJECT_NAME}...")
print("===================================================")

if not os.path.exists(PROJECT_DIR):
    print(f"❌ Error: Folder {PROJECT_DIR} not found.")
else:
    # Initialize Doctor
    qa = AgentQA(PROJECT_DIR, port=5000)
    
    # Start Treatment
    print("👉 Starting Server to detect crashes...")
    qa.run_checks()

print("===================================================")
print("✅ DIAGNOSIS COMPLETE. Try running the app now.")