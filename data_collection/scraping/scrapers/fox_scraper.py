from datetime import date
import logging
from bs4 import BeautifulSoup as BS

from scraping.scrapers.base_scraper import BaseScraper
from scraping.data_structures.story import Story
from services.dynamo_client import DynamoClient
from services.validators import StoryValidator
from settings import AppConfig, FoxScraperConfig

logger = logging.getLogger(__name__)

class FoxScraper(BaseScraper):
    def __init__(self, selenium_endpoint=AppConfig.SELENIUM_ENDPOINT):
        super(FoxScraper, self).__init__(selenium_endpoint=selenium_endpoint)

    def run(self, dynamo_endpoint=None):
        homepage_stories = self.scrape_stories_from_homepage()
        validated_stories = StoryValidator().validate_stories(homepage_stories)
        if dynamo_endpoint:
            response = DynamoClient(endpoint=dynamo_endpoint).put_stories(validated_stories)
        else:
            response = DynamoClient().put_stories(validated_stories)
        return response

    def scrape_stories_from_homepage(self):
        html = self.scrape_static_html(FoxScraperConfig.FOX_HOMEPAGE)
        stories = self._scrape_urls_linkheadlines_into_partial_stories(html)
        stories = self.set_source_to_fox(stories)
        stories = self.set_date_to_today(stories)
        return stories
    
    def set_source_to_fox(self, story_list):
        for s in story_list:
            s.source = 'fox'
        return story_list
    
    def set_date_to_today(self, story_list):
        for s in story_list:
            s.date = str(date.today())
        return story_list

    def _scrape_urls_linkheadlines_into_partial_stories(self, html):
        fox_soup = BS(html)
        homepage_content = fox_soup.find('main', {'class': 'main-content'})
        homepage_collections = homepage_content.find_all('div', {'class': 'collection'})
        homepage_articles = self._collections_to_articles(homepage_collections)
        partial_stories = self._articles_soup_to_partial_stories(homepage_articles)
        partial_stories = self._fill_article_fields_from_partial_stories(partial_stories)
        return partial_stories

    def _collections_to_articles(self, collections):
        all_articles = [] 
        for c in collections:
            c_articles = c.find_all('article', {'class': 'article'})
            all_articles.extend(c_articles)
        return all_articles

    def _articles_soup_to_partial_stories(self, articles):
        stories = [] 
        for art in articles:
            url, link_headline = self._scrape_url_linkheadline_from_article_tag(art)
            story = Story(url=url, link_headline=link_headline)
            stories.append(story)
        return stories

    def _scrape_url_linkheadline_from_article_tag(self, article_tag):
        """
        foxnews.com boxes stories in `article` html classes. The 
        article's headline/link is in an `h2` tag class='title'
        """
        headline = article_tag.find('h2', {'class': 'title'})
        link = headline.find('a')
        try:
            url = link.get('href')
        except AttributeError as err:
            logger.warning(f'link headline has no url\nlink: {link}')
            return None, headline
        headline = link.getText()
        return url, headline
    
    def _fill_article_fields_from_partial_stories(self, stories):
        for story in stories: 
            article_headline, article_text = self._scrape_headline_text_from_article_url(story.url)
            story.article_headline = article_headline
            story.article_text = article_text
        return stories

    def _scrape_headline_text_from_article_url(self, url):
        html = self.scrape_static_html(url)
        fox_soup = BS(html)
        
        first_headline = fox_soup.find('h1', {'class': 'headline'})
        sub_headline = fox_soup.find('h2', {'class': 'sub-headline'})
        article_body = fox_soup.find('div', {'class': 'article-body'})

        headline_text = None
        article_text = None

        if first_headline is not None:
            headline_text = first_headline.getText()
        if sub_headline is not None:
            headline_text += '; ' + sub_headline.getText()
        
        if article_body is not None:
            article_text = ''
            for c in article_body.contents:
                if c.name == 'p' and (c.getText() != c.getText().upper()):
                    article_text += c.getText() + ' '
        
        return headline_text, article_text
        
        
        