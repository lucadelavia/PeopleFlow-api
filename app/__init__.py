from flask import Flask
from flasgger import Swagger
from app.config import Config
from app.extensions import mongo


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "PeopleFlow",
            "description": "Prueba tecnica realizada con Python, Flask y MongoDB",
            "version": "1.0.0"
        },
        "host": "localhost:5000",
        "basePath": "/",
        "schemes": ["http"],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }
    
    Swagger(app, config=swagger_config, template=swagger_template)
    mongo.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    from app.api.employees_routes import employees_bp
    app.register_blueprint(employees_bp)
