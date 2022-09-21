"""
Scrape websites for articles
"""
#from scrapers.scraper import FoxScraper, CnnScraper
from scrapers.fox_scraper import FoxScraper 
from scrapers.cnn_scraper import CnnScraper
from datetime import date, timedelta 
import boto3 
from boto3.dynamodb.conditions import Key 

SOURCES = ['fox', 'cnn']

# Entry point for lambda function 
def main_handler(event, handler): 
    # Get Articles table in dynamodb
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Articles')

    # Get existing headlines from past week 
    last_week = date.today() - timedelta(weeks=1)
    fe = Key('date').between(str(last_week), str(date.today()))
    response = table.scan(FilterExpression=fe)['Items']
    existing_headlines = [] 
    existing_urls = []
    for i in response: 
        existing_headlines.append(i['headline'])
        existing_urls.append(i['url'])

    # Scrape articles 
    all_articles = [] 

    # Scrape fox articles if listed 
    if 'fox' in SOURCES: 
        try: 
            fs = FoxScraper() 
            fox_articles = fs.scrape() 
            all_articles.extend(fox_articles)
        except Exception as e: 
            if hasattr(e, 'message'): 
                print(f'FoxScraper encountered exception, skipping:\n{e}')
            else: 
                print(f'FoxScraper encountered exception, skipping:\n{e}')

    cnn_s = CnnScraper()
    cnn_articles = cnn_s.scrape()
    all_articles.extend(cnn_articles)

    # Put items into DB
    for a in all_articles: 
        print('\n\nputting item:', a['headline'])
        table.put_item(
            Item={
                'url': a['url'],
                'headline': a['headline'],
                'source': a['source'],
                'date': str(a['date']),
                'article': a['article'],
                'placement': a['placement']
            }
        )
        

# Used for testing 
if __name__ == '__main__': 
    main_handler(None, None)
