"""
Combines news scrapers into a single app
"""

import logging
import boto3
from boto3.dynamodb.conditions import Key
from datetime import date, timedelta
from scraping.scrapers.cnn_scraper import CnnScraper
from scraping.scrapers.fox_scraper import FoxScraper

logger = logging.getLogger(__name__)

class ScraperApp: 

    def scrape(self): 
        """
        Scrape data from websites, return an array with results
        """
        articles = [] 

        # Scrape Fox articles
        fox_scraper = FoxScraper()  
        try: 
            fox_articles = fox_scraper.scrape() 
            articles.extend(fox_articles)
        except Exception as e: 
            logger.error('Fox Scraper has encountered error: %s', e)


        # Scrape CNN articles
        cnn_scraper = CnnScraper()
        try: 
            cnn_articles = cnn_scraper.scrape()
            articles.extend(cnn_articles) 
        except Exception as e:
            logging.error('CNN scraper has encountered error: %s', e)

        return articles
    
    def run(self):
        """
        Main method for app; scrape and write to DynamoDB
        """
        articles = self.scrape() 
        logging.info('Articles are: %s', articles)