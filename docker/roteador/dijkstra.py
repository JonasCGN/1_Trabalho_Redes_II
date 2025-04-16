import heapq

def dijkstra(roteador_id, lsdb):
    # Criar grafo a partir da LSDB
    grafo = {}
    for r_id, dados in lsdb.items():
        grafo[r_id] = {}
        for viz, info in dados["vizinhos"].items():
            grafo[r_id][viz] = info["custo"]

    # Inicializações
    dist = {n: float('inf') for n in grafo}
    prev = {n: None for n in grafo}
    dist[roteador_id] = 0
    fila = [(0, roteador_id)]

    while fila:
        custo_atual, atual = heapq.heappop(fila)
        for vizinho, peso in grafo.get(atual, {}).items():
            nova_dist = custo_atual + peso
            if nova_dist < dist[vizinho]:
                dist[vizinho] = nova_dist
                prev[vizinho] = atual
                heapq.heappush(fila, (nova_dist, vizinho))

    # Construir tabela de next-hops
    next_hop = {}
    for destino in grafo:
        if destino == roteador_id or prev[destino] is None:
            continue
        # Caminho reverso
        hop = destino
        while prev[hop] != roteador_id:
            hop = prev[hop]
        next_hop[destino] = hop

    return next_hop
