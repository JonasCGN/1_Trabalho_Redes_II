all:
	@cd gera_yml && python gerar_yaml.py
	@cd gera_yml && python docker_compose_create.py
	@docker-compose up --build
	# @docker-compose up -d --build --remove-orphans

down:
	@docker-compose down 
	

clean:
	docker compose down --rmi all --volumes --remove-orphans

teste_ping:
	@cls
	@cd docker/roteador/script_teste && python teste_ping.py

teste_rotas:
	@cls
	@cd docker/roteador/script_teste && python teste_rotas.py

teste_vias:
	@cls
	@cd docker/roteador/script_teste && python teste_vias.py

teste_ping_host:
	@cls
	@cd docker/host/script_teste && python teste_ping.py