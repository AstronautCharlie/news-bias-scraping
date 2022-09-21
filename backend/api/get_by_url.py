from flask import Blueprint
import boto3 
#from settings import BackendConfig

get_by_url_bp = Blueprint('get_by_url', __name__, url_prefix='/api')

@get_by_url_bp.route('/article_url/<string:article_url>')
def get_by_url(article_url): 
    client = boto3.client('dynamodb') 

    response = client.query(
        TableName='articles_sample',
        KeyConditionExpression={
            'url': {
                'AttributeValueList': [{
                    'S': article_url
                }]
            }
        }
    )
    return {
        'response': response
    }