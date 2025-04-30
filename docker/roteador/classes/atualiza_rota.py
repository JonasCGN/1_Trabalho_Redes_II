import subprocess
import os
from classes.manipulacao import Manipulacao
from classes.gerenciador_rota import GerenciadorDeRotas

class AtualizadorDeRotas:
    def __init__(self,gerenciador_de_rotas:GerenciadorDeRotas):
        self.ROTEADOR_ID = os.getenv("ROTEADOR_ID")
        self.gerenciador_de_rotas = gerenciador_de_rotas

    def atualizar_rota(self, tabela):
        for destino, prox_salto in tabela.items():
            
            ip_destino = self.gerenciador_de_rotas.lsdb[destino]['ip']
            ip_prox_salto = self.gerenciador_de_rotas.lsdb[prox_salto]['ip']
            
            destino_subnet = Manipulacao.extrair_subnet_roteador_ip(ip_destino)
            gateway_roteador = Manipulacao.extrair_ip_roteadores_ip(ip_prox_salto)
            
            comando = f"ip route replace {destino_subnet} via {gateway_roteador}"
            print(f"[{self.ROTEADOR_ID}] Executando: {comando}")
            
            result = subprocess.run(comando, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[{self.ROTEADOR_ID}] Erro: {result.stderr.strip()}")
            else:
                print(f"[{self.ROTEADOR_ID}] Rota atualizada: {result.stdout.strip()}")

    def recalcular_rotas(self,inativos):
        self.gerenciador_de_rotas.set_inativos(inativos)
        
        tabela = self.gerenciador_de_rotas.dijkstra(self.ROTEADOR_ID)
        if tabela:
            print(f"[{self.ROTEADOR_ID}] Nova tabela de rotas:")
            for destino, prox_salto in tabela.items():
                print(f"  {destino} → via {prox_salto}")
            self.atualizar_rota(tabela)
        else:
            print(f"[{self.ROTEADOR_ID}] Nenhuma rota encontrada.")