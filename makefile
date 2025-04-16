all:
	@python docker_compose_create.py
	@python gerar_yaml.py
	@docker-compose up --build
	# @docker-compose up -d --build --remove-orphans

clean:
	docker compose down --rmi all --volumes --remove-orphans