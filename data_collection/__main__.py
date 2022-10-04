import logging
from time import sleep
#from scraping.scraper_app import ScraperApp
from scraping.scrapers.cnn_scraper import CnnScraper
from settings import AppConfig

import os 
from utils import parse_cmd_line_args_to_env_vars, set_env_var_defaults

logging.basicConfig(level=AppConfig.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    set_env_var_defaults()
    parse_cmd_line_args_to_env_vars()
    
    sleep(5)
    try:
        scraper = CnnScraper(selenium_endpoint=os.environ['SELENIUM_ENDPOINT'])
    except KeyError: 
        logging.error('You probably forgot to set env var "SELENIUM_ENDPOINT"')
    scraper.run()
    sleep(3) 
    #app = ScraperApp()
    #app.run()