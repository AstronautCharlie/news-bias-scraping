# Main method
run: 
	make data-collection

# Runs and Builds

build-data-collection: # scraper and selenium
	docker-compose --profile data build

data-collection: build-data-collection
	docker-compose --profile data up

data-collector: build-data-collection
	docker-compose up -d data-collection

run-localstack:
	docker-compose up -d localstack

build-dynamodb:
	docker-compose --profile dynamo_db build 

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

run-selenium:
	docker-compose up selenium
