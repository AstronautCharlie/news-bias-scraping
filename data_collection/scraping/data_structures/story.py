"""
This class defines the data structure for a story
"""
import math

class Story:
    def __init__(self, url=None, 
                        link_headline=None, 
                        article_headline=None,
                        article_text=None, 
                        date=None,
                        source=None):
            self.url = url
            self.link_headline = link_headline
            self.article_headline = article_headline
            self.article_text = article_text
            self.date = date
            self.source = source

    def dump(self):
        return self.__dict__

    def __str__(self):
        if len(self.article_text) == 0: 
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
