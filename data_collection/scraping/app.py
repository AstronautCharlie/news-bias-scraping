from scraping.scrapers.cnn_scraper import CnnScraper
from settings import AppConfig

class App:
    def run(self):
        cnn_scraper = CnnScraper(selenium_endpoint=AppConfig.SELENIUM_ENDPOINT)
        cnn_scraper.run()