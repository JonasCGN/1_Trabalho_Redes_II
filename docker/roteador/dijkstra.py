from collections import deque

def verifica_vizinhos(origem, lsdb, inativos=[]):
    # Filtra LSDB removendo roteadores inativos e seus vizinhos
    lsdb_filtrada = {}
    for router_id, dados in lsdb.items():
        if router_id in inativos:
            continue
        vizinhos_filtrados = {
            viz_id: viz_info
            for viz_id, viz_info in dados["vizinhos"].items()
            if viz_id not in inativos
        }
        lsdb_filtrada[router_id] = {
            "id": dados["id"],
            "ip": dados["ip"],
            "seq": dados["seq"],
            "vizinhos": vizinhos_filtrados
        }

    # Verifica se o roteador de origem está na LSDB filtrada
    if origem not in lsdb_filtrada:
        print("Origem inativa ou não encontrada.")
        return []

    # Inicializa fila e visitados para BFS (Busca em Largura)
    fila = deque([origem])
    visitados = set([origem])
    vizinhos_acessiveis = []

    while fila:
        atual = fila.popleft()

        # Para cada vizinho do roteador atual, adiciona à fila se ele não foi visitado
        for vizinho in lsdb_filtrada[atual]["vizinhos"]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                fila.append(vizinho)
                vizinhos_acessiveis.append(vizinho)

    # Caso não encontrem vizinhos acessíveis, tenta retornar os vizinhos diretamente conectados (que não estão inativos)
    if not vizinhos_acessiveis:
        print(f"Roteador {origem} não tem vizinhos acessíveis devido aos inativos.")
        # Agora, vamos buscar outros roteadores para possíveis rotas alternativas
        # Retorna os vizinhos diretamente conectados (se houver) que não estão inativos
        for vizinho, info in lsdb_filtrada[origem]["vizinhos"].items():
            if vizinho not in inativos:
                vizinhos_acessiveis.append(vizinho)
                
        return vizinhos_acessiveis

    return vizinhos_acessiveis

def dijkstra(origem, lsdb, inativos=[]):
    # 1. Construir grafo ignorando roteadores inativos e seus vizinhos
    grafo = {}
    for router_id, lsa in lsdb.items():
        if router_id in inativos:
            continue
        vizinhos_filtrados = {
            viz: info['custo']
            for viz, info in lsa['vizinhos'].items()
            if viz not in inativos
        }
        grafo[router_id] = vizinhos_filtrados

    # 2. Inicializar estruturas
    distancias = {router: float('inf') for router in grafo}
    distancias[origem] = 0
    anteriores = {router: None for router in grafo}
    visitados = set()

    while len(visitados) < len(grafo):
        atual = min((router for router in grafo if router not in visitados), key=lambda r: distancias[r])
        for vizinho, custo in grafo[atual].items():
            if vizinho not in visitados:
                if distancias[atual] == float('inf'):
                    nova_distancia = custo
                else:
                    nova_distancia = distancias[atual] + custo
                    
                if vizinho in distancias.keys() and nova_distancia < distancias[vizinho]:
                    distancias[vizinho] = nova_distancia
                    anteriores[vizinho] = atual
        
        visitados.add(atual)

    # 4. Construir tabela de rotas (descobrir próximo salto)
    tabela_rotas = {}
    for destino in grafo:
        if destino == origem:
            continue
        atual = destino
        anterior = anteriores[atual]
        if anterior is None:
            continue
        while anteriores[anterior] is not None and anteriores[anterior] != origem:
            anterior = anteriores[anterior]
        if anteriores[anterior] == origem:
            tabela_rotas[destino] = anterior
        else:
            tabela_rotas[destino] = anterior if anterior != destino else atual

    tabela_rotas = {destino: prox for destino, prox in tabela_rotas.items() if prox != origem}

    # 5. Mostrar tabela
    print("\nTabela de Roteamento:")
    for destino, prox in tabela_rotas.items():
        print(f"Destino: {destino}, Próximo Salto: {prox}")

    
    return tabela_rotas

if __name__ == "__main__":
    
    # Exemplo de uso
    lsdb = {
        'roteador1': {
            'id': 'roteador1',
            'ip': '172.21.0.2',
            'vizinhos': {
                'roteador8': {'ip': '172.21.7.2', 'custo': 10},
                'roteador2': {'ip': '172.21.1.2', 'custo': 10}
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
        'roteador3': {
            'id': 'roteador3',
            'ip': '172.21.2.2',
            'vizinhos': {
                'roteador2': {'ip': '172.21.1.2', 'custo': 10},
                'roteador4': {'ip': '172.21.3.2', 'custo': 10}
            },
            'seq': 3
        },
        'roteador4': {
            'id': 'roteador4',
            'ip': '172.21.3.2',
            'vizinhos': {
                'roteador3': {'ip': '172.21.2.2', 'custo': 10},
                'roteador5': {'ip': '172.21.4.2', 'custo': 10}
            },
            'seq': 4
        },
        'roteador5': {
            'id': 'roteador5',
            'ip': '172.21.4.2',
            'vizinhos': {
                'roteador4': {'ip': '172.21.3.2', 'custo': 10},
                'roteador6': {'ip': '172.21.5.2', 'custo': 10}
            },
            'seq': 5
        },
        'roteador6': {
            'id': 'roteador6',
            'ip': '172.21.5.2',
            'vizinhos': {
                'roteador5': {'ip': '172.21.4.2', 'custo': 10},
                'roteador7': {'ip': '172.21.6.2', 'custo': 10}
            },
            'seq': 6
        },
        'roteador7': {
            'id': 'roteador7',
            'ip': '172.21.6.2',
            'vizinhos': {
                'roteador6': {'ip': '172.21.5.2', 'custo': 10},
                'roteador8': {'ip': '172.21.7.2', 'custo': 10}
            },
            'seq': 7
        },
        'roteador8': {
            'id': 'roteador8',
            'ip': '172.21.7.2',
            'vizinhos': {
                'roteador7': {'ip': '172.21.6.2', 'custo': 10},
                'roteador1': {'ip': '172.21.0.2', 'custo': 10}
            },
            'seq': 8
        }
    }
    inativos = []
    print("Vizinhos acessíveis:", verifica_vizinhos("roteador1", lsdb, inativos))
    print(f"Roteador {inativos} inativo, recalculando rotas.")
    print(dijkstra("roteador1", lsdb,inativos))
    # dijkstra("roteador1", lsdb)