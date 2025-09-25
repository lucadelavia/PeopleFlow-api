from flask import Flask
from app.config import Config
from app.extensions import mongo


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mongo.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from app.api.employees_routes import employees_bp
    app.register_blueprint(employees_bp)
