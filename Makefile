build-backend: 
	docker-compose --profile backend build 

run-backend: 
	docker-compose --profile backend up 

clean: 
	docker-compose down --remove-orphans

test: clean
	docker-compose run --rm backend_shell 'python3.9 -m pytest'