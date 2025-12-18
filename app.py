import os
from extensions import db, migrate, bootstrap, moment
from flask import Flask
from socketio_handler import socketio
import payment_handler  # Import to initialize

from config import Config
from routes import routes_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    moment.init_app(app)

    # Register blueprints
    app.register_blueprint(routes_bp)

    # Initialize SocketIO
    socketio.init_app(app, message_queue=app.config.get('REDIS_URL'))

    return app

app = create_app()

# --- 🛠️ AUTO-DATABASE FIX (MAGIC CODE) 🛠️ ---
# Ye code har baar deploy hone par khud tables bana dega
# Is se "Internal Server Error" khatam ho jayega
with app.app_context():
    db.create_all()
    print("✅ Database Tables Created Successfully via app.py!")

if __name__ == '__main__':
    # Render ke liye Port setup
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
