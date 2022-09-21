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
from settings import ScraperConfig

logger = logging.getLogger(__name__)

class CnnScraper(BaseScraper): 
    def __init__(self, selenium_endpoint=ScraperConfig.SELENIUM_ENDPOINT):
        super(CnnScraper, self).__init__(selenium_endpoint=selenium_endpoint)
        self._selenium_endpoint = selenium_endpoint

    def run(self):
        return self.scrape_stories_from_homepage

    def scrape_stories_from_homepage(self):
        """
        Scrape stories from the CNN homepage.

        Return list of Stories
        """
        html = self.scrape_rendered_html(ScraperConfig.CNN_HOMEPAGE)
        story_items = self.extract_homepage_stories_from_html(html)
        
        return story_items

    def extract_homepage_stories_from_html(self, html):
        """
        Get stories from CNN html

        Return list of Stories
        """
        # List of sections on the CNN homepage that contain links to scrape
        homepage_sections = [
            'zn-homepage-injection-zone-1', # Ticker at top
            'zn-hompage1-zone-1', # First section of regular articles
            'zn-hompage2-zone-1', # Second section scrolling down
            'zn-homepage2-zone-2',
        ]

        stories = [] 
        
        for section in homepage_sections: 
            partial_stories = self.scrape_url_link_headline(html, section)
            story = self.populate_article_text_headline_from_url(partial_stories)
            stories.append(story)

        return stories 

    def scrape_url_link_headline(self, 
                        page_html,
                        class_name, 
                        html_type='section',
                        exclude_empty_headlines=True):
        """
        Get url and link_headline for all homepage Stories

        Return list of Stories (partially populated)
        """
        stories = [] 

        soup = BS(page_html)
        section_html = soup.find(html_type, {'class': class_name})
        links = section_html.find_all('a', href=True)

        for l in links: 
            link_headline = l.getText()
            url = l.get('href')
            if (link_headline != '') or exclude_empty_headlines:
                new_story = Story(link_headline=link_headline, url=url)
                stories.append(new_story)
        
        return stories
    
    def populate_article_text_headline_from_url(self, story):
        """
        Populate article_text and article_headline fields of Story from url field

        Returns Story
        """
        if story.url is None: 
            logging.error('Story url is undefined - cannot populate article')
            return story
        
        article_headline, article_text = self._scrape_article_headline_text_from_url(story.url)
        story.article_headline = article_headline
        story.article_text = article_text
        
        return story 

    def _scrape_article_headline_text_from_url(self, url):
        """
        Returns string (headline), string(article_text)
        """
        html = self.driver.get(url)
        soup = BS(html)
        article_headline = soup.find('h1', {'class': 'pg-headline'}).getText()
        article_text = soup.find('section', {'class': 'zn-body-text'}).getText()
        
        return article_headline, article_text

# class CnnScraper(): 
#     """
#     #TODO: fix placement misclassification of middle column stories with no bullet point follow-ups 
#     """
#     def __init__(self):
#         """
#         Because CNN has scripts executing at load time, use HTMLSession class from 
#         requests_html package to get page context post-script
#         """

#         # Removed in favor of selenium 
#         """
#         print('Using requests-html to get cnn.com')
#         s = HTMLSession()
#         r = s.get('https://www.cnn.com')
#         r.html.render() 
#         page_text = r.html.find('body')[0]
#         self.soup = BeautifulSoup(str(page_text.html), 'html.parser')
#         """
#         #print('Using selenium to get cnn.com')
#         options = webdriver.ChromeOptions()
#         #options.binary_location = '/usr/bin/google-chrome'
#         options.add_argument('headless')
#         options.add_argument('--no-sandbox')
#         driver = webdriver.Chrome(options=options)
#         driver.get('https://www.cnn.com')
#         html_element = driver.find_element(By.TAG_NAME, 'body')
#         #html_element = driver.find_element_by_tag_name('body')
#         html_text = html_element.get_attribute('innerHTML')
#         self.soup = BeautifulSoup(str(html_text), 'html.parser')

#         # all urls are given as stems off this base url
#         self.base_url = 'https://www.cnn.com'
    
#     # ----------------------------------
#     # Getting Article URLs from Homepage 
#     # ----------------------------------

#     def parse_column(self, column_html):
#         """
#         Helper function to parse a column in the headline section        
#         Returns list of 3-item dictionaries with keys 'placement' 'headline' 'url' 
#         Excludes any article that links to a video by checking if '/video/' is in the URL 
#         """

#         results = [] 

#         # Check for banner, parse if exists 
#         banner = column_html.find('a', {'class': 'link-banner'})
#         if banner: 
#             banner_headline = banner.text
#         else: 
#             banner_headline = None 
        
#         # Parse each li in the list 
#         lis = column_html.find_all('li')
#         i = 0 
#         for li in lis: 
#             #print(li.prettify())
#             # Content lives in the div with class = 'cd__content' 
#             content = li.find('div', {'class': 'cd__content'})
#             # If no content, then it's an empty row
#             if not content: 
#                 continue 
#             # Check if content has bullet points in the 'cd__description' div (i.e. in column 2, probably)
#             bullet_check = content.find('div', {'class': 'cd__description'})
#             if bullet_check: # in this case, must parse cd__headline and cd__description divs separately 
#                 # TODO 
#                 # Find headline, h3 class='cd__headline', get 'a', pull href and text
#                 headline_wrapper = content.find('h3', {'class': 'cd__headline'})
#                 headline = headline_wrapper.find('a', href=True)
#                 # Check that URL leads with www.cnn.com, if not append to front
#                 headline_url = headline.get('href')
#                 if 'www.cnn.com' not in headline_url: 
#                     headline_url = self.base_url + headline_url  
#                 item = {'placement': 'headline', 'headline': headline.text, 'url': headline_url}
#                 if '/videos/' not in (self.base_url + headline.get('href')):
#                     results.append(item)
#                 # Find followups under headline, find div class='cd__description'
#                 # find all 'a', pull href and text
#                 follow_up_wrapper = content.find('div', {'class': 'cd__description'})
#                 follow_ups = follow_up_wrapper.find_all('a', href=True)
#                 #print(follow_ups)
#                 for f in follow_ups: 
#                     if f.text and len(f.text) > 0 and not str.isspace(f.text):
#                         # Check that URL starts with www.cnn.com, if not append to front 
#                         url = f.get('href')
#                         if 'www.cnn.com' not in url: 
#                             url = self.base_url + url
#                         item = {'placement': 'main', 'headline': f.text, 'url': url}
#                         #print(item)
#                         if '/videos/' not in f.get('href'):
#                             results.append(item)
#             else: # in this case, one 'a' tag with both partial url and text 
#                 # TODO this
#                 # find h3 class='cd__headline'
#                 #  find 'a' (should be just one), pull href and text 
#                 #print(content.prettify())
#                 headline_wrapper = content.find('h3', {'class': 'cd__headline'})
#                 headline = headline_wrapper.find('a', href=True)
#                 headline_text = headline.text
#                 # Check that url leads with 'https://www.cnn.com/' 
#                 headline_url = headline.get('href')
#                 if 'www.cnn.com' not in headline_url: 
#                     headline_url = self.base_url + headline_url
#                 # First story in columns 1 & 3 is headline, rest are main 
#                 headline_placement = 'headline' if i == 0 else 'main' 
#                 # Check if i = 0, and banner_headline; if so, then append banner_headline to first headline
#                 if i == 0 and banner_headline:
#                     headline_text = banner_headline + ' ' + headline_text 
#                 item = {'placement': headline_placement, 'headline': headline_text, 'url': headline_url}
#                 #print(item)
#                 if '/videos/' not in headline_url:
#                     results.append(item) 
#             i += 1 
#         return results

#     def get_topline_stories(self):
#         """
#         Returns list of 3-item dictionaries with 'placement', 'headline', and 'url'
#         """
#         results = [] 

#         # Define and get topline section 
#         section_id = 'homepage1-zone-1'  
#         page_section = self.soup.find('section', {'id': section_id})

#         # Loop over the 3 columns that make up the headline section 
#         column_classes = ['zn__column--idx-0', 'zn__column--idx-1', 'zn__column--idx-2']
#         for col in column_classes: 
#             col_html = page_section.find('div', {'class': col})
#             # 'headlines' is a list of 3-item dictionaries, keys = {'placement', 'headline', 'url'}
#             headlines = self.parse_column(BeautifulSoup(str(col_html), 'html.parser'))
#             results.extend(headlines)
        
#         return results 
    
#     # ----------------------
#     # Parse Article from URL 
#     # ----------------------
#     def parse_article_from_url(self, article_url):
#         """
#         Scrape text from article, given article url 
#         """

#         #print('\n\n')
#         #print('About to search for', article_url)
#         #print('\n\n')
#         print('scraping url:', article_url)
#         try: 
#             r = requests.get(article_url)
#         except Exception as e: 
#             print('Connection error with url', article_url, '; retrying w/o "https://www.cnn.com"')
#             try: 
#                 r = requests.get(article_url.replace(self.base_url, ''))
#                 print('Success! Used url', article_url)
#             except Exception as e: 
#                 print('Failed again; skipping article, return no text')
#                 return None 
#         page_text = r.text 
#         soup = BeautifulSoup(page_text, 'html.parser')
#         article_body = soup.find('div', {'itemprop': 'articleBody'})
#         text = '' 
#         if not article_body: 
#             return text  
        

#         # Grab all paragraphs
#         paragraph_class = 'zn-body__paragraph'
#         paragraphs = article_body.find_all(class_=paragraph_class)

#         # String them together 
#         for p in paragraphs: 
#             if len(p.text) > 0 and not str.isspace(p.text): 
#                 text += p.text.replace('(CNN)', '') + ' '
        
#         return text 

#     # ------------------
#     # Main Scrape Method 
#     # ------------------
#     def scrape(self): 
#         """
#         #TODO Expand to secondary 
#         Scrape and parse all articles from cnn.com and 
#         create dictionary for each one containing: 
#             - URL
#             - Headline
#             - Date 
#             - Article 
#             - Source (always 'cnn')
#             - Placement ('headline' (bold, top of page) or 'main' (top of page, not bold)

#         output: list of dictionaries
#         """
#         results = [] 

#         # Compile json objects 
#         article_meta = self.get_topline_stories() # list of dictionaries w/ placement, headline, url
#         for a in article_meta: 
#             article_text = self.parse_article_from_url(a['url'])
#             article_date = date.today() 
#             new_item = {'placement': a['placement'],
#                         'url': a['url'],
#                         'headline': a['headline'],
#                         'article': article_text,
#                         'date': article_date,
#                         'source': 'cnn'}
#             # Don't add empty items: 
#             if len(new_item['article']) > 0 and not str.isspace(new_item['article']):
#                 results.append(new_item) 
        
#         return results 


# All tests go here 
if __name__ == '__main__': 
    
    cnn_s = CnnScraper()
    stories = cnn_s.scrape() 

    for s in stories: 
        for k, v in s.items(): 
            print(k,'\n\n', v)
        print('\n\n\n\n\n\n')
    
