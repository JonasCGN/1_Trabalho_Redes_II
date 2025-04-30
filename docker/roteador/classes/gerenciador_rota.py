import heapq

class GerenciadorDeRotas:
    def __init__(self, lsdb,inativos=[]):
        self.lsdb = lsdb
        self.inativos = inativos

    def set_inativos(self, inativos):
        self.inativos = inativos

    def _gerar_grafo(self):
        grafo = {}
        for router_id, dados in self.lsdb.items():
            if router_id in self.inativos:
                continue
            vizinhos = {
                viz: info['custo']
                for viz, info in dados['vizinhos'].items()
                if viz not in self.inativos
            }
            grafo[router_id] = vizinhos
        return grafo

    def dijkstra(self, origem):
        grafo = self._gerar_grafo()

        print(f"[Dijkstra] Inativos: {self.inativos}")
        
        if origem not in grafo:
            print(f"[Dijkstra] Origem {origem} não encontrada no grafo.")
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

        # Evita que o próximo salto seja o próprio destino
        tabela_rotas = {destino: prox for destino, prox in tabela_rotas.items() if prox != destino}
        
        return tabela_rotas

    def calcular_todas_rotas(self):
        self.tabela_de_rotas = {}
        for roteador in self.lsdb.keys():
            self.tabela_de_rotas[roteador] = self.dijkstra(roteador)

    def calcular_caminho(self, origem, destino, caminho_atual=None):
        if caminho_atual is None:
            caminho_atual = [origem]
        
        if origem == destino:
            return caminho_atual

        if origem not in self.tabela_de_rotas or destino not in self.tabela_de_rotas[origem]:
            return None
        
        proximo_salto = self.tabela_de_rotas[origem][destino]
        novo_caminho = caminho_atual + [proximo_salto]
        
        return self.calcular_caminho(proximo_salto, destino, novo_caminho)

    def exibir_caminhos(self):
        for origem in self.tabela_de_rotas:
            print(f"✅ Roteador: {origem}")
            for destino in self.tabela_de_rotas[origem]:
                caminho = self.calcular_caminho(origem, destino)
                if caminho:
                    caminho_completo = " ➜ ".join(caminho)
                    print(f"Destino: {destino}\tPróximo Salto: {self.tabela_de_rotas[origem][destino]}\tCaminho Completo: {caminho_completo}")
                else:
                    print(f"Destino: {destino}\tCaminho inválido")
            print()

if __name__ == "__main__":
    
    # Exemplo de uso
    lsdb = {
    'roteador1': {
        'id': 'roteador1',
        'ip': '172.21.0.2',
        'vizinhos': {
            'roteador5': {'ip': '172.21.4.2', 'custo': 10},
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
            'roteador1': {'ip': '172.21.0.2', 'custo': 10}
        },
        'seq': 5
    }
}

    # Lista de roteadores inativos para teste
    inativos = ['roteador3']

    # print("Vizinhos acessíveis:", verifica_vizinhos("roteador1", lsdb, inativos))
    
    lista_caminhos = {}
    roteador = GerenciadorDeRotas(lsdb,inativos)
    # Atualiza as rotas levando em consideração os inativos
    # for roteador in lsdb.keys():
    #     # print(roteador)
    #     lista_caminhos[roteador] = dijkstra(roteador, lsdb, inativos)
    
    print(roteador.dijkstra('roteador4'))
    # print(roteador.dijkstra('roteador4', lsdb, []))
