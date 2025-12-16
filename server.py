import sys
import os
import time
from flask import Flask, request, jsonify

# --- PATH FIX ---
# Current directory ko path mein add karte hain taake 'tasks' folder mil jaye
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from tasks.llm_tasks import run_llm_sync
except ImportError as e:
    print(f"Error importing tasks: {e}")
    # Fallback dummy function agar import fail ho
    def run_llm_sync(prompt):
        return f"Simulated Response for: {prompt}"

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "Online", "message": "Agent 50 Server Ready"})

@app.route('/llm/ask_sync', methods=['POST'])
def ask_llm_sync():
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    print(f"Received Prompt: {prompt}")
    
    try:
        # Call the logic from tasks/llm_tasks.py
        response = run_llm_sync(prompt)
        return jsonify({
            'status': 'success',
            'response': response
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Server on Port 5010...")
    app.run(debug=True, port=5010)