import requests
import json
import time
from typing import Optional

# Aapki API Key
API_KEY = "AIzaSyBt8MP2ELPbYvPR53TODFoyEcVbM4thMLc"

# ✅ WAPAS 2.0 PAR (Yeh aapke liye confirm chalta hai)
MODEL_NAME = "gemini-2.0-flash-exp"

# Version v1beta (Jo 2.0 ko support karta hai)
API_URL_BASE = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_NAME}:generateContent"

MAX_RETRIES = 10

def call_llm(prompt: str, *, system_prompt: Optional[str] = None) -> str:
    """
    Gemini Client: Reliable Mode.
    """
    
    # 2 Second wait taake spam na lagay
    time.sleep(2)
    
    url = f"{API_URL_BASE}?key={API_KEY}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
    }

    if system_prompt:
        payload["systemInstruction"] = {
            "parts": [{"text": system_prompt}]
        }
    
    for attempt in range(MAX_RETRIES):
        try:
            headers = {'Content-Type': 'application/json'}
            
            # Timeout 60s
            response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
            
            response.raise_for_status() 

            result = response.json()
            candidate = result.get('candidates', [{}])[0]
            text_response = candidate.get('content', {}).get('parts', [{}])[0].get('text', '')
            
            if text_response:
                return text_response.strip()
            
        except requests.exceptions.Timeout:
            print(f"  ⚠️ API Timeout. Retrying...")
            time.sleep(2)
            continue
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"  🛑 Traffic High (429). Cooling down for 10s...")
                time.sleep(10)
                continue
            
            print(f"  ⚠️ API Error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
            else:
                raise Exception(f"API Error: {e} - {response.text[:100]}")
            
        except Exception as e:
            print(f"  ⚠️ Connection Error: {e}")
            time.sleep(2)
            
    raise Exception("Gemini API failed after retries.")