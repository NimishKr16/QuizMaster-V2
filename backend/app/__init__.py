from flask import Flask
from .extensions import db, cors, jwt
from .routes.auth import auth_bp
from app import models  # Imports all models once
from .routes.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    cors.init_app(app,  supports_credentials=True)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp)

    return app