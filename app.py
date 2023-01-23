"""
Defines the API for the backend 
"""

import logging 

from flask import Flask
from flask_cors import CORS 

from api.health import health_bp
from api.get_by_url import get_by_url_bp
from api.scan_for_term import scan_for_term_bp

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
    app.register_blueprint(get_by_url_bp)
    app.register_blueprint(scan_for_term_bp)
