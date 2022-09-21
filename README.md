# News Bias 

## What is this? 
`data` - handles generating data. Scrapes news sources and puts data into DynamoDB
`backend` - processes requests from `frontend` and fetches from `data`
`frontend` - takes user requests

## How do I run this? 
Set `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` environment variables to whatever those should be. 

Then 
```
make build-backend
make run-backend
```