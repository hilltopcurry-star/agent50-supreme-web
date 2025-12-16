from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'AGENT 50', 'message': 'Working!'})

if __name__ == '__main__':
    print('🚀 TEST APP RUNNING...')
    app.run(port=5000)
