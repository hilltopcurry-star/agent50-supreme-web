from agent.ai_client import ai_client

print("=== Testing AI Client ===")
print(f"API Key present: {'Yes' if ai_client.api_key else 'No'}")
print(f"API Key: {ai_client.api_key[:10]}..." if ai_client.api_key else "API Key: None")

response = ai_client.ask_ai("Write a simple Python function that returns 'Hello World'")
print("\n=== AI Response ===")
print(response)