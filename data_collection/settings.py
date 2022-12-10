"""
All customizable settings for data collection should go here
"""
import argparse
import logging

class AppConfig:
    SELENIUM_ENDPOINT = 'http://selenium:4444/wd/hub'

    LOGGING_LEVEL = logging.INFO

    # Wait to let Selenium container spin up properly
    STARTUP_TIMER = 15

class DynamoConfig:
    # Local dev
    #DYNAMO_ENDPOINT = 'http://localstack-dynamodb:4566'
    # Writing to cloud
    DYNAMO_ENDPOINT = 'http://dynamodb.us-east-2.amazonaws.com'
    TABLE_NAME = 'stories'
    
class CnnScraperConfig: 
    CNN_HOMEPAGE = 'https://www.cnn.com'
    CNN_HOMEPAGE_SECTIONS = [
        'zn-homepage-injection-zone-1', # Ticker at top
        'zn-homepage1-zone-1',
        'zn-homepage2-zone-1',
        'zn-homepage2-zone-2', 
    ]

class FoxScraperConfig:
    FOX_HOMEPAGE = 'https://www.foxnews.com'