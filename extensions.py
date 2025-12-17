from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from flask_moment import Moment       # <--- Added
from flask_login import LoginManager  # <--- Added for safety
from flask_bcrypt import Bcrypt       # <--- Added for safety

# Initialize Extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
socketio = SocketIO(cors_allowed_origins="*") # Added CORS support for socket
bootstrap = Bootstrap()
moment = Moment()           # <--- Added (Yehi missing tha)
login_manager = LoginManager()
bcrypt = Bcrypt()

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    socketio.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)    # <--- Init Added
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Login Manager Settings
    login_manager.login_view = 'main_bp.login'
    login_manager.login_message_category = 'info'
