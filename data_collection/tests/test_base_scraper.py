from unittest import TestCase
from unittest.mock import patch
from tests.mock_data import expected_stories, mock_api_response
from scraping.scrapers.base_scraper import BaseScraper
from data_structures.api_response_wrapper import ApiResponseWrapper
import json

class TestBaseScraper:
    @patch('services.newsapi_client.NewsApiClient.query_api')
    @patch('scraping.scrapers.base_scraper.BaseScraper.scrape_article_text_from_url')
    def test_fetch_stories_from_api(self, mock_query_api, mock_scrape_url):
        mock_query_api.return_value = ApiResponseWrapper(mock_api_response)
        mock_scrape_url.return_value = "Lorem ipsum"
        
        scraper = BaseScraper()
        params = {} # Not important since query is mocked
        stories = scraper.fetch_stories_from_api()

        assert stories == expected_stories