import logging
import time

from scraping.scrapers.cnn_scraper import CnnScraper
from scraping.scrapers.fox_scraper import FoxScraper
from settings import AppConfig

logger = logging.getLogger(__name__)

class App:
    def run(self):
        # logger.info(f'Starting CNN Scraper...')
        # start_time = time.time()
        # cnn_scraper = CnnScraper(selenium_endpoint=AppConfig.SELENIUM_ENDPOINT)
        # cnn_scraper.run()
        # logger.info(f'CNN Scraper finished. Runtime = {time.time() - start_time} seconds')

        logger.info(f'Starting Fox Scraper...')
        start_time = time.time()
        fox_scraper = FoxScraper(selenium_endpoint=AppConfig.SELENIUM_ENDPOINT)
        response = fox_scraper.run()
        logger.info(f'Fox Scraper finished. Runtime = {time.time() - start_time} seconds')