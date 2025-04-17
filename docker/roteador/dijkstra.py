def dijkstra(origem,lsdb):
    # 1. Construir o grafo corretamente incluindo todos os roteadores
    # lsdb = {
    #     'roteador6': {
    #         'id': 'roteador6', 
    #         'ip': '172.21.5.2', 
    #         'vizinhos': {
    #             'roteador5': {'ip': '172.21.4.2', 'custo': 10}, 
    #             'roteador1': {'ip': '172.21.0.2', 'custo': 10}
    #         }, 
    #         'seq': 2
    #     }, 
    #     'roteador2': {
    #         'id': 'roteador2', 
    #         'ip': '172.21.1.2', 
    #         'vizinhos': {
    #               'roteador1': {'ip': '172.21.0.2', 'custo': 10}, 
    #               'roteador3': {'ip': '172.21.2.2', 'custo': 10}
    #            }, 
    #           'seq': 2
    #        },
    # }
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
    tabela_rotas = {}
    for destino, prox_salto in rotas.items():
        if prox_salto is not None:
            # tabela_rotas[tabela_ip[destino]] = tabela_ip[prox_salto]
            tabela_rotas[destino] = prox_salto
    
    return tabela_rotas

if __name__ == "__main__":
    # Exemplo de uso
    dijkstra("roteador1",{})