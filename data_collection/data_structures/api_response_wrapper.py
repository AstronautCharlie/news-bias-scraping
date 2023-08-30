"""
This class wraps the response from whatever API is used to fetch news articles
"""
from datetime import datetime

class ApiResponseWrapper:
    def __init__(self, articles):
        parsed_articles = self._parse_article_list(articles)
        self._articles = parsed_articles

    def _parse_article_list(self, articles):
        parsed_articles = []
        for a in articles:
            parsed_a = {} 
            parsed_a['source'] = a['source']['id']
            parsed_a['article_headline'] = a['title']
            parsed_a['url'] = a['url']
            parsed_a['date'] = self._convert_datetime_to_date(a['publishedAt'])
            parsed_articles.append(parsed_a)
        return parsed_articles

    @property
    def articles(self):
        return self._articles
    
    @articles.setter
    def articles(self, new_articles):
        self._articles = new_articles

    def _convert_datetime_to_date(self, datetime_string):
        input_format = "%Y-%m-%dT%H:%M:%SZ"
        output_format = "%Y-%m-%d"
        datetime_object = datetime.strptime(datetime_string, input_format)
        result = datetime.strftime(datetime_object, output_format)
        return result 
    

"""
    1 9 5 
    3 8 4 
    2 7 6

Can't have 3 and 9 together b/c then you need another 3
ditto 4 and 7 
ditto 3 and 6

2x + y = 15
y = 1, x = 7
y = 3, x = 6

1 5 9
1 6 8

2 4 9
2 5 8
2 6 7

3 4 8
3 5 7

4 5 6

6 8 1 
2 4 9 
7 3 5

OPTIONS:
159, 267, 348
168, 249, 357
       
 2 9 4 
 7 5 3 
 6 1 8 
"""