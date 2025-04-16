import threading
import time
import socket
import json
import os
from dijkstra import dijkstra

ROTEADOR_ID = os.getenv("ROTEADOR_ID")
VIZINHOS = json.loads(os.getenv("VIZINHOS"))  # {"roteador2": ["192.168.100.2", 10]}

LSDB = {}  # { "roteador1": {vizinhos..., seq: 1} }

PORTA_LSA = 5000

def adicionar_rotas(tabela):
    for destino, prox_salto in tabela.items():
        ip_destino = f"192.168.{destino.split('R')[1]}.1"  # Simples mapeamento
        ip_prox_salto = f"192.168.{prox_salto.split('R')[1]}.1"
        comando = f"route add {ip_destino} mask 255.255.255.0 {ip_prox_salto}"
        os.system(comando)  # Executa o comando no sistema
        print(f"[{ROTEADOR_ID}] Adicionada rota para {ip_destino} via {ip_prox_salto}")

def atualizar_tabela():
    while True:
        time.sleep(10)
        tabela = dijkstra(ROTEADOR_ID, LSDB)  # Obtém a tabela de rotas
        print(f"[{ROTEADOR_ID}] Nova tabela de rotas:")
        
        # Adiciona as rotas no sistema
        for destino, prox_salto in tabela.items():
            print(f"  {destino} → via {prox_salto}")
        
        # Adiciona as rotas com o comando `route add`
        adicionar_rotas(tabela)  # Passa a tabela como argumento

def enviar_lsa():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seq = 0
    while True:
        seq += 1
        lsa = {
            "id": ROTEADOR_ID,
            "vizinhos": {
                viz: {"ip": ip, "custo": custo}
                for viz, (ip, custo) in VIZINHOS.items()
            },
            "seq": seq
        }
        mensagem = json.dumps(lsa).encode()
        for viz, (ip, _) in VIZINHOS.items():
            sock.sendto(mensagem, (ip, PORTA_LSA))
        time.sleep(5)

def receber_lsa():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORTA_LSA))
    while True:
        dados, _ = sock.recvfrom(4096)
        lsa = json.loads(dados.decode())
        origem = lsa["id"]
        if origem not in LSDB or lsa["seq"] > LSDB[origem]["seq"]:
            LSDB[origem] = lsa
            print(f"[{ROTEADOR_ID}] Atualizou LSDB com LSA de {origem}")

def iniciar_threads():
    t1 = threading.Thread(target=enviar_lsa)
    t2 = threading.Thread(target=receber_lsa)
    t3 = threading.Thread(target=atualizar_tabela)

    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    
    t1.start()
    t2.start()
    t3.start()

    while True:
        time.sleep(10)

if __name__ == "__main__":
    print(f"[{ROTEADOR_ID}] Iniciado com vizinhos: {VIZINHOS}")
    iniciar_threads()
