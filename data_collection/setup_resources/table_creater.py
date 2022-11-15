"""
Create DynamoDB tables
"""

import boto3
from settings import DynamoConfig

def create_cnn_table(): 
    dynamodb = boto3.client('dynamodb', endpoint_url=DynamoConfig.ENDPOINT_URL)
    table = dynamodb.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'url',
                'AttributeType': 'S'
            },
        ],
        TableName='cnn',
        KeySchema=[
            {
                'AttributeName': 'url',
                'KeyType': 'HASH'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 10
        },
    )