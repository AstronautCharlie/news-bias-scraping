build-backend: 
	docker-compose --profile backend build 

run-backend: 
<<<<<<< HEAD
	docker-compose --profile backend up 

clean: 
	docker-compose down --remove-orphans

test: clean
	docker-compose run --rm backend_shell 'python3.9 -m pytest'
=======
	docker-compose --profile backend up 
>>>>>>> cc4b6667d568b24d1e3c1e8723644f78b005b94d
