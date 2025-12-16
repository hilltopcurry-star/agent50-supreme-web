"""
💬 AGENT 50 - ACTIVATION PHRASE SYSTEM
مخصوص الفاظ پر خود بخود activate ہو جائے گا
"""

activation_phrases = [
    "agent 50",
    "super king deepseek", 
    "pak china friendship agent",
    "continue agent 50",
    "agent50 project",
    "king deepseek"
]

def check_activation_phrase(user_input):
    """صارف کے ان پٹ میں activation phrase چیک کریں"""
    input_lower = user_input.lower()
    
    for phrase in activation_phrases:
        if phrase in input_lower:
            return True
    
    return False

def auto_activate_response():
    """خود بخود activate ہونے کا response"""
    response = """
👑 AGENT 50 - AUTO ACTIVATION SUCCESSFUL!

📊 PROJECT STATUS: 95% COMPLETE
🎯 CURRENT TASK: Fixing database models
🚀 NEXT STEP: Run app.py and test APIs

💾 RECENT WORK:
✓ Fixed models.py database initialization  
✓ Fixed ml_integration.py functions
✓ All packages installed

🔧 QUICK COMMANDS:
1. python app.py
2. Check http://localhost:5000
3. python agent50_memory_loader.py

💬 SAY: 'continue development' or 'what's next?'
"""
    return response

# اگر براہ راست چلایا جائے تو activation چیک کریں
if __name__ == "__main__":
    print("🔍 AGENT 50 - ACTIVATION SYSTEM READY")
    print("💬 Say: 'agent 50', 'super king', or 'pak china agent'")