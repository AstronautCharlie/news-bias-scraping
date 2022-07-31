from flask import Blueprint, jsonify
from http import HTTPStatus

health_bp = Blueprint('health', __name__, url_prefix='/api')

@health_bp.route('/health')
def healthcheck(): 
    services = {
        'api': 'healthy'
    }
    status = HTTPStatus.OK
    return jsonify(services=services), status