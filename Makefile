# Runs and Builds

build-backend: 
	docker-compose --profile backend build 

run-backend: 
	docker-compose --profile backend up 

build-dynamodb:
	docker-compose --profile dynamo_db build 

build-data: # selenium and scraper
	docker-compose --profile data build

run-data:
	docker-compose --profile data up

build-selenium:
	docker-compose build selenium

run-selenium:
	docker-compose up selenium

build-data-collection:
	docker-compose --profile data build

data-collection: build-data-collection
	docker-compose --profile data up

data-collector: build-data-collector
	docker-compose up -d data-collection

run-localstack:
	docker-compose up -d localstack

dynamodb: build-dynamodb
	docker-compose --profile dynamodb up

# Utility

clean: 
	docker-compose down --remove-orphans

test: clean
	docker-compose run --rm backend_shell 'python3.9 -m pytest'

build-sandbox: 
	docker-compose build sandbox

run-sandbox: 
	docker-compose up sandbox

run-setup:
	docker-compose --profile setup up

build:
	docker-compose -f docker-compose.yml build

run: build
	docker-compose -f docker-compose.yml up
