import os
import sys
from agent_qa import AgentQA

# Target Project jahan error aa raha hai
PROJECT_NAME = "Supreme_Food_Auto_Fix"
PROJECT_DIR = os.path.join("projects", PROJECT_NAME)

print(f"\n🚑 AGENT 50 DOCTOR: STARTING REPAIR FOR {PROJECT_NAME}...")
print("==========================================================")

if not os.path.exists(PROJECT_DIR):
    print(f"❌ Error: Folder {PROJECT_DIR} nahi mila.")
else:
    # Doctor ko bulao (Port 5000 par check karega)
    qa = AgentQA(PROJECT_DIR, port=5000)
    
    # Check aur Fix shuru karo
    print("👉 Starting Server to detect crashes...")
    success = qa.run_checks()
    
    if success:
        print("\n✅ REPAIR SUCCESSFUL! System is stable.")
    else:
        print("\n⚠️ REPAIR INCOMPLETE. Check logs.")

print("==========================================================")