from scraping.scrapers.fox_scraper import FoxScraper
from settings import FoxScraperConfig
from unittest import TestCase

selenium_endpoint = 'http://localhost:4444/wd/hub' # Assuming selenium is run in a docker container 

class FoxScraperTest(TestCase):
    def test_initial_html_not_null(self):
        scraper = FoxScraper('selenium_endpoint') # Assuming selenium is run in a docker container 
        response = scraper.scrape_rendered_html(FoxScraperConfig.FOX_HOMEPAGE)
        assert response is not None

    def test_count_of_scraped_stories_nonzero(self):
        scraper = FoxScraper(selenium_endpoint)
        html = scraper.scrape_rendered_html(FoxScraper.CNN_HOMEPAGE)
        stories = scraper.extract_homepage_stories_from_html(html)
        assert len(stories) > 0