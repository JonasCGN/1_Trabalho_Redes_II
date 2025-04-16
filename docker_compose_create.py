import yaml

def gerar_docker_compose(num_roteadores, num_hosts):
    serviços = {}

    # Definir o nome da rede
    redes = {
        f"rede{i+1}": {
            'driver': 'bridge',
            'ipam': {
                'config': [
                    {'subnet': f'172.21.{i+1}.0/24', 'gateway': f'172.21.{i+1}.1'}
                ]
            }
        }
        for i in range(num_roteadores)
    }

    # Gerar serviços para os roteadores
    for i in range(num_roteadores):
        serviços[f"roteador{i+1}"] = {
            'build': {'context': './docker/roteador', 'dockerfile': 'Dockerfile'},
            'container_name': f'roteador{i+1}',
            'environment': [
                f'ROTEADOR_ID=roteador{i+1}',
                f'VIZINHOS={{}}'  # Inicialmente sem vizinhos, vamos preencher dinamicamente
            ],
            'networks': {f'rede{i+1}': {'ipv4_address': f'172.21.{i+1}.2'}}
        }

    # Gerar serviços para os hosts
    for i in range(num_hosts):
        rede_associada = f'rede{(i % num_roteadores) + 1}'
        serviços[f'host{i+1}'] = {
            'build': {'context': './docker/host', 'dockerfile': 'Dockerfile'},
            'container_name': f'host{i+1}',
            'networks': {rede_associada: {'ipv4_address': f'172.21.{(i % num_roteadores) + 1}.{i+10}'}} 
        }

    # Criar o docker-compose final
    compose = {
        'version': '3.8',
        'services': serviços,
        'networks': redes
    }

    # Salvar o arquivo docker-compose.yml
    with open('docker-compose.yml', 'w') as file:
        yaml.dump(compose, file, default_flow_style=False)

    print("docker-compose.yml gerado com sucesso!")

# Exemplo de uso
gerar_docker_compose(3, 6)
