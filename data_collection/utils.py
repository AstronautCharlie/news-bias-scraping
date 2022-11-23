"""
Utility functions, such as getting all records from a table and returning 
them as a pandas dataframe 
"""
import os
import logging 
import argparse
from settings import AppConfig

logger = logging.getLogger('utils')

def set_env_var_defaults():
    """
    Set environment variable defaults
    """
    for env_var_name, env_var_val in AppConfig.ENVIRONMENT_VARIABLE_DEFAULTS.items():
        os.environ[env_var_name] = env_var_val 
        logger.info(f'setting env var {env_var_name} to {env_var_val} == {os.environ[env_var_name]}')

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
