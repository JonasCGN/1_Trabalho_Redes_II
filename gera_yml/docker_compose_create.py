import yaml
from jinja2 import Environment, FileSystemLoader

def main():
    # Carregar configuração
    with open('config.yaml') as f:
        config = yaml.safe_load(f)

    # Processar roteadores (calcular IPs dos vizinhos)
    routers = []
    for router in config['routers']:
        neighbors = []
        for neighbor in router['neighbors']:
            # Encontrar roteador vizinho
            neighbor_router = next(r for r in config['routers'] if r['id'] == neighbor['id'])
            # Encontrar rede compartilhada
            shared_network = next(n['name'] for n in router['networks'] if n['name'] in [rn['name'] for rn in neighbor_router['networks']])
            # Pegar IP do vizinho na rede compartilhada
            neighbor_ip = next(n['ip'] for n in neighbor_router['networks'] if n['name'] == shared_network)
            neighbors.append(f'"{neighbor["id"]}":["{neighbor_ip}",{neighbor["cost"]}]')
        
        routers.append({
            **router,
            'neighbors_str': ','.join(neighbors)
        })

    # Carregar template
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('docker-compose.j2')

    # Gerar docker-compose.yml
    output = template.render(
        routers=routers,
        hosts=config['hosts'],
        networks=config['networks']
    )

    with open('../docker-compose.yml', 'w') as f:
        f.write(output)

if __name__ == '__main__':
    main()