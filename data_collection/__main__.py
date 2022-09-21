import logging
from statistics import quantiles
from time import sleep
#from scraping.scraper_app import ScraperApp
from scraping.scrapers.cnn_scraper import CnnScraper

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    sleep(10)
    scraper = CnnScraper()
    rendered_html = scraper.
    print(scraper.soup.prettify())
    sleep(600) 
    #app = ScraperApp()
    #app.run()