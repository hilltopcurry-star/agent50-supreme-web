import os
os.environ['DEEPSEEK_API_KEY'] = 'sk-48278a456d04426f8b147f55df7ff1f2'

import requests

headers = {
    "Authorization": f"Bearer sk-48278a456d04426f8b147f55df7ff1f2",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {
            "role": "user", 
            "content": "Write a simple Python hello world function"
        }
    ],
    "stream": False
}

response = requests.post(
    "https://api.deepseek.com/v1/chat/completions",
    headers=headers,
    json=data,
    timeout=30
)

print("Status Code:", response.status_code)
print("Response:", response.json())