import os
import time
import json
import subprocess
import threading
from flask import Flask, render_template_string, jsonify, request
from agent_state import state_manager, STATE_FILE

app = Flask(__name__)
AGENT_SCRIPT = "multi_file_agent.py"

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Console - IT Engineer Ali Marri Baloch</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: 'Segoe UI', monospace; }
        .sidebar { height: 100vh; background: #161b22; padding: 20px; border-right: 1px solid #30363d; display: flex; flex-direction: column; }
        .log-window { background: #000; color: #39d353; height: 450px; overflow-y: scroll; padding: 15px; border: 1px solid #30363d; font-family: 'Consolas', monospace; font-size: 13px; border-radius: 6px; }
        .btn-engineer { background: #238636; color: white; border: 1px solid rgba(27,31,35,0.15); width: 100%; padding: 10px; font-weight: 600; }
        .btn-engineer:hover { background: #2ea043; color: white; }
        .phase-badge { font-size: 0.70rem; padding: 5px; border-radius: 4px; background: #21262d; border: 1px solid #30363d; color: #8b949e; display: block; margin-bottom: 5px; }
        .active-phase { background: #1f6feb; color: white; border-color: #1f6feb; box-shadow: 0 0 10px rgba(31,111,235,0.4); }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #0d1117; }
        ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
    </style>
</head>
<body>

<div class="container-fluid">
    <div class="row">
        <div class="col-md-3 sidebar">
            <div class="text-center mb-4">
                <i class="fas fa-user-tie fa-3x text-primary mb-2"></i>
                <h3>IT Engineer<br>Ali Marri Baloch</h3>
                <small class="text-muted">Supreme Automation Console</small>
            </div>
            <hr>
            <div class="d-grid gap-2">
                <button class="btn btn-engineer" onclick="startAgent()"><i class="fas fa-rocket"></i> INITIALIZE PROJECT</button>
                <button class="btn btn-outline-secondary" onclick="stopAgent()"><i class="fas fa-pause"></i> PAUSE SYSTEM</button>
                <button class="btn btn-outline-danger" onclick="resetAgent()"><i class="fas fa-eraser"></i> CLEAR MEMORY</button>
            </div>
            <div class="mt-auto">
                <div class="p-3 border border-secondary rounded bg-dark">
                    <label class="text-muted small">CURRENT MISSION:</label>
                    <h5 id="projName" class="text-white mt-1">--</h5>
                    <small>STATUS: <span id="currentPhase" class="text-warning">IDLE</span></small>
                </div>
            </div>
        </div>

        <div class="col-md-9 p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h4 class="m-0"><i class="fas fa-network-wired"></i> SYSTEM OPERATIONS</h4>
                <span class="badge bg-success">AGENT 50 ONLINE</span>
            </div>

            <div class="progress mb-4" style="height: 8px; background: #21262d;">
                <div id="progressBar" class="progress-bar bg-primary" style="width: 0%"></div>
            </div>

            <div class="d-flex justify-content-between text-center mb-4">
                <span id="ph_PLAN" class="phase-badge flex-fill mx-1">1. ARCHITECTURE</span>
                <span id="ph_GENERATE" class="phase-badge flex-fill mx-1">2. CODE GEN</span>
                <span id="ph_INSTALL" class="phase-badge flex-fill mx-1">3. INSTALL</span>
                <span id="ph_TEST" class="phase-badge flex-fill mx-1">4. AUTO-TEST</span>
                <span id="ph_DEPLOY" class="phase-badge flex-fill mx-1">5. DEPLOYMENT</span>
            </div>

            <div class="log-window" id="logWindow">
                <div class="text-muted">> Waiting for Engineer's command...</div>
            </div>

            <div class="mt-3">
                <h6 class="text-muted small">GENERATED ASSETS:</h6>
                <div id="fileList" class="d-flex flex-wrap gap-2"></div>
            </div>
        </div>
    </div>
</div>

<script>
    setInterval(updateState, 1000);

    function updateState() {
        fetch('/api/status').then(r => r.json()).then(data => {
            document.getElementById('projName').innerText = data.project_name || "Ready";
            document.getElementById('currentPhase').innerText = data.phase;
            
            let progress = 0;
            if(data.phase === 'PLAN') progress = 10;
            if(data.phase === 'GENERATE') progress = 40;
            if(data.phase === 'INSTALL') progress = 60;
            if(data.phase === 'TEST') progress = 80;
            if(data.phase === 'DEPLOY') progress = 90;
            if(data.phase === 'COMPLETED') progress = 100;
            
            document.getElementById('progressBar').style.width = progress + "%";

            document.querySelectorAll('.phase-badge').forEach(el => el.classList.remove('active-phase'));
            if(data.phase !== 'IDLE' && data.phase !== 'ERROR READING STATE') {
                const el = document.getElementById('ph_' + data.phase) || document.getElementById('ph_COMPLETED');
                if(el) el.classList.add('active-phase');
            }

            const fileContainer = document.getElementById('fileList');
            fileContainer.innerHTML = '';
            (data.files_plan || []).forEach(f => {
                const isDone = (data.generated_files || []).includes(f.filename);
                const bgClass = isDone ? 'bg-success text-white' : 'bg-dark text-muted border border-secondary';
                fileContainer.innerHTML += `<span class="badge ${bgClass} p-2 fw-normal">${f.filename}</span>`;
            });
        });
        
        fetch('/api/logs').then(r => r.text()).then(logs => {
            const win = document.getElementById('logWindow');
            if (win.innerHTML !== logs) {
                const isAtBottom = win.scrollHeight - win.scrollTop === win.clientHeight;
                win.innerHTML = logs;
                if(isAtBottom) win.scrollTop = win.scrollHeight;
            }
        });
    }

    function startAgent() { fetch('/api/start', {method: 'POST'}); }
    function stopAgent() { fetch('/api/stop', {method: 'POST'}); }
    function resetAgent() { if(confirm("Wipe memory?")) fetch('/api/reset', {method: 'POST'}); }
</script>
</body>
</html>
"""

process = None
log_buffer = []

def read_logs():
    global process
    if process:
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                log_buffer.append(f"<div>> {line.strip()}</div>")
                if len(log_buffer) > 200: log_buffer.pop(0)

@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/api/status')
def get_status():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f: return jsonify(json.load(f))
        except: pass
    return jsonify({"phase": "IDLE", "project_name": "Ready"})

@app.route('/api/logs')
def get_logs(): return "".join(log_buffer)

@app.route('/api/start', methods=['POST'])
def start_agent():
    global process
    if process and process.poll() is None: return jsonify({"status": "Running"})
    process = subprocess.Popen(['python', '-u', AGENT_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=os.getcwd())
    threading.Thread(target=read_logs, daemon=True).start()
    return jsonify({"status": "Started"})

@app.route('/api/stop', methods=['POST'])
def stop_agent():
    global process
    if process: process.kill(); process = None; log_buffer.append("<div style='color:red'>STOPPED</div>")
    return jsonify({"status": "Stopped"})

@app.route('/api/reset', methods=['POST'])
def reset_agent():
    global log_buffer
    if os.path.exists(STATE_FILE): os.remove(STATE_FILE)
    log_buffer = ["<div style='color:orange'>MEMORY WIPED</div>"]
    return jsonify({"status": "Reset"})

if __name__ == '__main__':
    print("👑 CONSOLE STARTED: http://127.0.0.1:8000")
    app.run(port=8000, debug=True)