"""
👑 KING DEEPSEEK - Error Debugger
"""

import requests

def test_endpoints():
    base_url = "http://127.0.0.1:5000"
    endpoints = ["/api/db/stats", "/api/users", "/api/projects", "/"]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            print(f"🔧 {endpoint}: Status {response.status_code}")
            if response.status_code != 200:
                print(f"   ❌ Error: {response.text}")
            else:
                print(f"   ✅ Success: {response.text[:100]}...")
        except Exception as e:
            print(f"   💥 Exception: {e}")

if __name__ == "__main__":
    print("👑 KING DEEPSEEK - Debugging App...")
    test_endpoints()