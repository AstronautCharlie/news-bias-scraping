"""
All customizable settings for data collection should go here
"""
import argparse
import logging

class AppConfig:
    ENVIRONMENT_VARIABLE_DEFAULTS = {
        """
        These should be settable by `utils.parse_cmd_line_args_to_env_vars()`
        """
        # `selenium` is for Docker Container
        'SELENIUM_ENDPOINT': 'http://selenium:4444/wd/hub'
    }

    LOGGING_LEVEL = logging.INFO
    
class ScraperConfig: 
    CNN_HOMEPAGE = 'https://www.cnn.com'
