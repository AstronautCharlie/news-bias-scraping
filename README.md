# News Bias Scrapers

# What is this? 
This repo defines how news sites are scraped for stories. It is intended to run in AWS ECS, to run every hour, writing stories to DynamoDB

# What does this do? 
Scrapes stories from cnn.com and foxnews.com and writes them to either a local instance of DynamoDB, or an actual DynamoDB table on AWS, depending on the configuration

# How do I run this? 
## Set Environment Variables
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`: 
If writing to cloud - set to values in AWS console. If not, no need to set 

`NEWSAPI_API_KEY`: 
Set this to the API key from `NewsAPI.org` - this is the API used to fetch stories 

## Set Configuration
Go to `settings.py` and set the value of `RUN_LOCALLY` in the `# Switches` block, depending on whether or not you want the scraper to write stories to a local DynamoDB instance or AWS. 

## Run containers
```
make run
```

# How do I test this? 
```
make test
```
Note that the selenium container MUST be running for tests to work - `make test` will spin up the container, wait for some time for the container to spin up, and then run the tests.

# TroubleShooting
### Error
```
botocore.exceptions.ClientError: An error occurred (UnrecognizedClientException) when calling the BatchWriteItem operation: The security token included in the request is invalid.
```

### Fixes
Make sure environment variables `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are set to the appropriate values.

# What's next to do? 
Fix base scraper test, then write FoxScraper and CnnScraper to implement `scrape_article_text_from_url` to pull article text from websites of those formats. 
