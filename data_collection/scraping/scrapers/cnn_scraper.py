"""
TODO: 
- Add opinion/analysis tagging 

NOTE: 
- If using selenium to get html, refer to following StackOverflow: 
https://stackoverflow.com/questions/47060735/selenium-remote-webdriver-not-working-with-aws-ec2
"""

from datetime import date
from time import sleep
import logging

from selenium import webdriver 
from bs4 import BeautifulSoup as BS

from scraping.data_structures.story import Story
from scraping.scrapers.base_scraper import BaseScraper
from services.dynamo_client import DynamoClient
from services.validators import StoryValidator
from settings import CnnScraperConfig, AppConfig

logger = logging.getLogger(__name__)

class CnnScraper(BaseScraper): 
    def __init__(self, selenium_endpoint=AppConfig.SELENIUM_ENDPOINT):
        super(CnnScraper, self).__init__(selenium_endpoint=selenium_endpoint)
        self._selenium_endpoint = selenium_endpoint

    def run(self, dynamo_endpoint=None):
        homepage_stories = self.scrape_stories_from_homepage()
        homepage_stories = self.set_source_to_cnn(homepage_stories)
        homepage_stories = self.set_date_to_today(homepage_stories)
        logger.info('homepage_stories:\n')
        for s in homepage_stories:
            logger.info(f'\n\n{s.dump()}')
        validated_stories = self.validate_stories(homepage_stories)
        logger.info('validated_stories:\n')
        for s in validated_stories:
            logger.info(f'\n\n{s.dump()}')
        response = DynamoClient(endpoint=dynamo_endpoint).put_stories(validated_stories)
        return response

    def scrape_stories_from_homepage(self):
        """
        Scrape stories from the CNN homepage.

        Return list of Stories
        """
        html = self.scrape_rendered_html(CnnScraperConfig.CNN_HOMEPAGE)
        story_items = self.extract_homepage_stories_from_html(html)
        
        return story_items

    def extract_homepage_stories_from_html(self, html):
        """
        Get stories from CNN html

        Return list of Stories
        """
        # List of sections on the CNN homepage that contain links to scrape
        homepage_sections = CnnScraperConfig.CNN_HOMEPAGE_SECTIONS

        stories = [] 
        
        for section in homepage_sections: 
            partial_stories = self.scrape_urllink_headlines(html, section)
            stories = [] 
            for partial_story in partial_stories: 
                story = self.populate_articletext_headline_from_url(partial_story)
                stories.append(story)

        return stories 

    def scrape_urllink_headlines(self, 
                        page_html,
                        class_name, 
                        html_type='section',
                        ):
        """
        Get url and link_headline for all homepage Stories

        Return list of Stories (partially populated)
        """
        stories = [] 

        # Scrape links ('a' tags) in section
        soup = BS(page_html, 'html.parser')
        section_html = soup.find(html_type, {'class': class_name})
        if section_html is None: 
            logger.warning(f'No stories found in \
                class_name={class_name}, \
                html_type={html_type}')
            return []
        links = section_html.find_all('a', href=True)

        # Get url and link, ignoring bad urls
        for l in links: 
            link_headline = l.getText()
            url = l.get('href')
            if not self._is_bad_link(url, link_headline):
                full_url = self._fill_partial_url(url)
                new_story = Story(link_headline=link_headline, url=full_url)
                stories.append(new_story)
        
        return stories

    def _is_bad_link(self, url_stub, headline_text):
        """
        Weed out url stubs (raw links from html), e.g. non-cnn links, 
        videos, stories with no headline_text)
        """
        excluded_headlines = [None, '']
        excluded_url_stubs = ['#', '/videos']

        # Check link headline
        if headline_text in excluded_headlines:
            return True
        # Check url
        for excluded_url_stub in excluded_url_stubs:
            if url_stub.startswith(excluded_url_stub):
                return True
        
        return False

    
    def _fill_partial_url(self, url):
        """
        Ensure all urls are properly filled out - some raw URLS from 
        the homepage are of the form '/2022/[date]/whatever'

        http vs https doesn't seem to matter, but one must 
        be provided

        can exclude www
        """
        # First check if is stub ('/')
        if url.startswith('/'):
            url = 'https://www.cnn.com' + url

        # Then check for protocol (http or https)
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url

        return url
    
    def populate_articletext_headline_from_url(self, story):
        """
        Populate article_text and article_headline fields of Story from url field

        Returns Story
        """
        if story.url is None: 
            logging.error('Story url is undefined - cannot populate article')
            return story
        article_headline, article_text = self.scrape_articleheadline_text_from_url(story.url)
        story.article_headline = article_headline
        story.article_text = article_text
        
        return story 

    def scrape_articleheadline_text_from_url(self, url):
        """
        Returns string (headline), string(article_text)
        """
        # At time of writing, CNN story articles are static
        html = self.scrape_static_html(url)
        if html is None: 
            logger.warning(f'Static scrape failed with url={url}')
            return None, None
        article_headline = self._find_articleheadline_in_page_html(html)#soup.find('h1', {'class': 'pg-headline'}).getText()
        article_text = self._find_articletext_in_page_html(html)#soup.find('section', {'class': 'zn-body-text'}).getText()

        return article_headline, article_text
    
    def _find_articleheadline_in_page_html(self, html):
        if html is None:
            logger.warning('Called _find_articleheadline_in_page_html with null HTML')
            return None
        soup = BS(html, 'html.parser')
        headline_tag = soup.find('h1', {"class": "headline__text"})
        if headline_tag is None: 
            return None
        return headline_tag.getText()
    
    def _find_articletext_in_page_html(self, html):
        soup = BS(html, 'html.parser')
        paragraph_html_tags = soup.find_all('p')
        story_text = [] 
        for tag in paragraph_html_tags: 
            # At time of writing, all `p` elements with `paragraph` class are part of the story
            if tag.get('class') is not None and 'paragraph' in tag.get('class'):
                story_text.append(tag.getText())
        full_text = ''.join(story_text) 
        return full_text

    def set_source_to_cnn(self, stories):
        """
        Set 'source' value of stories to 'cnn'
        """
        for story in stories:
            story.source = 'cnn'
        return stories

    def set_date_to_today(self, stories):
        """
        set 'date' value of stories to current day
        """
        for story in stories:
            story.date = str(date.today())
        return stories

    def validate_stories(self, stories):
        """
        Apply final data validations before writing to database
        """
        validated_stories = []

        for story in stories:
            story_dump = StoryValidator().dump(story)
            errors = StoryValidator().validate(story_dump)
            if len(errors) == 0:
                validated_stories.append(story)
            else:
                logger.info(f'errors are {errors}')

        return validated_stories
