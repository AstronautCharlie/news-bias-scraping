from unittest import TestCase
from services.newsapi_client import NewsApiClient
from datetime import datetime, timedelta
import requests
import json
import os

class TestNewsApiClient(TestCase):
    def test_news_api_client_response_fox(self):
        self._test_client_on_source('fox-news')

    def test_news_api_client_cnn(self):
        self._test_client_on_source('cnn')

    def _test_client_on_source(self, source):
        client = NewsApiClient()
        start = datetime.now() - timedelta(days=3)
        end = datetime.now() - timedelta(days=2)
        start_date = start.strftime('%Y-%m-%d')
        end_date = start.strftime('%Y-%m-%d')
        params = {'from': start_date, 'to': end_date, 'sources': source}

        # Result from using client
        client_response = client.query_api(params)

        # Result from manually querying API
        api_key = os.getenv('NEWSAPI_API_KEY')
        if api_key is None:
            raise ValueError('\'NEWSAPI_API_KEY\' environment variable not set')
        query_url = f'https://newsapi.org/v2/everything?from={start_date}&to={end_date}&sources={source}&apiKey={api_key}'
        manual_response = requests.get(query_url)
        total_results_manual = json.loads(manual_response.text)['totalResults']
        assert len(client_response.articles) == total_results_manual # client paginates automatically
