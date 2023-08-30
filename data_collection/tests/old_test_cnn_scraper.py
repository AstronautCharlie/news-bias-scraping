from scraping.scrapers.cnn_scraper import CnnScraper
from settings import CnnScraperConfig
from unittest import TestCase

selenium_endpoint = 'http://localhost:4444/wd/hub' # Assuming selenium is run in a docker container 

class CnnScraperTest(TestCase):

    def test_initial_html_not_null(self):
        scraper = CnnScraper(selenium_endpoint) 
        response = scraper.scrape_rendered_html(CnnScraperConfig.CNN_HOMEPAGE)
        assert response is not None

    def test_count_of_scraped_stories_nonzero(self):
        scraper = CnnScraper(selenium_endpoint)
        html = scraper.scrape_rendered_html(CnnScraperConfig.CNN_HOMEPAGE)
        stories = scraper.extract_homepage_stories_from_html(html)
        assert len(stories) > 0