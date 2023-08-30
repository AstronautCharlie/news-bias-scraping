"""
This class defines the data structure for a story
"""
import math

class Story:
    def __init__(self, url=None, 
                        link_headline=None, 
                        title=None,
                        article_text=None, 
                        date=None,
                        source=None):
            self._url = url
            self._link_headline = link_headline
            self._title = title
            self._article_text = article_text
            self._date = date
            self._source = source

    @property
    def url(self):
        return self._url
    
    @url.setter
    def url(self, new_url):
        self._url = new_url
    
    @property
    def link_headline(self):
        return self._link_headline

    @link_headline.setter
    def link_headline(self, new_link_headline):
        self._link_headline = new_link_headline
    
    @property 
    def title(self):
        return self._title
    
    @title.setter
    def title(self, new_title):
        self._title = new_title

    @property 
    def article_text(self):
        return self._article_text
    
    @article_text.setter
    def article_text(self, new_article_text):
        self._article_text = new_article_text

    @property 
    def date(self):
        return self._date
    
    @date.setter
    def date(self, new_date):
        self._date = new_date 

    @property
    def source(self):
        return self._source
    
    @source.setter
    def source(self, new_source):
        self._source = new_source
        
    def dump(self):
        return self.__dict__

    def __str__(self):
        if self.article_text is None:
            article_snippet = ''
        else:
            article_snippet = self.article_text[:(min(50, len(self.article_text)))]

        string_rep = f'{"url:".ljust(20)}{self.url}\n\
            {"link headline:".ljust(20)}{self.link_headline}\n\
            {"article headline:".ljust(20)}{self.article_headline}\n\
            {"article_text:".ljust(20)}{article_snippet}\n\
            {"date:".ljust(20)}{self.date}\n\
            {"source:".ljust(20)}{self.source}\n'
        
        return string_rep
