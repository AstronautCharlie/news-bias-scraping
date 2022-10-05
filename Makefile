# Runs and Builds

build-backend: 
	docker-compose --profile backend build 

run-backend: 
	docker-compose --profile backend up 

build-dynamodb:
	docker-compose --profile dynamo_db build 

run-dynamodb: 
	docker-compose --profile dynamo_db up 

build-data: # selenium and scraper
	docker-compose --profile data build

run-data:
	docker-compose --profile data up

build-selenium:
	docker-compose build -d selenium

run-selenium:
	docker-compose up -d selenium

# Utility

clean: 
	docker-compose down --remove-orphans

test: clean
	docker-compose run --rm backend_shell 'python3.9 -m pytest'

build-sandbox: 
	docker-compose build sandbox

run-sandbox: 
	docker-compose up sandbox