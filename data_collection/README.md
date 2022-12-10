# Data
This folder holds all code responsible for generating data for the service.

# What does it do? 
For now, it:
- scrapes Fox and CNN Homepages (see `scraping/scrapers/cnn_scraper.py` and `scraping/scrapers/fox_scraper.py`)

Next it will: 
- write to AWS

# How do I run this? 
## Environment Variables
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`: 
If running locally - i.e., using `localstack-dynamodb` instead of actually writing to AWS - set to `abc`, `xyz`, `us-east-2` respectively
If writing to cloud - set to values in AWS console

## Code changes
`settings.py`
If running locally, `DYNAMO_ENDPOINT=http://localstack-dynamodb:4566`. 
If writing to cloud, `DYNAMO_ENDPOINT=dynamodb.us-east-2.amazonaws.com`

## Run containers
```
make data-collection
```