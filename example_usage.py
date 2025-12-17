# example_usage.py
from agent_interface import AgentFileClient

client = AgentFileClient("agent50_test")   # test project name
js_code = "console.log('hello from agent');\n"
p = client.write("backend/server.js", js_code)
print("Saved at:", p)
print("Files in project:", client.list())
