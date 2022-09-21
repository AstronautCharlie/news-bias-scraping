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

# -----------
# CNN Scraper
# -----------

class CnnScraper(): 
    """
    #TODO: fix placement misclassification of middle column stories with no bullet point follow-ups 
    """
    def __init__(self):
        """
        Because CNN has scripts executing at load time, use HTMLSession class from 
        requests_html package to get page context post-script
        """

        # Removed in favor of selenium 
        """
        print('Using requests-html to get cnn.com')
        s = HTMLSession()
        r = s.get('https://www.cnn.com')
        r.html.render() 
        page_text = r.html.find('body')[0]
        self.soup = BeautifulSoup(str(page_text.html), 'html.parser')
        """
        #print('Using selenium to get cnn.com')
        options = webdriver.ChromeOptions()
        #options.binary_location = '/usr/bin/google-chrome'
        options.add_argument('headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.cnn.com')
        html_element = driver.find_element(By.TAG_NAME, 'body')
        #html_element = driver.find_element_by_tag_name('body')
        html_text = html_element.get_attribute('innerHTML')
        self.soup = BeautifulSoup(str(html_text), 'html.parser')

        # all urls are given as stems off this base url
        self.base_url = 'https://www.cnn.com'
    
    # ----------------------------------
    # Getting Article URLs from Homepage 
    # ----------------------------------

    def parse_column(self, column_html):
        """
        Helper function to parse a column in the headline section        
        Returns list of 3-item dictionaries with keys 'placement' 'headline' 'url' 
        Excludes any article that links to a video by checking if '/video/' is in the URL 
        """

        results = [] 

        # Check for banner, parse if exists 
        banner = column_html.find('a', {'class': 'link-banner'})
        if banner: 
            banner_headline = banner.text
        else: 
            banner_headline = None 
        
        # Parse each li in the list 
        lis = column_html.find_all('li')
        i = 0 
        for li in lis: 
            #print(li.prettify())
            # Content lives in the div with class = 'cd__content' 
            content = li.find('div', {'class': 'cd__content'})
            # If no content, then it's an empty row
            if not content: 
                continue 
            # Check if content has bullet points in the 'cd__description' div (i.e. in column 2, probably)
            bullet_check = content.find('div', {'class': 'cd__description'})
            if bullet_check: # in this case, must parse cd__headline and cd__description divs separately 
                # TODO 
                # Find headline, h3 class='cd__headline', get 'a', pull href and text
                headline_wrapper = content.find('h3', {'class': 'cd__headline'})
                headline = headline_wrapper.find('a', href=True)
                # Check that URL leads with www.cnn.com, if not append to front
                headline_url = headline.get('href')
                if 'www.cnn.com' not in headline_url: 
                    headline_url = self.base_url + headline_url  
                item = {'placement': 'headline', 'headline': headline.text, 'url': headline_url}
                if '/videos/' not in (self.base_url + headline.get('href')):
                    results.append(item)
                # Find followups under headline, find div class='cd__description'
                # find all 'a', pull href and text
                follow_up_wrapper = content.find('div', {'class': 'cd__description'})
                follow_ups = follow_up_wrapper.find_all('a', href=True)
                #print(follow_ups)
                for f in follow_ups: 
                    if f.text and len(f.text) > 0 and not str.isspace(f.text):
                        # Check that URL starts with www.cnn.com, if not append to front 
                        url = f.get('href')
                        if 'www.cnn.com' not in url: 
                            url = self.base_url + url
                        item = {'placement': 'main', 'headline': f.text, 'url': url}
                        #print(item)
                        if '/videos/' not in f.get('href'):
                            results.append(item)
            else: # in this case, one 'a' tag with both partial url and text 
                # TODO this
                # find h3 class='cd__headline'
                #  find 'a' (should be just one), pull href and text 
                #print(content.prettify())
                headline_wrapper = content.find('h3', {'class': 'cd__headline'})
                headline = headline_wrapper.find('a', href=True)
                headline_text = headline.text
                # Check that url leads with 'https://www.cnn.com/' 
                headline_url = headline.get('href')
                if 'www.cnn.com' not in headline_url: 
                    headline_url = self.base_url + headline_url
                # First story in columns 1 & 3 is headline, rest are main 
                headline_placement = 'headline' if i == 0 else 'main' 
                # Check if i = 0, and banner_headline; if so, then append banner_headline to first headline
                if i == 0 and banner_headline:
                    headline_text = banner_headline + ' ' + headline_text 
                item = {'placement': headline_placement, 'headline': headline_text, 'url': headline_url}
                #print(item)
                if '/videos/' not in headline_url:
                    results.append(item) 
            i += 1 
        return results

    def get_topline_stories(self):
        """
        Returns list of 3-item dictionaries with 'placement', 'headline', and 'url'
        """
        results = [] 

        # Define and get topline section 
        section_id = 'homepage1-zone-1'  
        page_section = self.soup.find('section', {'id': section_id})

        # Loop over the 3 columns that make up the headline section 
        column_classes = ['zn__column--idx-0', 'zn__column--idx-1', 'zn__column--idx-2']
        for col in column_classes: 
            col_html = page_section.find('div', {'class': col})
            # 'headlines' is a list of 3-item dictionaries, keys = {'placement', 'headline', 'url'}
            headlines = self.parse_column(BeautifulSoup(str(col_html), 'html.parser'))
            results.extend(headlines)
        
        return results 
    
    # ----------------------
    # Parse Article from URL 
    # ----------------------
    def parse_article_from_url(self, article_url):
        """
        Scrape text from article, given article url 
        """

        #print('\n\n')
        #print('About to search for', article_url)
        #print('\n\n')
        print('scraping url:', article_url)
        try: 
            r = requests.get(article_url)
        except Exception as e: 
            print('Connection error with url', article_url, '; retrying w/o "https://www.cnn.com"')
            try: 
                r = requests.get(article_url.replace(self.base_url, ''))
                print('Success! Used url', article_url)
            except Exception as e: 
                print('Failed again; skipping article, return no text')
                return None 
        page_text = r.text 
        soup = BeautifulSoup(page_text, 'html.parser')
        article_body = soup.find('div', {'itemprop': 'articleBody'})
        text = '' 
        if not article_body: 
            return text  
        

        # Grab all paragraphs
        paragraph_class = 'zn-body__paragraph'
        paragraphs = article_body.find_all(class_=paragraph_class)

        # String them together 
        for p in paragraphs: 
            if len(p.text) > 0 and not str.isspace(p.text): 
                text += p.text.replace('(CNN)', '') + ' '
        
        return text 

    # ------------------
    # Main Scrape Method 
    # ------------------
    def scrape(self): 
        """
        #TODO Expand to secondary 
        Scrape and parse all articles from cnn.com and 
        create dictionary for each one containing: 
            - URL
            - Headline
            - Date 
            - Article 
            - Source (always 'cnn')
            - Placement ('headline' (bold, top of page) or 'main' (top of page, not bold)

        output: list of dictionaries
        """
        results = [] 

        # Compile json objects 
        article_meta = self.get_topline_stories() # list of dictionaries w/ placement, headline, url
        for a in article_meta: 
            article_text = self.parse_article_from_url(a['url'])
            article_date = date.today() 
            new_item = {'placement': a['placement'],
                        'url': a['url'],
                        'headline': a['headline'],
                        'article': article_text,
                        'date': article_date,
                        'source': 'cnn'}
            # Don't add empty items: 
            if len(new_item['article']) > 0 and not str.isspace(new_item['article']):
                results.append(new_item) 
        
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

    # ---------------
    # Test CnnScraper
    # ---------------
    """
    cnn_s = CnnScraper()
    stories = cnn_s.scrape() 

    for s in stories: 
        for k, v in s.items(): 
            print(k,'\n\n', v)
        print('\n\n\n\n\n\n')
    """
