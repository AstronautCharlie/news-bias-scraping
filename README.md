# News Bias 

## What is this? 
`data_collection` - handles generating data. Scrapes news sources and puts data into DynamoDB. Currently pulls homepage stories from CNN and Fox News. 
`backend` - processes requests from `frontend`

## What's Next?
- Frontend to handle user requests

## Need More Docs? 
See READMEs in subfolders

## Trouble Shooting
- Is Docker Desktop Up? If you see this, maybe not:
```
ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively
refused it
```
- Is Selenium running? Is the Docker Container up? 