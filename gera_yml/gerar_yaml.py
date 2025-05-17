import os
import random
import yaml
import ipaddress
import sys

def gerar_yaml(num_roteadores, hosts_por_rede, topologia="anel"):
    if num_roteadores < 3:
        raise ValueError("Número de roteadores deve ser pelo menos 3.")
    if hosts_por_rede < 1 or hosts_por_rede > 254:
        raise ValueError("Número de hosts por rede deve ser entre 1 e 254.")

    redes = []
    roteadores = []
    hosts = []

    base_ip = ipaddress.IPv4Network("172.21.0.0/16")
    subnets = list(base_ip.subnets(new_prefix=24))
    
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
            router_ip = subnet.network_address + 2
            
            hosts.append({
                'name': f'host{i+1}{chr(97+j)}',  # h1a, h1b, etc
                'network': rede_nome,
                'router': str(router_ip),
                'ip': str(ip_host)
            })

    for i in range(num_roteadores):
        id_roteador = f"roteador{i+1}"

        networks = []
        neighbors = []

        # Topologia gerada corretamente
        if topologia == "anel":
            rede_host = redes[i]
            ip_host_rede = ipaddress.IPv4Address(rede_host['gateway']) + 1
            networks.append({'name': rede_host['name'], 'ip': str(ip_host_rede)})
                
            rede = [redes[(i + offset) % num_roteadores]for offset in [1,-1]]
            
            ip_ant = ipaddress.IPv4Address(rede[1]['gateway']) + 3
            ip_prox = ipaddress.IPv4Address(rede[0]['gateway']) + 2
            
            networks.append({'name': rede[0]['name'], 'ip': str(ip_prox)})
            networks.append({'name': rede[1]['name'], 'ip': str(ip_ant)})

            neighbors = [
                {'id': f'roteador{((i - 1) % num_roteadores) + 1}', 'cost': 10},
                {'id': f'roteador{((i + 1) % num_roteadores) + 1}', 'cost': 10}
            ]

        elif topologia == "estrela":
            rede_host = redes[i]
            ip_host_rede = ipaddress.IPv4Address(rede_host['gateway']) + 1
            networks.append({'name': rede_host['name'], 'ip': str(ip_host_rede)})

            if i == 0:
                # Roteador central conecta com todos
                for j in range(1, num_roteadores):
                    rede_vizinho = redes[j]
                    ip_vizinho = ipaddress.IPv4Address(rede_vizinho['gateway']) + 2
                    networks.append({'name': rede_vizinho['name'], 'ip': str(ip_vizinho)})
                    neighbors.append({'id': f'roteador{j+1}', 'cost': 10})
            else:
                # Roteadores periféricos conectam só com o central
                ip_central = ipaddress.IPv4Address(redes[0]['gateway']) + 3 + (i-1)
                networks.append({'name': redes[0]['name'], 'ip': str(ip_central)})
                neighbors.append({'id': 'roteador1', 'cost': 10})

        elif topologia == "totalmente_conectada":
            # Todos conectados a todos
            rede_host = redes[i]
            ip_host_rede = ipaddress.IPv4Address(rede_host['gateway']) + 1
            networks.append({'name': rede_host['name'], 'ip': str(ip_host_rede)})

            for j in range(num_roteadores):
                if j != i:
                    rede_vizinho = redes[j]
                    ip_vizinho = ipaddress.IPv4Address(rede_vizinho['gateway']) + 2 + i
                    networks.append({'name': rede_vizinho['name'], 'ip': str(ip_vizinho)})
                    neighbors.append({'id': f'roteador{j+1}', 'cost': 10})

        elif topologia == "tree":
            # Árvore binária sem criar novas redes ponto-a-ponto
            rede_host = redes[i]
            ip_host_rede = ipaddress.IPv4Address(rede_host['gateway']) + 1
            networks.append({'name': rede_host['name'], 'ip': str(ip_host_rede)})

            left = 2 * i + 1
            right = 2 * i + 2

            if left < num_roteadores:
                rede_vizinho = redes[left]
                ip_vizinho = ipaddress.IPv4Address(rede_vizinho['gateway']) + 2
                networks.append({'name': rede_vizinho['name'], 'ip': str(ip_vizinho)})
                neighbors.append({'id': f'roteador{left+1}', 'cost': 10})

            if right < num_roteadores:
                rede_vizinho = redes[right]
                ip_vizinho = ipaddress.IPv4Address(rede_vizinho['gateway']) + 2
                networks.append({'name': rede_vizinho['name'], 'ip': str(ip_vizinho)})
                neighbors.append({'id': f'roteador{right+1}', 'cost': 10})

            if i != 0:
                parent = (i - 1) // 2
                rede_pai = redes[parent]
                ip_pai = ipaddress.IPv4Address(rede_pai['gateway']) + 3 + (i - (2 * parent + 1))
                networks.append({'name': rede_pai['name'], 'ip': str(ip_pai)})
                neighbors.append({'id': f'roteador{parent+1}', 'cost': 10})
                
        elif topologia == "linha":
            rede_host = redes[i]
            ip_host_rede = ipaddress.IPv4Address(rede_host['gateway']) + 1
            networks.append({'name': rede_host['name'], 'ip': str(ip_host_rede)})

            # Se houver próximo roteador
            if i < num_roteadores - 1:
                rede_prox = redes[i + 1]
                ip_prox = ipaddress.IPv4Address(rede_prox['gateway']) + 2
                networks.append({'name': rede_prox['name'], 'ip': str(ip_prox)})
                neighbors.append({'id': f'roteador{i+2}', 'cost': 10})

            # Se houver roteador anterior
            if i > 0:
                rede_ant = redes[i - 1]
                ip_ant = ipaddress.IPv4Address(rede_ant['gateway']) + 3
                networks.append({'name': rede_ant['name'], 'ip': str(ip_ant)})
                neighbors.append({'id': f'roteador{i}', 'cost': 10})
                
        else:
            raise ValueError(f"Topologia '{topologia}' não suportada.")

        roteadores.append({
            'id': id_roteador,
            'ip': str(networks[0]['ip']),	
            'networks': networks,
            'neighbors': neighbors
        })

    dados = {
        'networks': redes,
        'routers': roteadores,
        'hosts': hosts
    }

    with open('config.yaml', 'w') as file:
        yaml.dump(dados, file, sort_keys=False, default_flow_style=False)

    print(f"✅ Arquivo 'config.yaml' gerado com sucesso para topologia '{topologia}'!")

class Args:
    def __init__(self, qtd_roteador, qtd_hosts, topologia):
        self.qtd_roteador = qtd_roteador
        self.qtd_hosts = qtd_hosts
        self.topologia = topologia

def ler_args(argc, argv):
    if argc < 3:
        print("Uso: <qtd_roteador> <qtd_hosts> <topologia>")
        qtd_roteador = 6
        qtd_hosts = 2
        topologia = "anel"
        print(f"Usando valores padrão: qtd_roteador={qtd_roteador}, qtd_hosts={qtd_hosts}, topologia={topologia}")	
    else:
        print(f"Uso: {argv[0]} <qtd_roteador> <qtd_hosts> <topologia>")
        print(argv)
        qtd_roteador = int(argv[1])
        qtd_hosts = int(argv[2]) 
        topologia = argv[3] if argc > 3 else "anel"
    return Args(qtd_roteador, qtd_hosts, topologia)

def main():
    args = ler_args(len(sys.argv), sys.argv)
    
    gerar_yaml(args.qtd_roteador, args.qtd_hosts, topologia=args.topologia)
    
if __name__ == "__main__":
    main()