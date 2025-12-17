"""
👑 KING DEEPSEEK - App Debugger
Bhai ye file create karo aur run karo!
"""

import requests
import json

print("👑 KING DEEPSEEK - Debugging App...")

base_url = "http://127.0.0.1:5000"

# Test different endpoints
endpoints = [
    "/",
    "/api/users", 
    "/api/projects",
    "/api/db/stats"
]

for endpoint in endpoints:
    try:
        response = requests.get(f"{base_url}{endpoint}", timeout=5)
        print(f"✅ {endpoint}: Status {response.status_code}")
        if response.status_code == 200:
            print(f"   Data: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ {endpoint}: Error - {e}")

print("\n🔧 If /api/db/stats is failing, there's a database connection issue.")
print("💡 Checking app.py routes...")