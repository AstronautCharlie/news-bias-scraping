import boto3 
import re 
import nltk 
from nltk.tokenize import word_tokenize 
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from boto3.dynamodb.conditions import Key 
from datetime import date, timedelta 

def main_handler(event, handler): 

    # Define stopwords
    STOPWORDS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
            'ourselves', 'you', "you're", "you've", "you'll",
            "you'd", 'your', 'yours', 'yourself', 'yourselves', 
            'he', 'him', 'his', 'himself', 'she', "she's", 'her', 
            'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 
            'them', 'their', 'theirs', 'themselves', 'what', 'which', 
            'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 
            'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 
            'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 
            'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
            'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'to', 
            'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 
            'under', 'again', 'further', 'then', 'once', 'here',
            'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 
            'each', 'few', 'more', 'most', 'other', 'some', 'such', 
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
            "don't", 'should', "should've", 'now', 'd', 'll', 'm', 
            'o', 're', 've', 'y', 'ain', 'aren', "aren't", 
            'couldn', "couldn't", 'didn', "didn't", 'doesn', 
            "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 
            'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 
            'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
            'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
    # Define pattern for removing punctuation 
    punct_pattern = "[^0-9A-Za-z ]"
    STOPWORDS = [re.sub(punct_pattern,"",w) for w in STOPWORDS] 


    print('Top of Main')
    # Get Articles that haven't been cleaned 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Articles')
    cleaned_table = dynamodb.Table('ArticlesCleaned')

    # Get all articles from past day (plus a 30 minute buffer period)
    yesterday = date.today() - timedelta(days=1)
    fe = Key('date').between(str(yesterday), str(date.today()))
    entries = table.scan(FilterExpression=fe)['Items']

    i = 0 
    # Clean articles 
    for e in entries: 
        # Remove punctuation 
        article_text = e['article']
        cleaned_text = re.sub(punct_pattern,"",article_text)
        if i == 0: 
            print(article_text,'\n\n\n')

        # Make lower case 
        cleaned_text = cleaned_text.lower()

        # Tokenize into words 
        tokens = word_tokenize(cleaned_text)
        
        # Remove stop words 
        #stopwords = nltk.corpus.stopwords.words('english')
        tokens = [t for t in tokens if t not in STOPWORDS]
        if i == 0:
            print(tokens, '\n\n\n')
        
        # Lemmatize words 
        wn = nltk.WordNetLemmatizer()
        tokens = [wn.lemmatize(t) for t in tokens]
        if i == 0: 
            print(tokens, '\n\n\n')

        # Push item to ArticlesCleaned
        cleaned_table.put_item(
            Item={
                'url': e['url'],
                'headline': e['headline'],
                'source': e['source'],
                'date': str(e['date']),
                'cleaned_article': tokens,
                'placement': e['placement']
            }
        )
        i += 1 

if __name__ == '__main__': 
    main_handler(None, None)