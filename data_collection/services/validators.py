from marshmallow import Schema, fields, validates, ValidationError

class StoryValidator(Schema):
    url = fields.String()
    link_headline = fields.String()
    article_headline = fields.String()
    article_text = fields.String()
    date = fields.String()
    source = fields.String()

    @validates("article_text")
    def validate_article_text(self, article_text):
        if article_text is None or article_text == '': 
            raise ValidationError(f'Article text is empty')