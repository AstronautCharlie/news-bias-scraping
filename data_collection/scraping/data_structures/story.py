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
        return str(self.dump())
