import subprocess
import json
import os

class VizinhosManager:
    def __init__(self):
        self.ROTEADOR_ID = os.getenv("ROTEADOR_ID")
        self.VIZINHOS = json.loads(os.getenv("VIZINHOS"))
        self.vizinhos_inativos = []
        
    def verifica_tcp(self, ip):
        try:
            resultado = subprocess.run(f"ping -c 1 -W 0.1 {ip}", shell=True, check=True, text=True, capture_output=True)
            return resultado.returncode == 0
        except subprocess.CalledProcessError:
            return False

    def verifica_roteadores_ativos(self,lsdb):
        for roteador, dados in list(lsdb.items()):  # Cria uma cópia do dicionário para iteração segura
            if not self.verifica_tcp(dados["ip"]):
                print(f"[{self.ROTEADOR_ID}] Roteador {roteador} inativo.")
                return False
            else:
                print(f"[{self.ROTEADOR_ID}] Roteador {roteador} ativo.")
        return True
    
    def atualiza_status_vizinhos(self):
        self.vizinhos_inativos = []
        
        for roteador, (ip, _) in self.VIZINHOS.items():
            if self.verifica_tcp(ip):
                print(f"[{self.ROTEADOR_ID}] Roteador vizinho {roteador} ativo.")
            else:
                self.vizinhos_inativos.append(roteador)
                print(f"[{self.ROTEADOR_ID}] Roteador vizinho {roteador} inativo.")