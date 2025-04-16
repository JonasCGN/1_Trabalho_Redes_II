all:
	@python docker_compose_create.py
	@docker compose up --build

clean:
	docker compose down --rmi all --volumes --remove-orphans