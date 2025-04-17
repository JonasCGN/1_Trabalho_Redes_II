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
            neighbor_router = next(r for r in config['routers'] if r['id'] == neighbor['id'])
            neighbor_ip = neighbor_router['networks'][0]['ip']
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