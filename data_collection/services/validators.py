from marshmallow import Schema, fields, validates, ValidationError

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('validator')

class StoryValidator(Schema):
    url = fields.String(required=True)
    link_headline = fields.String()
    article_headline = fields.String()
    article_text = fields.String(required=True)
    date = fields.String(required=True)
    source = fields.String(required=True)

    @validates("article_text")
    def validate_article_text(self, article_text):
        if article_text is None or article_text == '': 
            raise ValidationError(f'Article text is empty')

    def validate_stories(self, stories):
        """
        Pick out the valid stories from the given list and return them. Handle any errors
        """
        deduped_stories = self._dedup_stories(stories)

        story_dumps = [story.dump() for story in deduped_stories]

        errors = self.validate(story_dumps, many=True)
        if len(errors) == 0:
            return deduped_stories
        else: 
            valid_stories = []
            for i in range(len(deduped_stories)): 
                if i not in errors:
                    valid_stories.append(deduped_stories[i])
            self.handle_errors(errors, deduped_stories)
            return valid_stories

    def _dedup_stories(self, stories):
        """
        Remove stories with the same URL, defaulting to the story earlier in the list
        since that roughly corresponds to higher up on the page

        The primary instance where this occurs is when headlines above and below a 
        picture link to the same story. In that case, the headline above the picture
        (which is more prominent on the website), should come first in the list of 
        stories since it's scraped first
        """
        dup_indexes = [] 
        urls = [story.url for story in stories]

        for i in range(len(urls)):
            url = urls[i]
            for j in range(i+1, len(urls)):
                if url == urls[j]:
                    dup_indexes.append(j)

        deduped_stories = []
        
        for i in range(len(stories)):
            if i not in dup_indexes:
                deduped_stories.append(stories[i])
        
        return deduped_stories

    def handle_errors(self, errors, items):
        for err_num in errors:
            error_item = items[err_num]
            logger.info(f'story failed validation: url: {error_item.url}\n{errors[err_num]}')
