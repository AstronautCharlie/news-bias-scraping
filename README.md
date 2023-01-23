# News Bias Scrapers

# What does this do? 
Scrapes stories from cnn.com and foxnews.com and writes them to DynamoDB

# How do I run this? 
## Environment Variables
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`: 
If writing to cloud - set to values in AWS console. If not, no need to set 

## Code changes
`settings.py`, #switches section at top

## Run containers
```
make data-collection
```

# What's next to do? 
This works locally - scrapes from CNN and Fox and writes to DynamoDB just fine. Next is to deploy it to ECS and set it to run every hour. 