"""
Implements a client wrapper for the API used to fetch news stories
"""
import requests
import os
import logging
import json
from data_structures.api_response_wrapper import ApiResponseWrapper

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsApiClient:
    def query_api(self, params):
        articles = self._request_with_pagination(params)
        response_object = ApiResponseWrapper(articles)
        return response_object
    
    def _request_with_pagination(self, params):
        query_url = self._format_url_query(params)
        response = requests.get(query_url)
        total_response = json.loads(response.text)['totalResults']
        articles = json.loads(response.text)['articles']
        page_num = 1
        while len(articles) < total_response:
            page_num += 1 
            params['page'] = page_num
            query_url = self._format_url_query(params)
            response = requests.get(query_url)
            new_articles = json.loads(response.text)['articles']
            articles.extend(new_articles)
        return articles

    def _format_url_query(self, params):
        query_url = 'https://newsapi.org/v2/everything?'
        for k, v in params.items():
            query_url += f'{k}={v}&'
        api_key = os.getenv('NEWSAPI_API_KEY')
        if api_key is None:
            raise ValueError('\'NEWSAPI_API_KEY\' environment variable not set - required for scraping')
        query_url += f'apiKey={api_key}'
        return query_url