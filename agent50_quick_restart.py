"""
🚀 AGENT 50 - QUICK RESTART FOR NEW CHATS
نیو چیٹ میں فوری طور پر Agent 50 کو restart کرے گا
"""

import subprocess
import sys
import os

def quick_restart_agent50():
    print("👑 AGENT 50 - QUICK RESTART SYSTEM")
    print("=" * 60)
    
    # میموری سسٹم چیک کریں
    try:
        from agent50_memory_loader import memory
        memory.display_status()
    except ImportError:
        print("❌ Memory system not found - creating new...")
        # میموری سسٹم بنائیں
        memory_code = '''
# AGENT 50 MEMORY SYSTEM - Paste in new chat
import json
memory = {
    "project": "AGENT 50 - 95% COMPLETE", 
    "current_task": "Fix database models and run app.py",
    "next_step": "python app.py"
}
print("👑 AGENT 50 MEMORY LOADED - CONTINUE DEVELOPMENT")
'''
        print("📋 Paste this in new chat:")
        print(memory_code)
    
    # فائلز چیک کریں
    print("\n🔍 CHECKING CRITICAL FILES...")
    critical_files = [
        "app.py",
        "projects/agent50/models.py", 
        "projects/agent50/ml_integration.py",
        "projects/agent50/realtime_ws.py"
    ]
    
    for file in critical_files:
        if os.path.exists(file):
            print(f"✅ {file} - EXISTS")
        else:
            print(f"❌ {file} - MISSING")
    
    # فوری کمانڈز
    print("\n🚀 QUICK START COMMANDS:")
    print("1. python agent50_memory_loader.py")
    print("2. python app.py") 
    print("3. Check: http://localhost:5000")
    
    # اہم معلومات
    print("\n📋 PROJECT STATUS:")
    print("• 95% Complete - Only final testing remaining")
    print("• Current: Fixing database models")
    print("• Next: Test all API endpoints")
    print("• Last File: models.py (database initialization)")
    
    print("\n🎯 SAY: 'agent 50 continue development' TO ACTIVATE")

if __name__ == "__main__":
    quick_restart_agent50()