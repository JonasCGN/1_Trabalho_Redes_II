all:
	@cd gera_yml && python gerar_yaml.py
	@cd gera_yml && python docker_compose_create.py
	@docker-compose up --build
	# @docker-compose up -d --build --remove-orphans

clean:
	docker compose down --rmi all --volumes --remove-orphans

teste_ping:
	@cd docker/roteador/script_teste && python teste_ping.py

teste_rotas:
	@cd docker/roteador/script_teste && python teste_rotas.py