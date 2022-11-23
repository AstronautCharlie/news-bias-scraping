"""
All customizable settings for data collection should go here
"""
import argparse
import logging

class AppConfig:
    SELENIUM_ENDPOINT = 'http://selenium:4444/wd/hub'

    LOGGING_LEVEL = logging.INFO

class DynamoConfig:
    DYNAMO_ENDPOINT = 'http://localstack-dynamodb:4566'
    TABLE_NAME = 'stories'
    
class CnnScraperConfig: 
    CNN_HOMEPAGE = 'https://www.cnn.com'
    CNN_HOMEPAGE_SECTIONS = [
        'zn-homepage-injection-zone-1', # Ticker at top
        'zn-homepage1-zone-1',
        'zn-homepage2-zone-1',
        'zn-homepage2-zone-2', 
    ]
