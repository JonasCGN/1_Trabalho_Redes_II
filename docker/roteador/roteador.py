import threading
import time
import socket
import json
import os 
import subprocess
from dijkstra import dijkstra

ROTEADOR_ID = os.getenv("ROTEADOR_ID")
ENDERECO_IP = os.getenv("ENDERECO_IP")
VIZINHOS = json.loads(os.getenv("VIZINHOS"))

PORTA_LSA = 5000

def adicionar_rotas(tabela):
    for destino, prox_salto in tabela.items():
        
        destino = f"172.21.{int(destino.split('r')[-1]) - 1}.0/24"
        prox_salto = f"172.21.{int(prox_salto.split('r')[-1]) - 1}.2"
        comando = f"ip route add {destino} via {prox_salto}".split()
        print(f"[{ROTEADOR_ID}] Executando: {comando}")
        try:
            subprocess.run(comando,capture_output=True,text=True,check=True)  # Executa o comando no sistema operacional
        except Exception as e:
            print(f"[{ROTEADOR_ID}] Erro ao adicionar rota: {e}") 

def atualizar_tabela(lsdb):
    while True:
        # print('Atualizar Tabela:',lsdb)
        tabela = {}
        if lsdb:
            tabela = dijkstra(ROTEADOR_ID, lsdb)  # Obtém a tabela de rotas
        
        if tabela:
            print(f"[{ROTEADOR_ID}] Nova tabela de rotas:")
            
            # Adiciona as rotas no sistema
            for destino, prox_salto in tabela.items():
                print(f"  {destino} → via {prox_salto}")
            
            adicionar_rotas(tabela) 
        else:
            print(f"[{ROTEADOR_ID}] Nenhuma rota encontrada.")
        time.sleep(5)

def enviar_lsa():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    seq = 0
    while True:
        seq += 1
        lsa = {
            "id": ROTEADOR_ID,
            "ip": ENDERECO_IP,
            "vizinhos": {
                viz: {"ip": ip, "custo": custo} for viz, (ip, custo) in VIZINHOS.items()
            },
            "seq": seq
        }
        print(f"[{ROTEADOR_ID}] Enviando LSA para: {VIZINHOS.keys()}")
        
        mensagem = json.dumps(lsa).encode()
        for viz, (ip, _) in VIZINHOS.items():
            sock.sendto(mensagem, (ip, PORTA_LSA))
        
        time.sleep(5)  

# -------------------------------------------------------------------------
# def receber_lsa(lsdb):
#     while True:
#         # print('Receber LSA:',lsdb)
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         sock.bind(("0.0.0.0", PORTA_LSA))
#         while True:
#             dados, _ = sock.recvfrom(4096)
#             lsa = json.loads(dados.decode())
#             print(f"[{ROTEADOR_ID}] Recebendo LSA: {lsa}")
#             origem = lsa["id"]
#             if origem not in lsdb or lsa["seq"] > lsdb[origem]["seq"]:
#                 lsdb[origem] = lsa
                
#             print(f"[{ROTEADOR_ID}] Recebendo LSA de {origem}: {lsa}")
            
#             time.sleep(5)  
# ----------------------------------------------------------------------

def receber_lsa(lsdb):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORTA_LSA))
    while True:
        dados, addr = sock.recvfrom(4096)  # Recebe dados e endereço do remetente
        sender_ip = addr[0]  # Extrai o IP do remetente
        lsa = json.loads(dados.decode())
        origem = lsa["id"]
        
        # Atualiza o LSDB apenas se o LSA for mais recente
        if origem not in lsdb or lsa["seq"] > lsdb[origem]["seq"]:
            lsdb[origem] = lsa
            # Encaminha o LSA para todos os vizinhos (exceto o remetente)
            for viz, (ip, _) in VIZINHOS.items():
                if ip != sender_ip:
                    sock.sendto(dados, (ip, PORTA_LSA))
                    print(f"[{ROTEADOR_ID}] Encaminhando LSA para {viz} ({ip})")
    
def verificaLSDB(lsdb):
    while True:
        if lsdb:
            print(f"[{ROTEADOR_ID}] LSDB atual:")
            for router_id, lsa in lsdb.items():
                print(f"Id:{router_id}: lsa:{lsa}")
        else:
            print(f"[{ROTEADOR_ID}] LSDB vazia.")
            
        time.sleep(5) 

def iniciar_threads():
    lsdb = {}
    
    t1 = threading.Thread(target=enviar_lsa)
    t2 = threading.Thread(target=receber_lsa, args=(lsdb,))
    t3 = threading.Thread(target=atualizar_tabela, args=(lsdb,))
    t4 = threading.Thread(target=verificaLSDB, args=(lsdb,))
    
    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    threading.Event().wait()

if __name__ == "__main__":
    print(f"[{ROTEADOR_ID}] Iniciado com vizinhos: {VIZINHOS}")
    iniciar_threads()