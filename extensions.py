from flask_sqlalchemy import SQLAlchemy
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
