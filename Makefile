# Main method
run: 
	make data-collection

# Runs and Builds

build-data-collection: # scraper and selenium
	docker-compose --profile data build

data-collection: build-data-collection
	docker-compose --profile data up

run-localstack:
	docker-compose up -d localstack

build-dynamodb:
	docker-compose --profile dynamo_db build 

dynamodb: build-dynamodb
	docker-compose --profile dynamodb up

# Utility

clean: 
	docker-compose down --remove-orphans

# test: clean run-selenium
# 	timeout 15
# 	cd data_collection
# 	python -m pytest
# 	docker kill selenium 
# 	docker rm selenium

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

test: 
	pytest . -vv
