import logging

from scraping.scrapers.cnn_scraper import CnnScraper
from scraping.scrapers.fox_scraper import FoxScraper
from settings import AppConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class App:
    def run(self):
        cnn_scraper = CnnScraper(selenium_endpoint=AppConfig.SELENIUM_ENDPOINT)
        response = cnn_scraper.run()
        logger.info(f'CNN Scraper finished with response {response}')

        fox_scraper = FoxScraper(selenium_endpoint=AppConfig.SELENIUM_ENDPOINT)
        response = fox_scraper.run()
        logger.info(f'Fox Scraper finished with response {response}')