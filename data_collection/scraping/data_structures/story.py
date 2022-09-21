"""
This class defines the data structure for a story
"""

class Story:
    def __init__(self, url=None, 
                        link_headline=None, 
                        article_headline=None,
                        article_text=None, 
                        date=None):
        self._url = url
        self._link_headline = link_headline
        self._article_headline = article_headline
        self._article_text = article_text
        self._date = date

    @property 
    def url(self):
        return self._url
    
    @url.setter
    def url(self, value):
        self._url = value 

    @property
    def link_headline(self):
        return self._link_headline

    @link_headline.setter
    def link_headline(self, value):
        self._link_headline = value

    @property
    def article_headline(self):
        return self._article_headline
    
    @article_headline.setter
    def article_headline(self, value):
        self._article_headline = value

    @property
    def article_text(self):
        return self._article_text
    
    @article_text.setter
    def article_text(self, value):
        self._article_text = value

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value

