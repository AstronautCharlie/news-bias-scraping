"""
Unit test for healthcheck 
"""

from http import HTTPStatus
import json 
from pytest import fixture 

from flask.wrappers import Response 

from api.health import healthcheck 
from app import create_app

@fixture
def context(): 
    app = create_app() 
    client = app.test_client() 
    return locals().copy()

def test_health_check(context): 
    """
    Validate happy path
    """
    client = context["client"]

    response: Response = client.get('http://localhost:5000/api/health')
    resp = json.loads(response.data) 
    
    services = resp['services']
    assert services['api'] == 'healthy'
    assert response.status_code == HTTPStatus.OK