"""
Utility functions, such as getting all records from a table and returning 
them as a pandas dataframe 
"""
import os
import logging 
import argparse
from settings import AppConfig

logger = logging.getLogger(__name__)

def set_env_var_defaults():
    """
    Set environment variable defaults
    """
    for env_var_name, env_var_val in AppConfig.ENVIRONMENT_VARIABLE_DEFAULTS.items():
        os.environ[env_var_name] = env_var_val 

def parse_cmd_line_args_to_env_vars():
    """
    Parse command line arguments to environment variables
    """
    parser = argparse.ArgumentParser()

    # Add all arguments here
    parser.add_argument('-se', '--SELENIUM_ENDPOINT')

    # Parse to environment variables
    args = parser.parse_args()
    args_dict = vars(args) 
    for env_var_name, env_var_val in args_dict.items():
        if env_var_val is not None:
            os.environ[env_var_name] = env_var_val
        logger.debug(f'${env_var_name} = {os.environ[env_var_name]}') 

# import boto3 
# import pandas as pd 

# def get_table_as_df(table_name):
#     """
#     Get all items from given Dynamodb table and return as pandas dataframe
#     """
#     dynamodb = boto3.resource('dynamodb')
#     table = dynamodb.Table(table_name) 

#     lastEvaluatedKey = None 
#     items = [] 

#     while True: 
#         if lastEvaluatedKey == None: 
#             response = table.scan() 
#         else: 
#             response = table.scan(ExclusiveStartKey=lastEvaluatedKey)

#         items.extend(response['Items'])

#         if 'LastEvaluatedKey' in response: 
#             lastEvaluatedKey = response['LastEvaluatedKey']
#         else: 
#             break 

#     return pd.DataFrame(items) 

# def split_by_source(df):
#     """
#     Return a list of dictionaries mapping source string to df subset of that 
#     source 
#     """
#     results = {} 
#     sources = df.source.unique()

#     for source in sources:
#         results[source] = df.loc[df.source == source]

#     return results 

