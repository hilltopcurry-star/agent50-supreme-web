"""
agent_contract.py
The Single Source of Truth.
Backend and Frontend MUST follow these rules.
"""

PROJECT_CONFIG = {
    "port": 5000,
    "db_name": "production.db",
    "routes": {
        "login_api": "/auth/login",      # <-- YEH HAI WO RASTA (Fixed)
        "dashboard_page": "/dashboard",
        "home_page": "/",
        "ai_chat_api": "/api/ai/chat",
        "stats_api": "/api/stats"
    }
}

def get_contract_prompt():
    """Returns a string to inject into Gemini prompts."""
    return f"""
    CRITICAL CONTRACT RULES (DO NOT DEVIATE):
    1. Login API Route MUST be: '{PROJECT_CONFIG['routes']['login_api']}' (Method: POST)
    2. Dashboard Route MUST be: '{PROJECT_CONFIG['routes']['dashboard_page']}'
    3. AI Chat Route MUST be: '{PROJECT_CONFIG['routes']['ai_chat_api']}'
    4. Server Port: {PROJECT_CONFIG['port']}
    5. Database: SQLite ({PROJECT_CONFIG['db_name']})
    """