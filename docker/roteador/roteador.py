import threading
import time
import socket
import json
import os
import subprocess
from dijkstra import dijkstra
from script_teste.roteador import Roteador
import re

ROTEADOR_ID = os.getenv("ROTEADOR_ID")
ENDERECO_IP = os.getenv("ENDERECO_IP")
VIZINHOS = json.loads(os.getenv("VIZINHOS"))
VIZINHOS_ATIVOS = VIZINHOS.copy()

PORTA_LSA = 5000

def verifica_tcp(ip):
    try:
        # Tenta pingar o IP
        resultado = subprocess.run(f"ping -c 1 -W 0.1 {ip}", shell=True, check=True, text=True, capture_output=True)
        if resultado.returncode == 0:
            return True  # IP está acessível
        else:
            return False
    except subprocess.CalledProcessError:
        return False

    # # Se o ping falhou, executa traceroute
    # try:
    #     trace = subprocess.run(f"traceroute -n -w 1 -q 1 {ip}", shell=True, text=True, capture_output=True)
    #     hops = trace.stdout.strip().split('\n')

    #     # Pega o último IP válido (que não seja "*")
    #     for hop in reversed(hops):
    #         match = re.search(r'(\d+\.\d+\.\d+\.\d+)', hop)
    #         if match:
    #             router_id = match.group(1)
    #             router_id = f"roteador{(router_id.split('.')[-2])}"
    #             print(f"[!] Ping falhou, último roteador acessível: {router_id}")
    #             return False, router_id
    # except Exception as e:
    #     print(f"Erro ao executar traceroute: {e}")

    # return False, None

def verifica_vizinhos_inativos():
    inativos = []
    for roteador in list(VIZINHOS.keys()):
        retorno = verifica_tcp(VIZINHOS[roteador][0])
        if not retorno:
            inativos.append(roteador)
            print(f"[{ROTEADOR_ID}] Roteador {roteador} inativo.")
        else:
            print(f"[{ROTEADOR_ID}] Roteador {roteador} ativo.")
        
    return inativos

def verifica_vizinhos_ativos():
    inativos = []
    for roteador in list(VIZINHOS.keys()):
        retorno = verifica_tcp(VIZINHOS[roteador][0])
        if retorno:
            inativos.append(roteador)
            print(f"[{ROTEADOR_ID}] Roteador {roteador} ativo.")
        else:
            print(f"[{ROTEADOR_ID}] Roteador {roteador} inativo.")
        
    return inativos

def verifica_roteadores_inativos(lsdb):
    inativos = []
    
    for roteador, dados in lsdb.items():
        retorno = verifica_tcp(dados["ip"])
        if not retorno:
            inativos.append(roteador)
            print(f"[{ROTEADOR_ID}] Roteador {roteador} inativo.")
        else:
            print(f"[{ROTEADOR_ID}] Roteador {roteador} ativo.")
        
    return inativos

def rota_existe(destino):
    try:
        result = subprocess.run(f"ip route show {destino}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True
        return False
    except Exception as e:
        print(f"[{ROTEADOR_ID}] Erro ao verificar rota existente: {e}")
        return False

def atualizar_rota(tabela):
    for destino, prox_salto in tabela.items():
        destino = f"172.21.{int(destino.split('r')[-1]) - 1}.0/24"
        prox_salto = f"172.21.{int(prox_salto.split('r')[-1]) - 1}.2"
        
        if rota_existe(destino):
            print(f"[{ROTEADOR_ID}] Rota já existe. Atualizando...")
            subprocess.run(f"ip route del {destino}", shell=True, capture_output=True, text=True)
        
        comando_adicionar = f"ip route add {destino} via {prox_salto}"
        print(f"[{ROTEADOR_ID}] Executando: {comando_adicionar}")
        
        try:
            result = subprocess.run(comando_adicionar, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"[{ROTEADOR_ID}] Erro ao executar comando: {result.stderr.strip()}")
            else:
                print(f"[{ROTEADOR_ID}] Comando executado com sucesso: {result.stdout.strip()}")
        except Exception as e:
            print(f"[{ROTEADOR_ID}] Erro ao adicionar rota: {e}")

def atualizar_tabela(lsdb, inativos):
    while True:
        tabela = {}
        if lsdb:
            tabela = dijkstra(ROTEADOR_ID, lsdb, inativos)
        
        if tabela:
            print(f"[{ROTEADOR_ID}] Nova tabela de rotas:")
            for destino, prox_salto in tabela.items():
                print(f"  {destino} → via {prox_salto}")
            atualizar_rota(tabela)
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
                viz: {"ip": ip, "custo": custo} for viz, (ip, custo) in VIZINHOS_ATIVOS.items()
            },
            "seq": seq
        }

        print(f"[{ROTEADOR_ID}] Enviando LSA para: {list(VIZINHOS_ATIVOS.keys())}")
        
        mensagem = json.dumps(lsa).encode()
        for viz, (ip, _) in VIZINHOS_ATIVOS.items():
            sock.sendto(mensagem, (ip, PORTA_LSA))
        
        time.sleep(5)  # Intervalo de envio de LSAs (5 segundos)

def receber_lsa(lsdb):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", PORTA_LSA))
    while True:
        dados, addr = sock.recvfrom(4096)
        sender_ip = addr[0]
        lsa = json.loads(dados.decode())
        origem = lsa["id"]
        
        if origem not in lsdb or lsa["seq"] > lsdb[origem]["seq"]:
            lsdb[origem] = lsa
            for viz, (ip, _) in VIZINHOS.items():
                if ip != sender_ip:
                    sock.sendto(dados, (ip, PORTA_LSA))
                    print(f"[{ROTEADOR_ID}] Encaminhando LSA para {viz} ({ip})")

def verificar_vizinhos_ativos(inativos, lsdb):
    time.sleep(30)  # Ajuste o tempo de espera entre verificações
    
    while True:
        novos_ativos = verifica_vizinhos_ativos()
        novos_inativos = verifica_vizinhos_inativos()
        inativos.clear()  # Limpa a lista original, mantendo a referência
        inativos.extend(novos_inativos)  # Adiciona os novos valores

        # Remove vizinhos inativos do LSDB
        for inativo in novos_inativos:
            if inativo in VIZINHOS_ATIVOS:
                del VIZINHOS_ATIVOS[inativo]  # Remove do dicionário de vizinhos ativos
                
        for ativo in novos_ativos:
            if ativo not in VIZINHOS_ATIVOS:
                VIZINHOS_ATIVOS[ativo] = VIZINHOS[ativo]
                
        print(f"[{ROTEADOR_ID}] Vizinhos inativos: {inativos}")
        
        if novos_inativos or novos_ativos:
            print(f"[{ROTEADOR_ID}] Atualizando tabela de rotas...")
            
            tabela_atualizada = dijkstra(ROTEADOR_ID, lsdb, inativos)
            atualizar_rota(tabela_atualizada)
        
        time.sleep(10 if novos_inativos else 0.5)

def iniciar_threads():
    lsdb = {}
    inativos = []
    
    threads_lista = [
        threading.Thread(target=enviar_lsa),
        threading.Thread(target=receber_lsa, args=(lsdb,)),
        threading.Thread(target=atualizar_tabela, args=(lsdb, inativos)),
        threading.Thread(target=verificar_vizinhos_ativos, args=(inativos, lsdb)),
    ]
    
    for t in threads_lista:
        t.daemon = True
        t.start()

    threading.Event().wait()

if __name__ == "__main__":
    print(f"[{ROTEADOR_ID}] Iniciado com vizinhos: {VIZINHOS}")
    iniciar_threads()
