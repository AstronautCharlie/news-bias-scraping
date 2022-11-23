"""
TODO: 
- Add opinion/analysis tagging 

NOTE: 
- If using selenium to get html, refer to following StackOverflow: 
https://stackoverflow.com/questions/47060735/selenium-remote-webdriver-not-working-with-aws-ec2
"""

from bs4 import BeautifulSoup
import requests 
#from requests_html import HTMLSession
import re
from datetime import date

# Switched from requests_html to Selenium
from selenium import webdriver 
from selenium.webdriver.common.by import By

class FoxScraper(): 
    def __init__(self): 
        page = requests.get('https://www.foxnews.com')
        self.soup = BeautifulSoup(page.text, 'html.parser')

    # ----------------------------------
    # Getting Article URLs from Homepage
    # ---------------------------------- 
    def get_topline_stories(self): 
        # Returns dictionary {url->headline} where 
        #  stories are in order of appearance (headline first) 

        # Headline section containing lead and follow ups 
        topline_group = self.soup.find(class_='collection collection-spotlight has-hero')
        topline_group = topline_group.find(class_='info')

        # This section works if there is only one headline 
        try: 
            # Get the headline story (link + hyperlink text)
            headline = topline_group.find(class_='title title-color-default')
            headline_url = headline.find(href=True)

            # Headline story hyperlink text 
            headline_hyperlink_text = headline_url.string.replace('\n', '')        
            # URL to headline story 
            headline_story_url = headline_url.get('href')
            
            # Flag that there is only one headline
            one_headline_flag = True 

        except: 
            # Get all the stuff!
            #headline_section = topline_group.find(class_='info')
            
            links = topline_group.find_all(href=True)
            headline_headlines = [] 
            headline_urls = [] 
            for l in links: 
                if l.string: 
                    headline_headlines.append(l.string.replace('\n',''))
                    headline_urls.append(l.get('href'))

            one_headline_flag = False 

        # Get the follow-up stories (link + hyperlink text)
        followup = topline_group.find(class_='content')
        followup = followup.find(class_='related')
        followup = followup.find_all(href=True)
        followup_hyperlink_text = [] 
        followup_story_url = [] 
        for f in followup: 
            followup_hyperlink_text.append(f.string.replace('\n', ''))
            followup_story_url.append(f.get('href'))

        # Return links + story titles for topline stories
        if one_headline_flag:
            followup_hyperlink_text.insert(0, headline_hyperlink_text)
            followup_story_url.insert(0, headline_story_url)
            return dict(zip(followup_story_url, followup_hyperlink_text))
        else: 
            # Yes this is hacky as shit - done to preserve order; not sure if it matters 
            headline_headlines.extend(followup_hyperlink_text)
            headline_urls.extend(followup_story_url)
            return dict(zip(headline_urls, headline_headlines))

#        return dict(zip(followup_story_url, followup_hyperlink_text))

    def get_secondary_stories(self):
        """
        Returns a dictionary of {url->headline} for each of the secondary stories, 
            i.e. those in the 'collection collection-spotlight' class 
        """
        # Get all the secondary stories in the block below headline stuff 
        secondary_stories = self.soup.find(class_='collection collection-spotlight')
        secondary_stories = secondary_stories.find(class_='content')
        secondary_soup = BeautifulSoup(str(secondary_stories), 'html.parser')
        #secondary_story_list = secondary_soup.find_all(class_='info')
        
        # Extract the relevant links from each story, ignoring generic headers 
        secondary_headlines = [] 
        secondary_urls = [] 
        #for s in secondary_story_list: 
            
            # Get Top banner - should always be there 
        try:
            secondary_story_list = secondary_soup.find_all(class_='info')
            for s in secondary_story_list:
                title = s.find(class_='title title-color-default')
                link = title.find(href=True)
                headline = link.string.replace('\n', '')
                url = link.get('href')
                secondary_headlines.append(headline)
                secondary_urls.append(url)

                # Get related headline - may sometimes not exist 
                related = s.find(class_='related')
                if related: 
                    link = related.find(href=True)
                    headline = link.string.replace('\n', '')
                    url = link.get('href')
                    secondary_headlines.append(headline)
                    secondary_urls.append(url)
        except:
            secondary_stories = secondary_soup.find_all(href=True)
            for s in secondary_stories: 
                if s.string: 
                    secondary_headlines.append(s.string.replace('\n',''))
                    secondary_urls.append(s.get('href'))
                

        return dict(zip(secondary_urls, secondary_headlines))

    def get_tertiary_stories(self): 
        """
        Returns a dictionary of {url->headline} for each of the tertiary stories, 
            i.e. those in the 'main main-secondary' class 
        """
        # Get all tertiary stories in the ribbon below secondary 
        tertiary_story_html = self.soup.find(class_='main main-secondary')
        tertiary_story_html = tertiary_story_html.find(class_='content article-list')
        tertiary_soup = BeautifulSoup(str(tertiary_story_html), 'html.parser')
        tertiary_stories = tertiary_soup.find_all('article', class_=re.compile('^article story-'))

        # Get the headlines/urls from each story 
        tertiary_headlines = [] 
        tertiary_urls = [] 
        for t in tertiary_stories: 
            story = t.find(class_='info')
            story = story.find(class_='title title-color-default')
            link = story.find(href=True)
            headline = link.string.replace('\n', '')
            url = link.get('href')
            tertiary_headlines.append(headline)
            tertiary_urls.append(url) 

        return dict(zip(tertiary_urls, tertiary_headlines))


    # ---------------
    # Article Parsing
    # --------------- 
    def parse_article(self, page_html):
        """
        input: html of an article page
        output: article as a string 
        """
        # Load html into soup parser 
        soup = BeautifulSoup(page_html, 'html.parser')
        article_body = soup.find(class_='article-body')
        paragraphs = [] 
        
        # Grab all the paragraphs from the article 
        if article_body and article_body.contents: 
            for c in article_body.contents: 
                if c.name == 'p' and c.strong is None: 
                    paragraphs.append(c) 

        # Parse paragraphs and combine into one string 
        article = '' 
        for p in paragraphs: 
            contents = p.contents 
            for c in contents: 
                if c.string: 
                    sentence = c.string
                    article += sentence
            article += ' '

        return article 

    def parse_articles_from_urls(self, url_list):
        """
        input: list of URLs to articles 
        output: dictionary mapping urls to articles as strings
        """
        results = {} 
        # Get HTML for each URL and parse for article contents 
        for url in url_list: 
            page = requests.get(url)
            if (page.status_code // 100) != 2: 
                raise ValueError(f'URL {url} returned non-200 status code: {page.status_code}')
            article_text = self.parse_article(page.text)
            article_text = article_text.replace('  ', ' ')
            article_text = article_text.replace(u'\xa0', u' ')
            results[url] = article_text 
        return results 

    # -------------------------------------------------------
    # Central method - scrape website and create JSON objects
    #  for MongoDB
    # -------------------------------------------------------
    def scrape(self):
        """
        Scrape and parse all articles from foxnews.com and 
        create dictionary for each one containing: 
            - URL
            - Headline
            - Date [note this is just the date of script runtime - 
                    when adding to DB, check that record doesn't already 
                    exist]
            - Source (always 'fox')
            - Article 
            - Placement ('headline', 'main' [4 photos beneath headline], 'secondary' [long ribbon at bottom])

        output: list of dictionaries in JSON form  
        """
        
        # Get story URLs from homepage, keeping track of where they came from 
        url_to_placement = {} 
        url_to_headline = self.get_topline_stories()
        for u in url_to_headline.keys(): 
            url_to_placement[u] = 'headline'
        secondary_url_to_headline = self.get_secondary_stories()
        for u in secondary_url_to_headline.keys(): 
            url_to_placement[u] = 'main'
        url_to_headline.update(secondary_url_to_headline)
        tertiary_url_to_headline = self.get_tertiary_stories()
        for u in tertiary_url_to_headline.keys(): 
            url_to_placement[u] = 'secondary'
        url_to_headline.update(tertiary_url_to_headline)
        urls = list(url_to_headline.keys())

        # Parse each URL for article 
        url_to_article = self.parse_articles_from_urls(urls)

        # Combine into results 
        results = [] 
        for url in urls: 
            # Ignore articles with no content 
            if url_to_article[url] is not None and url_to_article[url] != '': 
                record = {
                    'url': url,
                    'headline': url_to_headline[url],
                    'date': date.today(),
                    'article': url_to_article[url],
                    'source': 'fox',
                    'placement': url_to_placement[url]
                }
                results.append(record) 

        return results 

# Used for testing only 
if __name__ == '__main__': 
    
    # ---------------
    # Test FoxScraper
    # ---------------

    fs = FoxScraper()

    # Test scraping secondary stories 
    #fs.get_secondary_stories()

    # Test scraping tertiary stories from front page 
    #fs.get_tertiary_stories()

    # Test 'scrape' method, should return all stories 
    results = fs.scrape() 
    for r in results: 
        print(f'\n\n{r}\n\n')
