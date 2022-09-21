"""
This file handles database-layer interactions 
"""
import boto3
from boto3.dynamodb.conditions import Attr
from settings import BackendConfig

class DynamoClient:
    def __init__(self):
        self.config = BackendConfig()

    def scan_for_word(self, search_term): 
        """
        Return all articles containing the search_term
        """
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(self.config.ARTICLE_TABLE_NAME)

        response = table.scan(
            FilterExpression=Attr(self.config.ARTICLE_COLUMN).contains(search_term)
        )

        matching_articles = response['Items']

        while 'LastEvaluatedKey' in response: 
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            matching_articles.extend(response['Items'])

        return matching_articles
