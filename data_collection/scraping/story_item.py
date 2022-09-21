"""
This file defines the Story class 
"""

class StoryItem:
    """
    This class defines the record that will be written to DynamoDB
    """
    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.headline = kwargs['headline']
        self.source = kwargs['source']
        self.date = kwargs['date']
    
    def get_item_as_dict(self):
        return self.__dict__
