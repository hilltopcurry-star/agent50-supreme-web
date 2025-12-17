import os
from dotenv import load_dotenv

# Load settings
load_dotenv()

# Check keys
print("--- 🔍 KEY CHECKER ---")
print(f"Current Folder: {os.getcwd()}")

gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key:
    print(f"✅ SUCCESS: Gemini Key mil gayi! (Shuru ke words: {gemini_key[:5]}...)")
else:
    print("❌ FAILURE: Gemini Key nahi mili!")
    print("\n--- Folder Files ---")
    # Folder ki files list karein taake dekhein .env ka asli naam kya hai
    for f in os.listdir():
        if ".env" in f:
            print(f"Found file: {f}")