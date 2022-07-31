"""
Defines the API for the backend 
"""

import logging 

from flask import Flask
from flask_cors import CORS 

from api.health import health_bp

def create_app() -> Flask: 
    app = Flask(__name__)

    CORS(app) 

    # Set up logging 
    handler = logging.StreamHandler() 
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s : %(levelname)s : %(filename)s : %(lineno)s -- %(message)s"
        )
    )

    logging.getLogger().addHandler(handler)
    add_blueprints(app)

    return app

def add_blueprints(app):
    app.register_blueprint(health_bp)
