import requests
import json

# Server URL (Mobile API Endpoint)
url = "http://127.0.0.1:5000/api/v1/auth/login"

# Fake Mobile App Data (Driver Login)
payload = {
    "email": "driver@example.com",
    "password": "123456"
}

print("📱 Testing Mobile Login API...")

try:
    # Request bhej rahe hain
    response = requests.post(url, json=payload)
    
    # Result check karein
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS! Mobile App Connected.")
        print(f"👤 User Role: {data['user']['role']}")
        # Token ka shuru ka hissa dikhayen
        print(f"🔑 Secure Token: {data['access_token'][:20]}...")
    else:
        print(f"\n❌ FAILED. Code: {response.status_code}")
        print("Reason:", response.text)

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Tip: Make sure server is running in another terminal!")