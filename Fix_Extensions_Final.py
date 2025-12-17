import os

# Ye script extensions.py ko PERFECTLY update karega (Old + New Combined)
code = """from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_cors import CORS

# Initialize Plugins
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
bootstrap = Bootstrap()
moment = Moment()
cors = CORS()
"""

try:
    with open("extensions.py", "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ extensions.py FIXED! (Login + Moment + JWT Sab set hai)")
except Exception as e:
    print(f"❌ Error: {e}")