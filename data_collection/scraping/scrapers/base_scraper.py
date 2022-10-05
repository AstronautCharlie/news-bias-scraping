from time import sleep
from selenium import webdriver
from settings import ScraperConfig

import logging 
import requests

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, selenium_endpoint=None):
        if selenium_endpoint is None: 
            logger.error('SELENIUM_ENDPOINT argument not provided to Base Scraper')
        self._selenium_endpoint = selenium_endpoint
    """
    @property
    def driver(self):
        return self._driver
    """
    @property
    def selenium_endpoint(self):
        return self._selenium_endpoint

    def _initialize_selenium_webdriver(self):
        """
        Create and return a selenium webdriver 
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Remote(self._selenium_endpoint, options=options)
        return driver 

    def scrape_rendered_html(self, url):
        """
        Uses Selenium
        """
        driver = self._initialize_selenium_webdriver()
        driver.get(url)
        html = str(driver.page_source)
        driver.quit()
        return html
    
    def scrape_static_html(self, url):
        """
        Uses Requests
        """
        response = requests.get(url)
        html = response.text
        return html


        # Set options for webdriver 
        #options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')

        #driver = webdriver.Remote(ScraperConfig.SELENIUM_ENDPOINT, options=options)

        # Fetch and render page, waiting in case rendering takes a moment
        # driver.get(url)
        # sleep(5)
        # rendered_html = driver.page_source 
        # driver.quit()
        # return rendered_html
        