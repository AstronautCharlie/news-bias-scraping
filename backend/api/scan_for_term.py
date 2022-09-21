"""
This endpoint returns all articles containing the given search term
"""

from flask import Blueprint
from services.dynamo_client import DynamoClient

scan_for_term_bp = Blueprint('scan_for_term', __name__, url_prefix='/api')

@scan_for_term_bp.route('/scan_for_term/<string:search_term>')
def scan_for_term(search_term): 
    client = DynamoClient()
    response = client.scan_for_word(search_term)

    return {
        'num response': len(response),
        'response': response
    }