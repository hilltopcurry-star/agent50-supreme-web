"""
AGENT 50 - QUICK START FOR NEW CHATS
نیو چیٹ میں فوری شروع ہونے کے لیے
"""

def quick_activate_agent50():
    print("🔧 INITIALIZING AGENT 50 QUICK START...")
    
    # فائلز چیک کریں
    required_files = [
        'agent50_memory_core.py',
        'agent50_auto_responder.py', 
        '.env',
        'requirements_advanced.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"⚠️ MISSING FILES: {missing_files}")
        print("📥 DOWNLOADING AGENT 50 CORE FILES...")
        # یہاں فائل ڈاؤنلوڈ/تخلیق کا کوڈ آئے گا
    else:
        print("✅ ALL AGENT 50 FILES PRESENT")
    
    # Agent 50 شروع کریں
    try:
        from agent50_auto_responder import auto_responder
        print("🎯 AGENT 50 SUCCESSFULLY ACTIVATED IN NEW CHAT!")
        return auto_responder
    except Exception as e:
        print(f"❌ ACTIVATION FAILED: {e}")
        return None

# اگر براہ راست چلایا جائے
if __name__ == "__main__":
    quick_activate_agent50()