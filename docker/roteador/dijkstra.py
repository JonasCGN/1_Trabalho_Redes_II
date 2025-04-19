def dijkstra(origem,lsdb):
    # 1. Construir o grafo corretamente incluindo todos os roteadores
    tabela_ip = {}
    tabela_ip = {viz: info["ip"] for viz, info in lsdb.items()}
    for _,valores in lsdb.items():
        for viz, info in valores["vizinhos"].items():
            tabela_ip[viz] = info["ip"]
                
    grafo = {}
    all_routers = set(lsdb.keys())
    
    for router_id, lsa in lsdb.items():
        vizinhos = lsa["vizinhos"]
        grafo[router_id] = {viz: info["custo"] for viz, info in vizinhos.items()}
        all_routers.update(vizinhos.keys())
        
    for router in all_routers:
        if router not in grafo:
            grafo[router] = {}
    
    distancias = {router: float('inf') for router in grafo}
    distancias[origem] = 0
    visitados = set()
    rotas = {router: None for router in grafo}
    
    while len(visitados) < len(grafo):
        atual = min((router for router in grafo if router not in visitados), key=lambda r: distancias[r])
        for vizinho, custo in grafo[atual].items():
            if vizinho not in visitados:
                if distancias[atual] == float('inf'):
                    nova_distancia = custo
                else:
                    nova_distancia = distancias[atual] + custo
                    
                if nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    rotas[vizinho] = atual
        
        visitados.add(atual)
    
    
    # tabela_rotas = {}
    # for destino in grafo:
    #     if destino != origem:
    #         prox_salto = destino
    #         while rotas[prox_salto] != origem and rotas[prox_salto] is not None:
    #             prox_salto = rotas[prox_salto]
    #         if rotas[prox_salto] is not None:
    #             tabela_rotas[destino] = prox_salto
    
    # Montar tabela de rotas
    tabela_rotas = {}

    for destino in grafo:
        if destino != origem:
            # Se o destino for um vizinho direto, redireciona para o próximo salto direto
            if origem in lsdb and destino in lsdb[origem]["vizinhos"]:
                tabela_rotas[destino] = origem
            else:
                # Se não for vizinho direto, redireciona para o vizinho mais próximo
                atual = destino
                while rotas[atual] != origem and rotas[atual] is not None:
                    atual = rotas[atual]

                # Atual aqui representa o próximo salto após o vizinho
                if origem in lsdb and "vizinhos" in lsdb[origem] and atual in lsdb[origem]["vizinhos"]:
                    tabela_rotas[destino] = atual
            
    print("Tabela de Roteamento:")
    for destino, prox_salto in tabela_rotas.items():
        print(f"Destino: {destino}, Próximo Salto: {prox_salto}")
    
    return tabela_rotas

if __name__ == "__main__":
    # Exemplo de uso
    lsdb = {
        'roteador1': {
            'id': 'roteador1',
            'ip': '172.21.0.2',
            'vizinhos': {
                'roteador2': {'ip': '172.21.1.2', 'custo': 10},
                'roteador6': {'ip': '172.21.5.2', 'custo': 15}
            },
            'seq': 1
        },
        'roteador2': {
            'id': 'roteador2',
            'ip': '172.21.1.2',
            'vizinhos': {
                'roteador1': {'ip': '172.21.0.2', 'custo': 10},
                'roteador3': {'ip': '172.21.2.2', 'custo': 10}
            },
            'seq': 2
        },
        # 'roteador3': {
        #     'id': 'roteador3',
        #     'ip': '172.21.2.2',
        #     'vizinhos': {
        #         'roteador2': {'ip': '172.21.1.2', 'custo': 10},
        #         'roteador4': {'ip': '172.21.3.2', 'custo': 5}
        #     },
        #     'seq': 3
        # },
        # 'roteador4': {
        #     'id': 'roteador4',
        #     'ip': '172.21.3.2',
        #     'vizinhos': {
        #         'roteador3': {'ip': '172.21.2.2', 'custo': 5},
        #         'roteador5': {'ip': '172.21.4.2', 'custo': 10}
        #     },
        #     'seq': 4
        # },
        # 'roteador5': {
        #     'id': 'roteador5',
        #     'ip': '172.21.4.2',
        #     'vizinhos': {
        #         'roteador4': {'ip': '172.21.3.2', 'custo': 15},
        #         'roteador6': {'ip': '172.21.5.2', 'custo': 10}
        #     },
        #     'seq': 5
        # },
        'roteador6': {
            'id': 'roteador6',
            'ip': '172.21.5.2',
            'vizinhos': {
                'roteador5': {'ip': '172.21.4.2', 'custo': 10},
                'roteador1': {'ip': '172.21.0.2', 'custo': 15}
            },
            'seq': 2
        }
    }
    dijkstra("roteador1", lsdb)
