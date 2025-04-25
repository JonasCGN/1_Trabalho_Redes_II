import yaml
import ipaddress

def gerar_yaml(num_roteadores, hosts_por_rede):
    if num_roteadores < 3 or num_roteadores > 10:
        raise ValueError("Número de roteadores deve ser entre 3 e 10.")
    if hosts_por_rede < 1 or hosts_por_rede > 254:
        raise ValueError("Número de hosts por rede deve ser entre 1 e 254.")
    
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
                'name': f'host{i+1}{chr(97+j)}',  # h1a, h1b, etc
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

        if num_roteadores > 2:
            rede3 = redes[(i - 1) % num_roteadores]
            ip3 = ipaddress.IPv4Address(rede3['gateway']) + 3
            nets.append({'name': rede3['name'], 'ip': str(ip3)})


        neighbors = []
        if num_roteadores > 1:
            neighbors.append({'id': f'roteador{((i - 1) % num_roteadores) + 1}', 'cost': 10})
            neighbors.append({'id': f'roteador{((i + 1) % num_roteadores) + 1}', 'cost': 10})

        roteadores.append({
            'id': id_roteador,
            'ip': str(ip1),
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

gerar_yaml(8, 1)