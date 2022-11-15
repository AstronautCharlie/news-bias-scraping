import logging
from time import sleep
#from scraping.scraper_app import ScraperApp
from scraping.scrapers.cnn_scraper import CnnScraper
from settings import AppConfig

logging.basicConfig(level=AppConfig.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    sleep(5)
    scraper = CnnScraper()
    scraper.run()
    