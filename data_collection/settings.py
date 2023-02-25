"""
All customizable settings for data collection should go here
"""
import argparse
import logging

# Switches
RUN_LOCALLY = False 

class AppConfig:
    if RUN_LOCALLY:
        SELENIUM_ENDPOINT = 'http://selenium:4444/wd/hub'
    else:
        SELENIUM_ENDPOINT = 'http://localhost:4444/wd/hub'

    LOGGING_LEVEL = logging.INFO

    # Wait to let Selenium container spin up properly
    STARTUP_TIMER = 90

    POLL_TIMER = 60 * 60 # Once an hour

class DynamoConfig:
    if RUN_LOCALLY:
        DYNAMO_ENDPOINT = 'http://localstack-dynamodb:4566'
    else:
        DYNAMO_ENDPOINT = 'http://dynamodb.us-east-2.amazonaws.com'

    TABLE_NAME = 'raw_stories'
    
class CnnScraperConfig: 
    CNN_HOMEPAGE = 'https://www.cnn.com'
    CNN_HOMEPAGE_SECTIONS = [
        'zn-homepage-injection-zone-1', # Ticker at top
        'zn-homepage1-zone-1',
        'zn-homepage2-zone-1',
        'zn-homepage2-zone-2', 
    ]

    SELENIUM_ENDPOINT = AppConfig.SELENIUM_ENDPOINT

class FoxScraperConfig:
    FOX_HOMEPAGE = 'https://www.foxnews.com'

    SELENIUM_ENDPOINT = AppConfig.SELENIUM_ENDPOINT