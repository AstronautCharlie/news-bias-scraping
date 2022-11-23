from datetime import date
import logging
from bs4 import BeautifulSoup as BS

from scraping.scrapers.base_scraper import BaseScraper
from settings import AppConfig

logger = logging.getLogger(__name__)

class FoxScraper(BaseScraper):
    def __init__(self, selenium_endpoint=AppConfig.SELENIUM_ENDPOINT):
        super(FoxScraper, self).__init__(selenium_endpoint=selenium_endpoint)
