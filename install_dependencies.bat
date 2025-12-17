@echo off
echo Installing AGENT 50 Dependencies...
python -m pip install flask
python -m pip install flask-sqlalchemy
python -m pip install flask-login
python -m pip install flask-socketio
python -m pip install python-socketio
python -m pip install python-dotenv
python -m pip install requests
echo All dependencies installed!
pause