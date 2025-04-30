import socket
import json
import os
from classes.gerenciar_vizinhos import VizinhosManager

PORTA_LSA = 5000

class LSAManager:
    def __init__(self, vizinhos_manager:VizinhosManager):
        self.ROTEADOR_ID = os.getenv("ROTEADOR_ID")
        self.ENDERECO_IP = os.getenv("ENDERECO_IP")
        self.vizinhos_manager = vizinhos_manager
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.seq = 0

    def enviar_lsa(self, event):
        while not event.is_set():
            self.seq += 1
            lsa = {
                "id": self.ROTEADOR_ID,
                "ip": self.ENDERECO_IP,
                "vizinhos": {viz: {"ip": ip, "custo": custo} for viz, (ip, custo) in self.vizinhos_manager.VIZINHOS.items() if viz not in self.vizinhos_manager.vizinhos_inativos},
                "seq": self.seq
            }
            mensagem = json.dumps(lsa).encode()
            for viz, (ip, _) in self.vizinhos_manager.VIZINHOS.items():
                if viz not in self.vizinhos_manager.vizinhos_inativos:
                    self.sock.sendto(mensagem, (ip, PORTA_LSA))
            event.wait(0.5)

    def receber_lsa(self, lsdb, event):
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        recv_sock.bind(("0.0.0.0", PORTA_LSA))
        while not event.is_set():
            try:
                dados, addr = recv_sock.recvfrom(4096)
                sender_ip = addr[0]
                lsa = json.loads(dados.decode())
                origem = lsa["id"]
                # print(f"[{self.ROTEADOR_ID}] Recebendo LSA de {origem} ({sender_ip})")
                if origem not in lsdb or lsa["seq"] > lsdb[origem]["seq"]:
                    lsdb[origem] = lsa
                    for viz, (ip, _) in self.vizinhos_manager.VIZINHOS.items():
                        if ip != sender_ip and viz not in self.vizinhos_manager.vizinhos_inativos:
                            recv_sock.sendto(dados, (ip, PORTA_LSA))
                            print(f"[{self.ROTEADOR_ID}] Encaminhando LSA para {viz} ({ip})")
            except socket.timeout:
                continue
