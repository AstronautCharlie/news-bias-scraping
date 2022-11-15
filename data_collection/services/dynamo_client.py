"""
Handles DB-level interaction, to be used by scrapers
"""

import boto3
import botocore
from settings import DynamoConfig

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('dynamo_client')

class DynamoClient:
    def __init__(self, endpoint=DynamoConfig.DYNAMO_ENDPOINT):
        self.dynamo_endpoint = endpoint

    def get_resource(self):
        return boto3.resource('dynamodb', endpoint_url=self.dynamo_endpoint)
    
    def get_table(self, table_name=DynamoConfig.TABLE_NAME):
        logger.info(f'table name is {table_name}')
        return self.get_resource().Table(name=table_name)
    
    def put_item(self, item, table_name=DynamoConfig.TABLE_NAME):
        table = self.get_table(table_name=table_name)
        try: 
            response = table.put_item(Item=item)
        except botocore.exceptions.ClientError as err:
            logging.error(f'item failed to write\n{item}\n{err}')
        return response

    def put_items(self, items, table_name=DynamoConfig.TABLE_NAME):
        """
        Batch write items
        """
        with self.get_table(table_name=table_name).batch_writer() as batch:
            for item in items: 
                logger.info(f'putting item:\n{item}')
                try:
                    batch.put_item(Item=item)
                except Exception as err:
                    logger.error(f'item write failed: {item}')

    def put_stories(self, stories, table_name=DynamoConfig.TABLE_NAME):
        """
        Batch write Storys
        """

        items = [story.dump() for story in stories]
        self.put_items(items, table_name=table_name)

