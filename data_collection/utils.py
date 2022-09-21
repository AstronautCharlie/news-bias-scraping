"""
Utility functions, such as getting all records from a table and returning 
them as a pandas dataframe 
"""

import boto3 
import pandas as pd 

def get_table_as_df(table_name):
    """
    Get all items from given Dynamodb table and return as pandas dataframe
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name) 

    lastEvaluatedKey = None 
    items = [] 

    while True: 
        if lastEvaluatedKey == None: 
            response = table.scan() 
        else: 
            response = table.scan(ExclusiveStartKey=lastEvaluatedKey)

        items.extend(response['Items'])

        if 'LastEvaluatedKey' in response: 
            lastEvaluatedKey = response['LastEvaluatedKey']
        else: 
            break 

    return pd.DataFrame(items) 

def split_by_source(df):
    """
    Return a list of dictionaries mapping source string to df subset of that 
    source 
    """
    results = {} 
    sources = df.source.unique()

    for source in sources:
        results[source] = df.loc[df.source == source]

    return results 
