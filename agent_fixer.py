from multi_file_agent import phase_test_and_heal, ensure_dirs

# Target Project
PROJECT_NAME = "Supreme_Food_v2"
p_dir = ensure_dirs(PROJECT_NAME)

print(f"\n🤖 AGENT 50: ACTIVATING EMERGENCY REPAIR FOR {PROJECT_NAME}...")
print("-----------------------------------------------------------")

# Agent ka wo function jo Crash pakadta hai aur Gemini se fix mangwata hai
phase_test_and_heal(p_dir)

print("-----------------------------------------------------------")
print("✅ AGENT 50: REPAIR COMPLETE. TRY RUNNING NOW.")