# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS          # ✅ NEW LINE
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ✅ Enable CORS (allow React frontend)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register routes/blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
