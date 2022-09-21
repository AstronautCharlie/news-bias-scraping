from time import sleep
from selenium import webdriver
from settings import ScraperConfig

class BaseScraper:
    def __init__(self, selenium_endpoint=ScraperConfig.SELENIUM_ENDPOINT):
        self._selenium_endpoint = selenium_endpoint
        self._driver = self._initialize_selenium_webdriver()

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
        Scrape the rendered html from the specified url
        """
        self._driver.get(url)
        return self._driver.page_source

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
        