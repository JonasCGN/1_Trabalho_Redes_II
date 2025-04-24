from collections import deque
import heapq

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
    # Filtra roteadores inativos do LSDB
    grafo = {}
    for router_id, dados in lsdb.items():
        if router_id in inativos:
            continue
        vizinhos = {
            viz: info['custo']
            for viz, info in dados['vizinhos'].items()
            if viz not in inativos
        }
        grafo[router_id] = vizinhos

    if origem not in grafo:
        print(f"[dijkstra] Origem {origem} não está no grafo.")
        return {}

    dist = {router: float('inf') for router in grafo}
    prev = {router: None for router in grafo}
    dist[origem] = 0

    heap = [(0, origem)]

    while heap:
        custo_atual, atual = heapq.heappop(heap)

        if custo_atual > dist[atual]:
            continue

        for vizinho, peso in grafo[atual].items():
            nova_dist = dist[atual] + peso
            if vizinho in dist.keys() and nova_dist < dist[vizinho]:
                dist[vizinho] = nova_dist
                prev[vizinho] = atual
                heapq.heappush(heap, (nova_dist, vizinho))

    # Calcula o próximo salto para cada destino
    tabela_rotas = {}
    for destino in grafo:
        if destino == origem or dist[destino] == float('inf'):
            continue
        atual = destino
        while prev[atual] != origem:
            atual = prev[atual]
            if atual is None:
                break
        if atual:
            tabela_rotas[destino] = atual
            
    tabela_rotas = {destino: prox for destino, prox in tabela_rotas.items() if prox != destino}

    return tabela_rotas

def calcular_caminho(tabela_de_rotas, origem, destino, caminho_atual=None):
    if caminho_atual is None:
        caminho_atual = [origem]
    
    # Se a origem for igual ao destino, retornamos o caminho encontrado
    if origem == destino:
        return caminho_atual

    # Caso contrário, verificamos os próximos saltos
    if origem not in tabela_de_rotas or destino not in tabela_de_rotas[origem]:
        return None  # Se não houver um próximo salto, o caminho não é válido
    
    # Recursivamente adicionamos o próximo salto ao caminho
    proximo_salto = tabela_de_rotas[origem][destino]
    novo_caminho = caminho_atual + [proximo_salto]
    
    # Recorremos para o próximo salto até o destino
    return calcular_caminho(tabela_de_rotas, proximo_salto, destino, novo_caminho)

def exibir_caminhos(tabela_de_rotas):
    for origem in tabela_de_rotas:
        print(f"✅ Roteador: {origem}")
        for destino in tabela_de_rotas[origem]:
            caminho = calcular_caminho(tabela_de_rotas, origem, destino)
            if caminho:
                caminho_completo = " ➜ ".join(caminho)
                print(f"Destino: {destino}\tPróximo Salto: {tabela_de_rotas[origem][destino]}\tCaminho Completo: {caminho_completo}")
            else:
                print(f"Destino: {destino}\tPróximo Salto: {tabela_de_rotas[origem][destino]}\tCaminho Completo: Caminho inválido")
        print()

# Exemplo de uso:
# Supondo que sua lista de tabelas seja como a que você mostrou
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

    # Lista de roteadores inativos para teste
    inativos = ['roteador4']

    print("Vizinhos acessíveis:", verifica_vizinhos("roteador1", lsdb, inativos))
    
    lista_caminhos = {}
    
    # Atualiza as rotas levando em consideração os inativos
    for roteador in lsdb.keys():
        # print(roteador)
        lista_caminhos[roteador] = dijkstra(roteador, lsdb, inativos)
        
    # print(lista_caminhos)
    # exibir_caminhos(lista_caminhos)
