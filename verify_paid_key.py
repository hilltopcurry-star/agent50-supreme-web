import os
import requests

# Set your new API key
API_KEY = "sk-9214c5054a7f4b828cf3f9d608a88f6a"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello! Just say 'PAID API SUCCESSFUL' if this works"}],
    "stream": False
}

print("🔍 Verifying Paid API Key...")
print(f"Key: {API_KEY[:10]}...")

try:
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers=headers,
        json=data,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        ai_response = result["choices"][0]["message"]["content"]
        print("🎉 ✅ PAID API KEY VERIFIED SUCCESSFULLY!")
        print("🤖 AI Response:", ai_response)
        
        # Check token usage
        usage = result.get("usage", {})
        print(f"📊 Token Usage: {usage}")
        
    elif response.status_code == 402:
        print("❌ INSUFFICIENT BALANCE - Payment not activated")
        print("Error:", response.text)
    elif response.status_code == 401:
        print("❌ INVALID API KEY")
    else:
        print(f"❌ API Error: {response.status_code}")
        print("Details:", response.text)
        
except Exception as e:
    print(f"❌ Request failed: {e}")