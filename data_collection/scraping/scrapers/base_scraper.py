from time import sleep
from selenium import webdriver
from data_structures.story import Story
from services.validators import StoryValidator
from services.newsapi_client import NewsApiClient
import abc

import logging 
import requests

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, selenium_endpoint=None):
        self._selenium_endpoint = selenium_endpoint

    @property
    def selenium_endpoint(self):
        return self._selenium_endpoint
    
    def fetch_stories_from_api(self, params):
        client = NewsApiClient()
        response = client.query_api(params)
        article_stubs = response.articles
        stories = self._convert_stubs_into_valid_stories(article_stubs)
        return stories
    
    def _convert_stubs_into_valid_stories(self, article_stubs):
        full_articles = self._add_article_text_to_stubs(article_stubs)
        full_stories = self._convert_articles_to_stories(full_articles)
        valid_stories = StoryValidator().filter_valid_stories(full_stories)
        return full_stories 
    
    def _add_article_text_to_stubs(self, article_stubs):
        for stub in article_stubs:
            article_text = self.scrape_article_text_from_url(stub['url'])
            stub['article_text'] = article_text 
        return article_stubs
    
    def _convert_articles_to_stories(self, articles):
        stories = [] 
        for article in articles:
            story = Story(**article)
            stories.append(story)
        return stories

    def scrape_article_text_from_url(self, url):
        raise NotImplementedError('Implement this method in scraper subclass')

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
        if self._selenium_endpoint is None: 
            raise ValueError(f'Cannot scraper rendered HTML with SELENIUM_ENDPOINT set to None.\
                Value is {self._selenium_endpoint}')

        driver = self._initialize_selenium_webdriver()
        driver.implicitly_wait(10)
        driver.get(url)
        html = str(driver.page_source)
        driver.quit()
        return html
    
    def scrape_static_html(self, url):
        """
        Scrapes html using `requests` package - returns None if operation fails
        """
        try:
            response = requests.get(url)
        except ConnectionError as err: 
            logger.warning(f'requests.get(url) failed to connect with url={url}')
            return None
        except Exception as err:
            logger.error(f'requests.get(url) failed with url={url}\nerr={err}')
            return None
        html = response.text
        return html
