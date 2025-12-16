python -c "content = '''from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agent50-simple'
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/')
def home():
    return jsonify({
        'status': 'AGENT 50 - SIMPLE MODE', 
        'message': 'Working Perfectly!',
        'timestamp': datetime.datetime.utcnow().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('message', {'data': 'Connected to AGENT 50'})

if __name__ == '__main__':
    print('🚀 AGENT 50 SIMPLE VERSION RUNNING...')
    socketio.run(app, port=5000)
'''

with open('app_simple.py', 'w') as f:
    f.write(content)

print('✅ FILE CREATED: app_simple.py')"