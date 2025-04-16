import yaml
import ipaddress

def gerar_yaml(num_roteadores, hosts_por_rede):
    redes = []
    roteadores = []
    hosts = []

    base_ip = ipaddress.IPv4Network("172.21.0.0/16")
    subnets = list(base_ip.subnets(new_prefix=24))

    # Geração das redes
    for i in range(num_roteadores):
        rede_nome = f"rede{i+1}"
        subnet = subnets[i]
        gateway = subnet.network_address + 1

        redes.append({
            'name': rede_nome,
            'subnet': str(subnet),
            'gateway': str(gateway)
        })

        # Hosts nessa rede
        for j in range(hosts_por_rede):
            ip_host = subnet.network_address + 10 + j
            hosts.append({
                'name': f'h{i+1}{chr(97+j)}',  # h1a, h1b, etc
                'network': rede_nome,
                'ip': str(ip_host)
            })

    # Geração dos roteadores (2 redes por roteador, em anel)
    for i in range(num_roteadores):
        id_roteador = f"roteador{i+1}"

        idx1 = i
        idx2 = (i + 1) % num_roteadores
        rede1 = redes[idx1]
        rede2 = redes[idx2]

        ip1 = ipaddress.IPv4Address(rede1['gateway']) + 1
        ip2 = ipaddress.IPv4Address(rede2['gateway']) + 2

        nets = [
            {'name': rede1['name'], 'ip': str(ip1)},
            {'name': rede2['name'], 'ip': str(ip2)}
        ]

        neighbors = [
            {'id': f'roteador{((i - 1) % num_roteadores) + 1}', 'cost': 10},
            {'id': f'roteador{((i + 1) % num_roteadores) + 1}', 'cost': 10}
        ]

        roteadores.append({
            'id': id_roteador,
            'networks': nets,
            'neighbors': neighbors
        })

    # Estrutura final
    dados = {
        'networks': redes,
        'routers': roteadores,
        'hosts': hosts
    }

    # Gerar YAML
    with open('config.yaml', 'w') as file:
        yaml.dump(dados, file, sort_keys=False, default_flow_style=False)

    print("Arquivo 'config.yaml' gerado com sucesso!")

gerar_yaml(6, 6)
